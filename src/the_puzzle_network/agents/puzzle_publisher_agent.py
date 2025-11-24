"""Specialized agent for publishing knight's tour word puzzles."""

from ..tools.puzzle_publisher_tool import PuzzlePublisherTool
from .puzzle_base_agent import PuzzleBaseAgent


class PuzzlePublisherAgent(PuzzleBaseAgent):
    def __init__(self) -> None:
        super().__init__()

    def _get_name(self) -> str:
        return __name__.split(".")[-1]

    def _get_tools(self) -> list:
        return [PuzzlePublisherTool().publish]

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
