 
#!/usr/bin/env python3
"""
Multi-LLM Symposium Manager v2.0
Clean entry point using modular MVC architecture.
"""

from views.cli import SymposiumCLI
from controllers.orchestrator import Orchestrator

def main():
    """Main entry point for the symposium system."""
    # For direct access to orchestrator
    # orchestrator = Orchestrator()
    
    # For CLI demo
    cli = SymposiumCLI()
    cli.run_demo()

if __name__ == "__main__":
    main()