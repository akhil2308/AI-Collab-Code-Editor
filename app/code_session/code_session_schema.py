from pydantic import BaseModel
from typing import Optional, Literal

# CodeSession schema
class CodeSessionCreateRequest(BaseModel):
    code_session_name: str
    content_type: Literal["python", "javascript"]
    content: Optional[str] = None
    created_by: Optional[str] = None

class CodeSessionUpdateRequest(BaseModel):
    code_session_name: Optional[str] = None
    content_type: Optional[Literal["python", "javascript"]] = None
    content: Optional[str] = None
    updated_by: Optional[str] = None

class CodeSessionResponse(BaseModel):
    code_session_id: str
    code_session_name: str
    content_type: str
    content: Optional[str] = None
    created_by: str
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


# CodeSessionUserAccess schema
class CodeSessionUserAccessInviteRequest(BaseModel):
    user_id: str
    code_session_id: str
    role: Literal["owner", "editor", "viewer"]

class CodeSessionUserAccessChangeRequest(BaseModel):
    user_id: str
    code_session_id: str
    new_role: Literal["owner", "editor", "viewer"]

class CodeSessionUserAccessResponse(BaseModel):
    id: int
    user_id: str
    code_session_id: str
    role: str

    class Config:
        from_attributes = True

class CodeSessionWithRoleResponse(BaseModel):
    id: int
    code_session_id: str
    code_session_name: str
    content_type: str
    role: str
    created_by: str
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True
