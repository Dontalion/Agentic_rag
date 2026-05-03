"""
Vector Store Module

Handles document loading, splitting, embedding, and Qdrant vector database creation.
Completely independent from the agent system.

Components:
- file_loaders: Format-specific file loading (PDF, TXT, MD)
- splitters: Document chunking with tokenizer awareness
- embeddings: Embedding model management
- loader: High-level document loading interface
- builder: Qdrant vector store construction
"""
from agentic_rag.vectorstore.loader import load_documents
from agentic_rag.vectorstore.builder import build_vectorstore, VectorStoreBuilder
from agentic_rag.vectorstore.splitters import TextSplitterManager
from agentic_rag.vectorstore.embeddings import EmbeddingManager

__all__ = [
    "load_documents",
    "build_vectorstore",
    "VectorStoreBuilder",
    "TextSplitterManager",
    "EmbeddingManager",
]
