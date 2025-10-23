"""Tests for PostoperativeDiagnosisSection builder."""

from lxml import etree

from ccdakit.builders.sections.postoperative_diagnosis import (
    PostoperativeDiagnosisSection,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class TestPostoperativeDiagnosisSection:
    """Tests for PostoperativeDiagnosisSection builder."""

    def test_section_basic(self):
        """Test basic PostoperativeDiagnosisSection creation."""
        section = PostoperativeDiagnosisSection(
            "Appendicitis with periappendiceal abscess"
        )
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:81-8101, CONF:81-10437)."""
        section = PostoperativeDiagnosisSection(
            "Acute cholecystitis",
            version=CDAVersion.R2_1,
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.35"
        # No extension specified for this section
        assert template.get("extension") is None

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        section = PostoperativeDiagnosisSection(
            "Perforated duodenal ulcer",
            version=CDAVersion.R2_0,
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.35"
        assert template.get("extension") is None

    def test_section_has_code(self):
        """Test section includes correct code (CONF:81-15401, CONF:81-15402, CONF:81-26488)."""
        section = PostoperativeDiagnosisSection("Inguinal hernia")
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10218-6"  # Postoperative Diagnosis
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Postoperative Diagnosis"

    def test_section_has_title(self):
        """Test section includes title (CONF:81-8103)."""
        section = PostoperativeDiagnosisSection(
            "Gastric perforation",
            title="Post-Operative Diagnosis",
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Post-Operative Diagnosis"

    def test_section_default_title(self):
        """Test section uses default title."""
        section = PostoperativeDiagnosisSection("Torn meniscus")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Postoperative Diagnosis"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:81-8104)."""
        section = PostoperativeDiagnosisSection("Fractured femur")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_paragraph(self):
        """Test narrative includes paragraph with diagnosis text."""
        diagnosis = "Appendicitis with periappendiceal abscess"
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == diagnosis

    def test_narrative_content(self):
        """Test narrative contains the diagnosis text correctly."""
        diagnosis = (
            "Acute cholecystitis with gallstones, chronic cholecystitis, "
            "and mild peritoneal inflammation"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == diagnosis

    def test_section_no_entries(self):
        """Test section does not contain entry elements."""
        section = PostoperativeDiagnosisSection("Diverticulitis")
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_to_string(self):
        """Test section serialization."""
        section = PostoperativeDiagnosisSection(
            "Appendicitis with periappendiceal abscess"
        )
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "10218-6" in xml  # Section code
        assert "Postoperative Diagnosis" in xml
        assert "periappendiceal abscess" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        section = PostoperativeDiagnosisSection("Colon cancer")
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

    def test_section_with_simple_diagnosis(self):
        """Test section with simple diagnosis text."""
        section = PostoperativeDiagnosisSection("Appendicitis")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == "Appendicitis"

    def test_section_with_detailed_diagnosis(self):
        """Test section with detailed diagnosis text."""
        diagnosis = (
            "Acute perforated appendicitis with localized peritonitis, "
            "appendiceal abscess, and reactive lymphadenopathy"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == diagnosis

    def test_section_with_multiple_diagnoses(self):
        """Test section with multiple diagnoses in text."""
        diagnosis = (
            "1. Acute cholecystitis with gallstones\n"
            "2. Chronic cholecystitis\n"
            "3. Mild peritoneal inflammation"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == diagnosis

    def test_section_with_special_characters(self):
        """Test section with special characters in diagnosis text."""
        diagnosis = "Patient's acute appendicitis & peritonitis (severe)"
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == diagnosis

    def test_section_with_empty_string(self):
        """Test section with empty diagnosis text."""
        section = PostoperativeDiagnosisSection("")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == ""

    def test_section_with_whitespace(self):
        """Test section preserves whitespace in diagnosis text."""
        diagnosis = "  Appendicitis  "
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == diagnosis

    def test_section_with_medical_terminology(self):
        """Test section with complex medical terminology."""
        diagnosis = (
            "Perforated sigmoid diverticulitis with diffuse purulent peritonitis "
            "and retroperitoneal abscess formation"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == diagnosis

    def test_section_version_r20(self):
        """Test section with R2.0 version."""
        section = PostoperativeDiagnosisSection(
            "Ruptured ovarian cyst",
            version=CDAVersion.R2_0,
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.35"
        assert template.get("extension") is None

        # Check other required elements
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_version_r21(self):
        """Test section with R2.1 version."""
        section = PostoperativeDiagnosisSection(
            "Gastric ulcer perforation",
            version=CDAVersion.R2_1,
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.35"
        assert template.get("extension") is None

        # Check other required elements
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        section = PostoperativeDiagnosisSection("Bowel obstruction")

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_xml_namespaces(self):
        """Test section uses correct XML namespaces."""
        section = PostoperativeDiagnosisSection("Pneumothorax")
        elem = section.to_element()

        # Check namespace
        assert elem.tag == f"{{{NS}}}section"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_with_unicode_characters(self):
        """Test section with unicode characters in diagnosis text."""
        diagnosis = (
            "Gastric perforation (español: perforación gástrica), "
            "status post laparotomy"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == diagnosis


class TestPostoperativeDiagnosisSectionIntegration:
    """Integration tests for PostoperativeDiagnosisSection."""

    def test_complete_section(self):
        """Test creating a complete postoperative diagnosis section."""
        section = PostoperativeDiagnosisSection(
            diagnosis_text=(
                "Acute perforated appendicitis with localized peritonitis. "
                "Appendiceal abscess formation noted during procedure. "
                "Reactive mesenteric lymphadenopathy."
            ),
            title="Postoperative Diagnosis",
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
        assert "perforated appendicitis" in paragraph.text

    def test_section_protocol_implementation(self):
        """Test section with protocol-compliant object."""

        class MockPostoperativeDiagnosis:
            """Mock postoperative diagnosis object."""

            @property
            def diagnosis_text(self):
                return "Ruptured ectopic pregnancy in right fallopian tube"

        mock_diagnosis = MockPostoperativeDiagnosis()
        section = PostoperativeDiagnosisSection(mock_diagnosis.diagnosis_text)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == "Ruptured ectopic pregnancy in right fallopian tube"

    def test_section_various_surgical_diagnoses(self):
        """Test section with various surgical diagnoses."""
        test_cases = [
            "Appendicitis with periappendiceal abscess",
            "Acute cholecystitis with gallstones",
            "Perforated duodenal ulcer",
            "Inguinal hernia, right side",
            "Acute diverticulitis with perforation",
            "Bowel obstruction secondary to adhesions",
            "Ruptured ovarian cyst with hemoperitoneum",
            "Torn anterior cruciate ligament, left knee",
            "Carpal tunnel syndrome, bilateral",
            "Lumbar disc herniation at L4-L5",
        ]

        for diagnosis in test_cases:
            section = PostoperativeDiagnosisSection(diagnosis)
            elem = section.to_element()

            # Verify each section is properly constructed
            assert elem.find(f"{{{NS}}}templateId") is not None
            assert elem.find(f"{{{NS}}}code") is not None
            assert elem.find(f"{{{NS}}}title") is not None

            text = elem.find(f"{{{NS}}}text")
            paragraph = text.find(f"{{{NS}}}paragraph")
            assert paragraph.text == diagnosis

    def test_section_serialization_and_parsing(self):
        """Test section can be serialized and parsed."""
        section = PostoperativeDiagnosisSection(
            "Appendicitis with periappendiceal abscess"
        )
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
        diagnosis = "Perforated gastric ulcer with peritonitis"

        # R2.0 version
        section_r20 = PostoperativeDiagnosisSection(
            diagnosis,
            version=CDAVersion.R2_0,
        )
        elem_r20 = section_r20.to_element()

        # R2.1 version
        section_r21 = PostoperativeDiagnosisSection(
            diagnosis,
            version=CDAVersion.R2_1,
        )
        elem_r21 = section_r21.to_element()

        # Both should have the same structure
        for elem in [elem_r20, elem_r21]:
            assert elem.find(f"{{{NS}}}templateId") is not None
            assert elem.find(f"{{{NS}}}code") is not None
            assert elem.find(f"{{{NS}}}title") is not None
            assert elem.find(f"{{{NS}}}text") is not None

    def test_section_conformance_requirements(self):
        """Test all conformance requirements are met."""
        section = PostoperativeDiagnosisSection("Acute appendicitis")
        elem = section.to_element()

        # CONF:81-8101: SHALL contain exactly one [1..1] templateId
        template_ids = elem.findall(f"{{{NS}}}templateId")
        assert len(template_ids) == 1

        # CONF:81-10437: templateId/@root="2.16.840.1.113883.10.20.22.2.35"
        assert template_ids[0].get("root") == "2.16.840.1.113883.10.20.22.2.35"

        # CONF:81-15401: SHALL contain exactly one [1..1] code
        codes = elem.findall(f"{{{NS}}}code")
        assert len(codes) == 1

        # CONF:81-15402: code/@code="10218-6"
        assert codes[0].get("code") == "10218-6"

        # CONF:81-26488: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        assert codes[0].get("codeSystem") == "2.16.840.1.113883.6.1"

        # CONF:81-8103: SHALL contain exactly one [1..1] title
        titles = elem.findall(f"{{{NS}}}title")
        assert len(titles) == 1

        # CONF:81-8104: SHALL contain exactly one [1..1] text
        texts = elem.findall(f"{{{NS}}}text")
        assert len(texts) == 1

    def test_section_minimal_valid(self):
        """Test section with minimal valid data."""
        section = PostoperativeDiagnosisSection("Hernia")
        elem = section.to_element()

        # Should still have all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

    def test_section_complex_narrative(self):
        """Test section with complex narrative."""
        diagnosis = (
            "Acute perforated appendicitis with diffuse peritonitis, "
            "appendiceal abscess measuring 3.5cm in right lower quadrant, "
            "and reactive mesenteric lymphadenopathy. Incidental finding of "
            "Meckel's diverticulum in distal ileum, approximately 60cm from "
            "ileocecal valve."
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert len(paragraph.text) > 100
        assert "appendicitis" in paragraph.text
        assert "Meckel's diverticulum" in paragraph.text

    def test_section_same_as_preoperative(self):
        """Test section when diagnosis is same as preoperative."""
        diagnosis = "Acute appendicitis (confirmed, same as preoperative diagnosis)"
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert "same as preoperative" in paragraph.text

    def test_section_changed_from_preoperative(self):
        """Test section when diagnosis differs from preoperative."""
        diagnosis = (
            "Perforated sigmoid diverticulitis with purulent peritonitis "
            "(preoperative diagnosis was suspected appendicitis)"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert "diverticulitis" in paragraph.text
        assert "preoperative" in paragraph.text

    def test_section_with_staging_information(self):
        """Test section with cancer staging information."""
        diagnosis = (
            "Adenocarcinoma of the sigmoid colon, pT3N1M0, "
            "Stage IIIB (AJCC 8th edition)"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert "pT3N1M0" in paragraph.text
        assert "Stage IIIB" in paragraph.text

    def test_section_with_anatomical_details(self):
        """Test section with detailed anatomical information."""
        diagnosis = (
            "Ruptured abdominal aortic aneurysm, infrarenal, "
            "measuring 6.8cm in maximum diameter with retroperitoneal hematoma"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert "infrarenal" in paragraph.text
        assert "6.8cm" in paragraph.text

    def test_section_with_multiple_surgical_findings(self):
        """Test section with multiple operative findings."""
        diagnosis = (
            "1. Acute gangrenous cholecystitis with empyema\n"
            "2. Cholelithiasis with multiple stones\n"
            "3. Chronic inflammation of gallbladder wall\n"
            "4. Mild hepatic steatosis (incidental finding)"
        )
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert "gangrenous cholecystitis" in paragraph.text
        assert "hepatic steatosis" in paragraph.text
        assert "incidental" in paragraph.text

    def test_section_operative_note_context(self):
        """Test section in operative note context."""
        # This section is contained by Operative Note (V3)
        diagnosis = "Appendicitis with periappendiceal abscess"
        section = PostoperativeDiagnosisSection(diagnosis)
        elem = section.to_element()

        # Verify it's a valid section
        assert local_name(elem) == "section"

        # Verify all conformance requirements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None
