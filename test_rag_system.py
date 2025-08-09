#!/usr/bin/env python3
"""
Test script for RAG system functionality

This script tests the RAG system by asking questions and checking if documents are being retrieved and provided to users.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import config
from src.llm_provider import LLMProvider
from src.vector_db import VectorDB
from src.rag_pipeline import RAGPipeline
from src.document_processor import DocumentProcessor

def test_document_retrieval():
    """Test if documents are being retrieved from the vector database."""
    print("📚 Testing document retrieval...")
    try:
        # Initialize vector database
        vector_db = VectorDB()
        
        # Test queries that should retrieve documents
        test_queries = [
            "Python programming",
            "machine learning",
            "database management",
            "web technology",
            "statistical analysis",
            "big data analytics"
        ]
        
        results = []
        for query in test_queries:
            print(f"\n🔍 Searching for: '{query}'")
            
            # Search for similar documents
            search_results = vector_db.search(query, n_results=3)
            
            if search_results:
                print(f"✅ Found {len(search_results)} documents for '{query}'")
                for i, result in enumerate(search_results[:2], 1):
                    doc_id = result.get('id', 'N/A')
                    content = result.get('content', '')[:200]
                    metadata = result.get('metadata', {})
                    filename = metadata.get('filename', 'Unknown')
                    print(f"   {i}. {filename}")
                    print(f"      Content preview: {content}...")
                results.append((query, len(search_results)))
            else:
                print(f"❌ No documents found for '{query}'")
                results.append((query, 0))
        
        return results
        
    except Exception as e:
        print(f"❌ Document retrieval test failed: {e}")
        return []

def test_rag_pipeline():
    """Test the complete RAG pipeline."""
    print("\n🔗 Testing RAG pipeline...")
    try:
        # Initialize RAG pipeline
        pipeline = RAGPipeline()
        
        # Test questions
        test_questions = [
            "What is Python programming?",
            "Explain machine learning concepts",
            "What are the main features of Python?",
            "How does database management work?",
            "What is statistical analysis?",
            "Explain big data analytics"
        ]
        
        results = []
        for question in test_questions:
            print(f"\n🤖 Question: '{question}'")
            
            # Get response from RAG pipeline
            response_data = pipeline.process_query(question)
            
            if response_data and isinstance(response_data, dict):
                response = response_data.get('response', '')
                sources = response_data.get('sources', {})
                documents = sources.get('documents', [])
                web_search = sources.get('web_search', [])
                
                if response and not response.startswith("Error:"):
                    print(f"✅ Response received")
                    print(f"   Response preview: {response[:300]}{'...' if len(response) > 300 else ''}")
                    print(f"   📄 Documents found: {len(documents)}")
                    print(f"   🌐 Web results: {len(web_search)}")
                    
                    # Check if response contains document references
                    if "document" in response.lower() or "file" in response.lower() or "source" in response.lower():
                        print(f"   📄 Document references found in response")
                    
                    results.append((question, True))
                else:
                    print(f"❌ Failed to get response: {response}")
                    results.append((question, False))
            else:
                print(f"❌ Invalid response format: {response_data}")
                results.append((question, False))
        
        return results
        
    except Exception as e:
        print(f"❌ RAG pipeline test failed: {e}")
        return []

def test_document_processing():
    """Test if documents are being processed and stored properly."""
    print("\n📄 Testing document processing...")
    try:
        # Initialize document processor
        processor = DocumentProcessor()
        
        # Check processed documents
        processed_path = config.get_paths().get('processed', './data/processed')
        if os.path.exists(processed_path):
            processed_files = os.listdir(processed_path)
            print(f"✅ Found {len(processed_files)} processed files")
            
            for file in processed_files[:5]:  # Show first 5
                print(f"   - {file}")
            
            if len(processed_files) > 5:
                print(f"   ... and {len(processed_files) - 5} more files")
        else:
            print("❌ No processed documents directory found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Document processing test failed: {e}")
        return False

def test_specific_questions():
    """Test specific questions that should retrieve documents."""
    print("\n🎯 Testing specific questions...")
    try:
        pipeline = RAGPipeline()
        
        # Questions that should retrieve specific documents
        specific_questions = [
            "What are the main topics covered in Python Module 1?",
            "Explain the concepts in Python Module 2",
            "What is covered in the Python question bank?",
            "What are the key concepts in big data analytics?",
            "What topics are covered in statistical analysis?",
            "What is machine learning and how is it used?"
        ]
        
        results = []
        for question in specific_questions:
            print(f"\n🎯 Question: '{question}'")
            
            # Get response
            response_data = pipeline.process_query(question)
            
            if response_data and isinstance(response_data, dict):
                response = response_data.get('response', '')
                sources = response_data.get('sources', {})
                documents = sources.get('documents', [])
                
                if response and not response.startswith("Error:"):
                    print(f"✅ Response received")
                    
                    # Check response quality
                    response_length = len(response)
                    if response_length > 100:
                        print(f"   📏 Response length: {response_length} characters")
                        print(f"   📄 Response preview: {response[:200]}...")
                        print(f"   📚 Documents found: {len(documents)}")
                        
                        # Check for document-specific content
                        if any(keyword in response.lower() for keyword in ['python', 'module', 'programming', 'learning', 'analysis']):
                            print(f"   🎯 Relevant content detected")
                        
                        results.append((question, True, response_length))
                    else:
                        print(f"   ⚠️ Short response: {response}")
                        results.append((question, False, response_length))
                else:
                    print(f"❌ Failed to get response: {response}")
                    results.append((question, False, 0))
            else:
                print(f"❌ Invalid response format: {response_data}")
                results.append((question, False, 0))
        
        return results
        
    except Exception as e:
        print(f"❌ Specific questions test failed: {e}")
        return []

def test_document_metadata():
    """Test if document metadata is being preserved and returned."""
    print("\n🏷️ Testing document metadata...")
    try:
        vector_db = VectorDB()
        
        # Search for documents and check metadata
        search_results = vector_db.search("python", n_results=5)
        
        if search_results:
            print(f"✅ Found {len(search_results)} documents with metadata")
            
            for i, result in enumerate(search_results, 1):
                metadata = result.get('metadata', {})
                filename = metadata.get('filename', 'Unknown')
                file_path = metadata.get('file_path', 'Unknown')
                file_type = metadata.get('file_type', 'Unknown')
                
                print(f"   {i}. {filename}")
                print(f"      Path: {file_path}")
                print(f"      Type: {file_type}")
                
                # Check if metadata contains useful information
                if filename != 'Unknown' and file_path != 'Unknown':
                    print(f"      ✅ Metadata preserved")
                else:
                    print(f"      ⚠️ Missing metadata")
        else:
            print("❌ No documents found for metadata test")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Document metadata test failed: {e}")
        return False

def main():
    """Run all RAG system tests."""
    print("🧪 RAG System Test")
    print("=" * 50)
    
    # Run tests
    print("\n1. Testing document retrieval...")
    retrieval_results = test_document_retrieval()
    
    print("\n2. Testing document processing...")
    processing_success = test_document_processing()
    
    print("\n3. Testing document metadata...")
    metadata_success = test_document_metadata()
    
    print("\n4. Testing RAG pipeline...")
    pipeline_results = test_rag_pipeline()
    
    print("\n5. Testing specific questions...")
    specific_results = test_specific_questions()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    # Document retrieval summary
    if retrieval_results:
        total_docs = sum(count for _, count in retrieval_results)
        avg_docs = total_docs / len(retrieval_results) if retrieval_results else 0
        print(f"📚 Document Retrieval: {avg_docs:.1f} avg documents per query")
    
    # Processing summary
    print(f"📄 Document Processing: {'✅ PASS' if processing_success else '❌ FAIL'}")
    
    # Metadata summary
    print(f"🏷️ Document Metadata: {'✅ PASS' if metadata_success else '❌ FAIL'}")
    
    # Pipeline summary
    if pipeline_results:
        pipeline_success = sum(1 for _, success in pipeline_results if success)
        print(f"🔗 RAG Pipeline: {pipeline_success}/{len(pipeline_results)} successful")
    
    # Specific questions summary
    if specific_results:
        specific_success = sum(1 for _, success, _ in specific_results if success)
        avg_length = sum(length for _, success, length in specific_results if success) / specific_success if specific_success > 0 else 0
        print(f"🎯 Specific Questions: {specific_success}/{len(specific_results)} successful (avg {avg_length:.0f} chars)")
    
    print("\n🎉 RAG system test completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
