"""
Advanced Retrieval Agent using smolagents.
This agent specializes in retrieving information from the knowledge base.
"""
from smolagents import InferenceClientModel, CodeAgent
from src.tools.retriever_tool import RetrieverTool
from src.config.config import get_settings

settings = get_settings()


def create_advanced_retrieval_agent(vectordb):
    """
    Create an advanced retrieval agent with the given vector database.
    
    Args:
        vectordb: A FAISS vector database instance
        
    Returns:
        CodeAgent configured for knowledge base retrieval
    """
    retriever_tool = RetrieverTool(vectordb)
    
    model = InferenceClientModel(
        settings.model_name,
        token=settings.huggingface_token if settings.huggingface_token else None,
    )

    agent = CodeAgent(
        tools=[retriever_tool],
        model=model,
        name="advanced_retrieval_agent",
        description="Specialized in retrieving information from the local knowledge base using semantic search.",
        max_steps=4,
        verbosity_level=2,
    )
    
    return agent