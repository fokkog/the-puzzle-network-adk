"""The Puzzle Network - Multi-agent word game generation system."""

from .agents import (
    AgentConfig,
    BasePuzzleAgent,
    BrainstormAgent,
    CoordinatorAgent,
    GameBuilderAgent,
    WordPickerAgent,
    create_agent_network,
    create_coordinator_with_network,
)
from .main import GameGenerationPipeline, GameGenerationService, GameRequest
from .tools import (
    AnswerKeyFormatter,
    ClueFormatter,
    DifficultyLevel,
    GameFormatter,
    GameType,
    GameValidator,
    WordAnalyzer,
)


__version__ = "0.1.0"
__author__ = "The Puzzle Network Team"

__all__ = [
    # Main service classes
    "GameGenerationService",
    "GameGenerationPipeline",
    "GameRequest",
    # Agent classes
    "BasePuzzleAgent",
    "BrainstormAgent",
    "WordPickerAgent",
    "GameBuilderAgent",
    "CoordinatorAgent",
    "AgentConfig",
    # Tool classes
    "WordAnalyzer",
    "GameValidator",
    "GameFormatter",
    "ClueFormatter",
    "AnswerKeyFormatter",
    # Enums and types
    "DifficultyLevel",
    "GameType",
    # Factory functions
    "create_agent_network",
    "create_coordinator_with_network",
]


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
