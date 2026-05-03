"""
CLI entry point for the Agentic RAG system.

Handles interactive user interface for querying the multi-agent system.

Usage:
    python -m agentic_rag.cli
    # or after pip install:
    agentic-rag
"""
import os
import sys

from agentic_rag.config.logging_config import get_logger, set_global_level
from agentic_rag.agents.multi_agent_system import create_multi_agent_system
from agentic_rag.initialization import build_rag_pipeline

logger = get_logger(__name__)

# Default knowledge base directory (relative to project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_KB_DIR = os.path.join(PROJECT_ROOT, "knowledge_base")


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
    
    # Build RAG pipeline
    logger.info("Initializing RAG system...")
    vectordb = build_rag_pipeline(kb_dir)

    # Create multi-agent system
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
