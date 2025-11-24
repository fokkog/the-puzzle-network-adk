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

## Workflow
**PuzzleNetworkWorkflow**: Sequential workflow
```
┌────────────────────────────────────────────────────────────────────────────┐
│                                SequentialAgent                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  GENERATOR  │───▶│ CLASSIFIER  │───▶│ FORMATTER   │───▶│ PUBLISHER   │  │
│  │             │    │             │    │             │    │             │  │
│  │ Creates     │    │ Determines  │    │ Converts to │    │ Delivers    │  │
│  │ knight's    │    │ difficulty  │    │ HTML format │    │ to audience │  │
│  │ tour puzzle │    │ level       │    │             │    │             │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**Agents:**
- **PuzzleGeneratorAgent**: Generates puzzle
- **PuzzleClassifierAgent**: Classifies puzzle as easy/medium/hard
- **PuzzleFormatterAgent**: Formats puzzle
- **PuzzlePublisherAgent**: Published puzzle to appropriate distribution list

**Tools:** 
- **PuzzlePublisherTool**: Published puzzle to appropriate distribution list

## Setup

### Prerequisites
- Python 3.10+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/fokkog/the-puzzle-network-adk.git
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
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

Run the worfklow:

```bash
python -m main
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

The project includes VS Code settings for automatic formatting and linting on save.

### Running Tests

```bash
pytest tests/
```

### GitHub Actions CI/CD

This project includes a comprehensive GitHub Actions workflow for continuous integration and deployment:

***CI Pipeline*** (`.github/workflows/ci.yml`):
   - Testing
   - Code quality checking
   - Type checking
   - Security scanning
   - Package building and validation
   - Pre-commit hook validation

To enable full CI/CD functionality, configure GOOGLE_API_KEY as a repository secret.