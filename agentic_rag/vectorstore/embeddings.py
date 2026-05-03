"""
Embedding model management.
Handles loading and caching of embedding models.
"""
from typing import Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


class EmbeddingManager:
    """Manages embedding model creation and lifecycle."""

    def __init__(self, embedding_model: Optional[str] = None):
        self.embedding_model = embedding_model or settings.embedding_model_name
        self._embeddings_cache = None

    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """
        Get or create the embedding model instance.
        
        Uses caching to avoid reloading the model multiple times.
        
        Returns:
            HuggingFaceEmbeddings instance.
        """
        if self._embeddings_cache is not None:
            logger.debug("Using cached embedding model: %s", self.embedding_model)
            return self._embeddings_cache

        logger.info("Loading embedding model: %s", self.embedding_model)
        self._embeddings_cache = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={"use_auth_token": settings.huggingface_token}
            if settings.huggingface_token
            else {},
        )
        return self._embeddings_cache

    def reset_cache(self) -> None:
        """Clear the cached embedding model to free memory."""
        logger.info("Clearing embedding model cache")
        self._embeddings_cache = None
