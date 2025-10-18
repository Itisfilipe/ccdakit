# Using uv with ccdakit

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management.

## Why uv?

- **10-100x faster** than pip
- **Unified tooling** - manages Python versions, virtual environments, and dependencies
- **Reproducible builds** with `uv.lock`
- **Drop-in replacement** for pip, pip-tools, and venv
- Created by Astral (makers of Ruff)

## Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

## Common Commands

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/Itisfilipe/ccdakit.git
cd ccdakit

# Sync dependencies (creates .venv and installs everything)
uv sync

# Or sync with all optional dependencies (dev, docs, validation)
uv sync --all-extras
```

### Running Commands

```bash
# Run pytest
uv run pytest

# Run pytest with coverage
uv run pytest --cov=ccdakit

# Run ruff format
uv run ruff format ccdakit tests

# Run ruff
uv run ruff check ccdakit
```

### Managing Dependencies

```bash
# Add a new dependency
uv add requests

# Add a dev dependency
uv add --dev pytest-mock

# Update all dependencies
uv sync --upgrade

# Update specific package
uv sync --upgrade lxml
```

### Python Version Management

```bash
# Install a specific Python version
uv python install 3.12

# Use a specific Python version for this project
uv python pin 3.12

# List available Python versions
uv python list
```

### Virtual Environment

```bash
# The .venv directory is created automatically by uv sync

# Activate the virtual environment (if you need direct access)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

## Development Workflow

### 1. Initial Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repository>
cd ccdakit
uv sync --all-extras
```

### 2. Daily Development

```bash
# Run tests before starting work
uv run pytest

# Make changes to code...

# Run tests after changes
uv run pytest tests/test_core/

# Format code
uv run ruff format ccdakit tests

# Lint
uv run ruff check ccdakit
```

### 3. Adding Features

```bash
# If you need a new dependency
uv add package-name

# If it's a dev dependency
uv add --dev package-name

# Update pyproject.toml manually if needed
# Then run:
uv sync
```

### 4. Before Committing

```bash
# Run full test suite
uv run pytest

# Check coverage
uv run pytest --cov=ccdakit --cov-report=term-missing

# Format and lint
uv run ruff format ccdakit tests
uv run ruff check ccdakit

# Commit (uv.lock will be included automatically)
git add .
git commit -m "Your commit message"
```

## uv vs pip/venv Comparison

| Task | pip/venv | uv |
|------|----------|-----|
| Create venv | `python -m venv .venv` | Automatic with `uv sync` |
| Activate venv | `source .venv/bin/activate` | Not needed for `uv run` |
| Install deps | `pip install -e ".[dev]"` | `uv sync --all-extras` |
| Run tests | `pytest` | `uv run pytest` |
| Add package | `pip install pkg && pip freeze` | `uv add pkg` |
| Lock deps | `pip freeze > requirements.txt` | Automatic `uv.lock` |
| Update deps | `pip install --upgrade pkg` | `uv sync --upgrade` |

## Project-Specific Commands

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test File

```bash
uv run pytest tests/test_core/test_base.py
```

### Run Tests with Coverage Report

```bash
uv run pytest --cov=ccdakit --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Code Formatting

```bash
uv run ruff format ccdakit tests
```

### Linting

```bash
uv run ruff check ccdakit
uv run ruff check --fix ccdakit  # Auto-fix issues
```

### Build Documentation

```bash
uv run mkdocs serve  # Live preview
uv run mkdocs build  # Build static site
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest --cov=ccdakit
```

## Troubleshooting

### uv.lock conflicts

```bash
# If you have merge conflicts in uv.lock
uv sync --upgrade
git add uv.lock
```

### Corrupted cache

```bash
# Clear uv cache
uv cache clean
uv sync
```

### Python version issues

```bash
# Check which Python uv is using
uv python list

# Pin to specific version
uv python pin 3.12

# Install specific version
uv python install 3.12
```

### Package not found

```bash
# Update the lock file
uv sync --upgrade

# Force reinstall
rm -rf .venv
uv sync --all-extras
```

## Benefits for ccdakit

1. **Fast CI/CD**: Tests run significantly faster in CI pipelines
2. **Reproducible**: `uv.lock` ensures everyone has identical dependencies
3. **Simple workflow**: `uv run` eliminates need to activate venv
4. **Version management**: Built-in Python version management
5. **Better errors**: Clear, actionable error messages

## Migration from pip

If you were using pip before:

```bash
# Remove old virtual environment
rm -rf venv/ .venv/

# Remove old lock files (if any)
rm -f requirements.txt requirements-dev.txt

# Initialize with uv
uv sync --all-extras

# Test that everything works
uv run pytest
```

## Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [Migration Guide](https://docs.astral.sh/uv/pip/compatibility/)

## Quick Reference Card

```bash
# Setup
uv sync                    # Install dependencies
uv sync --all-extras       # Install with optional deps
uv sync --upgrade          # Update all dependencies

# Running
uv run <command>           # Run command in project env
uv run pytest             # Run tests
uv run python script.py   # Run Python script

# Managing Dependencies
uv add <package>          # Add dependency
uv add --dev <package>    # Add dev dependency
uv remove <package>       # Remove dependency

# Python Versions
uv python install 3.12    # Install Python version
uv python pin 3.12        # Pin project to version
uv python list            # List installed versions

# Build & Publish
uv build                  # Build distribution
uv publish                # Publish to PyPI
```

---

**Note**: The `uv.lock` file is committed to version control to ensure reproducible builds across all environments.
