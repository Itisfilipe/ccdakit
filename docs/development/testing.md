# Testing Guide

Comprehensive testing guide for ccdakit.

## Test Organization

```
tests/
├── test_core/           # Core functionality
├── test_protocols/      # Protocol tests
├── test_builders/       # Builder tests
│   ├── test_document.py
│   ├── test_sections/
│   └── test_entries/
├── test_validators/     # Validation tests
├── test_utils/          # Utility tests
└── test_integration/    # Integration tests
```

## Running Tests

### Basic Commands

```bash
# All tests
pytest

# Specific file
pytest tests/test_builders/test_document.py

# Specific test
pytest tests/test_builders/test_document.py::TestClinicalDocument::test_basic_document

# With coverage
pytest --cov=ccdakit --cov-report=html

# Parallel execution
pytest -n auto
```

### Test Markers

```bash
# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# Validation tests (require schemas)
pytest -m validation

# Skip slow tests
pytest -m "not slow"
```

## Writing Tests

### Unit Test Example

```python
import pytest
from datetime import date
from ccdakit import ProblemsSection, CDAVersion

class TestProblemsSection:
    def test_basic_section(self):
        """Test basic problems section creation."""
        # Arrange
        class Problem:
            @property
            def name(self):
                return "Diabetes"

            @property
            def code(self):
                return "73211009"

            @property
            def code_system(self):
                return "SNOMED"

            @property
            def status(self):
                return "active"

            @property
            def onset_date(self):
                return date(2020, 1, 1)

        problems = [Problem()]

        # Act
        section = ProblemsSection(
            problems=problems,
            version=CDAVersion.R2_1
        )
        element = section.build()

        # Assert
        assert element is not None
        assert element.tag.endswith("section")
```

### Integration Test Example

```python
@pytest.mark.integration
def test_complete_document_generation():
    """Test complete C-CDA document generation."""
    from ccdakit import ClinicalDocument, ProblemsSection

    # Create full document
    doc = ClinicalDocument(
        patient=patient,
        sections=[
            ProblemsSection(problems=problems, version=CDAVersion.R2_1),
        ],
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml = doc.to_string()

    # Validate structure
    assert "<?xml" in xml
    assert "ClinicalDocument" in xml
    assert "section" in xml
```

### Validation Test Example

```python
@pytest.mark.validation
def test_xsd_validation():
    """Test XSD validation of generated document."""
    from ccdakit.validators import XSDValidator

    # Generate document
    xml = doc.to_string()

    # Validate
    validator = XSDValidator()
    result = validator.validate(xml)

    # Check result
    assert result.is_valid
    assert len(result.issues) == 0
```

## Test Fixtures

### Common Fixtures

```python
import pytest
from datetime import date

@pytest.fixture
def sample_patient():
    """Sample patient for testing."""
    class Patient:
        @property
        def first_name(self):
            return "John"

        @property
        def last_name(self):
            return "Doe"

        @property
        def date_of_birth(self):
            return date(1970, 1, 1)

        @property
        def sex(self):
            return "M"

    return Patient()

@pytest.fixture
def sample_problem():
    """Sample problem for testing."""
    class Problem:
        @property
        def name(self):
            return "Diabetes"

        @property
        def code(self):
            return "73211009"

        @property
        def code_system(self):
            return "SNOMED"

        @property
        def status(self):
            return "active"

        @property
        def onset_date(self):
            return date(2020, 1, 1)

    return Problem()
```

### Using Fixtures

```python
def test_with_fixtures(sample_patient, sample_problem):
    """Test using fixtures."""
    doc = ClinicalDocument(
        patient=sample_patient,
        sections=[
            ProblemsSection(
                problems=[sample_problem],
                version=CDAVersion.R2_1
            ),
        ],
    )
    assert doc is not None
```

## Coverage

### Generate Coverage Report

```bash
# HTML report
pytest --cov=ccdakit --cov-report=html

# Terminal report
pytest --cov=ccdakit --cov-report=term-missing

# XML for CI
pytest --cov=ccdakit --cov-report=xml
```

### Coverage Configuration

In `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["ccdakit"]
omit = ["tests/*", "examples/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install uv
          uv sync --all-extras

      - name: Run tests
        run: pytest --cov=ccdakit

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Best Practices

1. **Test naming**: Use descriptive names (test_what_when_expected)
2. **Arrange-Act-Assert**: Follow AAA pattern
3. **One assertion per test**: Keep tests focused
4. **Use fixtures**: Reduce duplication
5. **Mock external dependencies**: Keep tests fast
6. **Test edge cases**: Null, empty, invalid inputs
7. **Document complex tests**: Add docstrings

## Next Steps

- [Contributing Guide](contributing.md)
- [Development Setup](setup.md)
- [Architecture](architecture.md)
