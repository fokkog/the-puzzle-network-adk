"""Quick start guide for The Puzzle Network."""

# QUICK START GUIDE

Get up and running in 5 minutes.

## 1. Set Up (2 minutes)

```bash
# Clone/navigate to project
cd the-puzzle-network

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

## 2. Configure (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit and add your Google API key
# GOOGLE_API_KEY=sk_your_actual_key_here
```

**Don't have an API key?**
- Go to: https://ai.google.dev/tutorials/setup
- Click "Get API Key"
- Copy and paste into `.env`

## 3. Run (1 minute)

```bash
# Execute the game generation pipeline
python -m the_puzzle_network.main
```

You'll see:
1. **Brainstorm Agent**: Generates game themes and words
2. **Word Picker Agent**: Validates and refines selections
3. **Game Builder Agent**: Creates the final game

## 4. Check Results (1 minute)

The workflow outputs:
- Generated game theme and type
- Selected words with difficulty levels
- Final game structure with clues and answer key
- Quality metrics

## Example Request

The default example generates: "Create an educational word game about marine animals with 6-8 words. Make it appropriate for children."

Edit `src/the_puzzle_network/main.py` to change the request:

```python
example_requests = [
    "Your custom request here"
]
```

## Common Requests

### Simple Game
```
"Create a basic word game about colors with 5 words"
```

### Themed Game
```
"Create a challenging word game about space with 8 scientific terms"
```

### Category Game
```
"Create a word game about animals from different continents with 6 animals"
```

## Project Structure

```
src/the_puzzle_network/
├── main.py                     # Entry point
├── agents/
│   ├── base_agent.py          # Orchestrator
│   ├── brainstorm_agent.py    # Ideation
│   ├── word_picker_agent.py   # Validation
│   └── game_builder_agent.py  # Assembly
└── tools/
    ├── word_tools.py          # Word operations
    ├── format_tools.py        # Formatting
    └── validation_tools.py    # Quality checks
```

## Next Steps

- **Full Setup Guide**: See `SETUP.md` for detailed configuration
- **Architecture Details**: See `docs/ARCHITECTURE.md` for technical details
- **Run Examples**: See `examples.py` for more usage patterns
- **Run Tests**: `pytest tests/` to validate installation

## Troubleshooting

**"GOOGLE_API_KEY not set"**
- Check `.env` file exists and has your key

**"ModuleNotFoundError"**
- Activate venv: `source venv/bin/activate`
- Reinstall: `pip install -e .`

**API Errors**
- Verify your API key is valid
- Check internet connection
- Verify API is enabled in Google Cloud Console

## Support

For issues with Google ADK, see: https://ai.google.dev/adk/docs/

For detailed documentation, see SETUP.md and docs/ARCHITECTURE.md
