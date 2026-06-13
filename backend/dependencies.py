from __future__ import annotations
from functools import lru_cache
from langgraph.graph.state import CompiledStateGraph
from backend.services.session_store import SessionStore
from src.graphs.main_graph import travel_agent

# Singleton instances

@lru_cache(maxsize = 1)
def _get_session_store() -> SessionStore:
  return SessionStore()

def get_session_store() -> SessionStore:
  return _get_session_store()

def get_graph() -> CompiledStateGraph:
  return travel_agent()