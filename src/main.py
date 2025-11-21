"""Main entry point for The Puzzle Network workflow."""

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from the_puzzle_network.agents.puzzle_classifier_agent import PuzzleClassifierAgent
from the_puzzle_network.agents.puzzle_generator_agent import PuzzleGeneratorAgent
from the_puzzle_network.logging import get_logger
from the_puzzle_network.utils import extract_textpart, load_env


logger = get_logger(__name__)


async def main() -> None:
    try:
        app_name = load_env()

        session_service = InMemorySessionService()
        puzzle_generator_agent = PuzzleGeneratorAgent().agent
        runner = Runner(
            agent=puzzle_generator_agent,
            app_name=app_name,
            session_service=session_service,
        )
        response = await runner.run_debug("Please return next puzzle", quiet=True)
        puzzle = extract_textpart(response)
        logger.info("Generated puzzle: %s", puzzle)

        puzzle_classifier_agent = PuzzleClassifierAgent().agent
        runner = Runner(
            agent=puzzle_classifier_agent,
            app_name=app_name,
            session_service=session_service,
        )
        response = await runner.run_debug(
            f"Please classify this puzzle:\n{puzzle}", quiet=True
        )
        classification = extract_textpart(response)
        logger.info("Generated classification: %s", classification)

    except Exception as e:
        logger.error("❌ Unexpected error: %s", e)
        logger.debug("Full traceback:", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
