"""Factory classes and functions for creating tool collections and suites."""

from typing import Any

from google.adk.tools import FunctionTool

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
    GameValidator,
    check_content_quality_tool,
    validate_game_completion_tool,
    validate_theme_consistency_tool,
)
from .word_tools import (
    WordAnalyzer,
    calculate_difficulty_tool,
    check_word_variety_tool,
    validate_word_tool,
)


class ToolSuiteFactory:
    """Factory for creating and organizing tool collections."""

    @staticmethod
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

    @staticmethod
    def create_tool_suite() -> dict[str, Any]:
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
            "function_tools": ToolSuiteFactory.get_all_tools(),
        }

    @staticmethod
    def create_analyzer_suite() -> dict[str, Any]:
        """Create just the analyzer tools."""
        return {
            "word_analyzer": WordAnalyzer(),
            "game_validator": GameValidator(),
            "content_validator": ContentValidator(),
        }

    @staticmethod
    def create_formatter_suite() -> dict[str, Any]:
        """Create just the formatter tools."""
        return {
            "game_formatter": GameFormatter(),
            "clue_formatter": ClueFormatter(),
            "answer_key_formatter": AnswerKeyFormatter(),
        }

    @staticmethod
    def create_function_tool_suite() -> list[FunctionTool]:
        """Create just the function tools for backward compatibility."""
        return ToolSuiteFactory.get_all_tools()

    @classmethod
    def create_custom_suite(
        cls,
        include_analyzers: bool = True,
        include_formatters: bool = True,
        include_function_tools: bool = True,
    ) -> dict[str, Any]:
        """
        Create a custom tool suite with selective inclusion.

        Args:
            include_analyzers: Whether to include analyzer tools
            include_formatters: Whether to include formatter tools
            include_function_tools: Whether to include function tools

        Returns:
            Dictionary containing selected tool categories
        """
        suite: dict[str, Any] = {}

        if include_analyzers:
            suite["analyzers"] = cls.create_analyzer_suite()

        if include_formatters:
            suite["formatters"] = cls.create_formatter_suite()

        if include_function_tools:
            suite["function_tools"] = cls.create_function_tool_suite()

        return suite


# Convenience functions for backward compatibility
def get_all_tools() -> list[FunctionTool]:
    """Return a list of all available FunctionTool instances for backward compatibility."""
    return ToolSuiteFactory.get_all_tools()


def create_tool_suite() -> dict[str, Any]:
    """Create a complete tool suite with both classes and function tools."""
    return ToolSuiteFactory.create_tool_suite()
