"""
Vector store utility functions shared between CLI and UI.

This module contains focused helpers for common vector store operations
that are needed by both the command-line interface and the Streamlit UI.
"""

from typing import Optional

from langchain_core.documents import Document
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from agentic_rag.config.logging_config import get_logger
from agentic_rag.vectorstore.builder import VectorStoreBuilder

logger = get_logger(__name__)


def add_documents_to_vectorstore(
    client: QdrantClient,
    collection_name: str,
    docs: list[Document],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
) -> int:
    """
    Add new documents to an EXISTING Qdrant collection (incremental add).

    This function does NOT recreate the collection.
    It splits documents, generates embeddings, and upserts them into the target collection.

    This helper is shared between the CLI and the UI layers.

    Args:
        client: An existing QdrantClient instance.
        collection_name: Name of the target collection.
        docs: List of Document objects to add.
        chunk_size: Optional chunk size override.
        chunk_overlap: Optional overlap override.

    Returns:
        Number of chunks added to the collection.
    """
    if not docs:
        logger.warning("No documents provided to add_documents_to_vectorstore")
        return 0

    # Use VectorStoreBuilder only for splitting and embedding logic
    temp_builder = VectorStoreBuilder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    split_docs = temp_builder.splitter_manager.split_documents(docs)
    embeddings = temp_builder.embedding_manager.get_embeddings()

    logger.info(
        "Adding %d chunks to existing collection '%s'",
        len(split_docs),
        collection_name,
    )

    # Use LangChain Qdrant wrapper for clean upsert
    qdrant = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )
    qdrant.add_documents(split_docs)

    logger.info("Successfully added %d chunks", len(split_docs))
    return len(split_docs)
