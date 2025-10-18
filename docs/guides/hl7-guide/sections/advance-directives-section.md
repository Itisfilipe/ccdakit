# Advance Directives Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.21.1`
**Version:** 2015-08-01 (R2.1 | R2.0)
**Badge:** Extended Section

## Overview

The **Advance Directives Section (entries required)** contains advance directive data and references to supporting documentation. Advance directives are legal documents that record a person's wishes about life-sustaining medical treatment in the event they become unable to make decisions for themselves.

This section includes:
- **Living Wills:** Instructions about life-sustaining treatment
- **Healthcare Proxies/Power of Attorney:** Designated decision-makers
- **Resuscitation Status:** Do Not Resuscitate (DNR), Do Not Intubate (DNI), Full Code
- **Organ Donation:** Organ and tissue donation preferences
- **POLST/MOLST:** Physician/Medical Orders for Life-Sustaining Treatment

Understanding and respecting advance directives is essential for patient-centered care and honoring patient autonomy.

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.21.1`
- **Extension:** `2015-08-01`
- **LOINC Code:** `42348-3` (Advance Directives)

### Conformance Requirements
- **MAY** contain `@nullFlavor="NI"` if no information available (CONF:1198-32800)
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1198-30227)
- **SHALL** contain exactly one [1..1] `code` with code="42348-3" from LOINC (CONF:1198-32929)
- **SHALL** contain exactly one [1..1] `title` (CONF:1198-32932)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1198-32933)
- If `@nullFlavor` not present, **SHALL** contain at least one [1..*] `entry` (CONF:1198-30235)
- Each `entry` **SHALL** contain Advance Directive Observation (CONF:1198-30236, 32881)

### Cardinality
- **Section:** Optional
- **Entries:** Required if not using nullFlavor (1..*)
- **Advance Directive Observations:** One per entry

## Protocol Requirements

The section uses the `AdvanceDirectiveProtocol` from `ccdakit.protocols.advance_directive`:

### Required Properties
```python
@property
def directive_type(self) -> str:
    """Type: 'Resuscitate', 'Do Not Resuscitate', 'Living Will', etc."""

@property
def directive_value(self) -> str:
    """Detailed directive: 'Full code', 'No intubation', etc."""
```

### Optional Properties
```python
@property
def directive_type_code(self) -> Optional[str]:
    """Code for directive type (SNOMED CT or LOINC)"""

@property
def directive_type_code_system(self) -> Optional[str]:
    """Code system for directive type code"""

@property
def directive_value_code(self) -> Optional[str]:
    """Code for directive value (typically SNOMED CT)"""

@property
def directive_value_code_system(self) -> Optional[str]:
    """Code system for directive value code"""

@property
def start_date(self) -> Optional[date]:
    """Date when advance directive becomes effective"""

@property
def end_date(self) -> Optional[date]:
    """Date when advance directive ends or expires"""

@property
def custodian_name(self) -> Optional[str]:
    """Name of healthcare agent/proxy/custodian"""

@property
def custodian_relationship(self) -> Optional[str]:
    """Relationship to patient: 'Spouse', 'Child', 'Attorney', etc."""

@property
def custodian_relationship_code(self) -> Optional[str]:
    """Code for custodian relationship"""

@property
def custodian_phone(self) -> Optional[str]:
    """Contact phone number for custodian"""

@property
def custodian_address(self) -> Optional[str]:
    """Address of custodian"""

@property
def verifier_name(self) -> Optional[str]:
    """Name of clinician who verified the directive"""

@property
def verification_date(self) -> Optional[date]:
    """Date when directive was verified"""

@property
def document_id(self) -> Optional[str]:
    """Identifier for the advance directive document"""

@property
def document_url(self) -> Optional[str]:
    """URL reference to the advance directive document"""

@property
def document_description(self) -> Optional[str]:
    """Description of the advance directive document"""
```

## Code Example

### Basic Usage

```python
from datetime import date
from ccdakit import AdvanceDirectivesSection, CDAVersion

# Define advance directives
directives = [
    {
        "directive_type": "Resuscitation Status",
        "directive_value": "Do Not Resuscitate (DNR)",
        "directive_type_code": "304251008",
        "directive_type_code_system": "SNOMED",
        "directive_value_code": "304253006",
        "directive_value_code_system": "SNOMED",
        "start_date": date(2023, 6, 15),
        "verifier_name": "Dr. Sarah Johnson",
        "verification_date": date(2024, 1, 10),
    },
    {
        "directive_type": "Healthcare Proxy",
        "directive_value": "Jane Doe is designated healthcare proxy",
        "start_date": date(2023, 6, 15),
        "custodian_name": "Jane Doe",
        "custodian_relationship": "Spouse",
        "custodian_phone": "555-123-4567",
        "custodian_address": "123 Main St, Anytown, ST 12345",
    }
]

# Create section
section = AdvanceDirectivesSection(
    directives=directives,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Section with No Information

```python
# When no information is available
section = AdvanceDirectivesSection(
    directives=[],
    null_flavor="NI",  # No information
    version=CDAVersion.R2_1
)
```

### Empty Section (No Directives on File)

```python
# When patient has no advance directives
section = AdvanceDirectivesSection(
    directives=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No advance directives on file"
```

### Comprehensive Advance Directives

```python
directives = [
    # DNR/DNI Status
    {
        "directive_type": "Resuscitation Status",
        "directive_value": "Do Not Resuscitate, Do Not Intubate",
        "directive_type_code": "304251008",
        "directive_type_code_system": "SNOMED",
        "directive_value_code": "304253006",
        "directive_value_code_system": "SNOMED",
        "start_date": date(2024, 1, 15),
        "verifier_name": "Dr. Michael Chen",
        "verification_date": date(2024, 3, 1),
    },

    # Living Will
    {
        "directive_type": "Living Will",
        "directive_value": "No artificial nutrition or hydration if permanently unconscious",
        "directive_type_code": "52765003",
        "directive_type_code_system": "SNOMED",
        "start_date": date(2023, 8, 20),
        "document_id": "LW-2023-08-20-001",
        "document_url": "https://example.org/documents/living-will-12345.pdf",
        "custodian_name": "John Smith",
        "custodian_relationship": "Attorney",
        "custodian_phone": "555-987-6543",
    },

    # Healthcare Proxy
    {
        "directive_type": "Healthcare Power of Attorney",
        "directive_value": "Sarah Johnson authorized to make all healthcare decisions",
        "directive_type_code": "71388002",
        "directive_type_code_system": "SNOMED",
        "start_date": date(2023, 8, 20),
        "custodian_name": "Sarah Johnson",
        "custodian_relationship": "Daughter",
        "custodian_relationship_code": "DAUC",
        "custodian_phone": "555-234-5678",
        "custodian_address": "456 Oak Ave, Anytown, ST 12345",
    },

    # Organ Donation
    {
        "directive_type": "Consent for Organ Donation",
        "directive_value": "Willing to donate all organs and tissues",
        "directive_type_code": "304252001",
        "directive_type_code_system": "SNOMED",
        "start_date": date(2023, 8, 20),
        "document_id": "donor-registry-123456",
    }
]

section = AdvanceDirectivesSection(directives=directives)
```

### POLST Form

```python
# Physician Orders for Life-Sustaining Treatment
polst_directive = {
    "directive_type": "POLST - Medical Orders",
    "directive_value": "Comfort Measures Only - DNR, no hospital transfer, "
                      "comfort-focused treatment only",
    "directive_type_code": "304252001",
    "directive_type_code_system": "SNOMED",
    "start_date": date(2024, 2, 10),
    "verifier_name": "Dr. Amanda Rodriguez",
    "verification_date": date(2024, 2, 10),
    "document_id": "POLST-2024-02-10",
    "document_url": "https://example.org/polst/patient-12345.pdf",
}

section = AdvanceDirectivesSection(directives=[polst_directive])
```

### With Document Reference

```python
directive_with_doc = {
    "directive_type": "Living Will",
    "directive_value": "See attached living will document",
    "start_date": date(2023, 5, 1),
    "document_id": "LW-2023-001",
    "document_url": "https://hospital.example.org/documents/living-will-patient123.pdf",
    "document_description": "Living Will executed May 1, 2023",
    "custodian_name": "Legal Department",
    "verifier_name": "Dr. Emily White",
    "verification_date": date(2024, 1, 15),
}

section = AdvanceDirectivesSection(directives=[directive_with_doc])
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class AdvanceDirective:
    """Custom advance directive implementation."""
    directive_type: str
    directive_value: str
    directive_type_code: Optional[str] = None
    directive_type_code_system: Optional[str] = None
    directive_value_code: Optional[str] = None
    directive_value_code_system: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    custodian_name: Optional[str] = None
    custodian_relationship: Optional[str] = None
    custodian_relationship_code: Optional[str] = None
    custodian_phone: Optional[str] = None
    custodian_address: Optional[str] = None
    verifier_name: Optional[str] = None
    verification_date: Optional[date] = None
    document_id: Optional[str] = None
    document_url: Optional[str] = None
    document_description: Optional[str] = None

# Create directives
directives = [
    AdvanceDirective(
        directive_type="Do Not Intubate",
        directive_value="Patient does not wish to be intubated",
        directive_type_code="304251008",
        directive_type_code_system="SNOMED",
        start_date=date(2024, 1, 1),
        verifier_name="Dr. Robert Lee",
        verification_date=date(2024, 3, 15),
    )
]

section = AdvanceDirectivesSection(directives=directives)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Advance Directives Section (entries required)](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.21.1.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.21.1.html`

## Best Practices

### 1. Verify Current Status
```python
# Always verify directives are current
{
    "verifier_name": "Dr. Jane Smith",
    "verification_date": date(2024, 3, 15),  # Recent verification
}
```

### 2. Include Contact Information
```python
# Provide complete healthcare proxy information
{
    "custodian_name": "John Doe",
    "custodian_relationship": "Son",
    "custodian_phone": "555-123-4567",
    "custodian_address": "123 Main St, City, ST 12345",
}
```

### 3. Document Links
```python
# Link to actual directive documents
{
    "document_id": "AD-2024-001",
    "document_url": "https://emr.hospital.org/documents/advance-directive-12345.pdf",
    "document_description": "Advance Directive signed 2024-01-15",
}
```

### 4. Common Directive Types
```python
directive_types = [
    "Resuscitation Status",
    "Do Not Resuscitate",
    "Do Not Intubate",
    "Living Will",
    "Healthcare Power of Attorney",
    "Healthcare Proxy",
    "POLST/MOLST",
    "Organ Donation",
    "Guardianship",
]
```

### 5. Resuscitation Status Values
```python
resuscitation_values = {
    "Full Code": "Attempt resuscitation",
    "DNR": "Do not attempt resuscitation",
    "DNI": "Do not intubate",
    "DNR/DNI": "Do not resuscitate or intubate",
    "Comfort Measures Only": "Provide comfort care only",
    "Limited Intervention": "CPR but no intubation",
}
```

### 6. Effective Dates
```python
# Document when directive takes effect and expires
{
    "start_date": date(2024, 1, 1),   # When it becomes effective
    "end_date": None,                  # None if no expiration
}

# Or with expiration
{
    "start_date": date(2024, 1, 1),
    "end_date": date(2026, 1, 1),     # Requires renewal
}
```

### 7. Relationship Codes
```python
# Use standard relationship codes
relationship_codes = {
    "DAUC": "Daughter",
    "SONC": "Son",
    "SPS": "Spouse",
    "BRO": "Brother",
    "SIS": "Sister",
    "CHILD": "Child",
    "PRN": "Parent",
}
```

### 8. Narrative Generation
The section automatically generates an HTML table with:
- Type (directive type with unique ID reference)
- Directive details (with link if URL available)
- Start date and end date
- Custodian information
- Verification details

### 9. Code Systems
```python
# Use SNOMED CT for advance directive codes
{
    "directive_type_code": "304251008",      # Resuscitation status
    "directive_type_code_system": "SNOMED",
    "directive_value_code": "304253006",     # DNR
    "directive_value_code_system": "SNOMED",
}
```

### 10. Regular Updates
```python
# Update verification regularly
{
    "verification_date": date(2024, 3, 15),  # Recent verification
    "verifier_name": "Dr. Sarah Johnson",
}

# Document changes
{
    "start_date": date(2024, 3, 15),  # New directive date
    "end_date": date(2024, 3, 14),    # Previous directive ended
}
```

## Common SNOMED CT Codes

### Directive Type Codes
- `304251008` - Resuscitation status
- `52765003` - Living will
- `71388002` - Power of attorney
- `304252001` - Consent for organ donation
- `225204009` - Healthcare proxy

### Directive Value Codes
- `304253006` - Do not resuscitate
- `304252001` - Intubation
- `89666000` - CPR (cardiopulmonary resuscitation)
- `225287000` - Artificial nutrition
- `76691003` - Mechanical ventilation

## Common Pitfalls

1. **Outdated Information:** Regularly verify directive status and currency
2. **Missing Contact Info:** Always include healthcare proxy contact details
3. **No Verification:** Document who verified the directive and when
4. **Vague Language:** Use specific, clear terminology
5. **Missing Documents:** Link to actual advance directive documents when available
6. **Incomplete Proxies:** Include all designated decision-makers
7. **No Expiration Handling:** Document if/when directives expire
8. **Conflicting Directives:** Ensure consistency across multiple directives
9. **No Code Status:** Always document resuscitation preferences
10. **Missing Updates:** Update when patient's wishes change

## Legal Considerations

### Documentation Requirements
- Verify directives are properly executed according to state law
- Confirm witnesses/notarization as required
- Document patient competency at time of execution
- Note any changes or revocations

### Healthcare Proxy Authority
- Specify scope of decision-making authority
- Document when proxy authority becomes active
- Note any limitations on proxy decisions
- Include alternate proxies if designated

### Validity Across Settings
- Ensure directives transfer across care settings
- Verify POLST forms are signed by physician
- Confirm organ donation registry enrollment
- Document guardianship orders if applicable
