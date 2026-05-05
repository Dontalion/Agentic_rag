# Task 2: Common Utilities Structure (Revised)

**Date:** May 5, 2026  
**Status:** Structure Created  
**Phase:** 1 (MVP)

## Objective
Separate shared utilities from UI-specific utilities to keep the codebase clean and maintainable.

## New Folder Structure

```
agentic_rag/
├── common/                      # Shared utilities (CLI + UI)
│   └── __init__.py
├── vectorstore/
│   ├── builder.py
│   ├── utils.py                 # Shared vector store helpers (e.g. incremental add)
│   └── ...
├── ui/
│   ├── utils/                   # UI-only utilities
│   │   ├── __init__.py
│   │   ├── caching.py           # @st.cache_resource (Qdrant, embeddings, model)
│   │   ├── agents.py            # Lazy agent factories
│   │   ├── chat.py              # Chat session state
│   │   └── vectorstore.py       # UI wrapper around shared vectorstore/utils.py
│   └── ...
└── ...
```

## Design Principles

1. **Shared Layer (`agentic_rag/vectorstore/utils.py`)**
   - Contains logic that both CLI and UI need.
   - Example: `add_documents_to_vectorstore()` – incremental document addition.
   - No Streamlit dependencies allowed here.

2. **UI Layer (`agentic_rag/ui/utils/`)**
   - Contains only Streamlit-specific code.
   - Uses `@st.cache_resource`.
   - Wraps shared helpers when needed (e.g., `ui/utils/vectorstore.py` calls `vectorstore/utils.py`).

3. **Small Focused Files**
   - Each file has one clear responsibility.
   - File names clearly indicate their domain.

## Files Created in This Task

| File | Purpose |
|------|---------|
| `agentic_rag/common/__init__.py` | Package initializer for future shared utilities |
| `agentic_rag/vectorstore/utils.py` | Shared vector store helper (`add_documents_to_vectorstore`) |
| `agentic_rag/ui/utils/__init__.py` | UI utilities package initializer |

## Next Steps

- Implement `caching.py`, `agents.py`, `chat.py`, and `ui/utils/vectorstore.py` one file at a time.
- Update `PROJECT_STRUCTURE.md` after each file is added.
- Archive each small task separately.

This structure ensures that:
- The CLI remains untouched and lightweight.
- The UI can safely use Streamlit caching.
- Shared logic lives in one place and is easy to test.