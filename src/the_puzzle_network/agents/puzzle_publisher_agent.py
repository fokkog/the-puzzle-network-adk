"""Specialized agent for publishing knight's tour word puzzles."""

from ..tools.publisher_tool import PublisherTool
from .base_agent import BaseAgent


class PuzzlePublisherAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__()

    def _get_agent_name(self) -> str:
        return __name__.split(".")[-1]

    def _get_tools(self) -> list:
        return [PublisherTool().publish]

    def _get_output_key(self) -> str:
        return "distribution_status"

    def _get_instruction(self) -> str:
        return """
You are the puzzle publisher AI assistant for our company called 'The Puzzle Network'.
Your role is to publish a knight's tour puzzle that you receive as HTML input, along with its level.

Input:
Puzzle in HTML format along with level (provided in prompt).

Output:
None

Steps:
Use your tool to publish the puzzle to the appropriate (as per the level) distribution list."""
