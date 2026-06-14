import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import chat, sessions, health

@asynccontextmanager
async def lifespan(app: FastAPI):
  """Application lifespan — startup & shutdown hooks."""
  # Startup: có thể khởi tạo resources ở đây
  yield
  # Shutdown: giải phóng resources

def create_app() -> FastAPI:
  app = FastAPI(
    title = 'AI Travel Assistant',
    version = '1.0.0',
    lifespan = lifespan
  )

  # CORS middleware
  _default_origins = ['http://localhost:5713', 'http://localhost:3000']
  _env_origins = os.getenv('CORS_ORIGINS')
  cors_origins = (
    [o.strip() for o in _env_origins.split(",") if o.strip()]
    if _env_origins
    else _default_origins
  )

  app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

  # Routers
  app.include_router(chat.router)
  app.include_router(sessions.router)
  app.include_router(health.router)

  return app

app = create_app()