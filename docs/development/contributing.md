# Contributing to ccdakit

We welcome contributions! This guide will help you get started.

## Code of Conduct

Please read our [Code of Conduct](../../CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/Itisfilipe/ccdakit.git
cd ccdakit
```

### 2. Set Up Development Environment

```bash
# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras

# Activate virtual environment
source .venv/bin/activate
```

### 3. Download References

```bash
cd references/
git clone https://github.com/jddamore/ccda-search.git C-CDA_2.1
cd ..
```

## Development Workflow

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=ccdakit

# Specific file
pytest tests/test_builders/test_document.py

# Parallel execution
pytest -n auto
```

### Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
pyright ccdakit
```

### Before Committing

```bash
# Run all checks
ruff check . && ruff format . && pytest
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Your Changes

- Write clear, documented code
- Add tests for new functionality
- Update documentation
- Follow existing code style

### 3. Test Your Changes

```bash
pytest
ruff check .
pyright ccdakit
```

### 4. Commit

```bash
git add .
git commit -m "feat: add new feature"
```

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Formatting
- `chore:` Maintenance

### 5. Push and Create PR

```bash
git push origin feature/my-feature
```

Then create a Pull Request on GitHub.

## Adding New Sections

1. Create protocol in `ccdakit/protocols/`
2. Create builder in `ccdakit/builders/sections/`
3. Add tests in `tests/test_builders/`
4. Update documentation
5. Add to exports in `__init__.py`

## Documentation

### Building Docs

```bash
mkdocs serve
```

Visit http://127.0.0.1:8000

### Writing Docs

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Follow existing structure

## Questions?

- Open an issue for bugs
- Start a discussion for questions
- Join our community chat

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
