"""
RAG (Retrieval Augmented Generation) Agent.
Specialized in retrieving information from local knowledge base.
"""
from smolagents import CodeAgent
from langchain_core.vectorstores import VectorStore
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.tools.retriever_tool import RetrieverTool

logger = get_logger(__name__)
settings = get_settings()


def create_rag_agent(model, vectordb: VectorStore) -> CodeAgent:
    """
    Create a RAG agent for knowledge base retrieval.
    
    Args:
        model: The LLM model instance (InferenceClientModel).
        vectordb: FAISS vector store instance.
    
    Returns:
        CodeAgent configured for RAG tasks.
    """
    logger.info("Creating RAG agent")
    rag_tool = RetrieverTool(vectordb)
    
    rag_agent = CodeAgent(
        tools=[rag_tool],
        model=model,
        name="rag_agent",
        description="Specialized in retrieving information from the local knowledge base using semantic search.",
    )
    
    return rag_agent
