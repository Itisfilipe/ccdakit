# Results Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.3.1
**Version:** R2.1 (2015-08-01)
**Badge:** Core Section

## Overview

The Results Section contains laboratory test results, diagnostic test results, and other clinical observations grouped into panels or organizers. This section is fundamental for documenting diagnostic findings and monitoring patient health status over time.

### Clinical Purpose and Context

The Results Section records:
- Laboratory test results (chemistry, hematology, microbiology)
- Diagnostic test results (imaging reports as observations, pathology)
- Panel/battery results grouped logically
- Reference ranges and interpretations
- Result status (preliminary, final, corrected)

This information is essential for:
- Clinical diagnosis and monitoring
- Treatment decision-making
- Disease progression tracking
- Quality measurement and reporting
- Care coordination across providers
- Meeting Meaningful Use requirements

### When to Include

The Results Section is commonly included in:
- Continuity of Care Documents (CCD)
- Discharge Summaries
- Consultation Notes
- Progress Notes
- Transfer Summaries

The section is optional in many document types but highly recommended when laboratory or diagnostic test results are relevant to patient care.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.3.1
- **Extension:** 2015-08-01 (V3)

### Conformance Level
- **Conformance:** MAY or SHOULD (depending on document type)
- **Section Code:** 30954-2 (LOINC - "Relevant diagnostic tests and/or laboratory data")

### Cardinality
- **Section:** 0..1 (Optional in most document types)
- **Entries:** 1..* (If section is present, at least one Result Organizer entry is required)

### Related Templates
- **Result Organizer (V3):** 2.16.840.1.113883.10.20.22.4.1:2015-08-01
- **Result Observation (V3):** 2.16.840.1.113883.10.20.22.4.2:2015-08-01

## Protocol Requirements

The results data model uses two protocols: `ResultObservationProtocol` for individual test results and `ResultOrganizerProtocol` for grouping related results into panels.

### ResultObservationProtocol (Individual Test)

#### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `test_name` | `str` | Name of the test (e.g., "Glucose", "Hemoglobin") |
| `test_code` | `str` | LOINC code for the test |
| `value` | `str` | Measured value (numeric or text) |
| `status` | `str` | Status: 'completed', 'preliminary', 'final', 'corrected' |
| `effective_time` | `date` or `datetime` | Date and time the test was performed |

#### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `unit` | `Optional[str]` | Unit of measurement (UCUM) |
| `value_type` | `Optional[str]` | Type: "PQ" (quantity), "CD" (coded), "ST" (string) |
| `interpretation` | `Optional[str]` | Interpretation: "N", "H", "L", "HH", "LL" |
| `reference_range_low` | `Optional[str]` | Lower bound of reference range |
| `reference_range_high` | `Optional[str]` | Upper bound of reference range |
| `reference_range_unit` | `Optional[str]` | Unit for reference range |

### ResultOrganizerProtocol (Panel/Battery)

#### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `panel_name` | `str` | Name of the panel (e.g., "Complete Blood Count") |
| `panel_code` | `str` | LOINC code for the panel |
| `status` | `str` | Status: 'completed', 'active', 'aborted' |
| `effective_time` | `date` or `datetime` | Date when panel was collected/performed |
| `results` | `Sequence[ResultObservationProtocol]` | List of result observations |

### Data Types and Constraints
- **test_name/panel_name:** Human-readable test or panel name
- **test_code/panel_code:** LOINC codes (preferred vocabulary for lab tests)
- **value:** String representation of measurement (numeric values as strings)
- **unit:** UCUM standard units (e.g., "mg/dL", "g/dL", "10*3/uL")
- **value_type:** Determines XML representation (PQ for quantities, ST for text)
- **interpretation:** Standard observation interpretation codes
- **status:** Reflects completion state and reliability
- **effective_time:** When specimen was collected or test performed

## Code Example

Here's a complete working example using ccdakit to create a Results Section:

```python
from datetime import datetime
from ccdakit.builders.sections.results import ResultsSection
from ccdakit.core.base import CDAVersion

# Define a result observation
class ResultObservation:
    def __init__(self, test_name, test_code, value, status, effective_time,
                 unit=None, value_type=None, interpretation=None,
                 reference_range_low=None, reference_range_high=None,
                 reference_range_unit=None):
        self.test_name = test_name
        self.test_code = test_code
        self.value = value
        self.unit = unit
        self.status = status
        self.effective_time = effective_time
        self.value_type = value_type
        self.interpretation = interpretation
        self.reference_range_low = reference_range_low
        self.reference_range_high = reference_range_high
        self.reference_range_unit = reference_range_unit

# Define a result organizer
class ResultOrganizer:
    def __init__(self, panel_name, panel_code, status, effective_time, results):
        self.panel_name = panel_name
        self.panel_code = panel_code
        self.status = status
        self.effective_time = effective_time
        self.results = results

# Create result observations for a Complete Blood Count panel
collection_time = datetime(2023, 10, 18, 8, 30)

cbc_results = [
    ResultObservation(
        test_name="Hemoglobin",
        test_code="718-7",
        value="14.5",
        unit="g/dL",
        status="final",
        effective_time=collection_time,
        interpretation="N",
        reference_range_low="12.0",
        reference_range_high="16.0",
        reference_range_unit="g/dL"
    ),
    ResultObservation(
        test_name="Hematocrit",
        test_code="4544-3",
        value="42.0",
        unit="%",
        status="final",
        effective_time=collection_time,
        interpretation="N",
        reference_range_low="36.0",
        reference_range_high="46.0",
        reference_range_unit="%"
    ),
    ResultObservation(
        test_name="White Blood Cell Count",
        test_code="6690-2",
        value="7.2",
        unit="10*3/uL",
        status="final",
        effective_time=collection_time,
        interpretation="N",
        reference_range_low="4.5",
        reference_range_high="11.0",
        reference_range_unit="10*3/uL"
    ),
    ResultObservation(
        test_name="Platelet Count",
        test_code="777-3",
        value="250",
        unit="10*3/uL",
        status="final",
        effective_time=collection_time,
        interpretation="N",
        reference_range_low="150",
        reference_range_high="400",
        reference_range_unit="10*3/uL"
    )
]

# Create result observations for a Basic Metabolic Panel
bmp_results = [
    ResultObservation(
        test_name="Glucose",
        test_code="2345-7",
        value="105",
        unit="mg/dL",
        status="final",
        effective_time=collection_time,
        interpretation="H",
        reference_range_low="70",
        reference_range_high="100",
        reference_range_unit="mg/dL"
    ),
    ResultObservation(
        test_name="Creatinine",
        test_code="2160-0",
        value="0.9",
        unit="mg/dL",
        status="final",
        effective_time=collection_time,
        interpretation="N",
        reference_range_low="0.6",
        reference_range_high="1.2",
        reference_range_unit="mg/dL"
    ),
    ResultObservation(
        test_name="Sodium",
        test_code="2951-2",
        value="140",
        unit="mmol/L",
        status="final",
        effective_time=collection_time,
        interpretation="N",
        reference_range_low="135",
        reference_range_high="145",
        reference_range_unit="mmol/L"
    ),
    ResultObservation(
        test_name="Potassium",
        test_code="2823-3",
        value="4.2",
        unit="mmol/L",
        status="final",
        effective_time=collection_time,
        interpretation="N",
        reference_range_low="3.5",
        reference_range_high="5.0",
        reference_range_unit="mmol/L"
    )
]

# Create result organizers
organizers = [
    ResultOrganizer(
        panel_name="Complete Blood Count",
        panel_code="58410-2",
        status="completed",
        effective_time=collection_time,
        results=cbc_results
    ),
    ResultOrganizer(
        panel_name="Basic Metabolic Panel",
        panel_code="51990-0",
        status="completed",
        effective_time=collection_time,
        results=bmp_results
    )
]

# Build the Results Section
section_builder = ResultsSection(
    result_organizers=organizers,
    title="Results",
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
- Section: 5.48 - Results Section (entries required)

Additional resources:
- [LOINC Database](https://loinc.org/)
- [UCUM Unit Codes](https://ucum.org/)

## Best Practices

### Common Patterns

1. **Use LOINC Codes Consistently**
   - LOINC is the required vocabulary for laboratory tests
   - Use specific codes (e.g., 2345-7 for serum glucose)
   - Panel codes group related tests (e.g., 58410-2 for CBC)
   - Verify codes in LOINC database

2. **Group Related Tests in Organizers**
   - Use organizers to represent laboratory panels
   - Common panels: CBC, CMP, BMP, Lipid Panel, Liver Function
   - Maintains clinical context and ordering relationships
   - Supports laboratory workflow representation

3. **Include Reference Ranges**
   - Reference ranges provide context for interpretation
   - Essential for automated decision support
   - May vary by age, sex, and laboratory
   - Include both low and high bounds when applicable

4. **Document Result Interpretations**
   - Use standard codes: N (Normal), H (High), L (Low), HH (Critically High), LL (Critically Low)
   - Supports clinical alerting and decision support
   - Helps identify abnormal values quickly
   - Important for quality measurement

5. **Track Result Status**
   - 'preliminary' for unverified results
   - 'final' for verified results
   - 'corrected' for amended results
   - Supports laboratory workflow and clinical confidence

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 30954-2 (LOINC)
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes extension="2015-08-01"
   - V3 is the current version for R2.1

3. **LOINC Code Validation**
   - Verify test codes are valid LOINC codes
   - Verify panel codes represent batteries/panels
   - Use LOINC search tool for validation
   - Check for deprecated codes

4. **Unit Validation**
   - Use UCUM standard units
   - Case-sensitive: "mg/dL" not "MG/DL"
   - Special syntax: "10*3/uL" for thousands per microliter
   - Validate with UCUM validator

5. **Value Type Consistency**
   - PQ (Physical Quantity): numeric values with units
   - ST (String): text values without units
   - CD (Coded): coded values from value sets
   - Choose appropriate type for result

### Gotchas to Avoid

1. **Missing Organizer Structure**
   - Results must be wrapped in organizers
   - Don't add observations directly to section
   - Even single results need an organizer
   - Organizer represents the order/panel

2. **Incorrect UCUM Units**
   - Must use exact UCUM syntax
   - Case-sensitive
   - Special characters: "10*3/uL" not "K/uL"
   - Brackets for special units: "[pH]"

3. **Incomplete Reference Ranges**
   - Include both low and high when possible
   - Use same units as result value
   - Some tests only have upper or lower limit
   - Don't fabricate ranges if unknown

4. **Status Confusion**
   - Organizer status vs. observation status
   - Both should typically be aligned
   - 'completed' organizer contains 'final' observations
   - Track amendments with 'corrected' status

5. **Missing Interpretation**
   - While optional, interpretations are valuable
   - Supports clinical decision-making
   - Required for many quality measures
   - Can be calculated if reference range provided

6. **Date/Time Precision**
   - Use collection time, not report time
   - Time precision important for serial measurements
   - Supports trending and correlation
   - Use datetime for time-critical tests

7. **Panel Code Selection**
   - Use specific panel codes, not generic ones
   - Different panels have different LOINC codes
   - "Basic Metabolic Panel" ≠ "Comprehensive Metabolic Panel"
   - Check laboratory's panel definition

8. **Mixing Panel Components**
   - Keep panel components together in one organizer
   - Don't split CBC components across organizers
   - Maintains clinical and workflow context
   - Reflects how tests were ordered

9. **Text vs. Numeric Values**
   - Use appropriate value_type
   - Numeric values should use PQ (with unit)
   - Text results (e.g., "Positive") should use ST or CD
   - Don't put text in PQ values

10. **Microbiology Results**
    - Microbiology can be complex (organism, sensitivity)
    - Consider using CD for organism identification
    - Susceptibility testing may need multiple observations
    - May require specialized result structures

11. **Imaging Results**
    - Brief imaging findings can be observations
    - Full reports should be in Imaging Results section or as external document
    - Don't put lengthy narrative in result value
    - Consider DICOM references for images

12. **Critical Values**
    - Use HH (Critically High) or LL (Critically Low)
    - Important for clinical alerting
    - May trigger specific workflows
    - Document follow-up actions

13. **Historical Results**
    - Consider including previous results for trending
    - Use separate organizers for different collection times
    - Don't mix results from different dates in same organizer
    - Temporal context is critical

14. **Corrected Results**
    - Use status='corrected' for amendments
    - Consider including original value in comments
    - Document reason for correction if known
    - Important for patient safety

15. **Narrative-Entry Consistency**
    - Ensure narrative table matches structured entries
    - Builder handles this automatically
    - Include key details: value, unit, interpretation, reference range in narrative
    - Critical for human readers

16. **Pending Results**
    - Don't include results that haven't been resulted yet
    - Use status='preliminary' for unverified results
    - Don't use placeholder values
    - Results section is for actual results, not orders
