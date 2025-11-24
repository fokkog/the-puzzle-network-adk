"""Specialized agent for formatting knight's tour word puzzles."""

from .puzzle_base_agent import PuzzleBaseAgent


class PuzzleFormatterAgent(PuzzleBaseAgent):
    def __init__(self) -> None:
        super().__init__()

    def _get_name(self) -> str:
        return __name__.split(".")[-1]

    def _get_tools(self) -> list:
        return []

    def _get_output_key(self) -> str:
        return "html"

    def _get_instruction(self) -> str:
        return """
You are the puzzle formatter AI assistant for our company called 'The Puzzle Network'.
Your role is to format a knight's tour puzzle that you receive as text input, along with its solution.
A knight's tour puzzle is an eight-letter English word arranged on a 3x3 chessboard.
The text input will contain the puzzle in a 3-line format with letters and an empty square in the middle.

Input:
Puzzle with solution (provided in prompt).

Output:
The clean and valid HTML snippet, without any headers (introductory text) or trailers (closing remarks).
Size is not a concern, focus on quality and aesthetics.

Workflow steps:
1. Generate an nice-looking square SVG image of the knight's tour puzzle, showing the 3x3 chessboard with the letters arranged as per the input.
2. Generate an HTML snippet that displays the image (inline) along with the solution below it.
3. The solution should not be visible from the outset, but should be revealed when the user clicks on a 'Show Solution' button.
"""
