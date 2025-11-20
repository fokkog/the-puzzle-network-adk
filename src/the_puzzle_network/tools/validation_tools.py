"""Validation tools for game quality checks."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from google.adk.tools import FunctionTool


class GameType(Enum):
    """Enumeration of supported game types."""

    WORD_SEARCH = "word_search"
    CROSSWORD = "crossword"
    ANAGRAM = "anagram"
    WORD_MATCH = "word_match"
    TRIVIA = "trivia"


@dataclass
class GameValidationResult:
    """Result of game structure validation."""

    valid: bool
    message: str | None = None
    error: str | None = None
    missing_fields: list[str] | None = None


@dataclass
class QualityResult:
    """Result of content quality analysis."""

    valid: bool
    quality_score: int
    issues: list[str]
    total_issues: int


@dataclass
class ThemeConsistencyResult:
    """Result of theme consistency validation."""

    valid: bool
    theme: str
    theme_mentioned_in_description: bool
    word_count: int
    consistency_score: int
    error: str | None = None


class BaseGameValidator(ABC):
    """Abstract base class for game validation operations."""

    @abstractmethod
    def validate_game_completion(
        self, game_data: dict[str, Any]
    ) -> GameValidationResult:
        """Validate game structure completeness."""
        pass

    @abstractmethod
    def check_content_quality(
        self, title: str, words: list[str], instructions: str
    ) -> QualityResult:
        """Check content quality metrics."""
        pass

    @abstractmethod
    def validate_theme_consistency(
        self, theme: str, words: list[str], description: str
    ) -> ThemeConsistencyResult:
        """Validate theme consistency."""
        pass


class GameValidator(BaseGameValidator):
    """Comprehensive game validation and quality checking."""

    def __init__(
        self,
        required_fields: list[str] | None = None,
        valid_game_types: list[GameType] | None = None,
        quality_thresholds: dict[str, tuple[int, int]] | None = None,
    ) -> None:
        """
        Initialize game validator with configurable rules.

        Args:
            required_fields: List of required game data fields
            valid_game_types: Supported game types
            quality_thresholds: Quality score thresholds for various metrics
        """
        self.required_fields = required_fields or [
            "type",
            "title",
            "words",
            "difficulty",
        ]
        self.valid_game_types = valid_game_types or list(GameType)
        self.quality_thresholds = quality_thresholds or {
            "title_length": (3, 50),
            "word_count": (3, 50),
            "instructions_length": (10, 500),
        }

    def validate_game_completion(
        self, game_data: dict[str, Any]
    ) -> GameValidationResult:
        """
        Validate that a game has all required components.

        Args:
            game_data: Dictionary containing game structure

        Returns:
            GameValidationResult with validation status and any missing fields
        """
        missing = [field for field in self.required_fields if field not in game_data]

        if missing:
            return GameValidationResult(
                valid=False,
                error=f"Missing required fields: {', '.join(missing)}",
                missing_fields=missing,
            )

        # Validate content
        words = game_data.get("words", [])
        min_words = self.quality_thresholds["word_count"][0]

        if not words or len(words) < min_words:
            return GameValidationResult(
                valid=False, error=f"Game must contain at least {min_words} words"
            )

        # Validate game type
        game_type = game_data.get("type")
        valid_type_values = [gt.value for gt in self.valid_game_types]

        if game_type not in valid_type_values:
            return GameValidationResult(
                valid=False,
                error=f"Invalid game type. Must be one of: {', '.join(valid_type_values)}",
            )

        return GameValidationResult(valid=True, message="Game structure is valid")

    def check_content_quality(
        self, title: str, words: list[str], instructions: str
    ) -> QualityResult:
        """
        Check content quality metrics for a game.

        Args:
            title: Game title
            words: List of words in the game
            instructions: Game instructions text

        Returns:
            QualityResult with quality metrics and identified issues
        """
        quality_issues = []

        # Check title
        title_min, title_max = self.quality_thresholds["title_length"]
        if not title or len(title) < title_min:
            quality_issues.append(f"Title must be at least {title_min} characters")
        if len(title) > title_max:
            quality_issues.append(f"Title must be {title_max} characters or less")

        # Check words
        word_min, word_max = self.quality_thresholds["word_count"]
        if len(words) < word_min:
            quality_issues.append(f"Game must contain at least {word_min} words")
        if len(words) > word_max:
            quality_issues.append(f"Game should not exceed {word_max} words")

        # Check instructions
        instr_min, instr_max = self.quality_thresholds["instructions_length"]
        if not instructions or len(instructions) < instr_min:
            quality_issues.append(
                f"Instructions must be at least {instr_min} characters"
            )
        if len(instructions) > instr_max:
            quality_issues.append(
                f"Instructions should not exceed {instr_max} characters"
            )

        # Calculate quality score
        quality_score = 100
        if quality_issues:
            quality_score = max(0, 100 - (len(quality_issues) * 20))

        return QualityResult(
            valid=len(quality_issues) == 0,
            quality_score=quality_score,
            issues=quality_issues,
            total_issues=len(quality_issues),
        )

    def validate_theme_consistency(
        self, theme: str, words: list[str], description: str
    ) -> ThemeConsistencyResult:
        """
        Validate that words and description match the game theme.

        Args:
            theme: The game theme
            words: List of words in the game
            description: Game description

        Returns:
            ThemeConsistencyResult with consistency validation
        """
        if not theme:
            return ThemeConsistencyResult(
                valid=False,
                theme="",
                theme_mentioned_in_description=False,
                word_count=0,
                consistency_score=0,
                error="Theme cannot be empty",
            )

        if not words:
            return ThemeConsistencyResult(
                valid=False,
                theme=theme,
                theme_mentioned_in_description=False,
                word_count=0,
                consistency_score=0,
                error="Word list cannot be empty",
            )

        # Simple check: theme should be mentioned or related to words
        theme_lower = theme.lower()
        description_lower = description.lower()

        theme_presence = theme_lower in description_lower
        word_count = len(words)

        return ThemeConsistencyResult(
            valid=True,
            theme=theme,
            theme_mentioned_in_description=theme_presence,
            word_count=word_count,
            consistency_score=85 if theme_presence else 70,
        )

    def add_game_type(self, game_type: GameType) -> None:
        """Add a new supported game type."""
        if game_type not in self.valid_game_types:
            self.valid_game_types.append(game_type)

    def update_quality_threshold(self, metric: str, min_val: int, max_val: int) -> None:
        """Update quality threshold for a specific metric."""
        self.quality_thresholds[metric] = (min_val, max_val)

    def get_configuration(self) -> dict[str, Any]:
        """Get current validator configuration."""
        return {
            "required_fields": self.required_fields.copy(),
            "valid_game_types": [gt.value for gt in self.valid_game_types],
            "quality_thresholds": self.quality_thresholds.copy(),
        }


class ContentValidator(BaseGameValidator):
    """Specialized validator focused on content quality."""

    def __init__(self, strict_mode: bool = False) -> None:
        """
        Initialize content validator.

        Args:
            strict_mode: Whether to apply stricter validation rules
        """
        self.strict_mode = strict_mode
        self._game_validator = GameValidator()

    def validate_game_completion(
        self, game_data: dict[str, Any]
    ) -> GameValidationResult:
        """Delegate to GameValidator."""
        return self._game_validator.validate_game_completion(game_data)

    def check_content_quality(
        self, title: str, words: list[str], instructions: str
    ) -> QualityResult:
        """Enhanced content quality checking with strict mode support."""
        result = self._game_validator.check_content_quality(title, words, instructions)

        if self.strict_mode and result.quality_score < 90:
            # Apply stricter rules in strict mode
            additional_issues = []

            # More stringent title checks
            if len(title) < 5:
                additional_issues.append(
                    "Title should be at least 5 characters in strict mode"
                )

            # Word diversity check
            unique_words = {word.lower() for word in words}
            if len(unique_words) != len(words):
                additional_issues.append("All words must be unique in strict mode")

            if additional_issues:
                result.issues.extend(additional_issues)
                result.total_issues += len(additional_issues)
                result.quality_score = max(
                    0, result.quality_score - (len(additional_issues) * 10)
                )
                result.valid = result.quality_score >= 80

        return result

    def validate_theme_consistency(
        self, theme: str, words: list[str], description: str
    ) -> ThemeConsistencyResult:
        """Delegate to GameValidator."""
        return self._game_validator.validate_theme_consistency(
            theme, words, description
        )


# Create singleton instances for backward compatibility
_default_game_validator = GameValidator()
_default_content_validator = ContentValidator()


# Backward compatibility function wrappers
def validate_game_completion(game_data: dict[str, Any]) -> dict[str, Any]:
    """Backward compatibility wrapper for GameValidator.validate_game_completion."""
    result = _default_game_validator.validate_game_completion(game_data)
    return {
        "valid": result.valid,
        "message": result.message,
        "error": result.error,
        "missing_fields": result.missing_fields,
    }


def check_content_quality(
    title: str, words: list[str], instructions: str
) -> dict[str, Any]:
    """Backward compatibility wrapper for GameValidator.check_content_quality."""
    result = _default_game_validator.check_content_quality(title, words, instructions)
    return {
        "valid": result.valid,
        "quality_score": result.quality_score,
        "issues": result.issues,
        "total_issues": result.total_issues,
    }


def validate_theme_consistency(
    theme: str, words: list[str], description: str
) -> dict[str, Any]:
    """Backward compatibility wrapper for GameValidator.validate_theme_consistency."""
    result = _default_game_validator.validate_theme_consistency(
        theme, words, description
    )
    return {
        "valid": result.valid,
        "theme": result.theme,
        "theme_mentioned_in_description": result.theme_mentioned_in_description,
        "word_count": result.word_count,
        "consistency_score": result.consistency_score,
        "error": result.error,
    }


# Create FunctionTools for export
validate_game_completion_tool = FunctionTool(validate_game_completion)
check_content_quality_tool = FunctionTool(check_content_quality)
validate_theme_consistency_tool = FunctionTool(validate_theme_consistency)
