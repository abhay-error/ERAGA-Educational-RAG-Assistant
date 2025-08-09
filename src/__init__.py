# College RAG Assistant - Main Package

from .config import config
from .document_processor import DocumentProcessor
from .vector_db import VectorDB
from .web_search import WebSearch
from .llm_provider import LLMProvider
from .rag_pipeline import RAGPipeline

__version__ = "1.0.0"
__author__ = "College RAG Assistant Team"
__email__ = "support@college-rag-assistant.com"

__all__ = [
    'config',
    'DocumentProcessor',
    'VectorDB', 
    'WebSearch',
    'LLMProvider',
    'RAGPipeline'
]
