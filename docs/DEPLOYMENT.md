# Deployment Guide

This guide covers multiple deployment options for the Agentic RAG application, from local development to production servers.

---

## Table of Contents

1. [Local Development](#1-local-development)
2. [GitHub Codespaces](#2-github-codespaces)
3. [Streamlit Community Cloud](#3-streamlit-community-cloud-free)
4. [Docker](#4-docker)
5. [Linux Server (Production)](#5-linux-server-production)
6. [Important Notes](#important-notes)

---

## 1. Local Development

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup Instructions

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

---

## 2. GitHub Codespaces

GitHub Codespaces provides a cloud-based development environment.

### Setup Instructions

1. Open the repository in GitHub Codespaces:
   - Go to the repository on GitHub
   - Click the **Code** button → **Codespaces** tab → **Create codespace on main**

2. Once the codespace is ready, open a terminal and run:

```bash
pip install -e .
streamlit run agentic_rag/ui/app.py --server.address 0.0.0.0 --server.port 8501
```

3. Click the port `8501` link that appears in the VS Code **Ports** panel to open the application in your browser.

---

## 3. Streamlit Community Cloud (Free)

Streamlit Community Cloud offers free hosting for Streamlit applications.

### Setup Instructions

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

3. Click **New app** and configure:
   - **Repository**: Select `Dontalion/Agentic_rag`
   - **Branch**: `main`
   - **Main file path**: `agentic_rag/ui/app.py`

4. Add environment variables in **Settings**:
   - `AGENTIC_RAG_HUGGINGFACE_TOKEN`
   - `AGENTIC_RAG_OPENAI_API_KEY`

5. Click **Deploy** and wait for the build to complete.

---

## 4. Docker

Docker provides a consistent and portable deployment environment.

### Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "agentic_rag/ui/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

### Build and Run

```bash
# Build the Docker image
docker build -t agentic-rag .

# Run the container
docker run -p 8501:8501 \
  -e AGENTIC_RAG_HUGGINGFACE_TOKEN=your-token \
  -e AGENTIC_RAG_OPENAI_API_KEY=your-key \
  agentic-rag
```

The application will be available at `http://localhost:8501`.

### Docker Compose (Optional)

For more complex setups with Qdrant:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - AGENTIC_RAG_HUGGINGFACE_TOKEN=${AGENTIC_RAG_HUGGINGFACE_TOKEN}
      - AGENTIC_RAG_OPENAI_API_KEY=${AGENTIC_RAG_OPENAI_API_KEY}
      - AGENTIC_RAG_QDRANT_USE_DOCKER=true
    depends_on:
      - qdrant

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  qdrant_data:
```

Run with:
```bash
docker-compose up -d
```

---

## 5. Linux Server (Production)

For production deployments on a Linux server, use systemd for process management.

### Prerequisites

- Ubuntu/Debian-based Linux server
- Root or sudo access
- Python 3.10+

### Setup Instructions

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip git

# 2. Create application directory and clone the repository
mkdir -p /opt/agentic-rag
cd /opt/agentic-rag
git clone https://github.com/Dontalion/Agentic_rag.git .

# 3. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install dependencies
pip install -e .

# 5. Deactivate virtual environment (systemd will handle activation)
deactivate
```

### Create Systemd Service

Create the service file:

```bash
sudo nano /etc/systemd/system/agentic-rag.service
```

Add the following configuration:

```ini
[Unit]
Description=Agentic RAG Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/agentic-rag
ExecStart=/opt/agentic-rag/.venv/bin/streamlit run agentic_rag/ui/app.py --server.address 0.0.0.0 --server.port 8501
Environment=AGENTIC_RAG_HUGGINGFACE_TOKEN=your-token
Environment=AGENTIC_RAG_OPENAI_API_KEY=your-key
Restart=always

[Install]
WantedBy=multi-user.target
```

### Enable and Start the Service

```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable agentic-rag

# Start the service
sudo systemctl start agentic-rag

# Check the service status
sudo systemctl status agentic-rag
```

### View Logs

```bash
# View recent logs
sudo journalctl -u agentic-rag -f
```

---

## Important Notes

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AGENTIC_RAG_HUGGINGFACE_TOKEN` | Hugging Face API token for model access | Yes (for HF models) |
| `AGENTIC_RAG_OPENAI_API_KEY` | OpenAI API key for GPT models | Yes (for OpenAI models) |
| `AGENTIC_RAG_QDRANT_USE_DOCKER` | Enable Docker-based Qdrant vector store | No (default: false) |

Always store sensitive tokens securely. Consider using:
- `.env` files (add to `.gitignore`)
- Environment variable management tools
- Secret management services (AWS Secrets Manager, HashiCorp Vault, etc.)

### Qdrant Vector Store

If `AGENTIC_RAG_QDRANT_USE_DOCKER=true` is set, you need Docker and Docker Compose installed on your system. The application will automatically start a Qdrant container for vector storage.

### Firewall Configuration

Ensure port 8501 is open for the application to be accessible:

```bash
# Using UFW (Ubuntu/Debian)
sudo ufw allow 8501

# Using firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

### Reverse Proxy (Production)

For production deployments, it's recommended to use Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable HTTPS with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8501 already in use | Change port: `--server.port 8502` |
| Module not found errors | Ensure `pip install -e .` was run |
| Permission denied on Linux | Check user permissions for `/opt/agentic-rag` |
| Qdrant connection failed | Verify Qdrant is running and accessible |
