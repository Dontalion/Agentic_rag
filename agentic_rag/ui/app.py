"""
Agentic RAG - Streamlit UI
Main entry point for the web interface.

Run with: streamlit run agentic_rag/ui/app.py
"""

import streamlit as st

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
    st.subheader("Chat")
    # Placeholder for chat interface (will be implemented in later tasks)
    st.info("Chat interface will be added in Task 5.")

with col_sources:
    st.subheader("Sources")
    # Placeholder for source viewer (will be implemented in Task 7)
    st.info("Source viewer will appear here when you click on citations.")
