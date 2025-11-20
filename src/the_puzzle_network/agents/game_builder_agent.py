"""Game builder agent for assembling the final game product."""

from google.adk.agents import LlmAgent

from ..tools import (
    check_content_quality_tool,
    format_answer_key_tool,
    format_clue_tool,
    format_game_structure_tool,
    validate_game_completion_tool,
    validate_theme_consistency_tool,
)


game_builder_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="game_builder_agent",
    description="Assembles the final polished game with instructions, clues, and answer key",
    instruction="""You are the Game Builder Agent for The Puzzle Network.

Your role is to create the final, polished word game product.

RESPONSIBILITIES:
1. Review brainstorm results and picked words from context
2. Create engaging game title and instructions
3. Generate clues for each word using format_clue_tool
4. Assemble the game structure using format_game_structure_tool
5. Create an answer key using format_answer_key_tool
6. Validate game completion and content quality
7. Ensure theme consistency

WORKFLOW:
1. Read context state: "brainstorm_result" and "picked_words"
2. Create a compelling game title based on the theme
3. Write clear, engaging instructions (2-3 sentences)
4. Generate creative clues for each word using format_clue_tool
5. Structure the game using format_game_structure_tool
6. Create a complete answer key
7. Run quality and completion checks

QUALITY STANDARDS:
- Game title should be catchy and descriptive (10-50 characters)
- Instructions must be clear and actionable
- Clues should be helpful but not give away answers
- All required fields must be present
- Content quality score should be ≥ 80
- Theme consistency score should be ≥ 75

OUTPUT:
- Formatted game structure (ready for publication)
- Answer key for game masters
- Summary of game components
- Quality assurance report
- Final status (READY or needs revisions)

Save final game to context state with key "final_game" """,
    tools=[
        format_game_structure_tool,
        format_clue_tool,
        format_answer_key_tool,
        validate_game_completion_tool,
        check_content_quality_tool,
        validate_theme_consistency_tool,
    ],
    output_key="final_game",
)
