#!/usr/bin/env python3
"""
Test script for the download functionality of the College RAG Assistant.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path (same as main.py)
sys.path.append(str(Path(__file__).parent / "src"))

# Import the modules
try:
    from src.rag_pipeline import RAGPipeline
    from src.document_processor import DocumentProcessor
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the project root directory.")
    sys.exit(1)

def test_download_functionality():
    """Test the download functionality."""
    print("🧪 Testing download functionality...")
    
    try:
        # Initialize RAG pipeline
        rag = RAGPipeline()
        
        # Test 1: Get available documents
        print("\n1. Testing get_available_documents()...")
        documents = rag.get_available_documents()
        print(f"   Found {len(documents)} documents in the database")
        
        for doc in documents[:3]:  # Show first 3
            print(f"   - {doc.get('file_name', 'Unknown')} ({doc.get('file_type', 'Unknown')})")
        
        # Test 2: Search for documents
        print("\n2. Testing search_documents_for_download()...")
        search_results = rag.search_documents_for_download("python programming")
        print(f"   Found {len(search_results)} documents matching 'python programming'")
        
        # Test 3: Get document by path (if any documents exist)
        if documents:
            print("\n3. Testing get_document_by_path()...")
            first_doc = documents[0]
            doc_info = rag.get_document_by_path(first_doc['file_path'])
            if doc_info:
                print(f"   Document info: {doc_info['file_name']} ({doc_info['file_size']} bytes)")
            else:
                print("   No document info available")
        
        # Test 4: Test document content retrieval (if any documents exist)
        if documents:
            print("\n4. Testing get_document_content()...")
            first_doc = documents[0]
            content = rag.get_document_content(first_doc['file_path'])
            if content:
                print(f"   Successfully retrieved {len(content)} bytes of content")
            else:
                print("   Could not retrieve document content")
        
        print("\n✅ Download functionality tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing download functionality: {e}")
        import traceback
        traceback.print_exc()

def test_document_processor():
    """Test the document processor functionality."""
    print("\n🧪 Testing document processor...")
    
    # Create a temporary test document
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test document for the College RAG Assistant.\n")
        f.write("It contains information about Python programming.\n")
        f.write("This document is used to test the download functionality.\n")
        test_file_path = f.name
    
    try:
        # Initialize document processor
        processor = DocumentProcessor()
        
        # Test processing the file
        print(f"   Processing test file: {test_file_path}")
        chunks = processor.process_single_file(test_file_path)
        print(f"   Created {len(chunks)} chunks from test file")
        
        # Test file tracking
        print("   Testing file tracking...")
        is_processed = processor._is_file_processed(test_file_path)
        print(f"   File processed status: {is_processed}")
        
    except Exception as e:
        print(f"❌ Error testing document processor: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        if os.path.exists(test_file_path):
            os.unlink(test_file_path)
    
    print("✅ Document processor tests completed!")

if __name__ == "__main__":
    print("🚀 Starting download functionality tests...")
    
    try:
        test_document_processor()
        test_download_functionality()
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
