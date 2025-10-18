# Version Management

How ccdakit handles multiple C-CDA versions.

## Supported Versions

### C-CDA R2.1 (Default)

- **Extension**: 2015-08-01
- **Status**: Fully supported
- **Recommendation**: Use this for new implementations

### C-CDA R2.0

- **Extension**: 2014-06-09
- **Status**: Fully supported
- **Use case**: Legacy system compatibility


## Version Differences

### Template IDs

```python
# R2.1
"2.16.840.1.113883.10.20.22.2.5.1" extension="2015-08-01"

# R2.0
"2.16.840.1.113883.10.20.22.2.5.1" extension="2014-06-09"
```

### Required Elements

Some elements are version-specific. ccdakit handles this automatically.

## Specifying Versions

### Document Level

```python
from ccdakit import ClinicalDocument, CDAVersion

doc = ClinicalDocument(
    patient=patient,
    sections=[...],
    version=CDAVersion.R2_1  # Document-wide version
)
```

### Section Level

```python
from ccdakit import ProblemsSection, CDAVersion

# Override for specific section
section = ProblemsSection(
    problems=problems,
    version=CDAVersion.R2_0  # This section uses R2.0
)
```

### Global Configuration

```python
from ccdakit import configure, CDAConfig, CDAVersion

configure(CDAConfig(
    version=CDAVersion.R2_1  # Default for all documents
))
```

## Version Resolution

Priority order:
1. Section-level version (if specified)
2. Document-level version (if specified)
3. Global configuration version
4. Default (R2.1)

## Migration

### R2.0 → R2.1

Most code works without changes. Key differences:

1. Template extensions updated
2. Some new optional elements
3. Additional validation rules

```python
# Update version only
doc = ClinicalDocument(
    patient=patient,
    sections=[...],
    version=CDAVersion.R2_1  # Changed from R2_0
)
```

## Next Steps

- [Architecture](architecture.md)
- [Configuration](../guides/configuration.md)
