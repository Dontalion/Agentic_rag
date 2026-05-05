"""
Sidebar component for the Streamlit UI.

Displays indexed documents, stats, and controls (web search toggle, new chat).
"""

import streamlit as st
from agentic_rag.ui.utils.caching import get_settings_cached, get_qdrant_client
from agentic_rag.ui.utils.session import reset_chat_history
from agentic_rag.utils.vectorstore import get_indexed_documents_metadata, get_collection_document_count
from agentic_rag.ui.components.document_uploader import render_document_uploader


def render_sidebar() -> None:
    """
    Render the sidebar with document list, stats, and controls.
    """
    with st.sidebar:
        # Document uploader (first in sidebar)
        render_document_uploader()

        st.divider()

        # Stats
        st.header("📚 Knowledge Base")
        client = get_qdrant_client()
        doc_count = _get_unique_document_count(client)
        st.metric("Indexed Documents", doc_count)

        # Document list
        st.subheader("Documents")
        _render_document_list(client)

        st.divider()

        # Controls
        st.subheader("Controls")
        _render_web_search_toggle()
        _render_new_chat_button()

        st.divider()

        # Model info
        st.subheader("Model")
        _render_model_info()


def _get_unique_document_count(client) -> int:
    """
    Get the number of unique indexed documents.

    Args:
        client: QdrantClient instance.

    Returns:
        Number of unique documents.
    """
    metadata = get_indexed_documents_metadata(client)
    return len(metadata)


def _render_document_list(client) -> None:
    """
    Render the list of indexed documents.

    Args:
        client: QdrantClient instance.
    """
    metadata = get_indexed_documents_metadata(client)

    if not metadata:
        st.info("No documents indexed yet.")
        return

    for doc in metadata:
        source = doc["source"]
        doc_type = doc["type"]

        # Display type icon
        icon = {"pdf": "📄", "txt": "📝", "md": "📋", "web": "🌐"}.get(doc_type.lower(), "📄")

        # Truncate long filenames
        display_name = source.split("/")[-1]
        if len(display_name) > 30:
            display_name = display_name[:27] + "..."

        st.caption(f"{icon} {display_name}")


def _render_web_search_toggle() -> None:
    """
    Render the web search toggle switch.
    """
    web_search = st.toggle(
        "Enable Web Search",
        value=st.session_state.get("web_search_enabled", False),
        help="When enabled, the agent can search the web for up-to-date information.",
    )
    st.session_state.web_search_enabled = web_search


def _render_new_chat_button() -> None:
    """
    Render the new chat button.
    """
    if st.button("🗑️ New Chat", use_container_width=True):
        reset_chat_history()
        st.rerun()


def _render_model_info() -> None:
    """
    Render model information (read-only).
    """
    settings = get_settings_cached()
    st.caption(f"Model: `{settings.model_name}`")
