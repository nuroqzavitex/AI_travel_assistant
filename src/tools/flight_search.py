from langchain_core.tools import tool
from serpapi import GoogleSearch
from config.settings import SERPAPI_API_KEY
import json

@tool
def search_flights(departure_id: str, arrival_id: str, outbound_date: str) -> str:
  # Dùng google search thông qua serpapi để tìm kiếm thông tin chuyến bay

  # Tạo param cho serpapi
  params = {
    'engine': 'google_flights',
    'departure_id': departure_id,
    'arrival_id': arrival_id,
    'outbound_date': outbound_date,
    'currency': 'VND',
    'hl': 'vi',
    'type': '2', # 2: chuyến bay một chiều, 3: chuyến bay khứ hồi
    'api_key': SERPAPI_API_KEY
  }

  # Gọi API của serpapi
  try:
    search = GoogleSearch(params)
    results = search.get_dict()
  except Exception as e:
    return json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False)
  
  # Xử lí kết quả
  flights = []
  for flight in results.get('best_flights', []) + results.get('other_flights', []):
    segments = flight.get('flights', [])
    first = segments[0] if segments else {}
    last = segments[-1] if segments else {}
    flights.append({
      'price': flight.get('price', 0),
      'total_duration': flight.get('total_duration', 0),
      'airline': first.get('airline', ''),
      'flight_number': first.get('flight_number', ''),
      'departure_time': first.get('departure_airport', {}).get('time', ''),
      'arrival_time': last.get('arrival_airport', {}).get('time', ''),
      'departure_airport': first.get('departure_airport', {}).get('name', ''),
      'arrival_airport': last.get('arrival_airport', {}).get('name', ''),
      'stops': len(segments) - 1
    })

  return json.dumps({
    'status': 'success',
    'total': len(flights),
    'flights': flights
  }, ensure_ascii=False)