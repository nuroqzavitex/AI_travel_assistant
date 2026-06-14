import streamlit as st

def render_header():
  """Renders the main layout header."""
  st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 15px; padding-bottom: 15px; border-bottom: 1px solid rgba(128,128,128,0.2);">
      <div style="width: 40px; height: 40px; border-radius: 8px; background-color: #0d9488; display: flex; align-items: center; justify-content: center; font-size: 20px; color: white;">
        ✈️
      </div>
      <div>
        <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700;">Travel AI Assistant</h2>
        <span style="font-size: 0.8rem; opacity: 0.7;">Trợ lý du lịch thông minh, lập kế hoạch và săn deal ưu đãi</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True
  )
  st.write("")

def render_messages():
  """Renders all messages from the session state."""
  for msg in st.session_state.messages:
    role = msg.get("role")
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
      st.markdown(msg.get("content"))

def render_interrupt_ui():
  """Renders the HITL interrupt card if present in state."""
  if not st.session_state.interrupt_data:
    return
    
  plan_msg = st.session_state.interrupt_data.get("content", "Vui lòng xác nhận đề xuất.")
  with st.chat_message("assistant", avatar="🤖"):
    st.markdown(plan_msg)
    
    st.write("")
    st.markdown("⚠️ **Xác nhận kế hoạch trên:**")
    
    col_conf, col_mod = st.columns([1, 4])
    
    if col_conf.button("✓ Xác nhận", key="confirm_plan_btn", type="primary", use_container_width=True):
      # 1. Store plan as assistant's response
      st.session_state.messages.append({"role": "assistant", "content": plan_msg})
      # 2. Store user confirmation
      st.session_state.messages.append({"role": "user", "content": "✓ Xác nhận"})
      # 3. Trigger resume
      st.session_state.trigger_resume = True
      # 4. Clear interrupt status
      st.session_state.interrupt_data = None
      st.rerun()
      
    if col_mod.button("✎ Thay đổi", key="modify_plan_btn", use_container_width=True):
      # Store plan and cancellation message
      st.session_state.messages.append({
        "role": "assistant",
        "content": plan_msg + "\n\n✎ *Kế hoạch đã bị hủy. Hãy nhập yêu cầu mới hoặc sửa lại yêu cầu trước.*"
      })
      # Reset session ID to allow user to make updates fresh
      st.session_state.session_id = None
      st.session_state.interrupt_data = None
      st.rerun()