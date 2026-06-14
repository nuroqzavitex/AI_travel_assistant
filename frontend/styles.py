import streamlit as st

def inject_styles():
  """Inject custom CSS for premium look and feel."""
  st.markdown(
    """
    <style>
    /* Main container padding */
    .block-container {
      padding-top: 2rem;
      padding-bottom: 2rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
      background-color: rgba(245, 245, 244, 0.5);
    }
    
    /* Customize Primary Buttons */
    div.stButton > button[kind="primary"] {
      background-color: #0d9488 !important;
      border-color: #0d9488 !important;
      color: white !important;
    }
    div.stButton > button[kind="primary"]:hover {
      background-color: #14b8a6 !important;
      border-color: #14b8a6 !important;
    }
    
    /* Suggestions chips */
    div.stButton > button {
      border-radius: 10px;
      transition: all 0.2s ease;
    }
    </style>
    """,
    unsafe_allow_html=True
  )