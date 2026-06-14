import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def get_sessions():
  """Fetch all sessions from backend."""
  try:
    response = requests.get(f"{BACKEND_URL}/api/sessions", timeout=5)
    if response.status_code == 200:
      return response.json()
  except Exception:
    pass
  return []

def get_session_messages(session_id):
  """Fetch messages of a specific session."""
  try:
    response = requests.get(f"{BACKEND_URL}/api/sessions/{session_id}", timeout=5)
    if response.status_code == 200:
      data = response.json()
      return data.get("messages", [])
  except Exception as e:
    st.error(f"Không thể tải tin nhắn: {e}")
  return []

def delete_session(session_id):
  """Delete a session from backend."""
  try:
    requests.delete(f"{BACKEND_URL}/api/sessions/{session_id}", timeout=5)
  except Exception as e:
    st.error(f"Không thể xóa phiên trò chuyện: {e}")

def send_message_stream(message, session_id):
  """Send user message and request stream response."""
  url = f"{BACKEND_URL}/api/chat/stream"
  payload = {"message": message, "session_id": session_id}
  try:
    response = requests.post(url, json=payload, stream=True, timeout=30)
    response.raise_for_status()
    return response
  except Exception as e:
    st.error(f"Không thể kết nối với Backend: {e}")
    return None

def resume_message_stream(session_id, response_val="ok"):
  """Resume stream response after interrupt."""
  url = f"{BACKEND_URL}/api/chat/stream/resume"
  payload = {"session_id": session_id, "response": response_val}
  try:
    response = requests.post(url, json=payload, stream=True, timeout=30)
    response.raise_for_status()
    return response
  except Exception as e:
    st.error(f"Không thể tiếp tục cuộc trò chuyện: {e}")
    return None