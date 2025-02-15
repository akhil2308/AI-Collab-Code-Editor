from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth_dependency import get_current_user, User
from app.user.user_schema import UserCreateRequest, UserLoginRequest, UserCreateResponse, UserListResponse
from app.user.user_service import register_user, login_user, get_all_users_service
from app.user.user_auth import create_access_token

import logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=UserCreateResponse)
def register(request: UserCreateRequest, db: Session = Depends(get_db)):
    user = register_user(db, request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    return user

@router.post("/login")
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    user = login_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": user.user_id})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }


@router.get("/", response_model=list[UserListResponse])
def get_all_users_router(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    sessions = get_all_users_service(db)
    return sessions