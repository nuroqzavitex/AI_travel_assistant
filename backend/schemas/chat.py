from pydantic import BaseModel

class ChatRequest(BaseModel):
  message: str
  session_id: str | None = None

class ResumeRequest(BaseModel):
  """Request body for resuming after an interrupt (HITL)."""
  session_id: str
  response: str | dict = 'ok'

class ChatResponse(BaseModel):
  response: str
  session_id: str
  type: str = 'done'
  interrupt_data: dict | None = None