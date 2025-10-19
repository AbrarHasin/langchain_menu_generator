# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit web application that generates restaurant names based on country input using LangChain and Anthropic's Claude AI (claude-3-7-sonnet-20250219 model).

## Running the Application

**Start the Streamlit app:**
```bash
poetry run streamlit run src/streamlit/main.py
```

Alternative methods:
```bash
# Using poetry shell
poetry shell
streamlit run src/streamlit/main.py

# Specify different port if 8501 is in use
poetry run streamlit run src/streamlit/main.py --server.port 8502
```

## Development Commands

**Install dependencies:**
```bash
poetry install
```

**Add new dependencies:**
```bash
poetry add package_name
```

**Run tests:**
```bash
poetry run pytest
```

## Architecture

### Environment Configuration
- API keys are loaded from `.env` file at project root using python-dotenv
- The `langchain_helper.py` module loads the `.env` file from a relative path: `Path(__file__).parent.parent.parent / '.env'`
- Alternative: API key can be set in `src/langchain_menu_generator/secret_key.py` (not recommended, deprecated approach)
- The ANTHROPIC_API_KEY environment variable must be set for the application to function

### Application Structure
The application has a two-layer architecture:

1. **UI Layer** (`src/streamlit/main.py`):
   - Streamlit interface with sidebar for country input
   - Imports from `langchain_helper` via sys.path manipulation (adds current directory to path)
   - Displays generated restaurant name as header

2. **Business Logic Layer** (`src/streamlit/langchain_helper.py`):
   - Initializes ChatAnthropic LLM with model "claude-3-7-sonnet-20250219"
   - Uses LangChain's LLMChain with ChatPromptTemplate for restaurant name generation
   - Currently implements only restaurant name generation (menu items generation is commented out)
   - Uses SequentialChain to orchestrate the generation pipeline
   - The function `generate_resturant_name_n_items(country)` returns a dict with key "resturant_name"

### LangChain Chain Architecture
- **name_chain**: LLMChain that generates restaurant names based on country input
- **SequentialChain**: Orchestrates the chain execution with input_variables=["country"] and output_variables=["resturant_name"]
- Menu items chain is currently disabled (commented out in code)

### Import Path Configuration
The `main.py` file modifies `sys.path` to allow importing `langchain_helper` from the same directory. This is necessary because the Streamlit app is run from the project root, but modules need to be imported from the `src/streamlit/` directory.

## Key Configuration Details

**LLM Configuration:**
- Model: claude-3-7-sonnet-20250219
- Temperature: 0.1
- Max retries: 5
- Timeout: None

**Python Version:** Requires Python >=3.12,<4.0

**Package Management:** This project uses Poetry exclusively for dependency management.