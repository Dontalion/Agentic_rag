"""
Document loader for the vector store.
Supports PDF, TXT, and MD files.
"""
import os
from pathlib import Path
from typing import List, Union

from langchain_core.documents import Document
from pypdf import PdfReader
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def _load_pdf(file_path: str) -> str:
    """Extract text content from a PDF file."""
    reader = PdfReader(file_path)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n\n".join(text_parts)


def _load_text_file(file_path: str) -> str:
    """Read content from a plain text or markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_file(file_path: str) -> Document:
    """
    Load a single file and return it as a Document.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        A Document object with the file content and metadata.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is not supported.
    """
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = Path(file_path).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension '{ext}'. Supported: {SUPPORTED_EXTENSIONS}"
        )

    if ext == ".pdf":
        content = _load_pdf(file_path)
    else:
        content = _load_text_file(file_path)

    return Document(
        page_content=content,
        metadata={"source": file_path, "filename": os.path.basename(file_path)},
    )


def load_directory(directory_path: str, recursive: bool = True) -> List[Document]:
    """
    Load all supported files from a directory.

    Args:
        directory_path: Path to the directory containing documents.
        recursive: Whether to search subdirectories recursively.

    Returns:
        List of Document objects.
    """
    directory_path = os.path.abspath(directory_path)

    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Directory not found: {directory_path}")

    documents = []
    pattern = "**/*" if recursive else "*"
    for file_path in Path(directory_path).glob(pattern):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                doc = load_file(str(file_path))
                documents.append(doc)
                logger.info("Loaded: %s", file_path)
            except Exception as e:
                logger.warning("Failed to load %s: %s", file_path, e)

    logger.info("Loaded %d documents from %s", len(documents), directory_path)
    return documents


def load_documents(knowledge_base: Union[List[dict], str, List[str]]) -> List[Document]:
    """
    Load documents from various sources:
    - List of dicts with 'text' and 'source' keys (legacy support)
    - A single directory path (string)
    - A list of file paths (list of strings)

    Args:
        knowledge_base: Source of documents to load.

    Returns:
        List of Document objects.
    """
    # Legacy support: list of dicts
    if isinstance(knowledge_base, list) and knowledge_base and isinstance(knowledge_base[0], dict):
        source_docs = [
            Document(
                page_content=doc["text"],
                metadata={"source": doc["source"], "filename": doc["source"].split("/")[-1]},
            )
            for doc in knowledge_base
        ]
        return source_docs

    # Single directory path
    if isinstance(knowledge_base, str):
        return load_directory(knowledge_base)

    # List of file paths
    if isinstance(knowledge_base, list) and isinstance(knowledge_base[0], str):
        documents = []
        for file_path in knowledge_base:
            try:
                doc = load_file(file_path)
                documents.append(doc)
            except Exception as e:
                logger.warning("Failed to load %s: %s", file_path, e)
        return documents

    raise ValueError(
        "knowledge_base must be a list of dicts, a directory path, or a list of file paths"
    )
