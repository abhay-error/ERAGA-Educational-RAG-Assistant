<div align="center">
  <img src="https://via.placeholder.com/150" alt="ERAGA Logo" width="150"/>
  <h1>ERAGA: Enhanced RAG Assistant for General Academics</h1>
  <p>
    An AI-powered Retrieval-Augmented Generation (RAG) assistant for the School of Engineering at the University of Mysore. This system provides accurate, real-time academic and administrative information by combining document retrieval, web search, and large language models.
  </p>

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

## 📖 Table of Contents

- [🎯 Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [📁 Document Management](#-document-management)
- [💬 Using the Chat Interface](#-using-the-chat-interface)
- [📥 Downloading Documents](#-downloading-documents)
- [🔧 Configuration](#-configuration)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📞 Support](#-support)

---

## 🎯 Key Features

ERAGA is designed with powerful features to streamline access to academic information.

### Core Capabilities
| Feature | Description |
| :--- | :--- |
| **📄 Comprehensive Document Support** | Automatically ingests and processes **50+ file types**, including PDF, Word, PowerPoint, Code files, and more. |
| **🗄️ Vector Database** | Leverages **ChromaDB** for powerful semantic search with configurable sentence-transformer embeddings. |
| **🌐 Real-Time Web Search** | Optionally enhances answers with real-time web search using **DuckDuckGo** and **SerpAPI**. |
| **🤖 Multi-LLM Support** | Pluggable architecture supports various LLM providers like **OpenAI, Anthropic, Cohere, OpenRouter, and Ollama**. |
| **💬 Modern Chat Interface** | An intuitive **Streamlit-based** web interface with conversation history and source attribution. |
| **📤 Direct File Upload**| Upload and process documents directly through the user interface for instant knowledge base updates. |

### Enhanced Features
| Feature | Description |
| :--- | :--- |
| **🧠 Directory Structure Intelligence** | Intelligently analyzes your document directory structure to understand semantic paths like "module 1" or "Python notes." |
| **🗣️ Context-Aware Conversations**| Maintains conversational context, allowing for natural follow-up questions and contextually relevant responses. |
| **🔍 Intelligent Document Retrieval** | Combines content, metadata, and directory structure analysis for highly relevant, multi-criteria search results. |
| **💾 Downloadable Responses** | Easily export chat history and generated responses as text files for offline use and record-keeping. |

<details>
<summary><strong>🆕 Click to see all 50+ Supported File Types</strong></summary>

- **📄 Document Formats**: PDF (.pdf), Word (.docx, .doc), PowerPoint (.pptx, .ppt), OpenDocument (.odt, .ods, .odp)
- **📝 Text & Code**: Plain Text (.txt, .md, .rtf, .tex), Programming (.py, .java, .cpp, .js, .html, .css, .sql), Config (.json, .xml, .yaml)
- **📊 Spreadsheet Formats**: Excel (.xlsx, .xls), CSV/TSV (.csv, .tsv)
- **📧 Email & E-book Formats**: Email (.eml, .msg), E-books (.epub, .mobi, .azw3)
- **📦 Archive Formats**: Compressed (.zip, .rar, .7z, .tar, .gz) - Extracts and processes contents automatically.
</details>

---

## 🚀 Quick Start

Get your personal academic assistant up and running in minutes.

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd college-rag-assistant
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables** (Optional, but recommended)
    Create a `.env` file or export the following variables:
    ```bash
    # For OpenRouter (recommended)
    OPENROUTER_API_KEY="your-openrouter-api-key"
    
    # For OpenAI (alternative)
    OPENAI_API_KEY="your-openai-api-key"
    
    # For SerpAPI (for web search)
    SERPAPI_KEY="your-serpapi-key"
    ```

4.  **Add Your Documents**
    Place your academic materials into the `data/documents/` directory. The system will automatically detect the folder structure.
    ```bash
    cp /path/to/your/documents/* data/documents/
    ```

5.  **Create the Vector Database**
    This is an incremental process—only new or modified files will be processed.
    ```bash
    python create_vector_db.py
    ```
    > **Pro Tip:** Use `python create_vector_db.py --force` to re-process all documents from scratch.

6.  **Run the Application**
    ```bash
    python main.py
    ```

7.  **Open in Browser**
    Navigate to `http://localhost:8501` to start chatting with your assistant.

---

## 📁 Document Management

### Organizing Your Documents
For best results, organize your files in a structured manner. The Directory Structure Intelligence feature thrives on logical paths.

**Example Structure:**
```
data/documents/
├── python_programming/
│   ├── module_1/
│   │   ├── lecture_notes.pdf
│   │   └── assignment_1.docx
│   └── module_2/
│       └── slides.pptx
├── database_management/
│   ├── syllabus.pdf
│   └── practice_queries.sql
└── research_papers/
    └── paper_on_ai.pdf
```

### Ingesting Documents & Creating the Database
You can create or update your vector database using two methods:

#### Method 1: Command-Line Interface (Recommended)
```bash
python create_vector_db.py
python create_vector_db.py --force
python create_vector_db.py --info
python create_vector_db.py --search "machine learning algorithms"
```

#### Method 2: Web Interface
1.  Start the application: `python main.py`
2.  In the web UI, go to **"📥 Ingest Documents"**
3.  Click to process and view progress.

---

## 💬 Using the Chat Interface
Example:
> User: "I need Python notes for module 1"  
> Assistant: [Retrieves from python_programming/module_1/]  

> User: "What about module 2?"  
> Assistant: [Retrieves from python_programming/module_2/]  

Features:
- Contextual follow-ups
- Source attribution
- Web search toggle

---

## 📥 Downloading Documents
Automatic detection for requests like:
- "Can I get the syllabus?"
- "Download database management materials."

Or browse/download from the **📄 Download Documents** section.

---

## 🔧 Configuration
```yaml
llm:
  provider: "openrouter"
  model: "openai/gpt-4o"
  temperature: 0.7

vector_db:
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  similarity_threshold: 0.2

web_search:
  enabled: true
  providers: ["duckduckgo", "serpapi"]
```
