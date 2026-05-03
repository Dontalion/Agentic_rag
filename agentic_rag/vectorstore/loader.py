"""
Main document loader interface.
Handles loading documents from directories and multiple sources.

Delegates file format-specific logic to file_loaders module.
"""
import os
from pathlib import Path
from typing import List, Union

from langchain_core.documents import Document
from agentic_rag.config.logging_config import get_logger
from agentic_rag.vectorstore.file_loaders import load_single_file

logger = get_logger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


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
                doc = load_single_file(str(file_path))
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
        logger.info("Loaded %d documents from legacy format", len(source_docs))
        return source_docs

    # Single directory path
    if isinstance(knowledge_base, str):
        return load_directory(knowledge_base)

    # List of file paths
    if isinstance(knowledge_base, list):
        all_docs = []
        for path in knowledge_base:
            try:
                if os.path.isdir(path):
                    all_docs.extend(load_directory(path))
                else:
                    all_docs.append(load_single_file(path))
            except Exception as e:
                logger.warning("Failed to load %s: %s", path, e)
        
        logger.info("Loaded %d documents from file list", len(all_docs))
        return all_docs

    raise ValueError(
        f"Unsupported knowledge_base type: {type(knowledge_base)}. "
        "Expected: dict list, directory path, or file paths list"
    )
