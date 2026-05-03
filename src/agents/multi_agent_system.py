"""
Multi-Agent RAG System using smolagents.
This system includes:
- Web Search Agent: searches the internet for current information
- PDF Analyzer Agent: reads and analyzes PDF documents
- RAG Agent: retrieves information from the local knowledge base
- Manager Agent: orchestrates all sub-agents to answer complex queries
"""
from smolagents import CodeAgent, InferenceClientModel
from src.data.data_loader import load_documents
from src.tools.knowledge_base import process_documents
from src.tools.retriever_tool import RetrieverTool
from src.tools.pdf_analyzer_tool import PDFAnalyzerTool
from src.tools.web_search_tool import WebSearchTool
from src.config.config import get_settings

settings = get_settings()


def build_vectordb():
    """Build the vector database from the knowledge base."""
    # Example knowledge_base - replace with actual data loading
    knowledge_base = [
        {"text": "Example document text 1", "source": "source1/file.txt"},
        {"text": "Example document text 2", "source": "source2/file.txt"},
    ]
    source_docs = load_documents(knowledge_base)
    return process_documents(source_docs)


def create_multi_agent_system():
    """
    Create and return a multi-agent system with:
    - Web Search Agent
    - PDF Analyzer Agent
    - RAG Agent
    - Manager Agent that orchestrates the sub-agents
    """
    # Initialize the model
    model = InferenceClientModel(
        settings.model_name,
        token=settings.huggingface_token if settings.huggingface_token else None,
    )

    # Build the vector database for RAG
    vectordb = build_vectordb()

    # Create tools
    rag_tool = RetrieverTool(vectordb)
    pdf_tool = PDFAnalyzerTool()
    web_tool = WebSearchTool()

    # Create the RAG Agent (specialized in knowledge base retrieval)
    rag_agent = CodeAgent(
        tools=[rag_tool],
        model=model,
        name="rag_agent",
        description="Specialized in retrieving information from the local knowledge base using semantic search. Use this agent when you need to find information from pre-loaded documents.",
    )

    # Create the Web Search Agent (specialized in internet searches)
    web_search_agent = CodeAgent(
        tools=[web_tool],
        model=model,
        name="web_search_agent",
        description="Specialized in performing web searches to find current information from the internet. Use this agent when you need up-to-date information, news, or facts not available in the local knowledge base.",
    )

    # Create the PDF Analyzer Agent (specialized in PDF document analysis)
    pdf_analyzer_agent = CodeAgent(
        tools=[pdf_tool],
        model=model,
        name="pdf_analyzer_agent",
        description="Specialized in reading and analyzing PDF documents. Use this agent when you need to extract text, summarize content, or answer questions about a specific PDF file.",
    )

    # Create the Manager Agent that orchestrates all sub-agents
    manager_agent = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[rag_agent, web_search_agent, pdf_analyzer_agent],
        max_steps=10,
    )

    print("Multi-agent system initialized successfully!")
    print("Available agents:")
    print("  - rag_agent: Retrieves from local knowledge base")
    print("  - web_search_agent: Searches the internet")
    print("  - pdf_analyzer_agent: Analyzes PDF documents")
    print("  - manager_agent: Orchestrates all sub-agents")

    return manager_agent


def main():
    """Main entry point for the multi-agent system."""
    manager_agent = create_multi_agent_system()

    print("\n" + "=" * 60)
    print("Multi-Agent RAG System Ready!")
    print("=" * 60)
    print("Type your question and press Enter (or 'quit' to exit)")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye!")
                break

            print("\nProcessing your query...\n")
            result = manager_agent.run(user_input)
            print(f"\nAnswer: {result}")
            print("\n" + "-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
    