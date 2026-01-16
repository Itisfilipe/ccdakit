"""Example of creating a Hospital Discharge Instructions Section."""

from lxml import etree

from ccdakit.builders.sections.hospital_discharge_instructions import (
    HospitalDischargeInstructionsSection,
)
from ccdakit.core.base import CDAVersion


class MockDischargeInstruction:
    """Simple mock class implementing DischargeInstructionProtocol."""

    def __init__(self, instruction_text: str, instruction_category: str = None):
        self._instruction_text = instruction_text
        self._instruction_category = instruction_category

    @property
    def instruction_text(self) -> str:
        return self._instruction_text

    @property
    def instruction_category(self) -> str:
        return self._instruction_category


def main():
    """Create and display Hospital Discharge Instructions Section examples."""

    # Example 1: Simple narrative text only
    print("Example 1: Simple Discharge Instructions (Narrative Text Only)")
    print("=" * 80)

    simple_narrative = (
        "You are being discharged from the hospital. Please take all medications "
        "as prescribed, follow up with your primary care physician within 2 weeks, "
        "and call 911 if you experience any concerning symptoms."
    )
    section1 = HospitalDischargeInstructionsSection(
        narrative_text=simple_narrative,
        title="Hospital Discharge Instructions",
        version=CDAVersion.R2_1,
    )

    elem1 = section1.to_element()
    xml_string1 = etree.tostring(
        elem1, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string1)

    # Example 2: Structured instructions without categories
    print("\n" + "=" * 80)
    print("Example 2: Structured Instructions (Uncategorized)")
    print("=" * 80)

    instructions_simple = [
        MockDischargeInstruction("Take all medications as prescribed"),
        MockDischargeInstruction("Rest and avoid strenuous activity for 1 week"),
        MockDischargeInstruction("Follow up with Dr. Johnson in 2 weeks"),
        MockDischargeInstruction("Call 911 if you experience chest pain or difficulty breathing"),
        MockDischargeInstruction("Keep surgical wound clean and dry until follow-up visit"),
    ]

    section2 = HospitalDischargeInstructionsSection(
        instructions=instructions_simple,
        version=CDAVersion.R2_1,
    )

    elem2 = section2.to_element()
    xml_string2 = etree.tostring(
        elem2, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string2)

    # Example 3: Categorized instructions (most common use case)
    print("\n" + "=" * 80)
    print("Example 3: Comprehensive Categorized Discharge Instructions")
    print("=" * 80)

    instructions_categorized = [
        # Medications
        MockDischargeInstruction(
            "Take Aspirin 81mg once daily with food",
            instruction_category="Medications",
        ),
        MockDischargeInstruction(
            "Take Lisinopril 10mg once daily in the morning",
            instruction_category="Medications",
        ),
        MockDischargeInstruction(
            "Take Metoprolol 25mg twice daily for blood pressure",
            instruction_category="Medications",
        ),
        # Activity
        MockDischargeInstruction(
            "Avoid heavy lifting (more than 10 pounds) for 6 weeks",
            instruction_category="Activity",
        ),
        MockDischargeInstruction(
            "Walk 15-20 minutes twice daily as tolerated",
            instruction_category="Activity",
        ),
        MockDischargeInstruction(
            "No driving until cleared by your physician",
            instruction_category="Activity",
        ),
        # Diet
        MockDischargeInstruction(
            "Low sodium diet (less than 2000mg per day)",
            instruction_category="Diet",
        ),
        MockDischargeInstruction(
            "Heart-healthy diet with plenty of fruits and vegetables",
            instruction_category="Diet",
        ),
        MockDischargeInstruction(
            "Limit caffeine and alcohol consumption",
            instruction_category="Diet",
        ),
        # Follow-up Care
        MockDischargeInstruction(
            "Follow up with cardiologist Dr. Smith in 1 week",
            instruction_category="Follow-up Care",
        ),
        MockDischargeInstruction(
            "Schedule INR check at anticoagulation clinic in 3 days",
            instruction_category="Follow-up Care",
        ),
        # Uncategorized general instructions
        MockDischargeInstruction(
            "Monitor weight daily and report gain of more than 2 pounds in 24 hours"
        ),
        MockDischargeInstruction(
            "Call 911 immediately if you experience chest pain, severe shortness of breath, "
            "or severe dizziness"
        ),
    ]

    section3 = HospitalDischargeInstructionsSection(
        instructions=instructions_categorized,
        title="Discharge Instructions - Cardiac Care",
        version=CDAVersion.R2_1,
    )

    elem3 = section3.to_element()
    xml_string3 = etree.tostring(
        elem3, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string3)

    # Example 4: Combined narrative and structured instructions
    print("\n" + "=" * 80)
    print("Example 4: Narrative Preamble with Structured Instructions")
    print("=" * 80)

    preamble = (
        "You have been discharged from the hospital following successful surgery. "
        "It is very important that you follow all instructions carefully to ensure "
        "proper healing and recovery."
    )

    instructions_with_preamble = [
        MockDischargeInstruction(
            "Take pain medication (Hydrocodone 5mg) every 4-6 hours as needed",
            instruction_category="Medications",
        ),
        MockDischargeInstruction(
            "Take antibiotic (Cephalexin 500mg) three times daily for 7 days",
            instruction_category="Medications",
        ),
        MockDischargeInstruction(
            "Rest for the first 3 days, then gradually increase activity",
            instruction_category="Activity",
        ),
        MockDischargeInstruction(
            "No bathing or swimming for 2 weeks; showers are permitted after 48 hours",
            instruction_category="Activity",
        ),
        MockDischargeInstruction(
            "Resume normal diet as tolerated, starting with light meals",
            instruction_category="Diet",
        ),
        MockDischargeInstruction(
            "Follow up with surgeon Dr. Anderson in 10-14 days for suture removal",
            instruction_category="Follow-up Care",
        ),
    ]

    section4 = HospitalDischargeInstructionsSection(
        narrative_text=preamble,
        instructions=instructions_with_preamble,
        title="Post-Surgical Discharge Instructions",
        version=CDAVersion.R2_1,
    )

    elem4 = section4.to_element()
    xml_string4 = etree.tostring(
        elem4, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string4)

    # Example 5: C-CDA R2.0 version
    print("\n" + "=" * 80)
    print("Example 5: Hospital Discharge Instructions (C-CDA R2.0)")
    print("=" * 80)

    r20_narrative = (
        "DISCHARGE INSTRUCTIONS\n\n"
        "You are being discharged following treatment for pneumonia. "
        "Complete the full course of antibiotics even if you feel better. "
        "Rest and stay hydrated. Contact your doctor if fever persists or symptoms worsen."
    )

    section5 = HospitalDischargeInstructionsSection(
        narrative_text=r20_narrative,
        version=CDAVersion.R2_0,
    )

    elem5 = section5.to_element()
    xml_string5 = etree.tostring(
        elem5, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string5)

    # Show validation info
    print("\n" + "=" * 80)
    print("Section Summary:")
    print("=" * 80)
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.41")
    print("  - LOINC Code: 8653-8 (Hospital Discharge Instructions)")
    print("  - Section Type: Narrative-only (no structured entries required)")
    print("  - Versions: Supports both C-CDA R2.1 and R2.0")
    print("\nConformance Requirements:")
    print("  - CONF:81-9919: SHALL contain exactly one [1..1] templateId")
    print("  - CONF:81-10395: templateId/@root='2.16.840.1.113883.10.20.22.2.41'")
    print("  - CONF:81-15357: SHALL contain exactly one [1..1] code")
    print("  - CONF:81-15358: code/@code='8653-8' (Hospital Discharge Instructions)")
    print("  - CONF:81-26481: code/@codeSystem='2.16.840.1.113883.6.1' (LOINC)")
    print("  - CONF:81-9921: SHALL contain exactly one [1..1] title")
    print("  - CONF:81-9922: SHALL contain exactly one [1..1] text")
    print("\nUsage Notes:")
    print("  - This section records instructions provided to the patient at hospital discharge")
    print("  - Instructions can be provided as free-text narrative or structured by category")
    print("  - Common categories: Medications, Activity, Diet, Follow-up Care, Wound Care")
    print("  - No structured entries are required; this is a narrative-only section")
    print("  - Instructions should be clear, specific, and patient-friendly")

    # Display example categories and common instructions
    print("\n" + "=" * 80)
    print("Common Instruction Categories and Examples:")
    print("=" * 80)

    categories = {
        "Medications": [
            "Take all prescribed medications as directed",
            "Complete full course of antibiotics",
            "Do not stop medications without consulting physician",
            "Take pain medication as needed for comfort",
        ],
        "Activity": [
            "Rest for the first few days after discharge",
            "Gradually increase activity as tolerated",
            "Avoid heavy lifting or strenuous exercise",
            "No driving while taking narcotic pain medication",
        ],
        "Diet": [
            "Resume regular diet as tolerated",
            "Follow low sodium diet for heart health",
            "Stay hydrated with plenty of fluids",
            "Avoid alcohol while taking antibiotics",
        ],
        "Follow-up Care": [
            "Schedule follow-up appointment within specified timeframe",
            "Attend all scheduled lab work appointments",
            "Return for suture or staple removal as directed",
            "Contact physician if symptoms worsen",
        ],
        "Wound Care": [
            "Keep surgical site clean and dry",
            "Change dressings as instructed",
            "Watch for signs of infection (redness, swelling, drainage)",
            "No bathing or swimming until wounds are healed",
        ],
        "Warning Signs": [
            "Call 911 for chest pain, severe shortness of breath",
            "Contact physician for fever above 101F",
            "Report increased pain, redness, or swelling at surgical site",
            "Seek immediate care for confusion or severe dizziness",
        ],
    }

    for category, examples in categories.items():
        print(f"\n{category}:")
        for example in examples:
            print(f"  - {example}")

    print("\n" + "=" * 80)
    print("Example Integration:")
    print("=" * 80)
    print("This section is typically included in:")
    print("  - Hospital Discharge Summary documents")
    print("  - Continuity of Care Documents (CCD)")
    print("  - Transfer Summary documents")
    print("  - Patient education materials")
    print("\nThe section provides critical information for patients to follow")
    print("after leaving the hospital to ensure proper recovery and prevent")
    print("complications or readmissions.")


if __name__ == "__main__":
    main()
