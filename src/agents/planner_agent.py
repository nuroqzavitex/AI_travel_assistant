from langchain_core.messages import SystemMessage, AIMessage 
from pydantic import BaseModel, Field
from src.services.llm_service import get_llm
from config.constants import CITY_IATA, IATA_CITY
from config.prompts import PLANNER_AGENT_PROMPT
from datetime import datetime, timedelta

class TripPlan(BaseModel):
  steps: list[str] = Field(
    description="Danh sách các bước cần thực hiện. Ví dụ ['find_flights', 'find_hotels', 'check_weather']"
    )
  constraints: dict = Field(
    description='Các ràng buộc: budget, days, destination, departure_date, return_date, v.v.'
  )

  goal: str = Field(
    description='Mô tả mục tiêu tổng thể của strip'
  )

def _to_iata(city_name: str) -> str:
  # Chuyển tên thành iata code nếu có mapping
  if not city_name:
    return city_name
  if len(city_name) == 3 and city_name.isupper():
    return city_name
  key = city_name.lower().strip()
  if key in CITY_IATA:
    return CITY_IATA[key]
  for city, code in CITY_IATA.items():
    if city in key or key in city:
      return code
  return city_name

def _iata_to_city(code: str) -> str:
  return IATA_CITY.get(code, code)

STEP_LABELS = {
  'find_flights': 'Tìm vé máy bay',
  'find_hotels': 'Tìm khách sạn',
  'check_weather': 'Tra cứu thời tiết',
  'search_info': 'Tìm kiếm thông tin du lịch'
}

def planner_node(state: dict) -> dict:
  # Phân rã yêu cầu thành các bước cụ thể
  user_message = state['messages'][-1].content
  current_date = datetime.now().strftime('%Y-%m-%d')

  print(f'[PlannerAgent] Planning for: {user_message}')

  llm = get_llm().with_structured_output(TripPlan)

  recent_messages = state['messages'][-6:] # Lấy 6 tin nhắn gần nhất để cung cấp ngữ cảnh

  try:
    plan = llm.invoke([
      SystemMessage(content = PLANNER_AGENT_PROMPT.format(
        current_date = current_date
      )),
      *recent_messages,
    ])
    plan_dict = plan.model_dump()
    constraints = plan_dict.get('constraints', {})
    steps = plan_dict.get('steps', [])

    # Kiểm tra thiếu thông tin quan trọng
    needs_flights_or_hotels = any(
      s in steps for s in ['find_flights', 'find_hotels']
    )
    has_destination = bool(constraints.get('destination'))

    if needs_flights_or_hotels and not has_destination:
      missing = []
      if not constraints.get('destination'):
        missing.append('điểm đến')
      if not constraints.get('origin'):
        missing.append('điểm đi')
      
      ask_msg = (
        f"Bạn muốn tìm vé máy bay, nhưng mình cần thêm thông tin:\n\n"
        f"📌 Thiếu: **{', '.join(missing)}**\n\n"
        f"Ví dụ: *\"Tìm vé rẻ nhất từ HCM đi Đà Nẵng ngày 15/3\"*\n\n"
        f"Bạn bổ sung giúp mình nhé!"
      )
      print(f'[Planner] Missing info: {missing} -> asking user')
      return {
        'messages': [AIMessage(content = ask_msg)],
        'current_step': 'planner'
      }
    
    if constraints.get('origin'):
      raw = str(constraints['origin'])
      if len(raw) == 3 and raw.isupper():
        constraints['origin_name'] = _iata_to_city(raw)
      else:
        constraints['origin_name'] = raw
      constraints['origin'] = _to_iata(raw)

    if constraints.get('destination'):
      raw = str(constraints['destination'])
      if len(raw) == 3 and raw.isupper():
        constraints['destination_name'] = _iata_to_city(raw)
      else:
        constraints['destination_name'] = raw
      constraints['destination'] = _to_iata(raw)

    if not constraints.get('departure_date') and any(
      s in steps for s in ['find_flights', 'find_hotels']
    ):
      tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
      constraints['departure_date'] = tomorrow
      print(f'[Planner] No date specified, using tomorrow: {tomorrow}')

    plan_dict['constraints'] = constraints

    print(f'[Planner] Plan: {plan_dict}')

    return {
      'plan': plan_dict,
      'current_step_index': 0,
      'current_step': 'planner'
    }
  
  except Exception as e:
    print(f'[Planner] Error: {e}')
    return {
      'plan': {
        'steps': ['find_flights'],
        'constraints': {},
        'goal': user_message
      },
      'current_step_index': 0,
      'current_step': 'planner'
    }






