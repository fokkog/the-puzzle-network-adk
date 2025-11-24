"""Specialized agent for classifying knight's tour word puzzles."""

from .puzzle_base_agent import PuzzleBaseAgent


class PuzzleClassifierAgent(PuzzleBaseAgent):
    def __init__(self) -> None:
        super().__init__()

    def _get_name(self) -> str:
        return __name__.split(".")[-1]

    def _get_tools(self) -> list:
        return []

    def _get_output_key(self) -> str:
        return "classification"

    def _get_instruction(self) -> str:
        return """
You are the puzzle classifier AI assistant for our company called 'The Puzzle Network'.
Your role is to read the knight's tour puzzle that is passed to you and to classify it as 'easy', 'medium' or 'hard' depending on its complexity.

Input:
Puzzle with solution (provided in prompt).

Output:
The output should be the classification as a string, hence again 'easy', 'medium' or 'hard'.

For reference:
- Puzzle "OSQ\nU I\nTNE" with solution "QUESTION" is considered "easy"
- Puzzle "SEL\nU C\nHED" with solution "SCHEDULE" is considered "medium"
- Puzzle "LAI\nT E\nPCR" with solution "PARTICLE" is considered "hard"
"""
