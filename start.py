#!/usr/bin/env python3
"""
Simple startup script for College RAG Assistant

This script provides an easy way to start the application with proper setup.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import chromadb
        import sentence_transformers
        import yaml
        print("✅ All required dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables and directories."""
    print("🔧 Setting up environment...")
    
    # Set environment variables to force CPU usage and avoid GPU issues
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    
    # Create necessary directories
    directories = [
        'data/documents',
        'data/processed', 
        'data/cache',
        'logs',
        'vector_db'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created directory: {directory}")
    
    # Check for environment variables
    required_vars = ['OPENROUTER_API_KEY', 'OPENAI_API_KEY']
    found_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            found_vars.append(var)
    
    if found_vars:
        print(f"   ✅ Found API keys: {', '.join(found_vars)}")
    else:
        print("   ⚠️ No API keys found. Some features may not work.")
        print("   Please set OPENROUTER_API_KEY or OPENAI_API_KEY environment variables.")

def main():
    """Main function."""
    print("🎓 College RAG Assistant - Startup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    print("\n🚀 Starting College RAG Assistant...")
    print("📊 Opening Streamlit interface...")
    print("🌐 Access the application at: http://localhost:8501")
    print("\nPress Ctrl+C to stop the application.")
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user.")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
