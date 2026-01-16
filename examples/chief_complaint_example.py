"""Example of creating a Chief Complaint and Reason for Visit Section."""

from lxml import etree

from ccdakit.builders.sections.chief_complaint_reason_for_visit import (
    ChiefComplaintAndReasonForVisitSection,
)
from ccdakit.core.base import CDAVersion


# Define chief complaint data
class ExampleChiefComplaint:
    """Example chief complaint for demonstration."""

    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text


def main():
    """Create and display a Chief Complaint and Reason for Visit Section example."""

    # Example 1: Single chief complaint
    print("Example 1: Single Chief Complaint")
    print("=" * 80)

    complaint1 = ExampleChiefComplaint(text="Chest pain radiating to left arm")

    section1 = ChiefComplaintAndReasonForVisitSection(
        chief_complaints=[complaint1],
        title="Chief Complaint",
        version=CDAVersion.R2_1,
    )

    elem1 = section1.to_element()
    xml_string1 = etree.tostring(
        elem1, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string1)

    # Example 2: Multiple chief complaints and reason for visit
    print("\n" + "=" * 80)
    print("Example 2: Multiple Chief Complaints and Reason for Visit")
    print("=" * 80)

    complaints2 = [
        ExampleChiefComplaint(text="Patient reports persistent cough for 3 weeks"),
        ExampleChiefComplaint(text="Shortness of breath when climbing stairs"),
        ExampleChiefComplaint(text="Follow-up visit for recent pneumonia diagnosis"),
    ]

    section2 = ChiefComplaintAndReasonForVisitSection(
        chief_complaints=complaints2,
        title="Chief Complaint and Reason for Visit",
        version=CDAVersion.R2_1,
    )

    elem2 = section2.to_element()
    xml_string2 = etree.tostring(
        elem2, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string2)

    # Example 3: Reason for visit (provider's perspective)
    print("\n" + "=" * 80)
    print("Example 3: Reason for Visit (Provider's Perspective)")
    print("=" * 80)

    reason = ExampleChiefComplaint(
        text="Annual physical examination and diabetes management review"
    )

    section3 = ChiefComplaintAndReasonForVisitSection(
        chief_complaints=[reason],
        title="Reason for Visit",
        version=CDAVersion.R2_1,
    )

    elem3 = section3.to_element()
    xml_string3 = etree.tostring(
        elem3, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string3)

    # Example 4: No chief complaint documented
    print("\n" + "=" * 80)
    print("Example 4: No Chief Complaint Documented")
    print("=" * 80)

    section4 = ChiefComplaintAndReasonForVisitSection(
        chief_complaints=None,
        version=CDAVersion.R2_1,
    )

    elem4 = section4.to_element()
    xml_string4 = etree.tostring(
        elem4, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string4)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.13")
    print("  - LOINC Code: 46239-0 (Chief Complaint and Reason for Visit)")
    print("  - Section Type: Narrative-only (no structured entries)")
    print("  - Supported Versions: R2.1 and R2.0")
    print("\nConformance:")
    print("  - CONF:81-7840: Template ID present")
    print("  - CONF:81-10383: templateId/@root='2.16.840.1.113883.10.20.22.2.13'")
    print("  - CONF:81-15449: Code present")
    print("  - CONF:81-15450: code/@code='46239-0'")
    print("  - CONF:81-26473: code/@codeSystem='2.16.840.1.113883.6.1' (LOINC)")
    print("  - CONF:81-7842: Title present")
    print("  - CONF:81-7843: Narrative text present")
    print("\nUsage Notes:")
    print("  - This section records the patient's own description (chief complaint)")
    print("  - Or the provider's description of the reason for visit")
    print("  - Local policy determines if information is divided into two sections")
    print("    or recorded in one section serving both purposes")
    print("  - Single complaint displays as paragraph")
    print("  - Multiple complaints display as list")


if __name__ == "__main__":
    main()
