# Task 005: Phase 1 — Backend Agent Factories

**Date:** May 5, 2026  
**Status:** ✅ Completed  
**File:** `agentic_rag/utils/agents.py`

---

## Summary

Created backend agent factory functions for lazy agent creation.
UI only calls these functions and uses the returned agents — no agent logic in UI layer.

## Functions Implemented

| Function | Purpose |
|----------|---------|
| `get_rag_agent()` | Creates RAG agent (wraps `agents/rag_agent.py`) |
| `get_web_search_agent()` | Creates Web Search agent (wraps `agents/web_agent.py`) |
| `get_chat_manager()` | Creates manager with conditional sub-agents |

## Design Decisions

- `get_chat_manager()` conditionally includes agents:
  - RAG agent only if `qdrant_client`, `collection_name`, and `embeddings` are provided
  - Web Search agent only if `web_search_enabled=True`
- Reuses existing `create_rag_agent()` and `create_web_search_agent()` from `agents/`
- No PDF Analyzer agent (deferred to Phase 2)
- UI passes `model` from `ui/utils/caching.py` + vector store params → gets back a ready-to-use manager

## Next Step

Section 4: `ui/utils/session.py` — Session state management
