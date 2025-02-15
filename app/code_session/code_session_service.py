from sqlalchemy.orm import Session
from app.code_session.code_session_crud import create_code_session, update_code_session, add_code_session_user \
    ,change_code_session_user_access, get_code_sessions_by_user
from app.code_session.code_session_schema import CodeSessionCreateRequest, CodeSessionUpdateRequest, CodeSessionUserAccessInviteRequest \
    ,CodeSessionUserAccessChangeRequest


def create_code_session_service(db: Session, session_in: CodeSessionCreateRequest):
    # Create a new code session
    code_session = create_code_session(
        db=db,
        code_session_name=session_in.code_session_name,
        content_type=session_in.content_type,
        content=session_in.content,
        created_by=session_in.created_by
    )
    # Provide access to the user who created the code session
    add_code_session_user(
        db=db,
        user_id=code_session.created_by,
        code_session_id=code_session.code_session_id,
        role="owner"
    )
    return code_session

def update_code_session_service(db: Session, code_session_id: str, session_update: CodeSessionUpdateRequest):
    return update_code_session(
        db=db,
        code_session_id=code_session_id,
        code_session_name=session_update.code_session_name,
        content_type=session_update.content_type,
        content=session_update.content,
        updated_by=session_update.updated_by
    )
    
def invite_code_session_user_service(db: Session, invite: CodeSessionUserAccessInviteRequest):
    return add_code_session_user(
        db=db,
        user_id=invite.user_id,
        code_session_id=invite.code_session_id,
        role=invite.role
    )

def change_code_session_user_access_service(db: Session, access_change: CodeSessionUserAccessChangeRequest):
    return change_code_session_user_access(
        db=db,
        user_id=access_change.user_id,
        code_session_id=access_change.code_session_id,
        new_role=access_change.new_role
    )


def list_user_code_sessions_service(db: Session, user_id: str):
    return get_code_sessions_by_user(db, user_id)