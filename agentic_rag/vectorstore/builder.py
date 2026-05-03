"""
Vector store builder.
Handles document splitting, embedding, and FAISS creation.
"""
from typing import Optional

from tqdm import tqdm
from transformers import AutoTokenizer
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger

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

    def _create_splitter(self) -> RecursiveCharacterTextSplitter:
        """Create a text splitter using the configured tokenizer."""
        tokenizer = AutoTokenizer.from_pretrained(
            settings.tokenizer_model_name,
            use_auth_token=settings.huggingface_token or None,
        )
        return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=True,
            strip_whitespace=True,
            separators=["\n\n", "\n", ".", " ", ""],
        )

    def _split_documents(self, docs: list[Document]) -> list[Document]:
        """Split documents into chunks, keeping only unique content."""
        logger.info("Splitting %d documents...", len(docs))
        splitter = self._create_splitter()

        processed = []
        seen = set()
        for doc in tqdm(docs, desc="Splitting"):
            for chunk in splitter.split_documents([doc]):
                if chunk.page_content not in seen:
                    seen.add(chunk.page_content)
                    processed.append(chunk)

        logger.info("Produced %d unique chunks", len(processed))
        return processed

    def _create_embeddings(self) -> HuggingFaceEmbeddings:
        """Create the embedding model."""
        logger.info("Loading embedding model: %s", self.embedding_model)
        return HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={"use_auth_token": settings.huggingface_token}
            if settings.huggingface_token
            else {},
        )

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

        split_docs = self._split_documents(docs)

        logger.info("Embedding %d chunks...", len(split_docs))
        embeddings = self._create_embeddings()

        strategy = (
            DistanceStrategy.COSINE
            if self.distance_strategy.upper() == "COSINE"
            else DistanceStrategy.EUCLIDEAN_DISTANCE
        )

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
