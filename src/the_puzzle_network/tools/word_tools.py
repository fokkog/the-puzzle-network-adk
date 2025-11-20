"""Word operation tools for game generation."""

from google.adk.tools import FunctionTool


def validate_word(word: str) -> dict:
    """
    Validate a word for use in games.

    Checks word length, character composition, and basic validity.

    Args:
        word: The word to validate

    Returns:
        Dictionary with validation result and any error messages
    """
    word = word.strip().lower()

    if not word:
        return {"valid": False, "error": "Word cannot be empty"}

    if len(word) < 3:
        return {"valid": False, "error": "Word must be at least 3 characters"}

    if len(word) > 20:
        return {"valid": False, "error": "Word must be 20 characters or less"}

    if not word.isalpha():
        return {"valid": False, "error": "Word must contain only letters"}

    return {"valid": True, "word": word, "length": len(word)}


def calculate_difficulty(word: str) -> dict:
    """
    Calculate difficulty level for a word.

    Returns difficulty based on length and consonant/vowel ratio.

    Args:
        word: The word to analyze

    Returns:
        Dictionary with difficulty level (easy, medium, hard) and score
    """
    word = word.lower()
    vowels = sum(1 for c in word if c in "aeiou")
    consonants = len(word) - vowels

    # Calculate difficulty score
    length_score = len(word) / 20.0  # Normalized to 0-1
    ratio_score = abs(vowels - consonants) / len(word) if word else 0

    score = (length_score * 0.6 + ratio_score * 0.4) * 100

    if score < 30:
        difficulty = "easy"
    elif score < 60:
        difficulty = "medium"
    else:
        difficulty = "hard"

    return {
        "word": word,
        "difficulty": difficulty,
        "score": round(score, 2),
        "vowels": vowels,
        "consonants": consonants,
        "length": len(word),
    }


def check_word_variety(words: list[str]) -> dict:
    """
    Check variety and uniqueness in a list of words.

    Args:
        words: List of words to analyze

    Returns:
        Dictionary with variety metrics
    """
    if not words:
        return {"valid": False, "error": "Word list is empty"}

    unique_words = {w.lower() for w in words}

    if len(unique_words) != len(words):
        duplicates = len(words) - len(unique_words)
        return {
            "valid": False,
            "error": f"Found {duplicates} duplicate word(s)",
            "duplicate_count": duplicates,
        }

    # Check variety in difficulty
    difficulties = [calculate_difficulty(w)["difficulty"] for w in words]
    difficulty_distribution = {
        "easy": difficulties.count("easy"),
        "medium": difficulties.count("medium"),
        "hard": difficulties.count("hard"),
    }

    return {
        "valid": True,
        "total_words": len(words),
        "unique_words": len(unique_words),
        "difficulty_distribution": difficulty_distribution,
    }


# Create FunctionTools for export
validate_word_tool = FunctionTool(validate_word)
calculate_difficulty_tool = FunctionTool(calculate_difficulty)
check_word_variety_tool = FunctionTool(check_word_variety)
