# =================================================================
# ==   Step 2: The "Hello, World" Graph (Definitive Version)     ==
# =================================================================
# ==   Goal: Connect to the specified Senior Fellow: Gemini 2.5 Pro ==
# =================================================================

import os
from dotenv import load_dotenv
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

# --- 1. Load Environment Variables ---
load_dotenv()

# --- 2. Set up the Senior Fellow (LLM) ---
# CORRECTED: Using the specific, correct model name as directed.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

# --- 3. Define the Graph's State (Best Practice) ---
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]

# --- 4. Define the Nodes of the Graph ---
def senior_fellow_node(state: GraphState):
    print("--- CALLING SENIOR FELLOW (GEMINI 2.5 PRO) ---")
    response = llm.invoke(state["messages"])
    print(f"--- RESPONSE: {response.content} ---")
    return {"messages": [response]}

# --- 5. Build the Graph ---
workflow = StateGraph(GraphState)
workflow.add_node("senior_fellow", senior_fellow_node)
workflow.set_entry_point("senior_fellow")
workflow.add_edge("senior_fellow", END)
app = workflow.compile()


# --- 6. Run the Graph ---
if __name__ == "__main__":
    print("--- STARTING THE SYMPOSIUM ---")
    
    initial_input = {"messages": ["Hello, Symposium. This is the Director. Please confirm you are receiving me."]}
    
    for event in app.stream(initial_input):
        for node_name, node_output in event.items():
            print(f"--- OUTPUT FROM NODE: {node_name} ---")
            print(node_output)
            print("\n" + "="*40 + "\n")

    print("--- SYMPOSIUM CONCLUDED ---")