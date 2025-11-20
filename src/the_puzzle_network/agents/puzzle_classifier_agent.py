"""Specialized agent for generating knight's tour word puzzles."""

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types


class PuzzleClassifierAgent:
    def __init__(
        self,
        retry_options: types.HttpRetryOptions,
        puzzle: str,
    ) -> None:
        self.retry_options = retry_options
        self.puzzle = puzzle
        self.agent = self._create_llm_agent()

    def _create_llm_agent(self) -> LlmAgent:
        return LlmAgent(
            model=Gemini(
                model="gemini-3-pro-preview", retry_options=self.retry_options
            ),
            name="puzzle_classifier_agent",
            instruction=self._get_instruction(self.puzzle),
            output_key="classification",
        )

    def _get_instruction(self, puzzle: str) -> str:
        return f"""
You are the puzzle classifier AI assistant for our company called 'The Puzzle Network'.
Your role is to read the knight's tour puzzle that is passed to you and to classify it as 'easy', 'medium' or 'hard' depending on its complexity.
Puzzle with solution: {puzzle}

Output:
The output should be the classification as a string, hence again 'easy', 'medium' or 'hard'.

For reference:
- Puzzle "OSQ\nU I\nTNE" with solution "QUESTION" is considered "easy"
- Puzzle "SEL\nU C\nHED" with solution "SCHEDULE" is considered "medium"
- Puzzle "RTA\nE I\nPLC" with solution "PARTICLE" is considered "hard"
"""
