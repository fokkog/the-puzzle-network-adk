"""Formatting tools for game output and structure."""

import json
from typing import Any

from google.adk.tools import FunctionTool


class GameFormatter:
    """Handles formatting of game structures and content."""

    def __init__(self) -> None:
        """Initialize the GameFormatter."""
        pass

    def format_game_structure(
        self, game_type: str, title: str, words: list[str], difficulty: str
    ) -> str:
        """
        Format a game into a structured JSON string.

        Creates a standardized game structure with metadata.

        Args:
            game_type: Type of game (e.g., 'word_search', 'crossword', 'anagram')
            title: Title of the game
            words: List of words in the game
            difficulty: Overall difficulty level (easy, medium, hard)

        Returns:
            JSON formatted game structure as string
        """
        game = {
            "metadata": {
                "type": game_type,
                "title": title,
                "difficulty": difficulty,
                "word_count": len(words),
            },
            "content": {
                "words": words,
                "instructions": f"Solve the {game_type} puzzle using these {len(words)} words",
                "estimated_time_minutes": self._calculate_estimated_time(words),
            },
        }

        return json.dumps(game, indent=2)

    def _calculate_estimated_time(self, words: list[str]) -> int:
        """Calculate estimated completion time based on word count and complexity."""
        base_time = 5
        word_factor = len(words) // 5
        return base_time + word_factor


class ClueFormatter:
    """Handles formatting of clues and hints for words."""

    def __init__(self) -> None:
        """Initialize the ClueFormatter with predefined hint templates."""
        self._hint_templates = {
            "animal": "This is a {length}-letter animal",
            "place": "This is a {length}-letter location",
            "object": "This is a {length}-letter object",
            "action": "This is a {length}-letter verb",
            "general": "This is a {length}-letter word",
        }

    def format_clue(self, word: str, category: str | None = None) -> dict[str, Any]:
        """
        Format a clue for a word game.

        Args:
            word: The word to create a clue for
            category: Optional category hint

        Returns:
            Dictionary with word, hint, and category information
        """
        category = category or "general"
        template = self._hint_templates.get(category, self._hint_templates["general"])
        hint = template.format(length=len(word))

        return {
            "word": word,
            "hint": hint,
            "category": category,
            "letter_count": len(word),
        }

    def add_hint_template(self, category: str, template: str) -> None:
        """Add a new hint template for a category."""
        self._hint_templates[category] = template

    def get_available_categories(self) -> list[str]:
        """Get list of available hint categories."""
        return list(self._hint_templates.keys())


class AnswerKeyFormatter:
    """Handles formatting of answer keys and solutions."""

    def __init__(self) -> None:
        """Initialize the AnswerKeyFormatter."""
        pass

    def format_answer_key(self, words_with_answers: list[dict[str, Any]]) -> str:
        """
        Format an answer key for a game.

        Args:
            words_with_answers: List of dicts with 'word' and 'hint' keys

        Returns:
            Formatted answer key as string
        """
        lines = ["ANSWER KEY", "=" * 40]

        for i, item in enumerate(words_with_answers, 1):
            word = item.get("word", "")
            hint = item.get("hint", "")
            lines.append(f"{i}. {word.upper()} - {hint}")

        return "\n".join(lines)

    def format_solution_grid(self, words: list[str], grid_size: tuple[int, int]) -> str:
        """
        Format a solution grid for word puzzles.

        Args:
            words: List of words to display
            grid_size: Tuple of (rows, columns) for the grid

        Returns:
            Formatted grid as string
        """
        rows, cols = grid_size
        grid_lines = []

        for i in range(0, len(words), cols):
            row_words = words[i : i + cols]
            # Pad row if needed
            while len(row_words) < cols:
                row_words.append("")

            # Format each word to fit column width
            formatted_row = " | ".join(f"{word:<12}" for word in row_words)
            grid_lines.append(f"| {formatted_row} |")

            if i + cols < len(words):  # Add separator between rows
                grid_lines.append("-" * len(grid_lines[-1]))

        return "\n".join(grid_lines)


# Create singleton instances for backward compatibility and convenience
_game_formatter = GameFormatter()
_clue_formatter = ClueFormatter()
_answer_key_formatter = AnswerKeyFormatter()


# Function wrappers for backward compatibility
def format_game_structure(
    game_type: str, title: str, words: list[str], difficulty: str
) -> str:
    """Backward compatibility wrapper for GameFormatter.format_game_structure."""
    return _game_formatter.format_game_structure(game_type, title, words, difficulty)


def format_clue(word: str, category: str | None = None) -> dict[str, Any]:
    """Backward compatibility wrapper for ClueFormatter.format_clue."""
    return _clue_formatter.format_clue(word, category)


def format_answer_key(words_with_answers: list[dict[str, Any]]) -> str:
    """Backward compatibility wrapper for AnswerKeyFormatter.format_answer_key."""
    return _answer_key_formatter.format_answer_key(words_with_answers)


# Create FunctionTools for export
format_game_structure_tool = FunctionTool(format_game_structure)
format_clue_tool = FunctionTool(format_clue)
format_answer_key_tool = FunctionTool(format_answer_key)
