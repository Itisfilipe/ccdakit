# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ccdakit is a Python library for programmatic generation of HL7 C-CDA (Consolidated Clinical Document Architecture) clinical documents. It uses protocol-oriented design (structural typing) to work with any data model without inheritance requirements.

**Key facts:**
- Python 3.8+ required
- Uses `uv` for package management
- 39 C-CDA sections implemented
- Multi-version support: C-CDA R2.1 (primary) and R2.0

## Common Commands

```bash
# Install dependencies
uv sync --all-extras

# Run all tests
uv run pytest

# Run tests in parallel
uv run pytest -n auto

# Run specific test file
uv run pytest tests/test_builders/test_sections/test_problems.py -v

# Run single test
uv run pytest tests/test_builders/test_sections/test_problems.py::test_name -v

# Format code
uv run ruff format ccdakit tests

# Lint and auto-fix
uv run ruff check --fix ccdakit tests

# Type check
uv run pyright ccdakit

# Run example
uv run python examples/generate_ccda.py
```

## Architecture

```
ccdakit/
├── core/           # CDAElement base, CDAVersion, CDAConfig, validation
├── protocols/      # Data contracts (39 protocol files using typing.Protocol)
├── builders/
│   ├── document.py     # ClinicalDocument main builder
│   ├── documents/      # Document variants (CCD, Discharge Summary)
│   ├── sections/       # 39 section builders (problems, medications, etc.)
│   ├── entries/        # Entry-level builders
│   ├── header/         # Header components (patient, author, custodian)
│   └── common.py       # Shared builders (Code, StatusCode, etc.)
├── validators/     # XSD and Schematron validation
├── cli/            # Typer CLI with Flask web UI
└── utils/          # Code systems, value sets, test data generation
```

**Design pattern:** Protocols define data contracts that any object can satisfy via duck typing. Section builders accept protocol-compliant objects and generate XML.

```python
# Protocol defines interface
class ProblemProtocol(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def code(self) -> str: ...

# Any class with matching properties works
section = ProblemsSection(problems=[your_problem_objects])
```

## Section Builder Pattern

All sections follow this structure:

```python
class SectionNameSection(CDAElement):
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.X",
                extension="2015-08-01",
                description="Section description"
            ),
        ],
        CDAVersion.R2_0: [...]
    }

    def __init__(self, items: Sequence[ItemProtocol], version: CDAVersion = CDAVersion.R2_1):
        super().__init__(version=version)
        self.items = items

    def build(self) -> etree.Element:
        section = etree.Element(f"{{{NS}}}section")
        # ... XML construction
        return section
```

## XML Namespace

Always use the C-CDA namespace constant:

```python
NS = "urn:hl7-org:v3"
element = etree.Element(f"{{{NS}}}tagname")
```

## Code Standards

- Line length: 100 characters
- Type hints: Required for all public APIs
- Docstrings: Google-style format
- Linting: Ruff (replaces black, isort, flake8)
- Commit style: Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`)

## C-CDA Reference Documentation

HL7 specifications are in `references/C-CDA_2.1/` (must be downloaded separately):

```bash
cd references && git clone https://github.com/jddamore/ccda-search.git C-CDA_2.1
```

- HTML templates: `references/C-CDA_2.1/templates/{oid}.html`
- Metadata: `references/C-CDA_2.1/data.json`

## Adding a New Section

1. Find template ID and read spec from `references/C-CDA_2.1/templates/{oid}.html`
2. Create protocol in `ccdakit/protocols/<section_name>.py`
3. Create builder in `ccdakit/builders/sections/<section_name>.py`
4. Add tests in `tests/test_builders/test_sections/test_<section_name>.py`
5. Update exports in `ccdakit/builders/sections/__init__.py`
6. Run: `uv run pytest && uv run ruff check --fix ccdakit && uv run pyright ccdakit`

## Custom Agents

This project has specialized agents in `.claude/agents/`:
- `section-builder` - Implement C-CDA section builders
- `protocol-gen` - Create Protocol definitions
- `integration-test` - Create integration tests for C-CDA documents
- `validator-test` - Create validation tests
- `cli-command` - Build CLI commands with Typer/Rich
- `ccda-review` - Review code for C-CDA compliance
- `doc-sync` - Synchronize documentation
- `release-prep` - Prepare release packages

Agents can run in parallel for faster development.

## Important Notes

- This is an independent project, not affiliated with HL7 International
- Always validate generated documents against official HL7 specifications before production use
- Test coverage target: >90%
