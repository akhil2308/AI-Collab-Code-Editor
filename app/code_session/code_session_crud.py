import uuid
from sqlalchemy.orm import Session
from app.code_session.code_session_model import CodeSession, CodeSessionUserAccess

def create_code_session(db: Session, code_session_name: str, content_type: str, content: str, created_by: str):
    new_session = CodeSession(
        code_session_id=str(uuid.uuid4()),
        code_session_name=code_session_name,
        content_type=content_type,
        content=content,
        created_by=created_by,
        updated_by=created_by
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_code_session_by_code_session_id(db: Session, code_session_id: str):
    return db.query(CodeSession).filter(CodeSession.code_session_id == code_session_id).first()

def update_code_session(db: Session, code_session_id: str, code_session_name: str = None, content_type: str = None, content: str = None, updated_by: str = None):
    session_obj = db.query(CodeSession).filter(CodeSession.code_session_id == code_session_id).first()
    if not session_obj:
        return None
    if code_session_name is not None:
        session_obj.code_session_name = code_session_name
    if content_type is not None:
        session_obj.content_type = content_type
    if content is not None:
        session_obj.content = content
    if updated_by is not None:
        session_obj.updated_by = updated_by
    db.commit()
    db.refresh(session_obj)
    return session_obj


def add_code_session_user(db: Session, user_id: str, code_session_id: str, role: str):
    access = CodeSessionUserAccess(
        user_id=user_id,
        code_session_id=code_session_id,
        role=role
    )
    db.add(access)
    db.commit()
    db.refresh(access)
    return access

def change_code_session_user_access(db: Session, user_id: str, code_session_id: str, new_role: str):
    access = db.query(CodeSessionUserAccess).filter(
        CodeSessionUserAccess.user_id == user_id,
        CodeSessionUserAccess.code_session_id == code_session_id
    ).first()
    if not access:
        return None
    access.role = new_role
    db.commit()
    db.refresh(access)
    return access

def get_code_session_user_by_user_id(db: Session, user_id: str, code_session_id: str, role: str):
    return db.query(CodeSessionUserAccess).filter(
        CodeSessionUserAccess.user_id == user_id,
        CodeSessionUserAccess.code_session_id == code_session_id,
        CodeSessionUserAccess.role == role
    ).first()

def check_user_code_session_access(db: Session, user_id: str, code_session_id: str, role: list = ["owner", "editor"]):
    return db.query(CodeSessionUserAccess).filter(
        CodeSessionUserAccess.user_id == user_id,
        CodeSessionUserAccess.code_session_id == code_session_id,
        CodeSessionUserAccess.role.in_(role)
    ).first()

def get_code_sessions_by_user(db: Session, user_id: str):
    results = (
        db.query(
            CodeSession.id,
            CodeSession.code_session_id,
            CodeSession.code_session_name,
            CodeSession.content_type,
            CodeSession.created_by,
            CodeSession.updated_by,
            CodeSessionUserAccess.role
        )
          .join(
              CodeSessionUserAccess,
              CodeSession.code_session_id == CodeSessionUserAccess.code_session_id
          )
          .filter(CodeSessionUserAccess.user_id == user_id)
          .all()
    )
    return results
