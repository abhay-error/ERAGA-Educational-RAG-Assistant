#!/usr/bin/env python3
"""
Test script for College RAG Assistant

This script tests the core components of the system to ensure everything is working correctly.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import config
from src.document_processor import DocumentProcessor
from src.vector_db import VectorDB
from src.web_search import WebSearch
from src.llm_provider import LLMProvider
from src.rag_pipeline import RAGPipeline

def test_config():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    try:
        # Test basic config loading
        llm_config = config.get_llm_config()
        vector_config = config.get_vector_db_config()
        web_config = config.get_web_search_config()
        
        print(f"✅ Configuration loaded successfully")
        print(f"   LLM Provider: {llm_config.get('provider', 'N/A')}")
        print(f"   Vector DB: {vector_config.get('type', 'N/A')}")
        print(f"   Web Search: {'Enabled' if web_config.get('enabled') else 'Disabled'}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_document_processor():
    """Test document processor."""
    print("\n📄 Testing document processor...")
    try:
        processor = DocumentProcessor()
        print(f"✅ Document processor initialized")
        print(f"   Documents path: {processor.documents_path}")
        print(f"   Chunk size: {processor.chunk_size}")
        print(f"   Chunk overlap: {processor.chunk_overlap}")
        return True
    except Exception as e:
        print(f"❌ Document processor test failed: {e}")
        return False

def test_vector_db():
    """Test vector database."""
    print("\n🗄️ Testing vector database...")
    try:
        vector_db = VectorDB()
        info = vector_db.get_collection_info()
        print(f"✅ Vector database initialized")
        print(f"   Collection: {info.get('collection_name', 'N/A')}")
        print(f"   Documents: {info.get('total_documents', 0)}")
        print(f"   Model: {info.get('embedding_model', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Vector database test failed: {e}")
        return False

def test_web_search():
    """Test web search."""
    print("\n🌐 Testing web search...")
    try:
        web_search = WebSearch()
        print(f"✅ Web search initialized")
        print(f"   Enabled: {web_search.enabled}")
        print(f"   Providers: {', '.join(web_search.providers)}")
        
        # Test a simple search
        if web_search.enabled:
            results = web_search.search("University of Mysore", max_results=2)
            print(f"   Test search results: {len(results)} found")
        return True
    except Exception as e:
        print(f"❌ Web search test failed: {e}")
        return False

def test_llm_provider():
    """Test LLM provider."""
    print("\n🤖 Testing LLM provider...")
    try:
        llm = LLMProvider()
        print(f"✅ LLM provider initialized")
        print(f"   Provider: {llm.provider}")
        print(f"   Model: {llm.model}")
        
        # Test a simple response (without actual API call)
        print(f"   Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ LLM provider test failed: {e}")
        return False

def test_rag_pipeline():
    """Test RAG pipeline."""
    print("\n🔗 Testing RAG pipeline...")
    try:
        pipeline = RAGPipeline()
        print(f"✅ RAG pipeline initialized")
        
        # Get system info
        info = pipeline.get_system_info()
        print(f"   System status: {info.get('status', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ RAG pipeline test failed: {e}")
        return False

def create_test_document():
    """Create a test document for testing."""
    print("\n📝 Creating test document...")
    try:
        documents_path = config.get_paths().get('documents', './data/documents')
        os.makedirs(documents_path, exist_ok=True)
        
        test_content = """
# Python Programming Module 1

## Introduction to Python

Python is a high-level, interpreted programming language known for its simplicity and readability. This module covers the fundamentals of Python programming.

### Topics Covered

1. **Variables and Data Types**
   - Numbers (int, float)
   - Strings
   - Lists, tuples, and dictionaries
   - Boolean values

2. **Control Structures**
   - If-else statements
   - Loops (for, while)
   - Break and continue statements

3. **Functions**
   - Function definition and calling
   - Parameters and return values
   - Scope and lifetime

4. **File Handling**
   - Reading and writing files
   - File modes and operations

### Learning Objectives

By the end of this module, students should be able to:
- Write basic Python programs
- Use control structures effectively
- Define and use functions
- Handle file operations

### Assessment

- Weekly assignments (30%)
- Mid-term project (40%)
- Final examination (30%)

### Resources

- Python official documentation
- Online tutorials and exercises
- Practice problems and coding challenges
        """
        
        test_file_path = os.path.join(documents_path, "python_module1.md")
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"✅ Test document created: {test_file_path}")
        return test_file_path
    except Exception as e:
        print(f"❌ Failed to create test document: {e}")
        return None

def test_document_ingestion():
    """Test document ingestion."""
    print("\n📥 Testing document ingestion...")
    try:
        # Create test document
        test_file = create_test_document()
        if not test_file:
            return False
        
        # Test ingestion
        pipeline = RAGPipeline()
        result = pipeline.ingest_documents()
        
        if result['success']:
            print(f"✅ Document ingestion successful")
            print(f"   Chunks processed: {result['chunks_processed']}")
            return True
        else:
            print(f"❌ Document ingestion failed: {result['message']}")
            return False
    except Exception as e:
        print(f"❌ Document ingestion test failed: {e}")
        return False

def test_query_processing():
    """Test query processing."""
    print("\n🔍 Testing query processing...")
    try:
        pipeline = RAGPipeline()
        
        # Test query
        test_query = "What topics are covered in Python programming?"
        result = pipeline.process_query(test_query, use_web_search=False, max_docs=3)
        
        if result['response'] and not result['response'].startswith('Error'):
            print(f"✅ Query processing successful")
            print(f"   Query: {test_query}")
            print(f"   Response length: {len(result['response'])} characters")
            print(f"   Sources used: {len(result['sources'].get('documents', []))} documents")
            return True
        else:
            print(f"❌ Query processing failed: {result['response']}")
            return False
    except Exception as e:
        print(f"❌ Query processing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 College RAG Assistant - System Test")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Document Processor", test_document_processor),
        ("Vector Database", test_vector_db),
        ("Web Search", test_web_search),
        ("LLM Provider", test_llm_provider),
        ("RAG Pipeline", test_rag_pipeline),
        ("Document Ingestion", test_document_ingestion),
        ("Query Processing", test_query_processing),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
