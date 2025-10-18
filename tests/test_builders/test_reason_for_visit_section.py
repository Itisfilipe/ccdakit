"""Tests for ReasonForVisitSection builder."""

from lxml import etree

from ccdakit.builders.sections.reason_for_visit import ReasonForVisitSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class TestReasonForVisitSection:
    """Tests for ReasonForVisitSection builder."""

    def test_section_basic(self):
        """Test basic ReasonForVisitSection creation."""
        section = ReasonForVisitSection("Follow-up for hypertension")
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:81-7836, CONF:81-10448)."""
        section = ReasonForVisitSection(
            "Annual physical exam",
            version=CDAVersion.R2_1,
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.12"
        # R2.1 does not specify extension for this section
        assert template.get("extension") is None

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        section = ReasonForVisitSection(
            "Chest pain evaluation",
            version=CDAVersion.R2_0,
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.12"
        assert template.get("extension") is None

    def test_section_has_code(self):
        """Test section includes correct code (CONF:81-15429, CONF:81-15430, CONF:81-26494)."""
        section = ReasonForVisitSection("Routine checkup")
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "29299-5"  # Reason for Visit
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Reason for Visit"

    def test_section_has_title(self):
        """Test section includes title (CONF:81-7838)."""
        section = ReasonForVisitSection(
            "Follow-up diabetes",
            title="Reason for Patient Visit",
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Reason for Patient Visit"

    def test_section_default_title(self):
        """Test section uses default title."""
        section = ReasonForVisitSection("Fever and cough")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Reason for Visit"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:81-7839)."""
        section = ReasonForVisitSection("Back pain assessment")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_paragraph(self):
        """Test narrative includes paragraph with reason text."""
        reason = "Patient presents for evaluation of persistent headaches"
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == reason

    def test_narrative_content(self):
        """Test narrative contains the reason text correctly."""
        reason = "Follow-up visit for management of type 2 diabetes mellitus"
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == reason

    def test_section_no_entries(self):
        """Test section does not contain entry elements."""
        section = ReasonForVisitSection("Annual wellness visit")
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_to_string(self):
        """Test section serialization."""
        section = ReasonForVisitSection("Routine examination")
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "29299-5" in xml  # Section code
        assert "Reason for Visit" in xml
        assert "Routine examination" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        section = ReasonForVisitSection("Blood pressure check")
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

    def test_section_with_simple_reason(self):
        """Test section with simple reason text."""
        section = ReasonForVisitSection("Cough")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == "Cough"

    def test_section_with_detailed_reason(self):
        """Test section with detailed reason text."""
        reason = (
            "Patient presents for evaluation of progressively worsening "
            "shortness of breath over the past 3 weeks, associated with "
            "occasional wheezing and chest tightness"
        )
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == reason

    def test_section_with_multiline_reason(self):
        """Test section with multiline reason text."""
        reason = "Diabetes follow-up\nMedication refill\nLab review"
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == reason

    def test_section_with_special_characters(self):
        """Test section with special characters in reason text."""
        reason = "Follow-up for patient's chronic lower back pain & sciatica"
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == reason

    def test_section_with_empty_string(self):
        """Test section with empty reason text."""
        section = ReasonForVisitSection("")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == ""

    def test_section_with_whitespace(self):
        """Test section preserves whitespace in reason text."""
        reason = "  Follow-up visit  "
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == reason

    def test_section_with_numeric_text(self):
        """Test section with numeric characters in reason text."""
        reason = "3-month follow-up for hypertension"
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == reason

    def test_section_version_r20(self):
        """Test section with R2.0 version."""
        section = ReasonForVisitSection(
            "Medication review",
            version=CDAVersion.R2_0,
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.12"
        assert template.get("extension") is None

        # Check other required elements
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_version_r21(self):
        """Test section with R2.1 version."""
        section = ReasonForVisitSection(
            "Asthma exacerbation",
            version=CDAVersion.R2_1,
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.12"
        assert template.get("extension") is None

        # Check other required elements
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        section = ReasonForVisitSection("Knee pain evaluation")

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_xml_namespaces(self):
        """Test section uses correct XML namespaces."""
        section = ReasonForVisitSection("Sore throat")
        elem = section.to_element()

        # Check namespace
        assert elem.tag == f"{{{NS}}}section"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_with_unicode_characters(self):
        """Test section with unicode characters in reason text."""
        reason = "Follow-up for patient's chronic pain (español: dolor crónico)"
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == reason


class TestReasonForVisitSectionIntegration:
    """Integration tests for ReasonForVisitSection."""

    def test_complete_section(self):
        """Test creating a complete reason for visit section."""
        section = ReasonForVisitSection(
            reason_text="Patient presents for follow-up of hypertension and diabetes. "
            "Blood pressure has been well controlled on current medication. "
            "Patient reports good compliance with diet and exercise regimen.",
            title="Reason for Visit",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify all required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Verify narrative
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "hypertension and diabetes" in paragraph.text

    def test_section_protocol_implementation(self):
        """Test section with protocol-compliant object."""

        class MockReasonForVisit:
            """Mock reason for visit object."""

            @property
            def reason_text(self):
                return "Annual wellness visit for preventive care"

        mock_reason = MockReasonForVisit()
        section = ReasonForVisitSection(mock_reason.reason_text)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == "Annual wellness visit for preventive care"

    def test_section_various_use_cases(self):
        """Test section with various clinical use cases."""
        test_cases = [
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

        for reason in test_cases:
            section = ReasonForVisitSection(reason)
            elem = section.to_element()

            # Verify each section is properly constructed
            assert elem.find(f"{{{NS}}}templateId") is not None
            assert elem.find(f"{{{NS}}}code") is not None
            assert elem.find(f"{{{NS}}}title") is not None

            text = elem.find(f"{{{NS}}}text")
            paragraph = text.find(f"{{{NS}}}paragraph")
            assert paragraph.text == reason

    def test_section_serialization_and_parsing(self):
        """Test section can be serialized and parsed."""
        section = ReasonForVisitSection("Routine checkup")
        xml_str = section.to_string(pretty=True)

        # Parse the XML string
        parsed = etree.fromstring(xml_str.encode("utf-8"))

        assert local_name(parsed) == "section"
        assert parsed.find(f"{{{NS}}}templateId") is not None
        assert parsed.find(f"{{{NS}}}code") is not None
        assert parsed.find(f"{{{NS}}}title") is not None
        assert parsed.find(f"{{{NS}}}text") is not None

    def test_section_with_both_versions(self):
        """Test section generation for both R2.0 and R2.1."""
        reason = "Follow-up for chronic condition"

        # R2.0 version
        section_r20 = ReasonForVisitSection(reason, version=CDAVersion.R2_0)
        elem_r20 = section_r20.to_element()

        # R2.1 version
        section_r21 = ReasonForVisitSection(reason, version=CDAVersion.R2_1)
        elem_r21 = section_r21.to_element()

        # Both should have the same structure
        for elem in [elem_r20, elem_r21]:
            assert elem.find(f"{{{NS}}}templateId") is not None
            assert elem.find(f"{{{NS}}}code") is not None
            assert elem.find(f"{{{NS}}}title") is not None
            assert elem.find(f"{{{NS}}}text") is not None

    def test_section_conformance_requirements(self):
        """Test all conformance requirements are met."""
        section = ReasonForVisitSection("Follow-up visit")
        elem = section.to_element()

        # CONF:81-7836: SHALL contain exactly one [1..1] templateId
        template_ids = elem.findall(f"{{{NS}}}templateId")
        assert len(template_ids) == 1

        # CONF:81-10448: templateId/@root="2.16.840.1.113883.10.20.22.2.12"
        assert template_ids[0].get("root") == "2.16.840.1.113883.10.20.22.2.12"

        # CONF:81-15429: SHALL contain exactly one [1..1] code
        codes = elem.findall(f"{{{NS}}}code")
        assert len(codes) == 1

        # CONF:81-15430: code/@code="29299-5"
        assert codes[0].get("code") == "29299-5"

        # CONF:81-26494: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        assert codes[0].get("codeSystem") == "2.16.840.1.113883.6.1"

        # CONF:81-7838: SHALL contain exactly one [1..1] title
        titles = elem.findall(f"{{{NS}}}title")
        assert len(titles) == 1

        # CONF:81-7839: SHALL contain exactly one [1..1] text
        texts = elem.findall(f"{{{NS}}}text")
        assert len(texts) == 1

    def test_section_minimal_valid(self):
        """Test section with minimal valid data."""
        section = ReasonForVisitSection("Visit")
        elem = section.to_element()

        # Should still have all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_complex_narrative(self):
        """Test section with complex narrative."""
        reason = (
            "Patient presents for evaluation of new onset dyspnea on exertion, "
            "which has been progressively worsening over the past 2 months. "
            "Associated symptoms include orthopnea and lower extremity edema. "
            "Patient has a past medical history significant for hypertension "
            "and coronary artery disease."
        )
        section = ReasonForVisitSection(reason)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert len(paragraph.text) > 100
        assert "dyspnea" in paragraph.text
        assert "hypertension" in paragraph.text
