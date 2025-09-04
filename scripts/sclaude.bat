@echo off
setlocal

rem =================================================================
rem ==        Secure, Non-Interactive Wrapper for Claude CLI       ==
rem ==                  (v1.1 - With Automation Flags)             ==
rem =================================================================
rem
rem 1. Acts as a security sandbox to prevent directory traversal.
rem 2. Automatically applies flags for non-interactive execution.
rem

set "ARGS=%*"

rem --- SECURITY CHECK ---
rem Block absolute paths (like C:\) and directory traversal (like ..\)
echo "%ARGS%" | findstr /R /C:"[a-zA-Z]:" /C:"\.\." >nul
if %errorlevel% == 0 (
    echo [SECURITY] Blocked attempt to access outside of the project directory.
    echo [COMMAND] %ARGS%
    exit /b 1
)

rem --- EXECUTION ---
rem Execute the real Claude CLI with the original prompt AND the non-interactive flags.
rem -p flag tells it to proceed without asking for confirmation.
claude %* -p --allowedTools "Read,Write,Edit,Search" --verbose --output-format stream-json

endlocal