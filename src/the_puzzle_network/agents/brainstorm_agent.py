"""Brainstorm agent for generating game ideas and concepts."""

from dataclasses import dataclass
from typing import Any, cast

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool

from ..tools.validation_tools import GameType
from ..tools.word_tools import (
    calculate_difficulty_tool,
    check_word_variety_tool,
    validate_word_tool,
)
from .base_agent import (
    AgentConfig,
    AgentResult,
    AgentRole,
    BasePuzzleAgent,
    ProcessingStage,
)


@dataclass
class ConceptResult:
    """Result of concept generation."""

    theme: str
    game_type: GameType
    initial_words: list[str]
    concept_score: float
    reasoning: str


class BrainstormAgent(BasePuzzleAgent):
    """Specialized agent for creative game concept generation."""

    def __init__(
        self,
        config: AgentConfig | None = None,
        creativity_factor: float = 0.8,
        target_word_count: tuple[int, int] = (5, 10),
    ) -> None:
        """
        Initialize brainstorm agent.

        Args:
            config: Agent configuration
            creativity_factor: Factor for creativity vs. safety (0-1)
            target_word_count: (min, max) words for initial lists
        """
        self.creativity_factor = creativity_factor
        self.target_word_count = target_word_count

        super().__init__(
            name="brainstorm_agent",
            role=AgentRole.BRAINSTORM,
            config=config,
        )

    def _create_llm_agent(self) -> LlmAgent:
        """Create the brainstorm LlmAgent."""
        return LlmAgent(
            model=self.config.model,
            name=self.name,
            description="Generates creative game concepts, themes, and initial word lists",
            instruction=self._get_instruction(),
            tools=cast(list, self.get_required_tools()),
            output_key="brainstorm_result",
        )

    def _get_instruction(self) -> str:
        """Get brainstorm agent instruction template."""
        min_words, max_words = self.target_word_count

        return f"""You are the Brainstorm Agent for The Puzzle Network.

Your role is to generate creative and engaging word game ideas.

RESPONSIBILITIES:
1. Generate innovative game themes and concepts
2. Suggest game types (word search, crossword, anagram, word match, trivia)
3. Create initial word lists that fit the theme
4. Ensure word variety and appropriate difficulty distribution
5. Use available tools to validate and assess words

GUIDELINES:
- Themes should be specific and interesting (e.g., "Ocean Animals", "Summer Activities", "Kitchen Tools")
- Initial word lists should have {min_words}-{max_words} words for variety
- Mix difficulty levels (easy, medium, hard)
- Use the calculate_difficulty tool to assess each word
- Use the check_word_variety tool to validate your word selection

CREATIVITY FACTOR: {self.creativity_factor:.1f} (0.0 = safe/common themes, 1.0 = highly creative/unusual themes)

OUTPUT:
- Clearly state the game theme
- List the proposed game type
- Provide the selected words
- Explain why these words work well together
- Note the difficulty distribution

Save your final recommendations to context state with key "brainstorm_result" so next agents can use them."""

    def get_required_tools(self) -> list[BaseTool]:
        """Get required tools for brainstorming."""
        return [validate_word_tool, calculate_difficulty_tool, check_word_variety_tool]

    def validate_context(self, context: dict[str, Any]) -> bool:
        """Validate brainstorm context (minimal requirements)."""
        return True  # Brainstorm is typically the first stage

    def process_request(self, request: str, context: dict[str, Any]) -> AgentResult:
        """Process brainstorm request."""
        # Extract key requirements from request
        theme_keywords = self._extract_theme_keywords(request)

        return AgentResult(
            success=True,
            stage=ProcessingStage.CONCEPT_GENERATION,
            data={
                "request": request,
                "theme_keywords": theme_keywords,
                "creativity_factor": self.creativity_factor,
                "target_word_count": self.target_word_count,
            },
        )

    def _extract_theme_keywords(self, request: str) -> list[str]:
        """Extract potential theme keywords from request."""
        # Simple keyword extraction (could be enhanced with NLP)
        common_themes = [
            "animals",
            "ocean",
            "space",
            "food",
            "sports",
            "travel",
            "music",
            "art",
            "science",
            "nature",
            "technology",
            "history",
        ]

        request_lower = request.lower()
        found_themes = [theme for theme in common_themes if theme in request_lower]

        return found_themes

    def generate_concept(self, theme: str, game_type: GameType) -> ConceptResult:
        """Generate a complete game concept."""
        # This would typically be implemented with more sophisticated logic
        initial_words: list[str] = []  # Would be generated based on theme

        return ConceptResult(
            theme=theme,
            game_type=game_type,
            initial_words=initial_words,
            concept_score=75.0,  # Would be calculated
            reasoning=f"Generated concept for {theme} themed {game_type.value} game",
        )

    def evaluate_concept_creativity(self, concept: ConceptResult) -> float:
        """Evaluate creativity score of a concept."""
        # Implement creativity scoring algorithm
        base_score = 50.0

        # Theme uniqueness factor
        theme_uniqueness = (
            len(concept.theme.split()) * 10
        )  # More specific = more creative

        # Word variety factor
        word_variety = len(set(concept.initial_words)) * 5

        creativity_score = base_score + theme_uniqueness + word_variety
        return min(100.0, creativity_score)

    def get_creativity_configuration(self) -> dict[str, Any]:
        """Get creativity-specific configuration."""
        return {
            **self.get_configuration(),
            "creativity_factor": self.creativity_factor,
            "target_word_count": self.target_word_count,
        }


# Create default brainstorm agent instance for backward compatibility
brainstorm_agent_instance = BrainstormAgent()
brainstorm_agent = brainstorm_agent_instance.get_llm_agent()
