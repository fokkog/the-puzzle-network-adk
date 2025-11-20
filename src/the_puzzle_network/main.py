"""Main entry point for The Puzzle Network workflow orchestrator."""

import asyncio
import os
from dataclasses import dataclass
from typing import Any, cast

from dotenv import load_dotenv
from google.adk.agents import BaseAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from the_puzzle_network.agents.base_agent import AgentConfig, CoordinatorAgent
from the_puzzle_network.agents.brainstorm_agent import BrainstormAgent
from the_puzzle_network.agents.game_builder_agent import GameBuilderAgent
from the_puzzle_network.agents.word_picker_agent import WordPickerAgent


@dataclass
class PipelineConfig:
    """Configuration for the game generation pipeline."""

    app_name: str | None = None
    user_id: str = "default_user"
    session_prefix: str = "game_session"
    max_retries: int = 3
    timeout_seconds: int = 300
    quality_threshold: float = 85.0


@dataclass
class GameRequest:
    """Structured game generation request."""

    description: str
    theme: str | None = None
    difficulty: str = "medium"
    word_count: int = 8
    game_type: str | None = None
    target_audience: str | None = None

    @classmethod
    def from_text(cls, request_text: str) -> "GameRequest":
        """Create GameRequest from natural language text."""
        # Simple parsing - could be enhanced with NLP
        return cls(
            description=request_text,
            # Additional parsing logic would go here
        )

    def to_context(self) -> dict[str, Any]:
        """Convert request to context dictionary."""
        return {
            "description": self.description,
            "theme": self.theme,
            "difficulty": self.difficulty,
            "word_count": self.word_count,
            "game_type": self.game_type,
            "target_audience": self.target_audience,
        }


@dataclass
class PipelineMetrics:
    """Metrics collected during pipeline execution."""

    total_events: int = 0
    execution_time_seconds: float = 0.0
    agent_performance: dict[str, float] | None = None
    quality_scores: dict[str, float] | None = None
    error_count: int = 0


class GameGenerationPipeline:
    """Main orchestrator for the game generation workflow."""

    def __init__(
        self,
        config: PipelineConfig | None = None,
        brainstorm_agent: BrainstormAgent | None = None,
        word_picker_agent: WordPickerAgent | None = None,
        game_builder_agent: GameBuilderAgent | None = None,
    ) -> None:
        """
        Initialize the game generation pipeline.

        Args:
            config: Pipeline configuration
            brainstorm_agent: Custom brainstorm agent instance
            word_picker_agent: Custom word picker agent instance
            game_builder_agent: Custom game builder agent instance
        """
        # Load environment variables
        load_dotenv()

        self.config = config or PipelineConfig()
        self.config.app_name = self.config.app_name or os.getenv(
            "APP_NAME", "puzzle-network"
        )

        # Validate API key
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. "
                "Please add it to your .env file or set it as an environment variable."
            )

        print("✅ Gemini API key setup complete.")

        # Initialize agents
        agent_config = AgentConfig(quality_threshold=self.config.quality_threshold)

        self.brainstorm_agent = brainstorm_agent or BrainstormAgent(config=agent_config)
        self.word_picker_agent = word_picker_agent or WordPickerAgent(
            config=agent_config
        )
        self.game_builder_agent = game_builder_agent or GameBuilderAgent(
            config=agent_config
        )

        # Create coordinator
        self.coordinator = CoordinatorAgent(
            sub_agents=[
                self.brainstorm_agent,
                self.word_picker_agent,
                self.game_builder_agent,
            ],
            config=agent_config,
        )

        # Initialize session service
        self.session_service = InMemorySessionService()

        # Metrics tracking
        self.metrics = PipelineMetrics()

    def create_sequential_pipeline(self) -> SequentialAgent:
        """
        Create the sequential agent pipeline.

        Returns:
            SequentialAgent configured for game generation
        """
        # Get LlmAgent instances for Google ADK integration
        sub_agents = [
            self.brainstorm_agent.get_llm_agent(),
            self.word_picker_agent.get_llm_agent(),
            self.game_builder_agent.get_llm_agent(),
        ]

        return SequentialAgent(
            name="GameGenerationPipeline",
            description="Complete word game generation workflow",
            sub_agents=cast(list[BaseAgent], sub_agents),
        )

    async def execute(self, request: GameRequest) -> dict[str, Any]:
        """
        Execute the complete game generation pipeline.

        Args:
            request: Structured game generation request

        Returns:
            Dictionary with execution results and generated game
        """
        import time

        start_time = time.time()

        try:
            print(f"\n{'=' * 60}")
            print("The Puzzle Network - Game Generator")
            print(f"{'=' * 60}\n")
            print(f"Request: {request.description}\n")

            # Validate pipeline
            validation_result = self.validate_pipeline()
            if not validation_result["valid"]:
                raise ValueError(
                    f"Pipeline validation failed: {validation_result['error']}"
                )

            # Create session
            session_id = f"{self.config.session_prefix}_{int(time.time())}"
            await self.session_service.create_session(
                app_name=self.config.app_name or "puzzle-network",
                user_id=self.config.user_id,
                session_id=session_id,
            )

            # Create and execute pipeline
            pipeline = self.create_sequential_pipeline()
            runner = Runner(
                agent=pipeline,
                app_name=self.config.app_name,
                session_service=self.session_service,
            )

            # Execute pipeline
            print("Executing workflow...\n")
            print("-" * 60)

            user_message = types.Content(
                role="user", parts=[types.Part(text=request.description)]
            )

            # Process events
            final_response = None
            event_count = 0

            async for event in runner.run_async(
                user_id=self.config.user_id,
                session_id=session_id,
                new_message=user_message,
            ):
                event_count += 1
                self.metrics.total_events = event_count

                if event.is_final_response():
                    final_response = event
                    print("\n[Pipeline Complete]")

                # Print agent messages
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            print(f"{part.text}\n")

            print("-" * 60)

            # Process results
            execution_time = time.time() - start_time
            self.metrics.execution_time_seconds = execution_time

            result = {
                "success": True,
                "request": request,
                "execution_time": execution_time,
                "event_count": event_count,
                "final_response": final_response,
                "metrics": self.metrics,
            }

            # Display final game if available
            if (
                final_response
                and final_response.content
                and final_response.content.parts
            ):
                print("\n📋 FINAL GAME PRODUCT:")
                print("-" * 60)
                for part in final_response.content.parts:
                    if hasattr(part, "text"):
                        print(part.text)
                        result["final_game"] = part.text
            else:
                print("\n✅ Workflow completed successfully")
                print("(Game generation complete - check agent outputs above)")

            print(f"\n{'=' * 60}\n")
            return result

        except Exception as e:
            self.metrics.error_count += 1
            execution_time = time.time() - start_time
            self.metrics.execution_time_seconds = execution_time

            print(f"Error during game generation: {e}")
            import traceback

            traceback.print_exc()

            return {
                "success": False,
                "error": str(e),
                "request": request,
                "execution_time": execution_time,
                "metrics": self.metrics,
            }

    def validate_pipeline(self) -> dict[str, Any]:
        """Validate pipeline configuration and readiness."""
        issues = []

        # Check API key
        if not self.google_api_key:
            issues.append("Google API key not configured")

        # Check agents
        if not all(
            [self.brainstorm_agent, self.word_picker_agent, self.game_builder_agent]
        ):
            issues.append("Not all required agents are initialized")

        # Check session service
        if not self.session_service:
            issues.append("Session service not initialized")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "error": "; ".join(issues) if issues else None,
        }

    def get_execution_metrics(self) -> PipelineMetrics:
        """Get execution metrics for monitoring."""
        return self.metrics

    def get_configuration(self) -> dict[str, Any]:
        """Get pipeline configuration for debugging."""
        return {
            "config": {
                "app_name": self.config.app_name,
                "user_id": self.config.user_id,
                "session_prefix": self.config.session_prefix,
                "max_retries": self.config.max_retries,
                "timeout_seconds": self.config.timeout_seconds,
                "quality_threshold": self.config.quality_threshold,
            },
            "agents": {
                "brainstorm": self.brainstorm_agent.get_configuration(),
                "word_picker": self.word_picker_agent.get_configuration(),
                "game_builder": self.game_builder_agent.get_configuration(),
                "coordinator": self.coordinator.get_configuration(),
            },
        }


class GameGenerationService:
    """High-level service interface for game generation."""

    def __init__(self, pipeline: GameGenerationPipeline | None = None) -> None:
        """Initialize the service with optional custom pipeline."""
        self.pipeline = pipeline or GameGenerationPipeline()

    async def generate_game(self, request_text: str) -> dict[str, Any]:
        """
        Generate a game from natural language request.

        Args:
            request_text: Natural language game generation request

        Returns:
            Complete game generation result
        """
        request = GameRequest.from_text(request_text)
        return await self.pipeline.execute(request)

    async def generate_structured_game(self, request: GameRequest) -> dict[str, Any]:
        """
        Generate a game from structured request.

        Args:
            request: Structured GameRequest object

        Returns:
            Complete game generation result
        """
        return await self.pipeline.execute(request)

    def get_pipeline_status(self) -> dict[str, Any]:
        """Get current pipeline status and health."""
        validation = self.pipeline.validate_pipeline()
        metrics = self.pipeline.get_execution_metrics()

        return {
            "pipeline_valid": validation["valid"],
            "validation_issues": validation.get("issues", []),
            "metrics": {
                "total_executions": metrics.total_events,
                "average_execution_time": metrics.execution_time_seconds,
                "error_rate": metrics.error_count,
            },
            "configuration": self.pipeline.get_configuration(),
        }


# Backward compatibility functions
async def run_game_generation(user_request: str) -> None:
    """Backward compatibility wrapper."""
    service = GameGenerationService()
    await service.generate_game(user_request)


def create_game_generation_pipeline() -> SequentialAgent:
    """Backward compatibility wrapper."""
    pipeline = GameGenerationPipeline()
    return pipeline.create_sequential_pipeline()


async def main() -> None:
    """Main entry point with enhanced functionality."""
    service = GameGenerationService()

    # Example game generation requests
    example_requests = [
        "Create an educational word game about marine animals with 6-8 words. Make it appropriate for children.",
        "Design a challenging crossword puzzle about space exploration for adults.",
        "Make a fun anagram game using kitchen utensils for family game night.",
    ]

    for request_text in example_requests:
        try:
            result = await service.generate_game(request_text)

            if result["success"]:
                print(
                    f"✅ Successfully generated game in {result['execution_time']:.1f}s"
                )
                print(f"   Events processed: {result['event_count']}")
            else:
                print(f"❌ Failed to generate game: {result['error']}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
