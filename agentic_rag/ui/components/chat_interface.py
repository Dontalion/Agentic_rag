"""
Chat interface component for the Streamlit UI.

Displays chat history, handles user input, and shows agent responses.
All heavy logic (agent creation, vector store queries) is delegated to backend utils.
"""

import streamlit as st
from agentic_rag.ui.utils.caching import get_qdrant_client, get_embeddings, get_llm_model
from agentic_rag.ui.utils.session import init_session_state, add_chat_message, get_chat_messages
from agentic_rag.utils.agents import get_chat_manager
from agentic_rag.utils.vectorstore import get_collection_document_count


def render_chat_interface() -> None:
    """
    Render the main chat interface.

    Displays chat history, handles user input, and invokes the agent system.
    """
    init_session_state()

    # Display existing chat messages
    for message in get_chat_messages():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        add_chat_message("user", prompt)

        # Display assistant message with spinner
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = _process_query(prompt)
            st.markdown(response)
        add_chat_message("assistant", response)


def _process_query(query: str) -> str:
    """
    Process a user query through the agent system.

    Args:
        query: The user's question.

    Returns:
        The agent's response text.
    """
    # Check if any documents are indexed
    client = get_qdrant_client()
    doc_count = get_collection_document_count(client)

    if doc_count == 0:
        return "📄 No documents have been indexed yet. Please upload a document or add a web page to get started."

    # Get cached objects
    embeddings = get_embeddings()
    model = get_llm_model()

    # Build manager with appropriate agents
    web_search_enabled = st.session_state.get("web_search_enabled", False)
    manager = get_chat_manager(
        model=model,
        qdrant_client=client,
        collection_name=None,  # uses default from settings
        embeddings=embeddings,
        web_search_enabled=web_search_enabled,
    )

    # Run the query
    try:
        response = manager.run(query)
        return str(response)
    except Exception as e:
        return f"⚠️ An error occurred while processing your query: {e}"
