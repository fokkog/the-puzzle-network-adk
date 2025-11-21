"""Tests for PuzzleClassifierAgent classification values."""

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from the_puzzle_network.agents.puzzle_classifier_agent import PuzzleClassifierAgent
from the_puzzle_network.utils import extract_textpart, load_env, retry_options


async def run_classification_test(puzzle: str) -> str:
    """Run classification for a given puzzle."""
    app_name = load_env()
    session_service = InMemorySessionService()
    agent = PuzzleClassifierAgent(retry_options, puzzle)
    runner = Runner(
        agent=agent.agent,
        app_name=app_name,
        session_service=session_service,
    )

    response = await runner.run_debug("Please classify this puzzle", quiet=True)
    return extract_textpart(response)


def test_easy_classification():
    """Test that agent can classify a puzzle as easy."""
    puzzle = '{"puzzle":"OSQ\nU I\nTNE","solution","QUESTION"}'
    result = asyncio.run(run_classification_test(puzzle))
    assert "easy" == result


def test_medium_classification():
    """Test that agent can classify a puzzle as medium."""
    puzzle = '{"puzzle":"SEL\nU C\nHED","solution","SCHEDULE"}'
    result = asyncio.run(run_classification_test(puzzle))
    assert "medium" == result


def test_hard_classification():
    """Test that agent can classify a puzzle as hard."""
    puzzle = '{"puzzle":"RTA\nE I\nPLC","solution","PARTICLE"}'
    result = asyncio.run(run_classification_test(puzzle))
    assert "hard" == result
