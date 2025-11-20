"""Base coordinator agent for the puzzle network."""

from google.adk.agents import LlmAgent
from .brainstorm_agent import brainstorm_agent
from .word_picker_agent import word_picker_agent
from .game_builder_agent import game_builder_agent


def create_coordinator_agent() -> LlmAgent:
    """
    Create the main coordinator agent that orchestrates the workflow.
    
    The coordinator manages the three-stage pipeline:
    1. Brainstorm ideas and themes
    2. Pick appropriate words
    3. Build the final game
    
    Returns:
        LlmAgent configured as coordinator
    """
    coordinator = LlmAgent(
        model="gemini-2.5-flash",
        name="coordinator",
        description="Main orchestrator for word game generation pipeline",
        instruction="""You are the Puzzle Network Game Generator Coordinator.

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

Keep the workflow moving smoothly by maintaining context and ensuring clear communication between agents.""",
        sub_agents=[brainstorm_agent, word_picker_agent, game_builder_agent]
    )
    
    return coordinator
