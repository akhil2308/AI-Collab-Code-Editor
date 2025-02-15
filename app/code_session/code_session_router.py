from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth_dependency import get_current_user, User
from app.code_session.code_session_service import create_code_session_service, update_code_session_service, invite_code_session_user_service, \
    change_code_session_user_access_service, list_user_code_sessions_service
from app.code_session.code_session_schema import CodeSessionCreateRequest, CodeSessionUpdateRequest, CodeSessionUserAccessInviteRequest, \
    CodeSessionUserAccessChangeRequest, CodeSessionResponse, CodeSessionUserAccessResponse, CodeSessionWithRoleResponse
from app.code_session.code_session_crud import get_code_session_user_by_user_id

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=CodeSessionResponse)
def create_code_session_router(
    session_in: CodeSessionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    session_in.created_by = current_user.user_id
    session_obj = create_code_session_service(db, session_in)
    if not session_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to create code session")
    return session_obj


@router.put("/{code_session_id}", response_model=CodeSessionResponse)
def update_code_session_router(
    code_session_id: str, 
    session_update: CodeSessionUpdateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    session_update.updated_by = current_user.user_id
    session_obj = update_code_session_service(db, code_session_id, session_update)
    if not session_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code session not found")
    return session_obj


@router.post("/invite", response_model=CodeSessionUserAccessResponse)
def invite_user_to_session_router(
    invite: CodeSessionUserAccessInviteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    owner = get_code_session_user_by_user_id(db, current_user.user_id, invite.code_session_id, "owner")
    if not owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not the owner of this code session")
    
    access = invite_code_session_user_service(db, invite)
    if not access:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to invite user")
    return access


@router.put("/change-access", response_model=CodeSessionUserAccessResponse)
def change_user_access_router(
    access_change: CodeSessionUserAccessChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    owner = get_code_session_user_by_user_id(db, current_user.user_id, access_change.code_session_id, "owner")
    if not owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not the owner of this code session")
    
    access = change_code_session_user_access_service(db, access_change)
    if not access:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Access record not found")
    return access


@router.get("/code-sessions", response_model=list[CodeSessionWithRoleResponse])
def list_code_sessions_router(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    sessions = list_user_code_sessions_service(db, current_user.user_id)
    return sessions