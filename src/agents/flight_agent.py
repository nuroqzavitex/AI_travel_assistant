from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.tools.flight_search import search_flights
from src.services.llm_service import get_llm
from config.prompts import FLIGHT_AGENT_PROMPT
import json

# Tạo react agent với tool search_flights
flight_react_agent = create_react_agent(
  llm = get_llm(),
  tools = [search_flights],
  prompt = FLIGHT_AGENT_PROMPT
)

def flight_agent_node(state: dict) -> str:
  # Đưa react agent thành một node trong graph
  # Xây dựng messages cho agent
  plan = state.get('plan', {})
  constraints = plan.get('constraints', {}) if isinstance(plan, dict) else {}

  task_msg = (
    f"Tìm vé máy bay từ {constraints.get('origin', 'N/A')} "
    f"đến {constraints.get('destination', 'N/A')} "
    f"ngày {constraints.get('departure_date', 'N/A')}."
  )

  if constraints.get('budget'):
    task_msg += f" Budget tối đa: {constraints['budget']} VND."
  
  print(f'[Flight Agent] Task: {task_msg}')

  results = flight_react_agent.invoke(
    {'messages': [HumanMessage(content=task_msg)]}
  )

  # Trích xuất fligt_results từ kết quả agent
  flight_results = []
  for msg in results['messages']:
    if hasattr(msg, 'content') and msg.content:
      try:
        data = json.loads(msg.content)
        if isinstance(data, dict) and 'flights' in data:
          flight_results = data['flights']
          break
      except (json.JSONDecodeError, TypeError):
        continue

  # Sắp xếp theo giá
  if flight_results:
    flight_results = sorted(flight_results, key=lambda x: x.get('price', 0))[:10]
  
  print (f'[Flight Agent] Found {len(flight_results)} flights')

  return {
    'flights_results': flight_results,
    'current_step': 'flight_agent',
    'completed_agents': state.get('completed_agents', []) + ['flight_agent'],
  }