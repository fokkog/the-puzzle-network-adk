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

### Usage

Run the word game generation pipeline:

```bash
python -m the_puzzle_network.main
```

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```
