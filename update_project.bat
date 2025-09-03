@echo off
REM =================================================================
REM ==    Orchestrates the Full, Auditable Symposium Knowledge Update   ==
REM =================================================================

REM Change the current directory to the script's directory
cd /d "%~dp0"

REM --- PREPARATION ---
ECHO.
ECHO This script will orchestrate a full update of the project's knowledge base.
ECHO It requires an 'update_instructions.txt' file in the project root.
ECHO.
IF NOT EXIST update_instructions.txt (
    ECHO ERROR: 'update_instructions.txt' not found. Nothing to do.
    PAUSE
    EXIT /B 1
)
ECHO Instructions file found. Proceeding with update...
PAUSE

REM --- STEP 1: AI-Powered Narrative & Decision Updates ---
ECHO.
ECHO [STEP 1] Tasking Claude Code to execute instructions...
claude "Carefully read the file 'update_instructions.txt' and execute ALL the actions it describes, in order."
ECHO.
ECHO Claude Code task complete.

REM --- STEP 2: Automated Code Snapshot Generation ---
ECHO.
ECHO [STEP 2] Generating a fresh code snapshot for Gemini...
ECHO * Scanning src/ directory...
ECHO * Processing Python source files...  
ECHO * Including scripts/ directory...
ECHO * Capturing root configuration files...
python scripts/generate_code_snapshot.py
ECHO ✓ Code snapshot generation complete.

REM --- STEP 3: AUDIT & ARCHIVE ---
ECHO.
ECHO [STEP 3] Archiving the completed instruction file...
ECHO * Generating timestamp...

REM Get the current date using Python (more reliable than Windows date parsing)
python -c "import datetime; print(datetime.datetime.now().strftime('%%Y-%%m-%%d_%%H-%%M-%%S'))" > temp_date.txt
set /p timestamp=<temp_date.txt
del temp_date.txt

ECHO * Creating archive directory...
REM Create the archive directory if it doesn't exist
IF NOT EXIST "docs\Past Updates" MKDIR "docs\Past Updates"

ECHO * Moving instruction file to archive...
REM Rename the file to include the date and a success marker
REN update_instructions.txt %timestamp%_update_instructions_executed.txt

REM Move the archived file to the Past Updates folder
MOVE %timestamp%_update_instructions_executed.txt "docs\Past Updates\"

ECHO ✓ Instruction file archived as %timestamp%_update_instructions_executed.txt
ECHO.
ECHO =================================================================
ECHO ==           PROJECT KNOWLEDGE BASE IS NOW SYNCED              ==
ECHO =================================================================
PAUSE