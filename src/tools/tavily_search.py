from langchain_core.tools import tool
from tavily import TavilyClient
from config.settings import TAVILY_API_KEY

@tool
def search_web(query: str) -> str:
  # Tìm kiếm thông tin du lịch trên web thông qua Tavily
  # Ví dụ: 'kinh nghiệm du lịch Đà Nẵng 3 ngày'

  if not TAVILY_API_KEY:
    return 'Lỗi: Chưa cấu hình TAVILY_API_KEY'
  
  try: 
    client = TavilyClient(api_key = TAVILY_API_KEY)
    response = client.search(
      query=query,
      search_depth='basic', # search nhanh rẻ hơn 
      max_results=5,
      include_answer=True # tóm tắt câu trả lời từ kết quả tìm kiếm
    )

    # Trả answer tóm tắt + top results
    parts = []

    if response.get('answer'): # nếu có tóm tắt thì trả về
      parts.append(f'Tóm tắt: {response['answer']}\n')

    results = response.get('results', [])
    if results:
      parts.append('Nguồn tham khảo')
      for i, r in enumerate(results[:5], 1):
        title = r.get('title', 'N/A')
        snippet = r.get('content', '')[:200]
        url = r.get('url', '')
        parts.append(f'{i}. **{title}**\n {snippet}\n {url}\n')
    return '\n'.join(parts) if parts else 'Không tìm thấy kết quả phù hợp.'
  except Exception as e:
    return f'Lỗi khi tìm kiếm: {str(e)}'