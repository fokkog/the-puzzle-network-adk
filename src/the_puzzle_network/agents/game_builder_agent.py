"""Game builder agent for assembling the final game product."""

from dataclasses import dataclass
from typing import Any, cast

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool

from ..tools.format_tools import (
    format_answer_key_tool,
    format_clue_tool,
    format_game_structure_tool,
)
from ..tools.validation_tools import (
    GameType,
    check_content_quality_tool,
    validate_game_completion_tool,
    validate_theme_consistency_tool,
)
from .base_agent import (
    AgentConfig,
    AgentResult,
    AgentRole,
    BasePuzzleAgent,
    ProcessingStage,
)


@dataclass
class GameContent:
    """Complete game content structure."""

    title: str
    instructions: str
    clues: list[dict[str, Any]]
    answer_key: str
    estimated_time_minutes: int


@dataclass
class GameMetadata:
    """Game metadata information."""

    theme: str
    game_type: GameType
    difficulty: str
    word_count: int
    quality_score: float
    consistency_score: float


@dataclass
class CompleteGame:
    """Complete assembled game with all components."""

    metadata: GameMetadata
    content: GameContent
    formatted_structure: str
    validation_results: dict[str, Any]
    ready_for_publication: bool


class GameBuilderAgent(BasePuzzleAgent):
    """Specialized agent for final game assembly and polish."""

    def __init__(
        self,
        config: AgentConfig | None = None,
        quality_standards: dict[str, float] | None = None,
        format_templates: dict[str, str] | None = None,
    ) -> None:
        """
        Initialize game builder agent.

        Args:
            config: Agent configuration
            quality_standards: Minimum quality thresholds
            format_templates: Custom formatting templates
        """
        self.quality_standards = quality_standards or {
            "content_quality": 80.0,
            "theme_consistency": 75.0,
            "overall_quality": 85.0,
        }
        self.format_templates = format_templates or {}

        super().__init__(
            name="game_builder_agent",
            role=AgentRole.GAME_BUILDER,
            config=config,
        )

        # Initialize separate formatter instances
        from ..tools.format_tools import AnswerKeyFormatter, ClueFormatter

        self.clue_formatter = ClueFormatter()
        self.answer_key_formatter = AnswerKeyFormatter()

    def _create_llm_agent(self) -> LlmAgent:
        """Create the game builder LlmAgent."""
        return LlmAgent(
            model=self.config.model,
            name=self.name,
            description="Assembles the final polished game with instructions, clues, and answer key",
            instruction=self._get_instruction(),
            tools=cast(list, self.get_required_tools()),
            output_key="final_game",
        )

    def _get_instruction(self) -> str:
        """Get game builder agent instruction template."""
        standards = self.quality_standards

        return f"""You are the Game Builder Agent for The Puzzle Network.

Your role is to create the final, polished word game product.

RESPONSIBILITIES:
1. Review brainstorm results and picked words from context
2. Create engaging game title and instructions
3. Generate clues for each word using format_clue_tool
4. Assemble the game structure using format_game_structure_tool
5. Create an answer key using format_answer_key_tool
6. Validate game completion and content quality
7. Ensure theme consistency

QUALITY STANDARDS:
- Game title should be catchy and descriptive (10-50 characters)
- Instructions must be clear and actionable
- Clues should be helpful but not give away answers
- All required fields must be present
- Content quality score should be ≥ {standards["content_quality"]}
- Theme consistency score should be ≥ {standards["theme_consistency"]}
- Overall quality threshold: {standards["overall_quality"]}

WORKFLOW:
1. Read context state: "brainstorm_result" and "picked_words"
2. Create a compelling game title based on the theme
3. Write clear, engaging instructions (2-3 sentences)
4. Generate creative clues for each word using format_clue_tool
5. Structure the game using format_game_structure_tool
6. Create a complete answer key
7. Run quality and completion checks

OUTPUT:
- Formatted game structure (ready for publication)
- Answer key for game masters
- Summary of game components
- Quality assurance report
- Final status (READY or needs revisions)

Save final game to context state with key "final_game" """

    def get_required_tools(self) -> list[BaseTool]:
        """Get required tools for game building."""
        return [
            format_game_structure_tool,
            format_clue_tool,
            format_answer_key_tool,
            validate_game_completion_tool,
            check_content_quality_tool,
            validate_theme_consistency_tool,
        ]

    def validate_context(self, context: dict[str, Any]) -> bool:
        """Validate game builder context."""
        required_keys = ["brainstorm_result", "picked_words"]
        return all(key in context for key in required_keys)

    def process_request(self, request: str, context: dict[str, Any]) -> AgentResult:
        """Process game assembly request."""
        brainstorm_data = context.get("brainstorm_result", {})
        picked_words = context.get("picked_words", [])

        return AgentResult(
            success=True,
            stage=ProcessingStage.GAME_ASSEMBLY,
            data={
                "brainstorm_data": brainstorm_data,
                "picked_words": picked_words,
                "quality_standards": self.quality_standards,
            },
        )

    def assemble_game(
        self, theme: str, game_type: GameType, words: list[str], difficulty: str
    ) -> CompleteGame:
        """Assemble complete game from components."""
        # Generate game content
        title = self._generate_title(theme, game_type)
        instructions = self._generate_instructions(game_type, len(words))
        clues = self._generate_clues(words, theme)

        # Create content structure
        content = GameContent(
            title=title,
            instructions=instructions,
            clues=clues,
            answer_key=self._generate_answer_key(clues),
            estimated_time_minutes=self._estimate_completion_time(words, game_type),
        )

        # Format game structure
        formatted_structure = self.game_formatter.format_game_structure(
            game_type.value, title, words, difficulty
        )

        # Run validation
        validation_results = self._run_validations(content, theme, words)

        # Calculate quality scores
        quality_score = validation_results.get("quality_score", 0)
        consistency_score = validation_results.get("consistency_score", 0)

        # Create metadata
        metadata = GameMetadata(
            theme=theme,
            game_type=game_type,
            difficulty=difficulty,
            word_count=len(words),
            quality_score=quality_score,
            consistency_score=consistency_score,
        )

        # Check if ready for publication
        ready_for_publication = self._meets_quality_standards(validation_results)

        return CompleteGame(
            metadata=metadata,
            content=content,
            formatted_structure=formatted_structure,
            validation_results=validation_results,
            ready_for_publication=ready_for_publication,
        )

    def _generate_title(self, theme: str, game_type: GameType) -> str:
        """Generate engaging game title."""
        template = self.format_templates.get("title", "{theme} {game_type}")

        # Simple title generation - could be enhanced with more creativity
        game_type_names = {
            GameType.WORD_SEARCH: "Word Hunt",
            GameType.CROSSWORD: "Crossword",
            GameType.ANAGRAM: "Anagram Challenge",
            GameType.WORD_MATCH: "Word Match",
            GameType.TRIVIA: "Trivia Quest",
        }

        return template.format(
            theme=theme.title(),
            game_type=game_type_names.get(game_type, game_type.value.title()),
        )

    def _generate_instructions(self, game_type: GameType, word_count: int) -> str:
        """Generate clear game instructions."""
        instructions = {
            GameType.WORD_SEARCH: f"Find all {word_count} hidden words in the grid. Words can be horizontal, vertical, or diagonal.",
            GameType.CROSSWORD: f"Fill in the crossword puzzle using the {word_count} clues provided.",
            GameType.ANAGRAM: f"Unscramble each set of letters to form {word_count} valid words.",
            GameType.WORD_MATCH: f"Match each clue with the correct word from the list of {word_count} options.",
            GameType.TRIVIA: f"Answer all {word_count} trivia questions correctly.",
        }

        return instructions.get(
            game_type, f"Complete the puzzle using all {word_count} words provided."
        )

    def _generate_clues(self, words: list[str], theme: str) -> list[dict[str, Any]]:
        """Generate clues for each word."""
        clues = []

        for word in words:
            # Determine category based on theme and word
            category = self._determine_word_category(word, theme)

            clue_data = self.clue_formatter.format_clue(word, category)
            clues.append(clue_data)

        return clues

    def _generate_answer_key(self, clues: list[dict[str, Any]]) -> str:
        """Generate formatted answer key."""
        return self.answer_key_formatter.format_answer_key(clues)

    def _estimate_completion_time(self, words: list[str], game_type: GameType) -> int:
        """Estimate completion time in minutes."""
        base_time_per_word = {
            GameType.WORD_SEARCH: 1.5,
            GameType.CROSSWORD: 2.0,
            GameType.ANAGRAM: 1.0,
            GameType.WORD_MATCH: 0.5,
            GameType.TRIVIA: 1.0,
        }

        time_factor = base_time_per_word.get(game_type, 1.0)
        estimated_minutes = len(words) * time_factor + 2  # +2 for setup/reading

        return max(5, int(estimated_minutes))  # Minimum 5 minutes

    def _determine_word_category(self, word: str, theme: str) -> str:
        """Determine appropriate category for a word based on theme."""
        theme_lower = theme.lower()

        # Simple category mapping
        if "animal" in theme_lower or "creature" in theme_lower:
            return "animal"
        elif (
            "place" in theme_lower or "location" in theme_lower or "city" in theme_lower
        ):
            return "place"
        elif (
            "action" in theme_lower
            or "verb" in theme_lower
            or "activity" in theme_lower
        ):
            return "action"
        else:
            return "object"

    def _run_validations(
        self, content: GameContent, theme: str, words: list[str]
    ) -> dict[str, Any]:
        """Run comprehensive validation on assembled game."""
        # Game completion validation
        game_data = {
            "type": "word_game",  # Generic type for validation
            "title": content.title,
            "words": words,
            "difficulty": "medium",  # Default for validation
        }

        completion_result = self.game_validator.validate_game_completion(game_data)

        # Content quality validation
        quality_result = self.game_validator.check_content_quality(
            content.title, words, content.instructions
        )

        # Theme consistency validation
        consistency_result = self.game_validator.validate_theme_consistency(
            theme, words, content.instructions
        )

        return {
            "completion_valid": completion_result.valid,
            "completion_errors": completion_result.error,
            "quality_score": quality_result.quality_score,
            "quality_issues": quality_result.issues,
            "consistency_score": consistency_result.consistency_score,
            "theme_mentioned": consistency_result.theme_mentioned_in_description,
        }

    def _meets_quality_standards(self, validation_results: dict[str, Any]) -> bool:
        """Check if game meets quality standards for publication."""
        standards = self.quality_standards

        # Check completion
        if not validation_results.get("completion_valid", False):
            return False

        # Check quality thresholds
        quality_score = validation_results.get("quality_score", 0)
        consistency_score = validation_results.get("consistency_score", 0)

        return bool(
            quality_score >= standards["content_quality"]
            and consistency_score >= standards["theme_consistency"]
        )

    def generate_quality_report(self, game: CompleteGame) -> dict[str, Any]:
        """Generate comprehensive quality assessment report."""
        return {
            "game_title": game.content.title,
            "theme": game.metadata.theme,
            "word_count": game.metadata.word_count,
            "quality_scores": {
                "content_quality": game.metadata.quality_score,
                "theme_consistency": game.metadata.consistency_score,
                "overall_rating": (
                    game.metadata.quality_score + game.metadata.consistency_score
                )
                / 2,
            },
            "standards_met": game.ready_for_publication,
            "validation_details": game.validation_results,
            "recommendations": self._generate_recommendations(game),
        }

    def _generate_recommendations(self, game: CompleteGame) -> list[str]:
        """Generate improvement recommendations if needed."""
        recommendations = []

        if game.metadata.quality_score < self.quality_standards["content_quality"]:
            recommendations.append(
                "Improve content quality: review title length and instruction clarity"
            )

        if (
            game.metadata.consistency_score
            < self.quality_standards["theme_consistency"]
        ):
            recommendations.append(
                "Enhance theme consistency: ensure instructions mention the theme"
            )

        if not game.ready_for_publication:
            recommendations.append("Address validation issues before publication")

        return recommendations

    def get_builder_configuration(self) -> dict[str, Any]:
        """Get builder-specific configuration."""
        return {
            **self.get_configuration(),
            "quality_standards": self.quality_standards,
            "format_templates": self.format_templates,
        }


# Create default game builder agent instance for backward compatibility
game_builder_agent_instance = GameBuilderAgent()
game_builder_agent = game_builder_agent_instance.get_llm_agent()
