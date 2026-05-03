"""
CLI entry point for the Agentic RAG system.

Handles:
  - Loading documents from the knowledge base
  - Building the vector store
  - Creating the multi-agent system
  - Interactive user loop

Usage:
    python -m agentic_rag.cli
    # or after pip install:
    agentic-rag
"""
import os
import sys

from agentic_rag.config.logging_config import get_logger, set_global_level
from agentic_rag.vectorstore import load_documents, build_vectorstore
from agentic_rag.agents.multi_agent_system import create_multi_agent_system

logger = get_logger(__name__)

# Default knowledge base directory (relative to project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_KB_DIR = os.path.join(PROJECT_ROOT, "knowledge_base")


def _ensure_knowledge_base(kb_dir: str) -> None:
    """Create the knowledge base directory with a sample file if it doesn't exist."""
    if not os.path.exists(kb_dir):
        logger.warning("Knowledge base '%s' not found. Creating with sample document.", kb_dir)
        os.makedirs(kb_dir, exist_ok=True)
        sample = os.path.join(kb_dir, "sample.txt")
        with open(sample, "w", encoding="utf-8") as f:
            f.write(
                "This is a sample document for the Agentic RAG system.\n"
                "Replace this file with your own PDF, TXT, or MD documents.\n"
            )


def _build_pipeline(kb_dir: str):
    """Load documents and build the vector store."""
    _ensure_knowledge_base(kb_dir)

    logger.info("Loading documents from: %s", kb_dir)
    docs = load_documents(kb_dir)

    if not docs:
        logger.warning("No documents loaded. RAG agent will be disabled.")
        return None

    logger.info("Building vector store from %d documents...", len(docs))
    return build_vectorstore(docs)


def main(kb_dir: str = None, log_level: str = None) -> None:
    """
    Run the Agentic RAG interactive CLI.

    Args:
        kb_dir: Path to the knowledge base directory. Defaults to project/knowledge_base.
        log_level: Optional log level override (e.g. "DEBUG").
    """
    if log_level:
        set_global_level(log_level)

    kb_dir = kb_dir or DEFAULT_KB_DIR
    vectordb = _build_pipeline(kb_dir)

    logger.info("Creating multi-agent system...")
    manager = create_multi_agent_system(vectordb=vectordb)

    # Interactive loop
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
                logger.info("User exited.")
                break

            logger.info("Query: %s", user_input)
            print("\nProcessing...\n")
            result = manager.run(user_input)
            print(f"\nAnswer: {result}")
            print("\n" + "-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            logger.info("Interrupted by user.")
            break
        except Exception as e:
            logger.error("Error: %s", e, exc_info=True)
            print(f"\nError: {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
