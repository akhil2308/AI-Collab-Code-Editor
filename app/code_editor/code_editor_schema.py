from pydantic import BaseModel
from typing import Optional

class DebuggerRequest(BaseModel):
    code_session_id: str

class CodeGeneratorRequest(BaseModel):
    code_session_id: str
    query: Optional[str] = ""
