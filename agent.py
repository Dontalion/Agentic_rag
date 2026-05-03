from smolagents import InferenceClientModel, ToolCallingAgent
from retriever_tool import RetrieverTool
from data_loader import load_documents
from inget import process_documents
from config import get_settings

settings = get_settings()

def build_vectordb():
    knowledge_base = [
        {"text": "Example document text 1", "source": "source1/file.txt"},
        {"text": "Example document text 2", "source": "source2/file.txt"},
    ]
    source_docs = load_documents(knowledge_base)
    return process_documents(source_docs)


def main():
    vectordb = build_vectordb()
    model = InferenceClientModel(
        settings.model_name,
        token=settings.huggingface_token if settings.huggingface_token else None,
    )
    retriever_tool = RetrieverTool(vectordb)
    agent = ToolCallingAgent(tools=[retriever_tool], model=model)
    print("Agent initialized with retriever tool.")
    return agent


if __name__ == "__main__":
    main()