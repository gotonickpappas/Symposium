 
"""
Core Agent model with LLM provider integration.
Contains Agent class, provider enums, and model factory logic.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional, Any
from enum import Enum
from dotenv import load_dotenv

# LangChain LLM Provider imports
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_cerebras import ChatCerebras
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