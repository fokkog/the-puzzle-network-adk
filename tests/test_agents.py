"""Basic tests for agents module."""

import asyncio

from bs4 import BeautifulSoup

from the_puzzle_network.agents.puzzle_classifier_agent import PuzzleClassifierAgent
from the_puzzle_network.agents.puzzle_formatter_agent import PuzzleFormatterAgent
from the_puzzle_network.logging import get_logger


logger = get_logger(__name__)


def test_easy_classification():
    """Test that agent can classify a puzzle as easy."""
    puzzle = '{"puzzle":"OSQ\nU I\nTNE","solution","QUESTION"}'
    prompt = f"Please classify this puzzle:\n{puzzle}"
    result = asyncio.run(PuzzleClassifierAgent().run_agent(prompt))
    assert "easy" == result


def test_medium_classification():
    """Test that agent can classify a puzzle as medium."""
    puzzle = '{"puzzle":"SEL\nU C\nHED","solution","SCHEDULE"}'
    prompt = f"Please classify this puzzle:\n{puzzle}"
    result = asyncio.run(PuzzleClassifierAgent().run_agent(prompt))
    assert "medium" == result


def test_hard_classification():
    """Test that agent can classify a puzzle as hard."""
    puzzle = '{"puzzle":"LAI\nT E\nPCR","solution","PARTICLE"}'
    prompt = f"Please classify this puzzle:\n{puzzle}"
    result = asyncio.run(PuzzleClassifierAgent().run_agent(prompt))
    assert "hard" == result


def test_formatting():
    """Test that agent can format a puzzle."""
    puzzle = '{"puzzle":"LAI\nT E\nPCR","solution","PARTICLE"}'
    prompt = f"Please format this puzzle:\n{puzzle}"
    html = asyncio.run(PuzzleFormatterAgent().run_agent(prompt))
    logger.info("Generated HTML:\n%s\n", html)
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find("div")
