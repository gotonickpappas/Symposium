# =================================================================
# == The Multi-LLM Symposium Manager (Core Engine) ==
# =================================================================
# == Goal: Foundational classes for agent orchestration ==
# =================================================================

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dotenv import load_dotenv

# LangGraph and LangChain imports
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import Tool

# LLM Provider imports
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_cerebras import ChatCerebras

# Tool imports
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

# Load environment variables
load_dotenv()

class ModelProvider(Enum):
    """Enumeration of supported LLM providers."""
    GEMINI = "gemini"
    CLAUDE = "claude"
    GROQ = "groq"
    MISTRAL = "mistral"
    CEREBRAS = "cerebras"

class AgentTier(Enum):
    """Classification of agent capability and cost."""
    SENIOR_FELLOW = "senior_fellow"    # Premium models for complex reasoning
    RESEARCH_ASSISTANT = "research_assistant"  # Cheaper models for tool use

@dataclass
class Agent:
    """Represents a configured LLM agent with specific capabilities."""
    name: str
    provider: ModelProvider
    model_name: str
    tier: AgentTier
    persona_prompt: str
    tools: List[Tool] = field(default_factory=list)
    temperature: float = 0.0
    model_instance: Optional[Any] = field(default=None, init=False)
    
    def __post_init__(self):
        """Initialize the actual LLM instance after dataclass creation."""
        self.model_instance = self._create_model_instance()
    
    def _create_model_instance(self) -> Any:
        """Factory method to create the appropriate LLM instance."""
        try:
            if self.provider == ModelProvider.GEMINI:
                return ChatGoogleGenerativeAI(
                    model=self.model_name, 
                    temperature=self.temperature
                )
            elif self.provider == ModelProvider.CLAUDE:
                return ChatAnthropic(
                    model=self.model_name, 
                    temperature=self.temperature
                )
            elif self.provider == ModelProvider.GROQ:
                return ChatGroq(
                    model_name=self.model_name,
                    temperature=self.temperature
                )
            elif self.provider == ModelProvider.MISTRAL:
                return ChatMistralAI(
                    model_name=self.model_name,
                    temperature=self.temperature
                )
            elif self.provider == ModelProvider.CEREBRAS:
                return ChatCerebras(
                    model=self.model_name,
                    temperature=self.temperature
                )
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            print(f"Error creating model instance for {self.name}: {e}")
            return None

@dataclass
class GraphState:
    """State object that flows through LangGraph workflows."""
    messages: Annotated[List[BaseMessage], add_messages]
    current_agent: Optional[str] = None
    task_context: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class Symposium:
    """Main orchestration class for managing agents and workflows."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.active_workflows: Dict[str, Any] = {}
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
    
    def create_calculator_tool(self) -> Tool:
        """Create a simple calculator tool for testing."""
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
            description="Calculate basic math expressions. Input should be a math expression like '2+2' or '10*5'.",
            func=calculate
        )
    
    def create_tool_agent_graph(self, agent_name: str, tools: Optional[List[Tool]] = None) -> StateGraph:
        """Create a LangGraph workflow for a tool-using agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found in registry")
        
        # Use provided tools or default to calculator for research assistants
        if tools is None and agent.tier == AgentTier.RESEARCH_ASSISTANT:
            tools = [self.create_calculator_tool()]
        elif tools is None:
            tools = []
        
        # Bind tools to the agent's model instance
        if tools:
            model_with_tools = agent.model_instance.bind_tools(tools)
        else:
            model_with_tools = agent.model_instance
        
        def agent_node(state: GraphState) -> Dict[str, Any]:
            """Node function for the tool-using agent."""
            # Construct system message with persona
            system_message = HumanMessage(content=agent.persona_prompt)
            
            # Get all messages including system context
            messages = [system_message] + state.messages
            
            print(f"--- Calling {agent.name} ---")
            response = model_with_tools.invoke(messages)
            print(f"--- Response from {agent.name}: {response.content[:100]}... ---")
            
            return {
                "messages": [response],
                "current_agent": agent.name
            }
        
        def should_continue(state: GraphState) -> str:
            """Determine if the agent should use tools or finish."""
            last_message = state.messages[-1]
            
            # Check if the last message has tool calls
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return "tools"
            else:
                return "end"
        
        def tool_node(state: GraphState) -> Dict[str, Any]:
            """Execute tool calls and return results."""
            last_message = state.messages[-1]
            tool_calls = last_message.tool_calls
            
            tool_messages = []
            
            # Check the current agent to apply specific workarounds
            current_agent_name = state.current_agent
            
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_call_id = tool_call["id"]
                
                # Handle different parameter key formats across providers
                parameter_container = tool_call.get("parameters") or tool_call.get("args")
                if not parameter_container:
                    result = f"Error: No parameters found in tool call"
                else:
                    tool_to_use = None
                    for tool in tools:
                        if tool.name == tool_name:
                            tool_to_use = tool
                            break
                    
                    if tool_to_use:
                        try:
                            if "__arg1" in parameter_container:
                                result = tool_to_use.func(parameter_container["__arg1"])
                            else:
                                result = tool_to_use.func(**parameter_container)
                        except Exception as e:
                            result = f"Error: {str(e)}"
                    else:
                        result = f"Error: Tool '{tool_name}' not found"

                # Apply the Cerebras-specific workaround
                if current_agent_name == "Cerebras_Assistant":
                    # Add a supplementary HumanMessage to explicitly pass the tool output
                    # This helps the model to understand the tool's result.
                    tool_messages.append(
                        HumanMessage(content=f"Tool '{tool_name}' returned the result: {result}", name=tool_name)
                    )
                else:
                    # For other models, use the standard ToolMessage format.
                    tool_messages.append(
                        ToolMessage(content=str(result), tool_call_id=tool_call_id)
                    )
            
            return {"messages": tool_messages}
        
        # Build the graph
        workflow = StateGraph(GraphState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", tool_node)
        
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {"tools": "tools", "end": END}
        )
        # This is the key change. We are now conditionally routing the 'tools' node
        # based on the current agent.
        if agent_name == "Cerebras_Assistant":
            workflow.add_edge("tools", END)
        else:
            workflow.add_edge("tools", "agent")
        
        return workflow.compile()
    
    def quick_ask(self, agent_name: str, message: str, use_tools: bool = False) -> str:
        """Simple method to ask a single agent a question."""
        agent = self.get_agent(agent_name)
        if not agent:
            return f"Error: Agent {agent_name} not found"
        
        try:
            if use_tools and agent.tier == AgentTier.RESEARCH_ASSISTANT:
                # Use the tool-enabled workflow
                graph = self.create_tool_agent_graph(agent_name)
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
                    # This will handle the case where the graph terminates at the 'tools' node
                    # and the final state is not the 'agent' node.
                    last_message = final_state["tools"]["messages"][-1]
                    return last_message.content
            else:
                # Direct model call
                response = agent.model_instance.invoke([HumanMessage(content=message)])
                return response.content
        except Exception as e:
            return f"Error calling {agent_name}: {str(e)}"

# ===================== DEMO & TESTING =====================

if __name__ == "__main__":
    print("--- Initializing Symposium ---")
    symposium = Symposium()
    
    print("\n--- Agent Registry ---")
    for name, agent in symposium.get_agent_registry().items():
        status = "✓" if agent.model_instance else "✗"
        print(f"{status} {name} ({agent.provider.value}) - {agent.tier.value}")
    
    print("\n--- Testing Simple Agent Call ---")
    response = symposium.quick_ask("Claude", "What is 2+2? Answer in exactly 5 words.")
    print(f"Response: {response}")
    
    print("\n--- Testing Tool-Using Agents ---")
    research_assistants = ["Groq_Assistant", "Mistral_Assistant", "Cerebras_Assistant"]
    test_calculation = "Calculate 127 * 89 + 456"
    
    for assistant_name in research_assistants:
        print(f"\n--- Testing {assistant_name} ---")
        response = symposium.quick_ask(assistant_name, test_calculation, use_tools=True)
        print(f"{assistant_name}: {response}")
    
    print("\n--- Symposium Manager Ready ---")