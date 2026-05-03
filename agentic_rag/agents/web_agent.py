"""
Web Search Agent using smolagents.
Performs web searches and visits webpages to gather information.
"""
from smolagents import ToolCallingAgent, InferenceClientModel
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.tools.visit_webpage import visit_webpage
from agentic_rag.tools.web_search_tool import WebSearchTool

logger = get_logger(__name__)
settings = get_settings()

model = InferenceClientModel(
    settings.model_name,
    token=settings.huggingface_token if settings.huggingface_token else None,
)

web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage],
    model=model,
    max_steps=10,
    name="web_search_agent",
    description="Runs web searches and visits webpages to gather current information.",
)