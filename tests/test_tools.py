"""Basic tests for tools module."""

import pytest

from the_puzzle_network.tools.validation_tools import (
    check_content_quality,
    validate_game_completion,
)
from the_puzzle_network.tools.word_tools import (
    calculate_difficulty,
    check_word_variety,
    validate_word,
)


class TestWordTools:
    """Tests for word validation and difficulty calculation."""

    def test_validate_word_valid(self):
        """Test validation of a valid word."""
        result = validate_word("python")
        assert result["valid"] is True
        assert result["word"] == "python"
        assert result["length"] == 6

    def test_validate_word_too_short(self):
        """Test rejection of too short words."""
        result = validate_word("ab")
        assert result["valid"] is False
        assert "at least 3" in result["error"]

    def test_validate_word_too_long(self):
        """Test rejection of too long words."""
        result = validate_word("a" * 25)
        assert result["valid"] is False
        assert "20 characters" in result["error"]

    def test_validate_word_with_numbers(self):
        """Test rejection of words with numbers."""
        result = validate_word("word123")
        assert result["valid"] is False
        assert "only letters" in result["error"]

    def test_calculate_difficulty_easy(self):
        """Test difficulty calculation for easy word."""
        result = calculate_difficulty("cat")
        assert result["word"] == "cat"
        assert result["difficulty"] == "easy"
        assert result["length"] == 3

    def test_calculate_difficulty_hard(self):
        """Test difficulty calculation for hard word."""
        result = calculate_difficulty("extraordinary")
        assert result["difficulty"] == "hard"
        assert result["length"] == 13

    def test_check_word_variety_unique(self):
        """Test variety check with unique words."""
        words = ["apple", "banana", "cherry"]
        result = check_word_variety(words)
        assert result["valid"] is True
        assert result["unique_words"] == 3

    def test_check_word_variety_duplicates(self):
        """Test variety check with duplicate words."""
        words = ["apple", "banana", "apple"]
        result = check_word_variety(words)
        assert result["valid"] is False
        assert result["duplicate_count"] == 1


class TestValidationTools:
    """Tests for game validation tools."""

    def test_validate_game_completion_valid(self):
        """Test validation of complete game."""
        game = {
            "type": "crossword",
            "title": "Test Game",
            "words": ["apple", "banana"],
            "difficulty": "medium",
        }
        result = validate_game_completion(game)
        assert result["valid"] is True

    def test_validate_game_completion_missing_fields(self):
        """Test validation with missing required fields."""
        game = {"type": "crossword"}
        result = validate_game_completion(game)
        assert result["valid"] is False
        assert "Missing required fields" in result["error"]

    def test_validate_game_completion_too_few_words(self):
        """Test validation with too few words."""
        game = {
            "type": "crossword",
            "title": "Test",
            "words": ["apple"],
            "difficulty": "easy",
        }
        result = validate_game_completion(game)
        assert result["valid"] is False

    def test_check_content_quality_good(self):
        """Test content quality check for good content."""
        result = check_content_quality(
            title="Fruit Game",
            words=["apple", "banana", "cherry"],
            instructions="Find all the fruits in the puzzle",
        )
        assert result["valid"] is True
        assert result["quality_score"] >= 80

    def test_check_content_quality_short_title(self):
        """Test content quality with short title."""
        result = check_content_quality(
            title="a",
            words=["apple", "banana", "cherry"],
            instructions="Find all the fruits",
        )
        assert result["valid"] is False
        assert len(result["issues"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
