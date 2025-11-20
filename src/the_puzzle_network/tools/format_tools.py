"""Formatting tools for game output and structure."""

from google.adk.tools import FunctionTool
import json


def format_game_structure(game_type: str, title: str, words: list[str], difficulty: str) -> str:
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
            "word_count": len(words)
        },
        "content": {
            "words": words,
            "instructions": f"Solve the {game_type} puzzle using these {len(words)} words",
            "estimated_time_minutes": 5 + (len(words) // 5)
        }
    }
    
    return json.dumps(game, indent=2)


def format_clue(word: str, category: str = None) -> dict:
    """
    Format a clue for a word game.
    
    Args:
        word: The word to create a clue for
        category: Optional category hint
        
    Returns:
        Dictionary with word, hint, and category
    """
    hints = {
        "animal": f"This is a {len(word)}-letter animal",
        "place": f"This is a {len(word)}-letter location",
        "object": f"This is a {len(word)}-letter object",
        "action": f"This is a {len(word)}-letter verb"
    }
    
    hint = hints.get(category, f"This is a {len(word)}-letter word")
    
    return {
        "word": word,
        "hint": hint,
        "category": category or "general",
        "letter_count": len(word)
    }


def format_answer_key(words_with_answers: list[dict]) -> str:
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


# Create FunctionTools for export
format_game_structure_tool = FunctionTool(format_game_structure)
format_clue_tool = FunctionTool(format_clue)
format_answer_key_tool = FunctionTool(format_answer_key)
