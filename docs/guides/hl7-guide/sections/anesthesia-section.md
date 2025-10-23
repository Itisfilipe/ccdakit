# Anesthesia Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.25
**Version:** V2 (2014-06-09)
**Badge:** Surgical Section

## Overview

The Anesthesia Section records the type of anesthesia (e.g., general, local, regional) and may state the actual anesthetic agents used during a surgical or procedural intervention. This section may be included as a standalone section or as a subsection of the Procedure Description Section. The full details of anesthesia administration are usually found in a separate Anesthesia Note.

### Clinical Purpose and Context

The Anesthesia Section documents:
- Type of anesthesia used (general, local, regional, sedation)
- Specific anesthetic agents and medications administered
- Route of administration
- Timing of anesthesia (start and end times)
- Anesthesia provider information
- Clinical notes about anesthesia delivery

This section provides critical information for post-operative care, future anesthetic planning, and documentation of the complete surgical procedure.

### When to Include

The Anesthesia Section is typically included in:
- **Operative Notes** (primary use case)
- **Procedure Notes** (for procedures requiring anesthesia)
- **Surgical Summaries**
- **Discharge Summaries** (when documenting surgical procedures)

Note: Detailed anesthesia records are typically maintained in separate Anesthesia Notes; this section provides summary information.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.25
- **Extension:** 2014-06-09 (V2)

### Conformance Level
- **Conformance:** MAY (Optional)
- **Section Code:** 59774-0 (LOINC - "Anesthesia")

### Cardinality
- **Section:** 0..1 (Optional)
- **Entries:** 0..* (Procedure Activity and Medication Activity entries)

### Related Templates
- **Procedure Activity Procedure (V2):** 2.16.840.1.113883.10.20.22.4.14:2014-06-09 (for anesthesia type)
- **Medication Activity (V2):** 2.16.840.1.113883.10.20.22.4.16:2014-06-09 (for anesthetic agents)

## Protocol Requirements

The `AnesthesiaProtocol` defines the data contract for anesthesia records. Each anesthesia record must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `anesthesia_type` | `str` | Type of anesthesia (e.g., "General anesthesia") |
| `anesthesia_code` | `str` | SNOMED CT code for anesthesia type |
| `anesthesia_code_system` | `str` | Code system (typically "SNOMED CT") |
| `status` | `str` | Status: 'completed', 'active', 'aborted' |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `start_time` | `Optional[date\|datetime]` | When anesthesia was started |
| `end_time` | `Optional[date\|datetime]` | When anesthesia was stopped |
| `anesthesia_agents` | `Optional[list[MedicationProtocol]]` | Anesthetic medications used |
| `route` | `Optional[str]` | Primary route of administration |
| `performer_name` | `Optional[str]` | Name of anesthesiologist/anesthetist |
| `notes` | `Optional[str]` | Additional clinical notes |

### Data Types and Constraints
- **anesthesia_type:** Human-readable description (e.g., "General anesthesia")
- **anesthesia_code:** SNOMED CT code (e.g., "50697003" for general anesthesia)
- **start_time/end_time:** Can be date or datetime objects
- **anesthesia_agents:** List of medications, each implementing MedicationProtocol
- **route:** Common values: 'Inhalation', 'Intravenous', 'Intramuscular', 'Topical'

## Code Example

Here's a complete working example using ccdakit to create an Anesthesia Section:

```python
from datetime import datetime
from ccdakit.builders.sections.anesthesia import AnesthesiaSection
from ccdakit.core.base import CDAVersion

# Define an anesthetic medication class
class AnestheticAgent:
    def __init__(self, name, code, dose, route):
        self._name = name
        self._code = code
        self._dose = dose
        self._route = route

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dose(self):
        return self._dose

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return None

# Define anesthesia records using AnesthesiaProtocol
class AnesthesiaRecord:
    def __init__(self, anesthesia_type, code, agents=None, start_time=None,
                 end_time=None, route=None, performer=None):
        self._anesthesia_type = anesthesia_type
        self._anesthesia_code = code
        self._anesthesia_code_system = "SNOMED CT"
        self._status = "completed"
        self._start_time = start_time
        self._end_time = end_time
        self._anesthesia_agents = agents or []
        self._route = route
        self._performer_name = performer
        self._notes = None

    @property
    def anesthesia_type(self):
        return self._anesthesia_type

    @property
    def anesthesia_code(self):
        return self._anesthesia_code

    @property
    def anesthesia_code_system(self):
        return self._anesthesia_code_system

    @property
    def status(self):
        return self._status

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def anesthesia_agents(self):
        return self._anesthesia_agents

    @property
    def route(self):
        return self._route

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def notes(self):
        return self._notes

# Create anesthetic agents
agents = [
    AnestheticAgent(
        name="Propofol 10mg/mL injection",
        code="73133000",  # SNOMED CT for Propofol
        dose="200 mg",
        route="Intravenous"
    ),
    AnestheticAgent(
        name="Fentanyl 0.05mg/mL injection",
        code="373492002",  # SNOMED CT for Fentanyl
        dose="100 mcg",
        route="Intravenous"
    ),
    AnestheticAgent(
        name="Sevoflurane inhalation",
        code="386838001",  # SNOMED CT for Sevoflurane
        dose="2% concentration",
        route="Inhalation"
    )
]

# Create anesthesia record
anesthesia_records = [
    AnesthesiaRecord(
        anesthesia_type="General anesthesia",
        code="50697003",  # SNOMED CT for general anesthesia
        agents=agents,
        start_time=datetime(2024, 10, 15, 8, 30),
        end_time=datetime(2024, 10, 15, 11, 45),
        route="Intravenous",
        performer="Dr. Jane Smith, MD (Anesthesiologist)"
    )
]

# Build the Anesthesia Section
section_builder = AnesthesiaSection(
    anesthesia_records=anesthesia_records,
    title="Anesthesia",
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
- Section: Anesthesia Section (V2)

## Best Practices

### Common Patterns

1. **Document Complete Anesthesia Information**
   - Include both anesthesia type (procedure) and agents (medications)
   - Record timing (start and end times)
   - Document the anesthesia provider
   - Note the primary route of administration

2. **Use Standard Anesthesia Codes**
   - **General anesthesia:** 50697003 (SNOMED CT)
   - **Local anesthesia:** 386761002 (SNOMED CT)
   - **Regional anesthesia:** 231249005 (SNOMED CT)
   - **Spinal anesthesia:** 50697003 (SNOMED CT)
   - **Epidural anesthesia:** 18946005 (SNOMED CT)
   - **Conscious sedation:** 72641008 (SNOMED CT)

3. **Link Agents to Anesthesia Type**
   - Each anesthesia record can include multiple agents
   - Agents are represented as Medication Activity entries
   - Group related agents with their anesthesia type

4. **Document Timing Accurately**
   - Start time: When anesthesia was initiated
   - End time: When patient emerged from anesthesia
   - Use datetime objects for precise timing
   - Important for calculating anesthesia duration

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 59774-0 (LOINC "Anesthesia")
   - This is automatically set by the builder

2. **Entry Structure Validation**
   - Procedure Activity entries for anesthesia type
   - Medication Activity entries for anesthetic agents
   - Each entry has typeCode="DRIV"

3. **Code System Validation**
   - Anesthesia type codes from SNOMED CT
   - Medication codes from SNOMED CT or RxNorm
   - Route codes from NCIT or SNOMED CT

4. **Status Validation**
   - Use 'completed' for finished procedures
   - Use 'active' for ongoing anesthesia (rare in final documentation)
   - Use 'aborted' if anesthesia was started but discontinued

### Common Pitfalls

1. **Confusing with Medications Administered**
   - Use Anesthesia Section for anesthetic medications
   - Use Medications Administered Section for other medications given during procedure
   - Don't duplicate anesthetic agents in both sections

2. **Missing Timing Information**
   - While optional, timing is important for anesthesia
   - Include start and end times when available
   - Helps calculate anesthesia duration and recovery time

3. **Incomplete Agent Information**
   - List all significant anesthetic agents, not just induction agents
   - Include inhalational agents, IV agents, and adjuncts
   - Document doses when known

4. **Not Distinguishing Anesthesia Types**
   - Clearly identify the type of anesthesia used
   - Don't just list agents without specifying general vs regional
   - Anesthesia type affects post-operative care

5. **Missing Provider Information**
   - Document who provided the anesthesia
   - Important for accountability and follow-up
   - Include credentials (MD, CRNA, etc.) when known

6. **Route Confusion**
   - The route property is for the primary anesthesia route
   - Individual agents may have different routes
   - Common for combined techniques (IV + inhalational)

## Related Sections

- **Medications Administered Section:** Non-anesthetic medications given during procedure
- **Procedures Section:** The surgical procedure requiring anesthesia
- **Complications Section:** Anesthesia-related complications
- **Postoperative Diagnosis:** Diagnoses at end of surgery

## Code Systems and Terminologies

### Anesthesia Type Codes (SNOMED CT)
- **50697003** - General anesthesia
- **386761002** - Local anesthesia
- **231249005** - Regional anesthesia
- **18946005** - Epidural anesthesia
- **231253002** - Spinal anesthesia
- **72641008** - Conscious sedation
- **50697003** - Balanced anesthesia

### Anesthetic Agent Codes (SNOMED CT)
- **73133000** - Propofol
- **373492002** - Fentanyl
- **386838001** - Sevoflurane
- **387173000** - Isoflurane
- **387472004** - Desflurane
- **373200000** - Rocuronium
- **387222003** - Lidocaine

### Route Codes
- **447694001** - Inhalation (SNOMED CT)
- **47625008** - Intravenous (SNOMED CT)
- **78421000** - Intramuscular (SNOMED CT)
- **6064005** - Topical (SNOMED CT)

### Section Codes
- **Primary:** 59774-0 - "Anesthesia" (LOINC)

## Implementation Notes

### Dual Entry Pattern

The section uses a dual entry pattern:
1. **Procedure Activity** entry for anesthesia type/procedure
2. **Medication Activity** entries for each anesthetic agent

This allows complete documentation of both what type of anesthesia was used and what specific drugs were administered.

### Narrative Table Generation

The builder creates a comprehensive table with columns:
- Anesthesia Type
- Code
- Status
- Start Time
- End Time
- Route
- Agents (comma-separated list)
- Performer

### Time Formatting

The builder handles both date and datetime objects:
- **datetime:** Formatted as "YYYY-MM-DD HH:MM"
- **date:** Formatted as "YYYY-MM-DD"
- Checks for the presence of `hour` attribute to determine type

### Agent Handling

Anesthetic agents (medications) are:
- Passed as a list in the `anesthesia_agents` property
- Each agent must implement `MedicationProtocol`
- Automatically converted to Medication Activity entries
- Displayed in the narrative table

### Multiple Anesthesia Records

The section supports multiple anesthesia records:
- Useful for procedures with multiple anesthesia phases
- Each record becomes a separate set of entries
- Rare but possible (e.g., regional followed by general)

### Integration with Procedure Note

The Anesthesia Section is commonly part of:
- Operative Note documents
- Procedure Note documents
- Surgical Summaries

It provides context alongside:
- **Preoperative Diagnosis:** Why surgery was needed
- **Procedure Description:** What was done
- **Postoperative Diagnosis:** What was found
- **Complications:** Any adverse events

### Anesthesia Note vs. Anesthesia Section

**Anesthesia Section (this section):**
- Summary of anesthesia type and agents
- Included in operative/procedure notes
- Brief documentation for continuity of care

**Anesthesia Note (separate document):**
- Detailed anesthesia record
- Pre-anesthetic evaluation
- Intraoperative monitoring
- Complete medication administration record
- Vital signs throughout procedure
- Usually maintained separately

### Provider Documentation

The `performer_name` should include:
- Full name of anesthesia provider
- Credentials (MD, CRNA, CAA)
- Role if multiple providers (attending vs resident)

Example formats:
- "Dr. John Smith, MD, Anesthesiologist"
- "Mary Johnson, CRNA"
- "Anesthesia Care Team: Dr. Smith (Attending) and J. Johnson, CRNA"

### Route Documentation

The `route` property represents the primary route:
- For general anesthesia: Often "Intravenous" (induction) or "Inhalation" (maintenance)
- For regional: "Epidural", "Spinal", "Nerve block"
- For local: "Subcutaneous", "Topical"

Individual agents may have different routes from the primary route.
