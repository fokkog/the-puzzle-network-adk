"""Example scripts demonstrating The Puzzle Network usage."""

import asyncio
from dotenv import load_dotenv
from the_puzzle_network.main import run_game_generation


async def example_basic_game_generation():
    """Example: Generate a basic word game."""
    request = "Create a simple word game about fruits with 5 words, easy difficulty level"
    await run_game_generation(request)


async def example_themed_game():
    """Example: Generate a themed word game."""
    request = "Create a challenging word game about space exploration. Include scientific terms. Use 8-10 words with mixed difficulty."
    await run_game_generation(request)


async def example_category_game():
    """Example: Generate a category-based game."""
    request = "Create a word match game with animals from different continents. Include 6-8 animals with clear geographical themes."
    await run_game_generation(request)


async def run_all_examples():
    """Run all example game generation requests."""
    load_dotenv()
    
    examples = [
        ("Basic Game", example_basic_game_generation),
        ("Themed Game", example_themed_game),
        ("Category Game", example_category_game),
    ]
    
    for name, example_func in examples:
        print(f"\n\n{'='*70}")
        print(f"EXAMPLE: {name}")
        print(f"{'='*70}")
        try:
            await example_func()
        except Exception as e:
            print(f"Error in example: {e}")


if __name__ == "__main__":
    # Uncomment the example(s) you want to run
    load_dotenv()
    
    # Run a single example
    asyncio.run(example_basic_game_generation())
    
    # Or run all examples (comment out the line above)
    # asyncio.run(run_all_examples())
