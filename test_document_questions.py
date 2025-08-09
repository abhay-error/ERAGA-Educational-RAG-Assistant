#!/usr/bin/env python3
"""
Test script for asking questions from user's documents

This script tests the RAG system by asking specific questions from the user's actual documents.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import config
from src.rag_pipeline import RAGPipeline
from src.vector_db import VectorDB

def test_document_specific_questions():
    """Test questions that should retrieve specific documents from the user's files."""
    print("🎯 Testing Document-Specific Questions")
    print("=" * 50)
    
    try:
        pipeline = RAGPipeline()
        
        # Questions specifically about the user's documents
        document_questions = [
            # Python Module questions
            "What are the main topics covered in Python Module 1?",
            "What concepts are taught in Python Module 2?",
            "What types of questions are in the Python question bank?",
            "What programming concepts are covered in the Python notes?",
            
            # Big Data and Analytics
            "What are the key concepts in big data analytics?",
            "What is covered in the big data analytics course?",
            "What are the main topics in the AI and ML course?",
            
            # Database Management
            "What database concepts are covered in the course materials?",
            "What is database management and how is it taught?",
            
            # Statistical Analysis
            "What statistical analysis topics are covered?",
            "What are the main concepts in statistical analysis?",
            
            # General Course Questions
            "What are the main subjects covered in the 6th semester?",
            "What courses are available in the 5th semester?",
            "What programming languages are taught in the course?"
        ]
        
        results = []
        for question in document_questions:
            print(f"\n🎯 Question: '{question}'")
            print("-" * 40)
            
            # Get response from RAG pipeline
            response_data = pipeline.process_query(question)
            
            if response_data and isinstance(response_data, dict):
                response = response_data.get('response', '')
                sources = response_data.get('sources', {})
                documents = sources.get('documents', [])
                web_search = sources.get('web_search', [])
                
                print(f"✅ Response received ({len(response)} characters)")
                print(f"📚 Documents found: {len(documents)}")
                print(f"🌐 Web results: {len(web_search)}")
                
                # Show document sources if any
                if documents:
                    print(f"📄 Document sources:")
                    for i, doc in enumerate(documents[:3], 1):
                        metadata = doc.get('metadata', {})
                        filename = metadata.get('filename', 'Unknown')
                        file_path = metadata.get('file_path', 'Unknown')
                        print(f"   {i}. {filename}")
                        print(f"      Path: {file_path}")
                        
                        # Show a preview of the content
                        content = doc.get('content', '')[:150]
                        if content:
                            print(f"      Preview: {content}...")
                else:
                    print("   ⚠️ No documents found for this query")
                
                # Show response preview
                print(f"🤖 Response preview:")
                print(f"   {response[:300]}{'...' if len(response) > 300 else ''}")
                
                # Check if response seems relevant
                if any(keyword in response.lower() for keyword in ['python', 'module', 'programming', 'learning', 'analysis', 'database', 'statistical', 'big data']):
                    print(f"   🎯 Relevant content detected")
                
                results.append((question, True, len(documents), len(response)))
            else:
                print(f"❌ Failed to get response")
                results.append((question, False, 0, 0))
        
        return results
        
    except Exception as e:
        print(f"❌ Document-specific questions test failed: {e}")
        return []

def test_document_retrieval_quality():
    """Test the quality of document retrieval."""
    print("\n📚 Testing Document Retrieval Quality")
    print("=" * 50)
    
    try:
        vector_db = VectorDB()
        
        # Test queries that should match specific documents
        test_queries = [
            "python module 1",
            "python module 2", 
            "question bank",
            "big data analytics",
            "machine learning",
            "database management",
            "statistical analysis"
        ]
        
        results = []
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            
            # Search for documents
            search_results = vector_db.search(query, n_results=5)
            
            if search_results:
                print(f"✅ Found {len(search_results)} documents")
                
                for i, result in enumerate(search_results[:3], 1):
                    metadata = result.get('metadata', {})
                    filename = metadata.get('filename', 'Unknown')
                    file_path = metadata.get('file_path', 'Unknown')
                    content = result.get('content', '')[:200]
                    
                    print(f"   {i}. {filename}")
                    print(f"      Path: {file_path}")
                    print(f"      Content: {content}...")
                
                results.append((query, len(search_results)))
            else:
                print(f"❌ No documents found")
                results.append((query, 0))
        
        return results
        
    except Exception as e:
        print(f"❌ Document retrieval quality test failed: {e}")
        return []

def test_document_metadata_preservation():
    """Test if document metadata is being preserved properly."""
    print("\n🏷️ Testing Document Metadata Preservation")
    print("=" * 50)
    
    try:
        vector_db = VectorDB()
        
        # Search for documents and check metadata
        search_results = vector_db.search("python", n_results=10)
        
        if search_results:
            print(f"✅ Found {len(search_results)} documents with metadata")
            
            metadata_fields = set()
            for result in search_results:
                metadata = result.get('metadata', {})
                metadata_fields.update(metadata.keys())
            
            print(f"📋 Metadata fields found: {', '.join(sorted(metadata_fields))}")
            
            # Check specific metadata fields
            for i, result in enumerate(search_results[:5], 1):
                metadata = result.get('metadata', {})
                filename = metadata.get('filename', 'Unknown')
                file_path = metadata.get('file_path', 'Unknown')
                file_type = metadata.get('file_type', 'Unknown')
                
                print(f"\n   {i}. {filename}")
                print(f"      Path: {file_path}")
                print(f"      Type: {file_type}")
                
                # Check if metadata is complete
                if filename != 'Unknown' and file_path != 'Unknown':
                    print(f"      ✅ Metadata preserved")
                else:
                    print(f"      ⚠️ Missing metadata")
            
            return True
        else:
            print("❌ No documents found for metadata test")
            return False
        
    except Exception as e:
        print(f"❌ Document metadata preservation test failed: {e}")
        return False

def main():
    """Run all document-specific tests."""
    print("🧪 Document-Specific Questions Test")
    print("=" * 60)
    
    # Run tests
    print("\n1. Testing document-specific questions...")
    question_results = test_document_specific_questions()
    
    print("\n2. Testing document retrieval quality...")
    retrieval_results = test_document_retrieval_quality()
    
    print("\n3. Testing document metadata preservation...")
    metadata_success = test_document_metadata_preservation()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    # Question results summary
    if question_results:
        successful_questions = sum(1 for _, success, _, _ in question_results if success)
        total_questions = len(question_results)
        avg_documents = sum(docs for _, _, docs, _ in question_results if docs > 0) / max(1, sum(1 for _, _, docs, _ in question_results if docs > 0))
        avg_response_length = sum(length for _, _, _, length in question_results if length > 0) / max(1, sum(1 for _, _, _, length in question_results if length > 0))
        
        print(f"🎯 Document Questions: {successful_questions}/{total_questions} successful")
        print(f"📚 Average documents per question: {avg_documents:.1f}")
        print(f"📏 Average response length: {avg_response_length:.0f} characters")
    
    # Retrieval results summary
    if retrieval_results:
        total_docs_found = sum(count for _, count in retrieval_results)
        avg_docs_per_query = total_docs_found / len(retrieval_results) if retrieval_results else 0
        print(f"🔍 Document Retrieval: {avg_docs_per_query:.1f} avg documents per query")
    
    # Metadata summary
    print(f"🏷️ Document Metadata: {'✅ PASS' if metadata_success else '❌ FAIL'}")
    
    print("\n🎉 Document-specific test completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
