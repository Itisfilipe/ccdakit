# Validation

Validate C-CDA documents using XSD schemas and Schematron rules.

## XSD Validation

### Setup

Download C-CDA schemas from HL7:

```bash
# Visit: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492
# Download and extract to schemas/ directory
```

### Basic Validation

```python
from ccdakit.validators import XSDValidator

validator = XSDValidator()
result = validator.validate(xml_string)

if result.is_valid:
    print("✅ Valid C-CDA!")
else:
    print("❌ Validation errors:")
    for issue in result.issues:
        print(f"  - {issue.message} at {issue.location}")
```

### Validation Result

```python
class ValidationResult:
    is_valid: bool
    issues: List[ValidationIssue]

class ValidationIssue:
    level: ValidationLevel  # ERROR, WARNING, INFO
    message: str
    code: str
    location: Optional[str]
```

## Schematron Validation

More advanced rule-based validation:

```python
from ccdakit.validators import SchematronValidator

validator = SchematronValidator(
    schematron_path="path/to/ccda.sch"
)
result = validator.validate(xml_string)
```

## Custom Validation Rules

Create custom business rules:

```python
from ccdakit.validators import ValidationRule, ValidationIssue, ValidationLevel
from lxml import etree

class CustomRule(ValidationRule):
    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        issues = []

        # Your validation logic
        if condition_not_met:
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                message="Custom validation failed",
                code="custom_rule_01",
                location="//element/path",
            ))

        return issues

# Use it
rule = CustomRule()
issues = rule.validate(doc)
```

## Schema Manager

Manage XSD schemas:

```python
from ccdakit.validators.utils import SchemaManager

manager = SchemaManager()

# Check if schemas installed
if not manager.schemas_installed():
    print("Please install C-CDA schemas")

# Get schema directory
schema_dir = manager.get_schema_directory()
```

## Validation During Build

Enable validation during document generation:

```python
from ccdakit import configure, CDAConfig

configure(CDAConfig(
    validate_on_build=True  # Validate as you build
))
```

## Next Steps

- [Custom Rules Guide](../examples/validation.md)
- [API Reference](../api/validators.md)
