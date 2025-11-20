"""Main entry point for The Puzzle Network workflow orchestrator."""

import asyncio
import os
from dotenv import load_dotenv

from google.adk.agents import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from the_puzzle_network.agents import (
    create_coordinator_agent,
    brainstorm_agent,
    word_picker_agent,
    game_builder_agent
)


# Load environment variables
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "the_puzzle_network")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Please add it to your .env file or set it as an environment variable."
    )


def create_game_generation_pipeline() -> SequentialAgent:
    """
    Create the sequential game generation pipeline.
    
    The pipeline executes agents in order:
    1. brainstorm_agent - generates game ideas and themes
    2. word_picker_agent - validates and refines word selections
    3. game_builder_agent - assembles the final game
    
    Returns:
        SequentialAgent orchestrating the complete workflow
    """
    pipeline = SequentialAgent(
        name="GameGenerationPipeline",
        description="Complete word game generation workflow",
        sub_agents=[brainstorm_agent, word_picker_agent, game_builder_agent]
    )
    return pipeline


async def run_game_generation(user_request: str) -> None:
    """
    Execute the game generation pipeline.
    
    Args:
        user_request: The user's request for game generation (e.g., "Create a game about animals")
    """
    print(f"\n{'='*60}")
    print(f"The Puzzle Network - Game Generator")
    print(f"{'='*60}\n")
    
    print(f"Request: {user_request}\n")
    
    # Create the pipeline
    pipeline = create_game_generation_pipeline()
    
    # Initialize session service for state management
    session_service = InMemorySessionService()
    
    # Create a session for this game generation request
    user_id = "default_user"
    session_id = "game_session_001"
    
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    
    # Create runner to execute the pipeline
    runner = Runner(
        agent=pipeline,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    # Execute the pipeline with the user request
    print("Executing workflow...\n")
    print("-" * 60)
    
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=user_request)]
    )
    
    # Process all events from the pipeline execution
    final_response = None
    event_count = 0
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    ):
        event_count += 1
        
        # Handle different event types
        if event.is_final_response():
            final_response = event
            print(f"\n[Pipeline Complete]")
        
        # Print agent messages
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"{part.text}\n")
    
    print("-" * 60)
    
    if final_response and final_response.content and final_response.content.parts:
        print("\n📋 FINAL GAME PRODUCT:")
        print("-" * 60)
        for part in final_response.content.parts:
            if hasattr(part, 'text'):
                print(part.text)
    else:
        print("\n✅ Workflow completed successfully")
        print("(Game generation complete - check agent outputs above)")
    
    print(f"\n{'='*60}\n")


async def main():
    """Main entry point."""
    # Example game generation requests
    example_requests = [
        "Create an educational word game about marine animals with 6-8 words. Make it appropriate for children."
    ]
    
    for request in example_requests:
        try:
            await run_game_generation(request)
        except Exception as e:
            print(f"Error during game generation: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
