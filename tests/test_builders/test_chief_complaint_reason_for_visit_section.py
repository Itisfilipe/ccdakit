"""Tests for ChiefComplaintAndReasonForVisitSection builder."""

from lxml import etree

from ccdakit.builders.sections.chief_complaint_reason_for_visit import (
    ChiefComplaintAndReasonForVisitSection,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockChiefComplaint:
    """Mock chief complaint for testing."""

    def __init__(self, text="Chest pain"):
        self._text = text

    @property
    def text(self):
        return self._text


class TestChiefComplaintAndReasonForVisitSection:
    """Tests for ChiefComplaintAndReasonForVisitSection builder."""

    def test_section_basic(self):
        """Test basic ChiefComplaintAndReasonForVisitSection creation."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:81-7840, CONF:81-10383)."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints, version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.13"
        # No extension for this template
        assert template.get("extension") is None

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID (CONF:81-7840, CONF:81-10383)."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints, version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.13"
        # No extension for this template
        assert template.get("extension") is None

    def test_section_has_code(self):
        """Test section includes correct code (CONF:81-15449, CONF:81-15450, CONF:81-26473)."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "46239-0"  # Chief Complaint and Reason for Visit
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Chief Complaint and Reason for Visit"

    def test_section_has_title(self):
        """Test section includes title (CONF:81-7842)."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(
            complaints, title="Patient Chief Complaint"
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Chief Complaint"

    def test_section_default_title(self):
        """Test section uses default title."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Chief Complaint and Reason for Visit"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:81-7843)."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_single_complaint_as_paragraph(self):
        """Test single complaint displays as paragraph."""
        complaints = [MockChiefComplaint(text="Chest pain")]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None

        content = paragraph.find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Chest pain"
        assert content.get("ID") == "chief-complaint-1"

    def test_narrative_multiple_complaints_as_list(self):
        """Test multiple complaints display as list."""
        complaints = [
            MockChiefComplaint(text="Chest pain"),
            MockChiefComplaint(text="Shortness of breath"),
            MockChiefComplaint(text="Nausea"),
        ]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None

        items = list_elem.findall(f"{{{NS}}}item")
        assert len(items) == 3

        # Check first item
        content1 = items[0].find(f"{{{NS}}}content")
        assert content1.text == "Chest pain"
        assert content1.get("ID") == "chief-complaint-1"

        # Check second item
        content2 = items[1].find(f"{{{NS}}}content")
        assert content2.text == "Shortness of breath"
        assert content2.get("ID") == "chief-complaint-2"

        # Check third item
        content3 = items[2].find(f"{{{NS}}}content")
        assert content3.text == "Nausea"
        assert content3.get("ID") == "chief-complaint-3"

    def test_narrative_empty_complaints(self):
        """Test narrative when no complaints provided."""
        section = ChiefComplaintAndReasonForVisitSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not list
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No chief complaint or reason for visit documented"

        # Should not have list
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is None

    def test_narrative_none_complaints(self):
        """Test narrative when None is passed for complaints."""
        section = ChiefComplaintAndReasonForVisitSection(None)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No chief complaint or reason for visit documented"

    def test_section_no_entries(self):
        """Test section does not include entry elements.

        This section is narrative-only and should not have structured entries.
        """
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_to_string(self):
        """Test section serialization."""
        complaints = [MockChiefComplaint(text="Fever and cough")]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "46239-0" in xml  # Section code
        assert "Chief Complaint" in xml
        assert "Fever and cough" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names

        # templateId should come before code
        assert names.index("templateId") < names.index("code")
        # code should come before title
        assert names.index("code") < names.index("title")
        # title should come before text
        assert names.index("title") < names.index("text")

        # Should not have entry
        assert "entry" not in names

    def test_section_with_various_complaint_types(self):
        """Test section with various types of chief complaints."""
        complaints = [
            MockChiefComplaint(text="Acute chest pain radiating to left arm"),
            MockChiefComplaint(text="Persistent cough for 3 weeks"),
            MockChiefComplaint(text="Annual physical examination"),
            MockChiefComplaint(text="Follow-up for hypertension management"),
        ]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        items = list_elem.findall(f"{{{NS}}}item")

        assert len(items) == 4

        # Verify all complaints are present
        contents = [item.find(f"{{{NS}}}content") for item in items]
        texts = [content.text for content in contents]

        assert "Acute chest pain radiating to left arm" in texts
        assert "Persistent cough for 3 weeks" in texts
        assert "Annual physical examination" in texts
        assert "Follow-up for hypertension management" in texts

    def test_section_with_special_characters(self):
        """Test section handles special characters in complaint text."""
        complaints = [
            MockChiefComplaint(text='Patient reports "stabbing" pain in lower abdomen'),
        ]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        content = paragraph.find(f"{{{NS}}}content")

        assert "stabbing" in content.text
        assert "abdomen" in content.text

    def test_section_with_long_complaint_text(self):
        """Test section handles long complaint text."""
        long_text = (
            "Patient presents with severe headache that started 2 days ago, "
            "accompanied by nausea, vomiting, photophobia, and phonophobia. "
            "The pain is described as throbbing and is located primarily in "
            "the frontal region. No history of similar episodes in the past. "
            "Patient also reports recent travel to a tropical region."
        )
        complaints = [MockChiefComplaint(text=long_text)]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        content = paragraph.find(f"{{{NS}}}content")

        assert content.text == long_text

    def test_section_id_references_sequential(self):
        """Test that content ID references are sequential."""
        complaints = [
            MockChiefComplaint(text="Complaint 1"),
            MockChiefComplaint(text="Complaint 2"),
            MockChiefComplaint(text="Complaint 3"),
            MockChiefComplaint(text="Complaint 4"),
            MockChiefComplaint(text="Complaint 5"),
        ]
        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        items = list_elem.findall(f"{{{NS}}}item")

        for idx, item in enumerate(items, start=1):
            content = item.find(f"{{{NS}}}content")
            assert content.get("ID") == f"chief-complaint-{idx}"


class TestChiefComplaintAndReasonForVisitSectionIntegration:
    """Integration tests for ChiefComplaintAndReasonForVisitSection."""

    def test_complete_section_single_complaint(self):
        """Test creating a complete section with single complaint."""
        complaints = [MockChiefComplaint(text="Patient complains of severe headache")]

        section = ChiefComplaintAndReasonForVisitSection(
            complaints,
            title="Chief Complaint",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.13"

        # Verify code
        code = elem.find(f"{{{NS}}}code")
        assert code.get("code") == "46239-0"

        # Verify title
        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Chief Complaint"

        # Verify narrative
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None

    def test_complete_section_multiple_complaints(self):
        """Test creating a complete section with multiple complaints."""
        complaints = [
            MockChiefComplaint(text="Chest pain"),
            MockChiefComplaint(text="Shortness of breath"),
        ]

        section = ChiefComplaintAndReasonForVisitSection(
            complaints,
            title="Chief Complaint and Reason for Visit",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative list
        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        items = list_elem.findall(f"{{{NS}}}item")
        assert len(items) == 2

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        complaints = [MockChiefComplaint(text="Annual checkup")]
        section = ChiefComplaintAndReasonForVisitSection(complaints)

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_r20_version(self):
        """Test section with R2.0 version."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints, version=CDAVersion.R2_0)
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.13"
        assert template.get("extension") is None

        # Verify other required elements are present
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_r21_version(self):
        """Test section with R2.1 version."""
        complaints = [MockChiefComplaint()]
        section = ChiefComplaintAndReasonForVisitSection(complaints, version=CDAVersion.R2_1)
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.13"
        assert template.get("extension") is None

        # Verify other required elements are present
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_empty_complaints_list(self):
        """Test section with empty complaints list."""
        section = ChiefComplaintAndReasonForVisitSection([])
        elem = section.to_element()

        # Should still have all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Text should have default message
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == "No chief complaint or reason for visit documented"

        # Should not have any entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_with_reason_for_visit_text(self):
        """Test section with provider's reason for visit (not patient's complaint)."""
        complaints = [MockChiefComplaint(text="Follow-up visit for diabetes management")]

        section = ChiefComplaintAndReasonForVisitSection(
            complaints,
            title="Reason for Visit",
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Reason for Visit"

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        content = paragraph.find(f"{{{NS}}}content")
        assert content.text == "Follow-up visit for diabetes management"

    def test_section_with_combined_complaint_and_reason(self):
        """Test section combining both chief complaint and reason for visit."""
        complaints = [
            MockChiefComplaint(text="Patient complains of persistent cough"),
            MockChiefComplaint(text="Follow-up for recent pneumonia diagnosis"),
        ]

        section = ChiefComplaintAndReasonForVisitSection(complaints)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        items = list_elem.findall(f"{{{NS}}}item")

        assert len(items) == 2

        contents = [item.find(f"{{{NS}}}content").text for item in items]
        assert "Patient complains of persistent cough" in contents
        assert "Follow-up for recent pneumonia diagnosis" in contents

    def test_minimal_section(self):
        """Test minimal valid section with no complaints."""
        section = ChiefComplaintAndReasonForVisitSection()
        elem = section.to_element()

        # All required elements should be present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have exactly 4 children (templateId, code, title, text)
        assert len(list(elem)) == 4

    def test_section_conforms_to_all_conformance_rules(self):
        """Test that section conforms to all CONF rules from spec."""
        complaints = [MockChiefComplaint(text="Test complaint")]
        section = ChiefComplaintAndReasonForVisitSection(complaints, version=CDAVersion.R2_1)
        elem = section.to_element()

        # CONF:81-7840: SHALL contain exactly one [1..1] templateId
        template_ids = elem.findall(f"{{{NS}}}templateId")
        assert len(template_ids) == 1

        # CONF:81-10383: templateId/@root="2.16.840.1.113883.10.20.22.2.13"
        assert template_ids[0].get("root") == "2.16.840.1.113883.10.20.22.2.13"

        # CONF:81-15449: SHALL contain exactly one [1..1] code
        codes = elem.findall(f"{{{NS}}}code")
        assert len(codes) == 1

        # CONF:81-15450: code/@code="46239-0"
        assert codes[0].get("code") == "46239-0"

        # CONF:81-26473: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        assert codes[0].get("codeSystem") == "2.16.840.1.113883.6.1"

        # CONF:81-7842: SHALL contain exactly one [1..1] title
        titles = elem.findall(f"{{{NS}}}title")
        assert len(titles) == 1

        # CONF:81-7843: SHALL contain exactly one [1..1] text
        texts = elem.findall(f"{{{NS}}}text")
        assert len(texts) == 1
