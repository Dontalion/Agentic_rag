"""
Vector store builder.
Orchestrates document splitting, embedding, and Qdrant creation.

"""
from typing import Optional, Tuple

from langchain_core.documents import Document
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.vectorstore.splitters import TextSplitterManager
from agentic_rag.vectorstore.embeddings import EmbeddingManager

logger = get_logger(__name__)
settings = get_settings()


class VectorStoreBuilder:
    """Builds a Qdrant vector store from documents."""

    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        embedding_model: Optional[str] = None,
    ):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        self.embedding_model = embedding_model or settings.embedding_model_name

        # Initialize managers
        self.splitter_manager = TextSplitterManager(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        self.embedding_manager = EmbeddingManager(embedding_model=self.embedding_model)

    def build(self, docs: list[Document]) -> Tuple[QdrantClient, str]:
        """
        Build a Qdrant vector store from documents.

        Args:
            docs: List of Document objects.

        Returns:
            Tuple of (QdrantClient, collection_name).
        """
        if not docs:
            raise ValueError("Cannot build vector store from empty document list")

        # Split documents
        split_docs = self.splitter_manager.split_documents(docs)

        # Get embeddings
        logger.info("Embedding %d chunks...", len(split_docs))
        embeddings = self.embedding_manager.get_embeddings()

        # Setup Qdrant client
        if settings.qdrant_use_docker:
            logger.info("Initializing Qdrant client with Docker: %s", settings.qdrant_url)
            client = QdrantClient(url=settings.qdrant_url)
        else:
            logger.info("Initializing Qdrant client in-memory")
            client = QdrantClient(":memory:")

        collection_name = settings.qdrant_collection_name

        # Create collection and add documents
        logger.info("Creating Qdrant collection: %s", collection_name)
        Qdrant.from_documents(
            documents=split_docs,
            embedding=embeddings,
            client=client,
            collection_name=collection_name,
        )

        logger.info("Qdrant vector store built successfully")
        return client, collection_name


def build_vectorstore(
    docs: list[Document],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
    embedding_model: Optional[str] = None,
) -> Tuple[QdrantClient, str]:
    """
    Convenience function to build a Qdrant vector store.

    Args:
        docs: List of Document objects.
        chunk_size: Token chunk size (default from settings).
        chunk_overlap: Token overlap between chunks (default from settings).
        embedding_model: Embedding model name (default from settings).

    Returns:
        Tuple of (QdrantClient, collection_name).
    """
    builder = VectorStoreBuilder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        embedding_model=embedding_model,
    )
    return builder.build(docs)
