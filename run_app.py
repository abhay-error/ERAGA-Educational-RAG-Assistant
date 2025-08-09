#!/usr/bin/env python3
"""
Simple runner for College RAG Assistant Streamlit app
"""

import sys
import os
from pathlib import Path

def main():
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    src_dir = current_dir / "src"
    
    # Add src to Python path
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    # Change to the project root directory
    os.chdir(current_dir)
    
    # Import and run the Streamlit app
    try:
        from src.streamlit_app import main as run_streamlit
        print("🚀 Starting College RAG Assistant...")
        print("📱 The app will open in your browser at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print()
        run_streamlit()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running this from the project root directory")
        return 1
    except Exception as e:
        print(f"❌ Error starting the app: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
