@echo off
echo Starting College RAG Assistant...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "src\streamlit_app.py" (
    echo Error: Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Add src to Python path and run Streamlit
set PYTHONPATH=%CD%\src;%PYTHONPATH%
echo Starting Streamlit app...
echo.
echo The app will open in your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

python -m streamlit run src/streamlit_app.py --server.port=8501 --server.address=localhost

pause
