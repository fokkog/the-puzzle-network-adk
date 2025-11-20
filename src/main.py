"""Main entry point for The Puzzle Network workflow."""

import asyncio
import os

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

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

        root_agent = PuzzleGeneratorAgent(retry_options).agent
        runner = InMemoryRunner(agent=root_agent)
        response = await runner.run_debug("Please return next puzzle", quiet=True)
        if len(response) > 0:
            if (
                response[0].content
                and response[0].content.parts
                and len(response[0].content.parts) > 0
            ):
                print(response[0].content.parts[0].text)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
