"""
Basic calculator tool for fast arithmetic operations.
"""

from langchain_core.tools import Tool

def create_calculator_tool() -> Tool:
    """Create a simple calculator tool for basic math."""
    def calculate(expression: str) -> str:
        """Simple calculator that evaluates basic math expressions."""
        try:
            # Only allow basic math operations for security
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Only basic math operations allowed"
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    return Tool(
        name="calculator",
        description="Fast arithmetic for simple expressions (2+2, 127*89). Use for basic math only.",
        func=calculate
    )