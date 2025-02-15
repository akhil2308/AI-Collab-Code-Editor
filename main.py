import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.health.health_router import router as health_router
from app.user.user_router import router as user_router
from app.code_session.code_session_router import router as code_session_router
from app.code_editor.code_editor_router import router as code_editor_router
from app.ui.ui_router import router as ui_router
from app.database import engine
from app.settings import logging_config,  ALLOWED_HOSTS

import logging
logging.config.dictConfig(logging_config)

# Create tables
from app.user import user_model
from app.code_session import code_session_model

user_model.Base.metadata.create_all(bind=engine)
code_session_model.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI-Collab-Code-Editor",
    description="",
    version="1.0.0",
    docs_url="/docs",
    openapi_url = "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/v1/api/health", tags=["Health"])
app.include_router(user_router, prefix="/v1/api/user", tags=["User"])
app.include_router(code_session_router, prefix="/v1/api/code-sessions", tags=["Code Sessions"])
app.include_router(code_editor_router, prefix="/v1/api/code-editor", tags=["Code Editor"])
app.include_router(ui_router, prefix="", tags=["UI"])

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True)