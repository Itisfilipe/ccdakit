"""Tests for HospitalCourseSection builder."""

from lxml import etree

from ccdakit.builders.sections.hospital_course import HospitalCourseSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockHospitalCourse:
    """Mock hospital course data for testing."""

    def __init__(self, course_text="The patient was admitted on 03/15/2024."):
        self._course_text = course_text

    @property
    def course_text(self):
        return self._course_text


class TestHospitalCourseSection:
    """Tests for HospitalCourseSection builder."""

    def test_section_basic(self):
        """Test basic HospitalCourseSection creation."""
        section = HospitalCourseSection(
            narrative_text="The patient was admitted with pneumonia."
        )
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:81-7852, CONF:81-10459)."""
        section = HospitalCourseSection(
            narrative_text="Test", version=CDAVersion.R2_1
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "1.3.6.1.4.1.19376.1.5.3.1.3.5"
        # No extension in spec
        assert template.get("extension") is None

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        section = HospitalCourseSection(
            narrative_text="Test", version=CDAVersion.R2_0
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "1.3.6.1.4.1.19376.1.5.3.1.3.5"
        assert template.get("extension") is None

    def test_section_has_code(self):
        """Test section includes correct code (CONF:81-15487, CONF:81-15488, CONF:81-26480)."""
        section = HospitalCourseSection(narrative_text="Test")
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "8648-8"  # Hospital Course
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Hospital Course"

    def test_section_has_title(self):
        """Test section includes title (CONF:81-7854)."""
        section = HospitalCourseSection(
            narrative_text="Test", title="Hospital Course - ICU Stay"
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Hospital Course - ICU Stay"

    def test_section_default_title(self):
        """Test section uses default title."""
        section = HospitalCourseSection(narrative_text="Test")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Hospital Course"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:81-7855)."""
        section = HospitalCourseSection(narrative_text="Test")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_simple_text(self):
        """Test narrative with simple text."""
        narrative = (
            "The patient was admitted through the Emergency Department on 03/15/2024 "
            "with acute exacerbation of COPD."
        )
        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == narrative

    def test_narrative_with_protocol_object(self):
        """Test narrative using HospitalCourseProtocol object."""
        course = MockHospitalCourse(
            course_text="The patient was admitted on 03/15/2024 with acute MI."
        )
        section = HospitalCourseSection(hospital_course=course)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "The patient was admitted on 03/15/2024 with acute MI."

    def test_narrative_text_takes_precedence(self):
        """Test that narrative_text parameter takes precedence over protocol object."""
        course = MockHospitalCourse(
            course_text="This should not appear"
        )
        section = HospitalCourseSection(
            hospital_course=course,
            narrative_text="This should appear"
        )
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "This should appear"

    def test_narrative_empty_default_message(self):
        """Test narrative shows default message when no content provided."""
        section = HospitalCourseSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No hospital course information provided."

    def test_narrative_with_multiple_paragraphs(self):
        """Test narrative with multiple paragraphs separated by double line breaks."""
        narrative = (
            "The patient was admitted on 03/15/2024 with acute exacerbation of COPD.\n\n"
            "Initial treatment included supplemental oxygen and nebulizer treatments.\n\n"
            "By hospital day 2, the patient showed improvement with decreased work of breathing."
        )
        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")

        assert len(paragraphs) == 3
        assert "admitted on 03/15/2024" in paragraphs[0].text
        assert "Initial treatment" in paragraphs[1].text
        assert "hospital day 2" in paragraphs[2].text

    def test_narrative_with_single_newlines_ignored(self):
        """Test that single newlines don't create multiple paragraphs."""
        narrative = (
            "The patient was admitted on 03/15/2024\n"
            "with acute exacerbation of COPD."
        )
        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")

        # Should be one paragraph despite single newline
        assert len(paragraphs) == 1

    def test_section_no_entries(self):
        """Test section does not contain entry elements."""
        section = HospitalCourseSection(
            narrative_text="The patient was admitted."
        )
        elem = section.to_element()

        # Should not have any entries (this section is narrative-only)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        section = HospitalCourseSection(narrative_text="Test course")
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

    def test_section_to_string(self):
        """Test section serialization."""
        section = HospitalCourseSection(
            narrative_text="The patient was admitted."
        )
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "8648-8" in xml  # Section code
        assert "Hospital Course" in xml

    def test_long_narrative_text(self):
        """Test section with long narrative text."""
        long_text = (
            "The patient was admitted through the Emergency Department on 03/15/2024 "
            "with acute exacerbation of COPD. Initial vital signs showed respiratory "
            "distress with oxygen saturation of 88% on room air. Treatment was initiated "
            "with supplemental oxygen via nasal cannula at 3L/min, nebulizer treatments "
            "with albuterol and ipratropium every 4 hours, and IV methylprednisolone 125mg. "
            "Chest X-ray showed hyperinflation without acute infiltrate. Arterial blood gas "
            "revealed respiratory acidosis with pH 7.32, pCO2 55, pO2 65.\n\n"
            "By hospital day 2, the patient demonstrated clinical improvement with decreased "
            "work of breathing and improved oxygen saturation to 94% on 2L nasal cannula. "
            "Nebulizer treatments were spaced to every 6 hours and corticosteroids were "
            "transitioned to oral prednisone 40mg daily. Pulmonary consultation was obtained "
            "and recommended continuing current management with addition of azithromycin "
            "for possible infectious component.\n\n"
            "On hospital day 3, the patient continued to improve and was weaned to room air "
            "with oxygen saturations 92-94%. Discharge planning was initiated with patient "
            "education on inhaler technique, smoking cessation resources, and pulmonary "
            "rehabilitation referral. The patient was discharged home in stable condition "
            "on hospital day 4 with prescriptions and follow-up appointments scheduled."
        )
        section = HospitalCourseSection(narrative_text=long_text)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")

        # Should have 3 paragraphs
        assert len(paragraphs) == 3
        assert "admitted through the Emergency Department" in paragraphs[0].text
        assert "hospital day 2" in paragraphs[1].text
        assert "hospital day 3" in paragraphs[2].text

    def test_special_characters_in_text(self):
        """Test section handles special characters in text."""
        narrative = "Temperature > 101°F with O2 saturation < 88% noted."
        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        # Special characters should be preserved
        assert ">" in paragraph.text
        assert "<" in paragraph.text
        assert "°" in paragraph.text

    def test_empty_paragraphs_removed(self):
        """Test that empty paragraphs from multiple newlines are removed."""
        narrative = (
            "First paragraph with content.\n\n"
            "\n\n"  # Extra blank lines
            "Second paragraph with content."
        )
        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")

        # Should only have 2 paragraphs (empty ones removed)
        assert len(paragraphs) == 2
        assert "First paragraph" in paragraphs[0].text
        assert "Second paragraph" in paragraphs[1].text


class TestHospitalCourseSectionIntegration:
    """Integration tests for HospitalCourseSection."""

    def test_complete_section_with_detailed_course(self):
        """Test creating a complete hospital course section with detailed narrative."""
        narrative = (
            "The patient, a 65-year-old male with history of coronary artery disease and "
            "hypertension, was admitted to the hospital on 03/15/2024 via the Emergency "
            "Department with chief complaint of chest pain. Initial EKG showed ST-segment "
            "elevations in leads V2-V4 consistent with anterior STEMI. The patient was "
            "taken emergently to the cardiac catheterization laboratory where he underwent "
            "successful percutaneous coronary intervention with drug-eluting stent placement "
            "to the proximal left anterior descending artery. Door-to-balloon time was 45 minutes.\n\n"
            "Post-procedure, the patient was transferred to the Cardiac Care Unit for "
            "monitoring. He was started on dual antiplatelet therapy, high-intensity statin, "
            "ACE inhibitor, and beta-blocker. Serial cardiac enzymes showed peak troponin of "
            "25.6 ng/mL at 12 hours post-admission. Transthoracic echocardiogram on hospital "
            "day 2 revealed anterior wall hypokinesis with ejection fraction estimated at 45%. "
            "The patient remained hemodynamically stable without recurrent chest pain or "
            "arrhythmias.\n\n"
            "By hospital day 3, the patient was transferred to the telemetry floor and began "
            "cardiac rehabilitation with physical therapy. He ambulated in the hallways without "
            "difficulty and demonstrated proper understanding of medication regimen. Cardiology "
            "consultation recommended continuing current medical therapy with outpatient follow-up "
            "in 1 week. Discharge planning was completed with arrangements for cardiac rehabilitation "
            "program enrollment and smoking cessation counseling. The patient was discharged home "
            "in stable condition on hospital day 4 with prescriptions and follow-up appointments "
            "scheduled with both primary care physician and cardiologist."
        )

        section = HospitalCourseSection(
            narrative_text=narrative,
            title="Hospital Course - Cardiac Care",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Verify narrative content is structured into multiple paragraphs
        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert len(paragraphs) == 3

        # Verify content of each paragraph
        assert "admitted to the hospital" in paragraphs[0].text
        assert "Post-procedure" in paragraphs[1].text
        assert "hospital day 3" in paragraphs[2].text

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        section = HospitalCourseSection(
            narrative_text="The patient was admitted with pneumonia."
        )

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_r20_version(self):
        """Test section with R2.0 version."""
        section = HospitalCourseSection(
            narrative_text="Test", version=CDAVersion.R2_0
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "1.3.6.1.4.1.19376.1.5.3.1.3.5"
        assert template.get("extension") is None

    def test_section_r21_version(self):
        """Test section with R2.1 version."""
        section = HospitalCourseSection(
            narrative_text="Test", version=CDAVersion.R2_1
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "1.3.6.1.4.1.19376.1.5.3.1.3.5"
        assert template.get("extension") is None

    def test_realistic_surgical_course(self):
        """Test with realistic surgical hospital course content."""
        narrative = (
            "The patient, a 58-year-old female, was admitted on 03/20/2024 for elective "
            "laparoscopic cholecystectomy for symptomatic cholelithiasis. The patient had "
            "been experiencing recurrent episodes of right upper quadrant pain over the past "
            "3 months. Preoperative workup included ultrasound confirming multiple gallstones "
            "and normal liver function tests. The patient was taken to the operating room on "
            "the day of admission where she underwent uncomplicated laparoscopic cholecystectomy. "
            "Operative time was 75 minutes with minimal blood loss. The patient tolerated the "
            "procedure well and was transferred to the post-anesthesia care unit in stable condition.\n\n"
            "Postoperatively, the patient was managed with IV fluids and pain control with "
            "hydromorphone PCA. She was started on clear liquids on postoperative day 1 and "
            "advanced to regular diet as tolerated. Pain was well-controlled with transition to "
            "oral pain medications. The surgical incisions appeared clean, dry, and intact without "
            "signs of infection. The patient ambulated independently without difficulty.\n\n"
            "On postoperative day 2, the patient met all discharge criteria including adequate "
            "pain control on oral medications, tolerance of regular diet, and independent ambulation. "
            "Discharge instructions were reviewed including wound care, activity restrictions, and "
            "warning signs. The patient was discharged home in stable condition with prescription "
            "for oral pain medication and scheduled follow-up with the surgeon in 2 weeks."
        )

        section = HospitalCourseSection(
            narrative_text=narrative,
            title="Hospital Course",
        )

        elem = section.to_element()

        # Verify it builds successfully
        assert local_name(elem) == "section"

        # Verify it has multiple paragraphs
        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert len(paragraphs) == 3

        # Verify it can be serialized
        xml = section.to_string(pretty=True)
        assert "cholecystectomy" in xml

    def test_realistic_medical_course(self):
        """Test with realistic medical hospital course content."""
        narrative = (
            "The patient is a 72-year-old male with history of diabetes mellitus type 2, "
            "hypertension, and hyperlipidemia who presented to the Emergency Department on "
            "04/01/2024 with altered mental status and fever to 103.2°F. Initial workup "
            "revealed white blood cell count of 18,000, urinalysis with pyuria and bacteriuria, "
            "and chest X-ray without infiltrate. The patient was admitted with diagnosis of "
            "urosepsis and acute encephalopathy. Empiric antibiotic therapy was initiated with "
            "ceftriaxone and IV fluids were administered. Blood and urine cultures were obtained.\n\n"
            "Over the first 48 hours, the patient showed gradual improvement in mental status "
            "and defervescence of fever. Blood cultures returned positive for E. coli sensitive "
            "to ceftriaxone, and antibiotic therapy was continued. By hospital day 3, the patient "
            "was alert and oriented to person, place, and time with return to baseline cognitive "
            "function. Vital signs remained stable without fever. Repeat urinalysis showed "
            "improvement in pyuria.\n\n"
            "The patient continued to improve clinically and was transitioned to oral ciprofloxacin "
            "on hospital day 5. Home medications were resumed with adjustments to diabetic regimen "
            "due to hyperglycemia during acute illness. Endocrinology consultation recommended "
            "uptitration of long-acting insulin. The patient was discharged home on hospital day 6 "
            "in stable condition with 10-day course of oral antibiotics, modified insulin regimen, "
            "and follow-up appointments scheduled with primary care physician and endocrinology."
        )

        section = HospitalCourseSection(
            hospital_course=MockHospitalCourse(course_text=narrative),
            title="Hospital Course - Medical Service",
        )

        elem = section.to_element()

        # Verify it builds successfully
        assert local_name(elem) == "section"

        # Verify content
        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert len(paragraphs) == 3
        assert "urosepsis" in paragraphs[0].text

        # Verify it can be serialized
        xml = section.to_string(pretty=True)
        assert "Medical Service" in xml

    def test_section_with_simple_course(self):
        """Test section with simple, brief hospital course."""
        narrative = (
            "The patient was admitted for observation following a syncopal episode. "
            "Telemetry monitoring showed no arrhythmias. Orthostatic vital signs were negative. "
            "Echocardiogram was normal. The patient remained stable and was discharged home "
            "on hospital day 2 with cardiology follow-up."
        )

        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        # Should have single paragraph since no double line breaks
        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert len(paragraphs) == 1
        assert "syncopal episode" in paragraphs[0].text

    def test_section_with_protocol_object_detailed(self):
        """Test section using protocol object with detailed narrative."""
        course_text = (
            "The patient was admitted to the ICU with severe sepsis secondary to pneumonia. "
            "Initial management included mechanical ventilation, broad-spectrum antibiotics, "
            "and vasopressor support with norepinephrine.\n\n"
            "By hospital day 4, the patient showed improvement with successful liberation "
            "from mechanical ventilation. Vasopressor support was weaned off and the patient "
            "was transferred to the medical floor.\n\n"
            "The patient completed a 7-day course of antibiotics and was discharged home in "
            "stable condition on hospital day 8."
        )

        course = MockHospitalCourse(course_text=course_text)
        section = HospitalCourseSection(hospital_course=course)
        elem = section.to_element()

        # Verify structure
        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert len(paragraphs) == 3
        assert "ICU" in paragraphs[0].text
        assert "hospital day 4" in paragraphs[1].text
        assert "hospital day 8" in paragraphs[2].text

    def test_whitespace_handling(self):
        """Test proper handling of whitespace in narrative text."""
        narrative = (
            "   The patient was admitted.   \n\n"
            "   Treatment was initiated.   \n\n"
            "   The patient was discharged.   "
        )
        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")

        # Should strip whitespace from each paragraph
        assert len(paragraphs) == 3
        assert paragraphs[0].text == "The patient was admitted."
        assert paragraphs[1].text == "Treatment was initiated."
        assert paragraphs[2].text == "The patient was discharged."

    def test_section_with_numeric_data(self):
        """Test section with narrative containing numeric clinical data."""
        narrative = (
            "The patient was admitted with acute myocardial infarction. Initial troponin was "
            "0.15 ng/mL, rising to peak of 25.6 ng/mL at 12 hours. EKG showed ST elevations "
            "of 3mm in leads V2-V4. Blood pressure on admission was 145/92 mmHg. Heart rate "
            "was 98 bpm. Oxygen saturation was 94% on room air."
        )
        section = HospitalCourseSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")

        # Verify numeric data is preserved
        assert "0.15 ng/mL" in paragraph.text
        assert "25.6 ng/mL" in paragraph.text
        assert "3mm" in paragraph.text
        assert "145/92 mmHg" in paragraph.text
        assert "98 bpm" in paragraph.text
        assert "94%" in paragraph.text
