# Development commands for code quality and testing
# Uses UV for dependency management

.PHONY: help format lint type-check test quality install-dev clean

help:
	@echo "Available commands:"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make format        - Format code with Black"
	@echo "  make lint          - Lint code with Ruff"
	@echo "  make type-check    - Type check with mypy"
	@echo "  make test          - Run tests with pytest"
	@echo "  make quality       - Run format, lint, and type-check"
	@echo "  make clean         - Remove cache files and build artifacts"

install-dev:
	uv sync --group dev

format:
	uv run black .

lint:
	uv run ruff check .

type-check:
	uv run mypy backend/

test:
	uv run pytest -v

quality: format lint type-check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete
	find . -type f -name "*.so" -delete
	find . -type f -name "*.c" -delete