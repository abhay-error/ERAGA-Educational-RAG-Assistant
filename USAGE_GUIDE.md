# 🎓 College RAG Assistant - Complete Usage Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Installation & Setup](#installation--setup)
3. [Adding Documents](#adding-documents)
4. [Creating Vector Database](#creating-vector-database)
5. [Using the Chat Interface](#using-the-chat-interface)
6. [Downloading Documents](#downloading-documents)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)

## 🎯 System Overview

The College RAG Assistant is an AI-powered system that:
- **Processes** various document types (PDF, Word, PowerPoint, Excel, Text, etc.)
- **Creates** a searchable vector database from your documents
- **Answers** questions using your document knowledge + web search
- **Allows** downloading of original documents and notes
- **Provides** a modern web interface for easy interaction

## 🚀 Installation & Setup

### Step 1: Prerequisites
```bash
# Ensure you have Python 3.10+ installed
python --version

# Install required packages
pip install -r requirements.txt
```

### Step 2: Environment Setup
```bash
# Create necessary directories
mkdir -p data/documents
mkdir -p data/processed
mkdir -p vector_db
mkdir -p logs

# Set up API keys (optional but recommended)
export OPENROUTER_API_KEY="your-key-here"
export SERPAPI_KEY="your-key-here"
```

## 📁 Adding Documents

### Supported File Types

The system now supports **50+ file types**:

#### 📄 Document Formats
- **PDF** (.pdf) - Research papers, syllabi, course materials
- **Word** (.docx, .doc) - Course notes, assignments, reports
- **PowerPoint** (.pptx, .ppt) - Presentations, lecture slides
- **OpenDocument** (.odt, .ods, .odp) - LibreOffice/OpenOffice files

#### 📝 Text Formats
- **Plain Text** (.txt) - Notes, documentation
- **Markdown** (.md) - Documentation, README files
- **Rich Text** (.rtf) - Formatted text documents
- **LaTeX** (.tex) - Academic papers, mathematical documents
- **Configuration** (.ini, .cfg, .conf) - Settings files
- **Data Formats** (.json, .xml, .yaml, .yml, .toml) - Structured data

#### 💻 Programming Files
- **Python** (.py) - Python scripts and modules
- **Java** (.java) - Java source code
- **C/C++** (.c, .cpp, .h) - C/C++ source code
- **C#** (.cs) - C# source code
- **JavaScript** (.js) - JavaScript files
- **HTML/CSS** (.html, .htm, .css) - Web files
- **SQL** (.sql) - Database queries
- **Shell Scripts** (.sh, .bat, .ps1) - Scripts

#### 📊 Spreadsheet Formats
- **Excel** (.xlsx, .xls, .xlsm, .xlsb) - Microsoft Excel files
- **CSV/TSV** (.csv, .tsv) - Comma/tab-separated values

#### 📧 Email Formats
- **Email** (.eml, .msg) - Email messages

#### 📚 E-book Formats
- **EPUB** (.epub) - E-book format
- **MOBI** (.mobi) - Kindle format
- **AZW3** (.azw3) - Amazon format

#### 📦 Archive Formats
- **ZIP** (.zip) - Compressed archives
- **RAR** (.rar) - RAR archives
- **7Z** (.7z) - 7-Zip archives
- **TAR** (.tar, .tar.gz, .gz) - Unix archives

### Adding Your Documents

1. **Place files in the documents folder:**
   ```bash
   # Copy your documents to the data/documents folder
   cp /path/to/your/documents/* data/documents/
   
   # Or manually copy files to:
   # C:\MUSEAI\data\documents\
   ```

2. **Supported file structure:**
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

## 🗄️ Creating Vector Database

### Method 1: Using the Dedicated Script (Recommended)

```bash
# Create/update vector database (incremental - only new files)
python create_vector_db.py

# Force re-process all documents
python create_vector_db.py --force

# Check database information
python create_vector_db.py --info

# List all documents in database
python create_vector_db.py --list

# Search for specific documents
python create_vector_db.py --search "python programming"

# Clear all documents from database
python create_vector_db.py --clear
```

### Method 2: Using the Web Interface

1. **Start the application:**
   ```bash
   python main.py
   # or
   python start.py
   ```

2. **Open browser:** Go to `http://localhost:8501`

3. **Ingest documents:**
   - Click "📥 Ingest Documents" in the sidebar
   - Wait for processing to complete
   - See success message with document count

### Method 3: Using Command Line

```bash
# Ingest documents via command line
python main.py --ingest

# Start web interface
python main.py
```

## 💬 Using the Chat Interface

### Starting the Application

```bash
# Start the Streamlit app
python main.py

# Or use the simplified start script
python start.py
```

### Chat Interface Features

1. **Main Chat Area:**
   - Type your questions in the text input
   - Press Enter or click "Send" to ask
   - View conversation history
   - See source documents used

2. **Sidebar Controls:**
   - **Document Management:** Upload new files, ingest documents
   - **Download Documents:** Search and download original files
   - **System Settings:** Configure LLM, web search, etc.
   - **Chat History:** Download conversation history

3. **Example Questions:**
   ```
   "What are the main topics in the Python programming course?"
   "Can you explain database management systems?"
   "What are the requirements for the final project?"
   "Show me the course syllabus for Computer Science"
   "I need notes on machine learning algorithms"
   ```

### Advanced Chat Features

1. **Context-Aware Conversations:**
   - Ask follow-up questions
   - Reference previous conversation
   - Maintain context throughout session

2. **Source Attribution:**
   - See which documents were used
   - View web search results
   - Understand information sources

3. **Web Search Integration:**
   - Toggle web search on/off
   - Get real-time information
   - Combine document and web knowledge

## 📥 Downloading Documents

### Automatic Document Detection

The system automatically detects when you ask for documents:

**Example Requests:**
- "Can I get the notes for Python programming?"
- "I need the original syllabus document"
- "Download the course materials"
- "Show me the reference documents"
- "I want the lecture slides"
- "Give me the assignment files"

### Manual Document Search

1. **Use the sidebar:**
   - Go to "📄 Download Documents" section
   - Enter keywords (e.g., "python", "syllabus", "notes")
   - Click "🔍 Search Documents"
   - Click "📚 Show All Documents" to see everything

2. **Download process:**
   - Click the "📥 Download" button next to any document
   - File will download to your default download folder
   - Original file format is preserved

### Supported Download Formats

All original file types can be downloaded:
- **PDF** (.pdf) - Research papers, syllabi
- **Word** (.docx, .doc) - Course notes, assignments
- **PowerPoint** (.pptx, .ppt) - Presentations, slides
- **Excel** (.xlsx, .xls) - Spreadsheets, data
- **Text** (.txt, .md) - Notes, documentation
- **Code** (.py, .java, .cpp, etc.) - Source code
- **And many more...**

## 🔧 Advanced Features

### Configuration Management

1. **Edit config.yaml:**
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

2. **Environment Variables:**
   ```bash
   export OPENROUTER_API_KEY="your-key"
   export OPENAI_API_KEY="your-key"
   export SERPAPI_KEY="your-key"
   ```

### Batch Operations

1. **Process multiple files:**
   ```bash
   # Process all documents in a folder
   python create_vector_db.py --force
   ```

2. **Search across documents:**
   ```bash
   # Search for specific content
   python create_vector_db.py --search "machine learning"
   ```

3. **Database management:**
   ```bash
   # Check database status
   python create_vector_db.py --info
   
   # Clear and rebuild
   python create_vector_db.py --clear
   python create_vector_db.py --force
   ```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors:**
   ```bash
   # Ensure you're in the project root
   cd C:\MUSEAI
   
   # Install missing dependencies
   pip install -r requirements.txt
   ```

2. **File Processing Issues:**
   ```bash
   # Check file permissions
   # Ensure files are not corrupted
   # Try processing individual files
   ```

3. **Vector Database Issues:**
   ```bash
   # Clear and rebuild database
   python create_vector_db.py --clear
   python create_vector_db.py --force
   ```

4. **Memory Issues:**
   ```bash
   # Process files in smaller batches
   # Increase system memory
   # Use SSD storage for better performance
   ```

### Performance Tips

1. **For Large Document Collections:**
   - Process documents in batches
   - Use SSD storage
   - Increase system memory
   - Use incremental updates

2. **For Better Search Results:**
   - Use descriptive file names
   - Organize documents in folders
   - Use consistent naming conventions
   - Add metadata to documents

3. **For Faster Processing:**
   - Close other applications
   - Use dedicated processing time
   - Monitor system resources
   - Use force updates sparingly

## 📞 Support

### Getting Help

1. **Check logs:**
   ```bash
   # View processing logs
   cat logs/vector_db_creation.log
   ```

2. **Test functionality:**
   ```bash
   # Run test script
   python test_download_feature.py
   ```

3. **Verify setup:**
   ```bash
   # Check system information
   python create_vector_db.py --info
   ```

### File Type Support

If you encounter unsupported file types:
1. **Check the list** of supported formats above
2. **Convert files** to supported formats
3. **Contact support** for new format requests
4. **Use text extraction** for unknown formats

---

## 🎉 Quick Start Summary

1. **Setup:** `pip install -r requirements.txt`
2. **Add Documents:** Copy files to `data/documents/`
3. **Create Database:** `python create_vector_db.py`
4. **Start App:** `python main.py`
5. **Chat:** Ask questions at `http://localhost:8501`
6. **Download:** Use sidebar to find and download documents

**That's it!** Your College RAG Assistant is ready to help with academic queries and document management! 🚀
