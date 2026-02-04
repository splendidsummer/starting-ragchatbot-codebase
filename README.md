<!-- 
icon grab bag
🧠 Brain – highlights AI or reasoning.
🔍 Magnifying glass with tilt – great for search or retrieval.
📚 Stack of books – emphasizes course materials or knowledge base.
🗂️ Card index dividers – works for organized datasets or chunks.
🤖 Robot face – signals an automated assistant or bot persona.
⚙️ Gear – nice for configuration or backend system sections.
🚀 Rocket – perfect for “quick start” or deployment instructions.
🛡️ Shield – conveys security or reliability promises.
📝 Memo – ideal for notes, instructions, or reminders.
🌐 Globe with meridians – fits any integration or API-related section.
quick placement ideas
Title already uses 🧠; you could add 🔍 in the overview header, 📚 beside “Prerequisites,” 🚀 for “Quick Start,” and 🤖 for an FAQ or “Ask the Assistant” section.
In badges or callouts, mix ⚙️ for developer notes, 🛡️ for warnings, and 📝 for tips.

 -->


⚙️ This repo here contains my trial impls of a  [Claude Code Course Materials](https://www.deeplearning.ai/short-courses/claude-code-a-highly-agentic-coding-assistant/).

# 🧠 Course Materials RAG System

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

3. **Set up environment variables**
   
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

