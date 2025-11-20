"""Tools module - centralized export of classes and backward-compatible tools."""

from google.adk.tools import FunctionTool

# Import new class-based tools
from .format_tools import (
    AnswerKeyFormatter,
    ClueFormatter,
    GameFormatter,
    format_answer_key_tool,
    format_clue_tool,
    format_game_structure_tool,
)
from .validation_tools import (
    ContentValidator,
    GameType,
    GameValidator,
    check_content_quality_tool,
    validate_game_completion_tool,
    validate_theme_consistency_tool,
)
from .word_tools import (
    BaseWordAnalyzer,
    DifficultyLevel,
    WordAnalyzer,
    calculate_difficulty_tool,
    check_word_variety_tool,
    validate_word_tool,
)


# Export all classes and tools
__all__ = [
    # Classes - New class-based API
    "WordAnalyzer",
    "BaseWordAnalyzer",
    "GameValidator",
    "ContentValidator",
    "GameFormatter",
    "ClueFormatter",
    "AnswerKeyFormatter",
    # Enums and data types
    "DifficultyLevel",
    "GameType",
    # FunctionTools - Backward compatibility
    "validate_word_tool",
    "calculate_difficulty_tool",
    "check_word_variety_tool",
    "format_game_structure_tool",
    "format_clue_tool",
    "format_answer_key_tool",
    "validate_game_completion_tool",
    "check_content_quality_tool",
    "validate_theme_consistency_tool",
]


def get_all_tools() -> list[FunctionTool]:
    """Return a list of all available FunctionTool instances for backward compatibility."""
    return [
        validate_word_tool,
        calculate_difficulty_tool,
        check_word_variety_tool,
        format_game_structure_tool,
        format_clue_tool,
        format_answer_key_tool,
        validate_game_completion_tool,
        check_content_quality_tool,
        validate_theme_consistency_tool,
    ]


def create_tool_suite() -> dict[str, object]:
    """Create a complete tool suite with both classes and function tools."""
    return {
        "analyzers": {
            "word_analyzer": WordAnalyzer(),
            "game_validator": GameValidator(),
            "content_validator": ContentValidator(),
        },
        "formatters": {
            "game_formatter": GameFormatter(),
            "clue_formatter": ClueFormatter(),
            "answer_key_formatter": AnswerKeyFormatter(),
        },
        "function_tools": get_all_tools(),
    }
