 
"""
Main orchestration controller for agent selection and message routing.
Handles the core Director-Agent interaction logic.
"""

from typing import Optional
from langchain_core.messages import HumanMessage

from models.symposium import Symposium
from models.agent import Agent, AgentTier
from models.workflow import WorkflowManager, GraphState

class Orchestrator:
    """Main controller for routing messages to appropriate agents."""
    
    def __init__(self):
        self.symposium = Symposium()
        self.workflow_manager = WorkflowManager()
        self.active_workflows = {}
    
    def quick_ask(self, agent_name: str, message: str, use_tools: bool = False) -> str:
        """Simple method to ask a single agent a question."""
        agent = self.symposium.get_agent(agent_name)
        if not agent:
            return f"Error: Agent {agent_name} not found"
        
        try:
            if use_tools and agent.tier == AgentTier.RESEARCH_ASSISTANT:
                # Use the tool-enabled workflow
                graph = self.workflow_manager.create_tool_agent_graph(agent)
                initial_state = GraphState(
                    messages=[HumanMessage(content=message)],
                    current_agent=agent_name
                )
                
                final_state = None
                for event in graph.stream(initial_state):
                    final_state = event
                
                if final_state and "agent" in final_state:
                    last_message = final_state["agent"]["messages"][-1]
                    return last_message.content
                else:
                    # Handle case where graph terminates at tools node (Cerebras)
                    last_message = final_state["tools"]["messages"][-1]
                    return last_message.content
            else:
                # Direct model call
                response = agent.model_instance.invoke([HumanMessage(content=message)])
                return response.content
        except Exception as e:
            return f"Error calling {agent_name}: {str(e)}"
    
    def get_agent_registry(self):
        """Expose the agent registry for external access."""
        return self.symposium.get_agent_registry()
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get a specific agent."""
        return self.symposium.get_agent(name)
    
    def list_agents_by_tier(self, tier: AgentTier):
        """List agents by capability tier."""
        return self.symposium.list_agents_by_tier(tier)