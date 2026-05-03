from src.config.config import get_settings
from src.tools.visit_webpage import visit_webpage
from src.tools.web_search_tool import WebSearchTool
settings = get_settings()
from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    InferenceClientModel,
    WebSearchTool,
)

model = InferenceClientModel(model_id=settings.model_name)

web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage],
    model=model,
    max_steps=10,
    name="web_search_agent",
    description="Runs web searches for you.",
)