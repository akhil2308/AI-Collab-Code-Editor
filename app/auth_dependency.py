from fastapi import Depends, HTTPException, status, WebSocket, Cookie, status
from fastapi.websockets import WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db 
from app.user.user_model import User
from app.user.user_crud import get_user_by_user_id
from app.user.user_auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = get_user_by_user_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def get_current_user_ws(websocket: WebSocket) -> str:

    cookies = websocket.cookies
    session_token = cookies.get("jwt_token")

    if not session_token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect("Missing authentication cookie")

    try:
        payload = decode_access_token(session_token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")
        return user_id
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect(f"Invalid token: {str(e)}")
