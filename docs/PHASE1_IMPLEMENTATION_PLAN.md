# Phase 1 Implementation Plan: Chat with Documents (MVP)

**Repository:** Agentic_rag  
**Branch:** main  
**Date:** May 5, 2026  
**Focus:** Unified document chat experience (local files + web content)  
**Status:** Ready for incremental development

---

## 1. Phase 1 Objectives (MVP)

The goal of Phase 1 is to deliver a working Streamlit UI where users can:

- Upload local documents (PDF, TXT, MD)
- Add web pages via URL (fetch and index content)
- Chat with the uploaded/indexed documents using the RAG system
- Optionally enable web search during chat (RAG + Web Search Agent)
- See clear source citations in answers
- Click on citations to view the source content (basic version: expander or side panel)
- Maintain chat history within the session
- All documents are processed **exactly once** upon upload/indexing

**Out of Scope for Phase 1:**
- PDF Analyzer Agent (deferred to Phase 2)
- Advanced PDF highlighting in side panel
- Multiple saved chat sessions / persistence of history
- Streaming responses
- Disk-persisted Qdrant
- Docker mode selector in UI

---

## 2. Final UI Structure (Phase 1)

```
agentic_rag/
├── ui/
│   ├── __init__.py
│   ├── app.py
│   ├── utils.py                    # Caching, session state helpers, agent factories
│   └── components/
│       ├── __init__.py
│       ├── sidebar.py              # Document list, web toggle, stats, new chat
│       ├── document_uploader.py    # File upload + URL input
│       ├── chat_interface.py       # Main chat messages + input
│       └── source_viewer.py        # Basic source display (expander / columns)
├── vectorstore/                    # (existing - may need small enhancements)
├── agents/                         # (existing - will add lazy factory helpers)
└── tools/                          # (existing - may enhance retriever metadata)
```

**Run command:** `streamlit run agentic_rag/ui/app.py`

---

## 3. Key Technical Decisions

| Area | Decision for Phase 1 |
|------|----------------------|
| **Qdrant Mode** | Always use current mode from `settings.qdrant_url` (memory or Docker). No UI selector. |
| **Agent Loading** | Fully lazy. RAG agent created only when first document is indexed. Web Search agent created only when toggle is ON. |
| **Vector Store Updates** | Support **incremental addition**. Documents are added to existing collection without recreating it. |
| **Document Processing** | Every file/URL is processed **once** on upload. No "Rebuild" button. |
| **Chat Modes** | Single toggle: "Enable Web Search". When OFF → RAG only. When ON → RAG + Web agent. |
| **Source Citations** | Basic text citations `[1]`, `[2]` with hover tooltip. Clicking opens source in sidebar/expander. |
| **File Handling** | Uploaded files saved to temporary `uploads/` folder (added to `.gitignore`). |
| **Web Page Indexing** | Support adding web pages via URL using `markdownify` + existing `visit_webpage` logic. |
| **PDF Analyzer** | **Not included** in Phase 1 chat. Deferred to Phase 2. |
| **Dependencies** | Add `streamlit` (and optionally `streamlit-extras` for better tooltips). |

---

## 4. Detailed Task Breakdown (Implement One by One)

We will implement tasks **sequentially**. After each task is completed and tested, we move to the next only after your approval.

### Task 1: Project Setup & Dependencies

**Goal:** Prepare the project for Streamlit development.

**Actions:**
1. Add `streamlit` to `[project.dependencies]` in `pyproject.toml`.
2. (Optional) Add `streamlit-extras` for nice tooltips/hovers.
3. Update `requirements.txt` accordingly.
4. Create folder structure:
   - `agentic_rag/ui/`
   - `agentic_rag/ui/components/`
5. Create empty `__init__.py` files.
6. Create `agentic_rag/ui/app.py` with:
   - `st.set_page_config(...)`
   - Title: "Agentic RAG - Chat with Documents"
   - Basic layout (two columns: chat + sidebar)

**Files to edit/create:**
- `pyproject.toml`
- `requirements.txt`
- `agentic_rag/ui/__init__.py` (new)
- `agentic_rag/ui/components/__init__.py` (new)
- `agentic_rag/ui/app.py` (new)

**Success Criteria:** Running `streamlit run agentic_rag/ui/app.py` shows a clean page with title and sidebar.

---

### Task 2: Core Utilities & Caching (`utils.py`)

**Goal:** Centralize all heavy object creation and session state management.

**Key Functions to implement in `agentic_rag/ui/utils.py`:**

- `get_settings()` → cached
- `get_qdrant_client()` → `@st.cache_resource`
- `get_embeddings()` → `@st.cache_resource`
- `get_llm_model()` → `@st.cache_resource` (InferenceClientModel)
- `ensure_collection_exists(client, collection_name)` 
- `add_documents_to_vectorstore(docs: List[Document])` → incremental add (uses `Qdrant.add_documents` or direct upsert)
- `get_rag_agent()` → lazy creation of RAG agent (only if collection has documents)
- `get_web_search_agent()` → lazy creation
- `get_chat_manager(web_search_enabled: bool)` → creates manager with appropriate agents
- `reset_chat_history()`
- `get_uploaded_documents_metadata()` → list of sources from collection

**Important Enhancement Needed:**
Current `VectorStoreBuilder.build()` always creates a fresh collection. We need a new function (or extend the builder) that supports adding documents to an **existing** collection.

**Files:**
- `agentic_rag/ui/utils.py` (new)
- Possibly small update in `agentic_rag/vectorstore/builder.py` or new helper in `vectorstore/`

**Success Criteria:** All heavy objects are cached. Calling `get_chat_manager(False)` returns a manager with only RAG agent when documents exist.

---

### Task 3: Document Uploader Component

**Goal:** Allow users to add documents (files + URLs) that are indexed exactly once.

**Features:**
- `st.file_uploader` supporting multiple files (PDF, TXT, MD)
- Separate section: "Add Web Page" with `st.text_input` for URL + "Fetch & Index" button
- On upload/fetch:
  1. Save file to `uploads/` (or process bytes for files)
  2. Use existing `load_single_file` (for local) or create web document (for URL)
  3. Call `add_documents_to_vectorstore()`
  4. Show success + update document list in sidebar
- Display list of indexed documents in sidebar (filename + type + chunk count if possible)

**Files:**
- `agentic_rag/ui/components/document_uploader.py` (new)
- Update `agentic_rag/ui/components/sidebar.py` (will be created in Task 4)

**Note on Web Pages:** We will reuse logic from `visit_webpage` + `markdownify` to convert page to clean text, then create a `Document` with `metadata={"source": url, "type": "web"}`.

**Success Criteria:** User can upload a PDF → it appears in document list → chunks are added to Qdrant.

---

### Task 4: Sidebar Component

**Goal:** Provide controls and visibility.

**Contents:**
- Header: "Knowledge Base"
- List of indexed documents (with remove option? — simple version: just list)
- Toggle switch: `st.toggle("Enable Web Search", value=False)`
- Stats: "X documents • Y chunks"
- Button: "New Chat" (clears `st.session_state.messages`)
- Model info (read from settings, non-editable in Phase 1)

**Files:**
- `agentic_rag/ui/components/sidebar.py` (new)

**Success Criteria:** Sidebar updates live when documents are added. Toggle changes chat behavior.

---

### Task 5: Chat Interface (RAG Only First)

**Goal:** Working chat using only RAG agent.

**Implementation:**
- Use `st.chat_message` and `st.chat_input`
- Maintain `st.session_state.messages`
- On user input:
  - If no documents indexed → show friendly message "Please upload documents first"
  - Else → get RAG-only manager → `manager.run(user_input)`
  - Display assistant message
- Show "Thinking..." spinner during agent execution

**Files:**
- `agentic_rag/ui/components/chat_interface.py` (new)
- Update `app.py` to compose sidebar + chat

**Success Criteria:** Upload PDF → ask a question about its content → get relevant answer with citations.

---

### Task 6: Add Web Search Toggle & Dynamic Agents

**Goal:** When toggle is ON, include Web Search agent in the manager.

**Changes:**
- In `get_chat_manager(web_search_enabled)`, conditionally add web agent
- Update chat logic to pass the toggle state
- When web search is enabled, answers can include both local sources and fresh web results

**Files:**
- Update `agentic_rag/ui/utils.py`
- Update `chat_interface.py`

**Success Criteria:** With toggle OFF → answers only from uploaded docs. With toggle ON → answers can reference web results too.

---

### Task 7: Basic Source Citation & Viewer

**Goal:** Make sources visible and clickable.

**Steps:**
1. **Enhance Retriever Tool Output** (small change in `AdvancedQdrantRetrieverTool`):
   - Return richer information including `filename`, `source`, `score`, and a short snippet.
   - Or return structured data that the agent can cite as `[1] Document: filename.pdf (score: 0.92)`

2. **In Chat Interface:**
   - Parse citations from the final answer
   - Render them as clickable elements (use `st.markdown` with HTML or `st.button` styled as links)
   - On click → open `source_viewer`

3. **Source Viewer (Basic):**
   - Use `st.columns` or `st.expander` in the main area, or a dedicated right column
   - Show full text of the cited chunk + metadata
   - For web sources: show URL (clickable to open in new tab)

**Files:**
- `agentic_rag/tools/qdrant_retriever_tool.py` (small enhancement)
- `agentic_rag/ui/components/source_viewer.py` (new)
- `agentic_rag/ui/components/chat_interface.py` (citation rendering)

**Success Criteria:** Model answer contains `[1]`, `[2]`. Clicking them shows the source content.

---

### Task 8: Polish, Error Handling & Final Testing

**Goal:** Make the UI robust and user-friendly.

**Items:**
- Graceful handling when no HF token is set (show clear error)
- Loading spinners on upload and during generation
- Clear "Processing document..." messages
- Prevent duplicate indexing of the same file/URL (simple check by source)
- Responsive layout (chat takes most space, sidebar on left)
- Add basic custom CSS for better citation styling (via `st.markdown`)
- Test end-to-end flow multiple times
- Ensure CLI (`python -m agentic_rag.cli`) still works unchanged

**Files:** Minor updates across UI files + possibly `.gitignore` (add `uploads/`)

**Success Criteria:** The app feels polished. A new user can upload a document and start chatting within 30 seconds.

---

## 5. Order of Implementation (Recommended)

1. Task 1 (Setup)
2. Task 2 (Utils & Caching) — **critical foundation**
3. Task 3 (Document Uploader)
4. Task 4 (Sidebar)
5. Task 5 (Chat - RAG only)
6. Task 6 (Web Search toggle)
7. Task 7 (Source citations)
8. Task 8 (Polish)

We will **not** skip ahead. Each task will be planned, shown to you, approved, then implemented.

---

## 6. Open Questions / Decisions Before Starting

1. **Web Page Indexing:** Should we automatically index the top search results when web search is enabled, or only when user explicitly clicks "Add to Knowledge Base" on a search result? (Recommendation: explicit for Phase 1)

2. **Citation Style:** Do you want citations to appear as numbered superscripts `[1]` or as nice pills/badges?

3. **Temporary Upload Folder:** Should we create `uploads/` in the project root and add it to `.gitignore`?

4. **Source Viewer Location:** For Phase 1, do you prefer:
   - A right-side column that appears when a citation is clicked, or
   - An expander below the answer message?

Please confirm these (or suggest alternatives) so I can proceed with Task 1 confidently.

---

## 7. Next Step

Once you approve this plan and answer the questions above, I will:

1. Show the **exact code changes** for **Task 1: Project Setup**
2. Wait for your approval
3. Apply the changes
4. Move to Task 2

**Ready when you are.** Please reply with "Approved – start Task 1" (and answers to the 4 questions if you have preferences).