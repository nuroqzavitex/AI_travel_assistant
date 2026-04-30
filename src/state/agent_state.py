from typing import Annotated, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict, total=False):
  # Core
  messages: Annotated[list, add_messages]
  intent: str # ý định của user
  current_step: str
  error: str | None

  # Multi-Agent: Planner
  plan: dict # {"steps": [...], "constraints": {...}, "goal": "..."}
  current_step_index: int

  # Multi-Agent: Supervisor
  next_agent: str
  reasoning: str # giải thích tại sao chọn agent tiếp theo
  completed_agents: list[str] 

  # Multi-Agent: Agent results
  flight_results: list[dict[str, Any]]
  hotel_results: list[dict[str, Any]]
  weather_info: str
  search_info: str

  # Multi-Agent: Reflection
  reflection_issues: list[str] # danh sách các vấn đề 
  suggested_fixes: list[str]
  needs_revision: bool
  revision_count: int # số lần làm lại
  plan_modifications: dict # danh sách các sửa đổi 
  agents_to_retry: list[str] # danh sách các agent cần chạy lại sau khi sửa kế hoạch
