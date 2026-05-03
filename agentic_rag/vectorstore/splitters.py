"""
Text splitting and tokenization utilities.
Handles document chunking with tokenizer-aware splitting.
"""
from typing import Optional

from tqdm import tqdm
from transformers import AutoTokenizer
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


class TextSplitterManager:
    """Manages document splitting with tokenizer awareness."""

    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        tokenizer_model: Optional[str] = None,
    ):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        self.tokenizer_model = tokenizer_model or settings.tokenizer_model_name

    def create_splitter(self) -> RecursiveCharacterTextSplitter:
        """
        Create a text splitter using the configured tokenizer.
        
        Returns:
            RecursiveCharacterTextSplitter instance.
        """
        logger.info("Creating text splitter with model: %s", self.tokenizer_model)
        tokenizer = AutoTokenizer.from_pretrained(
            self.tokenizer_model,
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

    def split_documents(self, docs: list[Document]) -> list[Document]:
        """
        Split documents into chunks, keeping only unique content.

        Args:
            docs: List of Document objects to split.

        Returns:
            List of Document chunks with duplicates removed.
        """
        logger.info("Splitting %d documents...", len(docs))
        splitter = self.create_splitter()

        processed = []
        seen = set()
        for doc in tqdm(docs, desc="Splitting"):
            for chunk in splitter.split_documents([doc]):
                if chunk.page_content not in seen:
                    seen.add(chunk.page_content)
                    processed.append(chunk)

        logger.info("Produced %d unique chunks", len(processed))
        return processed
