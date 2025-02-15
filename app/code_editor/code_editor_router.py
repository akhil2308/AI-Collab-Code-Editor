import redis
import json
from fastapi import APIRouter, WebSocket, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth_dependency import get_current_user_ws, get_current_user
from app.code_editor.code_editor_service import code_session_websocket ,analyze_code_debugger, generate_code_from_session
from app.code_editor.code_editor_schema import DebuggerRequest, CodeGeneratorRequest


router = APIRouter() 


@router.websocket("/ws/{code_session_id}")
async def code_session_websocket_router(
    websocket: WebSocket,
    code_session_id: str,
    ):
    await code_session_websocket(websocket, code_session_id)


@router.post("/ai/code-debugger")
async def debugger_endpoint(
    request: DebuggerRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    # need to check if user has access to code session
    suggestions = await analyze_code_debugger(request.code_session_id, db)
    return {"suggestions": suggestions}


@router.post("/ai/code-generator")
async def code_generator_endpoint(
    request: CodeGeneratorRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    await generate_code_from_session(request.code_session_id, request.query, db)