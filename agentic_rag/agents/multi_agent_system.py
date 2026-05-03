"""
Multi-Agent RAG System using smolagents.

This module ONLY defines the agent architecture.
It does NOT handle:
  - Vector store building (use agentic_rag.vectorstore)
  - CLI interaction (use agentic_rag.cli)
  - Logging configuration (use agentic_rag.config.logging_config)

Usage:
    from agentic_rag.vectorstore import build_vectorstore, load_documents
    from agentic_rag.agents.multi_agent_system import create_multi_agent_system

    docs = load_documents("knowledge_base/")
    vectordb = build_vectorstore(docs)
    manager = create_multi_agent_system(vectordb=vectordb)
    result = manager.run("Your question here")
"""
from typing import Optional

from smolagents import CodeAgent, InferenceClientModel
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.tools.retriever_tool import RetrieverTool
from agentic_rag.tools.pdf_analyzer_tool import PDFAnalyzerTool
from agentic_rag.tools.web_search_tool import WebSearchTool

logger = get_logger(__name__)
settings = get_settings()


def create_multi_agent_system(vectordb=None):
    """
    Create and return a multi-agent system.

    Args:
        vectordb: A FAISS vector store instance. If None, the RAG agent
                  will not be included.

    Returns:
        CodeAgent (manager) that orchestrates all sub-agents.
    """
    model = InferenceClientModel(
        settings.model_name,
        token=settings.huggingface_token if settings.huggingface_token else None,
    )

    managed_agents = []

    # RAG Agent (only if vectordb is provided)
    if vectordb is not None:
        rag_tool = RetrieverTool(vectordb)
        rag_agent = CodeAgent(
            tools=[rag_tool],
            model=model,
            name="rag_agent",
            description="Specialized in retrieving information from the local knowledge base using semantic search.",
        )
        managed_agents.append(rag_agent)
    else:
        logger.warning("RAG agent disabled: no vector database provided")

    # Web Search Agent
    web_tool = WebSearchTool()
    web_search_agent = CodeAgent(
        tools=[web_tool],
        model=model,
        name="web_search_agent",
        description="Specialized in performing web searches to find current information from the internet.",
    )
    managed_agents.append(web_search_agent)

    # PDF Analyzer Agent
    pdf_tool = PDFAnalyzerTool()
    pdf_analyzer_agent = CodeAgent(
        tools=[pdf_tool],
        model=model,
        name="pdf_analyzer_agent",
        description="Specialized in reading and analyzing PDF documents. Use this agent when you need to extract text, summarize content, or answer questions about a specific PDF file.",
    )
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
    