@echo off
REM =================================================================
REM ==   Synthesized Setup for The Multi-LLM Symposium (v1.5)      ==
REM =================================================================

cd /d "%~dp0"

REM --- Configuration ---
set VENV_NAME=symposium_env
set PYTHON_VERSION=3.13

REM --- Safety Check ---
if exist "%VENV_NAME%" (
    echo.
    echo [INFO] Virtual environment '%VENV_NAME%' already exists.
    echo [INFO] To add new packages, this script will now proceed to the installation step.
    echo.
    goto install
)

REM --- Environment Creation ---
echo.
echo [STEP 1] Creating virtual environment with Python %PYTHON_VERSION%...
py -%PYTHON_VERSION% -m venv "%VENV_NAME%"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to create virtual environment.
    echo [ERROR] Please ensure Python %PYTHON_VERSION% is installed and in your PATH.
    goto end
)

:install
REM --- Activation and Installation ---
echo.
echo [STEP 2] Activating environment and upgrading pip...
call "%VENV_NAME%\Scripts\activate.bat"
python -m pip install --upgrade pip

echo.
echo [STEP 3] Installing project dependencies...

REM --- Historical Installations (for reference) ---
REM pip install langgraph langchain langchain-google-genai langchain-anthropic langchain-openai python-dotenv
REM pip install langgraph langchain langchain-google-genai langchain-anthropic langchain-openai python-dotenv langchain-groq langchain-mistralai langchain-community beautifulsoup4
REM pip install langgraph langchain langchain-google-genai langchain-anthropic langchain-openai python-dotenv langchain-groq langchain-mistralai langchain-community beautifulsoup4 langchain-cerebras

REM --- Current Full Installation (Senior Fellows + Assistants + Tools) ---
pip install langgraph langchain langchain-google-genai langchain-anthropic langchain-openai python-dotenv langchain-groq langchain-mistralai langchain-community beautifulsoup4 langchain-cerebras langchain-google-community

echo.
echo =================================================================
echo ==                   SETUP & INSTALLATION COMPLETE             ==
echo =================================================================
echo.

:end
pause