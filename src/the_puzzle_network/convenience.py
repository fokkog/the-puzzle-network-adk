"""Convenience utilities for The Puzzle Network package."""

from .main import GameGenerationService


def create_default_service() -> GameGenerationService:
    """Create a GameGenerationService with default configuration."""
    return GameGenerationService()


async def generate_game(request_text: str) -> dict:
    """
    Quick utility function to generate a game from text.

    Args:
        request_text: Natural language game generation request

    Returns:
        Game generation result dictionary
    """
    service = create_default_service()
    return await service.generate_game(request_text)
