"""
Session state management for the Streamlit UI.

Provides helpers for initializing, accessing, and resetting chat session state.
"""

import streamlit as st
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)


def init_session_state() -> None:
    """
    Initialize Streamlit session state variables if not already set.

    Sets up:
    - messages: Chat history (list of {"role", "content"})
    - web_search_enabled: Toggle state for web search
    - selected_source: Currently selected source for viewing
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.debug("Initialized chat messages")

    if "web_search_enabled" not in st.session_state:
        st.session_state.web_search_enabled = False
        logger.debug("Initialized web search toggle (OFF)")

    if "selected_source" not in st.session_state:
        st.session_state.selected_source = None
        logger.debug("Initialized selected source (None)")


def reset_chat_history() -> None:
    """
    Clear the chat history and reset session state.
    """
    st.session_state.messages = []
    st.session_state.selected_source = None
    logger.info("Chat history reset")


def get_chat_messages() -> list[dict]:
    """
    Get the current chat message history.

    Returns:
        List of message dicts with "role" and "content" keys.
    """
    return st.session_state.messages


def add_chat_message(role: str, content: str) -> None:
    """
    Add a message to the chat history.

    Args:
        role: Message role ("user" or "assistant").
        content: Message content.
    """
    st.session_state.messages.append({"role": role, "content": content})
