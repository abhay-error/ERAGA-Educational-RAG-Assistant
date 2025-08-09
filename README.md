

<div align="center">
  <img src="ERAGA_LOGO.png" alt="ERAGA Logo" width="150"/>
  <h1>ERAGA: Enhanced RAG Assistant for General Academics</h1>


<p>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Project Status"></a>
  <a href="https://github.com/SAMRUDDH15/EERAGA-Enhanced-RAG-Assistant-for-General-Academics/stargazers">
    <img src="https://img.shields.io/github/stars/SAMRUDDH15/EERAGA-Enhanced-RAG-Assistant-for-General-Academics?style=social" alt="GitHub Stars">
  </a>
</p>

</div>

---

## Overview

**ERAGA** (Enhanced RAG Assistant for General Academics) is a Retrieval-Augmented Generation (RAG) chatbot designed to act like ChatGPT **but powered by your own documents**. Documents are ingested and converted to a vector database (ChromaDB by default), so the assistant answers questions from your custom knowledge base plus optional web search.

This README is a ready-to-use guide for developers and administrators to install, configure, run, and extend ERAGA.

---

## 📖 Table of Contents

- [🎯 Key Features](#-key-features)  
- [⚡ Quick Start](#-quick-start)  
- [🏗️ Architecture & Data Flow](#-architecture--data-flow)  
- [📁 Document Management](#-document-management)  
- [💡 Usage Examples](#-usage-examples)  
- [⚙️ Configuration](#-configuration)  
- [💻 Running Locally (Dev)](#-running-locally-dev)  
- [🐳 Docker Deployment](#-docker-deployment)  
- [🔒 Security & Privacy](#-security--privacy)  
- [🛠️ Troubleshooting](#-troubleshooting)  
- [🤝 Contributing](#-contributing)  
- [📜 License](#-license)  
- [📞 Support](#-support)  

---




## 🎯 Key Features

- **RAG chatbot with custom knowledge base** — your documents are embedded into a vector DB so ERAGA responds using your content.
- **Supports 50+ file types** (PDF, DOCX, PPTX, code, spreadsheets, e‑books, archives, etc.).
- **ChromaDB vector store** with configurable sentence-transformer embeddings (default: `all-MiniLM-L6-v2`).
- **Pluggable LLM backends** (OpenRouter, OpenAI, Anthropic, Cohere, Ollama, local LLMs).
- **Optional real-time web search** (DuckDuckGo, SerpAPI) to augment answers when necessary.
- **Streamlit UI** with context-aware conversations, source attribution, downloads, and document ingestion from the web UI.
- **Incremental ingestion** — only new/modified files are processed by default.
- **Directory Structure Intelligence** — leverages folder paths and metadata for improved retrieval relevance.

> **Note:** This is an RAG system — the vector DB contains embeddings of your documents, so the assistant behaves like a ChatGPT tuned to your organization’s content (a custom knowledge base).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or newer
- `pip`

### Install
```bash
git clone <repository-url> eraga
cd eraga
pip install -r requirements.txt
```

### Add documents
Place files under `data/documents/` preserving any folder structure you want reflected in search:
```
data/documents/
├── course_materials/
├── research_papers/
└── code_examples/
```

### Create vector DB (incremental)
```bash
python create_vector_db.py
# or force a full rebuild
python create_vector_db.py --force
```

### Run the app (Streamlit)
```bash
python main.py
# then open http://localhost:8501
```

---

## 🏗 Architecture & Data Flow (high level)

1. **Ingest**: Files from `data/documents/` are scanned and text is extracted (PDF/text/Office/archives).
2. **Chunk & Embed**: Documents are chunked (configurable size/overlap) and embeddings are created via sentence-transformers or a remote embedding API.
3. **Store**: Embeddings + metadata are stored in ChromaDB (or other vector backends).
4. **Query**: On user query, top-k relevant chunks are retrieved and assembled into a prompt with optional web search results.
5. **Generate**: A chosen LLM (local or cloud) produces the answer; sources and citations are returned alongside the response.

---

## 📁 Document Management & Supported Types

ERAGA supports extraction from many formats (full list in the UI). Common examples:
- PDF, DOCX, PPTX, TXT, MD, LaTeX
- Python/Java/C/C++/JS source files
- Excel, CSV
- EPUB/MOBI e-books
- ZIP/RAR/TAR archives (auto-extracted)

**Pro tip:** Give files descriptive names and keep related files in the same folder to improve retrieval quality.

---

## 💬 Usage Examples

- **Simple question:** `What are the learning outcomes of the Database Management course?`
- **Contextual follow-up:** After asking about module 1, ask `What about module 2?` — the assistant will maintain context.
- **Download request:** `Download the syllabus for Computer Science` will return matching documents to download.
- **Search across corpus:** `Find examples of normalization in our course materials` — returns snippets and source files.

---

## ⚙️ Configuration

Primary configuration is in `config.yaml` and environment variables.

Example `config.yaml` (sensible defaults):
```yaml
llm:
  provider: "openrouter"      # openrouter, openai, anthropic, cohere, ollama, local
  model: "openai/gpt-4o"
  temperature: 0.0
  max_tokens: 1200

vector_db:
  backend: "chroma"           # chroma (default) -- pluggable in code
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  chunk_size: 800
  chunk_overlap: 100
  top_k: 6

web_search:
  enabled: true
  providers: ["duckduckgo", "serpapi"]
```

Environment variables (recommended via `.env`):
```bash
OPENROUTER_API_KEY="your-openrouter-key"
OPENAI_API_KEY="your-openai-key"
SERPAPI_KEY="your-serpapi-key"
```
Set secure keys in your deployment environment; avoid committing them to Git.

---

## 🧪 Running Locally (Development)

- Rebuild vector DB while debugging:
```bash
python create_vector_db.py --force --verbose
```
- Run Streamlit with live reload (useful during UI edits):
```bash
streamlit run main.py --server.port 8501

- Run everything Streamlit with live reload:
```bash
python start.py
```

---

## 🐳 Docker Deployment (optional)

A sample `Dockerfile` and `docker-compose.yml` are included to containerize the app. Build & run:
```bash
docker build -t eraga:latest .
docker run -p 8501:8501 --env-file .env -v $(pwd)/data:/app/data eraga:latest
```

---

## 🔒 Security & Privacy

- **Local-first storage:** By default embeddings & DB are stored locally (Chroma); review `config.yaml` if you're using managed vector stores.
- **PII:** The system will index any text present in the documents. Remove or redact personally identifiable information (PII) before ingestion if needed.
- **API keys:** Keep LLM and search API keys secret. Use environment variables and secrets management in production.

---

## 🛠 Troubleshooting

- **Missing dependencies**: `pip install -r requirements.txt`
- **Document not found in DB**: try `python create_vector_db.py --force` to re-index
- **High memory usage**: reduce `chunk_size` or process files in batches
- **Streamlit port conflict**: change port: `streamlit run main.py --server.port 8502`

Check logs under `logs/` for detailed errors.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-change`)
3. Commit your changes and open a pull request
4. Add tests where appropriate and update `requirements.txt` if needed

Suggested contribution areas:
- New document parsers / improved OCR
- Additional vector DB backends (Weaviate, Milvus)
- UI/UX improvements to the Streamlit interface
- CI, tests, and deployment automation

---

## 📄 License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## 📞 Support & Contact

- Check `logs/` and `data/processed/` for ingestion details
- For quick tests, use `python create_vector_db.py --info`

If you want, I can also:
- generate a `docker-compose.yml` for you,
- add a quick-start script (`start.sh`),
- or create unit tests for ingestion — tell me which you prefer.

---

