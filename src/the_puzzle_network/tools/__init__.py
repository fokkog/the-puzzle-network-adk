"""Tools module - centralized export of all available tools."""

from google.adk.tools import FunctionTool

# Import individual tools from modules
from .word_tools import (
    validate_word_tool,
    calculate_difficulty_tool,
    check_word_variety_tool
)
from .format_tools import (
    format_game_structure_tool,
    format_clue_tool,
    format_answer_key_tool
)
from .validation_tools import (
    validate_game_completion_tool,
    check_content_quality_tool,
    validate_theme_consistency_tool
)

# Export all tools
__all__ = [
    # Word tools
    "validate_word_tool",
    "calculate_difficulty_tool",
    "check_word_variety_tool",
    # Format tools
    "format_game_structure_tool",
    "format_clue_tool",
    "format_answer_key_tool",
    # Validation tools
    "validate_game_completion_tool",
    "check_content_quality_tool",
    "validate_theme_consistency_tool",
]


def get_all_tools() -> list[FunctionTool]:
    """Return a list of all available tools."""
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
