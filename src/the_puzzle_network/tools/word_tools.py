"""Word operation tools for game generation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from google.adk.tools import FunctionTool


class DifficultyLevel(Enum):
    """Enumeration of word difficulty levels."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class ValidationResult:
    """Result of word validation."""

    valid: bool
    word: str | None = None
    length: int | None = None
    error: str | None = None


@dataclass
class DifficultyResult:
    """Result of difficulty analysis."""

    word: str
    difficulty: DifficultyLevel
    score: float
    vowels: int
    consonants: int
    length: int


@dataclass
class VarietyResult:
    """Result of word variety analysis."""

    valid: bool
    total_words: int
    unique_words: int
    difficulty_distribution: dict[str, int] | None = None
    error: str | None = None
    duplicate_count: int | None = None


class BaseWordAnalyzer(ABC):
    """Abstract base class for word analysis operations."""

    @abstractmethod
    def validate_word(self, word: str) -> ValidationResult:
        """Validate a single word."""
        pass

    @abstractmethod
    def calculate_difficulty(self, word: str) -> DifficultyResult:
        """Calculate difficulty level for a word."""
        pass

    @abstractmethod
    def check_word_variety(self, words: list[str]) -> VarietyResult:
        """Check variety and uniqueness in a word list."""
        pass


class WordAnalyzer(BaseWordAnalyzer):
    """Comprehensive word analysis and validation."""

    def __init__(
        self,
        min_length: int = 3,
        max_length: int = 20,
        vowel_set: str = "aeiou",
        difficulty_thresholds: tuple[float, float] = (30.0, 60.0),
    ) -> None:
        """
        Initialize word analyzer with configurable parameters.

        Args:
            min_length: Minimum allowed word length
            max_length: Maximum allowed word length
            vowel_set: Characters considered vowels
            difficulty_thresholds: (easy_max, medium_max) score thresholds
        """
        self.min_length = min_length
        self.max_length = max_length
        self.vowel_set = set(vowel_set.lower())
        self.easy_threshold, self.medium_threshold = difficulty_thresholds

    def validate_word(self, word: str) -> ValidationResult:
        """
        Validate a word for use in games.

        Checks word length, character composition, and basic validity.

        Args:
            word: The word to validate

        Returns:
            ValidationResult with validation status and any error messages
        """
        cleaned_word = word.strip().lower()

        if not cleaned_word:
            return ValidationResult(valid=False, error="Word cannot be empty")

        if len(cleaned_word) < self.min_length:
            return ValidationResult(
                valid=False, error=f"Word must be at least {self.min_length} characters"
            )

        if len(cleaned_word) > self.max_length:
            return ValidationResult(
                valid=False, error=f"Word must be {self.max_length} characters or less"
            )

        if not cleaned_word.isalpha():
            return ValidationResult(valid=False, error="Word must contain only letters")

        return ValidationResult(valid=True, word=cleaned_word, length=len(cleaned_word))

    def calculate_difficulty(self, word: str) -> DifficultyResult:
        """
        Calculate difficulty level for a word.

        Returns difficulty based on length and consonant/vowel ratio.

        Args:
            word: The word to analyze

        Returns:
            DifficultyResult with difficulty level and analysis metrics
        """
        cleaned_word = word.lower()
        vowels = sum(1 for c in cleaned_word if c in self.vowel_set)
        consonants = len(cleaned_word) - vowels

        # Calculate difficulty score
        length_score = len(cleaned_word) / self.max_length  # Normalized to 0-1
        ratio_score = (
            abs(vowels - consonants) / len(cleaned_word) if cleaned_word else 0
        )

        score = (length_score * 0.6 + ratio_score * 0.4) * 100

        if score < self.easy_threshold:
            difficulty = DifficultyLevel.EASY
        elif score < self.medium_threshold:
            difficulty = DifficultyLevel.MEDIUM
        else:
            difficulty = DifficultyLevel.HARD

        return DifficultyResult(
            word=cleaned_word,
            difficulty=difficulty,
            score=round(score, 2),
            vowels=vowels,
            consonants=consonants,
            length=len(cleaned_word),
        )

    def check_word_variety(self, words: list[str]) -> VarietyResult:
        """
        Check variety and uniqueness in a list of words.

        Args:
            words: List of words to analyze

        Returns:
            VarietyResult with variety metrics
        """
        if not words:
            return VarietyResult(
                valid=False, total_words=0, unique_words=0, error="Word list is empty"
            )

        unique_words = {w.lower() for w in words}

        if len(unique_words) != len(words):
            duplicates = len(words) - len(unique_words)
            return VarietyResult(
                valid=False,
                total_words=len(words),
                unique_words=len(unique_words),
                error=f"Found {duplicates} duplicate word(s)",
                duplicate_count=duplicates,
            )

        # Check variety in difficulty
        difficulties = [self.calculate_difficulty(w).difficulty.value for w in words]
        difficulty_distribution = {
            "easy": difficulties.count("easy"),
            "medium": difficulties.count("medium"),
            "hard": difficulties.count("hard"),
        }

        return VarietyResult(
            valid=True,
            total_words=len(words),
            unique_words=len(unique_words),
            difficulty_distribution=difficulty_distribution,
        )

    def get_configuration(self) -> dict[str, Any]:
        """Get current analyzer configuration."""
        return {
            "min_length": self.min_length,
            "max_length": self.max_length,
            "vowel_set": "".join(sorted(self.vowel_set)),
            "easy_threshold": self.easy_threshold,
            "medium_threshold": self.medium_threshold,
        }


# Create singleton instance for backward compatibility
_default_analyzer = WordAnalyzer()


# Backward compatibility function wrappers
def validate_word(word: str) -> dict[str, Any]:
    """Backward compatibility wrapper for WordAnalyzer.validate_word."""
    result = _default_analyzer.validate_word(word)
    return {
        "valid": result.valid,
        "word": result.word,
        "length": result.length,
        "error": result.error,
    }


def calculate_difficulty(word: str) -> dict[str, Any]:
    """Backward compatibility wrapper for WordAnalyzer.calculate_difficulty."""
    result = _default_analyzer.calculate_difficulty(word)
    return {
        "word": result.word,
        "difficulty": result.difficulty.value,
        "score": result.score,
        "vowels": result.vowels,
        "consonants": result.consonants,
        "length": result.length,
    }


def check_word_variety(words: list[str]) -> dict[str, Any]:
    """Backward compatibility wrapper for WordAnalyzer.check_word_variety."""
    result = _default_analyzer.check_word_variety(words)
    return {
        "valid": result.valid,
        "total_words": result.total_words,
        "unique_words": result.unique_words,
        "difficulty_distribution": result.difficulty_distribution,
        "error": result.error,
        "duplicate_count": result.duplicate_count,
    }


# Create FunctionTools for export
validate_word_tool = FunctionTool(validate_word)
calculate_difficulty_tool = FunctionTool(calculate_difficulty)
check_word_variety_tool = FunctionTool(check_word_variety)
