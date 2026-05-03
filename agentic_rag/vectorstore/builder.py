"""
Vector store builder.
Orchestrates document splitting, embedding, and FAISS creation.

"""
from typing import Optional

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.vectorstore.splitters import TextSplitterManager
from agentic_rag.vectorstore.embeddings import EmbeddingManager

logger = get_logger(__name__)
settings = get_settings()


class VectorStoreBuilder:
    """Builds a FAISS vector store from documents."""

    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        embedding_model: Optional[str] = None,
        distance_strategy: Optional[str] = None,
    ):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        self.embedding_model = embedding_model or settings.embedding_model_name
        self.distance_strategy = distance_strategy or settings.distance_strategy

        # Initialize managers
        self.splitter_manager = TextSplitterManager(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        self.embedding_manager = EmbeddingManager(embedding_model=self.embedding_model)

    def build(self, docs: list[Document]) -> FAISS:
        """
        Build a FAISS vector store from documents.

        Args:
            docs: List of Document objects.

        Returns:
            FAISS vector store.
        """
        if not docs:
            raise ValueError("Cannot build vector store from empty document list")

        # Split documents
        split_docs = self.splitter_manager.split_documents(docs)

        # Get embeddings
        logger.info("Embedding %d chunks...", len(split_docs))
        embeddings = self.embedding_manager.get_embeddings()

        # Determine distance strategy
        strategy = (
            DistanceStrategy.COSINE
            if self.distance_strategy.upper() == "COSINE"
            else DistanceStrategy.EUCLIDEAN_DISTANCE
        )

        # Build FAISS vector store
        vectordb = FAISS.from_documents(
            documents=split_docs,
            embedding=embeddings,
            distance_strategy=strategy,
        )

        logger.info("Vector store built successfully")
        return vectordb


def build_vectorstore(
    docs: list[Document],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
    embedding_model: Optional[str] = None,
    distance_strategy: Optional[str] = None,
) -> FAISS:
    """
    Convenience function to build a FAISS vector store.

    Args:
        docs: List of Document objects.
        chunk_size: Token chunk size (default from settings).
        chunk_overlap: Token overlap between chunks (default from settings).
        embedding_model: Embedding model name (default from settings).
        distance_strategy: "COSINE" or "EUCLIDEAN" (default from settings).

    Returns:
        FAISS vector store.
    """
    builder = VectorStoreBuilder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        embedding_model=embedding_model,
        distance_strategy=distance_strategy,
    )
    return builder.build(docs)
