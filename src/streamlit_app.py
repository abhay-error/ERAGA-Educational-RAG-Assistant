# # import streamlit as st
# # import os
# # import sys
# # import logging
# # from typing import List, Dict, Any
# # import json
# # from datetime import datetime
# # import tempfile
# # import shutil

# # # Handle imports for both direct execution and package imports
# # try:
# #     from .rag_pipeline import RAGPipeline
# #     from .config import config
# # except ImportError:
# #     # Add the src directory to the path for direct execution
# #     current_dir = os.path.dirname(os.path.abspath(__file__))
# #     parent_dir = os.path.dirname(current_dir)
    
# #     # Add both src and parent directory to path
# #     if current_dir not in sys.path:
# #         sys.path.insert(0, current_dir)
# #     if parent_dir not in sys.path:
# #         sys.path.insert(0, parent_dir)
    
# #     try:
# #         from rag_pipeline import RAGPipeline
# #         from config import config
# #     except ImportError:
# #         from src.rag_pipeline import RAGPipeline
# #         from src.config import config

# # # Configure logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # class StreamlitApp:
# #     def __init__(self):
# #         self.config = config
# #         self._rag_pipeline = None  # Lazy loading
        
# #         # Initialize session state
# #         if 'chat_history' not in st.session_state:
# #             st.session_state.chat_history = []
        
# #         if 'web_search_enabled' not in st.session_state:
# #             st.session_state.web_search_enabled = True
        
# #         if 'system_info' not in st.session_state:
# #             st.session_state.system_info = None
    
# #     @property
# #     def rag_pipeline(self):
# #         """Lazy load the RAG pipeline."""
# #         if self._rag_pipeline is None:
# #             try:
# #                 self._rag_pipeline = RAGPipeline()
# #             except Exception as e:
# #                 st.error(f"Failed to initialize RAG pipeline: {e}")
# #                 return None
# #         return self._rag_pipeline
    
# #     def run(self):
# #         """Run the Streamlit application."""
# #         st.set_page_config(
# #             page_title="College RAG Assistant",
# #             page_icon="🎓",
# #             layout="wide",
# #             initial_sidebar_state="expanded"
# #         )
        
# #         # Custom CSS for modern chat interface with fixed bottom input
# #         st.markdown("""
# #         <style>
# #         /* Modern Chat Interface Styles */
# #         .main-header {
# #             font-size: 2.5rem;
# #             font-weight: bold;
# #             color: #1f77b4;
# #             text-align: center;
# #             margin-bottom: 2rem;
# #         }
        
# #         /* Chat container */
# #         .chat-container {
# #             background-color: #f8f9fa;
# #             border-radius: 15px;
# #             padding: 20px;
# #             margin: 20px 0;
# #             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
# #             height: calc(100vh - 300px);
# #             overflow-y: auto;
# #         }
        
# #         /* Message bubbles */
# #         .message-bubble {
# #             margin: 10px 0;
# #             padding: 15px 20px;
# #             border-radius: 20px;
# #             max-width: 80%;
# #             word-wrap: break-word;
# #             position: relative;
# #         }
        
# #         .user-message {
# #             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #             color: white;
# #             margin-left: auto;
# #             margin-right: 0;
# #             border-bottom-right-radius: 5px;
# #         }
        
# #         .assistant-message {
# #             background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
# #             color: white;
# #             margin-right: auto;
# #             margin-left: 0;
# #             border-bottom-left-radius: 5px;
# #         }
        
# #         /* Message timestamp */
# #         .message-timestamp {
# #             font-size: 0.7rem;
# #             opacity: 0.7;
# #             margin-top: 5px;
# #         }
        
# #         /* Source info */
# #         .source-info {
# #             font-size: 0.8rem;
# #             color: #666;
# #             margin-top: 10px;
# #             padding: 10px;
# #             background-color: rgba(255, 255, 255, 0.9);
# #             border-radius: 10px;
# #             border-left: 4px solid #007bff;
# #         }
        
# #         /* Fixed bottom input area */
# #         .fixed-bottom-input {
# #             position: fixed;
# #             bottom: 0;
# #             left: 0;
# #             right: 0;
# #             background: white;
# #             border-top: 1px solid #e0e0e0;
# #             padding: 20px;
# #             box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
# #             z-index: 1000;
# #         }
        
# #         .input-container {
# #             max-width: 1200px;
# #             margin: 0 auto;
# #             display: flex;
# #             align-items: center;
# #             gap: 10px;
# #         }
        
# #         .input-field {
# #             flex: 1;
# #             border: 2px solid #e0e0e0;
# #             border-radius: 25px;
# #             padding: 15px 20px;
# #             font-size: 16px;
# #             outline: none;
# #             transition: border-color 0.3s;
# #         }
        
# #         .input-field:focus {
# #             border-color: #667eea;
# #         }
        
# #         .send-button {
# #             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #             color: white;
# #             border: none;
# #             border-radius: 50%;
# #             width: 50px;
# #             height: 50px;
# #             display: flex;
# #             align-items: center;
# #             justify-content: center;
# #             cursor: pointer;
# #             transition: transform 0.2s;
# #             font-size: 20px;
# #         }
        
# #         .send-button:hover {
# #             transform: scale(1.1);
# #         }
        
# #         /* Sidebar styling */
# #         .sidebar .sidebar-content {
# #             background-color: #f8f9fa;
# #         }
        
# #         /* Document cards */
# #         .document-card {
# #             background: white;
# #             border-radius: 10px;
# #             padding: 15px;
# #             margin: 10px 0;
# #             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
# #             border-left: 4px solid #007bff;
# #         }
        
# #         /* Buttons */
# #         .stButton > button {
# #             border-radius: 25px;
# #             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #             color: white;
# #             border: none;
# #             padding: 10px 25px;
# #             font-weight: bold;
# #         }
        
# #         .stButton > button:hover {
# #             background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
# #             transform: translateY(-2px);
# #             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
# #         }
        
# #         /* Hide Streamlit default elements */
# #         #MainMenu {visibility: hidden;}
# #         footer {visibility: hidden;}
# #         header {visibility: hidden;}
        
# #         /* Add margin bottom to prevent content from being hidden behind fixed input */
# #         .main .block-container {
# #             padding-bottom: 100px;
# #         }
# #         </style>
# #         """, unsafe_allow_html=True)
        
# #         # Header
# #         st.markdown('<h1 class="main-header">🎓 College RAG Assistant</h1>', unsafe_allow_html=True)
# #         st.markdown("**School of Engineering, University of Mysore**")
        
# #         # Sidebar
# #         self._render_sidebar()
        
# #         # Main chat interface
# #         self._render_chat_interface()
        
# #         # Fixed bottom input
# #         self._render_fixed_bottom_input()
    
# #     def _render_sidebar(self):
# #         """Render the sidebar with system information and controls."""
# #         with st.sidebar:
# #             st.header("🔧 System Controls")
            
# #             # Check if RAG pipeline is available
# #             if self.rag_pipeline is None:
# #                 st.error("❌ RAG Pipeline not available")
# #                 st.info("Please check the logs for more information.")
# #                 return
            
# #             # System info
# #             if st.button("🔄 Refresh System Info"):
# #                 try:
# #                     st.session_state.system_info = self.rag_pipeline.get_system_info()
# #                 except Exception as e:
# #                     st.error(f"Failed to get system info: {e}")
            
# #             if st.session_state.system_info:
# #                 st.subheader("System Status")
# #                 info = st.session_state.system_info
                
# #                 if info.get('status') == 'operational':
# #                     st.success("✅ System Operational")
# #                 else:
# #                     st.error("❌ System Error")
                
# #                 # Vector DB info
# #                 if 'vector_database' in info:
# #                     vdb_info = info['vector_database']
# #                     st.write(f"**Documents in DB:** {vdb_info.get('total_documents', 0)}")
# #                     st.write(f"**Model:** {vdb_info.get('embedding_model', 'N/A')}")
                
# #                 # LLM info
# #                 if 'llm_provider' in info:
# #                     llm_info = info['llm_provider']
# #                     st.write(f"**LLM Provider:** {llm_info.get('provider', 'N/A')}")
# #                     st.write(f"**Model:** {llm_info.get('model', 'N/A')}")
                
# #                 # Web search info
# #                 if 'web_search' in info:
# #                     web_info = info['web_search']
# #                     status = "✅ Enabled" if web_info.get('enabled') else "❌ Disabled"
# #                     st.write(f"**Web Search:** {status}")
            
# #             st.divider()
            
# #             # Document Search Section
# #             st.subheader("📄 Document Search")
            
# #             # Search for documents
# #             search_query = st.text_input(
# #                 "Search documents:",
# #                 placeholder="e.g., python module 1, notes, syllabus",
# #                 help="Search for documents by keywords, filename, or content"
# #             )
            
# #             if search_query and st.button("🔍 Search Documents"):
# #                 with st.spinner("Searching documents..."):
# #                     documents = self.rag_pipeline.search_documents_for_download(search_query)
# #                     if documents:
# #                         st.success(f"Found {len(documents)} document(s)")
# #                         self._render_document_results(documents)
# #                     else:
# #                         st.warning("No documents found matching your search.")
            
# #             # Show all documents
# #             if st.button("📚 Show All Documents"):
# #                 with st.spinner("Loading documents..."):
# #                     documents = self.rag_pipeline.get_available_documents()
# #                     if documents:
# #                         st.success(f"Found {len(documents)} document(s) in the database")
# #                         self._render_document_results(documents)
# #                     else:
# #                         st.warning("No documents found in the database.")
            
# #             st.divider()
            
# #             # Document management
# #             st.subheader("📄 Document Management")
            
# #             if st.button("📥 Ingest Documents"):
# #                 with st.spinner("Ingesting documents..."):
# #                     result = self.rag_pipeline.ingest_documents()
# #                     if result['success']:
# #                         st.success(f"✅ {result['message']}")
# #                     else:
# #                         st.error(f"❌ {result['message']}")
            
# #             if st.button("🗑️ Clear All Documents"):
# #                 if st.checkbox("Confirm deletion"):
# #                     with st.spinner("Clearing documents..."):
# #                         result = self.rag_pipeline.clear_documents()
# #                         if result['success']:
# #                             st.success("✅ Documents cleared")
# #                         else:
# #                             st.error(f"❌ {result['message']}")
            
# #             st.divider()
            
# #             # File upload
# #             st.subheader("📤 Upload Files")
# #             uploaded_files = st.file_uploader(
# #                 "Choose files to upload",
# #                 type=['pdf', 'docx', 'pptx', 'txt', 'md', 'csv', 'xlsx'],
# #                 accept_multiple_files=True
# #             )
            
# #             if uploaded_files:
# #                 if st.button("Process Uploaded Files"):
# #                     self._process_uploaded_files(uploaded_files)
    
# #     def _render_document_results(self, documents: List[Dict[str, Any]]):
# #         """Render document search results in the sidebar."""
# #         if not documents:
# #             return
        
# #         st.subheader("📄 Search Results")
        
# #         # Group documents by directory
# #         documents_by_dir = {}
# #         for doc in documents:
# #             directory = doc.get('directory', 'Unknown')
# #             if directory not in documents_by_dir:
# #                 documents_by_dir[directory] = []
# #             documents_by_dir[directory].append(doc)
        
# #         # Display documents organized by directory
# #         for directory, docs in documents_by_dir.items():
# #             if directory != 'Unknown':
# #                 st.markdown(f"**📁 {directory}:**")
# #             else:
# #                 st.markdown(f"**📁 Other Documents:**")
            
# #             for doc in docs[:3]:  # Show top 3 per directory
# #                 with st.expander(f"📄 {doc.get('file_name', 'Unknown')}"):
# #                     # Document info
# #                     file_name = doc.get('file_name', 'Unknown')
# #                     file_type = doc.get('file_type', '').upper()
# #                     file_size = doc.get('file_size', 0)
# #                     exists = doc.get('exists', False)
# #                     relative_path = doc.get('relative_path', '')
# #                     directory = doc.get('directory', '')
# #                     score = doc.get('score', 0)
                    
# #                     # Format file size
# #                     if file_size > 0:
# #                         if file_size < 1024:
# #                             size_str = f"{file_size} B"
# #                         elif file_size < 1024 * 1024:
# #                             size_str = f"{file_size / 1024:.1f} KB"
# #                         else:
# #                             size_str = f"{file_size / (1024 * 1024):.1f} MB"
# #                     else:
# #                         size_str = "Unknown"
                    
# #                     # Status indicator
# #                     status = "✅ Available" if exists else "❌ File not found"
                    
# #                     st.write(f"**File:** {file_name}")
# #                     st.write(f"**Type:** {file_type}")
# #                     st.write(f"**Size:** {size_str}")
# #                     st.write(f"**Status:** {status}")
# #                     st.write(f"**Score:** ⭐{score}")
# #                     st.write(f"**Path:** `{relative_path}`")
# #                     if directory:
# #                         st.write(f"**Directory:** `{directory}`")
                    
# #                     # Download button
# #                     if exists:
# #                         self._create_download_button(doc)
    
# #     def _render_chat_interface(self):
# #         """Render the main chat interface."""
# #         st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
# #         # Check if RAG pipeline is available
# #         if self.rag_pipeline is None:
# #             st.error("❌ RAG Pipeline not available")
# #             st.info("Please check the logs for more information.")
# #             return
        
# #         # Web search toggle
# #         col1, col2 = st.columns([1, 3])
# #         with col1:
# #             web_search_enabled = st.checkbox(
# #                 "🔍 Web Search",
# #                 value=st.session_state.web_search_enabled,
# #                 help="Enable web search for additional context"
# #             )
# #             st.session_state.web_search_enabled = web_search_enabled
        
# #         # Chat history
# #         if st.session_state.chat_history:
# #             st.subheader("💬 Chat History")
# #             for message in st.session_state.chat_history:
# #                 self._render_message(message)
        
# #         st.markdown('</div>', unsafe_allow_html=True)
    
# #     def _render_fixed_bottom_input(self):
# #         """Render the fixed bottom input area like ChatGPT."""
# #         # Create a container for the fixed bottom input
# #         with st.container():
# #             st.markdown("""
# #             <div style="position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #e0e0e0; padding: 20px; box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1); z-index: 1000;">
# #                 <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 10px;">
# #                     <input type="text" id="chat-input" style="flex: 1; border: 2px solid #e0e0e0; border-radius: 25px; padding: 15px 20px; font-size: 16px; outline: none;" placeholder="Ask a question...">
# #                     <button onclick="sendMessage()" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 20px;">🚀</button>
# #                 </div>
# #             </div>
# #             """, unsafe_allow_html=True)
        
# #         # Add JavaScript for handling the input
# #         st.markdown("""
# #         <script>
# #         function sendMessage() {
# #             const input = document.getElementById('chat-input');
# #             const message = input.value.trim();
# #             if (message) {
# #                 // Create a custom event to send the message to Streamlit
# #                 const event = new CustomEvent('streamlit:sendMessage', { detail: message });
# #                 window.dispatchEvent(event);
# #                 input.value = '';
# #             }
# #         }
        
# #         // Handle Enter key
# #         document.addEventListener('DOMContentLoaded', function() {
# #             const input = document.getElementById('chat-input');
# #             if (input) {
# #                 input.addEventListener('keypress', function(e) {
# #                     if (e.key === 'Enter') {
# #                         sendMessage();
# #                     }
# #                 });
# #             }
# #         });
# #         </script>
# #         """, unsafe_allow_html=True)
        
# #         # Alternative: Use Streamlit's native input with better styling
# #         st.markdown("---")
        
# #         # Create a more prominent input area
# #         with st.container():
# #             col1, col2 = st.columns([6, 1])
# #             with col1:
# #                 query = st.text_input(
# #                     "Ask a question:",
# #                     placeholder="e.g., What topics are covered in Module 1 of Python programming?",
# #                     key="chat_input",
# #                     label_visibility="collapsed"
# #                 )
            
# #             with col2:
# #                 st.markdown("<br>", unsafe_allow_html=True)
# #                 if st.button("🚀", type="primary", use_container_width=True):
# #                     if query.strip():
# #                         self._process_query(query.strip())
# #                     else:
# #                         st.warning("Please enter a question.")
        
# #         # Clear chat button
# #         if st.session_state.chat_history:
# #             if st.button("🗑️ Clear Chat"):
# #                 st.session_state.chat_history = []
# #                 st.rerun()
    
# #     def _render_message(self, message: Dict[str, Any]):
# #         """Render a single chat message with modern styling."""
# #         if message['role'] == 'user':
# #             st.markdown(f"""
# #             <div class="message-bubble user-message">
# #                 <strong>You:</strong><br>
# #                 {message['content']}
# #                 <div class="message-timestamp">{message.get('timestamp', '')}</div>
# #             </div>
# #             """, unsafe_allow_html=True)
# #         else:
# #             st.markdown(f"""
# #             <div class="message-bubble assistant-message">
# #                 <strong>Assistant:</strong><br>
# #                 {message['content']}
# #                 <div class="message-timestamp">{message.get('timestamp', '')}</div>
# #             </div>
# #             """, unsafe_allow_html=True)
            
# #             # Show sources if available
# #             sources = message.get('sources', {})
# #             if sources:
# #                 source_info = []
                
# #                 if sources.get('documents'):
# #                     doc_count = len(sources['documents'])
# #                     source_info.append(f"📄 {doc_count} document(s) retrieved")
                
# #                 if sources.get('web_search'):
# #                     web_count = len(sources['web_search'])
# #                     source_info.append(f"🌐 {web_count} web result(s) found")
                
# #                 if source_info:
# #                     st.markdown(f"""
# #                     <div class="source-info">
# #                         <strong>Sources:</strong> {' | '.join(source_info)}
# #                     </div>
# #                     """, unsafe_allow_html=True)
            
# #             # Show directory structure matches if available
# #             directory_matches = message.get('directory_matches', [])
# #             if directory_matches:
# #                 st.markdown("**📁 Directory Structure Matches:**")
# #                 for match in directory_matches[:2]:  # Show top 2 matches
# #                     file_name = match.get('name', 'Unknown')
# #                     relative_path = match.get('relative_path', '')
# #                     match_reasons = match.get('match_reasons', [])
                    
# #                     match_info = f"• **{file_name}** (`{relative_path}`)"
# #                     if match_reasons:
# #                         match_info += f" - {', '.join(match_reasons)}"
                    
# #                     st.markdown(match_info)
            
# #             # Show query analysis if available
# #             query_analysis = message.get('query_analysis', {})
# #             if query_analysis:
# #                 analysis_parts = []
# #                 if query_analysis.get('module_numbers'):
# #                     analysis_parts.append(f"Module(s): {', '.join(query_analysis['module_numbers'])}")
# #                 if query_analysis.get('subjects'):
# #                     analysis_parts.append(f"Subject(s): {', '.join(query_analysis['subjects'])}")
# #                 if query_analysis.get('file_types'):
# #                     analysis_parts.append(f"File type(s): {', '.join(query_analysis['file_types'])}")
                
# #                 if analysis_parts:
# #                     st.markdown(f"**🔍 Query Analysis:** {', '.join(analysis_parts)}")
    
# #     def _process_query(self, query: str):
# #         """Process a user query and add to chat history with context awareness."""
# #         # Check if RAG pipeline is available
# #         if self.rag_pipeline is None:
# #             st.error("❌ RAG Pipeline not available")
# #             return
        
# #         # Add user message to history
# #         st.session_state.chat_history.append({
# #             'role': 'user',
# #             'content': query,
# #             'timestamp': datetime.now().isoformat()
# #         })
        
# #         # Check if user is asking for notes
# #         is_notes_request = self._is_notes_request(query)
        
# #         # Get recent chat history for context (last 6 messages)
# #         chat_history = st.session_state.chat_history[-6:] if len(st.session_state.chat_history) > 6 else st.session_state.chat_history
        
# #         # Process query with context
# #         with st.spinner("Processing your question..."):
# #             try:
# #                 result = self.rag_pipeline.process_query(
# #                     query=query,
# #                     use_web_search=st.session_state.web_search_enabled,
# #                     max_docs=getattr(st.session_state, 'max_docs', 5),
# #                     chat_history=chat_history
# #                 )
# #             except Exception as e:
# #                 st.error(f"Error processing query: {e}")
# #                 result = {
# #                     'response': f"I'm sorry, I encountered an error while processing your query: {str(e)}",
# #                     'sources': {},
# #                     'query_analysis': {},
# #                     'directory_matches': []
# #                 }
        
# #         # Handle notes requests specifically
# #         if is_notes_request:
# #             result = self._handle_notes_request(query, result)
        
# #         # Handle directory structure matches
# #         directory_matches = result.get('directory_matches', [])
# #         if directory_matches:
# #             result['response'] += "\n\n📁 **Directory Structure Matches:**\n"
# #             result['response'] += f"I found {len(directory_matches)} document(s) that match your request based on directory structure:\n\n"
            
# #             for i, match in enumerate(directory_matches[:3], 1):  # Show top 3 matches
# #                 file_name = match.get('name', 'Unknown')
# #                 relative_path = match.get('relative_path', '')
# #                 match_reasons = match.get('match_reasons', [])
# #                 relevance_score = match.get('score', 0)
                
# #                 result['response'] += f"{i}. **{file_name}**\n"
# #                 result['response'] += f"   📂 Path: `{relative_path}`\n"
# #                 if match_reasons:
# #                     result['response'] += f"   🎯 Matches: {', '.join(match_reasons)}\n"
# #                 result['response'] += f"   ⭐ Relevance: {relevance_score}/10\n\n"
        
# #         # Add assistant response to history
# #         st.session_state.chat_history.append({
# #             'role': 'assistant',
# #             'content': result['response'],
# #             'sources': result.get('sources', {}),
# #             'query_analysis': result.get('query_analysis', {}),
# #             'directory_matches': result.get('directory_matches', []),
# #             'timestamp': datetime.now().isoformat()
# #         })
        
# #         # Rerun to update the interface
# #         st.rerun()
    
# #     def _is_notes_request(self, query: str) -> bool:
# #         """Check if the query is asking for notes."""
# #         notes_keywords = [
# #             'notes', 'note', 'lecture', 'material', 'content', 'syllabus', 'module',
# #             'chapter', 'topic', 'subject', 'course', 'study', 'learning'
# #         ]
        
# #         query_lower = query.lower()
# #         return any(keyword in query_lower for keyword in notes_keywords)
    
# #     def _handle_notes_request(self, query: str, result: Dict[str, Any]) -> Dict[str, Any]:
# #         """Handle notes requests by searching the document structure."""
# #         try:
# #             # Search for relevant documents using the document structure
# #             documents = self.rag_pipeline.search_documents_for_download(query)
            
# #             if documents:
# #                 # Use LLM to understand and organize the results
# #                 context = self._prepare_notes_context(documents, query)
                
# #                 # Generate a more comprehensive response using the LLM
# #                 enhanced_response = self.rag_pipeline.llm_provider.generate_response(
# #                     context=context,
# #                     query=f"Based on the following documents, provide a comprehensive answer about {query}. Organize the information clearly and provide relevant document references. If there are multiple documents, categorize them by topic or module."
# #                 )
                
# #                 result['response'] = enhanced_response
# #                 result['response'] += "\n\n📄 **Relevant Documents Found:**\n"
# #                 result['response'] += f"I found {len(documents)} document(s) that might be relevant to your request:\n\n"
                
# #                 # Group documents by directory for better organization
# #                 documents_by_dir = {}
# #                 for doc in documents:
# #                     directory = doc.get('directory', 'Unknown')
# #                     if directory not in documents_by_dir:
# #                         documents_by_dir[directory] = []
# #                     documents_by_dir[directory].append(doc)
                
# #                 # Display documents organized by directory
# #                 for directory, docs in documents_by_dir.items():
# #                     if directory != 'Unknown':
# #                         result['response'] += f"📁 **{directory}:**\n"
# #                     else:
# #                         result['response'] += f"📁 **Other Documents:**\n"
                    
# #                     for i, doc in enumerate(docs[:3], 1):  # Show top 3 per directory
# #                         file_name = doc.get('file_name', 'Unknown')
# #                         file_type = doc.get('file_type', '').upper()
# #                         exists = doc.get('exists', False)
# #                         status = "✅ Available" if exists else "❌ File not found"
# #                         relative_path = doc.get('relative_path', '')
# #                         score = doc.get('score', 0)
                        
# #                         result['response'] += f"  {i}. **{file_name}** ({file_type}) - {status} ⭐{score}\n"
# #                         result['response'] += f"     📂 Path: `{relative_path}`\n"
                    
# #                     result['response'] += "\n"
                
# #                 result['response'] += "\n💡 **To download these documents:**\n"
# #                 result['response'] += "1. Go to the 'Document Search' section in the sidebar\n"
# #                 result['response'] += "2. Search for the documents you want\n"
# #                 result['response'] += "3. Click the download button next to each document\n"
                
# #                 # Add quick access links
# #                 result['response'] += "\n🔍 **Quick Search Suggestions:**\n"
# #                 unique_keywords = set()
# #                 for doc in documents:
# #                     keywords = doc.get('keywords', [])
# #                     unique_keywords.update(keywords)
                
# #                 if unique_keywords:
# #                     result['response'] += "Try searching for: " + ", ".join(list(unique_keywords)[:5]) + "\n"
# #             else:
# #                 result['response'] += "\n📄 **Document Search:**\n"
# #                 result['response'] += "I couldn't find specific documents matching your request. "
# #                 result['response'] += "You can search for documents in the 'Document Search' section in the sidebar.\n\n"
                
# #                 # Provide suggestions based on available documents
# #                 all_docs = self.rag_pipeline.get_available_documents()
# #                 if all_docs:
# #                     result['response'] += "💡 **Available Document Categories:**\n"
# #                     categories = set()
# #                     for doc in all_docs:
# #                         directory = doc.get('directory', '')
# #                         if directory:
# #                             categories.add(directory.split('/')[0] if '/' in directory else directory)
                    
# #                     for category in list(categories)[:5]:
# #                         result['response'] += f"- {category}\n"
        
# #         except Exception as e:
# #             logger.error(f"Error handling notes request: {e}")
# #             result['response'] += f"\n\n❌ Error searching for documents: {str(e)}"
        
# #         return result
    
# #     def _prepare_notes_context(self, documents: List[Dict[str, Any]], query: str) -> str:
# #         """Prepare context for notes requests."""
# #         context_parts = []
# #         context_parts.append(f"User is asking about: {query}")
# #         context_parts.append("\nRelevant documents found:")
        
# #         for i, doc in enumerate(documents[:5], 1):
# #             file_name = doc.get('file_name', 'Unknown')
# #             relative_path = doc.get('relative_path', '')
# #             directory = doc.get('directory', '')
# #             keywords = doc.get('keywords', [])
            
# #             context_parts.append(f"\nDocument {i}: {file_name}")
# #             context_parts.append(f"Path: {relative_path}")
# #             if directory:
# #                 context_parts.append(f"Directory: {directory}")
# #             if keywords:
# #                 context_parts.append(f"Keywords: {', '.join(keywords)}")
        
# #         return "\n".join(context_parts)
    
# #     def _create_download_button(self, doc: Dict[str, Any]):
# #         """Create a download button for a document."""
# #         try:
# #             file_path = doc['file_path']
# #             file_name = doc.get('file_name', 'Unknown')
# #             file_type = doc.get('file_type', '').lower()
            
# #             # Get document content
# #             content = self.rag_pipeline.get_document_content(file_path)
            
# #             if content is None:
# #                 st.write("❌ Error reading file")
# #                 return
            
# #             # Determine MIME type
# #             mime_types = {
# #                 '.pdf': 'application/pdf',
# #                 '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
# #                 '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
# #                 '.txt': 'text/plain',
# #                 '.md': 'text/markdown',
# #                 '.csv': 'text/csv',
# #                 '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# #             }
            
# #             mime_type = mime_types.get(file_type, 'application/octet-stream')
            
# #             # Create download button
# #             st.download_button(
# #                 label="📥 Download",
# #                 data=content,
# #                 file_name=file_name,
# #                 mime=mime_type,
# #                 key=f"download_{file_path.replace('/', '_').replace('\\', '_')}"
# #             )
            
# #         except Exception as e:
# #             st.write(f"❌ Error: {str(e)}")
    
# #     def _process_uploaded_files(self, uploaded_files):
# #         """Process uploaded files."""
# #         documents_path = self.config.get_paths().get('documents', './data/documents')
# #         os.makedirs(documents_path, exist_ok=True)
        
# #         processed_count = 0
# #         for uploaded_file in uploaded_files:
# #             try:
# #                 # Save file to documents directory
# #                 file_path = os.path.join(documents_path, uploaded_file.name)
# #                 with open(file_path, "wb") as f:
# #                     f.write(uploaded_file.getbuffer())
                
# #                 # Process the file
# #                 with st.spinner(f"Processing {uploaded_file.name}..."):
# #                     result = self.rag_pipeline.process_single_file(file_path)
# #                     if result['success']:
# #                         processed_count += 1
# #                         st.success(f"✅ {uploaded_file.name}: {result['message']}")
# #                     else:
# #                         st.error(f"❌ {uploaded_file.name}: {result['message']}")
                        
# #             except Exception as e:
# #                 st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
# #         if processed_count > 0:
# #             st.success(f"✅ Successfully processed {processed_count} file(s)")

# # def main():
# #     """Main function to run the Streamlit app."""
# #     app = StreamlitApp()
# #     app.run()

# # if __name__ == "__main__":
# #     main()





# import streamlit as st
# import os
# import sys
# import logging
# from typing import List, Dict, Any
# from datetime import datetime

# # This import block remains the same as it's for project structure
# try:
#     # Attempt to import from the same directory (standard case)
#     from .rag_pipeline import RAGPipeline
#     from .config import config
# except ImportError:
#     # Fallback for when 'app.py' is run directly, common in development
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     parent_dir = os.path.dirname(current_dir)
#     if current_dir not in sys.path:
#         sys.path.insert(0, current_dir)
#     if parent_dir not in sys.path:
#         sys.path.insert(0, parent_dir)
    
#     try:
#         from rag_pipeline import RAGPipeline
#         from config import config
#     except ImportError:
#         # Fallback for running from within a 'src' directory
#         from src.rag_pipeline import RAGPipeline
#         from src.config import config

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class StreamlitApp:
#     def __init__(self):
#         """Initializes the Streamlit App with session state and configuration."""
#         self.config = config
#         self._rag_pipeline = None  # Lazy loading for performance

#         # Initialize session state variables if they don't exist
#         if 'chat_history' not in st.session_state:
#             st.session_state.chat_history = []
#         if 'web_search_enabled' not in st.session_state:
#             st.session_state.web_search_enabled = True
#         if 'system_info' not in st.session_state:
#             st.session_state.system_info = None
#         if 'confirm_delete' not in st.session_state:
#             st.session_state.confirm_delete = False

#     @property
#     def rag_pipeline(self):
#         """Lazy load and cache the RAG pipeline instance."""
#         if self._rag_pipeline is None:
#             with st.spinner("Initializing RAG Pipeline... Please wait."):
#                 try:
#                     self._rag_pipeline = RAGPipeline()
#                 except Exception as e:
#                     logger.error(f"Failed to initialize RAG pipeline: {e}")
#                     st.error(f"Fatal Error: Could not initialize the RAG pipeline. Please check logs. Error: {e}")
#                     st.stop()
#         return self._rag_pipeline

#     def _inject_custom_css(self):
#         """Injects custom CSS for a modern, colorful, and cohesive look."""
#         st.markdown("""
#         <style>
#             @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

#             /* --- CSS Variables for Theming --- */
#             :root {
#                 --primary-color: #1f77b4;      /* Strong Blue */
#                 --secondary-color: #2ca02c;    /* Vibrant Green */
#                 --user-msg-bg: linear-gradient(135deg, #007FFF, #005fcc);
#                 --assistant-msg-bg: linear-gradient(135deg, #28a745, #218838);
#                 --bg-color: #f0f2f6;           /* Light Gray Background */
#                 --sidebar-bg: #ffffff;
#                 --text-color: #333333;
#                 --light-text-color: #ffffff;
#                 --border-radius: 25px;
#                 --border-radius-sm: 15px;
#                 --destructive-color: #d9534f;
#                 --destructive-hover-color: #c9302c;
#             }
            
#             /* --- General & Typography --- */
#             body {
#                 font-family: 'Poppins', sans-serif;
#                 color: var(--text-color);
#             }

#             h1, h2, h3 {
#                 font-weight: 700;
#             }

#             /* --- Hide Streamlit Branding --- */
#             #MainMenu, footer { visibility: hidden; }

#             /* --- Main App Container --- */
#             [data-testid="stAppViewContainer"] {
#                 background-color: var(--bg-color);
#             }
            
#             /* --- Sidebar Styling --- */
#             [data-testid="stSidebar"] {
#                 background: var(--sidebar-bg);
#                 border-right: 1px solid #e6e6e6;
#             }

#             .st-emotion-cache-16txtl3 { /* Sidebar Header */
#                  font-size: 1.5rem;
#             }

#             /* --- Main Header & Subtitle --- */
#             .main-header {
#                 font-size: 2.8rem;
#                 font-weight: 700;
#                 color: var(--primary-color);
#                 text-align: center;
#                 margin-bottom: 0.5rem;
#                 text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#             }
#             .sub-header {
#                 text-align: center;
#                 color: #555;
#                 font-weight: 600;
#                 margin-top: -0.5rem;
#                 margin-bottom: 2rem;
#             }

#             /* --- Bubble Chat Style --- */
#             [data-testid="stChatMessage"] {
#                 border-radius: var(--border-radius);
#                 padding: 18px 22px;
#                 max-width: 75%;
#                 word-wrap: break-word;
#                 margin-top: 8px;
#                 margin-bottom: 8px;
#                 box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
#                 border: none;
#                 transition: transform 0.2s ease-out;
#             }
#             [data-testid="stChatMessage"]:hover {
#                 transform: scale(1.02);
#             }

#             /* User message (blue, right-aligned) */
#             [data-testid="stChatMessage"]:has(span[data-testid="chat-avatar-user"]) {
#                 background: var(--user-msg-bg);
#                 color: var(--light-text-color);
#                 border-bottom-right-radius: 5px;
#                 margin-left: auto;
#                 margin-right: 0;
#             }

#             /* Assistant message (green, left-aligned) */
#             [data-testid="stChatMessage"]:has(span[data-testid="chat-avatar-assistant"]) {
#                 background: var(--assistant-msg-bg);
#                 color: var(--light-text-color);
#                 border-bottom-left-radius: 5px;
#                 margin-left: 0;
#                 margin-right: auto;
#             }
            
#             /* --- Source & Info Box Styling --- */
#             .source-info {
#                 font-size: 0.8rem;
#                 color: #333;
#                 margin-top: 12px;
#                 padding: 10px 15px;
#                 background-color: rgba(40, 167, 69, 0.1);
#                 border-radius: var(--border-radius-sm);
#                 border-left: 5px solid var(--secondary-color);
#             }
#             .st-emotion-cache-1wivap2 { /* Streamlit's default Info box */
#                 border-left-color: var(--primary-color);
#                 background-color: rgba(31, 119, 180, 0.1);
#             }

#             /* --- General & Specific Button Styling --- */
#             div[data-testid="stButton"] > button {
#                 border-radius: var(--border-radius);
#                 background-color: var(--primary-color);
#                 color: var(--light-text-color);
#                 border: none;
#                 padding: 12px 28px;
#                 font-weight: 600;
#                 transition: all 0.2s ease-in-out;
#             }
#             div[data-testid="stButton"] > button:hover {
#                 background-color: #005fcc;
#                 box-shadow: 0 4px 8px rgba(0, 95, 204, 0.3);
#             }
#             div[data-testid="stButton"] > button:disabled {
#                  opacity: 0.6;
#             }

#             /* Destructive action button */
#             div[data-testid="stButton"] > button[kind="primary"] {
#                 background-color: var(--destructive-color);
#             }
#             div[data-testid="stButton"] > button[kind="primary"]:hover {
#                 background-color: var(--destructive-hover-color);
#                 box-shadow: 0 4px 8px rgba(201, 48, 44, 0.3);
#             }

#             /* --- Expander / Accordion Styling in Sidebar --- */
#             [data-testid="stExpander"] {
#                 border: 1px solid #e0e0e0;
#                 border-radius: var(--border-radius-sm);
#                 overflow: hidden;
#             }
#             [data-testid="stExpander"] summary { /* Expander Header */
#                 font-weight: 600;
#                 font-size: 1.05rem;
#                 padding: 5px 15px;
#             }
#         </style>
#         """, unsafe_allow_html=True)

#     def _render_sidebar(self):
#         """Render the sidebar with system information and controls."""
#         with st.sidebar:
#             st.header("🔧 Controls & Settings")

#             # Chat Settings Expander
#             with st.expander("⚙️ Chat Settings", expanded=True):
#                 st.session_state.web_search_enabled = st.toggle(
#                     "🌐 Enable Web Search",
#                     value=st.session_state.web_search_enabled,
#                     help="Allow the assistant to search the web for up-to-date information."
#                 )
#                 if st.button("🗑️ Clear Chat History"):
#                     st.session_state.chat_history = []
#                     st.rerun()

#             # System Status Expander
#             with st.expander("📊 System Status"):
#                 if st.button("🔄 Refresh System Info"):
#                     with st.spinner("Fetching system info..."):
#                         try:
#                             st.session_state.system_info = self.rag_pipeline.get_system_info()
#                         except Exception as e:
#                             st.error(f"Failed to get system info: {e}")
                
#                 if st.session_state.system_info:
#                     info = st.session_state.system_info
#                     st.success("✅ System Operational" if info.get('status') == 'operational' else "❌ System Error")
#                     if 'vector_database' in info:
#                         vdb = info['vector_database']
#                         st.info(f"**Docs in DB:** {vdb.get('total_documents', 'N/A')}\n\n"
#                                 f"**Embedding:** {vdb.get('embedding_model', 'N/A')}")
#                     if 'llm_provider' in info:
#                         llm = info['llm_provider']
#                         st.info(f"**LLM:** {llm.get('provider', 'N/A')} ({llm.get('model', 'N/A')})")

#             st.divider()

#             # Document Management
#             st.subheader("📄 Document Management")
#             uploaded_files = st.file_uploader(
#                 "Upload & Process Files",
#                 type=['pdf', 'docx', 'pptx', 'txt', 'md', 'csv', 'xlsx'],
#                 accept_multiple_files=True
#             )
#             if uploaded_files:
#                 if st.button("Process Uploaded Files"):
#                     self._process_uploaded_files(uploaded_files)

#             if st.button("🔄 Ingest Documents from Source"):
#                 with st.spinner("Ingesting documents..."):
#                     result = self.rag_pipeline.ingest_documents()
#                     st.success(f"✅ {result['message']}") if result['success'] else st.error(f"❌ {result['message']}")

#             # Safer deletion process
#             st.session_state.confirm_delete = st.checkbox(
#                 "I want to clear all documents",
#                 value=st.session_state.confirm_delete,
#                 help="Check this box to enable the delete button."
#             )
#             if st.button("💥 Clear All Documents", disabled=not st.session_state.confirm_delete, type="primary"):
#                 with st.spinner("Clearing all documents..."):
#                     result = self.rag_pipeline.clear_documents()
#                     st.success("✅ All documents cleared.") if result['success'] else st.error(f"❌ {result['message']}")
#                 st.session_state.confirm_delete = False # Reset checkbox
#                 st.rerun()

#             st.divider()

#             # Document Search
#             st.subheader("🔍 Document Search & Download")
#             search_query = st.text_input("Search for documents...", placeholder="e.g., python module 1")
#             if st.button("Search Documents"):
#                 if search_query:
#                     with st.spinner("Searching..."):
#                         docs = self.rag_pipeline.search_documents_for_download(search_query)
#                         self._render_document_results(docs)
#                 else:
#                     st.warning("Please enter a search query.")

#     def _render_document_results(self, documents: List[Dict[str, Any]]):
#         """Render document search results in the sidebar."""
#         if not documents:
#             st.warning("No documents found.")
#             return

#         st.success(f"Found {len(documents)} document(s).")
#         for doc in documents:
#             with st.expander(f"📄 {doc.get('file_name', 'Unknown')}"):
#                 file_size = doc.get('file_size', 0)
#                 if file_size < 1024: size_str = f"{file_size} B"
#                 elif file_size < 1024**2: size_str = f"{file_size/1024:.1f} KB"
#                 else: size_str = f"{file_size/1024**2:.1f} MB"
                
#                 st.markdown(f"""
#                 - **Type:** `{doc.get('file_type', 'N/A').upper()}`
#                 - **Size:** `{size_str}`
#                 - **Path:** `{doc.get('relative_path', 'N/A')}`
#                 - **Score:** ⭐ `{doc.get('score', 0):.2f}`
#                 """)
#                 if doc.get('exists'):
#                     self._create_download_button(doc)
#                 else:
#                     st.error("File not found on disk.")

#     def _create_download_button(self, doc: Dict[str, Any]):
#         """Create a download button for a document."""
#         try:
#             content = self.rag_pipeline.get_document_content(doc['file_path'])
#             if content:
#                 st.download_button(
#                     label="📥 Download",
#                     data=content,
#                     file_name=doc.get('file_name', 'download'),
#                     key=f"download_{doc['file_path']}"
#                 )
#         except Exception as e:
#             st.error(f"Download failed: {e}")

#     def _render_chat_interface(self):
#         """Renders the main chat interface using modern Streamlit elements."""
#         for message in st.session_state.chat_history:
#             avatar = "🧑‍💻" if message["role"] == "user" else "🎓"
#             with st.chat_message(message["role"], avatar=avatar):
#                 st.markdown(message["content"])
#                 if message["role"] == "assistant":
#                     self._render_assistant_extras(message)
        
#         if prompt := st.chat_input("Ask a question about your documents..."):
#             self._process_query(prompt)

#     def _render_assistant_extras(self, message: Dict[str, Any]):
#         """Renders extra information below an assistant's message."""
#         sources = message.get('sources', {})
#         source_info = []
#         if sources.get('documents'):
#             source_info.append(f"📄 {len(sources['documents'])} doc(s)")
#         if sources.get('web_search'):
#             source_info.append(f"🌐 {len(sources['web_search'])} web result(s)")
        
#         if source_info:
#             st.markdown(f"""
#             <div class="source-info">
#                 <strong>Sources:</strong> {' | '.join(source_info)}
#             </div>
#             """, unsafe_allow_html=True)
            
#         query_analysis = message.get('query_analysis', {})
#         if query_analysis:
#             parts = [f"{k.replace('_', ' ').title()}: {', '.join(v)}" for k, v in query_analysis.items() if v]
#             if parts:
#                 st.info(f"🔍 **Query Analysis:** {', '.join(parts)}")

#     def _process_query(self, query: str):
#         """Adds user query to history and triggers a rerun to display it."""
#         st.session_state.chat_history.append({
#             'role': 'user',
#             'content': query,
#             'timestamp': datetime.now().isoformat()
#         })
#         st.rerun()

#     def _handle_assistant_response(self):
#         """Generates and displays the assistant's response."""
#         last_message = st.session_state.chat_history[-1]
#         if last_message['role'] == 'user':
#             query = last_message['content']
            
#             with st.chat_message("assistant", avatar="🎓"):
#                 with st.spinner("Thinking..."):
#                     try:
#                         # Provide the last 6 messages (3 turns) as context
#                         chat_history_context = st.session_state.chat_history[-7:-1]
                        
#                         result = self.rag_pipeline.process_query(
#                             query=query,
#                             use_web_search=st.session_state.web_search_enabled,
#                             max_docs=5,
#                             chat_history=chat_history_context
#                         )
#                     except Exception as e:
#                         logger.error(f"Error processing query: {e}", exc_info=True)
#                         result = {
#                             'response': f"I'm sorry, I encountered a technical error. Please check the system logs. Error: {e}",
#                             'sources': {}, 'query_analysis': {}, 'directory_matches': []
#                         }
                
#                 assistant_message = {
#                     'role': 'assistant',
#                     'content': result['response'],
#                     'sources': result.get('sources', {}),
#                     'query_analysis': result.get('query_analysis', {}),
#                     'directory_matches': result.get('directory_matches', []),
#                     'timestamp': datetime.now().isoformat()
#                 }
#                 st.session_state.chat_history.append(assistant_message)
#                 st.rerun()

#     def _process_uploaded_files(self, uploaded_files):
#         """Process uploaded files and ingest them."""
#         documents_path = self.config.get_paths().get('documents', './data/documents')
#         os.makedirs(documents_path, exist_ok=True)
        
#         processed_count = 0
#         progress_bar = st.progress(0, text="Starting upload...")
#         for i, uploaded_file in enumerate(uploaded_files):
#             try:
#                 progress_text = f"Processing {uploaded_file.name}..."
#                 progress_bar.progress((i + 1) / len(uploaded_files), text=progress_text)
                
#                 file_path = os.path.join(documents_path, uploaded_file.name)
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
                
#                 result = self.rag_pipeline.process_single_file(file_path)
#                 if result['success']:
#                     processed_count += 1
#                 else:
#                     st.error(f"❌ {uploaded_file.name}: {result['message']}")
#             except Exception as e:
#                 st.error(f"❌ Failed to process {uploaded_file.name}: {e}")
        
#         progress_bar.empty()
#         if processed_count > 0:
#             st.success(f"Successfully processed and ingested {processed_count} file(s).")

#     def run(self):
#         """Main function to run the Streamlit application."""
#         st.set_page_config(
#             page_title="College RAG Assistant",
#             page_icon="🎓",
#             layout="wide",
#             initial_sidebar_state="expanded"
#         )
        
#         self._inject_custom_css()
#         self._render_sidebar()

#         st.markdown('<h1 class="main-header">🎓 College RAG Assistant</h1>', unsafe_allow_html=True)
#         st.markdown("<p class='sub-header'>School of Engineering, University of Mysore</p>", unsafe_allow_html=True)
        
#         self._render_chat_interface()

#         if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == 'user':
#             self._handle_assistant_response()

# def main():
#     """Main function to run the Streamlit app."""
#     app = StreamlitApp()
#     app.run()

# if __name__ == "__main__":
#     main()



import streamlit as st
import os
import sys
import logging
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

# This import block remains the same as it's for project structure
try:
    from .rag_pipeline import RAGPipeline
    from .config import config
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    try:
        from rag_pipeline import RAGPipeline
        from config import config
    except ImportError:
        from src.rag_pipeline import RAGPipeline
        from src.config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StreamlitApp:
    def __init__(self):
        """Initializes the Streamlit App with session state and configuration."""
        self.config = config
        self._rag_pipeline = None
        
        self.documents_root = os.path.abspath(self.config.get_paths().get('documents', './data/documents'))
        os.makedirs(self.documents_root, exist_ok=True)

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'web_search_enabled' not in st.session_state:
            st.session_state.web_search_enabled = True
        if 'system_info' not in st.session_state:
            st.session_state.system_info = None
        if 'confirm_delete' not in st.session_state:
            st.session_state.confirm_delete = False
        if 'current_browser_path' not in st.session_state:
            st.session_state.current_browser_path = self.documents_root
        # UPDATED: Key counter for resetting the chat input
        if 'chat_input_key_counter' not in st.session_state:
            st.session_state.chat_input_key_counter = 0

    @property
    def rag_pipeline(self):
        """Lazy load and cache the RAG pipeline instance."""
        if self._rag_pipeline is None:
            with st.spinner("Initializing RAG Pipeline... Please wait."):
                try:
                    self._rag_pipeline = RAGPipeline()
                except Exception as e:
                    logger.error(f"Failed to initialize RAG pipeline: {e}")
                    st.error(f"Fatal Error: Could not initialize the RAG pipeline. Error: {e}")
                    st.stop()
        return self._rag_pipeline

    def _inject_custom_css(self):
        """Injects custom CSS for a modern, colorful, and cohesive look."""
        # UPDATED: Removed the previous, non-working CSS fix for the chat input.
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
            :root {
                --primary-color: #1f77b4; --secondary-color: #2ca02c;
                --user-msg-bg: linear-gradient(135deg, #007FFF, #005fcc);
                --assistant-msg-bg: linear-gradient(135deg, #28a745, #218838);
                --bg-color: #f0f2f6; --sidebar-bg: #ffffff;
                --text-color: #333333; --light-text-color: #ffffff;
                --border-radius: 25px; --border-radius-sm: 15px;
                --destructive-color: #d9534f; --destructive-hover-color: #c9302c;
            }
            body { font-family: 'Poppins', sans-serif; color: var(--text-color); }
            h1, h2, h3 { font-weight: 700; }
            #MainMenu, footer { visibility: hidden; }
            [data-testid="stAppViewContainer"] { background-color: var(--bg-color); }
            [data-testid="stSidebar"] { background: var(--sidebar-bg); border-right: 1px solid #e6e6e6; }
            .st-emotion-cache-16txtl3 { font-size: 1.5rem; }
            .main-header {
                font-size: 2.8rem; font-weight: 700; color: var(--primary-color);
                text-align: center; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            .sub-header {
                text-align: center; color: #555; font-weight: 600;
                margin-top: -0.5rem; margin-bottom: 2rem;
            }
            [data-testid="stChatMessage"] {
                border-radius: var(--border-radius); padding: 18px 22px; max-width: 75%;
                word-wrap: break-word; margin-top: 8px; margin-bottom: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); border: none;
                transition: transform 0.2s ease-out;
            }
            [data-testid="stChatMessage"]:hover { transform: scale(1.02); }
            [data-testid="stChatMessage"]:has(span[data-testid="chat-avatar-user"]) {
                background: var(--user-msg-bg); color: var(--light-text-color);
                border-bottom-right-radius: 5px; margin-left: auto; margin-right: 0;
            }
            [data-testid="stChatMessage"]:has(span[data-testid="chat-avatar-assistant"]) {
                background: var(--assistant-msg-bg); color: var(--light-text-color);
                border-bottom-left-radius: 5px; margin-left: 0; margin-right: auto;
            }
            .source-info {
                font-size: 0.8rem; color: #333; margin-top: 12px; padding: 10px 15px;
                background-color: rgba(40, 167, 69, 0.1); border-radius: var(--border-radius-sm);
                border-left: 5px solid var(--secondary-color);
            }
            .st-emotion-cache-1wivap2 {
                border-left-color: var(--primary-color);
                background-color: rgba(31, 119, 180, 0.1);
            }
            div[data-testid="stButton"] > button, .stDownloadButton > button {
                border-radius: var(--border-radius); background-color: var(--primary-color);
                color: var(--light-text-color); border: none; padding: 12px 28px;
                font-weight: 600; transition: all 0.2s ease-in-out;
            }
            div[data-testid="stButton"] > button:hover, .stDownloadButton > button:hover {
                background-color: #005fcc; box-shadow: 0 4px 8px rgba(0, 95, 204, 0.3);
            }
            div[data-testid="stButton"] > button:disabled { opacity: 0.6; }
            div[data-testid="stButton"] > button[kind="primary"] { background-color: var(--destructive-color); }
            div[data-testid="stButton"] > button[kind="primary"]:hover {
                background-color: var(--destructive-hover-color);
                box-shadow: 0 4px 8px rgba(201, 48, 44, 0.3);
            }
            [data-testid="stExpander"] {
                border: 1px solid #e0e0e0; border-radius: var(--border-radius-sm); overflow: hidden;
            }
            [data-testid="stExpander"] summary { font-weight: 600; font-size: 1.05rem; padding: 5px 15px; }
            [data-testid="stChatInput"] {
                border-top: 1px solid #e0e0e0; padding-top: 1.5rem; background-color: var(--bg-color);
            }
        </style>
        """, unsafe_allow_html=True)

    def _render_sidebar(self):
        with st.sidebar:
            st.header("🔧 Controls & Settings")
            with st.expander("⚙️ Chat Settings", expanded=True):
                st.session_state.web_search_enabled = st.toggle(
                    "🌐 Enable Web Search",
                    value=st.session_state.web_search_enabled,
                    help="Allow the assistant to search the web for up-to-date information."
                )
                if st.button("🗑️ Clear Chat History"):
                    st.session_state.chat_history = []
                    st.session_state.chat_input_key_counter = 0 # Also reset the key
                    st.rerun()

            with st.expander("📊 System Status"):
                if st.button("🔄 Refresh System Info"):
                    with st.spinner("Fetching system info..."):
                        try:
                            st.session_state.system_info = self.rag_pipeline.get_system_info()
                        except Exception as e:
                            st.error(f"Failed to get system info: {e}")
                
                if st.session_state.system_info:
                    info = st.session_state.system_info
                    st.success("✅ System Operational" if info.get('status') == 'operational' else "❌ System Error")
                    if 'vector_database' in info:
                        vdb = info['vector_database']
                        st.info(f"**Docs in DB:** {vdb.get('total_documents', 'N/A')}\n\n"
                                f"**Embedding:** {vdb.get('embedding_model', 'N/A')}")
                    if 'llm_provider' in info:
                        llm = info['llm_provider']
                        st.info(f"**LLM:** {llm.get('provider', 'N/A')} ({llm.get('model', 'N/A')})")
            st.divider()
            st.subheader("📄 Document Management")
            uploaded_files = st.file_uploader(
                "Upload & Process Files",
                type=['pdf', 'docx', 'pptx', 'txt', 'md', 'csv', 'xlsx'],
                accept_multiple_files=True
            )
            if uploaded_files:
                if st.button("Process Uploaded Files"):
                    self._process_uploaded_files(uploaded_files)

            if st.button("🔄 Ingest Documents from Source"):
                with st.spinner("Ingesting documents..."):
                    result = self.rag_pipeline.ingest_documents()
                    st.success(f"✅ {result['message']}") if result['success'] else st.error(f"❌ {result['message']}")

            st.session_state.confirm_delete = st.checkbox(
                "I want to clear all documents",
                value=st.session_state.confirm_delete,
                help="Check this box to enable the delete button."
            )
            if st.button("💥 Clear All Documents", disabled=not st.session_state.confirm_delete, type="primary"):
                with st.spinner("Clearing all documents..."):
                    result = self.rag_pipeline.clear_documents()
                    st.success("✅ All documents cleared.") if result['success'] else st.error(f"❌ {result['message']}")
                st.session_state.confirm_delete = False
                st.rerun()
            st.divider()
            st.subheader("🔍 Document Search & Download")
            search_query = st.text_input("Search for documents...", placeholder="e.g., python module 1")
            if st.button("Search Documents"):
                if search_query:
                    with st.spinner("Searching..."):
                        docs = self.rag_pipeline.search_documents_for_download(search_query)
                        self._render_document_results(docs)
                else:
                    st.warning("Please enter a search query.")
            self._render_document_browser()

    def _render_document_browser(self):
        with st.expander("📂 Document Browser", expanded=False):
            current_path = st.session_state.current_browser_path
            if not os.path.abspath(current_path).startswith(self.documents_root):
                st.error("Access Denied. Resetting to root directory.")
                st.session_state.current_browser_path = self.documents_root
                st.rerun()

            display_path = Path(os.path.relpath(current_path, self.documents_root))
            st.markdown(f"**Current location:** `./{display_path}`")

            if os.path.abspath(current_path) != self.documents_root:
                if st.button("⬆️ Go Up to Parent Directory"):
                    st.session_state.current_browser_path = os.path.dirname(current_path)
                    st.rerun()
            
            try:
                items = os.listdir(current_path)
                dirs = sorted([d for d in items if os.path.isdir(os.path.join(current_path, d))])
                files = sorted([f for f in items if os.path.isfile(os.path.join(current_path, f))])

                for dirname in dirs:
                    if st.button(f"📁 {dirname}", key=f"dir_{dirname}", use_container_width=True):
                        st.session_state.current_browser_path = os.path.join(current_path, dirname)
                        st.rerun()

                st.markdown("---")
                col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
                for filename in files:
                    full_path = os.path.join(current_path, filename)
                    with col1:
                        st.text(f"📄 {filename}")
                    with col2:
                        try:
                            with open(full_path, "rb") as fp:
                                content = fp.read()
                            st.download_button(
                                label="📥", data=content, file_name=filename,
                                key=f"dl_{full_path}", help="Download file"
                            )
                        except Exception:
                            st.error("!")
                    with col3:
                        delete_popover = st.popover("🗑️", help="Delete file", use_container_width=True)
                        with delete_popover:
                            st.warning(f"Delete `{filename}` permanently?")
                            if st.button("🔴 Confirm", key=f"del_{full_path}", type="primary"):
                                try:
                                    result = self.rag_pipeline.delete_document_by_path(full_path)
                                    st.success("Deleted!") if result['success'] else st.error(f"Failed: {result['message']}")
                                except Exception as e:
                                    logger.error(f"UI failed to delete {full_path}: {e}")
                                    st.error(f"Error: {e}")
                                st.rerun()
            except Exception as e:
                st.error(f"Could not read directory: {e}")
    
    def _render_document_results(self, documents: List[Dict[str, Any]]):
        if not documents:
            st.warning("No documents found.")
            return
        st.success(f"Found {len(documents)} document(s).")
        for doc in documents:
            with st.expander(f"📄 {doc.get('file_name', 'Unknown')}"):
                file_size = doc.get('file_size', 0)
                size_str = f"{file_size/1024**2:.1f} MB" if file_size >= 1024**2 else f"{file_size/1024:.1f} KB" if file_size >= 1024 else f"{file_size} B"
                st.markdown(f"""
                - **Type:** `{doc.get('file_type', 'N/A').upper()}`
                - **Size:** `{size_str}`
                - **Path:** `{doc.get('relative_path', 'N/A')}`
                - **Score:** ⭐ `{doc.get('score', 0):.2f}`
                """)
                if doc.get('exists'):
                    self._create_download_button(doc)
                else:
                    st.error("File not found on disk.")

    def _create_download_button(self, doc: Dict[str, Any]):
        try:
            with open(doc['file_path'], "rb") as fp:
                content = fp.read()
            if content:
                st.download_button(
                    label="📥 Download", data=content,
                    file_name=doc.get('file_name', 'download'),
                    key=f"download_{doc['file_path']}"
                )
        except Exception as e:
            st.error(f"Download failed: {e}")

    def _render_chat_interface(self):
        for message in st.session_state.chat_history:
            avatar = "🧑‍💻" if message["role"] == "user" else "🎓"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                if message["role"] == "assistant":
                    self._render_assistant_extras(message)
        
        # UPDATED: Using the dynamic key here
        prompt = st.chat_input(
            "Ask a question about your documents...",
            key=f"chat_input_{st.session_state.chat_input_key_counter}"
        )
        if prompt:
            self._process_query(prompt)

    def _render_assistant_extras(self, message: Dict[str, Any]):
        sources = message.get('sources', {})
        source_info = []
        if sources.get('documents'):
            source_info.append(f"📄 {len(sources['documents'])} doc(s)")
        if sources.get('web_search'):
            source_info.append(f"🌐 {len(sources['web_search'])} web result(s)")
        if source_info:
            st.markdown(f"""
            <div class="source-info">
                <strong>Sources:</strong> {' | '.join(source_info)}
            </div>
            """, unsafe_allow_html=True)


### -------------- query_analysis --------------
# COMMENT TO DISABLE QUERY ANALYSIS
# ----------------------------------------------
        query_analysis = message.get('query_analysis', {})
        if query_analysis:
            # AFTER (This is the corrected line)
            parts = [f"{k.replace('_', ' ').title()}: {', '.join([str(item[0]) for item in v])}" for k, v in query_analysis.items() if v]
            if parts:
                st.info(f"🔍 **Query Analysis:** {', '.join(parts)}")


# ----------------------------------------------
# ----------------------------------------------





    def _process_query(self, query: str):
        # UPDATED: Incrementing the counter before the rerun
        st.session_state.chat_history.append({
            'role': 'user', 'content': query, 'timestamp': datetime.now().isoformat()
        })
        st.session_state.chat_input_key_counter += 1
        st.rerun()

    def _handle_assistant_response(self):
        last_message = st.session_state.chat_history[-1]
        if last_message['role'] == 'user':
            query = last_message['content']
            with st.chat_message("assistant", avatar="🎓"):
                with st.spinner("Thinking..."):
                    try:
                        chat_history_context = st.session_state.chat_history[-7:-1]
                        result = self.rag_pipeline.process_query(
                            query=query, use_web_search=st.session_state.web_search_enabled,
                            max_docs=5, chat_history=chat_history_context
                        )
                    except Exception as e:
                        logger.error(f"Error processing query: {e}", exc_info=True)
                        result = {
                            'response': f"I'm sorry, I encountered a technical error. Error: {e}",
                            'sources': {}, 'query_analysis': {}, 'directory_matches': []
                        }
                assistant_message = {
                    'role': 'assistant', 'content': result['response'],
                    'sources': result.get('sources', {}),
                    'query_analysis': result.get('query_analysis', {}),
                    'directory_matches': result.get('directory_matches', []),
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.chat_history.append(assistant_message)
                st.rerun()

    def _process_uploaded_files(self, uploaded_files):
        os.makedirs(self.documents_root, exist_ok=True)
        processed_count = 0
        progress_bar = st.progress(0, text="Starting upload...")
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                progress_text = f"Processing {uploaded_file.name}..."
                progress_bar.progress((i + 1) / len(uploaded_files), text=progress_text)
                file_path = os.path.join(self.documents_root, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                result = self.rag_pipeline.process_single_file(file_path)
                if result['success']:
                    processed_count += 1
                else:
                    st.error(f"❌ {uploaded_file.name}: {result['message']}")
            except Exception as e:
                st.error(f"❌ Failed to process {uploaded_file.name}: {e}")
        progress_bar.empty()
        if processed_count > 0:
            st.success(f"Successfully processed and ingested {processed_count} file(s).")

    def run(self):
        st.set_page_config(
            page_title="ERAGA", page_icon="🎓",
            layout="wide", initial_sidebar_state="expanded"
        )
        self._inject_custom_css()
        self._render_sidebar()
        st.markdown('<h1 class="main-header">🎓 ERAGA: Enhanced RAG Assistant for General Academics</h1>', unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Mysore University School of Engineering, University of Mysore</p>", unsafe_allow_html=True)
        self._render_chat_interface()
        if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == 'user':
            self._handle_assistant_response()

def main():
    """Main function to run the Streamlit app."""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()