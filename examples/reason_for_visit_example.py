"""Example of creating a Reason for Visit Section."""

from lxml import etree

from ccdakit.builders.sections.reason_for_visit import ReasonForVisitSection
from ccdakit.core.base import CDAVersion


def main():
    """Create and display a Reason for Visit Section example."""

    # Example 1: Simple reason for visit
    print("Example 1: Simple Reason for Visit")
    print("=" * 80)

    simple_reason = "Annual physical examination"
    section1 = ReasonForVisitSection(
        reason_text=simple_reason,
        title="Reason for Visit",
        version=CDAVersion.R2_1,
    )

    elem1 = section1.to_element()
    xml_string1 = etree.tostring(
        elem1, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string1)

    # Example 2: Detailed reason for visit
    print("\n" + "=" * 80)
    print("Example 2: Detailed Reason for Visit")
    print("=" * 80)

    detailed_reason = (
        "Patient presents for evaluation of progressively worsening shortness of breath "
        "over the past 3 weeks, associated with occasional wheezing and chest tightness. "
        "Patient has a past medical history significant for asthma and hypertension."
    )
    section2 = ReasonForVisitSection(
        reason_text=detailed_reason,
        version=CDAVersion.R2_1,
    )

    elem2 = section2.to_element()
    xml_string2 = etree.tostring(
        elem2, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string2)

    # Example 3: Follow-up visit
    print("\n" + "=" * 80)
    print("Example 3: Follow-up Visit")
    print("=" * 80)

    followup_reason = (
        "Follow-up visit for management of type 2 diabetes mellitus. "
        "Blood pressure has been well controlled on current medication. "
        "Patient reports good compliance with diet and exercise regimen."
    )
    section3 = ReasonForVisitSection(
        reason_text=followup_reason,
        title="Reason for Patient Visit",
        version=CDAVersion.R2_1,
    )

    elem3 = section3.to_element()
    xml_string3 = etree.tostring(
        elem3, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string3)

    # Example 4: C-CDA R2.0 version
    print("\n" + "=" * 80)
    print("Example 4: Reason for Visit (C-CDA R2.0)")
    print("=" * 80)

    r20_reason = "Post-operative wound check following appendectomy"
    section4 = ReasonForVisitSection(
        reason_text=r20_reason,
        version=CDAVersion.R2_0,
    )

    elem4 = section4.to_element()
    xml_string4 = etree.tostring(
        elem4, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string4)

    # Show validation info
    print("\n" + "=" * 80)
    print("Section Summary:")
    print("=" * 80)
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.12")
    print("  - LOINC Code: 29299-5 (Reason for Visit)")
    print("  - Section Type: Narrative-only (no structured entries)")
    print("  - Versions: Supports both C-CDA R2.1 and R2.0")
    print("\nConformance Requirements:")
    print("  - CONF:81-7836: SHALL contain exactly one [1..1] templateId")
    print("  - CONF:81-10448: templateId/@root='2.16.840.1.113883.10.20.22.2.12'")
    print("  - CONF:81-15429: SHALL contain exactly one [1..1] code")
    print("  - CONF:81-15430: code/@code='29299-5' (Reason for Visit)")
    print("  - CONF:81-26494: code/@codeSystem='2.16.840.1.113883.6.1' (LOINC)")
    print("  - CONF:81-7838: SHALL contain exactly one [1..1] title")
    print("  - CONF:81-7839: SHALL contain exactly one [1..1] text")
    print("\nUsage Notes:")
    print("  - This section records the patient's reason for visit as documented by the provider")
    print("  - Local policy determines whether Reason for Visit and Chief Complaint")
    print("    are in separate or combined sections")
    print("  - The section contains only narrative text without structured entries")
    print("  - Reason text should clearly explain why the patient is seeking care")

    # Display example use cases
    print("\n" + "=" * 80)
    print("Common Use Cases:")
    print("=" * 80)
    use_cases = [
        "Follow-up for diabetes mellitus type 2",
        "Evaluation of chest pain",
        "Annual physical examination",
        "Post-operative wound check",
        "Medication review and refill",
        "Hypertension management",
        "Pre-operative evaluation",
        "Workers compensation evaluation",
        "Routine prenatal visit",
        "Psychiatric medication management",
    ]

    for i, use_case in enumerate(use_cases, 1):
        print(f"  {i}. {use_case}")


if __name__ == "__main__":
    main()
