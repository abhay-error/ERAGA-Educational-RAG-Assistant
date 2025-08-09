#!/usr/bin/env python3
"""
Test script for document structure manager
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.document_structure import DocumentStructureManager

def test_document_structure():
    """Test the document structure manager."""
    print("🔍 Testing Document Structure Manager...")
    
    try:
        # Initialize document structure manager
        dsm = DocumentStructureManager()
        print("✅ Document Structure Manager initialized successfully")
        
        # Scan documents
        structure = dsm.scan_documents()
        print(f"📁 Found {len(structure['documents'])} documents")
        
        # Test search
        search_results = dsm.search_documents("python")
        print(f"🔍 Found {len(search_results)} documents matching 'python'")
        
        # Show some results
        if search_results:
            print("\n📄 Sample search results:")
            for i, result in enumerate(search_results[:3], 1):
                print(f"  {i}. {result.get('name', 'Unknown')} (Score: {result.get('score', 0)})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_document_structure()
    if success:
        print("\n🎉 Document Structure Manager test completed successfully!")
    else:
        print("\n❌ Document Structure Manager test failed!")
