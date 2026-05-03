"""
Web Search Agent.
Performs web searches and visits webpages to gather current information.
"""
from smolagents import CodeAgent
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.tools.web_search_tool import WebSearchTool
from agentic_rag.tools.visit_webpage import visit_webpage

logger = get_logger(__name__)
settings = get_settings()


def create_web_search_agent(model) -> CodeAgent:
    """
    Create a web search agent for internet information retrieval.
    
    Args:
        model: The LLM model instance (InferenceClientModel).
    
    Returns:
        CodeAgent configured for web search tasks.
    """
    logger.info("Creating web search agent")
    
    web_search_agent = CodeAgent(
        tools=[WebSearchTool(), visit_webpage],
        model=model,
        max_steps=10,
        name="web_search_agent",
        description="Runs web searches and visits webpages to gather current information.",
    )
    
    return web_search_agent