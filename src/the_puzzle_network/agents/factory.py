"""Factory classes and functions for creating agent networks and configurations."""

from .base_agent import AgentConfig, BasePuzzleAgent, CoordinatorAgent
from .brainstorm_agent import BrainstormAgent
from .game_builder_agent import GameBuilderAgent
from .word_picker_agent import WordPickerAgent


class AgentNetworkFactory:
    """Factory for creating and configuring agent networks."""

    @staticmethod
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

    @staticmethod
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
        agents = AgentNetworkFactory.create_agent_network(config)
        sub_agents = list(agents.values())

        return CoordinatorAgent(sub_agents=sub_agents, config=config)

    @classmethod
    def create_custom_network(
        cls,
        agent_configs: dict[str, AgentConfig] | None = None,
        default_config: AgentConfig | None = None,
    ) -> dict[str, BasePuzzleAgent]:
        """
        Create a custom network with individual agent configurations.

        Args:
            agent_configs: Individual configurations for specific agents
            default_config: Default configuration for agents not specified

        Returns:
            Dictionary mapping agent names to configured instances
        """
        agent_configs = agent_configs or {}
        default_config = default_config or AgentConfig()

        return {
            "brainstorm": BrainstormAgent(
                config=agent_configs.get("brainstorm", default_config)
            ),
            "word_picker": WordPickerAgent(
                config=agent_configs.get("word_picker", default_config)
            ),
            "game_builder": GameBuilderAgent(
                config=agent_configs.get("game_builder", default_config)
            ),
        }


# Convenience functions for backward compatibility
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
    return AgentNetworkFactory.create_agent_network(config)


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
    return AgentNetworkFactory.create_coordinator_with_network(config)
