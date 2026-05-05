# Task 2: Core Utilities & Caching – Planned Structure

**Date:** May 5, 2026  
**Status:** Planning (Not Implemented Yet)  
**Phase:** 1 (MVP)

## Goal
Avoid creating a single large `utils.py` file. Instead, organize all UI utilities into a dedicated folder with small, focused, and clearly named files.

## New Folder Structure

```
agentic_rag/ui/
├── utils/
│   ├── __init__.py
│   ├── caching.py           # @st.cache_resource for heavy objects
│   ├── vectorstore.py       # Incremental document addition helper
│   ├── agents.py            # Lazy agent factory functions
│   └── chat.py              # Chat history and session state helpers
├── components/
├── app.py
└── ...
```

## File Responsibilities

### `caching.py`
- Contains all `@st.cache_resource` decorated functions.
- Responsibilities:
  - `get_qdrant_client()`
  - `get_embeddings()`
  - `get_llm_model()`
- Keeps heavy objects (Qdrant client, embedding model, LLM) cached across reruns.

### `vectorstore.py`
- Contains the **new helper function** for adding documents incrementally.
- New function to be added in `agentic_rag/vectorstore/builder.py`:
  - `add_documents_to_vectorstore(client, collection_name, docs) -> int`
- UI wrapper: `add_documents_incrementally(docs)`
- Handles splitting + embedding + upsert into existing collection (no rebuild).

### `agents.py`
- Lazy creation of agents (only when needed).
- Functions:
  - `get_rag_agent(...)`
  - `get_web_search_agent(...)`
  - `get_chat_manager(web_search_enabled: bool)`
- Uses cached objects from `caching.py`.

### `chat.py`
- Manages chat-related session state.
- Functions:
  - `reset_chat_history()`
  - `get_indexed_documents_metadata()`
  - `add_user_message(...)`
  - `add_assistant_message(...)`

## Why This Structure?
- Each file has a single responsibility.
- File names clearly indicate their purpose.
- Easy to maintain and extend in future phases.
- Follows the "small focused files" principle requested.

## Next Steps After Approval
1. Implement the new helper `add_documents_to_vectorstore()` in `vectorstore/builder.py`.
2. Create the four files inside `agentic_rag/ui/utils/`.
3. Update `PROJECT_STRUCTURE.md`.
4. Archive this task summary.

**This document serves as the reference for implementing Task 2.**