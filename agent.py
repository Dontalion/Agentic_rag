from smolagents import InferenceClientModel, ToolCallingAgent
from retriever_tool import RetrieverTool
from langchain_core.vectorstores import VectorStore
from inget import vectordb
from config import get_settings

settings = get_settings()

model = InferenceClientModel(settings.model_name, token=settings.huggingface_token if settings.huggingface_token else None)

retriever_tool = RetrieverTool(vectordb)
agent = ToolCallingAgent(
    tools=[retriever_tool], model=model
)