# Development Setup

Complete setup guide for contributors.

## Prerequisites

- Python 3.8 or higher
- Git
- uv (recommended) or pip

## Initial Setup

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/Itisfilipe/ccdakit.git
cd ccdakit
```

### 2. Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install Dependencies

```bash
uv sync --all-extras
```

This creates a virtual environment at `.venv/` and installs:
- Production dependencies
- Development tools (pytest, ruff, pyright)
- Documentation tools (mkdocs)
- Optional extras

### 4. Activate Environment

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 5. Download C-CDA References

```bash
mkdir -p references
cd references
git clone https://github.com/jddamore/ccda-search.git C-CDA_2.1
cd ..
```

## Development Tools

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=ccdakit --cov-report=html

# Specific test
pytest tests/test_builders/test_document.py::TestClinicalDocument

# Parallel
pytest -n auto

# Watch mode
pytest-watch
```

### Code Quality

```bash
# Lint
ruff check .

# Auto-fix
ruff check --fix .

# Format
ruff format .

# Type check
pyright ccdakit
```

### Documentation

```bash
# Serve docs locally
mkdocs serve

# Build docs
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## IDE Setup

### VS Code

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.linting.enabled": false,
  "ruff.enable": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

Recommended extensions:
- Python
- Pylance
- Ruff

### PyCharm

1. Open project
2. Select `.venv/bin/python` as interpreter
3. Enable pytest as test runner
4. Configure Ruff as external tool

## Project Structure

```
ccdakit/
├── ccdakit/              # Source code
│   ├── core/            # Core classes
│   ├── protocols/       # Protocol definitions
│   ├── builders/        # XML builders
│   ├── validators/      # Validation
│   └── utils/           # Utilities
├── tests/               # Test suite
├── examples/            # Example scripts
├── docs/                # Documentation
├── references/          # C-CDA references
└── schemas/             # XSD schemas
```

## Common Tasks

### Add a New Section

1. Create protocol: `ccdakit/protocols/mysection.py`
2. Create builder: `ccdakit/builders/sections/mysection.py`
3. Add tests: `tests/test_builders/test_mysection.py`
4. Update exports: `ccdakit/__init__.py`
5. Document it: `docs/guides/sections.md`

### Run Specific Tests

```bash
# Single test
pytest tests/test_core/test_config.py::test_configure

# All unit tests
pytest tests/test_core

# Integration tests
pytest tests/test_integration

# Coverage for specific module
pytest --cov=ccdakit.builders tests/test_builders
```

### Debug Tests

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use pytest
pytest --pdb
```

## Troubleshooting

### Import Errors

```bash
# Reinstall in development mode
uv pip install -e .
```

### Test Failures

```bash
# Verbose output
pytest -vv

# Show print statements
pytest -s

# Stop on first failure
pytest -x
```

### Type Errors

```bash
# Check specific file
pyright ccdakit/builders/document.py

# Ignore specific errors
# Add to pyrightconfig.json
```

## Next Steps

- [Contributing Guide](contributing.md)
- [Testing Guide](testing.md)
- [Architecture](architecture.md)
