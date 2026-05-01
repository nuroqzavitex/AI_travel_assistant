from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.services.llm_service import get_llm
from src.tools.tavily_search import search_web
from config.prompts import INFO_AGENT_PROMPT

info_react_agent = create_react_agent(
  model = get_llm(),
  tools = [search_web],
  prompt = INFO_AGENT_PROMPT
)

def info_agent_node(state: dict) -> dict:
  plan = state.get('plan', {})
  constraints = plan.get('constraints', {}) if isinstance(plan, dict) else {}
  goal = plan.get('goal', '')

  destination = constraints.get('destination_name', constraints.get('destination', ''))
  days = constraints.get('days', '')

  # Tạo search query từ plan
  if destination:
    task_msg = f"Tìm kiếm thông tin du lịch {destination}"
    if days:
      task_msg += f" trong {days} ngày"
    task_msg += f'. Bao gồm cả các tips, địa điểm nổi bật, ẩm thực và kinh nghiệm du lịch.'
  else:
    task_msg = f'Tìm thông tin du lịch: {goal}'

  print(f'[Info Agent] Task: {task_msg}')

  results = info_react_agent.invoke(
    {'messages': [HumanMessage(content=task_msg)]}
  )

  info_results = results['messages'][-1].content if results['messages'] else '' # Lấy content của message cuối cùng làm kết quả thông tin
  print(f'[Info Agent] Results: {info_results[:100]}...')

  return {
    'search_info': info_results,
    'current_step': 'info_agent',
    'completed_agents': state.get('completed_agents', []) + ['info_agent'],
  }