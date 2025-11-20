"""Base classes and utilities for puzzle network agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, cast

from google.adk.agents import BaseAgent, LlmAgent
from google.adk.tools import BaseTool

from ..tools.format_tools import GameFormatter
from ..tools.validation_tools import GameValidator
from ..tools.word_tools import WordAnalyzer


class AgentRole(Enum):
    """Enumeration of agent roles in the puzzle network."""

    COORDINATOR = "coordinator"
    BRAINSTORM = "brainstorm"
    WORD_PICKER = "word_picker"
    GAME_BUILDER = "game_builder"


class ProcessingStage(Enum):
    """Enumeration of processing stages."""

    CONCEPT_GENERATION = "concept_generation"
    WORD_SELECTION = "word_selection"
    GAME_ASSEMBLY = "game_assembly"
    QUALITY_VALIDATION = "quality_validation"


@dataclass
class AgentConfig:
    """Configuration for puzzle network agents."""

    model: str = "gemini-2.5-flash"
    max_retries: int = 3
    quality_threshold: float = 80.0
    enable_validation: bool = True


@dataclass
class AgentResult:
    """Standard result format for agent operations."""

    success: bool
    stage: ProcessingStage
    data: dict[str, Any]
    quality_score: float | None = None
    errors: list[str] | None = None
    warnings: list[str] | None = None


class BasePuzzleAgent(ABC):
    """Abstract base class for all puzzle network agents."""

    def __init__(
        self,
        name: str,
        role: AgentRole,
        config: AgentConfig | None = None,
        word_analyzer: WordAnalyzer | None = None,
        game_validator: GameValidator | None = None,
        game_formatter: GameFormatter | None = None,
    ) -> None:
        """
        Initialize base puzzle agent.

        Args:
            name: Agent name/identifier
            role: Agent role in the network
            config: Agent configuration
            word_analyzer: Word analysis tool instance
            game_validator: Game validation tool instance
            game_formatter: Game formatting tool instance
        """
        self.name = name
        self.role = role
        self.config = config or AgentConfig()
        self.word_analyzer = word_analyzer or WordAnalyzer()
        self.game_validator = game_validator or GameValidator()
        self.game_formatter = game_formatter or GameFormatter()

        # Initialize the underlying LlmAgent
        self._llm_agent = self._create_llm_agent()

    @abstractmethod
    def _create_llm_agent(self) -> LlmAgent:
        """Create the underlying LlmAgent instance."""
        pass

    @abstractmethod
    def get_required_tools(self) -> list[BaseTool]:
        """Get list of required tools for this agent."""
        pass

    @abstractmethod
    def validate_context(self, context: dict[str, Any]) -> bool:
        """Validate that context contains required data for processing."""
        pass

    @abstractmethod
    def process_request(self, request: str, context: dict[str, Any]) -> AgentResult:
        """Process a request with given context."""
        pass

    def get_llm_agent(self) -> LlmAgent:
        """Get the underlying LlmAgent for use in workflows."""
        return self._llm_agent

    def get_stage(self) -> ProcessingStage:
        """Get the primary processing stage for this agent."""
        stage_mapping = {
            AgentRole.BRAINSTORM: ProcessingStage.CONCEPT_GENERATION,
            AgentRole.WORD_PICKER: ProcessingStage.WORD_SELECTION,
            AgentRole.GAME_BUILDER: ProcessingStage.GAME_ASSEMBLY,
            AgentRole.COORDINATOR: ProcessingStage.QUALITY_VALIDATION,
        }
        return stage_mapping.get(self.role, ProcessingStage.CONCEPT_GENERATION)

    def validate_output_quality(self, result: AgentResult) -> bool:
        """Validate that agent output meets quality standards."""
        if not result.success:
            return False

        if result.quality_score is not None:
            return result.quality_score >= self.config.quality_threshold

        return True

    def get_configuration(self) -> dict[str, Any]:
        """Get agent configuration for debugging/monitoring."""
        return {
            "name": self.name,
            "role": self.role.value,
            "stage": self.get_stage().value,
            "model": self.config.model,
            "quality_threshold": self.config.quality_threshold,
            "validation_enabled": self.config.enable_validation,
        }


class CoordinatorAgent(BasePuzzleAgent):
    """Enhanced coordinator agent with better orchestration capabilities."""

    def __init__(
        self,
        sub_agents: list[BasePuzzleAgent] | None = None,
        config: AgentConfig | None = None,
    ) -> None:
        """
        Initialize coordinator agent.

        Args:
            sub_agents: List of agents to coordinate
            config: Agent configuration
        """
        self.sub_agents = sub_agents or []
        super().__init__(
            name="coordinator",
            role=AgentRole.COORDINATOR,
            config=config,
        )

    def _create_llm_agent(self) -> LlmAgent:
        """Create the coordinator LlmAgent."""
        # Get sub-agent LlmAgent instances
        sub_llm_agents = [agent.get_llm_agent() for agent in self.sub_agents]

        return LlmAgent(
            model=self.config.model,
            name=self.name,
            description="Main orchestrator for word game generation pipeline",
            instruction=self._get_instruction(),
            sub_agents=cast(list[BaseAgent], sub_llm_agents),
        )

    def _get_instruction(self) -> str:
        """Get coordinator instruction template."""
        return """You are the Puzzle Network Game Generator Coordinator.

Your role is to guide the creation of engaging word games through a multi-stage process.

WORKFLOW:
1. First, you receive a request to create a word game
2. Delegate to the brainstorm_agent to generate creative game concepts and ideas
3. Delegate to the word_picker_agent to select appropriate words based on difficulty and theme
4. Delegate to the game_builder_agent to assemble the final polished game

RESPONSIBILITIES:
- Ensure each stage is completed successfully
- Pass results between agents through the workflow
- Validate the final game meets quality standards
- Provide clear feedback on the generation process

Keep the workflow moving smoothly by maintaining context and ensuring clear communication between agents."""

    def get_required_tools(self) -> list[BaseTool]:
        """Coordinator typically doesn't use tools directly."""
        return []

    def validate_context(self, context: dict[str, Any]) -> bool:
        """Validate coordinator context."""
        return True  # Coordinator is the entry point

    def process_request(self, request: str, context: dict[str, Any]) -> AgentResult:
        """Process coordination request."""
        return AgentResult(
            success=True,
            stage=self.get_stage(),
            data={"request": request, "context": context},
        )

    def add_sub_agent(self, agent: BasePuzzleAgent) -> None:
        """Add a sub-agent to coordination."""
        self.sub_agents.append(agent)
        # Recreate LlmAgent with updated sub-agents
        self._llm_agent = self._create_llm_agent()


def create_coordinator_agent(
    sub_agents: list[BasePuzzleAgent] | None = None,
    config: AgentConfig | None = None,
) -> CoordinatorAgent:
    """
    Create enhanced coordinator agent.

    Args:
        sub_agents: List of agents to coordinate
        config: Agent configuration

    Returns:
        CoordinatorAgent instance
    """
    return CoordinatorAgent(sub_agents=sub_agents, config=config)
