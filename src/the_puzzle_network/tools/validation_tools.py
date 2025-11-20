"""Validation tools for game quality checks."""

from google.adk.tools import FunctionTool


def validate_game_completion(game_data: dict) -> dict:
    """
    Validate that a game has all required components.

    Args:
        game_data: Dictionary containing game structure

    Returns:
        Dictionary with validation result and any missing fields
    """
    required_fields = ["type", "title", "words", "difficulty"]

    missing = [field for field in required_fields if field not in game_data]

    if missing:
        return {
            "valid": False,
            "error": f"Missing required fields: {', '.join(missing)}",
            "missing_fields": missing,
        }

    # Validate content
    if not game_data.get("words") or len(game_data["words"]) < 3:
        return {"valid": False, "error": "Game must contain at least 3 words"}

    valid_types = ["word_search", "crossword", "anagram", "word_match", "trivia"]
    if game_data["type"] not in valid_types:
        return {
            "valid": False,
            "error": f"Invalid game type. Must be one of: {', '.join(valid_types)}",
        }

    return {"valid": True, "message": "Game structure is valid"}


def check_content_quality(title: str, words: list[str], instructions: str) -> dict:
    """
    Check content quality metrics for a game.

    Args:
        title: Game title
        words: List of words in the game
        instructions: Game instructions text

    Returns:
        Dictionary with quality metrics
    """
    quality_issues = []

    # Check title
    if not title or len(title) < 3:
        quality_issues.append("Title must be at least 3 characters")
    if len(title) > 50:
        quality_issues.append("Title must be 50 characters or less")

    # Check words
    if len(words) < 3:
        quality_issues.append("Game must contain at least 3 words")
    if len(words) > 50:
        quality_issues.append("Game should not exceed 50 words")

    # Check instructions
    if not instructions or len(instructions) < 10:
        quality_issues.append("Instructions must be at least 10 characters")
    if len(instructions) > 500:
        quality_issues.append("Instructions should not exceed 500 characters")

    quality_score = 100
    if quality_issues:
        quality_score = max(0, 100 - (len(quality_issues) * 20))

    return {
        "valid": len(quality_issues) == 0,
        "quality_score": quality_score,
        "issues": quality_issues,
        "total_issues": len(quality_issues),
    }


def validate_theme_consistency(theme: str, words: list[str], description: str) -> dict:
    """
    Validate that words and description match the game theme.

    Args:
        theme: The game theme
        words: List of words in the game
        description: Game description

    Returns:
        Dictionary with consistency validation result
    """
    if not theme:
        return {"valid": False, "error": "Theme cannot be empty"}

    if not words:
        return {"valid": False, "error": "Word list cannot be empty"}

    # Simple check: theme should be mentioned or related to words
    theme_lower = theme.lower()
    description_lower = description.lower()

    theme_presence = theme_lower in description_lower
    word_count = len(words)

    return {
        "valid": True,
        "theme": theme,
        "theme_mentioned_in_description": theme_presence,
        "word_count": word_count,
        "consistency_score": 85 if theme_presence else 70,
    }


# Create FunctionTools for export
validate_game_completion_tool = FunctionTool(validate_game_completion)
check_content_quality_tool = FunctionTool(check_content_quality)
validate_theme_consistency_tool = FunctionTool(validate_theme_consistency)
