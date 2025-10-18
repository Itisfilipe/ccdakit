# Code Systems & Value Sets

Working with medical terminologies in ccdakit.

## Code Systems

Standard medical code systems used in C-CDA.

### Common Systems

| System | OID | Purpose |
|--------|-----|---------|
| SNOMED CT | 2.16.840.1.113883.6.96 | Diagnoses, procedures |
| LOINC | 2.16.840.1.113883.6.1 | Lab tests, vital signs |
| RxNorm | 2.16.840.1.113883.6.88 | Medications |
| ICD-10-CM | 2.16.840.1.113883.6.90 | Diagnoses |
| CVX | 2.16.840.1.113883.12.292 | Vaccines |
| CPT | 2.16.840.1.113883.6.12 | Procedures |

### Using Code Systems

```python
from ccdakit.utils import CodeSystemRegistry

# Get OID
oid = CodeSystemRegistry.get_oid("SNOMED")
# "2.16.840.1.113883.6.96"

# Get name from OID
name = CodeSystemRegistry.get_name("2.16.840.1.113883.6.96")
# "SNOMED"

# Validate system
is_valid = CodeSystemRegistry.is_valid_system("LOINC")
# True

# Get system info
info = CodeSystemRegistry.get_system_info("RxNorm")
# {'oid': '...', 'url': '...', 'description': '...'}

# List all systems
systems = CodeSystemRegistry.list_systems()
```

## Value Sets

Predefined sets of valid codes.

### Available Value Sets

- **PROBLEM_STATUS**: active, inactive, resolved
- **MEDICATION_STATUS**: active, completed, discontinued
- **ALLERGY_STATUS**: active, inactive, resolved
- **ALLERGY_SEVERITY**: mild, moderate, severe
- **SMOKING_STATUS**: current smoker, former smoker, never smoker
- And more...

### Using Value Sets

```python
from ccdakit.utils import ValueSetRegistry

# Check if code is valid
is_valid = ValueSetRegistry.is_valid_code(
    "PROBLEM_STATUS",
    "55561003"  # Active
)

# Get display name
display = ValueSetRegistry.get_display_name(
    "PROBLEM_STATUS",
    "55561003"
)  # "Active"

# Get all codes in a set
codes = ValueSetRegistry.get_codes("PROBLEM_STATUS")
# ["55561003", "73425007", "413322009"]

# Search by display name
matches = ValueSetRegistry.search_by_display(
    "PROBLEM_STATUS",
    "active"
)
# ["55561003"]

# Get code info
info = ValueSetRegistry.get_code_info(
    "PROBLEM_STATUS",
    "55561003"
)
# {'code': '55561003', 'display': 'Active', 'system': 'SNOMED'}
```

## Code Validation

Validate codes against value sets:

```python
# In your business logic
if not ValueSetRegistry.is_valid_code("PROBLEM_STATUS", code):
    raise ValueError(f"Invalid status code: {code}")
```

## Custom Value Sets

Add custom value sets:

```python
custom_codes = {
    "MY_CUSTOM_SET": {
        "oid": "2.16.840.1.113883.3.CUSTOM",
        "name": "My Custom Value Set",
        "codes": {
            "CODE1": {
                "display": "Display Name 1",
                "system": "CUSTOM"
            },
            "CODE2": {
                "display": "Display Name 2",
                "system": "CUSTOM"
            }
        }
    }
}

ValueSetRegistry.VALUE_SETS.update(custom_codes)
```

## Next Steps

- [Working with Sections](sections.md)
- [API Reference](../api/utilities.md)
