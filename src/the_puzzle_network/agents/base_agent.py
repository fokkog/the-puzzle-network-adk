"""Abstract base class for all puzzle network agents."""

from abc import ABC, abstractmethod

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types


class BaseAgent(ABC):
    def __init__(self, retry_options: types.HttpRetryOptions) -> None:
        self.retry_options = retry_options
        self.agent = self._create_llm_agent()

    def _create_llm_agent(self) -> LlmAgent:
        return LlmAgent(
            model=Gemini(
                model="gemini-3-pro-preview", retry_options=self.retry_options
            ),
            name=self._get_agent_name(),
            instruction=self._get_instruction(),
            output_key=self._get_output_key(),
        )

    @abstractmethod
    def _get_agent_name(self) -> str:
        """Get the name for this agent."""
        pass

    @abstractmethod
    def _get_instruction(self) -> str:
        """Get the instruction prompt for this agent."""
        pass

    @abstractmethod
    def _get_output_key(self) -> str:
        """Get the output key for this agent's response."""
        pass
