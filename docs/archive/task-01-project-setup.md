# Task 1: Project Setup

**Date:** May 5, 2026  
**Status:** Completed  
**Phase:** 1 (MVP – Chat with Documents)

## Objective
Prepare the project structure and dependencies for Streamlit UI development. Create the base folder layout and initial `app.py` skeleton.

## Changes Made

### 1. Dependencies
- Added `streamlit>=1.32.0` to `pyproject.toml`

### 2. Git Configuration
- Added `uploads/` to `.gitignore` (temporary storage for uploaded files)

### 3. Folder Structure Created
```
agentic_rag/
├── ui/
│   ├── __init__.py
│   ├── app.py
│   └── components/
│       └── __init__.py
└── uploads/
    └── .gitkeep
```

### 4. New Files
| File | Purpose |
|------|---------|
| `agentic_rag/ui/__init__.py` | UI package initializer |
| `agentic_rag/ui/components/__init__.py` | Components package initializer |
| `agentic_rag/ui/app.py` | Main Streamlit entry point (page config + two-column layout) |
| `uploads/.gitkeep` | Keeps the uploads folder tracked in git |

### 5. Initial UI Layout
- Page title: "Agentic RAG"
- Wide layout with two columns:
  - Left (3/4): Chat area (placeholder)
  - Right (1/4): Sources area (placeholder)

## Result
Project is now ready for Streamlit development. Running `streamlit run agentic_rag/ui/app.py` shows a clean English interface with placeholders for future components.
