"""Specialized agent for generating knight's tour word puzzles."""

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types


class PuzzleGeneratorAgent:
    def __init__(
        self,
        retry_options: types.HttpRetryOptions,
    ) -> None:
        self.retry_options = retry_options
        self.agent = self._create_llm_agent()

    def _create_llm_agent(self) -> LlmAgent:
        return LlmAgent(
            model=Gemini(
                model="gemini-3-pro-preview", retry_options=self.retry_options
            ),
            name="puzzle_generator_agent",
            instruction=self._get_instruction(),
            output_key="puzzle",
        )

    def _get_instruction(self) -> str:
        return """
You are the puzzle generator AI assistant for our company called 'The Puzzle Network'.
Your role is to generate a new knight's tour puzzle.

Workflow steps:
1. Pick a random English word that is exactly 8 letters long. The word has to be well-known and generally understood.
2. Create a puzzle by arranging its letters in a knight's tour pattern on a 3x3 chessboard with the middle square left empty,
use a random starting position and a random starting direction.
3. Create the string representation of the chessboard which is strictly 3 lines of text, each line containing 3 characters.
All letters must be uppercase and the position in the middle (2nd character of 2nd line) should be a space.

Output:
The output should be a properly formatted JSON object with 2 elements:
- puzzle, being the string representation of the chessboard
- solution, being the original word
"""
