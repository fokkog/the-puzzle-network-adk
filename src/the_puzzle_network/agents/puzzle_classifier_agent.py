"""Specialized agent for classifying knight's tour word puzzles."""

from google.genai import types

from .base_agent import BaseAgent


class PuzzleClassifierAgent(BaseAgent):
    def __init__(
        self,
        retry_options: types.HttpRetryOptions,
        puzzle: str,
    ) -> None:
        self.puzzle = puzzle
        super().__init__(retry_options)

    def _get_agent_name(self) -> str:
        return "puzzle_classifier_agent"

    def _get_output_key(self) -> str:
        return "classification"

    def _get_instruction(self) -> str:
        return f"""
You are the puzzle classifier AI assistant for our company called 'The Puzzle Network'.
Your role is to read the knight's tour puzzle that is passed to you and to classify it as 'easy', 'medium' or 'hard' depending on its complexity.
Puzzle with solution: {self.puzzle}

Output:
The output should be the classification as a string, hence again 'easy', 'medium' or 'hard'.

For reference:
- Puzzle "OSQ\nU I\nTNE" with solution "QUESTION" is considered "easy"
- Puzzle "SEL\nU C\nHED" with solution "SCHEDULE" is considered "medium"
- Puzzle "RTA\nE I\nPLC" with solution "PARTICLE" is considered "hard"
"""
