"""
File loaders for different document formats.
Handles PDF, TXT, and Markdown files independently.
"""
import os
from pathlib import Path
from typing import Optional

from langchain_core.documents import Document
from pypdf import PdfReader
from agentic_rag.config.logging_config import get_logger

logger = get_logger(__name__)


def load_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        file_path: Path to the PDF file.
    
    Returns:
        Extracted text from all pages.
    """
    logger.info("Loading PDF: %s", file_path)
    reader = PdfReader(file_path)
    text_parts = []
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
        else:
            logger.warning("No text extracted from page %d of %s", page_num + 1, file_path)
    
    return "\n\n".join(text_parts)


def load_text_file(file_path: str) -> str:
    """
    Read content from a plain text or markdown file.
    
    Args:
        file_path: Path to the text/markdown file.
    
    Returns:
        File content as string.
    """
    logger.info("Loading text file: %s", file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_single_file(file_path: str) -> Document:
    """
    Load a single file and return it as a Document.
    
    Supports: PDF, TXT, MD files.

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
    supported_extensions = {".pdf", ".txt", ".md"}
    
    if ext not in supported_extensions:
        raise ValueError(
            f"Unsupported file extension '{ext}'. Supported: {supported_extensions}"
        )

    if ext == ".pdf":
        content = load_pdf(file_path)
    else:
        content = load_text_file(file_path)

    return Document(
        page_content=content,
        metadata={"source": file_path, "filename": os.path.basename(file_path)},
    )
