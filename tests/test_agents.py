"""Tests for PuzzleClassifierAgent classification values."""

import asyncio

from bs4 import BeautifulSoup
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from the_puzzle_network.agents.puzzle_classifier_agent import PuzzleClassifierAgent
from the_puzzle_network.agents.puzzle_formatter_agent import PuzzleFormatterAgent
from the_puzzle_network.utils import extract_textpart, load_env, retry_options


async def _run_classification_test(puzzle: str) -> str:
    """Run classifier for a given puzzle."""
    runner = Runner(
        agent=PuzzleClassifierAgent(retry_options).agent,
        app_name=load_env(),
        session_service=InMemorySessionService(),
    )
    response = await runner.run_debug(
        f"Please classify this puzzle:\n{puzzle}", quiet=True
    )
    return extract_textpart(response)


async def _run_formatting_test(puzzle: str) -> str:
    """Run formatter for a given puzzle."""
    runner = Runner(
        agent=PuzzleFormatterAgent(retry_options).agent,
        app_name=load_env(),
        session_service=InMemorySessionService(),
    )
    response = await runner.run_debug(
        f"Please format this puzzle:\n{puzzle}", quiet=True
    )
    return extract_textpart(response)


def test_easy_classification():
    """Test that agent can classify a puzzle as easy."""
    puzzle = '{"puzzle":"OSQ\nU I\nTNE","solution","QUESTION"}'
    result = asyncio.run(_run_classification_test(puzzle))
    assert "easy" == result


def test_medium_classification():
    """Test that agent can classify a puzzle as medium."""
    puzzle = '{"puzzle":"SEL\nU C\nHED","solution","SCHEDULE"}'
    result = asyncio.run(_run_classification_test(puzzle))
    assert "medium" == result


def test_hard_classification():
    """Test that agent can classify a puzzle as hard."""
    puzzle = '{"puzzle":"RTA\nE I\nPLC","solution","PARTICLE"}'
    result = asyncio.run(_run_classification_test(puzzle))
    assert "hard" == result


def test_formatting():
    """Test that agent can format a puzzle."""
    puzzle = '{"puzzle":"RTA\nE I\nPLC","solution","PARTICLE"}'
    html = asyncio.run(_run_formatting_test(puzzle))
    print(html)
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find("div")
