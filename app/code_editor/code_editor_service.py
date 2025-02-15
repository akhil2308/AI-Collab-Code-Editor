import json
import redis.asyncio as redis
from openai import AsyncOpenAI
from typing import Dict, List, Optional
from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status
from sqlalchemy.orm import Session
from redis.exceptions import RedisError

from app.database import SessionLocal
from app.auth_dependency import get_current_user_ws
from app.utils.helper import extract_all_code
from app.settings import OPENAI_API_KEY, OPENAI_API_MODEL, REDIS_HOST, REDIS_PORT, REDIS_DB
from app.code_session.code_session_crud import get_code_session_by_code_session_id
from app.code_session.code_session_crud import check_user_code_session_access, get_code_session_by_code_session_id

import logging
logger = logging.getLogger(__name__)

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

class ConnectionManager:
    def __init__(self):
        self.active_sessions: Dict[str, List[WebSocket]] = {}
        self.redis = redis_client

    async def connect(self, session_id: str, websocket: WebSocket):
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = []
        self.active_sessions[session_id].append(websocket)
        await self.redis.incr(f"code_session:{session_id}:connections")

    async def disconnect(self, session_id: str, websocket: WebSocket):
        content = None
        if session_id in self.active_sessions:
            content = await self.get_content(session_id)
            self.active_sessions[session_id].remove(websocket)
            count = await self.redis.decr(f"code_session:{session_id}:connections")
            if count <= 0:
                await self.redis.delete(f"code_session:{session_id}:connections")
                await self.redis.delete(f"code_session:{session_id}:content")
            if not self.active_sessions[session_id]:
                del self.active_sessions[session_id]
        
        return content

    async def broadcast(self, session_id: str, message: str, type: str = "update"):
        await self.redis.set(f"code_session:{session_id}:content", message)
        broadcast_message = {
            "type": type,
            "content": message
        }
        for connection in self.active_sessions.get(session_id, []):
            await connection.send_json(broadcast_message)


    async def get_content(self, session_id: str) -> str:
        content = await self.redis.get(f"code_session:{session_id}:content")
        if content is None:
            return ""
        return content.decode("utf-8")

manager = ConnectionManager()


async def code_session_websocket(
    websocket: WebSocket,
    code_session_id: str
    ):
    db = SessionLocal()
    try:
        await websocket.accept()
        
        user_id = await get_current_user_ws(websocket)
        access = check_user_code_session_access(db, user_id, code_session_id)
        if not access:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            logger.warning(f"Unauthorized access attempt by {user_id}")
            return
    
        code_session = get_code_session_by_code_session_id(db, code_session_id)
        if not code_session:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            logger.error(f"Missing session {code_session_id}")
            return
        
        try:
            initial_content = await manager.get_content(code_session_id)
            if not initial_content:
                initial_content = code_session.content or ""
                await manager.redis.set(f"code_session:{code_session_id}:content", initial_content)
        except RedisError as e:
            logger.error(f"Redis init failed: {e}")
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
            return
            
        content = {"type": "update", "content": initial_content}
        await websocket.send_json(content)
        await manager.connect(code_session_id, websocket)

        while True:
            data = await websocket.receive_text()
            """
            The data received from the client is a JSON string.
            {
                "type": "edit",
                "content": "your code here"
            }
            """
            data = json.loads(data)
            await manager.broadcast(code_session_id, data["content"])

    except WebSocketDisconnect:
        content = await manager.disconnect(code_session_id, websocket)
        if content:
            code_session.content = content
            db.commit()
    except Exception as e:
        logger.error(e,exc_info=True)
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
    finally:
        db.close()



async def get_code_content(code_session_id: str, db: Session) -> str:
    code = await manager.get_content(code_session_id)
    if not code:
        code_session = get_code_session_by_code_session_id(db, code_session_id)
        if not code_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Code session not found"
            )
        code = code_session.content or ""
        await manager.redis.set(f"code_session:{code_session_id}:content", code)
    return code


async def analyze_code_debugger(code_session_id: str, db: Session) -> str:
    code = await get_code_content(code_session_id, db)
    
    system_prompt = (
        "You are an expert code analyzer. Analyze the following code strictly for debugging purposes. "
        "Identify syntax errors, potential bugs, and suggest performance improvements. Provide your suggestions "
        "as a concise bullet list without additional commentary."
    )
    user_message = f"Please analyze the following code and provide debugging suggestions:\n\n{code}"

    try:
        response = await openai_client.chat.completions.create(
            model=OPENAI_API_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=500,
        )
    except Exception as e:
        logger.error(f"Debugging AI error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service error"
        )

    suggestions = response.choices[0].message.content
    return suggestions


async def generate_code_from_session(code_session_id: str, query: str, db: Session):
    code = await get_code_content(code_session_id, db)
    
    # Broadcast a lock message to disable editing during code generation
    await manager.broadcast(
        session_id=code_session_id,
        message="Code generation in progress. Editing is disabled.",
        type="lock"
    )
    
    system_prompt = (
        "You are an expert code generator. Based on the provided code and any additional instructions, "
        "generate a complete, self-contained, working code file. Your output must consist solely of the code "
        "with no extra commentary, and if modifications are requested, produce the entire revised code."
    )
    if query:
        user_message = f"Code:\n{code}\n\nInstructions: {query}"
    else:
        user_message = f"Code:\n{code}\n\nPlease generate the complete, working code file."
    
    try:
        response = await openai_client.chat.completions.create(
            model=OPENAI_API_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=2048,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service error"
        )

    generated_code = response.choices[0].message.content
    extracted_code = extract_all_code(generated_code)
    await manager.broadcast(code_session_id, extracted_code)
    