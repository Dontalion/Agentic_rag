# Agentic_rag

A Multi-Agent RAG (Retrieval-Augmented Generation) System built with smolagents, featuring PDF analysis, web search, and advanced retrieval capabilities.

## Features

- 🤖 Multi-agent architecture with specialized agents
- 📄 PDF document analysis and processing
- 🌐 Web search and content retrieval
- 🔍 Advanced vector-based retrieval with Qdrant
- 💬 Interactive Streamlit UI
- 🔧 CLI interface for programmatic access

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/Dontalion/Agentic_rag.git
cd Agentic_rag

# 2. Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Linux/Mac:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# 3. Install dependencies
pip install -e .

# 4. Set environment variables (optional but recommended)
export AGENTIC_RAG_HUGGINGFACE_TOKEN="your-token-here"
export AGENTIC_RAG_OPENAI_API_KEY="your-key-here"

# 5. Run the application
streamlit run agentic_rag/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

The application will be available at `http://localhost:8501`.

## Deployment Options

This application supports multiple deployment methods:

- **Local Development** - See setup instructions above
- **GitHub Codespaces** - Cloud-based development environment
- **Streamlit Community Cloud** - Free hosting for Streamlit apps
- **Docker** - Containerized deployment
- **Linux Server** - Production deployment with systemd

For detailed deployment instructions, see the [Deployment Guide](docs/DEPLOYMENT.md).

## Project Structure

```
agentic_rag/
├── agents/           # Agent implementations
├── config/           # Configuration and logging
├── tools/            # Agent tools (retrieval, web search, etc.)
├── ui/               # Streamlit UI components
├── utils/            # Utility functions
└── vectorstore/      # Vector store management
```

## License

See [LICENSE](LICENSE) for details.