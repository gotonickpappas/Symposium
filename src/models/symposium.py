 
"""
Agent registry and symposium management.
Handles agent creation, registration, and retrieval.
"""

from typing import Dict, List, Optional
from .agent import Agent, ModelProvider, AgentTier

class Symposium:
    """Main class for managing the agent registry and their relationships."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self._initialize_default_agents()
    
    def _initialize_default_agents(self) -> None:
        """Create the standard agent roster based on verified providers."""
        # Senior Fellows (premium models)
        self.register_agent(Agent(
            name="Gemini",
            provider=ModelProvider.GEMINI,
            model_name="gemini-2.5-pro",
            tier=AgentTier.SENIOR_FELLOW,
            persona_prompt="You are Gemini, a visionary Senior Fellow. Your role is strategic thinking, creative problem-solving, and comprehensive analysis."
        ))
        
        self.register_agent(Agent(
            name="Claude", 
            provider=ModelProvider.CLAUDE,
            model_name="claude-sonnet-4-20250514",
            tier=AgentTier.SENIOR_FELLOW,
            persona_prompt="You are Claude, a analytical Senior Fellow. Your role is critical evaluation, logical reasoning, and identifying potential flaws."
        ))
        
        # Research Assistants (tool-using models)
        self.register_agent(Agent(
            name="Groq_Assistant",
            provider=ModelProvider.GROQ,
            model_name="llama-3.3-70b-versatile",
            tier=AgentTier.RESEARCH_ASSISTANT,
            persona_prompt="You are a Research Assistant. Your role is to execute specific tasks using tools and provide concise, factual results."
        ))
        
        self.register_agent(Agent(
            name="Mistral_Assistant",
            provider=ModelProvider.MISTRAL,
            model_name="mistral-large-latest", 
            tier=AgentTier.RESEARCH_ASSISTANT,
            persona_prompt="You are a Research Assistant specialized in analysis and synthesis of information from multiple sources."
        ))
        
        self.register_agent(Agent(
            name="Cerebras_Assistant",
            provider=ModelProvider.CEREBRAS,
            model_name="llama-3.3-70b",
            tier=AgentTier.RESEARCH_ASSISTANT, 
            persona_prompt="You are a fast Research Assistant optimized for quick responses and straightforward task execution."
        ))
    
    def register_agent(self, agent: Agent) -> None:
        """Add an agent to the registry."""
        if agent.model_instance is None:
            print(f"Warning: Agent {agent.name} failed to initialize")
            return
        self.agents[agent.name] = agent
        print(f"Registered agent: {agent.name} ({agent.provider.value})")
    
    def get_agent_registry(self) -> Dict[str, Agent]:
        """Return the complete agent registry."""
        return self.agents.copy()
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Retrieve a specific agent by name."""
        return self.agents.get(name)
    
    def list_agents_by_tier(self, tier: AgentTier) -> List[Agent]:
        """Get all agents of a specific tier."""
        return [agent for agent in self.agents.values() if agent.tier == tier]