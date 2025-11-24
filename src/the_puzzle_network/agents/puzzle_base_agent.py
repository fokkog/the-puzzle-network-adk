"""Abstract base class for all puzzle network agents."""

from abc import ABC, abstractmethod

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.plugins import LoggingPlugin
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from the_puzzle_network.utils import extract_textpart, load_env


# Default retry options for all agents
retry_options = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


class PuzzleBaseAgent(ABC):
    def __init__(self) -> None:
        self.agent = LlmAgent(
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

    async def run_agent(self, prompt: str) -> str:
        runner = Runner(
            agent=self.agent,
            app_name=load_env(),
            session_service=InMemorySessionService(),
            plugins=[LoggingPlugin()],
        )
        response = await runner.run_debug(prompt, quiet=True)
        return extract_textpart(response)
