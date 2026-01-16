"""Tests for AllergiesSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockAllergy:
    """Mock allergy for testing."""

    def __init__(
        self,
        allergen="Penicillin",
        allergen_code="70618",
        allergen_code_system="RxNorm",
        allergy_type="allergy",
        reaction="Hives",
        severity="moderate",
        status="active",
        onset_date=date(2020, 5, 15),
    ):
        self._allergen = allergen
        self._allergen_code = allergen_code
        self._allergen_code_system = allergen_code_system
        self._allergy_type = allergy_type
        self._reaction = reaction
        self._severity = severity
        self._status = status
        self._onset_date = onset_date

    @property
    def allergen(self):
        return self._allergen

    @property
    def allergen_code(self):
        return self._allergen_code

    @property
    def allergen_code_system(self):
        return self._allergen_code_system

    @property
    def allergy_type(self):
        return self._allergy_type

    @property
    def reaction(self):
        return self._reaction

    @property
    def severity(self):
        return self._severity

    @property
    def status(self):
        return self._status

    @property
    def onset_date(self):
        return self._onset_date


class TestAllergiesSection:
    """Tests for AllergiesSection builder."""

    def test_allergies_section_basic(self):
        """Test basic AllergiesSection creation."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_allergies_section_has_template_id_r21(self):
        """Test AllergiesSection includes R2.1 template IDs.

        Per C-CDA spec, the section includes both:
        - Base template (entries optional): 2.16.840.1.113883.10.20.22.2.6
        - Entries required template: 2.16.840.1.113883.10.20.22.2.6.1
        """
        allergy = MockAllergy()
        section = AllergiesSection([allergy], version=CDAVersion.R2_1)
        elem = section.to_element()

        templates = elem.findall(f"{{{NS}}}templateId")
        assert len(templates) == 2

        # Check both template IDs are present
        template_roots = [t.get("root") for t in templates]
        assert "2.16.840.1.113883.10.20.22.2.6" in template_roots
        assert "2.16.840.1.113883.10.20.22.2.6.1" in template_roots

        # Both should have R2.1 extension
        for template in templates:
            assert template.get("extension") == "2015-08-01"

    def test_allergies_section_has_template_id_r20(self):
        """Test AllergiesSection includes R2.0 template IDs.

        Per C-CDA spec, the section includes both:
        - Base template (entries optional): 2.16.840.1.113883.10.20.22.2.6
        - Entries required template: 2.16.840.1.113883.10.20.22.2.6.1
        """
        allergy = MockAllergy()
        section = AllergiesSection([allergy], version=CDAVersion.R2_0)
        elem = section.to_element()

        templates = elem.findall(f"{{{NS}}}templateId")
        assert len(templates) == 2

        # Check both template IDs are present
        template_roots = [t.get("root") for t in templates]
        assert "2.16.840.1.113883.10.20.22.2.6" in template_roots
        assert "2.16.840.1.113883.10.20.22.2.6.1" in template_roots

        # Both should have the same extension for R2.0
        for template in templates:
            assert template.get("extension") == "2015-08-01"

    def test_allergies_section_has_code(self):
        """Test AllergiesSection includes section code."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "48765-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Allergies and adverse reactions Document"

    def test_allergies_section_has_title(self):
        """Test AllergiesSection includes title."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy], title="My Allergies")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Allergies"

    def test_allergies_section_default_title(self):
        """Test AllergiesSection uses default title."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Allergies and Intolerances"

    def test_allergies_section_has_narrative(self):
        """Test AllergiesSection includes narrative text."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_allergies_section_narrative_table(self):
        """Test narrative includes HTML table."""
        allergy = MockAllergy(
            allergen="Penicillin",
            allergy_type="allergy",
            reaction="Hives",
            severity="moderate",
            status="active",
            onset_date=date(2020, 5, 15),
        )
        section = AllergiesSection([allergy])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"

        # Check table header
        thead = table.find(f"{{{NS}}}thead")
        assert thead is not None
        tr = thead.find(f"{{{NS}}}tr")
        ths = tr.findall(f"{{{NS}}}th")
        assert len(ths) == 6  # Allergen, Type, Reaction, Severity, Status, Onset Date

    def test_allergies_section_narrative_content(self):
        """Test narrative contains allergy data."""
        allergy = MockAllergy(
            allergen="Peanuts",
            allergy_type="allergy",
            reaction="Anaphylaxis",
            severity="severe",
            status="active",
            onset_date=date(2015, 3, 10),
        )
        section = AllergiesSection([allergy])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 6

        # Check allergen name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Peanuts"
        assert content.get("ID") == "allergy-1"

        # Check type
        assert tds[1].text == "Allergy"

        # Check reaction
        assert tds[2].text == "Anaphylaxis"

        # Check severity
        assert tds[3].text == "Severe"

        # Check status
        assert tds[4].text == "Active"

        # Check onset date
        assert tds[5].text == "2015-03-10"

    def test_allergies_section_narrative_without_reaction(self):
        """Test narrative shows 'Not specified' for missing reaction."""
        allergy = MockAllergy(reaction=None)
        section = AllergiesSection([allergy])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check reaction shows "Not specified"
        assert tds[2].text == "Not specified"

    def test_allergies_section_narrative_without_severity(self):
        """Test narrative shows 'Not specified' for missing severity."""
        allergy = MockAllergy(severity=None)
        section = AllergiesSection([allergy])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check severity shows "Not specified"
        assert tds[3].text == "Not specified"

    def test_allergies_section_narrative_without_onset_date(self):
        """Test narrative shows 'Unknown' for missing onset date."""
        allergy = MockAllergy(onset_date=None)
        section = AllergiesSection([allergy])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check onset date shows "Unknown"
        assert tds[5].text == "Unknown"

    def test_allergies_section_narrative_multiple_allergies(self):
        """Test narrative with multiple allergies."""
        allergies = [
            MockAllergy(allergen="Penicillin", allergen_code="70618"),
            MockAllergy(allergen="Peanuts", allergen_code="762952008"),
            MockAllergy(allergen="Latex", allergen_code="111088007"),
        ]
        section = AllergiesSection(allergies)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 3

        # Check IDs are sequential
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")
        content3 = trs[2].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "allergy-1"
        assert content2.get("ID") == "allergy-2"
        assert content3.get("ID") == "allergy-3"

    def test_allergies_section_narrative_resolved_allergy(self):
        """Test narrative shows resolved status correctly."""
        allergy = MockAllergy(
            allergen="Shellfish",
            status="resolved",
            onset_date=date(2010, 1, 1),
        )
        section = AllergiesSection([allergy])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[4].text == "Resolved"

    def test_allergies_section_empty_narrative(self):
        """Test narrative when no allergies."""
        section = AllergiesSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No known allergies"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_allergies_section_has_entries(self):
        """Test AllergiesSection includes entry elements."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_allergies_section_entry_has_concern_act(self):
        """Test entry contains Allergy Concern Act element."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

        # Check template ID
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.30"

    def test_allergies_section_entry_has_observation(self):
        """Test entry contains allergy observation."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

        observation = entry_rel.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"

    def test_allergies_section_concern_act_active_status(self):
        """Test Allergy Concern Act has active status for active allergies."""
        allergy = MockAllergy(status="active")
        section = AllergiesSection([allergy])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "active"

    def test_allergies_section_concern_act_completed_status(self):
        """Test Allergy Concern Act has completed status for resolved allergies."""
        allergy = MockAllergy(status="resolved")
        section = AllergiesSection([allergy])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_allergies_section_concern_act_effective_time(self):
        """Test Allergy Concern Act includes effectiveTime."""
        allergy = MockAllergy(
            onset_date=date(2020, 5, 15),
            status="active",
        )
        section = AllergiesSection([allergy])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20200515"

    def test_allergies_section_multiple_entries(self):
        """Test AllergiesSection with multiple allergies."""
        allergies = [
            MockAllergy(allergen="Penicillin", allergen_code="70618"),
            MockAllergy(allergen="Peanuts", allergen_code="762952008"),
        ]
        section = AllergiesSection(allergies)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an act
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None

    def test_allergies_section_to_string(self):
        """Test AllergiesSection serialization."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "48765-2" in xml  # Section code
        assert "Allergi" in xml  # Should contain "Allergies" or "Allergen"

    def test_allergies_section_structure_order(self):
        """Test that section elements are in correct order."""
        allergy = MockAllergy()
        section = AllergiesSection([allergy])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        # templateId should come before code
        assert names.index("templateId") < names.index("code")
        # code should come before title
        assert names.index("code") < names.index("title")
        # title should come before text
        assert names.index("title") < names.index("text")
        # text should come before entry
        assert names.index("text") < names.index("entry")


class TestAllergiesSectionIntegration:
    """Integration tests for AllergiesSection."""

    def test_complete_allergies_section(self):
        """Test creating a complete allergies section."""
        allergies = [
            MockAllergy(
                allergen="Penicillin",
                allergen_code="70618",
                allergen_code_system="RxNorm",
                allergy_type="allergy",
                reaction="Hives",
                severity="moderate",
                status="active",
                onset_date=date(2015, 3, 10),
            ),
            MockAllergy(
                allergen="Peanuts",
                allergen_code="762952008",
                allergen_code_system="SNOMED CT",
                allergy_type="allergy",
                reaction="Anaphylaxis",
                severity="severe",
                status="active",
                onset_date=date(2010, 8, 22),
            ),
            MockAllergy(
                allergen="Latex",
                allergen_code="111088007",
                allergen_code_system="SNOMED CT",
                allergy_type="allergy",
                reaction="Contact dermatitis",
                severity="mild",
                status="active",
                onset_date=date(2018, 11, 5),
            ),
        ]

        section = AllergiesSection(allergies, title="Known Allergies")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 3 entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        allergy = MockAllergy()
        section = AllergiesSection([allergy])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None
