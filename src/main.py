"""Main entry point for The Puzzle Network workflow."""

import asyncio
import os

from dotenv import load_dotenv
from google.adk.events import Event
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from the_puzzle_network.agents.puzzle_classifier_agent import PuzzleClassifierAgent
from the_puzzle_network.agents.puzzle_generator_agent import PuzzleGeneratorAgent


async def main() -> None:
    try:
        load_dotenv()
        app_name = os.getenv("APP_NAME")
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        print(
            f"✅ GOOGLE_API_KEY environment variable has been set, {app_name} can proceed."
        )

        retry_options = types.HttpRetryOptions(
            attempts=5,  # Maximum retry attempts
            exp_base=7,  # Delay multiplier
            initial_delay=1,
            http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
        )

        session_service = InMemorySessionService()
        puzzle_generator_agent = PuzzleGeneratorAgent(retry_options).agent
        runner = Runner(
            agent=puzzle_generator_agent,
            app_name=app_name,
            session_service=session_service,
        )
        response = await runner.run_debug("Please return next puzzle", quiet=True)
        puzzle = extract_textpart(response)
        print(f"Generated puzzle: {puzzle}")

        puzzle_classifier_agent = PuzzleClassifierAgent(retry_options, puzzle).agent
        runner = Runner(
            agent=puzzle_classifier_agent,
            app_name=app_name,
            session_service=session_service,
        )
        response = await runner.run_debug("Please classify next puzzle", quiet=True)
        classification = extract_textpart(response)
        print(f"Generated classification: {classification}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()


def extract_textpart(response: list[Event]) -> str:
    textpart = "N/A"
    if (
        len(response) > 0
        and response[0].content
        and response[0].content.parts
        and len(response[0].content.parts) > 0
        and response[0].content.parts[0].text
    ):
        textpart = response[0].content.parts[0].text
    return textpart


if __name__ == "__main__":
    asyncio.run(main())
