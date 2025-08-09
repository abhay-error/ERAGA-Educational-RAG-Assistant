#!/usr/bin/env python3
"""
Vector Database Creation and Update Script

This script creates and updates the vector database for the College RAG Assistant.
It supports:
- Initial creation of the vector database
- Incremental updates (only processes new/modified documents)
- Persistent storage (vector database is saved and reused)
- Batch processing of documents
- Progress tracking and logging

Usage:
    python create_vector_db.py                    # Create/update vector database
    python create_vector_db.py --force           # Force re-processing of all documents
    python create_vector_db.py --info            # Show database information
    python create_vector_db.py --clear           # Clear all documents from database
    python create_vector_db.py --help            # Show help
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime
import time

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.rag_pipeline import RAGPipeline
    from src.document_processor import DocumentProcessor
    from src.vector_db import VectorDB
    from src.config import config
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the project root directory.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/vector_db_creation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VectorDBCreator:
    def __init__(self):
        """Initialize the Vector Database Creator."""
        self.rag_pipeline = RAGPipeline()
        self.document_processor = DocumentProcessor()
        self.vector_db = VectorDB()
        self.config = config
        
        # Get paths
        self.documents_path = self.config.get_paths().get('documents', './data/documents')
        self.processed_path = self.config.get_paths().get('processed', './data/processed')
        self.vector_db_path = self.config.get_vector_db_config().get('persist_directory', './vector_db')
        
        logger.info(f"Vector DB Creator initialized")
        logger.info(f"Documents path: {self.documents_path}")
        logger.info(f"Vector DB path: {self.vector_db_path}")
    
    def create_vector_db(self, force_update: bool = False) -> dict:
        """
        Create or update the vector database.
        
        Args:
            force_update (bool): If True, re-process all documents even if already processed
            
        Returns:
            dict: Results of the operation
        """
        start_time = time.time()
        
        try:
            logger.info("Starting vector database creation/update...")
            
            # Check if documents directory exists
            if not os.path.exists(self.documents_path):
                logger.warning(f"Documents directory does not exist: {self.documents_path}")
                return {
                    'success': False,
                    'message': f'Documents directory does not exist: {self.documents_path}',
                    'documents_processed': 0,
                    'chunks_created': 0,
                    'time_taken': 0
                }
            
            # Get current database info
            current_info = self.get_database_info()
            logger.info(f"Current database: {current_info['total_documents']} documents, {current_info['total_chunks']} chunks")
            
            # Process documents
            if force_update:
                logger.info("Force update mode: Re-processing all documents")
                processed_chunks = self.document_processor.process_documents(force=True)
            else:
                logger.info("Incremental update mode: Processing only new/modified documents")
                processed_chunks = self.document_processor.process_documents(force=False)
            
            if not processed_chunks:
                logger.info("No new documents to process")
                return {
                    'success': True,
                    'message': 'No new documents to process',
                    'documents_processed': 0,
                    'chunks_created': 0,
                    'time_taken': time.time() - start_time,
                    'database_info': current_info
                }
            
            # Add to vector database
            logger.info(f"Adding {len(processed_chunks)} chunks to vector database...")
            success = self.vector_db.add_documents(processed_chunks)
            
            if not success:
                logger.error("Failed to add documents to vector database")
                return {
                    'success': False,
                    'message': 'Failed to add documents to vector database',
                    'documents_processed': 0,
                    'chunks_created': 0,
                    'time_taken': time.time() - start_time
                }
            
            # Get updated database info
            updated_info = self.get_database_info()
            
            # Calculate statistics
            time_taken = time.time() - start_time
            documents_processed = len(set(chunk['file_path'] for chunk in processed_chunks))
            
            logger.info(f"Vector database update completed successfully!")
            logger.info(f"Documents processed: {documents_processed}")
            logger.info(f"Chunks created: {len(processed_chunks)}")
            logger.info(f"Time taken: {time_taken:.2f} seconds")
            
            return {
                'success': True,
                'message': f'Successfully processed {documents_processed} documents and created {len(processed_chunks)} chunks',
                'documents_processed': documents_processed,
                'chunks_created': len(processed_chunks),
                'time_taken': time_taken,
                'database_info': updated_info,
                'new_chunks': len(processed_chunks)
            }
            
        except Exception as e:
            logger.error(f"Error during vector database creation: {e}")
            return {
                'success': False,
                'message': f'Error during vector database creation: {str(e)}',
                'documents_processed': 0,
                'chunks_created': 0,
                'time_taken': time.time() - start_time
            }
    
    def get_database_info(self) -> dict:
        """Get information about the current vector database."""
        try:
            collection_info = self.vector_db.get_collection_info()
            
            # Get additional information
            total_documents = collection_info.get('total_documents', 0)
            collection_name = collection_info.get('collection_name', 'N/A')
            embedding_model = collection_info.get('embedding_model', 'N/A')
            
            # Count unique documents
            unique_documents = 0
            if total_documents > 0:
                try:
                    results = self.vector_db.collection.get()
                    if results['metadatas']:
                        unique_files = set()
                        for metadata in results['metadatas']:
                            if metadata and 'file_path' in metadata:
                                unique_files.add(metadata['file_path'])
                        unique_documents = len(unique_files)
                except Exception as e:
                    logger.warning(f"Could not count unique documents: {e}")
                    unique_documents = total_documents
            
            return {
                'total_documents': total_documents,
                'unique_documents': unique_documents,
                'total_chunks': total_documents,
                'collection_name': collection_name,
                'embedding_model': embedding_model,
                'database_path': self.vector_db_path,
                'exists': os.path.exists(self.vector_db_path)
            }
            
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {
                'total_documents': 0,
                'unique_documents': 0,
                'total_chunks': 0,
                'collection_name': 'N/A',
                'embedding_model': 'N/A',
                'database_path': self.vector_db_path,
                'exists': False,
                'error': str(e)
            }
    
    def clear_database(self) -> dict:
        """Clear all documents from the vector database."""
        try:
            logger.info("Clearing vector database...")
            success = self.vector_db.clear_collection()
            
            if success:
                logger.info("Vector database cleared successfully")
                return {
                    'success': True,
                    'message': 'Vector database cleared successfully'
                }
            else:
                logger.error("Failed to clear vector database")
                return {
                    'success': False,
                    'message': 'Failed to clear vector database'
                }
                
        except Exception as e:
            logger.error(f"Error clearing vector database: {e}")
            return {
                'success': False,
                'message': f'Error clearing vector database: {str(e)}'
            }
    
    def list_documents(self) -> list:
        """List all documents in the vector database."""
        try:
            documents = self.rag_pipeline.get_available_documents()
            return documents
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
    
    def search_documents(self, query: str, limit: int = 10) -> list:
        """Search for documents in the vector database."""
        try:
            results = self.vector_db.search(query, n_results=limit)
            return results
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Vector Database Creation and Update Script for College RAG Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python create_vector_db.py                    # Create/update vector database
    python create_vector_db.py --force           # Force re-processing of all documents
    python create_vector_db.py --info            # Show database information
    python create_vector_db.py --clear           # Clear all documents from database
    python create_vector_db.py --list            # List all documents in database
    python create_vector_db.py --search "python" # Search for documents containing "python"
        """
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-processing of all documents (even if already processed)'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show database information'
    )
    
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all documents from the database'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all documents in the database'
    )
    
    parser.add_argument(
        '--search',
        type=str,
        help='Search for documents containing the specified query'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Limit for search results (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data/documents', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('vector_db', exist_ok=True)
    
    # Initialize creator
    creator = VectorDBCreator()
    
    try:
        if args.info:
            # Show database information
            info = creator.get_database_info()
            print("\n" + "="*60)
            print("VECTOR DATABASE INFORMATION")
            print("="*60)
            print(f"Database Path: {info['database_path']}")
            print(f"Exists: {'✅ Yes' if info['exists'] else '❌ No'}")
            print(f"Collection Name: {info['collection_name']}")
            print(f"Embedding Model: {info['embedding_model']}")
            print(f"Total Documents: {info['total_documents']}")
            print(f"Unique Documents: {info['unique_documents']}")
            print(f"Total Chunks: {info['total_chunks']}")
            
            if 'error' in info:
                print(f"Error: {info['error']}")
            
            print("="*60)
            
        elif args.clear:
            # Clear database
            result = creator.clear_database()
            if result['success']:
                print("✅ " + result['message'])
            else:
                print("❌ " + result['message'])
                sys.exit(1)
                
        elif args.list:
            # List documents
            documents = creator.list_documents()
            print(f"\n📄 Documents in Database ({len(documents)} total):")
            print("-" * 60)
            
            if documents:
                for i, doc in enumerate(documents, 1):
                    status = "✅ Available" if doc.get('exists', False) else "❌ Missing"
                    print(f"{i:3d}. {doc.get('file_name', 'Unknown')} ({doc.get('file_type', 'Unknown')}) - {status}")
            else:
                print("No documents found in database.")
                
        elif args.search:
            # Search documents
            results = creator.search_documents(args.search, args.limit)
            print(f"\n🔍 Search Results for '{args.search}' ({len(results)} results):")
            print("-" * 60)
            
            if results:
                for i, result in enumerate(results, 1):
                    metadata = result.get('metadata', {})
                    file_name = metadata.get('file_name', 'Unknown')
                    similarity = result.get('similarity_score', 0)
                    print(f"{i:3d}. {file_name} (similarity: {similarity:.3f})")
            else:
                print("No results found.")
                
        else:
            # Create/update database
            print("🚀 Starting vector database creation/update...")
            print(f"Documents path: {creator.documents_path}")
            print(f"Vector DB path: {creator.vector_db_path}")
            print("-" * 60)
            
            result = creator.create_vector_db(force_update=args.force)
            
            if result['success']:
                print("✅ " + result['message'])
                print(f"⏱️  Time taken: {result['time_taken']:.2f} seconds")
                
                if 'database_info' in result:
                    info = result['database_info']
                    print(f"📊 Database stats: {info['total_documents']} chunks from {info['unique_documents']} documents")
            else:
                print("❌ " + result['message'])
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
