# Task 2: Restructure – Shared Utilities Folder

**Date:** May 5, 2026  
**Status:** Completed  
**Phase:** 1 (MVP)

## Objective
Reorganize the shared utilities according to the user's exact instructions:
- Rename the `common` folder to `utils`
- Move the shared vector store helper file into this folder
- Rename the helper file to clearly reflect its purpose (short and descriptive)
- Update all project documentation accordingly
- Archive the changes

## Changes Performed

### 1. Folder Rename
- `agentic_rag/common/` → `agentic_rag/utils/`

### 2. File Relocation and Rename
- `agentic_rag/vectorstore/utils.py` → `agentic_rag/utils/vectorstore_add.py`

**New file name explanation:**
- `vectorstore_add.py` clearly indicates that the file provides an "add" (incremental) operation for the vector store.
- The name is short, descriptive, and follows the "small focused files" principle.

### 3. Documentation Updates
- Updated `docs/PROJECT_STRUCTURE.md`:
  - Added `utils/` to the high-level directory tree
  - Replaced the old `vectorstore/utils.py` entry with the new `utils/vectorstore_add.py`
  - Updated the `ui/utils/` section to reference the correct shared path (`agentic_rag/utils/vectorstore_add.py`)
  - Added a dedicated section for `agentic_rag/utils/`

### 4. Archive
- Created this file: `docs/archive/task-02-restructure.md`

## Final Structure (Relevant Parts)

```
agentic_rag/
├── utils/
│   ├── __init__.py
│   └── vectorstore_add.py          # Shared helper: add_documents_to_vectorstore()
├── vectorstore/
│   ├── builder.py
│   ├── loader.py
│   └── ...
├── ui/
│   ├── utils/
│   │   ├── caching.py
│   │   ├── vectorstore.py          # UI wrapper around shared helper
│   │   └── ...
│   └── ...
└── ...
```

## Result
The project now has a clean separation:
- `agentic_rag/utils/` → Shared utilities (CLI + UI)
- `agentic_rag/ui/utils/` → UI-only utilities (Streamlit-specific)

All documentation reflects the new structure. No heavy implementation was done — only structural changes as requested.

## Next
Continue with small, focused implementation tasks (e.g., `caching.py`) one file at a time.