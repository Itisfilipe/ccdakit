# Installation

## Requirements

- Python 3.8 or higher
- lxml >= 4.9.0

## Using pip

```bash
pip install ccdakit
```

## Installation with Extras

```bash
# Development tools
pip install ccdakit[dev]

# Documentation tools
pip install ccdakit[docs]

# Validation utilities
pip install ccdakit[validation]

# Test data generation
pip install ccdakit[test-data]

# All extras
pip install ccdakit[dev,docs,validation,test-data]
```

## For Contributors (uv)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/Itisfilipe/ccdakit.git
cd ccdakit
uv sync --all-extras
```

## Verify Installation

```python
import ccdakit
print(ccdakit.__version__)
```

## Next Steps

- [Quick Start](quickstart.md)
- [Basic Concepts](concepts.md)
