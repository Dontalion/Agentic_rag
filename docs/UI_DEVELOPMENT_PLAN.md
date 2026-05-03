# Agentic RAG - Streamlit UI Development Plan

**Repository:** Agentic_rag  
**Date:** May 3, 2026  
**Status:** Planning Phase  
**Language:** English

---

## 1. Project Goals

Build a modern, user-friendly Streamlit web interface for the existing Agentic RAG multi-agent system with the following priorities:

1. **Primary Goal (Phase 1):** Enable users to **chat with documents** (uploaded files + web content).
2. Support both local documents and web-retrieved content in a unified chat experience.
3. Provide clear source attribution with hover/click interactions.
4. Maintain chat history (session + per-conversation).
5. Keep the system lightweight and suitable for both testing (in-memory) and production (Docker).

---

## 2. Agreed UI Structure

We will follow this folder structure:

```
agentic_rag/
├── ui/
│   ├── __init__.py
│   ├── app.py                      # Main Streamlit entry point
│   ├── components/
│   │   ├── chat_interface.py       # Main chat + message rendering
│   │   ├── sidebar.py              # Settings, toggles, document list
│   │   ├── document_uploader.py    # File + URL upload handler
│   │   └── source_viewer.py        # Side panel for document/web source
│   └── utils.py                    # Session state helpers, caching
├── agents/
├── tools/
├── vectorstore/
└── ...
```

**Entry point:** `streamlit run agentic_rag/ui/app.py`

---

## 3. Core Design Decisions (Based on User Feedback)

| # | Decision | Details |
|---|----------|---------|
| 1 | **No Docker mode selector in UI** | UI will always use the current Qdrant mode (memory for testing, Docker when running via compose). No UI toggle. |
| 2 | **Lazy agent loading** | Do **not** load all agents at startup. Load RAG agent when documents exist. Load Web Search agent only when the "Enable Web Search" toggle is ON. |
| 3 | **Unified "Chat with Documents"** | No separate "Chat with PDF" mode. One chat interface that works with any document type (PDF, TXT, MD, web pages). |
| 4 | **User modes (via toggle)** | - Mode A: Chat only with uploaded documents (RAG only)<br>- Mode B: Chat with documents + web search (RAG + Web agent) |
| 5 | **Source interaction** | When model cites a source:<br>- Hover → show source title/URL/snippet<br>- Click → open in side panel (PDF with highlight) or new browser tab (web) |
| 6 | **Process once on upload** | Every uploaded file (or web URL) is processed **exactly once** immediately after upload and added to the vector store. No manual "Rebuild" button needed. |
| 7 | **Chat History** | Support full conversation history within a session + ability to start new chats. |
| 8 | **No "no documents" state** | The system always expects documents. If none exist, the UI should guide the user to upload or search the web first. |
| 9 | **No disk persistence** | Qdrant remains in-memory (`:memory:`) for this phase. |
| 10 | **PDFAnalyzerTool clarification needed** | See section 6. |

---

## 4. Development Phases & Task Breakdown

### Phase 1: MVP – Chat with Documents (Current Focus)

**Goal:** User can upload documents (files + URLs), chat with them, get sourced answers, and see sources on click/hover.

#### Sub-Tasks (Small & Incremental)

**1.1 Project Setup**
- Add `streamlit` and `streamlit-extras` (or `streamlit-chat`) to `pyproject.toml` and `requirements.txt`.
- Create `agentic_rag/ui/` folder and basic `__init__.py`.
- Create `agentic_rag/ui/app.py` with basic page config and title.

**1.2 Session State & Caching Design**
- Design `st.session_state` structure:
  - `messages`: list of chat messages
  - `qdrant_client`, `collection_name`, `embeddings`
  - `multi_agent_manager` (or dynamic agents)
  - `uploaded_documents`: list of processed docs metadata
  - `web_search_enabled`: bool toggle
- Use `@st.cache_resource` for heavy objects (Qdrant client, embeddings, model).

**1.3 Document Uploader Component**
- Create `components/document_uploader.py`
- Support:
  - File upload (PDF, TXT, MD, etc.)
  - URL input (web page)
- On upload:
  - Save file temporarily or process in-memory
  - Call existing `load_documents` + `build_vectorstore` logic
  - Add to Qdrant **only once**
  - Show success message + document list in sidebar

**1.4 Basic Chat Interface**
- Create `components/chat_interface.py`
- Use `st.chat_input` + `st.chat_message`
- On user message:
  - If `web_search_enabled` → use manager with RAG + Web agents
  - Else → use RAG-only agent (or direct retriever + LLM)
- Display assistant response with basic source citations (text links first)

**1.5 Sidebar**
- Create `components/sidebar.py`
- Show:
  - List of uploaded documents (with remove option?)
  - Toggle: "Enable Web Search"
  - Current collection stats (number of chunks)
  - Button: "Clear Chat History"
  - Settings info (model name, embedding model)

**1.6 Source Viewer (Basic Version)**
- Create `components/source_viewer.py`
- For now: Show source text in an expander or side column when user clicks a citation.
- Later: PDF highlight + web browser open.

**1.7 Integration with Existing Agents**
- Modify or wrap `create_multi_agent_system` so it can be called with only RAG agent or RAG + Web agent dynamically.
- Avoid loading PDF agent unless explicitly needed (Phase 2).

**1.8 Basic Source Citation Rendering**
- Update `AdvancedQdrantRetrieverTool` or add metadata so responses include source references (chunk id, file name, page, score).
- Render citations in chat as `[1]`, `[2]` with hover text.

**1.9 Testing & Polish**
- Test end-to-end flow: upload PDF → chat → get sourced answer.
- Handle empty knowledge base gracefully (prompt user to upload).
- Add loading spinners during retrieval and generation.

---

### Phase 2 (Future)

- Advanced source viewer (PDF highlight in side panel, web page preview)
- Full chat history persistence (save/load conversations)
- Multiple chat sessions (like ChatGPT)
- Streaming responses
- PDF Analyzer integration for direct PDF Q&A
- Web page content extraction and chatting with live websites
- Better error handling and logging in UI

---

## 5. Technical Implementation Notes

- **Lazy Agent Creation:** We will create a helper function `get_or_create_rag_agent(...)` and `get_or_create_web_agent(...)` that are cached and only instantiated when first needed.
- **Vector Store Lifecycle:** One Qdrant client per Streamlit session (cached). Documents added incrementally.
- **File Handling:** Uploaded files will be saved to a temporary `uploads/` folder or processed directly from `UploadedFile` bytes to avoid disk writes where possible.
- **Model Access:** Model is created via `InferenceClientModel`. We will cache it.
- **Styling:** Use Streamlit's native theming + light custom CSS for source highlights.

---

## 6. Clarifications Needed (Especially Point 11)

### Regarding PDFAnalyzerTool

The current `PDFAnalyzerTool` in `agentic_rag/tools/pdf_analyzer_tool.py` expects a **file path** on disk.

In Streamlit:
- `st.file_uploader` returns a `UploadedFile` object (in-memory bytes).
- We have two options:

**Option A (Simple):** Save the uploaded file to a temp directory, then pass the path to `PDFAnalyzerTool`. Clean up after use.

**Option B (Cleaner):** Extend `PDFAnalyzerTool` (or create a new version) to accept:
- `bytes`
- `file-like object`
- or `UploadedFile`

This would allow direct in-memory PDF parsing using `pypdf` without writing to disk.

**Question for you:**
Which approach do you prefer for Phase 1?

- Use Option A (temp files) for speed of development, or
- Implement Option B (in-memory) from the beginning?

Also, do you want the PDF Analyzer agent to be available in the first chat UI, or should we keep the initial focus strictly on the RAG retriever + web search?

---

## 7. Next Steps

1. Review and approve this plan.
2. Confirm the clarification in Section 6.
3. I will then start **Task 1.1** (Project Setup) and show the exact code changes before applying them.
4. We proceed feature-by-feature, with your approval at each major step.

---

**Ready to begin when you approve.** Please reply with any changes or "Approved – start with Phase 1".