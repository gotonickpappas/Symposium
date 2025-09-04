@echo off
setlocal

rem =================================================================
rem ==        Secure, Non-Interactive Wrapper for Claude CLI       ==
rem ==                  (v1.3 - Finalized Flags)                   ==
rem =================================================================

set "ARGS=%*"

rem --- SECURITY CHECK ---
rem (Our existing security check remains here)
echo "%ARGS%" | findstr /R /C:"[a-zA-Z]:" /C:"\.\." >nul
if %errorlevel% == 0 (
    echo [SECURITY] Blocked attempt to access outside of the project directory.
    echo [COMMAND] %ARGS%
    exit /b 1
)

rem --- EXECUTION ---
rem Execute with a minimal, safe toolset AND the required non-interactive/verbose flags.
claude %* --allowedTools "Read,Write,Edit,Search"

endlocal