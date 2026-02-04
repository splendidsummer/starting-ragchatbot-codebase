# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Retrieval-Augmented Generation (RAG) system for querying course materials using ChromaDB for vector storage and Anthropic's Claude API for AI-powered responses. The system uses semantic search with tool-based retrieval to answer questions about course content.

## Development Commands

### Setup
```bash
# Install dependencies
uv sync

# Set up environment variables
# Create .env file with: ANTHROPIC_API_KEY=your_key_here
```

### Running the Application
```bash
# Quick start (recommended)
./run.sh

# Manual start
cd backend && uv run uvicorn app:app --reload --port 8000
```

The application serves both the API and frontend at `http://localhost:8000`.

### Testing
```bash
# Run all tests
uv run pytest backend/tests/ -v

# Run specific test file
uv run pytest backend/tests/test_api_endpoints.py -v

# Run tests with coverage
uv run pytest backend/tests/ --cov=backend --cov-report=term-missing
```

Tests use pytest with async support. Mock fixtures are defined in `backend/tests/conftest.py`.

## Architecture Overview

### Core Components

**RAGSystem** (`backend/rag_system.py`)
- Main orchestrator that coordinates all components
- Manages document ingestion, query processing, and tool-based search
- Entry point: `query()` method processes user questions using AI with tool calling

**VectorStore** (`backend/vector_store.py`)
- ChromaDB-based storage with two collections:
  - `course_catalog`: Course metadata (titles, instructors, lessons) for semantic course name matching
  - `course_content`: Chunked course material for content search
- Key method: `search()` handles course name resolution and filtered content retrieval
- Uses sentence-transformers (all-MiniLM-L6-v2) for embeddings

**DocumentProcessor** (`backend/document_processor.py`)
- Parses course documents with expected format:
  ```
  Course Title: [title]
  Course Link: [url]
  Course Instructor: [name]
  Lesson N: [lesson title]
  Lesson Link: [url]
  [lesson content]
  ```
- Chunks text using sentence-based splitting with configurable overlap (800 chars, 100 overlap)
- Creates Course and CourseChunk objects for storage

**AIGenerator** (`backend/ai_generator.py`)
- Handles Claude API interactions with tool calling support
- System prompt enforces: one search per query, no meta-commentary, concise responses
- Implements agentic loop: query → tool use → tool execution → final response

**Tool System** (`backend/search_tools.py`)
- `CourseSearchTool`: Semantic search with optional course/lesson filtering
- `ToolManager`: Registers tools and executes them during AI generation
- Tools track sources for UI display

### Data Flow

1. **Document Ingestion**: Documents → DocumentProcessor → Course/CourseChunk objects → VectorStore (catalog + content collections)

2. **Query Processing**:
   - User query → RAGSystem.query()
   - AIGenerator receives query + tools + conversation history
   - Claude decides to use search_course_content tool
   - ToolManager executes search via VectorStore
   - VectorStore resolves course names semantically, applies filters, returns chunks
   - AIGenerator synthesizes final response from search results
   - SessionManager tracks conversation history

### Key Design Patterns

- **Two-tier vector search**: Separate collections for course metadata (fuzzy matching) and content (precise retrieval)
- **Tool-based RAG**: AI decides when/how to search rather than always retrieving context
- **Semantic course resolution**: Partial course names (e.g., "MCP") matched via vector similarity
- **Conversation memory**: SessionManager maintains limited history (MAX_HISTORY=2 exchanges)
- **Async-first architecture**: All components use async/await patterns for I/O operations

## Configuration

All settings in `backend/config.py`:
- `ANTHROPIC_MODEL`: claude-sonnet-4-20250514
- `EMBEDDING_MODEL`: all-MiniLM-L6-v2
- `CHUNK_SIZE`: 800 characters
- `CHUNK_OVERLAP`: 100 characters
- `MAX_RESULTS`: 5 search results
- `MAX_HISTORY`: 2 conversation exchanges

## API Endpoints

- `POST /api/query`: Process user query with optional session_id
- `GET /api/courses`: Get course statistics and titles
- `GET /`: Serves frontend (index.html) and API health check

The API uses FastAPI with automatic OpenAPI documentation at `http://localhost:8000/docs`.

## Document Format Requirements

Course documents must follow this structure:
- Line 1: `Course Title: [title]`
- Line 2: `Course Link: [url]`
- Line 3: `Course Instructor: [name]`
- Subsequent lines: `Lesson N: [title]` followed by optional `Lesson Link: [url]` and lesson content

Documents are loaded from `docs/` folder on startup.

## Development Notes

- **Package Management**: Uses `uv` for dependency management (see `pyproject.toml`)
- **Python Version**: Requires Python 3.13+ (specified in `.python-version`)
- **Frontend**: Static files served from `frontend/` directory
- **Environment**: API key must be set in `.env` as `ANTHROPIC_API_KEY`
- **Testing**: Comprehensive test fixtures in `backend/tests/conftest.py` mock all major components
