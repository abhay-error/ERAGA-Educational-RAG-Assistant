
# # import logging
# # from typing import List, Dict, Any, Optional
# # from .document_processor import DocumentProcessor
# # from .vector_db import VectorDB
# # from .web_search import WebSearch
# # from .llm_provider import LLMProvider
# # from .document_structure import DocumentStructureManager
# # import os

# # logger = logging.getLogger(__name__)

# # class RAGPipeline:
# #     def __init__(self):
# #         try:
# #             self.document_processor = DocumentProcessor()
# #             self.vector_db = VectorDB()
# #             self.web_search = WebSearch()
# #             self.llm_provider = LLMProvider()
# #             self.document_structure = DocumentStructureManager()
            
# #             logger.info("RAG Pipeline initialized")
# #         except Exception as e:
# #             logger.error(f"Error initializing RAG Pipeline: {e}")
# #             raise e
    
# #     def ingest_documents(self) -> Dict[str, Any]:
# #         """Ingest and process all documents in the documents folder."""
# #         try:
# #             logger.info("Starting document ingestion...")
            
# #             # Process documents
# #             processed_chunks = self.document_processor.process_documents()
            
# #             if not processed_chunks:
# #                 logger.info("No new documents to process")
# #                 return {
# #                     'success': True,
# #                     'message': 'No new documents to process',
# #                     'chunks_processed': 0
# #                 }
            
# #             # Add to vector database
# #             success = self.vector_db.add_documents(processed_chunks)
            
# #             if success:
# #                 logger.info(f"Successfully ingested {len(processed_chunks)} chunks")
# #                 return {
# #                     'success': True,
# #                     'message': f'Successfully processed {len(processed_chunks)} document chunks',
# #                     'chunks_processed': len(processed_chunks)
# #                 }
# #             else:
# #                 logger.error("Failed to add documents to vector database")
# #                 return {
# #                     'success': False,
# #                     'message': 'Failed to add documents to vector database',
# #                     'chunks_processed': 0
# #                 }
                
# #         except Exception as e:
# #             logger.error(f"Error during document ingestion: {e}")
# #             return {
# #                 'success': False,
# #                 'message': f'Error during document ingestion: {str(e)}',
# #                 'chunks_processed': 0
# #             }
    
# #     def process_query(self, query: str, use_web_search: bool = True, max_docs: int = 3, chat_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
# #         """
# #         Process a user query and return a response.
        
# #         Args:
# #             query: User query
# #             use_web_search: Whether to use web search
# #             max_docs: Maximum number of documents to retrieve
# #             chat_history: Previous chat messages for context
# #         """
# #         try:
# #             logger.info(f"Processing query: {query}")
            
# #             # Step 1: Search for relevant documents using document structure
# #             structure_results = self.document_structure.search_documents(query)
            
# #             # Step 2: Retrieve relevant documents from vector database
# #             doc_results = self.vector_db.search(query, n_results=max_docs)
            
# #             # Step 3: Combine structure and vector search results
# #             enhanced_results = self._enhance_results_with_structure(doc_results, structure_results)
            
# #             # Step 4: Perform web search if enabled
# #             web_results = []
# #             if use_web_search and self.web_search.enabled:
# #                 logger.info("Performing web search...")
# #                 web_results = self.web_search.search(query)
            
# #             # Step 5: Prepare context with chat history
# #             context = self._prepare_context(enhanced_results, web_results, chat_history)
            
# #             # Step 6: Generate response using LLM
# #             logger.info("Generating response...")
# #             response = self.llm_provider.generate_response(context, query)
            
# #             # Step 7: Prepare response with document information
# #             response_data = {
# #                 'response': response,
# #                 'sources': {
# #                     'documents': enhanced_results,
# #                     'web_search': web_results
# #                 },
# #                 'query_analysis': self._analyze_query_for_structure(query),
# #                 'directory_matches': structure_results[:5]  # Top 5 structure matches
# #             }
            
# #             logger.info("Query processing completed successfully")
# #             return response_data
            
# #         except Exception as e:
# #             logger.error(f"Error processing query: {e}")
# #             return {
# #                 'response': f"I'm sorry, I encountered an error while processing your query: {str(e)}",
# #                 'sources': {},
# #                 'query_analysis': {},
# #                 'directory_matches': []
# #             }
    
# #     def _analyze_query_for_structure(self, query: str) -> Dict[str, Any]:
# #         """Analyze query for dynamic structure patterns without hardcoding."""
# #         query_lower = query.lower()
# #         analysis = {
# #             'keywords': [],
# #             'numbers': [],
# #             'file_extensions': [],
# #             'path_patterns': [],
# #             'semantic_terms': []
# #         }
        
# #         # Extract numbers (could be module numbers, page numbers, etc.)
# #         import re
# #         numbers = re.findall(r'\b\d+\b', query_lower)
# #         analysis['numbers'] = numbers
        
# #         # Extract file extensions if mentioned
# #         extensions = re.findall(r'\.(\w+)\b', query_lower)
# #         analysis['file_extensions'] = extensions
        
# #         # Extract potential path patterns (words that might be directory names)
# #         path_patterns = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_-]*\b', query_lower)
# #         # Filter out common words and keep potential directory/file names
# #         common_words = {'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'about', 'this', 'that', 'these', 'those', 'what', 'where', 'when', 'why', 'how', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must', 'shall'}
# #         analysis['path_patterns'] = [word for word in path_patterns if word not in common_words and len(word) > 2]
        
# #         # Extract semantic terms (words that might indicate content type or subject)
# #         semantic_terms = []
# #         words = query_lower.split()
# #         for word in words:
# #             if len(word) > 3 and word not in common_words:
# #                 semantic_terms.append(word)
# #         analysis['semantic_terms'] = semantic_terms
        
# #         # Extract any quoted strings as potential exact matches
# #         quoted_strings = re.findall(r'"([^"]*)"', query)
# #         analysis['exact_matches'] = quoted_strings
        
# #         return analysis
    
# #     def _enhance_results_with_structure(self, doc_results: List[Dict[str, Any]], structure_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
# #         """Enhance search results with document structure information."""
# #         enhanced_results = []
        
# #         # Add vector search results
# #         for result in doc_results:
# #             enhanced_result = result.copy()
# #             enhanced_result['source'] = 'vector_search'
# #             enhanced_results.append(enhanced_result)
        
# #         # Add structure search results
# #         for result in structure_results:
# #             # Check if this document is already in enhanced_results
# #             existing = next((r for r in enhanced_results if r.get('metadata', {}).get('file_path') == result.get('path')), None)
            
# #             if existing:
# #                 # Enhance existing result with structure info
# #                 existing['structure_score'] = result.get('score', 0)
# #                 existing['match_reasons'] = result.get('match_reasons', [])
# #                 existing['source'] = 'combined'
# #             else:
# #                 # Add new result from structure search
# #                 enhanced_result = {
# #                     'content': f"Document: {result.get('name', 'Unknown')}",
# #                     'metadata': {
# #                         'file_path': result.get('path', ''),
# #                         'file_name': result.get('name', ''),
# #                         'file_type': result.get('type', ''),
# #                         'directory': result.get('directory', ''),
# #                         'relative_path': result.get('relative_path', '')
# #                     },
# #                     'score': result.get('score', 0),
# #                     'structure_score': result.get('score', 0),
# #                     'match_reasons': result.get('match_reasons', []),
# #                     'source': 'structure_search'
# #                 }
# #                 enhanced_results.append(enhanced_result)
        
# #         # Sort by combined score
# #         enhanced_results.sort(key=lambda x: (x.get('score', 0) + x.get('structure_score', 0)), reverse=True)
        
# #         return enhanced_results
    
# #     def _get_directory_matches(self, enhanced_results: List[Dict[str, Any]], query_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         """Get dynamic structure matches for the query."""
# #         matches = []
        
# #         for result in enhanced_results:
# #             metadata = result.get('metadata', {})
# #             file_path = metadata.get('file_path', '')
# #             file_name = metadata.get('file_name', '')
# #             text = result.get('text', '')
# #             match_reasons = result.get('match_reasons', [])
            
# #             # Check if this result has any matches
# #             if match_reasons:
# #                 matches.append({
# #                     'file_path': file_path,
# #                     'file_name': file_name,
# #                     'relative_path': metadata.get('relative_path', ''),
# #                     'match_reasons': match_reasons,
# #                     'relevance_score': result.get('structure_relevance', 0),
# #                     'query_analysis': query_analysis
# #                 })
        
# #         return matches
    
# #     def _prepare_context(self, doc_results: List[Dict[str, Any]], web_results: List[Dict[str, Any]], chat_history: List[Dict[str, Any]] = None) -> str:
# #         """Prepare context for LLM with enhanced directory structure information."""
# #         context_parts = []
        
# #         # Add chat history context if available
# #         if chat_history and len(chat_history) > 0:
# #             recent_context = []
# #             for msg in chat_history[-3:]:  # Last 3 messages for context
# #                 if msg.get('role') == 'user':
# #                     recent_context.append(f"User: {msg.get('content', '')}")
# #                 elif msg.get('role') == 'assistant':
# #                     recent_context.append(f"Assistant: {msg.get('content', '')}")
            
# #             if recent_context:
# #                 context_parts.append("Recent conversation context:")
# #                 context_parts.extend(recent_context)
# #                 context_parts.append("")
        
# #         # Add document context with dynamic structure information
# #         if doc_results:
# #             context_parts.append("Relevant documents from knowledge base:")
            
# #             for i, result in enumerate(doc_results[:3], 1):
# #                 metadata = result.get('metadata', {})
# #                 text = result.get('text', '')
# #                 file_path = metadata.get('file_path', '')
# #                 file_name = metadata.get('file_name', '')
# #                 match_reasons = result.get('match_reasons', [])
# #                 relevance_score = result.get('structure_relevance', 0)
                
# #                 # Add file information
# #                 file_info = f"Document {i}: {file_name}"
# #                 if file_path:
# #                     file_info += f" (Path: {file_path})"
                
# #                 # Add match information if available
# #                 if match_reasons:
# #                     file_info += f" [Matches: {', '.join(match_reasons)}]"
                
# #                 if relevance_score > 0:
# #                     file_info += f" [Relevance: {relevance_score}]"
                
# #                 context_parts.append(file_info)
# #                 context_parts.append(f"Content: {text[:300]}...")  # Reduced to 300 chars for faster processing
# #                 context_parts.append("")
        
# #         # Add web search results
# #         if web_results:
# #             context_parts.append("Additional information from web search:")
# #             for i, result in enumerate(web_results[:2], 1):
# #                 context_parts.append(f"Web result {i}: {result.get('title', 'No title')}")
# #                 context_parts.append(f"URL: {result.get('url', 'No URL')}")
# #                 context_parts.append(f"Content: {result.get('content', '')[:300]}...")
# #                 context_parts.append("")
        
# #         return "\n".join(context_parts)
    
# #     def get_system_info(self) -> Dict[str, Any]:
# #         """Get system information and status."""
# #         try:
# #             # Get vector database info
# #             vector_db_info = self.vector_db.get_collection_info()
            
# #             # Get web search status
# #             web_search_status = {
# #                 'enabled': self.web_search.enabled,
# #                 'providers': self.web_search.providers
# #             }
            
# #             # Get LLM provider info
# #             llm_info = {
# #                 'provider': self.llm_provider.provider,
# #                 'model': self.llm_provider.model
# #             }
            
# #             return {
# #                 'vector_database': vector_db_info,
# #                 'web_search': web_search_status,
# #                 'llm_provider': llm_info,
# #                 'status': 'operational'
# #             }
            
# #         except Exception as e:
# #             logger.error(f"Error getting system info: {e}")
# #             return {
# #                 'status': 'error',
# #                 'error': str(e)
# #             }
    
# #     def clear_documents(self) -> Dict[str, Any]:
# #         """Clear all documents from the vector database."""
# #         try:
# #             success = self.vector_db.clear_collection()
# #             if success:
# #                 return {
# #                     'success': True,
# #                     'message': 'All documents cleared from vector database'
# #                 }
# #             else:
# #                 return {
# #                     'success': False,
# #                     'message': 'Failed to clear documents from vector database'
# #                 }
# #         except Exception as e:
# #             logger.error(f"Error clearing documents: {e}")
# #             return {
# #                 'success': False,
# #                 'message': f'Error clearing documents: {str(e)}'
# #             }
    
# #     def process_single_file(self, file_path: str) -> Dict[str, Any]:
# #         """Process a single file and add it to the vector database."""
# #         try:
# #             logger.info(f"Processing single file: {file_path}")
            
# #             # Process the file
# #             processed_chunks = self.document_processor.process_single_file(file_path)
            
# #             if not processed_chunks:
# #                 return {
# #                     'success': False,
# #                     'message': f'No content extracted from {file_path}',
# #                     'chunks_processed': 0
# #                 }
            
# #             # Add to vector database
# #             success = self.vector_db.add_documents(processed_chunks)
            
# #             if success:
# #                 logger.info(f"Successfully processed {len(processed_chunks)} chunks from {file_path}")
# #                 return {
# #                     'success': True,
# #                     'message': f'Successfully processed {len(processed_chunks)} chunks from {file_path}',
# #                     'chunks_processed': len(processed_chunks)
# #                 }
# #             else:
# #                 logger.error(f"Failed to add documents from {file_path} to vector database")
# #                 return {
# #                     'success': False,
# #                     'message': f'Failed to add documents from {file_path} to vector database',
# #                     'chunks_processed': 0
# #                 }
                
# #         except Exception as e:
# #             logger.error(f"Error processing file {file_path}: {e}")
# #             return {
# #                 'success': False,
# #                 'message': f'Error processing file {file_path}: {str(e)}',
# #                 'chunks_processed': 0
# #             }

# #     def get_available_documents(self) -> List[Dict[str, Any]]:
# #         """Get list of all available documents in the vector database."""
# #         try:
# #             # Use document structure manager to get documents
# #             structure = self.document_structure.structure
# #             documents = []
            
# #             for doc_path, doc_info in structure.get('documents', {}).items():
# #                 documents.append({
# #                     'file_path': doc_info.get('path', ''),
# #                     'file_name': doc_info.get('name', ''),
# #                     'file_type': doc_info.get('type', ''),
# #                     'file_size': doc_info.get('size', 0),
# #                     'exists': os.path.exists(doc_info.get('path', '')),
# #                     'relative_path': doc_info.get('relative_path', ''),
# #                     'directory': doc_info.get('directory', ''),
# #                     'keywords': doc_info.get('keywords', [])
# #                 })
            
# #             return documents
            
# #         except Exception as e:
# #             logger.error(f"Error getting available documents: {e}")
# #             return []

# #     def get_document_by_path(self, file_path: str) -> Optional[Dict[str, Any]]:
# #         """Get document information by file path."""
# #         try:
# #             if not os.path.exists(file_path):
# #                 logger.warning(f"File does not exist: {file_path}")
# #                 return None
            
# #             # Get file stats
# #             file_stat = os.stat(file_path)
            
# #             return {
# #                 'file_path': file_path,
# #                 'file_name': os.path.basename(file_path),
# #                 'file_type': os.path.splitext(file_path)[1].lower(),
# #                 'file_size': file_stat.st_size,
# #                 'last_modified': file_stat.st_mtime,
# #                 'exists': True
# #             }
            
# #         except Exception as e:
# #             logger.error(f"Error getting document info for {file_path}: {e}")
# #             return None

# #     def search_documents_for_download(self, query: str) -> List[Dict[str, Any]]:
# #         """Search for documents that match the query for download purposes."""
# #         try:
# #             # Use document structure manager to search for documents
# #             search_results = self.document_structure.search_documents(query)
            
# #             # Convert to the expected format
# #             documents = []
# #             for result in search_results:
# #                 doc_info = {
# #                     'file_path': result.get('path', ''),
# #                     'file_name': result.get('name', ''),
# #                     'file_type': result.get('type', ''),
# #                     'file_size': result.get('size', 0),
# #                     'exists': os.path.exists(result.get('path', '')),
# #                     'relative_path': result.get('relative_path', ''),
# #                     'directory': result.get('directory', ''),
# #                     'keywords': result.get('keywords', []),
# #                     'score': result.get('score', 0),
# #                     'match_reasons': result.get('match_reasons', [])
# #                 }
# #                 documents.append(doc_info)
            
# #             return documents
            
# #         except Exception as e:
# #             logger.error(f"Error searching documents for download: {e}")
# #             return []

# #     def get_document_content(self, file_path: str) -> Optional[bytes]:
# #         """Get the raw content of a document file."""
# #         try:
# #             if not os.path.exists(file_path):
# #                 logger.warning(f"File does not exist: {file_path}")
# #                 return None
            
# #             with open(file_path, 'rb') as f:
# #                 return f.read()
                
# #         except Exception as e:
# #             logger.error(f"Error reading document content for {file_path}: {e}")
# #             return None








# import logging
# from typing import List, Dict, Any, Optional
# from .document_processor import DocumentProcessor
# from .vector_db import VectorDB
# from .web_search import WebSearch
# from .llm_provider import LLMProvider
# from .document_structure import DocumentStructureManager
# import os
# import re
# import json
# import ast

# logger = logging.getLogger(__name__)


# class RAGPipeline:
#     def __init__(self):
#         try:
#             self.document_processor = DocumentProcessor()
#             self.vector_db = VectorDB()
#             self.web_search = WebSearch()
#             self.llm_provider = LLMProvider()
#             self.document_structure = DocumentStructureManager()

#             logger.info("RAG Pipeline initialized")
#         except Exception as e:
#             logger.error(f"Error initializing RAG Pipeline: {e}")
#             raise e

#     def ingest_documents(self) -> Dict[str, Any]:
#         """Ingest and process all documents in the documents folder."""
#         try:
#             logger.info("Starting document ingestion...")

#             # Process documents
#             processed_chunks = self.document_processor.process_documents()

#             if not processed_chunks:
#                 logger.info("No new documents to process")
#                 return {
#                     'success': True,
#                     'message': 'No new documents to process',
#                     'chunks_processed': 0
#                 }

#             # Add to vector database
#             success = self.vector_db.add_documents(processed_chunks)

#             if success:
#                 logger.info(f"Successfully ingested {len(processed_chunks)} chunks")
#                 return {
#                     'success': True,
#                     'message': f'Successfully processed {len(processed_chunks)} document chunks',
#                     'chunks_processed': len(processed_chunks)
#                 }
#             else:
#                 logger.error("Failed to add documents to vector database")
#                 return {
#                     'success': False,
#                     'message': 'Failed to add documents to vector database',
#                     'chunks_processed': 0
#                 }

#         except Exception as e:
#             logger.error(f"Error during document ingestion: {e}")
#             return {
#                 'success': False,
#                 'message': f'Error during document ingestion: {str(e)}',
#                 'chunks_processed': 0
#             }

#     def process_query(self, query: str, use_web_search: bool = True, max_docs: int = 3, chat_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
#         """
#         Process a user query and return a response.

#         Args:
#             query: User query
#             use_web_search: Whether to use web search
#             max_docs: Maximum number of documents to retrieve
#             chat_history: Previous chat messages for context
#         """
#         try:
#             logger.info(f"Processing query: {query}")

#             # Step 1: Search for relevant documents using document structure
#             structure_results = self.document_structure.search_documents(query)

#             # Step 2: Retrieve relevant documents from vector database
#             doc_results = self.vector_db.search(query, n_results=max_docs)

#             # Step 3: Combine structure and vector search results
#             enhanced_results = self._enhance_results_with_structure(doc_results, structure_results)

#             # Step 4: Perform web search if enabled
#             web_results = []
#             if use_web_search and getattr(self.web_search, "enabled", False):
#                 logger.info("Performing web search...")
#                 web_results = self.web_search.search(query)

#             # Step 5: Prepare context with chat history
#             context = self._prepare_context(enhanced_results, web_results, chat_history)

#             # Step 6: Generate response using LLM
#             logger.info("Generating response...")
#             response = self.llm_provider.generate_response(context, query)

#             # Step 7: Prepare response with document information
#             response_data = {
#                 'response': response,
#                 'sources': {
#                     'documents': enhanced_results,
#                     'web_search': web_results
#                 },
#                 'query_analysis': self._analyze_query_for_structure(query),
#                 'directory_matches': structure_results[:5]  # Top 5 structure matches
#             }

#             logger.info("Query processing completed successfully")
#             return response_data

#         except Exception as e:
#             logger.error(f"Error processing query: {e}", exc_info=True)
#             return {
#                 'response': f"I'm sorry, I encountered an error while processing your query: {str(e)}",
#                 'sources': {},
#                 'query_analysis': {},
#                 'directory_matches': []
#             }

#     def _analyze_query_for_structure(self, query: str) -> Dict[str, Any]:
#         """Analyze query for dynamic structure patterns without hardcoding."""
#         query_lower = query.lower()
#         analysis = {
#             'keywords': [],
#             'numbers': [],
#             'file_extensions': [],
#             'path_patterns': [],
#             'semantic_terms': []
#         }

#         # Extract numbers (could be module numbers, page numbers, etc.)
#         numbers = re.findall(r'\b\d+\b', query_lower)
#         analysis['numbers'] = numbers

#         # Extract file extensions if mentioned
#         extensions = re.findall(r'\.(\w+)\b', query_lower)
#         analysis['file_extensions'] = extensions

#         # Extract potential path patterns (words that might be directory names)
#         path_patterns = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_-]*\b', query_lower)
#         # Filter out common words and keep potential directory/file names
#         common_words = {'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'about', 'this', 'that', 'these', 'those', 'what', 'where', 'when', 'why', 'how', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must', 'shall'}
#         analysis['path_patterns'] = [word for word in path_patterns if word not in common_words and len(word) > 2]

#         # Extract semantic terms (words that might indicate content type or subject)
#         semantic_terms = []
#         words = query_lower.split()
#         for word in words:
#             if len(word) > 3 and word not in common_words:
#                 semantic_terms.append(word)
#         analysis['semantic_terms'] = semantic_terms

#         # Extract any quoted strings as potential exact matches
#         quoted_strings = re.findall(r'"([^"]*)"', query)
#         analysis['exact_matches'] = quoted_strings

#         return analysis

#     def _enhance_results_with_structure(self, doc_results: List[Dict[str, Any]], structure_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         """Enhance search results with document structure information."""
#         enhanced_results = []

#         # Add vector search results
#         for result in doc_results:
#             enhanced_result = result.copy()
#             enhanced_result['source'] = 'vector_search'
#             enhanced_results.append(enhanced_result)

#         # Add structure search results
#         for result in structure_results:
#             # Check if this document is already in enhanced_results
#             existing = next((r for r in enhanced_results if r.get('metadata', {}).get('file_path') == result.get('path')), None)

#             if existing:
#                 # Enhance existing result with structure info
#                 existing['structure_score'] = result.get('score', 0)
#                 existing['match_reasons'] = result.get('match_reasons', [])
#                 existing['source'] = 'combined'
#             else:
#                 # Add new result from structure search
#                 enhanced_result = {
#                     'content': f"Document: {result.get('name', 'Unknown')}",
#                     'metadata': {
#                         'file_path': result.get('path', ''),
#                         'file_name': result.get('name', ''),
#                         'file_type': result.get('type', ''),
#                         'directory': result.get('directory', ''),
#                         'relative_path': result.get('relative_path', '')
#                     },
#                     'score': result.get('score', 0),
#                     'structure_score': result.get('score', 0),
#                     'match_reasons': result.get('match_reasons', []),
#                     'source': 'structure_search'
#                 }
#                 enhanced_results.append(enhanced_result)

#         # Sort by combined score
#         enhanced_results.sort(key=lambda x: (x.get('score', 0) + x.get('structure_score', 0)), reverse=True)

#         return enhanced_results

#     def _get_directory_matches(self, enhanced_results: List[Dict[str, Any]], query_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Get dynamic structure matches for the query."""
#         matches = []

#         for result in enhanced_results:
#             metadata = result.get('metadata', {})
#             file_path = metadata.get('file_path', '')
#             file_name = metadata.get('file_name', '')
#             text = result.get('text', '')
#             match_reasons = result.get('match_reasons', [])

#             # Check if this result has any matches
#             if match_reasons:
#                 matches.append({
#                     'file_path': file_path,
#                     'file_name': file_name,
#                     'relative_path': metadata.get('relative_path', ''),
#                     'match_reasons': match_reasons,
#                     'relevance_score': result.get('structure_relevance', 0),
#                     'query_analysis': query_analysis
#                 })

#         return matches

#     def _prepare_context(self, doc_results: List[Dict[str, Any]], web_results: List[Dict[str, Any]], chat_history: List[Dict[str, Any]] = None) -> str:
#         """Prepare context for LLM with enhanced directory structure information."""
#         context_parts = []

#         # Add chat history context if available
#         if chat_history and len(chat_history) > 0:
#             recent_context = []
#             for msg in chat_history[-3:]:  # Last 3 messages for context
#                 if msg.get('role') == 'user':
#                     recent_context.append(f"User: {msg.get('content', '')}")
#                 elif msg.get('role') == 'assistant':
#                     recent_context.append(f"Assistant: {msg.get('content', '')}")

#             if recent_context:
#                 context_parts.append("Recent conversation context:")
#                 context_parts.extend(recent_context)
#                 context_parts.append("")

#         # Add document context with dynamic structure information
#         if doc_results:
#             context_parts.append("Relevant documents from knowledge base:")

#             for i, result in enumerate(doc_results[:3], 1):
#                 metadata = result.get('metadata', {})
#                 text = result.get('text', '')
#                 file_path = metadata.get('file_path', '')
#                 file_name = metadata.get('file_name', '')
#                 match_reasons = result.get('match_reasons', [])
#                 relevance_score = result.get('structure_relevance', 0)

#                 # Add file information
#                 file_info = f"Document {i}: {file_name}"
#                 if file_path:
#                     file_info += f" (Path: {file_path})"

#                 # Add match information if available
#                 if match_reasons:
#                     file_info += f" [Matches: {', '.join(match_reasons)}]"

#                 if relevance_score > 0:
#                     file_info += f" [Relevance: {relevance_score}]"

#                 context_parts.append(file_info)
#                 context_parts.append(f"Content: {text[:300]}...")  # Reduced to 300 chars for faster processing
#                 context_parts.append("")

#         # Add web search results
#         if web_results:
#             context_parts.append("Additional information from web search:")
#             for i, result in enumerate(web_results[:2], 1):
#                 context_parts.append(f"Web result {i}: {result.get('title', 'No title')}")
#                 context_parts.append(f"URL: {result.get('url', 'No URL')}")
#                 context_parts.append(f"Content: {result.get('content', '')[:300]}...")
#                 context_parts.append("")

#         return "\n".join(context_parts)

#     def get_system_info(self) -> Dict[str, Any]:
#         """Get system information and status."""
#         try:
#             # Get vector database info
#             vector_db_info = self.vector_db.get_collection_info()

#             # Get web search status
#             web_search_status = {
#                 'enabled': getattr(self.web_search, 'enabled', False),
#                 'providers': getattr(self.web_search, 'providers', [])
#             }

#             # Get LLM provider info
#             llm_info = {
#                 'provider': getattr(self.llm_provider, 'provider', 'unknown'),
#                 'model': getattr(self.llm_provider, 'model', 'unknown')
#             }

#             return {
#                 'vector_database': vector_db_info,
#                 'web_search': web_search_status,
#                 'llm_provider': llm_info,
#                 'status': 'operational'
#             }

#         except Exception as e:
#             logger.error(f"Error getting system info: {e}")
#             return {
#                 'status': 'error',
#                 'error': str(e)
#             }

#     def clear_documents(self) -> Dict[str, Any]:
#         """Clear all documents from the vector database."""
#         try:
#             success = self.vector_db.clear_collection()
#             if success:
#                 return {
#                     'success': True,
#                     'message': 'All documents cleared from vector database'
#                 }
#             else:
#                 return {
#                     'success': False,
#                     'message': 'Failed to clear documents from vector database'
#                 }
#         except Exception as e:
#             logger.error(f"Error clearing documents: {e}")
#             return {
#                 'success': False,
#                 'message': f'Error clearing documents: {str(e)}'
#             }

#     def process_single_file(self, file_path: str) -> Dict[str, Any]:
#         """Process a single file and add it to the vector database."""
#         try:
#             logger.info(f"Processing single file: {file_path}")

#             # Process the file
#             processed_chunks = self.document_processor.process_single_file(file_path)

#             if not processed_chunks:
#                 return {
#                     'success': False,
#                     'message': f'No content extracted from {file_path}',
#                     'chunks_processed': 0
#                 }

#             # Add to vector database
#             success = self.vector_db.add_documents(processed_chunks)

#             if success:
#                 logger.info(f"Successfully processed {len(processed_chunks)} chunks from {file_path}")
#                 return {
#                     'success': True,
#                     'message': f'Successfully processed {len(processed_chunks)} chunks from {file_path}',
#                     'chunks_processed': len(processed_chunks)
#                 }
#             else:
#                 logger.error(f"Failed to add documents from {file_path} to vector database")
#                 return {
#                     'success': False,
#                     'message': f'Failed to add documents from {file_path} to vector database',
#                     'chunks_processed': 0
#                 }

#         except Exception as e:
#             logger.error(f"Error processing file {file_path}: {e}")
#             return {
#                 'success': False,
#                 'message': f'Error processing file {file_path}: {str(e)}',
#                 'chunks_processed': 0
#             }

#     def get_available_documents(self) -> List[Dict[str, Any]]:
#         """Get list of all available documents in the vector database."""
#         try:
#             # Use document structure manager to get documents
#             structure = getattr(self.document_structure, 'structure', {})
#             documents = []

#             for doc_path, doc_info in structure.get('documents', {}).items():
#                 documents.append({
#                     'file_path': doc_info.get('path', ''),
#                     'file_name': doc_info.get('name', ''),
#                     'file_type': doc_info.get('type', ''),
#                     'file_size': doc_info.get('size', 0),
#                     'exists': os.path.exists(doc_info.get('path', '')),
#                     'relative_path': doc_info.get('relative_path', ''),
#                     'directory': doc_info.get('directory', ''),
#                     'keywords': doc_info.get('keywords', [])
#                 })

#             return documents

#         except Exception as e:
#             logger.error(f"Error getting available documents: {e}")
#             return []

#     def get_document_by_path(self, file_path: str) -> Optional[Dict[str, Any]]:
#         """Get document information by file path."""
#         try:
#             if not os.path.exists(file_path):
#                 logger.warning(f"File does not exist: {file_path}")
#                 return None

#             # Get file stats
#             file_stat = os.stat(file_path)

#             return {
#                 'file_path': file_path,
#                 'file_name': os.path.basename(file_path),
#                 'file_type': os.path.splitext(file_path)[1].lower(),
#                 'file_size': file_stat.st_size,
#                 'last_modified': file_stat.st_mtime,
#                 'exists': True
#             }

#         except Exception as e:
#             logger.error(f"Error getting document info for {file_path}: {e}")
#             return None

#     def search_documents_for_download(self, query: str, llm_rerank: bool = True, max_results: int = 50) -> List[Dict[str, Any]]:
#         """
#         LLM-aware document search across nested directories.

#         Steps:
#          - Use document structure search (filename / path metadata)
#          - Use vector DB semantic search
#          - Merge results, deduplicate
#          - Optionally ask LLM to re-rank the merged results (returns a map file_path -> score)
#          - Return sorted list suitable for the UI
#         """
#         try:
#             # Step 1: Structure-based search (filename, path keywords)
#             structure_results = self.document_structure.search_documents(query) or []

#             # Normalize structure results into a common schema
#             norm_structure = []
#             for r in structure_results:
#                 file_path = r.get('path') or r.get('file_path') or ''
#                 norm_structure.append({
#                     'file_path': file_path,
#                     'file_name': r.get('name') or os.path.basename(file_path),
#                     'file_type': r.get('type') or os.path.splitext(file_path)[1].lstrip('.'),
#                     'file_size': r.get('size', 0),
#                     'exists': os.path.exists(file_path),
#                     'relative_path': r.get('relative_path', ''),
#                     'directory': r.get('directory', ''),
#                     'keywords': r.get('keywords', []),
#                     'score': float(r.get('score', 0)),
#                     'match_reasons': r.get('match_reasons', [])
#                 })

#             # Step 2: Vector-based semantic search (document content)
#             vector_results = self.vector_db.search(query, n_results=max_results) or []

#             norm_vector = []
#             for res in vector_results:
#                 meta = res.get('metadata', {})
#                 fp = meta.get('file_path') or meta.get('path') or ''
#                 # try to get size if file exists
#                 size = 0
#                 if fp and os.path.exists(fp):
#                     try:
#                         size = os.path.getsize(fp)
#                     except Exception:
#                         size = 0
#                 norm_vector.append({
#                     'file_path': fp,
#                     'file_name': meta.get('file_name') or os.path.basename(fp),
#                     'file_type': meta.get('file_type') or os.path.splitext(fp)[1].lstrip('.'),
#                     'file_size': size,
#                     'exists': os.path.exists(fp),
#                     'relative_path': meta.get('relative_path', ''),
#                     'directory': meta.get('directory', ''),
#                     'keywords': meta.get('keywords', []),
#                     'score': float(res.get('score', 0)),
#                     'match_reasons': meta.get('match_reasons', [])
#                 })

#             # Step 3: Merge & deduplicate by file_path, keep best score seen
#             merged: Dict[str, Dict[str, Any]] = {}
#             for doc in (norm_structure + norm_vector):
#                 fp = doc.get('file_path') or f"__unknown__:{doc.get('file_name')}"
#                 if fp in merged:
#                     # keep the highest score and merge match_reasons
#                     merged[fp]['score'] = max(merged[fp].get('score', 0), doc.get('score', 0))
#                     merged[fp]['match_reasons'] = list(set(merged[fp].get('match_reasons', []) + doc.get('match_reasons', [])))
#                 else:
#                     merged[fp] = doc.copy()

#             docs_list = list(merged.values())

#             # Step 4: Optionally ask LLM to re-rank documents by relevance to the query
#             if llm_rerank and getattr(self.llm_provider, 'generate_response', None):
#                 try:
#                     # Prepare a compact prompt listing document candidates
#                     prompt_lines = [
#                         "You are given a user query and a list of candidate documents (file path and short metadata).",
#                         "Return a JSON object mapping each file_path to a relevance score between 0.0 (irrelevant) and 1.0 (very relevant).",
#                         "Only return valid JSON. Do not include any extra commentary.",
#                         "",
#                         f"User query: {query}",
#                         "",
#                         "Candidates:"
#                     ]
#                     for d in docs_list[:40]:  # limit to top 40 candidates for prompt length
#                         prompt_lines.append(json.dumps({
#                             'file_path': d.get('file_path'),
#                             'file_name': d.get('file_name'),
#                             'file_type': d.get('file_type'),
#                             'file_size': d.get('file_size'),
#                             'score': d.get('score', 0),
#                             'match_reasons': d.get('match_reasons', [])
#                         }))
#                     prompt_text = "\n".join(prompt_lines)

#                     # Call the LLM to produce scores
#                     llm_resp = self.llm_provider.generate_response(prompt_text, query=None)  # if LLM expects (context, query), we put prompt_text as context.
#                     # Try to extract JSON from LLM response
#                     json_text = llm_resp.strip()
#                     # If LLM added text before/after JSON, try to find the JSON block
#                     json_match = re.search(r'(\{[\s\S]*\})', json_text)
#                     if json_match:
#                         json_text = json_match.group(1)

#                     score_map = {}
#                     try:
#                         score_map = json.loads(json_text)
#                     except Exception:
#                         # as fallback, try ast.literal_eval
#                         try:
#                             score_map = ast.literal_eval(json_text)
#                         except Exception:
#                             score_map = {}

#                     # If we have a workable score_map, apply it
#                     if isinstance(score_map, dict) and score_map:
#                         for d in docs_list:
#                             fp = d.get('file_path')
#                             if fp in score_map:
#                                 try:
#                                     d['llm_score'] = float(score_map[fp])
#                                 except Exception:
#                                     d['llm_score'] = 0.0
#                             else:
#                                 d['llm_score'] = 0.0

#                         # sort by llm_score then fallback to 'score'
#                         docs_list.sort(key=lambda x: (x.get('llm_score', 0.0), x.get('score', 0.0)), reverse=True)
#                         # Limit number returned
#                         return docs_list[:max_results]
#                     else:
#                         logger.warning("LLM re-rank returned no usable JSON; falling back to combined-score ranking.")
#                 except Exception as e:
#                     logger.error(f"LLM re-ranking failed: {e}", exc_info=True)

#             # Step 5: Fallback ranking using combined score (structure + semantic)
#             for d in docs_list:
#                 # combined_score uses available 'score'; structure-derived docs often have 'score' from structure,
#                 # vector docs have 'score' from vector DB. This is a simple heuristic.
#                 d['combined_score'] = float(d.get('score', 0.0))
#             docs_list.sort(key=lambda x: x.get('combined_score', 0.0), reverse=True)

#             return docs_list[:max_results]

#         except Exception as e:
#             logger.error(f"Error searching documents for download: {e}", exc_info=True)
#             return []

#     def get_document_content(self, file_path: str) -> Optional[bytes]:
#         """Get the raw content of a document file."""
#         try:
#             if not os.path.exists(file_path):
#                 logger.warning(f"File does not exist: {file_path}")
#                 return None

#             with open(file_path, 'rb') as f:
#                 return f.read()

#         except Exception as e:
#             logger.error(f"Error reading document content for {file_path}: {e}")
#             return None



# rag_pipeline.py
import logging
from typing import List, Dict, Any, Optional
import os
import re
import json
import ast
from datetime import datetime

from .document_processor import DocumentProcessor
from .vector_db import VectorDB
from .web_search import WebSearch
from .llm_provider import LLMProvider
from .document_structure import DocumentStructureManager

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Default weights (tweak as needed)
VECTOR_WEIGHT = 0.55
STRUCTURE_WEIGHT = 0.30
HIERARCHY_WEIGHT = 0.15

# ---------- default abbreviation map ----------
# Keys should be lowercase. Values are expansions (phrases) used during normalization.
DEFAULT_ABBREV_MAP = {
    # Module / structural
    "mod": "module",
    "mod.": "module",
    "module": "module",

    # Semester / sem
    "sem": "semester",
    "semester": "semester",

    # Evaluation / grading terms
    "cie": "continuous internal evaluation",
    "cie.": "continuous internal evaluation",
    "qp": "question paper",
    "qp.": "question paper",
    "qb": "question bank",
    "qp qb": "question bank",

    # Common course abbreviations / subjects
    "dbms": "database management system",
    "pai": "principles of ai",
    "atc": "autometa",
    "m&e": "management and entrepreneurship",
    "me": "management and entrepreneurship",
    "web-tech": "web technology",
    "webtech": "web technology",
    "big_data": "big data",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "ds": "data science",
    "csd": "computer science and design",
    "cse": "computer science and engineering",
    "qb cie": "question bank continuous internal evaluation",
    "qp cie": "question paper continuous internal evaluation"
}
# ----------------------------------------------

class RAGPipeline:
    def __init__(self,
                 documents_root: Optional[str] = None,
                 vector_weight: float = VECTOR_WEIGHT,
                 structure_weight: float = STRUCTURE_WEIGHT,
                 hierarchy_weight: float = HIERARCHY_WEIGHT,
                 abbrev_map: Optional[Dict[str, str]] = None,
                 abbrev_file: Optional[str] = None,
                 debug: bool = False):
        """
        RAGPipeline with configurable abbreviation expansion.

        Args:
            documents_root: base path for filesystem fallback search.
            abbrev_map: optional dict of abbreviations to load/merge with defaults.
            abbrev_file: optional path to JSON file to load abbreviations from.
            debug: enable debug logging and extra debug_info in responses.
        """
        try:
            # core components
            self.document_processor = DocumentProcessor()
            self.vector_db = VectorDB()
            self.web_search = WebSearch()
            self.llm_provider = LLMProvider()
            self.document_structure = DocumentStructureManager()

            # scoring weights
            self.vector_weight = vector_weight
            self.structure_weight = structure_weight
            self.hierarchy_weight = hierarchy_weight

            # abbreviation map: start with defaults, then extend with file and provided map
            self.abbrev_map = {k.lower(): v for k, v in DEFAULT_ABBREV_MAP.items()}

            # if abbrev_file provided, try to load and merge
            self.abbrev_file = None
            if abbrev_file:
                try:
                    loaded = self._load_abbrev_file(abbrev_file)
                    if loaded:
                        self.abbrev_map.update({k.lower(): v for k, v in loaded.items()})
                        self.abbrev_file = os.path.abspath(abbrev_file)
                        logger.debug(f"Loaded abbreviations from file: {self.abbrev_file}")
                except Exception as e:
                    logger.warning(f"Failed to load abbreviation file {abbrev_file}: {e}", exc_info=True)

            # merge provided abbrev_map
            if abbrev_map:
                self.abbrev_map.update({k.lower(): v for k, v in abbrev_map.items()})

            # compute documents_root (priority: constructor -> doc structure -> default)
            self.documents_root = None
            if documents_root:
                self.documents_root = os.path.abspath(documents_root)
            else:
                for attr in ('root', 'root_dir', 'base_path', 'documents_root', 'root_path'):
                    candidate = getattr(self.document_structure, attr, None)
                    if candidate:
                        self.documents_root = os.path.abspath(candidate)
                        break
            if not self.documents_root:
                self.documents_root = os.path.abspath(os.path.join('.', 'data', 'documents'))

            # debug mode and last expansions container
            self.debug = debug
            self._last_expansions = []  # stores tuples (abbr, expansion) for last normalization
            if debug:
                logger.setLevel(logging.DEBUG)
                if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
                    ch = logging.StreamHandler()
                    ch.setLevel(logging.DEBUG)
                    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
                    ch.setFormatter(formatter)
                    logger.addHandler(ch)
                logger.debug("Debug enabled for RAGPipeline")

            logger.info(f"RAG Pipeline initialized (documents_root={self.documents_root})")
        except Exception as e:
            logger.error(f"Error initializing RAG Pipeline: {e}", exc_info=True)
            raise

    # ---------- Abbreviation file helpers ----------
    def _load_abbrev_file(self, path: str) -> Dict[str, str]:
        """Load abbreviations from a JSON file (returns dict)."""
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Abbreviation file must contain a JSON object mapping abbreviations to expansions.")
        return {k.lower(): v for k, v in data.items()}

    def save_abbreviations(self, path: Optional[str] = None) -> str:
        """Save current abbreviations to a JSON file. Returns the path saved to."""
        out = path or self.abbrev_file or os.path.abspath('abbreviations.json')
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(self.abbrev_map, f, ensure_ascii=False, indent=2)
        self.abbrev_file = os.path.abspath(out)
        logger.info(f"Saved abbreviations to {self.abbrev_file}")
        return self.abbrev_file

    def add_abbreviation(self, abbr: str, expansion: str, persist: bool = False) -> None:
        """Add or update an abbreviation mapping. Optionally persist to file."""
        if not abbr or not expansion:
            raise ValueError("abbr and expansion must be non-empty strings")
        self.abbrev_map[abbr.lower()] = expansion
        logger.debug(f"Abbreviation added: {abbr.lower()} -> {expansion}")
        if persist and self.abbrev_file:
            self.save_abbreviations(self.abbrev_file)

    def remove_abbreviation(self, abbr: str, persist: bool = False) -> bool:
        """Remove an abbreviation mapping. Returns True if removed."""
        k = abbr.lower()
        if k in self.abbrev_map:
            del self.abbrev_map[k]
            logger.debug(f"Abbreviation removed: {k}")
            if persist and self.abbrev_file:
                self.save_abbreviations(self.abbrev_file)
            return True
        return False

    def get_abbreviations(self) -> Dict[str, str]:
        """Return a copy of the abbreviation map."""
        return dict(self.abbrev_map)

    # ---------- Ingestion (unchanged) ----------
    def ingest_documents(self) -> Dict[str, Any]:
        try:
            logger.info("Starting document ingestion...")
            processed_chunks = self.document_processor.process_documents()
            if not processed_chunks:
                logger.info("No new documents to process")
                return {'success': True, 'message': 'No new documents to process', 'chunks_processed': 0}
            success = self.vector_db.add_documents(processed_chunks)
            if success:
                logger.info(f"Successfully ingested {len(processed_chunks)} chunks")
                return {'success': True, 'message': f'Successfully processed {len(processed_chunks)} document chunks', 'chunks_processed': len(processed_chunks)}
            else:
                logger.error("Failed to add documents to vector database")
                return {'success': False, 'message': 'Failed to add documents to vector database', 'chunks_processed': 0}
        except Exception as e:
            logger.error("Error during document ingestion", exc_info=True)
            return {'success': False, 'message': f'Error during document ingestion: {str(e)}', 'chunks_processed': 0}

    # ---------- Query processing ----------
    def process_query(self, query: str, use_web_search: bool = True, max_docs: int = 3, chat_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        debug_info: Dict[str, Any] = {'timestamp': datetime.utcnow().isoformat(), 'query': query}
        try:
            logger.info(f"Processing query: {query}")
            normalized_query = self._normalize_query(query)
            debug_info['normalized_query'] = normalized_query
            debug_info['expansions_applied'] = list(self._last_expansions)  # copy

            # Step 1: structure search
            try:
                structure_results = self.document_structure.search_documents(normalized_query) or []
            except Exception as e:
                logger.warning(f"DocumentStructureManager.search_documents failed: {e}", exc_info=True)
                structure_results = []
            debug_info['structure_count'] = len(structure_results)
            logger.debug(f"Structure search returned {len(structure_results)} items")

            # Step 2: vector search
            try:
                doc_results = self.vector_db.search(normalized_query, n_results=max_docs) or []
            except Exception as e:
                logger.warning(f"VectorDB.search failed: {e}", exc_info=True)
                doc_results = []
            debug_info['vector_count'] = len(doc_results)
            logger.debug(f"Vector search returned {len(doc_results)} items")

            # Step 3: filesystem fallback as before
            fs_results = []
            should_fs_search = False
            if not structure_results or not doc_results:
                should_fs_search = True
            if re.search(r'[\\/]|\.pdf|\.ppt|module|mod|qp|qb|question|paper|\bmod\d+\b|\bcie\b', normalized_query):
                should_fs_search = True
            if should_fs_search:
                try:
                    fs_results = self._filesystem_search(query, max_results=200)
                except Exception as e:
                    logger.warning(f"Filesystem search failed: {e}", exc_info=True)
                    fs_results = []
            debug_info['filesystem_count'] = len(fs_results)
            logger.debug(f"Filesystem fallback search returned {len(fs_results)} items")

            # Step 4: merge and enhance
            enhanced_results = self._enhance_results_with_structure(doc_results, structure_results, normalized_query, fs_results)
            debug_info['enhanced_count'] = len(enhanced_results)
            logger.debug(f"Enhanced results count: {len(enhanced_results)}")

            # Step 5: web search (optional)
            web_results = []
            if use_web_search and getattr(self.web_search, "enabled", False):
                try:
                    web_results = self.web_search.search(normalized_query)
                except Exception as e:
                    logger.warning(f"Web search failed: {e}", exc_info=True)
            debug_info['web_count'] = len(web_results)

            # Step 6: LLM
            context = self._prepare_context(enhanced_results, web_results, chat_history)
            logger.debug("Prepared LLM context (truncated) -> " + (context[:400] + "..." if context else "EMPTY"))
            try:
                response_text = self.llm_provider.generate_response(context, query)
            except Exception as e:
                logger.error(f"LLM generate_response failed: {e}", exc_info=True)
                response_text = "Sorry — LLM generation failed."

            # Debug printout if debug mode enabled
            if self.debug:
                self._debug_log_summary(structure_results, doc_results, fs_results, enhanced_results)

            result = {
                'response': response_text,
                'sources': {
                    'documents': enhanced_results,
                    'web_search': web_results
                },
                'query_analysis': self._analyze_query_for_structure(query),
                'directory_matches': enhanced_results[:5],
                'debug_info': debug_info
            }
            logger.info("Query processed successfully")
            return result

        except Exception as e:
            logger.error("Error processing query", exc_info=True)
            return {
                'response': f"I'm sorry, I encountered an error while processing your query: {str(e)}",
                'sources': {},
                'query_analysis': {},
                'directory_matches': [],
                'debug_info': debug_info
            }

    # ---------- Normalization & abbreviation expansion ----------
    def _normalize_query(self, query: str) -> str:
        """Lowercase, expand abbreviations (using whole-word matching), normalize punctuation/spaces.
           Records expansions in self._last_expansions list as tuples (abbr, expansion)."""
        self._last_expansions = []
        if not query:
            return ""

        q = query.strip()
        q_lower = q.lower()

        # avoid expanding inside quoted exact phrases: temporarily mask them
        quoted_matches = re.findall(r'"([^"]+)"', q)
        mask_map = {}
        for i, qm in enumerate(quoted_matches):
            token = f"__QUOTE_MASK_{i}__"
            mask_map[token] = qm
            q_lower = q_lower.replace(qm.lower(), token)

        # expand abbreviations using word boundaries.
        # Longer keys should be expanded first to avoid partial expansion (sort by length desc).
        for abbr in sorted(self.abbrev_map.keys(), key=lambda x: -len(x)):
            expansion = self.abbrev_map[abbr]
            # pattern: word boundary before and after; handle punctuation near tokens
            pattern = r'(?<!\w)' + re.escape(abbr) + r'(?!\w)'
            new_q, count = re.subn(pattern, expansion, q_lower, flags=re.IGNORECASE)
            if count > 0:
                self._last_expansions.append((abbr, expansion))
                logger.debug(f"Expanded abbreviation in query: '{abbr}' -> '{expansion}' (count={count})")
                q_lower = new_q  # continue running expansions on updated string

        # restore quoted phrases
        for token, original in mask_map.items():
            q_lower = q_lower.replace(token, original.lower())

        # normalize punctuation/spaces and remove duplicate whitespace
        q_lower = re.sub(r'[,_\(\)\[\]\{\}]', ' ', q_lower)
        q_lower = re.sub(r'\s+', ' ', q_lower).strip()

        return q_lower

    def _analyze_query_for_structure(self, query: str) -> Dict[str, Any]:
        q = (query or "").lower()
        analysis = {'original': query, 'normalized': self._normalize_query(query), 'modules': [], 'semesters': [], 'numbers': [], 'extensions': [], 'quoted': [], 'expansions': list(self._last_expansions)}
        analysis['modules'] = re.findall(r'\bmod(?:ule)?\s*\.?(\d+)\b', q)
        analysis['semesters'] = re.findall(r'\b(\d+)(?:st|nd|rd|th)?\s*(?:sem|semester)\b', q)
        analysis['numbers'] = re.findall(r'\b\d+\b', q)
        analysis['extensions'] = re.findall(r'\.(pdf|pptx?|docx?|jpeg|jpg|png)\b', q)
        analysis['quoted'] = re.findall(r'"([^"]+)"', query or "")
        return analysis

    # ---------- Filesystem search (unchanged) ----------
    def _filesystem_search(self, query: str, max_results: int = 200) -> List[Dict[str, Any]]:
        logger.debug(f"Running filesystem search under {self.documents_root} for query: {query}")
        if not os.path.isdir(self.documents_root):
            logger.warning(f"documents_root does not exist or is not a directory: {self.documents_root}")
            return []
        normalized_query = self._normalize_query(query)
        tokens = [t for t in normalized_query.split() if t]
        quoted = re.findall(r'"([^"]+)"', query or "")
        results = []
        for root, dirs, files in os.walk(self.documents_root):
            rel_root = os.path.relpath(root, self.documents_root)
            for fname in files:
                try:
                    abs_path = os.path.abspath(os.path.join(root, fname))
                    rel_path = os.path.join(rel_root, fname).replace('\\', '/')
                    name_lower = fname.lower()
                    path_lower = rel_path.lower()
                    score = 0.0
                    reasons = []
                    for q in quoted:
                        if q.lower() in name_lower or q.lower() in path_lower:
                            score += 1.0
                            reasons.append(f'quoted match: "{q}"')
                    if normalized_query and (normalized_query in name_lower or normalized_query in path_lower):
                        score += 0.8
                        reasons.append('full query substring match')
                    for t in tokens:
                        if t in name_lower:
                            score += 0.25
                            reasons.append(f'token in filename: {t}')
                        if t in path_lower:
                            score += 0.12
                            reasons.append(f'token in path: {t}')
                    ext = os.path.splitext(fname)[1].lstrip('.').lower()
                    if ext and ext in tokens:
                        score += 0.08
                        reasons.append(f'extension match: {ext}')
                    if score > 0:
                        results.append({
                            'path': abs_path,
                            'name': fname,
                            'relative_path': rel_path,
                            'filesystem_score': float(score),
                            'match_reasons': list(dict.fromkeys(reasons))
                        })
                except Exception as e:
                    logger.debug(f"Skipping file in FS search due to error: {e}")
        results.sort(key=lambda x: x.get('filesystem_score', 0.0), reverse=True)
        logger.debug(f"Filesystem search found {len(results)} candidate files (returning top {max_results})")
        return results[:max_results]

    # ---------- Merge & ranking (same as prior debug-enabled version) ----------
    def _enhance_results_with_structure(self,
                                       doc_results: List[Dict[str, Any]],
                                       structure_results: List[Dict[str, Any]],
                                       normalized_query: str,
                                       fs_results: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        if fs_results is None:
            fs_results = []
        logger.debug("Merging vector, structure and filesystem results...")
        merged: Dict[str, Dict[str, Any]] = {}
        def _abs_path(fp_candidate: str) -> str:
            if not fp_candidate:
                return fp_candidate
            if os.path.isabs(fp_candidate):
                return os.path.abspath(fp_candidate)
            return os.path.abspath(os.path.join(self.documents_root, fp_candidate))
        for r in (doc_results or []):
            meta = r.get('metadata') or {}
            fp = meta.get('file_path') or meta.get('path') or meta.get('source') or ''
            fp_abs = _abs_path(fp) if fp else f"__vector__:{r.get('id','')}"
            merged.setdefault(fp_abs, {
                'file_path': fp_abs,
                'file_name': meta.get('file_name') or os.path.basename(fp_abs),
                'metadata': meta,
                'content': r.get('content') or r.get('text') or '',
                'vector_score': float(r.get('score', 0.0) or 0.0),
                'structure_score': 0.0,
                'filesystem_score': 0.0,
                'hierarchy_score': self._calculate_hierarchy_score(fp_abs),
                'match_reasons': list(set(meta.get('match_reasons', []) or [])),
                'source': 'vector_search'
            })
        for r in (structure_results or []):
            fp = r.get('path') or r.get('file_path') or r.get('file')
            fp_abs = _abs_path(fp) if fp else f"__structure__:{r.get('name','')}"
            entry = merged.get(fp_abs)
            if entry:
                entry['structure_score'] = max(entry.get('structure_score', 0.0), float(r.get('score', 0.0) or 0.0))
                entry['match_reasons'] = list(dict.fromkeys(entry.get('match_reasons', []) + (r.get('match_reasons') or [])))
                entry['source'] = 'combined'
            else:
                merged[fp_abs] = {
                    'file_path': fp_abs,
                    'file_name': r.get('name') or os.path.basename(fp_abs),
                    'metadata': r,
                    'content': r.get('excerpt') or '',
                    'vector_score': 0.0,
                    'structure_score': float(r.get('score', 0.0) or 0.0),
                    'filesystem_score': 0.0,
                    'hierarchy_score': self._calculate_hierarchy_score(fp_abs),
                    'match_reasons': r.get('match_reasons') or [],
                    'source': 'structure_search'
                }
        for r in (fs_results or []):
            fp_abs = os.path.abspath(r.get('path'))
            entry = merged.get(fp_abs)
            if entry:
                entry['filesystem_score'] = max(entry.get('filesystem_score', 0.0), float(r.get('filesystem_score', 0.0)))
                entry['match_reasons'] = list(dict.fromkeys(entry.get('match_reasons', []) + (r.get('match_reasons') or [])))
                entry['source'] = 'combined' if entry.get('source') != 'vector_search' else 'vector+fs'
            else:
                merged[fp_abs] = {
                    'file_path': fp_abs,
                    'file_name': r.get('name'),
                    'metadata': {'relative_path': r.get('relative_path')},
                    'content': '',
                    'vector_score': 0.0,
                    'structure_score': 0.0,
                    'filesystem_score': float(r.get('filesystem_score', 0.0)),
                    'hierarchy_score': self._calculate_hierarchy_score(fp_abs),
                    'match_reasons': r.get('match_reasons') or [],
                    'source': 'filesystem_search'
                }
        results_list = []
        query_tokens = set((normalized_query or "").split())
        for fp, e in merged.items():
            v = float(e.get('vector_score', 0.0))
            s = float(e.get('structure_score', 0.0))
            fscore = float(e.get('filesystem_score', 0.0))
            h = float(e.get('hierarchy_score', 0.0))
            exact_boost = 0.0
            try:
                name_lower = (e.get('file_name') or '').lower()
                path_lower = (e.get('file_path') or '').lower()
                for t in query_tokens:
                    if t and (t in name_lower):
                        exact_boost += 0.06
                    if t and (t in path_lower):
                        exact_boost += 0.03
                exact_boost = min(exact_boost, 0.4)
            except Exception:
                exact_boost = 0.0
            combined = (
                (self.vector_weight * v) +
                (self.structure_weight * s) +
                (self.hierarchy_weight * h) +
                (0.5 * fscore)
            ) + exact_boost
            e['final_score'] = combined
            e['computed'] = {'vector': v, 'structure': s, 'filesystem': fscore, 'hierarchy': h, 'exact_boost': exact_boost}
            e['match_reasons'] = e.get('match_reasons', [])
            results_list.append(e)
        results_list.sort(key=lambda x: x.get('final_score', 0.0), reverse=True)
        logger.debug(f"Total merged candidates: {len(results_list)}; top final scores: {[r.get('final_score') for r in results_list[:5]]}")
        return results_list

    def _calculate_hierarchy_score(self, file_path: str) -> float:
        if not file_path:
            return 0.0
        try:
            normalized = file_path.lower().replace('\\', '/')
            depth = max(0, normalized.count('/') - (self.documents_root.lower().count('/') if self.documents_root else 0))
            depth_score = min(depth * 0.1, 0.8)
            module_bonus = 0.5 if re.search(r'\bmod(?:ule)?\s*\.?\d+\b', normalized) or re.search(r'/mod\d+/', normalized) else 0.0
            subject_bonus = 0.4 if any(sub in normalized for sub in ['java', 'dbms', 'autometa', 'pai', 'smart', 'web', 'python', 'statistical', 'big_data', 'analytics']) else 0.0
            synthetic_penalty = -0.3 if file_path.startswith("__") else 0.0
            score = depth_score + module_bonus + subject_bonus + synthetic_penalty
            return max(0.0, min(score, 2.0))
        except Exception:
            return 0.0

    def _prepare_context(self, doc_results: List[Dict[str, Any]], web_results: List[Dict[str, Any]], chat_history: List[Dict[str, Any]] = None) -> str:
        parts = []
        if chat_history:
            parts.append("Conversation context:")
            for msg in chat_history[-4:]:
                parts.append(f"{msg.get('role','user').capitalize()}: {msg.get('content','')}")
            parts.append("")
        if doc_results:
            parts.append("Top relevant documents:")
            for i, doc in enumerate(doc_results[:5], start=1):
                parts.append(f"{i}. {doc.get('file_name')} (path: {doc.get('file_path')}) [score: {doc.get('final_score'):.4f}]")
                if doc.get('match_reasons'):
                    parts.append(f"   Reasons: {', '.join(doc.get('match_reasons'))}")
                snippet = (doc.get('content') or '')[:400]
                if snippet:
                    parts.append(f"   Snippet: {snippet}...")
                parts.append("")
        if web_results:
            parts.append("Web results:")
            for i, w in enumerate(web_results[:3], start=1):
                parts.append(f"{i}. {w.get('title','No title')} - {w.get('url','')}")
                parts.append((w.get('content') or '')[:300])
        return "\n".join(parts)

    def _debug_log_summary(self, structure_results, vector_results, fs_results, enhanced_results):
        if not self.debug:
            return
        try:
            logger.debug("=== DEBUG SUMMARY ===")
            logger.debug(f"Abbreviations (sample up to 20): {list(self.abbrev_map.items())[:20]}")
            logger.debug(f"Last expansions applied: {self._last_expansions}")
            logger.debug(f"Structure results: {len(structure_results) if structure_results is not None else 0}")
            if structure_results:
                for i, r in enumerate(structure_results[:5], start=1):
                    logger.debug(f"  S{i}: name={r.get('name')} path={r.get('path')} score={r.get('score')}")
            logger.debug(f"Vector results: {len(vector_results) if vector_results is not None else 0}")
            if vector_results:
                for i, r in enumerate(vector_results[:5], start=1):
                    meta = r.get('metadata') or {}
                    logger.debug(f"  V{i}: id={r.get('id','-')} file_path={meta.get('file_path')} score={r.get('score')}")
            logger.debug(f"Filesystem results: {len(fs_results) if fs_results is not None else 0}")
            if fs_results:
                for i, r in enumerate(fs_results[:5], start=1):
                    logger.debug(f"  F{i}: name={r.get('name')} rel={r.get('relative_path')} fscore={r.get('filesystem_score')} reasons={r.get('match_reasons')}")
            logger.debug(f"Enhanced top results: {len(enhanced_results)}")
            for i, r in enumerate(enhanced_results[:8], start=1):
                logger.debug(f"  E{i}: file={r.get('file_name')} path={r.get('file_path')} final={r.get('final_score'):.4f} computed={r.get('computed')} reasons={r.get('match_reasons')}")
            logger.debug("=== END DEBUG SUMMARY ===")
        except Exception as e:
            logger.debug(f"Error printing debug summary: {e}")

    # ---------- Remaining utility methods (unchanged) ----------
    def get_system_info(self) -> Dict[str, Any]:
        try:
            vector_db_info = self.vector_db.get_collection_info()
            web_search_status = {'enabled': getattr(self.web_search, 'enabled', False), 'providers': getattr(self.web_search, 'providers', [])}
            llm_info = {'provider': getattr(self.llm_provider, 'provider', 'unknown'), 'model': getattr(self.llm_provider, 'model', 'unknown')}
            return {'vector_database': vector_db_info, 'web_search': web_search_status, 'llm_provider': llm_info, 'status': 'operational'}
        except Exception as e:
            logger.error("Error getting system info", exc_info=True)
            return {'status': 'error', 'error': str(e)}

    def clear_documents(self) -> Dict[str, Any]:
        try:
            success = self.vector_db.clear_collection()
            if success:
                return {'success': True, 'message': 'All documents cleared from vector database'}
            else:
                return {'success': False, 'message': 'Failed to clear documents from vector database'}
        except Exception as e:
            logger.error("Error clearing documents", exc_info=True)
            return {'success': False, 'message': f'Error clearing documents: {e}'}

    def process_single_file(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info(f"Processing single file: {file_path}")
            processed_chunks = self.document_processor.process_single_file(file_path)
            if not processed_chunks:
                return {'success': False, 'message': f'No content extracted from {file_path}', 'chunks_processed': 0}
            success = self.vector_db.add_documents(processed_chunks)
            if success:
                return {'success': True, 'message': f'Successfully processed {len(processed_chunks)} chunks from {file_path}', 'chunks_processed': len(processed_chunks)}
            else:
                return {'success': False, 'message': f'Failed to add documents from {file_path} to vector database', 'chunks_processed': 0}
        except Exception as e:
            logger.error("Error processing single file", exc_info=True)
            return {'success': False, 'message': f'Error processing file {file_path}: {e}', 'chunks_processed': 0}

    def get_available_documents(self) -> List[Dict[str, Any]]:
        try:
            structure = getattr(self.document_structure, 'structure', {}) or {}
            documents = []
            for doc_path, doc_info in structure.get('documents', {}).items():
                documents.append({
                    'file_path': doc_info.get('path', ''),
                    'file_name': doc_info.get('name', ''),
                    'file_type': doc_info.get('type', ''),
                    'file_size': doc_info.get('size', 0),
                    'exists': os.path.exists(doc_info.get('path', '')),
                    'relative_path': doc_info.get('relative_path', ''),
                    'directory': doc_info.get('directory', ''),
                    'keywords': doc_info.get('keywords', [])
                })
            return documents
        except Exception as e:
            logger.error("Error getting available documents", exc_info=True)
            return []

    def get_document_by_path(self, file_path: str) -> Optional[Dict[str, Any]]:
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File does not exist: {file_path}")
                return None
            file_stat = os.stat(file_path)
            return {'file_path': file_path, 'file_name': os.path.basename(file_path), 'file_type': os.path.splitext(file_path)[1].lower(), 'file_size': file_stat.st_size, 'last_modified': file_stat.st_mtime, 'exists': True}
        except Exception as e:
            logger.error("Error getting document by path", exc_info=True)
            return None

    def search_documents_for_download(self, query: str, llm_rerank: bool = True, max_results: int = 50) -> List[Dict[str, Any]]:
        try:
            normalized_query = self._normalize_query(query)
            structure_results = self.document_structure.search_documents(normalized_query) or []
            vector_results = self.vector_db.search(normalized_query, n_results=max_results) or []
            fs_results = self._filesystem_search(query, max_results=max_results)
            norm_structure = []
            for r in structure_results:
                file_path = r.get('path') or r.get('file_path') or ''
                norm_structure.append({
                    'file_path': file_path,
                    'file_name': r.get('name') or os.path.basename(file_path),
                    'file_type': r.get('type') or os.path.splitext(file_path)[1].lstrip('.'),
                    'file_size': r.get('size', 0),
                    'exists': os.path.exists(file_path) if file_path else False,
                    'relative_path': r.get('relative_path', ''),
                    'directory': r.get('directory', ''),
                    'keywords': r.get('keywords', []),
                    'score': float(r.get('score', 0)),
                    'match_reasons': r.get('match_reasons', [])
                })
            norm_vector = []
            for res in vector_results:
                meta = res.get('metadata', {}) or {}
                fp = meta.get('file_path') or meta.get('path') or ''
                size = 0
                if fp and os.path.exists(fp):
                    try:
                        size = os.path.getsize(fp)
                    except Exception:
                        size = 0
                norm_vector.append({
                    'file_path': fp,
                    'file_name': meta.get('file_name') or os.path.basename(fp),
                    'file_type': meta.get('file_type') or os.path.splitext(fp)[1].lstrip('.'),
                    'file_size': size,
                    'exists': os.path.exists(fp),
                    'relative_path': meta.get('relative_path', ''),
                    'directory': meta.get('directory', ''),
                    'keywords': meta.get('keywords', []),
                    'score': float(res.get('score', 0)),
                    'match_reasons': meta.get('match_reasons', [])
                })
            merged: Dict[str, Dict[str, Any]] = {}
            for doc in (norm_structure + norm_vector):
                fp = doc.get('file_path') or f"__unknown__:{doc.get('file_name')}"
                if fp in merged:
                    merged[fp]['score'] = max(merged[fp].get('score', 0), doc.get('score', 0))
                    merged[fp]['match_reasons'] = list(set(merged[fp].get('match_reasons', []) + doc.get('match_reasons', [])))
                else:
                    merged[fp] = doc.copy()
            for f in fs_results:
                fp = f.get('path')
                if not fp:
                    continue
                if fp in merged:
                    merged[fp]['score'] = max(merged[fp].get('score', 0), f.get('filesystem_score', 0))
                    merged[fp]['match_reasons'] = list(set(merged[fp].get('match_reasons', []) + f.get('match_reasons', [])))
                else:
                    merged[fp] = {
                        'file_path': fp,
                        'file_name': f.get('name'),
                        'file_type': os.path.splitext(f.get('name'))[1].lstrip('.'),
                        'file_size': os.path.getsize(fp) if os.path.exists(fp) else 0,
                        'exists': os.path.exists(fp),
                        'relative_path': f.get('relative_path', ''),
                        'directory': os.path.dirname(fp),
                        'keywords': [],
                        'score': float(f.get('filesystem_score', 0)),
                        'match_reasons': f.get('match_reasons', [])
                    }
            docs_list = list(merged.values())
            # Optional LLM rerank (same logic as prior)
            if llm_rerank and getattr(self.llm_provider, 'generate_response', None):
                try:
                    prompt_lines = [
                        "You are given a user query and a list of candidate documents (file path and short metadata).",
                        "Return a JSON object mapping each file_path to a relevance score between 0.0 (irrelevant) and 1.0 (very relevant).",
                        "Only return valid JSON. Do not include any extra commentary.",
                        "",
                        f"User query: {query}",
                        "",
                        "Candidates:"
                    ]
                    for d in docs_list[:60]:
                        prompt_lines.append(json.dumps({
                            'file_path': d.get('file_path'),
                            'file_name': d.get('file_name'),
                            'file_size': d.get('file_size'),
                            'score': d.get('score', 0),
                            'match_reasons': d.get('match_reasons', [])
                        }))
                    prompt_text = "\n".join(prompt_lines)
                    llm_resp = self.llm_provider.generate_response(prompt_text, query=None)
                    json_text = llm_resp.strip()
                    m = re.search(r'(\{[\s\S]*\})', json_text)
                    if m:
                        json_text = m.group(1)
                    score_map = {}
                    try:
                        score_map = json.loads(json_text)
                    except Exception:
                        try:
                            score_map = ast.literal_eval(json_text)
                        except Exception:
                            score_map = {}
                    if isinstance(score_map, dict) and score_map:
                        for d in docs_list:
                            d['llm_score'] = float(score_map.get(d.get('file_path'), 0.0))
                        docs_list.sort(key=lambda x: (x.get('llm_score', 0.0), x.get('score', 0.0)), reverse=True)
                        return docs_list[:max_results]
                except Exception as e:
                    logger.error("LLM re-ranking failed", exc_info=True)
            docs_list.sort(key=lambda x: x.get('score', 0.0), reverse=True)
            return docs_list[:max_results]
        except Exception as e:
            logger.error("Error in search_documents_for_download", exc_info=True)
            return []

    def get_document_content(self, file_path: str) -> Optional[bytes]:
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File does not exist: {file_path}")
                return None
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error("Error reading document content", exc_info=True)
            return None
