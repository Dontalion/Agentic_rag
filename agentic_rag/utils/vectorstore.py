"""
Vector store utilities shared between CLI and UI layers.

Provides functions for managing Qdrant collections, adding documents,
and querying metadata. All logic lives here — UI only consumes results.
"""

from typing import List, Optional

from langchain_core.documents import Document
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.vectorstore.builder import VectorStoreBuilder
from agentic_rag.vectorstore.embeddings import EmbeddingManager

logger = get_logger(__name__)


def ensure_collection_exists(client: QdrantClient, collection_name: Optional[str] = None) -> bool:
    """
    Ensure a Qdrant collection exists. Creates it if missing.

    Args:
        client: QdrantClient instance.
        collection_name: Collection name (defaults to settings).

    Returns:
        True if collection exists (or was created), False on failure.
    """
    settings = get_settings()
    name = collection_name or settings.qdrant_collection_name

    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if name in existing:
        logger.debug("Collection '%s' already exists", name)
        return True

    # Create collection with correct vector size
    embedding_manager = EmbeddingManager()
    embeddings = embedding_manager.get_embeddings()
    vector_size = len(embeddings.embed_query("test"))

    logger.info("Creating collection '%s' with vector size %d", name, vector_size)
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    return True


def add_documents_to_vectorstore(
    client: QdrantClient,
    docs: List[Document],
    collection_name: Optional[str] = None,
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
) -> int:
    """
    Add new documents to an EXISTING Qdrant collection (incremental add).

    This function does NOT recreate the collection.
    It splits documents, generates embeddings, and upserts them into the target collection.

    Args:
        client: QdrantClient instance.
        docs: List of Document objects to add.
        collection_name: Collection name (defaults to settings).
        chunk_size: Optional chunk size override.
        chunk_overlap: Optional chunk overlap override.

    Returns:
        Number of chunks added to the collection.
    """
    settings = get_settings()
    name = collection_name or settings.qdrant_collection_name

    if not docs:
        logger.warning("No documents provided to add_documents_to_vectorstore")
        return 0

    # Use VectorStoreBuilder only for splitting and embedding logic
    temp_builder = VectorStoreBuilder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    split_docs = temp_builder.splitter_manager.split_documents(docs)
    embeddings = temp_builder.embedding_manager.get_embeddings()

    logger.info(
        "Adding %d chunks to existing collection '%s'",
        len(split_docs),
        name,
    )

    # Use LangChain Qdrant wrapper for clean upsert
    qdrant = Qdrant(
        client=client,
        collection_name=name,
        embeddings=embeddings,
    )
    qdrant.add_documents(split_docs)

    logger.info("Successfully added %d chunks", len(split_docs))
    return len(split_docs)


def get_collection_document_count(
    client: QdrantClient,
    collection_name: Optional[str] = None,
) -> int:
    """
    Get the total number of points (chunks) in the collection.

    Args:
        client: QdrantClient instance.
        collection_name: Collection name (defaults to settings).

    Returns:
        Number of indexed chunks.
    """
    settings = get_settings()
    name = collection_name or settings.qdrant_collection_name

    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if name not in existing:
        return 0

    info = client.get_collection(name)
    return info.points_count


def get_indexed_documents_metadata(
    client: QdrantClient,
    collection_name: Optional[str] = None,
) -> List[dict]:
    """
    Get metadata of all indexed documents (unique sources).

    Args:
        client: QdrantClient instance.
        collection_name: Collection name (defaults to settings).

    Returns:
        List of dicts with 'source', 'type', and 'chunk_count' keys.
    """
    settings = get_settings()
    name = collection_name or settings.qdrant_collection_name

    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if name not in existing:
        return []

    # Scroll through all points to collect unique sources
    sources: dict[str, dict] = {}
    offset = None

    while True:
        points, next_offset = client.scroll(
            collection_name=name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        for point in points:
            payload = point.payload or {}
            source = payload.get("source", "unknown")
            doc_type = payload.get("type", "file")

            if source not in sources:
                sources[source] = {"source": source, "type": doc_type, "chunk_count": 0}
            sources[source]["chunk_count"] += 1

        if next_offset is None:
            break
        offset = next_offset

    return list(sources.values())
