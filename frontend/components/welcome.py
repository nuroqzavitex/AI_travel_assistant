import streamlit as st

def render_welcome_screen():
  """Renders the welcome header and grid of clickable recommendation cards."""
  st.markdown(
    """
    <div style="text-align: center; padding: 40px 10px;">
      <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 10px;">Chào bạn, tôi có thể giúp gì?</h1>
      <p style="opacity: 0.7; font-size: 1.05rem; margin-bottom: 25px;">Hãy nhập yêu cầu lập kế hoạch du lịch của bạn hoặc chọn các gợi ý bên dưới.</p>
    </div>
    """,
    unsafe_allow_html=True
  )
  
  col1, col2 = st.columns(2)
  with col1:
    if st.button("✈️ Săn deal vé máy bay đi Đà Nẵng giá rẻ tuần sau", use_container_width=True):
      st.session_state.messages.append({"role": "user", "content": "Săn deal vé máy bay đi Đà Nẵng giá rẻ tuần sau"})
      st.rerun()
    if st.button("🏨 Tìm khách sạn tốt nhất ở Phú Quốc cho 3 ngày", use_container_width=True):
      st.session_state.messages.append({"role": "user", "content": "Tìm khách sạn tốt nhất ở Phú Quốc cho 3 ngày"})
      st.rerun()
  with col2:
    if st.button("☀️ Thời tiết tại Đà Lạt có thích hợp du lịch ngày mai không?", use_container_width=True):
      st.session_state.messages.append({"role": "user", "content": "Thời tiết tại Đà Lạt có thích hợp du lịch ngày mai không?"})
      st.rerun()
    if st.button("🗺️ Lên kế hoạch du lịch Nha Trang 4 ngày 3 đêm cho gia đình", use_container_width=True):
      st.session_state.messages.append({"role": "user", "content": "Lên kế hoạch du lịch Nha Trang 4 ngày 3 đêm cho gia đình"})
      st.rerun()