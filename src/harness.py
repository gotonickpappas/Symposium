# =================================================================
# ==   Step 5: Lab Assistant Harness (v1.3)                      ==
# =================================================================
# ==   Goal: Provide unified control for all assistants.         ==
# =================================================================

import os
from dotenv import load_dotenv

# Import the LLM providers
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_cerebras import ChatCerebras

# Load API keys
load_dotenv()

class LabAssistants:
    def __init__(self):
        self.assistants = {}
        self.initialized = False

        try:
            # CORRECTED: Updated to the latest Llama 3.1 model on Groq.
            self.assistants["Groq"] = ChatGroq(model_name="llama-3.3-70b-versatile")
            
            self.assistants["Mistral"] = ChatMistralAI(model_name="mistral-large-latest")
            
            self.assistants["Cerebras"] = ChatCerebras(model="llama3.1-8b")
            
            print("--- Assistants Initialized Successfully ---")
            self.initialized = True

        except Exception as e:
            print(f"!!! ERROR initializing assistants: {e}")

    def _normalize_response(self, response):
        """Extracts the model’s output in a consistent way."""
        if hasattr(response, "content"):
            return response.content
        elif hasattr(response, "text"):
            return response.text
        else:
            return str(response)

    def ask_all(self, prompt: str):
        """Send the same prompt to all assistants."""
        results = {}
        if not self.initialized:
            results["System"] = "[ERROR] Assistants were not initialized."
            return results
            
        for name, llm in self.assistants.items():
            try:
                response = llm.invoke(prompt)
                results[name] = self._normalize_response(response)
            except Exception as e:
                results[name] = f"[ERROR] {e}"
        return results

    def ask(self, names: list, prompt: str):
        """Send the prompt only to the chosen assistants."""
        results = {}
        if not self.initialized:
            results["System"] = "[ERROR] Assistants were not initialized."
            return results

        for name in names:
            if name not in self.assistants:
                results[name] = "[ERROR] Assistant not found"
                continue
            try:
                response = self.assistants[name].invoke(prompt)
                results[name] = self._normalize_response(response)
            except Exception as e:
                results[name] = f"[ERROR] {e}"
        return results


# ===================== DEMO =====================

if __name__ == "__main__":
    lab = LabAssistants()

    if lab.initialized:
        test_prompt = "System check: Please respond with your model name."
        
        print("\n--- ASK ALL ---")
        results = lab.ask_all(test_prompt)
        for name, reply in results.items():
            print(f"{name}: {reply}\n")

        print("\n--- ASK MISTRAL + CEREBRAS ---")
        results = lab.ask(["Mistral", "Cerebras"], "What is 2 + 2?")
        for name, reply in results.items():
            print(f"{name}: {reply}\n")