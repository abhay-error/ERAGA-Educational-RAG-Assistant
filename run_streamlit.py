#!/usr/bin/env python3
"""
Streamlit Runner for College RAG Assistant

This script runs the Streamlit app with proper path setup.
"""

import sys
import os
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Now run the Streamlit app
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    
    # Set the script path
    script_path = str(src_dir / "streamlit_app.py")
    
    # Run Streamlit
    sys.argv = ["streamlit", "run", script_path, "--server.port=8501", "--server.address=localhost"]
    sys.exit(stcli.main())
