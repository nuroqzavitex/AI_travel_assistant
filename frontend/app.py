import streamlit as st
import json

# Configure page settings (MUST be called first in Streamlit)
st.set_page_config(
  page_title="AI Travel Deal Hunter",
  page_icon="🤖",
  layout="wide",
  initial_sidebar_state="expanded"
)

# Import local modules
from styles import inject_styles
from api_client import send_message_stream, resume_message_stream
from components.sidebar import render_sidebar
from components.welcome import render_welcome_screen
from components.chat import render_header, render_messages, render_interrupt_ui

# Inject CSS styles
inject_styles()

# ── Session State Initialization ──────────────────────
if "session_id" not in st.session_state:
  st.session_state.session_id = None
if "messages" not in st.session_state:
  st.session_state.messages = []
if "interrupt_data" not in st.session_state:
  st.session_state.interrupt_data = None
if "trigger_resume" not in st.session_state:
  st.session_state.trigger_resume = False

# ── Render Sidebar ────────────────────────────────────
render_sidebar()

# ── Render Header ─────────────────────────────────────
render_header()

# ── Render Message History ────────────────────────────
render_messages()

# ── Render Interrupt (HITL UI) ────────────────────────
render_interrupt_ui()

# ── Handle Resuming (After confirmation) ──────────────
if st.session_state.trigger_resume:
  st.session_state.trigger_resume = False  # Reset flag immediately
  
  with st.chat_message("assistant", avatar="🤖"):
    message_placeholder = st.empty()
    current_text = ""
    interrupt_payload = None
    
    response = resume_message_stream(st.session_state.session_id)
    if response:
      for line in response.iter_lines():
        if line:
          decoded = line.decode('utf-8')
          if decoded.startswith('data: '):
            event_str = decoded[6:].strip()
            if not event_str:
              continue
            try:
              event = json.loads(event_str)
              etype = event.get('type')
              if etype == 'chunk':
                current_text += event.get('content', '')
                message_placeholder.markdown(current_text)
              elif etype == 'interrupt':
                interrupt_payload = event
                current_text = event.get('content', '')
                message_placeholder.markdown(current_text)
              elif etype == 'done':
                break
              elif etype == 'error':
                err_content = event.get('content', 'Lỗi không xác định')
                st.error(err_content)
                current_text += f"\n\n❌ Lỗi: {err_content}"
                message_placeholder.markdown(current_text)
            except Exception:
              pass
        
      # Persist results
      if interrupt_payload:
        st.session_state.interrupt_data = interrupt_payload
      elif current_text:
        st.session_state.messages.append({"role": "assistant", "content": current_text})
        
      st.rerun()

# ── Welcome Screen ────────────────────────────────────
show_welcome = len(st.session_state.messages) == 0 and not st.session_state.interrupt_data

if show_welcome:
  render_welcome_screen()

# ── New Message Input and Stream Processing ──────────
# Disable input if waiting for interrupt confirmation
input_disabled = bool(st.session_state.interrupt_data) or st.session_state.trigger_resume

# If user sends a message
if prompt := st.chat_input("Nhập câu hỏi hoặc yêu cầu du lịch của bạn...", disabled=input_disabled):
  # Append user message
  st.session_state.messages.append({"role": "user", "content": prompt})
  st.rerun()

# Process new user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and not st.session_state.interrupt_data and not st.session_state.trigger_resume:
  with st.chat_message("assistant", avatar="🤖"):
    message_placeholder = st.empty()
    current_text = ""
    new_session_id = st.session_state.session_id
    interrupt_payload = None
    
    response = send_message_stream(st.session_state.messages[-1]["content"], st.session_state.session_id)
    if response:
      for line in response.iter_lines():
        if line:
          decoded = line.decode('utf-8')
          if decoded.startswith('data: '):
            event_str = decoded[6:].strip()
            if not event_str:
              continue
            try:
              event = json.loads(event_str)
              etype = event.get('type')
              if etype == 'session':
                new_session_id = event.get('session_id')
                st.session_state.session_id = new_session_id
              elif etype == 'chunk':
                current_text += event.get('content', '')
                message_placeholder.markdown(current_text)
              elif etype == 'interrupt':
                interrupt_payload = event
                current_text = event.get('content', '')
                message_placeholder.markdown(current_text)
              elif etype == 'done':
                break
              elif etype == 'error':
                err_content = event.get('content', 'Lỗi không xác định')
                st.error(err_content)
                current_text += f"\n\n❌ Lỗi: {err_content}"
                message_placeholder.markdown(current_text)
            except Exception:
              pass
        
      # Persist response
      if interrupt_payload:
        st.session_state.interrupt_data = interrupt_payload
      elif current_text:
        st.session_state.messages.append({"role": "assistant", "content": current_text})
        
      st.rerun()