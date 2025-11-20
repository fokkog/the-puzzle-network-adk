"""Architecture and design documentation for The Puzzle Network."""

# THE PUZZLE NETWORK - ARCHITECTURE DOCUMENTATION

## System Overview

The Puzzle Network is a multi-agent AI system built with Google ADK (Agent Development Kit) that automates the creation of engaging word games. The system uses specialized agents that coordinate through a sequential workflow to transform user requests into complete, polished games.

### Key Design Principles

1. **Separation of Concerns**: Each agent has a single, well-defined responsibility
2. **Sequential Orchestration**: Agents execute in a defined order, passing state between stages
3. **Tool-Based Logic**: Agents leverage specialized tools for validation, formatting, and quality checks
4. **State Management**: Shared session state enables data flow between agents
5. **Simplicity First**: Minimal dependencies, clear code, easy to extend

## Agent Architecture

### 1. Brainstorm Agent
**Responsibility**: Generate creative game concepts and initial word selections

**Input**: User request (e.g., "Create a game about animals")

**Process**:
- Generate game themes and concepts
- Select game type (word_search, crossword, anagram, etc.)
- Create initial word list (5-10 words)
- Validate words and check variety
- Calculate difficulty distribution

**Tools Used**:
- `validate_word_tool`: Check word validity
- `calculate_difficulty_tool`: Score word difficulty
- `check_word_variety_tool`: Ensure variety in selections

**Output**: Brainstorm result saved to state key "brainstorm_result"
- Theme and game type
- Proposed word list
- Difficulty analysis

### 2. Word Picker Agent
**Responsibility**: Validate and refine words, ensure quality standards

**Input**: Reads brainstorm_result from context state

**Process**:
- Validate each word (length, characters, spelling)
- Recalculate difficulty for validation
- Check overall variety and distribution
- Flag and replace problematic words
- Ensure theme consistency

**Tools Used**:
- `validate_word_tool`: Validate individual words
- `calculate_difficulty_tool`: Verify difficulty scores
- `check_word_variety_tool`: Validate overall distribution

**Output**: Approved word list saved to state key "picked_words"
- Final validated word list
- Validation results
- Difficulty distribution confirmation
- Any replacements made

### 3. Game Builder Agent
**Responsibility**: Create the final polished game with instructions, clues, and metadata

**Input**: Reads brainstorm_result and picked_words from context state

**Process**:
- Create engaging game title
- Write clear instructions
- Generate clues for each word
- Format game structure
- Create answer key
- Run quality checks

**Tools Used**:
- `format_game_structure_tool`: Create structured game format
- `format_clue_tool`: Generate clues for words
- `format_answer_key_tool`: Create answer key
- `validate_game_completion_tool`: Verify all components present
- `check_content_quality_tool`: Quality metrics
- `validate_theme_consistency_tool`: Theme validation

**Output**: Complete game saved to state key "final_game"
- Formatted game structure (JSON)
- Answer key
- Game metadata
- Quality report

## Tool Organization

Tools are organized into three modules by functionality:

### word_tools.py
Functions related to word operations:
- `validate_word()`: Check word validity (length, characters)
- `calculate_difficulty()`: Calculate word difficulty score
- `check_word_variety()`: Validate word list diversity

### format_tools.py
Functions for output formatting:
- `format_game_structure()`: Create structured game JSON
- `format_clue()`: Generate word clues
- `format_answer_key()`: Create printable answer key

### validation_tools.py
Functions for quality validation:
- `validate_game_completion()`: Check all required fields present
- `check_content_quality()`: Calculate content quality metrics
- `validate_theme_consistency()`: Verify theme coherence

## State Flow

```
User Request
    ↓
[Brainstorm Agent]
    ├─ Generates ideas
    └─ State: brainstorm_result
        ↓
[Word Picker Agent]
    ├─ Validates & refines
    └─ State: picked_words
        ↓
[Game Builder Agent]
    ├─ Creates final game
    └─ State: final_game
        ↓
    Final Game Ready for Publication
```

Session state keys:
- `brainstorm_result`: Generated themes, game type, initial words
- `picked_words`: Validated and approved word list
- `final_game`: Complete, polished game with all components

## Execution Flow

1. **Initialization**: Load environment, create session service
2. **Pipeline Creation**: Instantiate SequentialAgent with sub-agents
3. **Request Processing**: Convert user request to Content message
4. **Execution**: Runner executes agents sequentially
5. **Event Processing**: Handle events from each agent
6. **Finalization**: Return final game or error status

## Extension Points

### Adding New Agent Capabilities
To add a new specialized agent:
1. Create agent file in `src/agents/`
2. Define LlmAgent with specific instruction and tools
3. Add to agents/__init__.py exports
4. Update orchestration (base_agent.py) if needed

### Creating Custom Tools
To add new tools:
1. Create function with clear docstring
2. Wrap with `FunctionTool(function_name)`
3. Add to appropriate module (word_tools, format_tools, validation_tools)
4. Export from tools/__init__.py

### Modifying Workflow
To change the workflow order or add new agents:
1. Update the `sub_agents` list in SequentialAgent definition
2. Update agent instructions if context dependencies change
3. Ensure state keys align with what downstream agents expect

## Dependencies

### Core
- `google-adk>=1.19.0`: Agent framework
- `python-dotenv>=1.0.0`: Environment configuration

### Runtime Requirements
- Python 3.13+
- Google Gemini API key (from Google Cloud Console)
- Internet connection (for Gemini API)

## Error Handling

Current implementation uses:
- Environment variable validation (fails fast if GOOGLE_API_KEY missing)
- Try-catch in main execution loop
- Agent-level validation through tools

Future improvements:
- Detailed error logging
- Retry mechanisms for API failures
- Graceful degradation for partial failures

## Performance Characteristics

- **Sequential execution**: Each agent waits for previous to complete
- **Average generation time**: 30-60 seconds per game (depends on API latency)
- **Token usage**: ~500-1000 tokens per game generation
- **State memory**: In-memory session service (lost on restart)

## Production Deployment Considerations

### Database Integration
- Replace InMemorySessionService with persistent storage (Redis, PostgreSQL)
- Store generated games for analytics and publication

### API Layer
- Wrap orchestrator in REST API (FastAPI)
- Implement daily scheduling (APScheduler)
- Add rate limiting and authentication

### Monitoring
- Log all agent execution and decisions
- Track API costs and token usage
- Monitor generation success rates

### Scaling
- Horizontally scale with multiple orchestrator instances
- Use distributed session service
- Consider async task queue (Celery) for high volume

## Testing Strategy

### Unit Tests
- Test individual tools (validate_word, calculate_difficulty, etc.)
- Mock LLM responses for deterministic testing
- Verify tool output formats

### Integration Tests
- Test agent interactions with mocked GenAI responses
- Verify state passing between agents
- Validate complete workflow execution

### End-to-End Tests
- Run against real Gemini API with test prompts
- Verify game quality and completeness
- Monitor generation performance

## Future Enhancements

1. **Multiple Workflows**: Support different game types (crossword, trivia, etc.)
2. **User Preferences**: Accept theme, difficulty, word count as parameters
3. **Game Analytics**: Track which games are most popular
4. **Content Moderation**: Add content filtering for inappropriate words
5. **Multi-Language Support**: Generate games in different languages
6. **Caching**: Cache generated games to reduce API calls
7. **Publishing Integration**: Direct API integration for game publication
