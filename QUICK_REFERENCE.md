"""Quick reference card for The Puzzle Network commands."""

═══════════════════════════════════════════════════════════════════════════════
                        THE PUZZLE NETWORK - QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════════════

🚀 SETUP (First Time Only)

    cd /Users/fokkog/the-puzzle-network
    python3.13 -m venv venv
    source venv/bin/activate
    pip install -e .
    cp .env.example .env
    # Edit .env and add GOOGLE_API_KEY


💻 COMMON COMMANDS

    # Run the game generator
    python -m the_puzzle_network.main

    # Run example scripts
    python examples.py

    # Run tests
    pytest tests/ -v

    # Run specific test
    pytest tests/test_tools.py::TestWordTools::test_validate_word_valid -v

    # View test coverage
    pytest tests/ --cov=the_puzzle_network

    # Activate virtual environment (if not active)
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate     # Windows


📁 KEY FILE LOCATIONS

    /Users/fokkog/the-puzzle-network/

    Configuration:
    • .env                  ← Your API key and settings
    • pyproject.toml        ← Dependencies

    Source Code:
    • src/the_puzzle_network/main.py          ← Entry point
    • src/the_puzzle_network/agents/          ← Agent definitions
    • src/the_puzzle_network/tools/           ← Tools implementations

    Documentation:
    • QUICKSTART.md         ← Start here (5 min)
    • SETUP.md              ← Detailed setup
    • docs/ARCHITECTURE.md  ← Technical deep dive
    • README.md             ← Project overview


🔧 CUSTOMIZATION EXAMPLES

    # Change game request in main.py
    example_requests = [
        "Your custom request here"
    ]

    # Add new tool in word_tools.py
    def my_tool(param: str) -> dict:
        """Clear description of what tool does."""
        return {"result": value}

    my_tool_instance = FunctionTool(my_tool)

    # Export from tools/__init__.py
    from .word_tools import my_tool_instance
    __all__ = [..., "my_tool_instance"]

    # Add to agent
    some_agent = LlmAgent(
        ...
        tools=[my_tool_instance, ...],
        ...
    )


📊 PROJECT STRUCTURE AT A GLANCE

    the-puzzle-network/
    ├── src/the_puzzle_network/
    │   ├── main.py              ← Start here
    │   ├── agents/              ← 4 agents
    │   │   ├── base_agent.py      (coordinator)
    │   │   ├── brainstorm_agent.py (ideation)
    │   │   ├── word_picker_agent.py (validation)
    │   │   └── game_builder_agent.py (assembly)
    │   └── tools/               ← 3 tool modules
    │       ├── word_tools.py     (3 functions)
    │       ├── format_tools.py   (3 functions)
    │       └── validation_tools.py (3 functions)
    ├── tests/
    │   └── test_tools.py        ← Unit tests
    ├── docs/
    │   └── ARCHITECTURE.md      ← Technical docs
    ├── QUICKSTART.md            ← 5-minute setup
    ├── SETUP.md                 ← Detailed setup
    ├── README.md                ← Overview
    ├── pyproject.toml           ← Dependencies
    ├── .env.example             ← Config template
    └── examples.py              ← Example usage


🔄 WORKFLOW

    User Request
        ↓
    [Brainstorm Agent] → generates theme, game type, words
        ↓
    [Word Picker Agent] → validates & refines words
        ↓
    [Game Builder Agent] → creates final game
        ↓
    Published Game Ready


📝 AGENT OUTPUT STATE KEYS

    brainstorm_result  ← Theme, game type, initial words
    picked_words       ← Validated word list
    final_game         ← Complete game with clues & answer key


🛠️  TOOLS OVERVIEW

    Word Tools (word_tools.py):
    • validate_word(word) → {valid, word, length}
    • calculate_difficulty(word) → {difficulty, score, vowels, consonants}
    • check_word_variety(words) → {valid, difficulty_distribution}

    Format Tools (format_tools.py):
    • format_game_structure(type, title, words, difficulty) → JSON string
    • format_clue(word, category) → {word, hint, category}
    • format_answer_key(words_with_answers) → formatted string

    Validation Tools (validation_tools.py):
    • validate_game_completion(game_data) → {valid, error/message}
    • check_content_quality(title, words, instructions) → {valid, score, issues}
    • validate_theme_consistency(theme, words, description) → {valid, score}


🐛 TROUBLESHOOTING

    Problem: "GOOGLE_API_KEY not set"
    Solution: Check .env file exists in project root with your key

    Problem: "ModuleNotFoundError: No module named 'the_puzzle_network'"
    Solution: Activate venv, then: pip install -e .

    Problem: "ModuleNotFoundError: No module named 'google.adk'"
    Solution: pip install google-adk>=1.19.0 --upgrade

    Problem: Rate limiting errors
    Solution: Add delays between requests or upgrade API quota


📚 DOCUMENTATION

    5-minute start:  QUICKSTART.md
    Full setup:      SETUP.md
    Architecture:    docs/ARCHITECTURE.md
    API reference:   docs/ARCHITECTURE.md (Agent/Tool sections)
    Examples:        examples.py


✅ VERIFICATION CHECKLIST

    □ Virtual environment created and activated
    □ Dependencies installed (pip install -e .)
    □ .env file created with GOOGLE_API_KEY
    □ Tools can be imported without errors
    □ Tests pass (pytest tests/ -v)
    □ Main script runs (python -m the_puzzle_network.main)


🎯 NEXT STEPS

    1. Follow QUICKSTART.md (5 minutes)
    2. Run: python -m the_puzzle_network.main
    3. Customize game requests
    4. Add new tools as needed
    5. Build REST API wrapper (FastAPI)
    6. Set up scheduling (APScheduler)
    7. Deploy to production


═══════════════════════════════════════════════════════════════════════════════
                        For more help, see SETUP.md
═══════════════════════════════════════════════════════════════════════════════
