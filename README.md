# The Puzzle Network

A state-of-the-art multi-agent AI system for generating daily word games using Google ADK.

## Overview

The Puzzle Network uses a coordinated team of AI agents (via Google ADK) to create engaging word games daily.
Specifically the games are of the type knight’s tour word puzzle, e.g.:
```
NRR
T G
EAS
```
...with a solution of STRANGER.
Every day 3 games (of type easy, medium and hard) are published to the respective subscribers.

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
- Python 3.10+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
cd the-puzzle-network
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
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

### Usage

Run the word game generation pipeline:

```bash
python -m the_puzzle_network.main
```

### Development Tools

This project uses modern Python development tools for code quality and consistency:

- **ruff**: Fast linter and formatter (replaces black, flake8, isort)
- **mypy**: Static type checking with gradual typing
- **pre-commit**: Automated code quality checks on git commits

#### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

#### Set Up Pre-commit Hooks

```bash
pre-commit install
```

#### Code Quality Commands

```bash
# Format code
ruff format .

# Check and fix linting issues
ruff check --fix .

# Run type checking
mypy .

# Run all pre-commit hooks manually
pre-commit run --all-files
```

#### VS Code Integration

The project includes VS Code settings for automatic formatting and linting on save. Install the ruff extension for the best experience.

### Running Tests

```bash
pytest tests/
```
