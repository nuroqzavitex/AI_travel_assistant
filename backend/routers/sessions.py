from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from backend.dependencies import get_session_store
from backend.schemas.session import DeleteResponse, SessionInfo, SessionDetail
from backend.services.session_store import SessionStore

router = APIRouter(prefix = 'api/sessions', tags = ['sessions'])

@router.get('', response_model = list[SessionInfo])
async def list_sessions(store: SessionStore = Depends(get_session_store)) -> list[SessionInfo]:
  return store.list_all()

@router.get('/{session_id}', response_model = SessionDetail)
async def get_session(session_id: str, store: SessionStore = Depends(get_session_store)) -> SessionDetail:
  if not store.exists(session_id):
    raise HTTPException(status_code = 404, detail = 'Session not found')
  return SessionDetail(messages = store.get_messages(session_id))

@router.delete('/{session_id}', response_model = DeleteResponse)
async def delete_session(session_id: str, store: SessionStore = Depends(get_session_store)) -> DeleteResponse:
  store.delete(session_id)
  return DeleteResponse()