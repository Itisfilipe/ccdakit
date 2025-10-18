# Payers Section

**OID:** 2.16.840.1.113883.10.20.22.2.18
**Version:** 2015-08-01
**Badge:** Administrative Section

## Overview

The Payers Section contains data on the patient's payers, whether third-party insurance, self-pay, other payer, or guarantor. Each unique instance of a payer and all pertinent data needed to contact, bill to, and collect from that payer should be included.

This section is essential for billing, eligibility verification, and coordination of benefits. It typically includes insurance company information, policy numbers, coverage periods, and priority of coverage.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.18
- **Extension:** 2015-08-01
- **Conformance:** SHOULD
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 48768-6 "Payers"

## Protocol Requirements

### PayerProtocol
```python
from typing import Protocol, Optional
from datetime import date

class PayerProtocol(Protocol):
    payer_name: str                  # Insurance company name
    insurance_type: str              # Type of insurance (e.g., "Commercial", "Medicare", "Medicaid")
    member_id: str                   # Member/subscriber ID
    group_number: Optional[str]      # Group number (if applicable)
    start_date: Optional[date]       # Coverage start date
    end_date: Optional[date]         # Coverage end date (None if active)
    sequence_number: Optional[int]   # Priority: 1=Primary, 2=Secondary, 3=Tertiary
```

## Code Example

### Single Insurance
```python
from ccdakit import PayersSection, CDAVersion
from datetime import date

# Define payer information
payers = [
    {
        "payer_name": "Blue Cross Blue Shield",
        "insurance_type": "Commercial PPO",
        "member_id": "ABC123456789",
        "group_number": "GRP-00123",
        "start_date": date(2024, 1, 1),
        "end_date": None,  # Active coverage
        "sequence_number": 1  # Primary insurance
    }
]

section = PayersSection(
    payers=payers,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Multiple Insurance Coverage
```python
from ccdakit import PayersSection, CDAVersion
from datetime import date

# Primary and secondary insurance
payers = [
    {
        "payer_name": "Medicare Part A and B",
        "insurance_type": "Medicare",
        "member_id": "1EG4-TE5-MK72",
        "group_number": None,
        "start_date": date(2020, 7, 1),
        "end_date": None,
        "sequence_number": 1  # Primary
    },
    {
        "payer_name": "AARP Medicare Supplement",
        "insurance_type": "Medicare Supplement",
        "member_id": "SUP-987654321",
        "group_number": None,
        "start_date": date(2020, 7, 1),
        "end_date": None,
        "sequence_number": 2  # Secondary
    }
]

section = PayersSection(
    payers=payers,
    title="Insurance Coverage",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Medicaid Coverage
```python
from ccdakit import PayersSection, CDAVersion
from datetime import date

payers = [
    {
        "payer_name": "State Medicaid Program",
        "insurance_type": "Medicaid",
        "member_id": "MC-12345678",
        "group_number": None,
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31),
        "sequence_number": 1
    }
]

section = PayersSection(
    payers=payers,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Commercial Insurance with Historical Coverage
```python
from ccdakit import PayersSection, CDAVersion
from datetime import date

# Show current and recent past insurance
payers = [
    {
        "payer_name": "United Healthcare",
        "insurance_type": "Commercial HMO",
        "member_id": "UHC-777888999",
        "group_number": "EMPLOYER-2024",
        "start_date": date(2024, 1, 1),
        "end_date": None,
        "sequence_number": 1
    },
    {
        "payer_name": "Aetna",
        "insurance_type": "Commercial PPO",
        "member_id": "ATN-123456789",
        "group_number": "EMPLOYER-2023",
        "start_date": date(2023, 1, 1),
        "end_date": date(2023, 12, 31),
        "sequence_number": 1
    }
]

section = PayersSection(
    payers=payers,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Complex Coverage Scenario
```python
from ccdakit import PayersSection, CDAVersion
from datetime import date

# Patient with primary commercial, secondary Medicare, and tertiary supplement
payers = [
    {
        "payer_name": "Employee Health Plan",
        "insurance_type": "Commercial",
        "member_id": "EMP-123456",
        "group_number": "COMPANY-001",
        "start_date": date(2020, 1, 1),
        "end_date": None,
        "sequence_number": 1  # Primary
    },
    {
        "payer_name": "Medicare Part B",
        "insurance_type": "Medicare",
        "member_id": "1AB2-CD3-EF45",
        "group_number": None,
        "start_date": date(2022, 6, 1),
        "end_date": None,
        "sequence_number": 2  # Secondary
    },
    {
        "payer_name": "Medigap Plan G",
        "insurance_type": "Medicare Supplement",
        "member_id": "MG-789012",
        "group_number": None,
        "start_date": date(2022, 6, 1),
        "end_date": None,
        "sequence_number": 3  # Tertiary
    }
]

section = PayersSection(
    payers=payers,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Payers Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.18.html)

## Best Practices

1. **Verify Current Coverage**: Always verify that insurance information is current and accurate before documenting.

2. **Order by Priority**: List insurance in order of priority (primary, secondary, tertiary) using the sequence_number field.

3. **Complete Information**: Include all available information (member ID, group number, coverage dates) for accurate billing.

4. **Update Regularly**: Keep insurance information current, especially during annual open enrollment periods.

5. **Historical Coverage**: Consider including recent expired coverage for continuity of care and billing reconciliation.

6. **Coordination of Benefits**: Properly document multiple insurance to ensure correct coordination of benefits.

7. **Self-Pay Patients**: For self-pay patients, document appropriately with insurance_type="Self-pay".

8. **Contact Information**: When available, include payer contact information for verification and claims.

9. **Eligibility Verification**: Document when eligibility was last verified and by whom.

10. **Special Programs**: Document participation in special programs (e.g., patient assistance programs, charity care).

## Common Insurance Types

- **Commercial**: Private insurance (HMO, PPO, EPO, POS)
- **Medicare**: Federal health insurance for 65+ or disabled
- **Medicare Part A**: Hospital insurance
- **Medicare Part B**: Medical insurance
- **Medicare Part C**: Medicare Advantage plans
- **Medicare Part D**: Prescription drug coverage
- **Medicare Supplement**: Medigap policies
- **Medicaid**: State/federal insurance for low-income
- **CHIP**: Children's Health Insurance Program
- **TRICARE**: Military health system
- **Veterans Affairs**: VA healthcare
- **Workers Compensation**: Work-related injury coverage
- **Self-pay**: No insurance coverage

## Sequence Number Priority

- **1**: Primary insurance - billed first
- **2**: Secondary insurance - billed after primary
- **3**: Tertiary insurance - billed after secondary
- **Higher numbers**: Additional coverage levels (rare)

## Coverage Period Considerations

- Active coverage: `end_date` is None or in the future
- Expired coverage: `end_date` is in the past
- Future coverage: `start_date` is in the future
- Always document coverage periods to avoid billing errors
