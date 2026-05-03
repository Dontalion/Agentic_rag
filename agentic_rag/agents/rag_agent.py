"""
RAG (Retrieval Augmented Generation) Agent.
Specialized in retrieving information from local knowledge base.
"""
from smolagents import CodeAgent
from qdrant_client import QdrantClient
from langchain_core.embeddings import Embeddings
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.tools.qdrant_retriever_tool import AdvancedQdrantRetrieverTool

logger = get_logger(__name__)
settings = get_settings()


def create_rag_agent(
    model, qdrant_client: QdrantClient, collection_name: str, embeddings: Embeddings
) -> CodeAgent:
    """
    Create a RAG agent for knowledge base retrieval using Qdrant.

    Args:
        model: The LLM model instance (InferenceClientModel).
        qdrant_client: Qdrant client instance.
        collection_name: Name of the Qdrant collection.
        embeddings: Embeddings instance for query encoding.

    Returns:
        CodeAgent configured for RAG tasks.
    """
    logger.info("Creating RAG agent with Qdrant backend")
    rag_tool = AdvancedQdrantRetrieverTool(
        qdrant_client=qdrant_client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    rag_agent = CodeAgent(
        tools=[rag_tool],
        model=model,
        name="rag_agent",
        description="Specialized in retrieving information from the local knowledge base using semantic search via Qdrant.",
    )

    return rag_agent
