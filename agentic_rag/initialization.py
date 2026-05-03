"""
CLI initialization and setup utilities.
Handles knowledge base preparation and pipeline setup.
"""
import os
from agentic_rag.config.logging_config import get_logger
from agentic_rag.vectorstore import load_documents, build_vectorstore

logger = get_logger(__name__)


def ensure_knowledge_base(kb_dir: str) -> None:
    """
    Ensure knowledge base directory exists with sample file if needed.
    
    Args:
        kb_dir: Path to the knowledge base directory.
    """
    if not os.path.exists(kb_dir):
        logger.warning("Knowledge base '%s' not found. Creating with sample document.", kb_dir)
        os.makedirs(kb_dir, exist_ok=True)
        sample = os.path.join(kb_dir, "sample.txt")
        with open(sample, "w", encoding="utf-8") as f:
            f.write(
                "This is a sample document for the Agentic RAG system.\n"
                "Replace this file with your own PDF, TXT, or MD documents.\n"
            )


def build_rag_pipeline(kb_dir: str):
    """
    Load documents and build the vector store.
    
    Args:
        kb_dir: Path to the knowledge base directory.
    
    Returns:
        FAISS vector store or None if no documents found.
    """
    ensure_knowledge_base(kb_dir)

    logger.info("Loading documents from: %s", kb_dir)
    docs = load_documents(kb_dir)

    if not docs:
        logger.warning("No documents loaded. RAG agent will be disabled.")
        return None

    logger.info("Building vector store from %d documents...", len(docs))
    return build_vectorstore(docs)
