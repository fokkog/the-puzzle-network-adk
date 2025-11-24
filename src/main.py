"""Main entry point for The Puzzle Network workflow."""

import asyncio

from the_puzzle_network.logging import get_logger
from the_puzzle_network.workflows.puzzle_network_workflow import PuzzleNetworkWorkflow


logger = get_logger(__name__)


async def main() -> None:
    try:
        workflow = PuzzleNetworkWorkflow()
        await workflow.run_workflow()

    except Exception as e:
        logger.error("❌ Unexpected error: %s", e)
        logger.debug("Full traceback:", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
