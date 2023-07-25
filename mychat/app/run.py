import streamlit as st 
from .chat import chat
from .profile_form import profile_form

def run_app():
    
    with st.sidebar:
        
        st.divider()
        profile_form()
        
    chat()
