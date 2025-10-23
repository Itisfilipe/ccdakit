# Instructions Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.45
**Version:** V2 (2014-06-09)
**Badge:** Educational Section

## Overview

The Instructions Section records instructions given to a patient. It can be used to document patient education materials, decision aids, medication instructions, discharge instructions, and other guidance provided to patients or their caregivers. Instructions are prospective in nature, representing what the patient should do or know.

### Clinical Purpose and Context

Instructions documented in this section represent:
- Patient education materials provided
- Decision aids given to patients
- Medication-specific instructions
- Care instructions for conditions or procedures
- Vaccine Information Statements (VIS)
- Follow-up care instructions
- Self-care guidance

This section helps ensure patients and caregivers have clear documentation of the guidance they received during the encounter or hospitalization.

### When to Include

The Instructions Section is typically included in:
- **Discharge Summaries** (discharge instructions)
- **Procedure Notes** (post-procedure care)
- **Consultation Notes** (specialist guidance)
- **Visit Summaries** (patient education)

Use this section when documenting prospective instructions. For completed instruction activities (patient education already provided), use the Procedure Activity Act template instead.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.45
- **Extension:** 2014-06-09 (V2)

### Conformance Level
- **Conformance:** MAY (Optional)
- **Section Code:** 69730-0 (LOINC - "Instructions")

### Cardinality
- **Section:** 0..1 (Optional)
- **Entries:** 1..* (SHALL contain at least one entry if section is not nullFlavored)

### Related Templates
- **Instruction (V2):** 2.16.840.1.113883.10.20.22.4.20:2014-06-09
- **Procedure Activity Act:** For completed instruction activities

## Protocol Requirements

The `InstructionProtocol` defines the data contract for instruction entries. Each instruction must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `str` | Unique identifier for the instruction |
| `text` | `str` | The instruction text content |
| `status` | `str` | Status code (SHALL be 'completed') |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `code` | `Optional[str]` | Type of instruction code (from Patient Education value set) |
| `code_system` | `Optional[str]` | Code system (typically 'SNOMED') |
| `display_name` | `Optional[str]` | Human-readable display name for code |

### Data Types and Constraints
- **id:** UUID or other unique identifier
- **text:** Clear, actionable instruction text for patients
- **status:** Must be 'completed' per template requirements
- **code:** SHOULD be from Patient Education value set (2.16.840.1.113883.11.20.9.34)
- Common codes: "409073007" (Education), "311401005" (Patient education)

## Code Example

Here's a complete working example using ccdakit to create an Instructions Section:

```python
from ccdakit.builders.sections.instructions import InstructionsSection
from ccdakit.core.base import CDAVersion
import uuid

# Define instructions using a class that implements InstructionProtocol
class Instruction:
    def __init__(self, text, code=None, code_system=None, display_name=None):
        self._id = str(uuid.uuid4())
        self._text = text
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = "completed"

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name

    @property
    def status(self):
        return self._status

# Create instruction instances
instructions = [
    Instruction(
        text="Take aspirin 81mg by mouth once daily with food. Continue this medication unless directed otherwise by your physician.",
        code="409073007",
        code_system="SNOMED",
        display_name="Education"
    ),
    Instruction(
        text="Monitor your blood pressure daily at home. Record readings and bring the log to your follow-up appointment. Call your doctor if readings are consistently above 140/90.",
        code="311401005",
        code_system="SNOMED",
        display_name="Patient education"
    ),
    Instruction(
        text="Follow a low-sodium diet (less than 2000mg per day). Avoid processed foods, canned soups, and adding salt to meals. A dietitian will contact you for detailed counseling.",
        code="409073007",
        code_system="SNOMED",
        display_name="Education"
    ),
    Instruction(
        text="Follow up with your cardiologist within 7-10 days of discharge. Call to schedule the appointment within 48 hours.",
        code="409073007",
        code_system="SNOMED",
        display_name="Education"
    )
]

# Build the Instructions Section
section_builder = InstructionsSection(
    instructions=instructions,
    title="Instructions",
    version=CDAVersion.R2_1
)

# Generate XML element
section_element = section_builder.build()

# Convert to XML string (for demonstration)
from lxml import etree
xml_string = etree.tostring(section_element, pretty_print=True, encoding='unicode')
print(xml_string)

# Example: Creating section with null flavor (no instructions available)
section_no_info = InstructionsSection(
    instructions=[],
    title="Instructions",
    null_flavor="NI",  # No Information
    version=CDAVersion.R2_1
)
```

## Official Reference

For complete specification details, refer to the official HL7 C-CDA R2.1 documentation:
- [HL7 C-CDA R2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- Section: Instructions Section (V2)
- Entry: Instruction (V2)
- Conformance IDs: CONF:1098-10112 through CONF:1098-31398

## Best Practices

### Common Patterns

1. **Write Patient-Friendly Instructions**
   - Use clear, simple language
   - Avoid medical jargon when possible
   - Be specific and actionable
   - Include what, when, how, and why

2. **Organize by Category**
   - Group related instructions together
   - Medication instructions
   - Activity/lifestyle instructions
   - Monitoring instructions
   - Follow-up instructions

3. **Include Specific Details**
   - Exact doses and timing
   - Warning signs to watch for
   - When to call the doctor
   - Contact information

4. **Use Appropriate Codes**
   - Select codes from Patient Education value set when possible
   - "409073007" - Education (general)
   - "311401005" - Patient education
   - "710837008" - Medication education

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 69730-0 (LOINC "Instructions")
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes extension="2014-06-09"
   - Both V2 templates are included automatically

3. **Entry Requirements**
   - SHALL contain at least one entry if nullFlavor is not present
   - If no instructions, use nullFlavor="NI" on section element

4. **Instruction Status**
   - Status SHALL be "completed" for Instruction (V2) template
   - This indicates instruction was created, not that patient completed it

### Common Pitfalls

1. **Confusing with Procedure Activity**
   - Use Instructions Section for prospective guidance (what to do)
   - Use Procedure Activity Act for completed education (what was done)
   - Instructions are intent-based (moodCode=INT)

2. **Missing Required Entry**
   - If section is present without nullFlavor, must have at least one entry
   - Empty instructions list without nullFlavor fails validation
   - Use nullFlavor="NI" if no instructions available

3. **Incorrect Status Code**
   - Status must be "completed" per template requirement
   - Don't use "active" or other status codes
   - "Completed" means instruction was given, not followed

4. **Too Technical**
   - Instructions should be patient-facing
   - Avoid overly medical language
   - Write at appropriate health literacy level

5. **Missing Critical Information**
   - Don't assume patients remember verbal instructions
   - Include all key details in the text
   - Specify quantities, frequencies, durations

6. **Not Using Structured Format**
   - While text is free-form, consider consistent formatting
   - Numbered lists or clear paragraphs
   - Separate instructions for different topics

## Related Sections

- **Hospital Discharge Instructions Section:** Specific discharge guidance
- **Plan of Treatment Section:** Care plans and treatments
- **Medications Section:** Medication regimens
- **Procedure Section:** Procedures performed (if instructions were given as procedure)

## Code Systems and Terminologies

### Instruction Type Codes
- **Patient Education Value Set:** 2.16.840.1.113883.11.20.9.34
  - SNOMED CT codes for education and instruction
  - "409073007" - Education
  - "311401005" - Patient education
  - "710837008" - Medication education
  - "409066002" - Education, guidance, and counseling

### Section Codes
- **Primary:** 69730-0 - "Instructions" (LOINC)

### Status Codes
- **Fixed:** "completed" (required by Instruction V2 template)

## Implementation Notes

### Null Flavor Support

The section supports null flavor for cases where no instructions are available:

```python
section = InstructionsSection(
    instructions=[],
    null_flavor="NI",  # No Information
    version=CDAVersion.R2_1
)
```

Valid null flavors:
- **NI** - No Information
- **NA** - Not Applicable
- **UNK** - Unknown

### Narrative Table Generation

The builder creates a simple two-column table:
- **Instruction Type:** Display name from code or "Instruction"
- **Details:** The instruction text with content ID

### Text Property Flexibility

The builder supports both property names for backward compatibility:
- `text` (preferred)
- `instruction_text` (also supported)

### ID Generation

Each instruction requires a unique ID:
- Use UUID for new instructions
- Reuse IDs when referring to same instruction across documents
- IDs can be referenced by other document elements

### Integration with Other Content

Instructions often relate to:
- **Medications:** Medication-specific instructions
- **Procedures:** Post-procedure care instructions
- **Problems:** Disease management instructions
- **Plan of Treatment:** Treatment plan guidance

### Instruction vs. Procedure Activity

**Use Instructions Section when:**
- Providing prospective guidance
- Documenting what patient should do
- Recording decision aids or educational materials
- Intent-based (moodCode=INT)

**Use Procedure Activity Act when:**
- Documenting completed patient education
- Recording that teaching occurred
- Event-based (moodCode=EVN)
- Part of procedures section

### Multi-Topic Instructions

For complex discharge scenarios:
1. Create separate instruction entries for different topics
2. Use codes to categorize (medication, activity, diet, etc.)
3. Order instructions logically
4. Consider using display_name to show instruction category

### Patient Education Materials

When documenting specific educational materials:
- Reference the material name/title in the text
- Include version or date of material if applicable
- Document language of materials provided
- Consider linking to external resources (URLs) if appropriate

### Medication Instructions

For medication-specific instructions:
- Include in this section OR as part of Medication Activity
- Use code "710837008" for medication education
- Reference specific medication by name
- Include special administration instructions

### Follow-up Instructions

Common follow-up instruction patterns:
- Specify timeframe (e.g., "within 7-10 days")
- Include who to follow up with
- Provide contact information
- List warning signs that require earlier contact
