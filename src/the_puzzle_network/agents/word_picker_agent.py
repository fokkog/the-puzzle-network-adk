"""Word picker agent for selecting and refining game words."""

from dataclasses import dataclass
from typing import Any, cast

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool

from ..tools import (
    calculate_difficulty_tool,
    check_word_variety_tool,
    validate_word_tool,
)
from ..tools.word_tools import DifficultyLevel, ValidationResult, VarietyResult
from .base_agent import (
    AgentConfig,
    AgentResult,
    AgentRole,
    BasePuzzleAgent,
    ProcessingStage,
)


@dataclass
class SelectionCriteria:
    """Criteria for word selection and refinement."""

    min_words: int = 5
    max_words: int = 15
    difficulty_balance: dict[str, float] | None = (
        None  # e.g., {"easy": 0.3, "medium": 0.5, "hard": 0.2}
    )
    theme_relevance_threshold: float = 0.7
    allow_proper_nouns: bool = False


@dataclass
class RefinedWordList:
    """Result of word refinement process."""

    original_words: list[str]
    final_words: list[str]
    replacements: dict[str, str]  # old_word -> new_word
    validation_results: list[ValidationResult]
    variety_result: VarietyResult
    quality_score: float


class WordPickerAgent(BasePuzzleAgent):
    """Specialized agent for word selection and validation."""

    def __init__(
        self,
        config: AgentConfig | None = None,
        selection_criteria: SelectionCriteria | None = None,
        strict_validation: bool = True,
    ) -> None:
        """
        Initialize word picker agent.

        Args:
            config: Agent configuration
            selection_criteria: Criteria for word selection
            strict_validation: Whether to apply strict validation rules
        """
        self.selection_criteria = selection_criteria or SelectionCriteria()
        self.strict_validation = strict_validation

        super().__init__(
            name="word_picker_agent",
            role=AgentRole.WORD_PICKER,
            config=config,
        )

    def _create_llm_agent(self) -> LlmAgent:
        """Create the word picker LlmAgent."""
        return LlmAgent(
            model=self.config.model,
            name=self.name,
            description="Selects, validates, and refines words for the game",
            instruction=self._get_instruction(),
            tools=cast(list, self.get_required_tools()),
            output_key="picked_words",
        )

    def _get_instruction(self) -> str:
        """Get word picker agent instruction template."""
        criteria = self.selection_criteria

        return f"""You are the Word Picker Agent for The Puzzle Network.

Your role is to validate and refine the word selections from the brainstorm stage.

RESPONSIBILITIES:
1. Review brainstorm results from context state key "brainstorm_result"
2. Validate each word using the validate_word tool
3. Calculate difficulty for each word using calculate_difficulty_tool
4. Verify overall word variety and balance using check_word_variety_tool
5. Refine or replace any problematic words
6. Ensure consistency with the game theme

SELECTION CRITERIA:
- Word count: {criteria.min_words}-{criteria.max_words} words
- Validation mode: {"Strict" if self.strict_validation else "Lenient"}
- Proper nouns allowed: {criteria.allow_proper_nouns}
- Theme relevance threshold: {criteria.theme_relevance_threshold:.1f}

QUALITY CHECKS:
- All words must be valid (3-20 characters, letters only)
- Verify difficulty distribution is balanced
- Check for duplicates or near-duplicates
- Ensure words fit the stated theme

WORKFLOW:
1. Read the brainstorm_result from context
2. Validate each word individually
3. Check overall variety and difficulty distribution
4. Flag any issues or suggest replacements
5. Provide final approved word list

OUTPUT:
- Confirm or suggest changes to the word list
- Show validation results for each word
- Explain any replacements made
- Confirm final difficulty distribution
- Save final word list to context state with key "picked_words" """

    def get_required_tools(self) -> list[BaseTool]:
        """Get required tools for word picking."""
        return [validate_word_tool, calculate_difficulty_tool, check_word_variety_tool]

    def validate_context(self, context: dict[str, Any]) -> bool:
        """Validate word picker context."""
        return "brainstorm_result" in context

    def process_request(self, request: str, context: dict[str, Any]) -> AgentResult:
        """Process word selection request."""
        brainstorm_data = context.get("brainstorm_result", {})

        return AgentResult(
            success=True,
            stage=ProcessingStage.WORD_SELECTION,
            data={
                "brainstorm_data": brainstorm_data,
                "selection_criteria": self.selection_criteria,
                "strict_validation": self.strict_validation,
            },
        )

    def refine_word_list(self, initial_words: list[str], theme: str) -> RefinedWordList:
        """Refine and validate a word list."""
        validation_results = []
        final_words = []
        replacements = {}

        for word in initial_words:
            validation = self.word_analyzer.validate_word(word)
            validation_results.append(validation)

            if validation.valid and validation.word:
                final_words.append(validation.word)
            else:
                # Try to find replacement
                replacement = self._suggest_replacement(word, theme)
                if replacement:
                    replacements[word] = replacement
                    final_words.append(replacement)

        # Check overall variety
        variety_result = self.word_analyzer.check_word_variety(final_words)

        # Calculate quality score
        quality_score = self._calculate_quality_score(
            validation_results, variety_result
        )

        return RefinedWordList(
            original_words=initial_words,
            final_words=final_words,
            replacements=replacements,
            validation_results=validation_results,
            variety_result=variety_result,
            quality_score=quality_score,
        )

    def balance_difficulty(self, words: list[str]) -> list[str]:
        """Balance difficulty distribution in word list."""
        if not self.selection_criteria.difficulty_balance:
            return words

        # Analyze current difficulty distribution
        word_difficulties = []
        for word in words:
            difficulty = self.word_analyzer.calculate_difficulty(word)
            word_difficulties.append((word, difficulty))

        # Group by difficulty
        easy_words = [
            w for w, d in word_difficulties if d.difficulty == DifficultyLevel.EASY
        ]
        medium_words = [
            w for w, d in word_difficulties if d.difficulty == DifficultyLevel.MEDIUM
        ]
        hard_words = [
            w for w, d in word_difficulties if d.difficulty == DifficultyLevel.HARD
        ]

        # Apply target distribution
        target = self.selection_criteria.difficulty_balance
        total_words = len(words)

        target_easy = int(total_words * target.get("easy", 0.33))
        target_medium = int(total_words * target.get("medium", 0.33))
        target_hard = total_words - target_easy - target_medium

        # Select words to meet target distribution
        balanced_words = []
        balanced_words.extend(easy_words[:target_easy])
        balanced_words.extend(medium_words[:target_medium])
        balanced_words.extend(hard_words[:target_hard])

        return balanced_words

    def _suggest_replacement(self, invalid_word: str, theme: str) -> str | None:
        """Suggest a replacement for an invalid word."""
        # Simple replacement logic - could be enhanced with thematic word databases
        if len(invalid_word) < 3:
            return None

        # Try to create a valid version
        cleaned = "".join(c for c in invalid_word.lower() if c.isalpha())

        if len(cleaned) >= 3:
            validation = self.word_analyzer.validate_word(cleaned)
            if validation.valid:
                return cleaned

        return None

    def _calculate_quality_score(
        self, validation_results: list[ValidationResult], variety_result: VarietyResult
    ) -> float:
        """Calculate overall quality score for word selection."""
        # Base score from validation success rate
        valid_count = sum(1 for v in validation_results if v.valid)
        validation_score = (
            (valid_count / len(validation_results)) * 50 if validation_results else 0
        )

        # Variety score
        variety_score = 50 if variety_result.valid else 25

        # Bonus for good difficulty distribution
        distribution_bonus = 0.0
        if variety_result.difficulty_distribution:
            dist = variety_result.difficulty_distribution
            # Ideal distribution is roughly 1/3 each
            ideal_ratio = variety_result.total_words / 3
            distribution_quality = 1.0 - (
                abs(dist["easy"] - ideal_ratio)
                + abs(dist["medium"] - ideal_ratio)
                + abs(dist["hard"] - ideal_ratio)
            ) / (variety_result.total_words * 2)
            distribution_bonus = distribution_quality * 20

        return validation_score + variety_score + distribution_bonus

    def get_selection_configuration(self) -> dict[str, Any]:
        """Get selection-specific configuration."""
        return {
            **self.get_configuration(),
            "selection_criteria": {
                "min_words": self.selection_criteria.min_words,
                "max_words": self.selection_criteria.max_words,
                "difficulty_balance": self.selection_criteria.difficulty_balance,
                "theme_relevance_threshold": self.selection_criteria.theme_relevance_threshold,
                "allow_proper_nouns": self.selection_criteria.allow_proper_nouns,
            },
            "strict_validation": self.strict_validation,
        }


# Create default word picker agent instance for backward compatibility
word_picker_agent_instance = WordPickerAgent()
word_picker_agent = word_picker_agent_instance.get_llm_agent()
