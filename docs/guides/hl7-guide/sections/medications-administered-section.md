# Medications Administered Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.38
**Version:** V2 (2014-06-09)
**Badge:** Procedural Section

## Overview

The Medications Administered Section documents medications and fluids administered to a patient during a procedure, encounter, or other clinical activity. This section captures the actual administration events with specific timing, dose, route, and other administration details, excluding anesthetic medications (which should be documented in the Anesthesia Section).

### Clinical Purpose and Context

The Medications Administered Section documents:
- Medications given during procedures or encounters
- IV fluids administered during treatment
- Contrast agents used during imaging
- Medications administered during emergency department visits
- Intraoperative medications (non-anesthetic)
- Procedural medications and sedation

This section provides a record of what medications were actually given to the patient, which is essential for continuity of care, medication reconciliation, and clinical decision-making.

### When to Include

The Medications Administered Section is typically included in:
- **Procedure Notes** (medications during procedures)
- **Operative Notes** (non-anesthetic medications)
- **Emergency Department Notes** (medications given in ED)
- **Visit Summaries** (medications administered during visit)
- **Observation Notes** (medications during observation)

Note: This section differs from the Medications Section, which documents ongoing medication regimens and prescriptions.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.38
- **Extension:** 2014-06-09 (V2)

### Conformance Level
- **Conformance:** MAY (Optional)
- **Section Code:** 29549-3 (LOINC - "Medications Administered")

### Cardinality
- **Section:** 0..1 (Optional)
- **Entries:** 1..* (SHALL contain at least one entry if not nullFlavored)

### Related Templates
- **Medication Activity (V2):** 2.16.840.1.113883.10.20.22.4.16:2014-06-09

## Protocol Requirements

The `MedicationAdministeredProtocol` defines the data contract for medication administration entries. Each administered medication must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Human-readable medication name |
| `code` | `str` | RxNorm code for the medication |
| `administration_time` | `datetime` | When medication was administered |
| `dose` | `str` | Dosage amount with units |
| `route` | `str` | Route of administration |
| `status` | `str` | Administration status |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `administration_end_time` | `Optional[datetime]` | When administration ended (for infusions) |
| `rate` | `Optional[str]` | Rate of administration (e.g., "100 mL/hr") |
| `site` | `Optional[str]` | Anatomical site of administration |
| `performer` | `Optional[str]` | Person who administered medication |
| `indication` | `Optional[str]` | Reason for administration |
| `instructions` | `Optional[str]` | Administration instructions/notes |

### Data Types and Constraints
- **name:** Medication name with strength and form
- **code:** RxNorm code (preferred) or SNOMED CT
- **administration_time:** Datetime object for precise timing
- **dose:** Amount with units (e.g., "500 mg", "100 mL")
- **route:** From FDA Route of Administration value set
- **status:** Typically 'completed' for administered medications

## Code Example

Here's a complete working example using ccdakit to create a Medications Administered Section:

```python
from datetime import datetime
from ccdakit.builders.sections.medications_administered import MedicationsAdministeredSection
from ccdakit.core.base import CDAVersion

# Define administered medications using a class that implements MedicationAdministeredProtocol
class AdministeredMedication:
    def __init__(self, name, code, admin_time, dose, route, status="completed",
                 end_time=None, rate=None, site=None, performer=None,
                 indication=None, instructions=None):
        self._name = name
        self._code = code
        self._administration_time = admin_time
        self._administration_end_time = end_time
        self._dose = dose
        self._route = route
        self._rate = rate
        self._site = site
        self._status = status
        self._performer = performer
        self._indication = indication
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def administration_time(self):
        return self._administration_time

    @property
    def administration_end_time(self):
        return self._administration_end_time

    @property
    def dose(self):
        return self._dose

    @property
    def route(self):
        return self._route

    @property
    def rate(self):
        return self._rate

    @property
    def site(self):
        return self._site

    @property
    def status(self):
        return self._status

    @property
    def performer(self):
        return self._performer

    @property
    def indication(self):
        return self._indication

    @property
    def instructions(self):
        return self._instructions

# Example 1: Medications administered during a procedure
medications = [
    AdministeredMedication(
        name="Ondansetron 4mg/2mL injection",
        code="312086",  # RxNorm
        admin_time=datetime(2024, 10, 15, 9, 30),
        dose="4 mg",
        route="IV",
        site="left arm",
        performer="Jane Smith, RN",
        indication="Nausea prophylaxis"
    ),
    AdministeredMedication(
        name="Cefazolin 1g injection",
        code="1659149",  # RxNorm
        admin_time=datetime(2024, 10, 15, 9, 15),
        dose="1 g",
        route="IV",
        site="left arm",
        performer="Jane Smith, RN",
        indication="Surgical prophylaxis",
        instructions="Given 30 minutes prior to incision"
    ),
    AdministeredMedication(
        name="Normal Saline 0.9% 1000mL",
        code="313002",  # RxNorm
        admin_time=datetime(2024, 10, 15, 9, 0),
        end_time=datetime(2024, 10, 15, 13, 0),
        dose="1000 mL",
        route="IV",
        rate="125 mL/hr",
        site="left arm",
        performer="Jane Smith, RN",
        indication="Fluid maintenance"
    )
]

section_builder = MedicationsAdministeredSection(
    medications=medications,
    title="Medications Administered",
    version=CDAVersion.R2_1
)

# Example 2: Emergency department medications
ed_medications = [
    AdministeredMedication(
        name="Nitroglycerin 0.4mg sublingual tablet",
        code="564666",  # RxNorm
        admin_time=datetime(2024, 10, 15, 14, 22),
        dose="0.4 mg",
        route="Sublingual",
        performer="Dr. Johnson",
        indication="Chest pain"
    ),
    AdministeredMedication(
        name="Aspirin 325mg oral tablet",
        code="243670",  # RxNorm
        admin_time=datetime(2024, 10, 15, 14, 25),
        dose="325 mg",
        route="Oral",
        performer="Dr. Johnson",
        indication="Suspected acute coronary syndrome",
        instructions="Chewed and swallowed"
    )
]

# Example 3: No medications administered (using null flavor)
section_no_meds = MedicationsAdministeredSection(
    medications=[],
    null_flavor="NI",  # No Information
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
- Section: Medications Administered Section (V2)
- Entry: Medication Activity (V2)
- Conformance IDs: CONF:1098-8152 through CONF:1098-15499

## Best Practices

### Common Patterns

1. **Document Complete Administration Details**
   - Include precise administration times
   - Record exact doses and units
   - Specify route and site when relevant
   - Note who administered the medication

2. **Distinguish from Anesthesia**
   - Use Anesthesia Section for anesthetic agents
   - Use this section for other medications during procedures
   - Don't duplicate anesthetic medications

3. **Handle IV Infusions**
   - Use administration_end_time for infusions
   - Include rate for continuous infusions
   - Document total volume administered

4. **Track Emergency Medications**
   - Precise timing is critical in emergencies
   - Include indication for emergency meds
   - Document response to medication when relevant

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 29549-3 (LOINC "Medications Administered")
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes extension="2014-06-09"
   - V2 is the current version

3. **Entry Requirements**
   - SHALL contain at least one entry if nullFlavor not present
   - Each entry is a Medication Activity (V2)
   - Entry typeCode should be "DRIV"

4. **Timing Validation**
   - Use datetime objects for administration_time
   - End time must be after start time for infusions
   - Precise timestamps are important

### Common Pitfalls

1. **Confusing with Medications Section**
   - Medications Section: Ongoing prescriptions and regimens
   - Medications Administered: Actual administration events
   - Different clinical contexts and purposes

2. **Missing Administration Time**
   - Administration time is required
   - Must be datetime, not just date
   - Precision is important for medication reconciliation

3. **Incomplete Dose Information**
   - Always include units with dose
   - Specify exact amount administered
   - For infusions, include total volume and rate

4. **Not Documenting IV Fluids**
   - IV fluids are medications
   - Include maintenance fluids
   - Document boluses and continuous infusions

5. **Missing Route Information**
   - Route is required
   - Use standard route codes
   - Be specific (e.g., "IV" not "parenteral")

6. **Anesthesia Medication Confusion**
   - Don't include anesthetic agents here
   - Use Anesthesia Section for anesthesia drugs
   - This section is for other procedural medications

## Related Sections

- **Anesthesia Section:** Anesthetic medications during procedures
- **Medications Section:** Ongoing medication regimens
- **Procedures Section:** The procedure requiring medication administration
- **Allergies Section:** Medication allergies to check before administration

## Code Systems and Terminologies

### Medication Codes
- **RxNorm (Preferred):** Standard for medication names
  - OID: 2.16.840.1.113883.6.88
  - Use RxNorm Clinical Drug or Branded Drug codes
  - Examples: "312086" (Ondansetron 4mg injection)

### Route Codes
- **FDA Route of Administration:** Value set 2.16.840.1.113883.3.88.12.3221.8.7
- Common routes:
  - **C38276** - Intravenous (IV)
  - **C38288** - Oral
  - **C38276** - Intramuscular (IM)
  - **C38279** - Subcutaneous
  - **C38284** - Topical
  - **C38300** - Sublingual

### Status Codes
- **completed** - Medication was administered (most common)
- **active** - Administration in progress (for infusions)
- **aborted** - Administration was stopped
- **held** - Planned but not given

### Section Codes
- **Primary:** 29549-3 - "Medications Administered" (LOINC)

## Implementation Notes

### Narrative Table Generation

The builder creates a comprehensive table with columns:
- Medication name
- Dose
- Route
- Administration Time (or time range for infusions)
- Site
- Rate (if applicable)
- Performer
- Status

### Time Range Display

For medications with end times (infusions):
- Displays as: "2024-10-15 09:00 - 2024-10-15 13:00"
- Single-dose medications show only administration time

### Null Flavor Support

The section supports null flavor:
```python
section = MedicationsAdministeredSection(
    medications=[],
    null_flavor="NI",  # No Information
    version=CDAVersion.R2_1
)
```

Valid null flavors:
- **NI** - No Information
- **NA** - Not Applicable

### Medication Activity Entries

Each medication becomes:
- A Medication Activity (V2) entry
- Entry typeCode="DRIV"
- Contains consumable, dose, route, timing

### Integration with Procedure Notes

Commonly used in procedure notes:
1. **Preoperative Diagnosis:** Why procedure needed
2. **Anesthesia:** Anesthetic agents
3. **Medications Administered:** Other medications (this section)
4. **Procedure Description:** What was done
5. **Postoperative Diagnosis:** Findings

### Medication Reconciliation

Administered medications inform:
- Post-procedure medication orders
- Discharge medication reconciliation
- Allergy checking and documentation
- Drug-drug interaction screening

### Emergency Medicine Use

Critical in emergency documentation:
- Time-sensitive medication administration
- Code blue medications
- Rapid sequence intubation drugs
- Emergency cardiac medications

### IV Fluid Documentation

For IV fluids:
- Document type (crystalloid, colloid)
- Total volume administered
- Rate of administration
- Indication (maintenance, resuscitation, etc.)

Example:
```python
AdministeredMedication(
    name="Lactated Ringer's 1000mL",
    code="313422",  # RxNorm
    admin_time=datetime(2024, 10, 15, 8, 0),
    end_time=datetime(2024, 10, 15, 16, 0),
    dose="1000 mL",
    route="IV",
    rate="125 mL/hr",
    indication="Maintenance fluid"
)
```

### Contrast Agents

Document contrast for imaging:
```python
AdministeredMedication(
    name="Iohexol 300mg/mL injection",
    code="242970",  # RxNorm
    admin_time=datetime(2024, 10, 15, 10, 15),
    dose="100 mL",
    route="IV",
    indication="CT scan contrast enhancement",
    performer="Radiology Tech"
)
```

### Medication Reconciliation Context

This section helps with:
- Pre-procedure medication review
- Intraoperative medication tracking
- Post-procedure orders
- Discharge medication reconciliation
- Continuity of care documentation

### Performer Documentation

The performer field should include:
- Name of person who administered
- Credentials (RN, MD, PharmD, etc.)
- Role if relevant (e.g., "ED Nurse", "OR Nurse")

### Site Specificity

For injections and IV medications:
- Specify anatomical location
- Use standard anatomical terms
- Important for site rotation tracking
- Relevant for adverse event documentation

### Rate Documentation

For continuous infusions:
- Specify infusion rate with units
- Use standard units (mL/hr, mg/min, etc.)
- Important for dosing calculations
- Critical for vasoactive medications

### Clinical Decision Support

Administered medications data supports:
- Medication allergy alerts
- Drug-drug interaction checking
- Dose range verification
- Route appropriateness validation
- Cumulative dose tracking
- Medication use evaluation
