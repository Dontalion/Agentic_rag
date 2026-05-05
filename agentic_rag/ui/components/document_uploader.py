"""
Document uploader component for the Streamlit UI.

Allows users to upload local files (PDF, TXT, MD) and add web pages via URL.
All uploaded documents are indexed into the Qdrant vector store.
"""

import os
import tempfile
from pathlib import Path

import streamlit as st
from langchain_core.documents import Document
from agentic_rag.ui.utils.caching import get_qdrant_client
from agentic_rag.utils.vectorstore import add_documents_to_vectorstore, ensure_collection_exists
from agentic_rag.vectorstore.file_loaders import load_single_file
from agentic_rag.tools.visit_webpage import visit_webpage


def render_document_uploader() -> None:
    """
    Render the document uploader with file upload and URL input sections.
    """
    st.subheader("📤 Add Documents")

    # File upload section
    _render_file_uploader()

    st.divider()

    # Web page section
    _render_web_page_uploader()


def _render_file_uploader() -> None:
    """
    Render the file uploader for local documents.
    """
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if _is_already_indexed(uploaded_file.name):
                st.info(f"⏭️ `{uploaded_file.name}` is already indexed.")
                continue

            if st.button(f"Index `{uploaded_file.name}`", key=f"btn_{uploaded_file.name}"):
                _index_file(uploaded_file)


def _render_web_page_uploader() -> None:
    """
    Render the web page URL input and index button.
    """
    st.subheader("🌐 Add Web Page")
    url = st.text_input("URL", placeholder="https://example.com/article", label_visibility="collapsed")

    if url and st.button("Fetch & Index", use_container_width=True):
        _index_web_page(url)


def _is_already_indexed(filename: str) -> bool:
    """
    Check if a file is already indexed in the vector store.

    Args:
        filename: Name of the file to check.

    Returns:
        True if already indexed, False otherwise.
    """
    client = get_qdrant_client()
    collections = client.get_collections().collections
    collection_name = "agentic_rag"

    existing = [c.name for c in collections]
    if collection_name not in existing:
        return False

    # Scroll through points to check for matching source
    offset = None
    while True:
        points, next_offset = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        for point in points:
            payload = point.payload or {}
            source = payload.get("source", "")
            if filename in source:
                return True

        if next_offset is None:
            break
        offset = next_offset

    return False


def _index_file(uploaded_file) -> None:
    """
    Index an uploaded file into the vector store.

    Args:
        uploaded_file: Streamlit UploadedFile object.
    """
    with st.spinner(f"Processing `{uploaded_file.name}`..."):
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=Path(uploaded_file.name).suffix,
            ) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            # Load and create document
            doc = load_single_file(tmp_path)
            doc.metadata["type"] = Path(uploaded_file.name).suffix.lower().lstrip(".")

            # Ensure collection exists and add
            client = get_qdrant_client()
            ensure_collection_exists(client)
            chunks_added = add_documents_to_vectorstore(client, [doc])

            # Cleanup
            os.unlink(tmp_path)

            st.success(f"✅ Indexed `{uploaded_file.name}` ({chunks_added} chunks)")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Failed to index `{uploaded_file.name}`: {e}")


def _index_web_page(url: str) -> None:
    """
    Fetch and index a web page.

    Args:
        url: URL of the web page to index.
    """
    with st.spinner(f"Fetching `{url}`..."):
        try:
            # Fetch webpage content
            content = visit_webpage(url)

            if content.startswith("Error"):
                st.error(f"❌ {content}")
                return

            # Create document
            doc = Document(
                page_content=content,
                metadata={"source": url, "type": "web"},
            )

            # Ensure collection exists and add
            client = get_qdrant_client()
            ensure_collection_exists(client)
            chunks_added = add_documents_to_vectorstore(client, [doc])

            st.success(f"✅ Indexed web page ({chunks_added} chunks)")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Failed to index web page: {e}")
