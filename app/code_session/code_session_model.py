import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CodeSession(Base):
    id                  = Column(Integer, primary_key=True, index=True)
    code_session_id     = Column(String, unique=True, index=True, nullable=False)
    code_session_name   = Column(String, nullable=False)
    content_type        = Column(String, nullable=False)
    content             = Column(Text, nullable=True)
    created_at          = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at          = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by          = Column(String, nullable=False)
    updated_by          = Column(String, nullable=True)
    
    __tablename__ = 'code_sessions'


class CodeSessionUserAccess(Base):
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(String, nullable=False)
    code_session_id = Column(String, nullable=False)
    role            = Column(String, nullable=False) # 'owner', 'editor', or 'viewer'

    __tablename__ = 'code_session_user_access'