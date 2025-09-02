"""
LangGraph workflow management with provider-specific handling.
Contains workflow creation logic and execution state management.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from typing_extensions import Annotated

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import Tool

from .agent import Agent, AgentTier
from .tools.calculator import create_calculator_tool
from .tools.python_executor import create_python_executor_tool

@dataclass
class GraphState:
    """State object that flows through LangGraph workflows."""
    messages: Annotated[List[BaseMessage], add_messages]
    current_agent: Optional[str] = None
    task_context: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowManager:
    """Manages LangGraph workflow creation and execution."""
    
    def create_tool_agent_graph(self, agent: Agent, tools: Optional[List[Tool]] = None) -> StateGraph:
        """Create a LangGraph workflow for a tool-using agent."""
        if tools is None and agent.tier == AgentTier.RESEARCH_ASSISTANT:
            tools = [create_calculator_tool(), create_python_executor_tool()]
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

                # Apply Cerebras-specific workaround
                if current_agent_name == "Cerebras_Assistant":
                    # Cerebras doesn't handle ToolMessage objects properly
                    tool_messages.append(
                        HumanMessage(content=f"Tool '{tool_name}' returned the result: {result}", name=tool_name)
                    )
                else:
                    # Standard ToolMessage format for other providers
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
        
        # Cerebras requires different workflow termination
        if agent.name == "Cerebras_Assistant":
            workflow.add_edge("tools", END)
        else:
            workflow.add_edge("tools", "agent")
        
        return workflow.compile()