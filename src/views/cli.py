 
"""
Command-line interface for testing and interacting with the symposium.
"""

from controllers.orchestrator import Orchestrator
from models.agent import AgentTier

class SymposiumCLI:
    """Simple CLI interface for testing symposium functionality."""
    
    def __init__(self):
        self.orchestrator = Orchestrator()
    
    def run_demo(self):
        """Run the standard demo sequence from the original manager."""
        print("--- Initializing Symposium ---")
        
        print("\n--- Agent Registry ---")
        for name, agent in self.orchestrator.get_agent_registry().items():
            status = "✓" if agent.model_instance else "✗"
            print(f"{status} {name} ({agent.provider.value}) - {agent.tier.value}")
        
        print("\n--- Testing Simple Agent Call ---")
        response = self.orchestrator.quick_ask("Claude", "What is 2+2? Answer in exactly 5 words.")
        print(f"Response: {response}")
        
        print("\n--- Testing Tool-Using Agents ---")
        research_assistants = ["Groq_Assistant", "Mistral_Assistant", "Cerebras_Assistant"]
        test_calculation = "Calculate 127 * 89 + 456"
        
        for assistant_name in research_assistants:
            print(f"\n--- Testing {assistant_name} ---")
            response = self.orchestrator.quick_ask(assistant_name, test_calculation, use_tools=True)
            print(f"{assistant_name}: {response}")
        
        print("\n--- Symposium Ready ---")

if __name__ == "__main__":
    cli = SymposiumCLI()
    cli.run_demo()