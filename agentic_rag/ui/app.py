"""
Agentic RAG - Streamlit UI
Main entry point for the web interface.

Run with: streamlit run agentic_rag/ui/app.py
"""

import streamlit as st
from agentic_rag.ui.components.chat_interface import render_chat_interface

st.set_page_config(
    page_title="Agentic RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Agentic RAG")
st.caption("Chat with your documents and the web")

# Main layout: Chat (left) + Sources (right)
col_chat, col_sources = st.columns([3, 1])

with col_chat:
    render_chat_interface()

with col_sources:
    st.subheader("Sources")
    st.info("Source viewer will appear here when you click on citations.")
