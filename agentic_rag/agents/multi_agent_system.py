"""
Multi-Agent RAG System using smolagents.

Orchestrates multiple specialized agents:
- RAG Agent: local knowledge base retrieval
- Web Search Agent: internet information
- PDF Analyzer Agent: document analysis

This module ONLY handles orchestration.
"""
from typing import Optional, Tuple

from smolagents import CodeAgent, InferenceClientModel
from qdrant_client import QdrantClient
from langchain_core.embeddings import Embeddings
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.agents.rag_agent import create_rag_agent
from agentic_rag.agents.web_agent import create_web_search_agent
from agentic_rag.agents.pdf_agent import create_pdf_analyzer_agent

logger = get_logger(__name__)
settings = get_settings()


def create_multi_agent_system(
    qdrant_client: Optional[QdrantClient] = None,
    collection_name: Optional[str] = None,
    embeddings: Optional[Embeddings] = None,
) -> CodeAgent:
    """
    Create and return a multi-agent system.

    Args:
        qdrant_client: A Qdrant client instance. If None, the RAG agent
                       will not be included.
        collection_name: Name of the Qdrant collection.
        embeddings: Embeddings instance for query encoding.

    Returns:
        CodeAgent (manager) that orchestrates all sub-agents.
    """
    # Create the base model
    logger.info("Creating base LLM model: %s", settings.model_name)
    model = InferenceClientModel(
        settings.model_name,
        token=settings.huggingface_token if settings.huggingface_token else None,
    )

    managed_agents = []

    # RAG Agent (only if qdrant_client and embeddings are provided)
    if qdrant_client is not None and collection_name is not None and embeddings is not None:
        rag_agent = create_rag_agent(model, qdrant_client, collection_name, embeddings)
        managed_agents.append(rag_agent)
    else:
        logger.warning("RAG agent disabled: no Qdrant vector database provided")

    # Web Search Agent
    web_search_agent = create_web_search_agent(model)
    managed_agents.append(web_search_agent)

    # PDF Analyzer Agent
    pdf_analyzer_agent = create_pdf_analyzer_agent(model)
    managed_agents.append(pdf_analyzer_agent)

    # Manager Agent
    manager_agent = CodeAgent(
        tools=[],
        model=model,
        managed_agents=managed_agents,
        max_steps=10,
    )

    logger.info("Multi-agent system initialized with agents: %s", [a.name for a in managed_agents])
    return manager_agent