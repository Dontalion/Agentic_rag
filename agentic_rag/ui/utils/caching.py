"""
Streamlit caching utilities for heavy objects.

Provides cached access to settings, Qdrant client, embeddings, and LLM model.
These functions use @st.cache_resource to avoid reloading expensive objects
on every Streamlit rerun.
"""

import streamlit as st
from qdrant_client import QdrantClient
from langchain_core.embeddings import Embeddings
from smolagents import InferenceClientModel
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.vectorstore.embeddings import EmbeddingManager

logger = get_logger(__name__)


@st.cache_resource
def get_settings_cached():
    """
    Get cached application settings.

    Returns:
        Settings instance from pydantic-settings.
    """
    return get_settings()


@st.cache_resource
def get_qdrant_client() -> QdrantClient:
    """
    Get or create a cached Qdrant client.

    Returns:
        QdrantClient instance (in-memory or Docker based on settings).
    """
    settings = get_settings_cached()

    if settings.qdrant_use_docker:
        logger.info("Initializing Qdrant client with Docker: %s", settings.qdrant_url)
        client = QdrantClient(url=settings.qdrant_url)
    else:
        logger.info("Initializing Qdrant client in-memory")
        client = QdrantClient(":memory:")

    return client


@st.cache_resource
def get_embeddings() -> Embeddings:
    """
    Get or create a cached embedding model.

    Returns:
        HuggingFaceEmbeddings instance.
    """
    settings = get_settings_cached()
    embedding_manager = EmbeddingManager(embedding_model=settings.embedding_model_name)
    return embedding_manager.get_embeddings()


@st.cache_resource
def get_llm_model() -> InferenceClientModel:
    """
    Get or create a cached LLM model.

    Returns:
        InferenceClientModel instance.
    """
    settings = get_settings_cached()

    if not settings.huggingface_token:
        logger.warning("HuggingFace token not set. LLM calls may fail.")

    return InferenceClientModel(
        settings.model_name,
        token=settings.huggingface_token if settings.huggingface_token else None,
    )
