# The Puzzle Network

A state-of-the-art multi-agent AI system for generating daily word games using Google ADK.

## Overview

The Puzzle Network uses a coordinated team of AI agents (via Google ADK) to create engaging word games daily. The system orchestrates specialized agents that brainstorm game concepts, select appropriate words, and assemble polished final games ready for publication.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Coordinator Agent                          │
│          (Orchestrates the workflow)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
  ┌─────────────┐ ┌──────────────┐ ┌─────────────────┐
  │  Brainstorm │ │ Word Picker  │ │ Game Builder    │
  │   Agent     │ │   Agent      │ │   Agent         │
  └─────────────┘ └──────────────┘ └─────────────────┘
        │              │                    │
        └──────────────┴────────────────────┘
                       │
                       ▼
            Shared Session State
       (Ideas → Words → Final Game)
```

**Agents:**
- **Brainstorm Agent**: Generates creative game concepts and themes
- **Word Picker Agent**: Selects appropriate words based on difficulty and theme
- **Game Builder Agent**: Assembles the final game with answers, hints, and metadata

**Tools:** Distributed across modular tool modules:
- `word_tools.py`: Word validation, difficulty scoring, word list management
- `format_tools.py`: Game structure formatting, output preparation
- `validation_tools.py`: Quality checks, constraint validation

## Setup

### Prerequisites
- Python 3.13+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
cd the-puzzle-network
```

2. Create and activate a virtual environment:
```bash
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Usage

Run the word game generation pipeline:

```bash
python -m the_puzzle_network.main
```

## Project Structure

```
the-puzzle-network/
├── src/the_puzzle_network/
│   ├── __init__.py
│   ├── main.py                    # Entry point & workflow orchestrator
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Root coordinator agent
│   │   ├── brainstorm_agent.py   # Idea generation agent
│   │   ├── word_picker_agent.py  # Word selection agent
│   │   └── game_builder_agent.py # Game assembly agent
│   └── tools/
│       ├── __init__.py
│       ├── word_tools.py          # Word operations
│       ├── format_tools.py        # Formatting utilities
│       └── validation_tools.py    # Quality validation
├── tests/
│   └── __init__.py
├── docs/
│   └── ARCHITECTURE.md
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

### Configuration

Edit `.env` to customize:
- `GOOGLE_API_KEY`: Your Gemini API key
- `APP_NAME`: Application identifier
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## API Reference

See `docs/ARCHITECTURE.md` for detailed agent and tool API documentation.

## License

Apache 2.0

## Contributing

Contributions welcome. Please ensure Python 3.13+ compatibility and add tests for new features.
