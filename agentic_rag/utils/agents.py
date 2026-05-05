"""
Lazy agent factories for the multi-agent system.

Provides functions to create RAG, Web Search, and Manager agents on demand.
These are backend functions — UI only calls them and passes the result to the agent.
"""

from typing import Optional

from smolagents import CodeAgent
from qdrant_client import QdrantClient
from langchain_core.embeddings import Embeddings
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.agents.rag_agent import create_rag_agent
from agentic_rag.agents.web_agent import create_web_search_agent

logger = get_logger(__name__)


def get_rag_agent(
    model,
    qdrant_client: QdrantClient,
    collection_name: str,
    embeddings: Embeddings,
) -> CodeAgent:
    """
    Create a RAG agent for knowledge base retrieval.

    Args:
        model: LLM model instance (InferenceClientModel).
        qdrant_client: Qdrant client instance.
        collection_name: Name of the Qdrant collection.
        embeddings: Embeddings instance for query encoding.

    Returns:
        CodeAgent configured for RAG tasks.
    """
    return create_rag_agent(model, qdrant_client, collection_name, embeddings)


def get_web_search_agent(model) -> CodeAgent:
    """
    Create a web search agent for internet information retrieval.

    Args:
        model: LLM model instance (InferenceClientModel).

    Returns:
        CodeAgent configured for web search tasks.
    """
    return create_web_search_agent(model)


def get_chat_manager(
    model,
    qdrant_client: Optional[QdrantClient] = None,
    collection_name: Optional[str] = None,
    embeddings: Optional[Embeddings] = None,
    web_search_enabled: bool = False,
) -> CodeAgent:
    """
    Create a manager agent with the appropriate sub-agents.

    Args:
        model: LLM model instance (InferenceClientModel).
        qdrant_client: Qdrant client instance (optional — RAG agent skipped if None).
        collection_name: Name of the Qdrant collection.
        embeddings: Embeddings instance for query encoding.
        web_search_enabled: Whether to include the web search agent.

    Returns:
        CodeAgent (manager) that orchestrates sub-agents.
    """
    settings = get_settings()
    managed_agents = []

    # RAG Agent (only if vector store is available)
    if qdrant_client is not None and collection_name is not None and embeddings is not None:
        rag_agent = get_rag_agent(model, qdrant_client, collection_name, embeddings)
        managed_agents.append(rag_agent)
        logger.info("RAG agent included in manager")
    else:
        logger.warning("RAG agent disabled: no Qdrant vector database provided")

    # Web Search Agent (only if enabled)
    if web_search_enabled:
        web_agent = get_web_search_agent(model)
        managed_agents.append(web_agent)
        logger.info("Web search agent included in manager")

    # Manager Agent
    manager = CodeAgent(
        tools=[],
        model=model,
        managed_agents=managed_agents,
        max_steps=10,
    )

    logger.info(
        "Chat manager created with agents: %s",
        [a.name for a in managed_agents],
    )
    return manager
