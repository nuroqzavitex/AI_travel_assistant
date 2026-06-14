import streamlit as st
from api_client import get_sessions, get_session_messages, delete_session

def render_sidebar():
  """Renders the session history and sidebar actions."""
  sessions = get_sessions()

  st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
      <span style="font-size: 24px;">🤖</span>
      <h3 style="margin: 0; font-weight: 700;">TRAVEL AGENT</h3>
    </div>
    """,
    unsafe_allow_html=True
  )

  # New chat button
  if st.sidebar.button("➕ Cuộc trò chuyện mới", use_container_width=True, type="primary"):
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.interrupt_data = None
    st.session_state.trigger_resume = False
    st.rerun()

  st.sidebar.markdown("---")
  st.sidebar.markdown("**LỊCH SỬ TRÒ CHUYỆN**")

  # List active sessions
  if not sessions:
    st.sidebar.info("Chưa có cuộc trò chuyện nào.")
  else:
    for s in sessions:
      sid = s["session_id"]
      title = s["title"]
      msg_count = s.get("message_count", 0)
      
      is_active = (st.session_state.session_id == sid)
      btn_label = f"{'⭐ ' if is_active else '💬 '}{title} ({msg_count})"
      
      col1, col2 = st.sidebar.columns([8, 2])
      
      if col1.button(btn_label, key=f"sel_{sid}", use_container_width=True):
        st.session_state.session_id = sid
        st.session_state.interrupt_data = None
        st.session_state.trigger_resume = False
        st.session_state.messages = get_session_messages(sid)
        st.rerun()
        
      if col2.button("🗑️", key=f"del_{sid}", help="Xóa cuộc trò chuyện này"):
        delete_session(sid)
        if st.session_state.session_id == sid:
          st.session_state.session_id = None
          st.session_state.messages = []
          st.session_state.interrupt_data = None
          st.session_state.trigger_resume = False
        st.rerun()