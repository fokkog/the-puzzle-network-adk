"""Agents module - enhanced class-based agents for the puzzle network."""

# Import new class-based agents
from .base_agent import (
    AgentConfig,
    AgentResult,
    AgentRole,
    BasePuzzleAgent,
    CoordinatorAgent,
    ProcessingStage,
    create_coordinator_agent,
)
from .brainstorm_agent import BrainstormAgent, brainstorm_agent
from .game_builder_agent import GameBuilderAgent, game_builder_agent
from .word_picker_agent import WordPickerAgent, word_picker_agent


__all__ = [
    # New class-based agents
    "BasePuzzleAgent",
    "BrainstormAgent",
    "WordPickerAgent",
    "GameBuilderAgent",
    "CoordinatorAgent",
    # Configuration and data classes
    "AgentConfig",
    "AgentResult",
    "AgentRole",
    "ProcessingStage",
    # Factory functions
    "create_coordinator_agent",
    # Backward compatibility - LlmAgent instances
    "brainstorm_agent",
    "word_picker_agent",
    "game_builder_agent",
]


def create_agent_network(
    config: AgentConfig | None = None,
) -> dict[str, BasePuzzleAgent]:
    """
    Create a complete network of puzzle agents.

    Args:
        config: Shared configuration for all agents

    Returns:
        Dictionary mapping agent names to instances
    """
    shared_config = config or AgentConfig()

    return {
        "brainstorm": BrainstormAgent(config=shared_config),
        "word_picker": WordPickerAgent(config=shared_config),
        "game_builder": GameBuilderAgent(config=shared_config),
    }


def create_coordinator_with_network(
    config: AgentConfig | None = None,
) -> CoordinatorAgent:
    """
    Create coordinator with a complete agent network.

    Args:
        config: Configuration for all agents

    Returns:
        Configured CoordinatorAgent with sub-agents
    """
    agents = create_agent_network(config)
    sub_agents = list(agents.values())

    return CoordinatorAgent(sub_agents=sub_agents, config=config)
