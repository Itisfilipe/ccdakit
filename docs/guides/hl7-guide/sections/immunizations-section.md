# Immunizations Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.2.1
**Version:** R2.1 (2015-08-01)
**Badge:** Core Section

## Overview

The Immunizations Section documents vaccines administered to a patient, including childhood immunizations, adult boosters, seasonal vaccines (like influenza), and travel-related immunizations. This section is essential for preventive care tracking and public health reporting.

### Clinical Purpose and Context

The Immunizations Section records:
- All vaccines administered to the patient
- Dates of immunization administration
- Vaccine product details (CVX codes)
- Administration status (completed, refused, etc.)
- Lot numbers and manufacturer information
- Route and site of administration

This information is essential for:
- Maintaining accurate immunization records
- Determining due dates for upcoming vaccines
- Public health surveillance and outbreak management
- School and employment immunization requirements
- Travel medicine planning
- Meeting Meaningful Use requirements

### When to Include

The Immunizations Section is a **required section** in most C-CDA document types, including:
- Continuity of Care Documents (CCD)
- Consultation Notes
- History and Physical Notes
- Transfer Summaries
- Discharge Summaries

Even if a patient has no recorded immunizations, the section should be included with narrative text stating "No known immunizations."

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.2.1
- **Extension:** 2015-08-01 (R2.1) / 2014-06-09 (R2.0)

### Conformance Level
- **Conformance:** SHALL (Required in entries-required variant)
- **Section Code:** 11369-6 (LOINC - "History of Immunization Narrative")

### Cardinality
- **Section:** 1..1 (Required in most C-CDA document types)
- **Entries:** 1..* (At least one Immunization Activity entry is required for entries-required variant)

### Related Templates
- **Immunization Activity (V3):** 2.16.840.1.113883.10.20.22.4.52:2015-08-01
- **Immunization Refusal Reason:** 2.16.840.1.113883.10.20.22.4.53

## Protocol Requirements

The `ImmunizationProtocol` defines the data contract for immunization entries. Each immunization must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `vaccine_name` | `str` | Name of the vaccine |
| `cvx_code` | `str` | CVX code for the vaccine (CDC vaccine code system) |
| `administration_date` | `date` or `datetime` | Date the vaccine was administered |
| `status` | `str` | Status: 'completed', 'refused', 'not_administered' |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `lot_number` | `Optional[str]` | Vaccine lot number |
| `manufacturer` | `Optional[str]` | Vaccine manufacturer name |
| `route` | `Optional[str]` | Route of administration (e.g., "Intramuscular") |
| `site` | `Optional[str]` | Body site where administered (e.g., "Left deltoid") |
| `dose_quantity` | `Optional[str]` | Dose quantity and unit (e.g., "0.5 mL") |

### Data Types and Constraints
- **vaccine_name:** Free-text vaccine name (e.g., "Influenza vaccine")
- **cvx_code:** Must be a valid CVX code from CDC's vaccine code system
- **administration_date:** Can be date or datetime object
- **status:** Typically 'completed' for administered vaccines, 'refused' for patient refusals
- **lot_number:** Manufacturer's lot number for vaccine traceability
- **manufacturer:** Organization name or MVX code
- **route:** FDA Route of Administration code (e.g., "Intramuscular", "Oral", "Intranasal")
- **site:** Body site code from SNOMED CT or display name

## Code Example

Here's a complete working example using ccdakit to create an Immunizations Section:

```python
from datetime import date, datetime
from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.core.base import CDAVersion

# Define an immunization using a simple class that implements ImmunizationProtocol
class Immunization:
    def __init__(self, vaccine_name, cvx_code, administration_date, status,
                 lot_number=None, manufacturer=None, route=None, site=None, dose_quantity=None):
        self.vaccine_name = vaccine_name
        self.cvx_code = cvx_code
        self.administration_date = administration_date
        self.status = status
        self.lot_number = lot_number
        self.manufacturer = manufacturer
        self.route = route
        self.site = site
        self.dose_quantity = dose_quantity

# Create immunization instances
immunizations = [
    Immunization(
        vaccine_name="Influenza vaccine",
        cvx_code="141",
        administration_date=date(2023, 10, 15),
        status="completed",
        lot_number="U3421AA",
        manufacturer="Sanofi Pasteur",
        route="Intramuscular",
        site="Left deltoid",
        dose_quantity="0.5 mL"
    ),
    Immunization(
        vaccine_name="Tetanus, diphtheria toxoids and acellular pertussis vaccine (Tdap)",
        cvx_code="115",
        administration_date=date(2020, 5, 10),
        status="completed",
        lot_number="P8765ZZ",
        manufacturer="GlaxoSmithKline",
        route="Intramuscular",
        site="Right deltoid",
        dose_quantity="0.5 mL"
    ),
    Immunization(
        vaccine_name="Pneumococcal conjugate vaccine",
        cvx_code="133",
        administration_date=date(2022, 3, 20),
        status="completed",
        manufacturer="Pfizer",
        route="Intramuscular",
        site="Left deltoid"
    ),
    Immunization(
        vaccine_name="Zoster vaccine (shingles)",
        cvx_code="121",
        administration_date=date(2021, 8, 5),
        status="completed",
        lot_number="X2109BC",
        manufacturer="Merck",
        route="Subcutaneous"
    )
]

# Build the Immunizations Section
section_builder = ImmunizationsSection(
    immunizations=immunizations,
    title="Immunizations",
    version=CDAVersion.R2_1
)

# Generate XML element
section_element = section_builder.build()

# Convert to XML string (for demonstration)
from lxml import etree
xml_string = etree.tostring(section_element, pretty_print=True, encoding='unicode')
print(xml_string)
```

## Official Reference

For complete specification details, refer to the official HL7 C-CDA R2.1 documentation:
- [HL7 C-CDA R2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- Section: 5.27 - Immunizations Section (entries required)

Additional resources:
- [CDC CVX Codes](https://www2a.cdc.gov/vaccines/iis/iisstandards/vaccines.asp?rpt=cvx)
- [CDC Vaccine Manufacturer Codes (MVX)](https://www2a.cdc.gov/vaccines/iis/iisstandards/vaccines.asp?rpt=mvx)

## Best Practices

### Common Patterns

1. **Use CVX Codes Consistently**
   - CVX codes are the standard for vaccine identification
   - Always use the most specific CVX code available
   - Check CDC's CVX code list for updates regularly
   - Example: CVX 141 = Influenza, seasonal, injectable

2. **Document Lot Numbers for Traceability**
   - Lot numbers are critical for vaccine recalls
   - Should be recorded at time of administration
   - Required by many immunization registries
   - Improves patient safety and quality reporting

3. **Include Manufacturer Information**
   - Manufacturer names or MVX codes help with specificity
   - Important for distinguishing between similar products
   - Required for some vaccine types with multiple brands

4. **Record Administration Details**
   - Route and site provide complete administration record
   - Important for proper technique documentation
   - Can affect efficacy and adverse event assessment

5. **Track Historical Immunizations**
   - Include childhood immunizations when available
   - Document vaccines from previous providers
   - Note patient-reported immunizations with appropriate qualifiers

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 11369-6 (LOINC)
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes correct extension
   - R2.1: extension="2015-08-01"
   - R2.0: extension="2014-06-09"

3. **CVX Code Validation**
   - Verify CVX codes are current and valid
   - Check CDC's CVX code list
   - Some CVX codes are deprecated and should not be used

4. **Status Code Validation**
   - 'completed' (moodCode="EVN", statusCode="completed")
   - 'not_administered' requires negationInd="true"
   - 'refused' should include refusal reason

5. **Date Format Validation**
   - Administration dates should be in the past (not future)
   - Use YYYYMMDD format for dates
   - Can include time for precise documentation (YYYYMMDDHHMMSS)

### Gotchas to Avoid

1. **Using Outdated CVX Codes**
   - CDC periodically deprecates CVX codes
   - Check CVX code status before implementation
   - Update systems when codes are changed or retired

2. **Missing Lot Numbers**
   - While optional in the schema, lot numbers are clinically important
   - Many immunization registries require lot numbers
   - Record at time of administration, as retrospective capture is difficult

3. **Incorrect Route Codes**
   - Route must match the vaccine's approved administration method
   - Use FDA Route of Administration terminology
   - Examples: IM (Intramuscular), SC (Subcutaneous), PO (Oral), IN (Intranasal)

4. **Confusing Status Codes**
   - Don't use 'active' for immunizations (use 'completed')
   - 'completed' means the vaccine was administered
   - Use negationInd for vaccines that were not given

5. **Duplicate Entries**
   - Avoid documenting the same vaccine administration multiple times
   - Check for duplicates when consolidating from multiple sources
   - Use unique IDs to track across documents

6. **Historical Data Quality**
   - Patient-reported immunizations may lack detail
   - Document source of information (patient reported vs. verified)
   - May lack lot numbers, manufacturer, or specific dates

7. **Date Precision**
   - Some historical records may only have year or month
   - Use date precision indicators appropriately
   - Don't fabricate precise dates from vague records

8. **Manufacturer Codes vs. Names**
   - MVX codes are preferred but names are acceptable
   - Ensure manufacturer name matches the lot number
   - Cross-reference with CDC's MVX code list

9. **Combination Vaccines**
   - Use appropriate CVX code for combination products
   - Example: CVX 130 for DTaP-IPV (4-component)
   - Don't list individual components separately

10. **Refused Immunizations**
    - Document refusals with status="refused" or negationInd="true"
    - Include refusal reason when available
    - Important for outbreak investigations and coverage calculations

11. **Future Immunizations**
    - Don't document scheduled but not-yet-administered vaccines
    - Use Care Plan or Procedure Plan for future vaccines
    - Immunization section is for historical/completed vaccines

12. **Narrative-Entry Consistency**
    - Ensure narrative table matches structured entries
    - The builder handles this automatically
    - Include key details (lot number, date) in narrative
