"""Configuration and setup guide for The Puzzle Network."""

# SETUP & CONFIGURATION GUIDE

## Prerequisites

- **Python 3.13+**: The project requires Python 3.13 or later
- **Google Gemini API Key**: Obtain from Google Cloud Console
- **pip**: Python package manager (included with Python)

## Step 1: Clone and Navigate

```bash
cd the-puzzle-network
```

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3.13 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

## Step 3: Install Dependencies

```bash
# Install the project and all dependencies
pip install -e .

# For development (includes testing tools)
pip install -e ".[dev]"
```

## Step 4: Configure Environment

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
APP_NAME=the_puzzle_network
LOG_LEVEL=INFO
```

## Step 5: Verify Installation

Test that imports work correctly:

```bash
python -c "from the_puzzle_network.main import run_game_generation; print('✓ Installation successful')"
```

## Step 6: Run the System

### Option A: Run Main Orchestrator

```bash
python -m the_puzzle_network.main
```

This will execute the example game generation request and display the workflow execution.

### Option B: Run Examples

```bash
python examples.py
```

Modify the file to run different example requests.

## Step 7: Run Tests

```bash
pytest tests/ -v
```

Tests validate that the tools work correctly without requiring API calls.

## Configuration Details

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | (required) | Your Google Gemini API key |
| `APP_NAME` | the_puzzle_network | Application identifier for sessions |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

### Project Structure

```
the-puzzle-network/
├── src/the_puzzle_network/          # Main package
│   ├── __init__.py
│   ├── main.py                      # Entry point
│   ├── agents/                      # Agent definitions
│   │   ├── base_agent.py           # Coordinator
│   │   ├── brainstorm_agent.py     # Ideation
│   │   ├── word_picker_agent.py    # Validation
│   │   └── game_builder_agent.py   # Assembly
│   └── tools/                       # Tool modules
│       ├── word_tools.py            # Word operations
│       ├── format_tools.py          # Output formatting
│       └── validation_tools.py      # Quality checks
├── tests/                           # Test suite
├── docs/                            # Documentation
├── examples.py                      # Example scripts
├── pyproject.toml                  # Dependencies
├── .env.example                    # Template
├── README.md                       # Overview
└── .gitignore                      # Git exclusions
```

## Getting Your Google API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (if needed)
3. Enable the Generative AI API
4. Create an API key in "Credentials"
5. Copy the key and add to `.env`:

```
GOOGLE_API_KEY=sk_gNHAjk...your_key_here
```

## Troubleshooting

### "GOOGLE_API_KEY not set" Error

**Solution**: 
1. Check that `.env` file exists in project root
2. Verify API key is correctly entered
3. Ensure no spaces around the `=` sign

```bash
# Verify it's set:
echo $GOOGLE_API_KEY  # macOS/Linux
echo %GOOGLE_API_KEY% # Windows
```

### "Import 'the_puzzle_network' could not be resolved"

**Solution**:
1. Make sure virtual environment is activated
2. Reinstall the package: `pip install -e .`
3. Restart your IDE if using one

### "ModuleNotFoundError: No module named 'google.adk'"

**Solution**:
```bash
pip install google-adk>=1.19.0 --upgrade
```

### API Rate Limiting

**Symptom**: Requests getting rate limited after multiple consecutive calls

**Solution**:
- Add delays between requests
- Check your Google Cloud quota
- Upgrade your API plan if needed

## Development Workflow

### Adding New Features

1. **New Tool**:
   - Create function in appropriate tools module (word_tools.py, format_tools.py, validation_tools.py)
   - Wrap with `FunctionTool(function_name)`
   - Export from tools/__init__.py

2. **New Agent**:
   - Create `agent_name.py` in src/agents/
   - Define LlmAgent with clear instruction
   - Add to agents/__init__.py exports
   - Include in base_agent.py sub_agents if part of workflow

3. **Running Tests**:
   ```bash
   pytest tests/test_tools.py -v
   pytest tests/test_tools.py::TestWordTools::test_validate_word_valid -v
   ```

### Code Style

- Follow PEP 8
- Use type hints where possible
- Write clear docstrings for all functions
- Keep functions focused and single-responsibility

## Next Steps

1. **Customize Instructions**: Edit agent instructions in `src/agents/` to match your game requirements
2. **Add More Tools**: Extend tools modules with domain-specific validators and formatters
3. **Integrate Database**: Replace InMemorySessionService for persistent storage
4. **Build API**: Wrap main.py in FastAPI for HTTP endpoint
5. **Schedule Daily Runs**: Use APScheduler for automatic daily game generation

See `docs/ARCHITECTURE.md` for deeper technical documentation.
