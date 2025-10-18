# Contributing to ccdakit

Thank you for your interest in contributing to ccdakit! This document provides guidelines and instructions for contributing to the project.

## Important Notice

**This is an independent, community project not affiliated with HL7 International.** This project was developed extensively with AI assistance. By contributing, you acknowledge:

- This is not an official HL7 project
- Contributions may involve or be assisted by AI tools
- All contributions are subject to the MIT License
- You agree to the terms in our [Disclaimer](docs/about/disclaimer.md)

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](../CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/Itisfilipe/ccdakit.git
cd ccdakit
```

2. **Install uv** (recommended for 10-100x faster package management)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Install dependencies**

```bash
# Using uv (recommended)
uv sync --all-extras

# Or using pip
pip install -e ".[dev,docs,validation]"
```

4. **Download C-CDA 2.1 references** (required for development)

```bash
cd references/
git clone https://github.com/jddamore/ccda-search.git C-CDA_2.1
cd ..
```

> **⚠️ Important**: The C-CDA 2.1 reference documentation is NOT included in the repository. You must download it separately. This reference is essential for implementing new sections correctly according to the official HL7 C-CDA specification. See `references/README.md` for more details.

5. **Verify your setup**

```bash
# Run tests
uv run pytest

# Check code formatting
uv run ruff check ccdakit
uv run ruff format --check ccdakit
```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

1. **Bug Reports** - Found a bug? Let us know!
2. **Feature Requests** - Have an idea? We'd love to hear it!
3. **Documentation** - Improve or add documentation
4. **Code** - Fix bugs or add new features
5. **Tests** - Add or improve test coverage
6. **Examples** - Add example scripts or use cases

### Development Workflow

1. **Create a branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. **Make your changes**

Follow our [coding standards](#coding-standards) and ensure your code is well-tested.

3. **Run tests and linters**

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=ccdakit --cov-report=html

# Format code
uv run ruff format ccdakit tests

# Lint code
uv run ruff check --fix ccdakit tests
```

4. **Commit your changes**

```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve issue with X"
```

We follow [Conventional Commits](https://www.conventionalcommits.org/) style:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `chore:` - Build process or auxiliary tool changes

5. **Push and create a Pull Request**

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Coding Standards

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting. Ruff combines the functionality of black, isort, flake8, and more.

**Key principles:**
- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints for all functions and methods
- Write clear, descriptive variable and function names
- Add docstrings to all public modules, classes, and functions

### Type Hints

This project uses type hints extensively. All public APIs should have complete type annotations.

```python
from typing import Optional, List
from datetime import date

def create_patient(
    first_name: str,
    last_name: str,
    date_of_birth: date,
    sex: str,
    middle_name: Optional[str] = None,
) -> Patient:
    """Create a patient record.

    Args:
        first_name: Patient's first name
        last_name: Patient's last name
        date_of_birth: Patient's date of birth
        sex: Patient's administrative sex (M/F/UN)
        middle_name: Optional middle name

    Returns:
        Patient object with provided information
    """
    ...
```

### Documentation

- **Docstrings**: Use Google-style docstrings
- **Comments**: Use inline comments sparingly and only when the code cannot be made self-explanatory
- **Type hints**: Prefer type hints over type comments

### Architecture Patterns

This project follows specific architectural patterns. Please maintain consistency:

1. **Protocol-Oriented Design**: Use Python protocols (structural subtyping) for data contracts
2. **Builder Pattern**: Use builders for constructing XML elements
3. **Composition over Inheritance**: Favor composition
4. **Version Awareness**: Support multiple C-CDA versions (R2.1, R2.0)

See [Architecture](./docs/development/architecture.md) for detailed design principles.

## Testing

### Test Requirements

- All new code must include tests
- Aim for >90% code coverage
- Tests should be fast and isolated
- Use descriptive test names

### Test Organization

```
tests/
├── test_core/           # Core functionality tests
├── test_protocols/      # Protocol tests
├── test_builders/       # Builder tests
├── test_validators/     # Validation tests
└── test_integration/    # Integration tests
```

### Writing Tests

```python
import pytest
from ccdakit import ClinicalDocument, ProblemsSection
from datetime import date

def test_creates_valid_document():
    """Test that a document with problems section is created successfully."""
    # Arrange
    patient = create_test_patient()
    problems = [create_test_problem()]

    # Act
    doc = ClinicalDocument(
        patient=patient,
        sections=[ProblemsSection(problems=problems)],
    )

    # Assert
    xml = doc.to_string()
    assert "<ClinicalDocument" in xml
    assert "<component>" in xml
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_builders/test_document.py

# Run tests matching pattern
uv run pytest -k "test_problem"

# Run with coverage
uv run pytest --cov=ccdakit --cov-report=html

# Run tests in parallel (faster)
uv run pytest -n auto
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** - If you've changed APIs, update the relevant documentation
2. **Add tests** - Ensure your changes are covered by tests
3. **Update CHANGELOG.md** - Add a brief description of your changes under "Unreleased"
4. **Run the full test suite** - Make sure all tests pass
5. **Create the Pull Request** - Provide a clear description of the changes

### Pull Request Guidelines

Your PR should:
- Have a clear, descriptive title
- Reference any related issues
- Include a description of what changed and why
- Include test results
- Pass all CI checks

**PR Title Format:**
```
feat: add procedures section support
fix: resolve issue with null flavor handling
docs: improve quick start guide
test: add coverage for vital signs organizer
```

### Code Review Process

1. A maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Description** - Clear description of the bug
2. **Steps to Reproduce** - Minimal steps to reproduce the issue
3. **Expected Behavior** - What you expected to happen
4. **Actual Behavior** - What actually happened
5. **Environment**:
   - Python version
   - ccdakit version
   - Operating system
6. **Code Sample** - Minimal code that reproduces the issue

**Bug Report Template:**

```markdown
## Bug Description
[Clear description]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Python version: 3.11.5
- ccdakit version: 0.1.0a1
- OS: macOS 14.0

## Code Sample
```python
# Minimal code to reproduce
```
```

### Feature Requests

When requesting features, please include:

1. **Use Case** - Describe the problem you're trying to solve
2. **Proposed Solution** - Your idea for solving it (if you have one)
3. **Alternatives** - Other approaches you've considered
4. **Additional Context** - Any other relevant information

## Development Tips

### Quick Commands Reference

```bash
# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run tests in parallel
uv run pytest -n auto

# Format code
uv run ruff format ccdakit tests

# Lint code
uv run ruff check --fix ccdakit

# Build package
uv build

# Run example
uv run python examples/generate_ccda.py
```

### Project Structure

Understanding the project structure will help you navigate:

```
ccdakit/
├── ccdakit/                  # Main package
│   ├── core/               # Core infrastructure
│   ├── protocols/          # Data contracts (interfaces)
│   ├── builders/           # XML builders
│   │   ├── entries/       # Entry-level builders
│   │   ├── sections/      # Section builders
│   │   └── header/        # Header components
│   └── validators/         # Validation tools
├── tests/                  # Test suite
├── examples/               # Example scripts
└── docs/                   # Documentation
```

## Questions?

If you have questions:
- Check existing documentation
- Search existing issues
- Create a new issue with your question
- Join our discussions

## AI-Assisted Development

This project embraces AI-assisted development:

- **AI tools are welcome** - Feel free to use AI assistants (Claude, ChatGPT, Copilot, etc.) for contributions
- **Disclose AI usage** - Please note in your PR if significant portions were AI-generated
- **Review is required** - All AI-generated code must be reviewed and tested by humans
- **You're responsible** - Contributors are responsible for the quality and correctness of their contributions, regardless of how they were created

## License

By contributing to ccdakit, you agree that your contributions will be licensed under the MIT License.

## Disclaimer

Contributors should be aware that:
- This is not an official HL7 product
- Always validate implementations against official HL7 specifications
- See full [Disclaimer](docs/about/disclaimer.md) for details

---

Thank you for contributing to ccdakit! 🎉
