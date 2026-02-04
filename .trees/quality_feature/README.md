# Course Materials RAG System

A Retrieval-Augmented Generation (RAG) system designed to answer questions about course materials using semantic search and AI-powered responses.

## Overview

This application is a full-stack web application that enables users to query course materials and receive intelligent, context-aware responses. It uses ChromaDB for vector storage, Anthropic's Claude for AI generation, and provides a web interface for interaction.


## Prerequisites

- Python 3.13 or higher
- uv (Python package manager)
- An Anthropic API key (for Claude AI)
- **For Windows**: Use Git Bash to run the application commands - [Download Git for Windows](https://git-scm.com/downloads/win)

## Installation

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Python dependencies**
   ```bash
   uv sync
   ```

3. **Install development dependencies** (optional, for code quality tools)
   ```bash
   uv sync --extra dev
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Running the Application

### Quick Start

Use the provided shell script:
```bash
chmod +x run.sh
./run.sh
```

### Manual Start

```bash
cd backend
uv run uvicorn app:app --reload --port 8000
```

The application will be available at:
- Web Interface: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

## Code Quality and Development Tools

The project includes several code quality tools to maintain consistent formatting and catch potential issues:

### Formatters and Linters
- **Black**: Automatic code formatting (line length: 88)
- **Ruff**: Fast Python linter with auto-fixing capabilities
- **EditorConfig**: Consistent editor settings across IDEs
- **Pre-commit**: Git hooks for automated checks before commits

### Type Checking and Testing
- **mypy**: Static type checking for Python code
- **pytest**: Testing framework (no tests yet, but infrastructure ready)

### Development Commands

All quality checks are available via `Makefile` commands:

```bash
# Install development dependencies
make install-dev

# Format code with Black
make format

# Lint code with Ruff
make lint

# Type check with mypy
make type-check

# Run tests with pytest
make test

# Run all quality checks (format, lint, type-check)
make quality

# Clean up cache files and build artifacts
make clean
```

### Pre-commit Hooks

To automatically run quality checks before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Manually run hooks on all files
pre-commit run --all-files
```

### Configuration Files
- `pyproject.toml`: Tool configurations (Black, Ruff, mypy) and dependencies
- `.pre-commit-config.yaml`: Pre-commit hooks definition
- `.editorconfig`: Editor settings
- `Makefile`: Development commands

### Workflow Recommendations
1. Run `make quality` before committing to ensure code meets standards
2. Use `pre-commit install` to automate checks
3. Fix any linting issues with `make lint` (Ruff can auto-fix many issues)
4. Ensure type checking passes with `make type-check`

