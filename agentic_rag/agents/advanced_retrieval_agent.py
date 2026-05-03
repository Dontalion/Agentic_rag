"""
Advanced Retrieval Agent using smolagents.
This agent specializes in retrieving information from the knowledge base.
"""
from smolagents import InferenceClientModel, CodeAgent
from qdrant_client import QdrantClient
from langchain_core.embeddings import Embeddings
from agentic_rag.tools.qdrant_retriever_tool import AdvancedQdrantRetrieverTool
from agentic_rag.config.config import get_settings

settings = get_settings()


def create_advanced_retrieval_agent(
    qdrant_client: QdrantClient, collection_name: str, embeddings: Embeddings
):
    """
    Create an advanced retrieval agent with the given Qdrant vector database.

    Args:
        qdrant_client: A Qdrant client instance
        collection_name: Name of the Qdrant collection
        embeddings: Embeddings instance for query encoding

    Returns:
        CodeAgent configured for knowledge base retrieval
    """
    retriever_tool = AdvancedQdrantRetrieverTool(
        qdrant_client=qdrant_client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    model = InferenceClientModel(
        settings.model_name,
        token=settings.huggingface_token if settings.huggingface_token else None,
    )

    agent = CodeAgent(
        tools=[retriever_tool],
        model=model,
        name="advanced_retrieval_agent",
        description="Specialized in retrieving information from the local knowledge base using semantic search via Qdrant.",
        max_steps=4,
        verbosity_level=2,
    )

    return agent