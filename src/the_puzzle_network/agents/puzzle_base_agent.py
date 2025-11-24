"""Abstract base class for all puzzle network agents."""

from abc import ABC, abstractmethod

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types


# Default retry options for all agents
retry_options = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


class PuzzleBaseAgent(ABC):
    def __init__(self) -> None:
        self.agent = self._create_llm_agent()

    def _create_llm_agent(self) -> LlmAgent:
        return LlmAgent(
            model=Gemini(model="gemini-3-pro-preview", retry_options=retry_options),
            name=self._get_name(),
            tools=self._get_tools(),
            output_key=self._get_output_key(),
            instruction=self._get_instruction(),
        )

    @abstractmethod
    def _get_name(self) -> str:
        """Get the name for this agent."""
        pass

    @abstractmethod
    def _get_tools(self) -> list:
        """Get the list of tools for this agent."""
        pass

    @abstractmethod
    def _get_output_key(self) -> str:
        """Get the output key for this agent's response."""
        pass

    @abstractmethod
    def _get_instruction(self) -> str:
        """Get the instruction prompt for this agent."""
        pass
