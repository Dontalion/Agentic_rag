"""
Vector Store Module

Handles document loading, splitting, embedding, and FAISS vector database creation.
Completely independent from the agent system.
"""
from agentic_rag.vectorstore.loader import load_documents
from agentic_rag.vectorstore.builder import build_vectorstore, VectorStoreBuilder

__all__ = ["load_documents", "build_vectorstore", "VectorStoreBuilder"]
