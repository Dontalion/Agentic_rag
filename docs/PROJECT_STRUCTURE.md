# Agentic RAG – Project Structure

This document provides a clear overview of the project structure for developers and contributors who are new to the codebase.

## 1. Project Overview

**Agentic RAG** is a multi-agent Retrieval-Augmented Generation (RAG) system built with `smolagents`.  
It allows users to chat with their documents (PDF, TXT, MD) and optionally search the web for up-to-date information.

The system consists of specialized agents that work together under a manager agent:
- **RAG Agent**: Retrieves information from the local knowledge base (Qdrant).
- **Web Search Agent**: Fetches current information from the internet.
- **PDF Analyzer Agent**: Analyzes PDF files in detail (planned for Phase 2).

---

## 2. High-Level Directory Structure

```
Agentic_rag/
├── agentic_rag/                 # Main Python package
│   ├── agents/                  # Specialized agents (RAG, Web, PDF)
│   ├── tools/                   # Custom tools used by agents
│   ├── vectorstore/             # Document loading, splitting, and Qdrant integration
│   ├── utils/                   # back-end utilities 
│   ├── config/                  # Configuration and logging
│   ├── ui/                      # Streamlit web interface (Phase 1+)
│   ├── cli.py                   # Command-line interface entry point
│   ├── initialization.py        # RAG pipeline setup
│   └── __init__.py
├── docs/                        # Project documentation
├── knowledge_base/              # Default folder for user documents
├── uploads/                     # Temporary storage for uploaded files (gitignored)
├── main.py                      # Simple entry point
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Dependency list
└── README.md
```

---

## 3. Detailed Component Breakdown

### `agentic_rag/agents/`

Contains all specialized agents that perform specific tasks.

| File | Responsibility |
|------|----------------|
| `multi_agent_system.py` | Creates the main manager agent and orchestrates sub-agents |
| `rag_agent.py` | Agent responsible for retrieving information from the local vector database |
| `web_agent.py` | Agent that performs web searches using DuckDuckGo |
| `pdf_agent.py` | Agent for deep PDF analysis (uses `PDFAnalyzerTool`) |
| `advanced_retrieval_agent.py` | Alternative retrieval agent with more control |

### `agentic_rag/tools/`

Custom tools that agents can call. Each tool is a self-contained function with a clear description.

| File | Purpose |
|------|---------|
| `qdrant_retriever_tool.py` | Semantic search over the Qdrant vector store |
| `web_search_tool.py` | Performs web searches via DuckDuckGo |
| `visit_webpage.py` | Fetches and converts webpage content to clean text |
| `pdf_analyzer_tool.py` | Extracts and analyzes text from PDF files |
| `retriever_tool.py` | Legacy / basic retriever (kept for compatibility) |

### `agentic_rag/vectorstore/`

Handles everything related to documents and the vector database.

| File | Responsibility |
|------|----------------|
| `builder.py` | Builds and manages the Qdrant vector store |
| `loader.py` | Loads documents from directories or file lists |
| `file_loaders.py` | Low-level loaders for PDF, TXT, and Markdown files |
| `splitters.py` | Text chunking logic |
| `embeddings.py` | Embedding model management (currently `thenlper/gte-small`) |

### `agentic_rag/utils/`

Contains utility functions used in back-end layer.

| File | Responsibility |
|------|----------------|
| `vectorstore_add.py` | Incremental document addition helper (`add_documents_to_vectorstore`) – adds new documents to an existing Qdrant collection without rebuilding it |

### `agentic_rag/config/`

Central configuration and logging.

| File | Purpose |
|------|---------|
| `config.py` | Pydantic settings (model name, Qdrant URL, chunk size, etc.) |
| `logging_config.py` | Logger setup used across the project |

### `agentic_rag/ui/` (New – Phase 1)

Contains the Streamlit web interface.

| File / Folder | Purpose |
|---------------|---------|
| `app.py` | Main Streamlit application entry point |
| `utils/` | UI-only utilities |
| `components/` | Reusable UI components (sidebar, chat, uploader, source viewer) |

**`agentic_rag/ui/utils/` contents:**

| File | Responsibility |
|------|----------------|



### Root Files

| File | Description |
|------|-------------|
| `main.py` | Simple launcher that calls the CLI |
| `cli.py` | Interactive command-line interface for the multi-agent system |
| `initialization.py` | Builds the RAG pipeline (loads documents and creates Qdrant collection) |
| `pyproject.toml` | Project configuration (dependencies, scripts, package discovery) |

---

## 4. Data & Knowledge Folders

| Folder | Purpose |
|--------|---------|
| `knowledge_base/` | Default location where users place their documents (PDF, TXT, MD). The system loads from here when using the CLI. |
| `uploads/` | Temporary folder used by the Streamlit UI to store uploaded files during a session. This folder is listed in `.gitignore`. |

---

## 5. Documentation (`docs/`)

| File | Content |
|------|---------|
| `PROJECT_STRUCTURE.md` | This file – explains the codebase organization |
| `archive/` | Completed task documentation (e.g., `task-01-project-setup.md`) |

---

## 6. Key Technologies

- **smolagents** – Multi-agent framework
- **Qdrant** – Vector database (in-memory or Docker)
- **LangChain** – Document loading and text splitting
- **Streamlit** – Web UI (under development)
- **DuckDuckGo** – Web search (no API key required)

---

This structure keeps the codebase modular, testable, and easy to extend. Each folder has a single responsibility, making it straightforward for new contributors to understand where to make changes.