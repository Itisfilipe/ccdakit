# Configuration

Configure ccdakit globally or per-document.

## Global Configuration

```python
from ccdakit import configure, CDAConfig, OrganizationInfo, CDAVersion

config = CDAConfig(
    organization=OrganizationInfo(
        name="Example Medical Center",
        npi="1234567890",
        oid_root="2.16.840.1.113883.3.EXAMPLE",
        address="123 Main St",
        city="Boston",
        state="MA",
        postal_code="02101",
        country="US",
        telecom="tel:617-555-1234",
    ),
    version=CDAVersion.R2_1,
    generate_narrative=True,
    validate_on_build=False,
)

configure(config)
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `organization` | `OrganizationInfo` | Required | Your organization details |
| `version` | `CDAVersion` | `R2_1` | Default C-CDA version |
| `generate_narrative` | `bool` | `True` | Auto-generate HTML tables |
| `validate_on_build` | `bool` | `False` | Validate during generation |

## Getting Configuration

```python
from ccdakit import get_config

current = get_config()
print(current.version)
```

## Resetting Configuration

```python
from ccdakit import reset_config

reset_config()  # Back to defaults
```

## Per-Document Configuration

Override global config:

```python
doc = ClinicalDocument(
    patient=patient,
    sections=[...],
    version=CDAVersion.R2_0,  # Override version
)
```

## Environment-Specific Config

```python
import os
from ccdakit import configure, CDAConfig, OrganizationInfo

# Load from environment
config = CDAConfig(
    organization=OrganizationInfo(
        name=os.getenv("ORG_NAME"),
        npi=os.getenv("ORG_NPI"),
        oid_root=os.getenv("ORG_OID_ROOT"),
    ),
)
configure(config)
```

## Next Steps

- [Validation](validation.md)
- [API Reference](../api/core.md)
