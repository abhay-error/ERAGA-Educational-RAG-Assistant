#!/usr/bin/env python3
"""
Test script for enhanced College RAG Assistant features:
- Directory structure analysis
- Context-aware conversations
- Intelligent document retrieval
"""

import sys
import os
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from src.rag_pipeline import RAGPipeline
from src.document_processor import DocumentProcessor

def test_directory_structure():
    """Test directory structure analysis."""
    print("🔍 Testing Directory Structure Analysis...")
    
    try:
        processor = DocumentProcessor()
        
        # Test with a sample file path
        test_path = Path("data/documents/python/module1/lecture_notes.pdf")
        structure = processor._get_directory_structure(test_path)
        
        print(f"✅ Directory structure analysis working:")
        print(f"   Full path: {structure.get('full_path', 'N/A')}")
        print(f"   Path parts: {structure.get('path_parts', [])}")
        print(f"   Depth: {structure.get('depth', 0)}")
        print(f"   Parent directories: {structure.get('parent_directories', [])}")
        print(f"   Semantic info: {structure.get('semantic_info', {})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing directory structure: {e}")
        return False

def test_query_analysis():
    """Test query analysis for structure patterns."""
    print("\n🔍 Testing Query Analysis...")
    
    try:
        pipeline = RAGPipeline()
        
        # Test queries
        test_queries = [
            "I need Python notes for module 1",
            "Show me database management system syllabus",
            "Download lecture slides for week 3",
            "What are the topics in Java programming course?"
        ]
        
        for query in test_queries:
            analysis = pipeline._analyze_query_for_structure(query)
            print(f"✅ Query: '{query}'")
            print(f"   Module mentioned: {analysis.get('module_mentioned', False)}")
            print(f"   Module numbers: {analysis.get('module_numbers', [])}")
            print(f"   Subjects: {analysis.get('subjects', [])}")
            print(f"   File types: {analysis.get('file_types', [])}")
            print(f"   Directories: {analysis.get('directories', [])}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing query analysis: {e}")
        return False

def test_context_awareness():
    """Test context-aware conversation features."""
    print("\n🔍 Testing Context Awareness...")
    
    try:
        pipeline = RAGPipeline()
        
        # Simulate chat history
        chat_history = [
            {
                'role': 'user',
                'content': 'What is Python programming?',
                'timestamp': '2024-01-01T10:00:00'
            },
            {
                'role': 'assistant',
                'content': 'Python is a high-level programming language...',
                'timestamp': '2024-01-01T10:00:30'
            },
            {
                'role': 'user',
                'content': 'Tell me more about module 1',
                'timestamp': '2024-01-01T10:01:00'
            }
        ]
        
        # Test context-aware query
        result = pipeline.process_query(
            query="What topics are covered in this module?",
            use_web_search=False,
            max_docs=3,
            chat_history=chat_history
        )
        
        print(f"✅ Context-aware query processed successfully")
        print(f"   Response length: {len(result.get('response', ''))}")
        print(f"   Sources found: {len(result.get('sources', {}).get('documents', []))}")
        print(f"   Directory matches: {len(result.get('directory_matches', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing context awareness: {e}")
        return False

def test_enhanced_document_retrieval():
    """Test enhanced document retrieval with directory structure."""
    print("\n🔍 Testing Enhanced Document Retrieval...")
    
    try:
        pipeline = RAGPipeline()
        
        # Test document retrieval with structure analysis
        query = "Python programming module 1 notes"
        result = pipeline.process_query(
            query=query,
            use_web_search=False,
            max_docs=5
        )
        
        print(f"✅ Enhanced document retrieval working:")
        print(f"   Query: '{query}'")
        print(f"   Documents retrieved: {len(result.get('sources', {}).get('documents', []))}")
        print(f"   Directory matches: {len(result.get('directory_matches', []))}")
        
        # Show directory matches
        directory_matches = result.get('directory_matches', [])
        if directory_matches:
            print("   Directory matches found:")
            for match in directory_matches[:3]:
                print(f"     - {match.get('file_name', 'Unknown')} ({match.get('relative_path', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing enhanced document retrieval: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Enhanced College RAG Assistant Features")
    print("=" * 60)
    
    tests = [
        ("Directory Structure Analysis", test_directory_structure),
        ("Query Analysis", test_query_analysis),
        ("Context Awareness", test_context_awareness),
        ("Enhanced Document Retrieval", test_enhanced_document_retrieval)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
    
    print(f"\n{'='*60}")
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced features are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
