# Validation Examples

Validating C-CDA documents.

## XSD Validation

### Basic Validation

```python
from ccdakit.validators import XSDValidator

# Create validator
validator = XSDValidator()

# Validate XML string
xml = doc.to_string()
result = validator.validate(xml)

if result.is_valid:
    print("✅ Document is valid!")
else:
    print(f"❌ Found {len(result.issues)} validation errors:")
    for issue in result.issues:
        print(f"  {issue.level.name}: {issue.message}")
        if issue.location:
            print(f"    Location: {issue.location}")
```

### Validation Result Details

```python
result = validator.validate(xml)

# Check validity
print(f"Valid: {result.is_valid}")
print(f"Total issues: {len(result.issues)}")

# Group by level
errors = [i for i in result.issues if i.level == ValidationLevel.ERROR]
warnings = [i for i in result.issues if i.level == ValidationLevel.WARNING]

print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")

# Get issue details
for issue in result.issues:
    print(f"Code: {issue.code}")
    print(f"Message: {issue.message}")
    print(f"Level: {issue.level.name}")
    print(f"Location: {issue.location}")
```

## Custom Validation Rules

### Simple Custom Rule

```python
from ccdakit.validators import ValidationRule, ValidationIssue, ValidationLevel
from lxml import etree
from typing import List

class RequirePatientNameRule(ValidationRule):
    """Ensure patient has a name."""

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find patient name
        names = document.xpath(
            "//cda:patient/cda:name/cda:given/text()",
            namespaces=ns
        )

        if not names:
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                message="Patient must have a given name",
                code="missing_patient_given_name",
                location="//patient/name"
            ))

        return issues

# Use the rule
rule = RequirePatientNameRule()
issues = rule.validate(doc)

for issue in issues:
    print(f"{issue.level.name}: {issue.message}")
```

### Business Rule Example

```python
class MedicationDosageRule(ValidationRule):
    """Validate medication dosages are within safe limits."""

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find all medication dosages
        dosages = document.xpath(
            "//cda:substanceAdministration/cda:doseQuantity/@value",
            namespaces=ns
        )

        for idx, dosage in enumerate(dosages, 1):
            try:
                value = float(dosage)
                if value > 1000:  # Example threshold
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message=f"Unusually high dosage: {value}",
                        code="high_medication_dosage",
                        location=f"//substanceAdministration[{idx}]/doseQuantity"
                    ))
            except ValueError:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Invalid dosage value: {dosage}",
                    code="invalid_dosage_value",
                    location=f"//substanceAdministration[{idx}]/doseQuantity"
                ))

        return issues
```

## Rule Composition

### Multiple Rules

```python
from ccdakit.validators.common_rules import (
    TemplateIDRule,
    PatientNameRule,
    DocumentDateRule,
)

# Create multiple rules
rules = [
    TemplateIDRule(required_templates=[
        "2.16.840.1.113883.10.20.22.1.1",  # C-CDA R2.1
    ]),
    PatientNameRule(require_given=True, require_family=True),
    DocumentDateRule(allow_future=False),
    RequirePatientNameRule(),
    MedicationDosageRule(),
]

# Validate with all rules
all_issues = []
for rule in rules:
    issues = rule.validate(doc)
    all_issues.extend(issues)

# Report
if not all_issues:
    print("✅ All validation rules passed!")
else:
    print(f"❌ Found {len(all_issues)} issues:")
    for issue in all_issues:
        print(f"  {issue.code}: {issue.message}")
```

## Validation During Build

### Enable Build-Time Validation

```python
from ccdakit import configure, CDAConfig

# Enable validation during document generation
configure(CDAConfig(
    validate_on_build=True
))

# Now validation happens automatically
try:
    doc = ClinicalDocument(
        patient=patient,
        sections=[...],
    )
    xml = doc.to_string()  # Validation runs here
    print("✅ Document generated and validated!")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")
    for issue in e.issues:
        print(f"  {issue.message}")
```

## Schema Management

### Check Schema Installation

```python
from ccdakit.validators.utils import SchemaManager

manager = SchemaManager()

if manager.schemas_installed():
    print("✅ Schemas are installed")
    print(f"Location: {manager.get_schema_directory()}")
else:
    print("❌ Schemas not found")
    print("Download from: https://www.hl7.org/...")
```

### Install Schemas

```python
# Option 1: Manual download (recommended)
# 1. Visit https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492
# 2. Download CCDA_R2.1_Schemas.zip
# 3. Extract to schemas/ directory

# Option 2: Programmatic (may not work due to HL7 licensing)
from ccdakit.validators.utils import print_schema_installation_help

print_schema_installation_help()
```

## Next Steps

- [Validation Guide](../guides/validation.md)
- [API Reference](../api/validators.md)
- [Custom Rules](../guides/validation.md#custom-validation-rules)
