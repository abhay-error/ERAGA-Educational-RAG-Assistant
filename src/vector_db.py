import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
import re

from .config import config

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self):
        self.config = config.get_vector_db_config()
        self.persist_directory = self.config.get('persist_directory', './vector_db')
        self.embedding_model_name = self.config.get('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2')
        self.similarity_threshold = self.config.get('similarity_threshold', 0.2)
        
        # Create persist directory if it doesn't exist
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        try:
            # Try to initialize with proper device handling
            import torch
            
            # Set environment variable to force CPU usage
            os.environ['CUDA_VISIBLE_DEVICES'] = ''
            
            # Initialize the model without device specification first
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Try to move to CPU if needed, but handle meta tensor issues
            try:
                if hasattr(self.embedding_model, 'to'):
                    # Check if model is already on CPU
                    if next(self.embedding_model.parameters()).device.type != 'cpu':
                        self.embedding_model = self.embedding_model.to('cpu')
            except Exception as device_error:
                logger.warning(f"Could not move model to CPU: {device_error}")
                # Continue with the model as is
                
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            # Try alternative initialization without device specification
            try:
                self.embedding_model = SentenceTransformer(self.embedding_model_name)
            except Exception as e2:
                logger.error(f"Alternative initialization also failed: {e2}")
                raise e
        
        # Get or create collection
        self.collection = self._get_or_create_collection()
        
        logger.info(f"VectorDB initialized with model: {self.embedding_model_name}")
    
    def _get_or_create_collection(self):
        """Get existing collection or create a new one."""
        try:
            collection = self.client.get_collection("college_rag_documents")
            logger.info("Using existing collection: college_rag_documents")
        except:
            collection = self.client.create_collection(
                name="college_rag_documents",
                metadata={"description": "College RAG Assistant document embeddings"}
            )
            logger.info("Created new collection: college_rag_documents")
        
        return collection
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        try:
            # Clean and validate texts
            cleaned_texts = []
            for text in texts:
                if isinstance(text, str):
                    # Remove any problematic characters and ensure it's a valid string
                    cleaned_text = text.strip()
                    # Replace any non-printable characters and handle encoding issues
                    import re
                    # Remove surrogate pairs and other problematic characters
                    cleaned_text = re.sub(r'[\ud800-\udfff]', ' ', cleaned_text)
                    # Replace any non-printable characters
                    cleaned_text = re.sub(r'[^\x20-\x7E]', ' ', cleaned_text)
                    # Normalize whitespace
                    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
                    
                    if len(cleaned_text) > 0:
                        cleaned_texts.append(cleaned_text)
                    else:
                        # If text is empty, add a placeholder
                        cleaned_texts.append("empty document")
                else:
                    # If text is not a string, convert to string
                    cleaned_texts.append(str(text) if text else "empty document")
            
            if not cleaned_texts:
                logger.warning("No valid texts to embed")
                return []
            
            # Ensure all texts are strings and not empty
            final_texts = []
            for text in cleaned_texts:
                if isinstance(text, str) and text.strip():
                    final_texts.append(text.strip())
                else:
                    final_texts.append("empty document")
            
            # Generate embeddings in batches to avoid memory issues
            batch_size = 32
            all_embeddings = []
            
            for i in range(0, len(final_texts), batch_size):
                batch_texts = final_texts[i:i + batch_size]
                try:
                    # Generate embeddings for this batch
                    batch_embeddings = self.embedding_model.encode(batch_texts, convert_to_tensor=False)
                    
                    # Convert to list format
                    if hasattr(batch_embeddings, 'tolist'):
                        batch_list = batch_embeddings.tolist()
                    elif isinstance(batch_embeddings, list):
                        batch_list = batch_embeddings
                    else:
                        # Convert numpy array to list
                        import numpy as np
                        if isinstance(batch_embeddings, np.ndarray):
                            batch_list = batch_embeddings.tolist()
                        else:
                            logger.error(f"Unexpected embedding format: {type(batch_embeddings)}")
                            return []
                    
                    all_embeddings.extend(batch_list)
                    
                except Exception as e:
                    logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {e}")
                    # Add zero embeddings for failed batch
                    for _ in batch_texts:
                        all_embeddings.append([0.0] * 384)  # Default embedding size for all-MiniLM-L6-v2
            
            return all_embeddings
                    
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to the vector database."""
        if not documents:
            logger.warning("No documents to add")
            return False
        
        try:
            # Clean and prepare texts
            cleaned_documents = []
            for doc in documents:
                # Clean the text content
                text = doc.get('text', '')
                if isinstance(text, str):
                    # Remove problematic characters
                    import re
                    text = re.sub(r'[\ud800-\udfff]', ' ', text)
                    text = re.sub(r'[^\x20-\x7E]', ' ', text)
                    text = re.sub(r'\s+', ' ', text)
                    text = text.strip()
                    
                    if not text:
                        text = "empty document"
                else:
                    text = str(text) if text else "empty document"
                
                # Create cleaned document
                cleaned_doc = doc.copy()
                cleaned_doc['text'] = text
                cleaned_documents.append(cleaned_doc)
            
            texts = [doc['text'] for doc in cleaned_documents]
            embeddings = self._generate_embeddings(texts)
            
            if not embeddings:
                logger.error("Failed to generate embeddings")
                return False
            
            # Generate IDs for documents
            ids = [f"doc_{i}_{doc['file_name']}_{doc['chunk_index']}" 
                   for i, doc in enumerate(cleaned_documents)]
            
            # Prepare metadata
            metadatas = []
            for doc in cleaned_documents:
                metadata = {
                    'file_path': doc['file_path'],
                    'file_name': doc['file_name'],
                    'chunk_index': doc['chunk_index'],
                    'total_chunks': doc['total_chunks'],
                    'file_type': doc['file_type']
                }
                metadatas.append(metadata)
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully added {len(cleaned_documents)} documents to vector database")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector database: {e}")
            return False
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        try:
            # Generate embedding for query
            query_embedding = self._generate_embeddings([query])
            
            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return []
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Process results
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0], 
                    results['metadatas'][0], 
                    results['distances'][0]
                )):
                    # Convert distance to similarity score
                    similarity_score = 1 - distance
                    
                    # Only include results above threshold
                    if similarity_score >= self.similarity_threshold:
                        search_results.append({
                            'text': doc,
                            'metadata': metadata,
                            'similarity_score': similarity_score,
                            'rank': i + 1
                        })
            
            logger.info(f"Found {len(search_results)} relevant documents for query")
            return search_results
            
        except Exception as e:
            logger.error(f"Error searching vector database: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection.name,
                'embedding_model': self.embedding_model_name
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    def delete_documents_by_file(self, file_path: str) -> bool:
        """Delete all documents from a specific file."""
        try:
            # Get all documents from the file
            results = self.collection.get(
                where={"file_path": file_path}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} documents from {file_path}")
                return True
            else:
                logger.info(f"No documents found for file: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting documents for file {file_path}: {e}")
            return False
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection."""
        try:
            self.collection.delete(where={})
            logger.info("Cleared all documents from collection")
            return True
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            return False
