#!/usr/bin/env python3
"""
College RAG Assistant - Main Entry Point

This is the main entry point for the College RAG Assistant application.
It provides a command-line interface for running the application.

Usage:
    python main.py                    # Run the Streamlit app
    python main.py --help            # Show help
    python main.py --ingest          # Ingest documents only
    python main.py --info            # Show system info
"""

import argparse
import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.rag_pipeline import RAGPipeline
from src.config import config

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/rag_assistant.log')
        ]
    )

def show_system_info():
    """Show system information."""
    try:
        rag_pipeline = RAGPipeline()
        info = rag_pipeline.get_system_info()
        
        print("\n" + "="*50)
        print("COLLEGE RAG ASSISTANT - SYSTEM INFO")
        print("="*50)
        
        if info.get('status') == 'operational':
            print("✅ System Status: Operational")
        else:
            print("❌ System Status: Error")
            if 'error' in info:
                print(f"Error: {info['error']}")
        
        # Vector DB info
        if 'vector_database' in info:
            vdb_info = info['vector_database']
            print(f"\n📄 Vector Database:")
            print(f"   Documents: {vdb_info.get('total_documents', 0)}")
            print(f"   Model: {vdb_info.get('embedding_model', 'N/A')}")
            print(f"   Collection: {vdb_info.get('collection_name', 'N/A')}")
        
        # LLM info
        if 'llm_provider' in info:
            llm_info = info['llm_provider']
            print(f"\n🤖 LLM Provider:")
            print(f"   Provider: {llm_info.get('provider', 'N/A')}")
            print(f"   Model: {llm_info.get('model', 'N/A')}")
        
        # Web search info
        if 'web_search' in info:
            web_info = info['web_search']
            status = "Enabled" if web_info.get('enabled') else "Disabled"
            print(f"\n🌐 Web Search:")
            print(f"   Status: {status}")
            print(f"   Providers: {', '.join(web_info.get('providers', []))}")
        
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"❌ Error getting system info: {e}")

def ingest_documents():
    """Ingest documents from the documents folder."""
    try:
        print("📥 Starting document ingestion...")
        rag_pipeline = RAGPipeline()
        result = rag_pipeline.ingest_documents()
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"   Chunks processed: {result['chunks_processed']}")
        else:
            print(f"❌ {result['message']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error during document ingestion: {e}")
        return False

def run_streamlit():
    """Run the Streamlit application."""
    try:
        print("🚀 Starting College RAG Assistant...")
        print("📊 Opening Streamlit interface...")
        print("🌐 The app will open in your browser at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print()
        
        # Get the path to the Streamlit app
        current_dir = Path(__file__).parent
        streamlit_app_path = current_dir / "src" / "streamlit_app.py"
        
        if not streamlit_app_path.exists():
            print(f"❌ Error: Streamlit app not found at {streamlit_app_path}")
            return
        
        # Set up environment for Streamlit
        os.environ['PYTHONPATH'] = f"{current_dir / 'src'}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"
        
        # Run Streamlit using subprocess
        import subprocess
        import sys
        
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(streamlit_app_path),
            "--server.port=8501",
            "--server.address=localhost"
        ]
        
        subprocess.run(cmd)
        
    except ImportError as e:
        print(f"❌ Error importing Streamlit: {e}")
        print("Make sure you have installed all dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error running Streamlit app: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="College RAG Assistant - AI-powered chat assistant for the School of Engineering, University of Mysore",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                    # Run the Streamlit app
    python main.py --ingest          # Ingest documents only
    python main.py --info            # Show system info
    python main.py --help            # Show this help message
        """
    )
    
    parser.add_argument(
        '--ingest',
        action='store_true',
        help='Ingest documents from the documents folder'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show system information'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='College RAG Assistant v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data/documents', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/cache', exist_ok=True)
    os.makedirs('vector_db', exist_ok=True)
    
    # Handle different modes
    if args.info:
        show_system_info()
    elif args.ingest:
        success = ingest_documents()
        sys.exit(0 if success else 1)
    else:
        # Default: run Streamlit app
        run_streamlit()

if __name__ == "__main__":
    main()
