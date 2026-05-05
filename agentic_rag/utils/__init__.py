"""Shared utilities used by both CLI and UI layers."""

from agentic_rag.utils.vectorstore import (
    ensure_collection_exists,
    add_documents_to_vectorstore,
    get_collection_document_count,
    get_indexed_documents_metadata,
)
from agentic_rag.utils.agents import (
    get_rag_agent,
    get_web_search_agent,
    get_chat_manager,
)

__all__ = [
    # Vector store
    "ensure_collection_exists",
    "add_documents_to_vectorstore",
    "get_collection_document_count",
    "get_indexed_documents_metadata",
    # Agents
    "get_rag_agent",
    "get_web_search_agent",
    "get_chat_manager",
]