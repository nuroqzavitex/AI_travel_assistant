from pydantic import BaseModel

class SessionInfo(BaseModel):
  session_id: str
  title: str
  message_count: int

class SessionMessage(BaseModel):
  role: str
  content: str

class SessionDetail(BaseModel):
  messages: list[SessionMessage] = []