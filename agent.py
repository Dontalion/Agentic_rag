from smolagents import InferenceClientModel, ToolCallingAgent
from retriver_tool import RetrieverTool
from langchain_core.vectorstores import VectorStore

model = InferenceClientModel("meta-llama/Llama-3.1-70B-Instruct")

retriever_tool = RetrieverTool(vectordb)
agent = ToolCallingAgent(
    tools=[retriever_tool], model=model
)