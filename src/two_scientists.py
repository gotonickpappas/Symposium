# =================================================================
# ==   Step 3: The Two-Scientist Dialogue (Experiment)             ==
# =================================================================
# ==   Goal: Test if Claude can respond when he goes first.       ==
# =================================================================

import os
from dotenv import load_dotenv
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, BaseMessage

from langgraph.graph import StateGraph, END

# --- 1. Load Environment Variables ---
load_dotenv()

# --- 2. Set up the Senior Fellows ---
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
claude = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

# --- 3. Define the Graph's State ---
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]

# --- 4. Define the Nodes of the Graph ---
def scientist_node(state: GraphState, llm, model_name: str):
    print(f"--- CALLING {model_name.upper()} ---")
    response = llm.invoke(state["messages"])
    print(f"--- RESPONSE FROM {model_name.upper()}: {response.content} ---")
    return {"messages": [response]}

# --- 5. Define the Routing Logic ---
def router(state: GraphState) -> str:
    print("--- ROUTING ---")
    
    if len(state["messages"]) >= 3:
        print("--- Decision: End Conversation ---")
        return END

    last_message: BaseMessage = state["messages"][-1]
    
    # EXPERIMENT: Swapped the logic. If last message was from Claude, route to Gemini.
    if "claude" in last_message.response_metadata.get("model_name", ""):
         print("--- Decision: Route to Gemini ---")
         return "gemini_node"
    # Otherwise (it was from the user), route to Claude.
    else:
        print("--- Decision: Route to Claude ---")
        return "claude_node"

# --- 6. Build the Graph ---
workflow = StateGraph(GraphState)

workflow.add_node("gemini_node", lambda state: scientist_node(state, gemini, "Gemini"))
workflow.add_node("claude_node", lambda state: scientist_node(state, claude, "Claude"))

# EXPERIMENT: The entry point is now Claude.
workflow.set_entry_point("claude_node")

# We still need both conditional edges for a potential loop.
workflow.add_conditional_edges(
    "gemini_node", router, {"claude_node": "claude_node", END: END}
)
workflow.add_conditional_edges(
    "claude_node", router, {"gemini_node": "gemini_node", END: END}
)

app = workflow.compile()


# --- 7. Run the Graph ---
if __name__ == "__main__":
    print("--- STARTING THE SYMPOSIUM ---")
    
    config = {"recursion_limit": 10}
    
    # Using the simplest prompt that worked before.
    initial_input = {
        "messages": [
            HumanMessage(content="Please provide a one-sentence summary of the theory of relativity.")
        ]
    }
    
    for event in app.stream(initial_input, config=config):
        for node_name, node_output in event.items():
            print(f"--- OUTPUT FROM NODE: {node_name} ---")
            print(node_output)
            print("\n" + "="*40 + "\n")

    print("--- SYMPOSIUM CONCLUDED ---")