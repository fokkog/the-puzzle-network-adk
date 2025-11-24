"""Sequential workflow for the Puzzle Network using SequentialAgent."""

from google.adk.agents import SequentialAgent
from google.adk.plugins import LoggingPlugin
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from the_puzzle_network.agents.puzzle_classifier_agent import PuzzleClassifierAgent
from the_puzzle_network.agents.puzzle_formatter_agent import PuzzleFormatterAgent
from the_puzzle_network.agents.puzzle_generator_agent import PuzzleGeneratorAgent
from the_puzzle_network.agents.puzzle_publisher_agent import PuzzlePublisherAgent
from the_puzzle_network.utils import load_env


class PuzzleNetworkWorkflow:
    def __init__(self) -> None:
        self.agent = SequentialAgent(
            name=self._get_name(),
            sub_agents=[
                PuzzleGeneratorAgent().agent,
                PuzzleClassifierAgent().agent,
                PuzzleFormatterAgent().agent,
                PuzzlePublisherAgent().agent,
            ],
        )

    def _get_name(self) -> str:
        return __name__.split(".")[-1]

    async def run_workflow(self) -> None:
        prompt = (
            "Generate a puzzle, then classify it, format it as HTML and publish it."
        )
        runner = Runner(
            agent=self.agent,
            app_name=load_env(),
            session_service=InMemorySessionService(),
            plugins=[LoggingPlugin()],
        )
        await runner.run_debug(prompt, quiet=False)
