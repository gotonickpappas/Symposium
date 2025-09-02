"""
Whitelist-based Python execution tool.
Safe for basic calculations, falls back to Docker for complex operations.
"""

import ast
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from langchain_core.tools import Tool

# Whitelist of safe operations
SAFE_IMPORTS = {
    'math', 'decimal', 'statistics', 'random', 'json', 're', 'datetime'
}

SAFE_BUILTINS = {
    'print', 'len', 'range', 'enumerate', 'zip', 'sum', 'max', 'min', 
    'abs', 'round', 'sorted', 'reversed', 'any', 'all', 'int', 'float', 
    'str', 'list', 'dict', 'set', 'tuple', 'bool'
}

def _analyze_code_safety(code: str) -> tuple[bool, str]:
    """Analyze if code contains only whitelisted operations."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in SAFE_IMPORTS:
                    return False, f"Non-whitelisted import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module not in SAFE_IMPORTS:
                return False, f"Non-whitelisted import: {node.module}"
    
    return True, "Safe"

def create_python_executor_tool() -> Tool:
    """Create whitelist-based Python executor with Docker fallback option."""
    
    def execute_python(code: str) -> str:
        """Execute Python code with safety analysis."""
        
        # Analyze code safety
        is_safe, safety_msg = _analyze_code_safety(code)
        
        if not is_safe:
            return f"Code rejected by whitelist: {safety_msg}\n(Docker fallback not implemented yet)"
        
        # Execute safe code directly
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        safe_globals = {
            '__builtins__': {name: getattr(__builtins__, name) for name in SAFE_BUILTINS}
        }
        
        # Add safe modules
        try:
            import math, decimal, statistics, random, json, re, datetime
            safe_globals.update({
                'math': math,
                'decimal': decimal,
                'Decimal': decimal.Decimal,
                'statistics': statistics,
                'random': random,
                'json': json,
                're': re,
                'datetime': datetime,
            })
        except ImportError:
            pass
        
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, safe_globals)
            
            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()
            
            if stderr_output:
                return f"Error: {stderr_output.strip()}"
            elif stdout_output:
                return stdout_output.strip()
            else:
                return "Code executed successfully (no output)"
                
        except Exception as e:
            return f"Execution error: {str(e)}"
    
    return Tool(
        name="python_executor",
        description="Execute Python code with whitelist security. Supports math, decimal, statistics, datetime, json, re modules. Include print() statements to show results.",
        func=execute_python
    )