# College RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) assistant for the School of Engineering at the University of Mysore. This system provides accurate, real-time academic and administrative information by combining document retrieval, web search, and large language models.

## 🎯 Features

### Core Capabilities
- **📄 Comprehensive Document Support**: Automatic ingestion and processing of **50+ file types** including PDF, Word, PowerPoint, Excel, Text, Code files, Archives, E-books, and more
- **🗄️ Vector Database**: ChromaDB-based semantic search with configurable embeddings
- **🌐 Web Search**: Optional real-time web search using DuckDuckGo and SerpAPI
- **🤖 Multi-LLM Support**: Pluggable LLM providers (OpenAI, Anthropic, Cohere, OpenRouter, Ollama)
- **💬 Chat Interface**: Modern Streamlit-based web interface with conversation history
- **📤 File Upload**: Direct file upload and processing through the UI
- **📥 Document Downloads**: Download original documents and notes when requested

### Advanced Features
- **🎯 Context-Aware Conversations**: Maintains conversation context for follow-up queries
- **📊 Source Attribution**: Shows which documents and web sources were used
- **💾 Downloadable Responses**: Export chat history and responses as text files
- **🔍 Smart Document Detection**: Automatically detects when users ask for notes or documents
- **⚙️ Configurable Settings**: Easy configuration via YAML file
- **🏗️ Modular Architecture**: Easy to extend and modify
- **🔄 Incremental Updates**: Only processes new/modified documents to save compute

### 🆕 Enhanced Features

#### 📁 Directory Structure Intelligence
- **Smart File Organization**: Automatically analyzes and understands your document directory structure
- **Semantic Path Matching**: Recognizes patterns like "module 1", "Python programming", "lecture notes"
- **Intelligent Retrieval**: When you ask for "Python notes for module 1", the system understands the directory structure and finds relevant files
- **Multi-part Module Support**: Automatically detects when modules are split into multiple parts and provides all relevant files

#### 💬 Context-Aware Conversations
- **Chat History**: Maintains conversation context across multiple interactions
- **Follow-up Questions**: Ask follow-up questions like "Tell me more about this" or "What about module 2?"
- **Contextual Responses**: Responses are enhanced with previous conversation context
- **Smart Suggestions**: System suggests relevant documents based on conversation history

#### 🎯 Intelligent Document Retrieval
- **Structure-Based Matching**: Matches queries against directory structure patterns
- **Semantic Analysis**: Understands file purposes (notes, syllabus, assignments, etc.)
- **Relevance Scoring**: Ranks documents by relevance to your query
- **Multi-criteria Search**: Combines content, structure, and metadata for better results

### Example Usage Scenarios

#### Scenario 1: Module-Based Queries
```
User: "I need Python notes for module 1"
Assistant: [Analyzes directory structure, finds files like:
  - python/module1/lecture_notes.pdf
  - python/module1/tutorial_guide.docx
  - python/module1/assignment1.pdf]

User: "What about module 2?"
Assistant: [Uses context from previous query, finds module 2 files]
```

#### Scenario 2: Subject-Based Queries
```
User: "Show me database management system materials"
Assistant: [Finds files in dbms/ directory with syllabus, notes, assignments]

User: "I need the syllabus specifically"
Assistant: [Filters to syllabus files based on context]
```

#### Scenario 3: Context-Aware Follow-ups
```
User: "What is Python programming?"
Assistant: [Provides general information about Python]

User: "Tell me more about the topics covered"
Assistant: [Uses context to provide specific topics from Python course materials]
```

### 🆕 Enhanced File Type Support

The system now supports **50+ file types** across multiple categories:

#### 📄 Document Formats
- **PDF** (.pdf) - Research papers, syllabi, course materials
- **Word** (.docx, .doc) - Course notes, assignments, reports  
- **PowerPoint** (.pptx, .ppt) - Presentations, lecture slides
- **OpenDocument** (.odt, .ods, .odp) - LibreOffice/OpenOffice files

#### 📝 Text & Code Formats
- **Plain Text** (.txt, .md, .rtf, .tex) - Notes, documentation, academic papers
- **Programming** (.py, .java, .cpp, .c, .cs, .js, .html, .css, .sql, .sh, .bat, .ps1)
- **Configuration** (.ini, .cfg, .conf, .json, .xml, .yaml, .yml, .toml)
- **Data** (.csv, .tsv) - Spreadsheets and data files

#### 📊 Spreadsheet Formats
- **Excel** (.xlsx, .xls, .xlsm, .xlsb) - Microsoft Excel files
- **CSV/TSV** (.csv, .tsv) - Comma/tab-separated values

#### 📧 Email & E-book Formats
- **Email** (.eml, .msg) - Email messages
- **E-books** (.epub, .mobi, .azw3) - Digital books

#### 📦 Archive Formats
- **Compressed** (.zip, .rar, .7z, .tar, .tar.gz, .gz) - Extracts and processes contents

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd college-rag-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional but recommended)
   ```bash
   # For OpenRouter (recommended)
   export OPENROUTER_API_KEY="your-openrouter-api-key"
   
   # For OpenAI (alternative)
   export OPENAI_API_KEY="your-openai-api-key"
   
   # For SerpAPI (optional, for web search)
   export SERPAPI_KEY="your-serpapi-key"
   ```

4. **Add your documents**
   ```bash
   # Copy your documents to the data/documents folder
   cp /path/to/your/documents/* data/documents/
   ```

5. **Create vector database**
   ```bash
   # Create/update vector database (incremental - only new files)
   python create_vector_db.py
   
   # Or force re-process all documents
   python create_vector_db.py --force
   ```

6. **Run the application**
   ```bash
   # Start the Streamlit app
   python main.py
   
   # Or use the simplified start script
   python start.py
   ```

7. **Open browser**: Go to `http://localhost:8501`

## 📁 Document Management

### Adding Documents

1. **Place files in the documents folder:**
   ```
   data/documents/
   ├── course_materials/
   │   ├── syllabus.pdf
   │   ├── lecture_notes.docx
   │   └── assignments.xlsx
   ├── research_papers/
   │   ├── paper1.pdf
   │   └── paper2.docx
   ├── code_examples/
   │   ├── example.py
   │   └── algorithm.java
   └── other_files/
       ├── notes.txt
       └── config.json
   ```

2. **Supported file types:** The system automatically detects and processes 50+ file types including:
   - **Documents**: PDF, Word, PowerPoint, OpenDocument
   - **Text**: TXT, MD, RTF, TEX, JSON, XML, YAML
   - **Code**: Python, Java, C/C++, JavaScript, HTML, CSS, SQL
   - **Spreadsheets**: Excel, CSV, TSV
   - **Archives**: ZIP, RAR, 7Z, TAR
   - **E-books**: EPUB, MOBI, AZW3
   - **Email**: EML, MSG

### Creating Vector Database

#### Method 1: Dedicated Script (Recommended)
```bash
# Create/update vector database (incremental)
python create_vector_db.py

# Force re-process all documents
python create_vector_db.py --force

# Check database information
python create_vector_db.py --info

# List all documents
python create_vector_db.py --list

# Search for documents
python create_vector_db.py --search "python programming"
```

#### Method 2: Web Interface
1. Start the app: `python main.py`
2. Open browser: `http://localhost:8501`
3. Click "📥 Ingest Documents" in sidebar
4. Wait for processing to complete

## 💬 Using the Chat Interface

### Basic Usage

1. **Start the application:**
   ```bash
   python main.py
   # or
   python start.py
   ```

2. **Open browser:** Go to `http://localhost:8501`

3. **Ask questions:**
   - Type your questions in the chat input
   - Press Enter or click "Send"
   - View conversation history and sources

### Example Questions

```
"What are the main topics in the Python programming course?"
"Can you explain database management systems?"
"What are the requirements for the final project?"
"Show me the course syllabus for Computer Science"
"I need notes on machine learning algorithms"
"Can I get the original syllabus document?"
"Download the course materials"
```

### Advanced Features

- **Context-Aware Conversations**: Ask follow-up questions
- **Source Attribution**: See which documents were used
- **Web Search Integration**: Toggle real-time web search
- **Document Downloads**: Download original files when requested

## 📥 Downloading Documents

### Automatic Detection

The system automatically detects when you ask for documents:

**Example Requests:**
- "Can I get the notes for Python programming?"
- "I need the original syllabus document"
- "Download the course materials"
- "Show me the reference documents"

### Manual Search

1. **Use the sidebar:**
   - Go to "📄 Download Documents" section
   - Enter keywords (e.g., "python", "syllabus", "notes")
   - Click "🔍 Search Documents"
   - Click "📚 Show All Documents" to see everything

2. **Download process:**
   - Click the "📥 Download" button next to any document
   - File will download to your default download folder
   - Original file format is preserved

## 🔧 Configuration

### Environment Variables

```bash
# LLM Configuration
export OPENROUTER_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export COHERE_API_KEY="your-key"

# Web Search
export SERPAPI_KEY="your-key"
```

### Configuration File

Edit `config.yaml` to customize settings:

```yaml
# LLM Configuration
llm:
  provider: "openrouter"  # openai, anthropic, cohere, openrouter, ollama
  model: "openai/gpt-4o"
  temperature: 0.7

# Vector Database
vector_db:
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
  similarity_threshold: 0.2

# Web Search
web_search:
  enabled: true
  providers: ["duckduckgo", "serpapi"]
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors:**
   ```bash
   # Ensure you're in the project root
   cd C:\MUSEAI
   pip install -r requirements.txt
   ```

2. **File Processing Issues:**
   ```bash
   # Check file permissions and corruption
   # Try processing individual files
   ```

3. **Vector Database Issues:**
   ```bash
   # Clear and rebuild database
   python create_vector_db.py --clear
   python create_vector_db.py --force
   ```

### Performance Tips

- **Large Collections**: Process in batches, use SSD storage
- **Better Search**: Use descriptive file names, organize in folders
- **Faster Processing**: Close other apps, monitor system resources

## 📞 Support

### Getting Help

1. **Check logs:**
   ```bash
   cat logs/vector_db_creation.log
   ```

2. **Test functionality:**
   ```bash
   python test_download_feature.py
   ```

3. **Verify setup:**
   ```bash
   python create_vector_db.py --info
   ```

### File Type Support

If you encounter unsupported file types:
1. Check the list of supported formats above
2. Convert files to supported formats
3. Contact support for new format requests
4. Use text extraction for unknown formats

## 📚 Documentation

- **[Complete Usage Guide](USAGE_GUIDE.md)** - Detailed step-by-step instructions
- **[Configuration Guide](docs/configuration.md)** - Advanced configuration options
- **[API Documentation](docs/api.md)** - Developer documentation
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions

## 🎉 Quick Start Summary

1. **Setup:** `pip install -r requirements.txt`
2. **Add Documents:** Copy files to `data/documents/`
3. **Create Database:** `python create_vector_db.py`
4. **Start App:** `python main.py`
5. **Chat:** Ask questions at `http://localhost:8501`
6. **Download:** Use sidebar to find and download documents

**That's it!** Your College RAG Assistant is ready to help with academic queries and document management! 🚀
