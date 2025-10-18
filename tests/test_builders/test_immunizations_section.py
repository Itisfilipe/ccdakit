"""Tests for ImmunizationsSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockImmunization:
    """Mock immunization for testing."""

    def __init__(
        self,
        vaccine_name="Influenza vaccine",
        cvx_code="141",
        administration_date=date(2023, 9, 1),
        status="completed",
        lot_number=None,
        manufacturer=None,
        route=None,
        site=None,
        dose_quantity=None,
    ):
        self._vaccine_name = vaccine_name
        self._cvx_code = cvx_code
        self._administration_date = administration_date
        self._status = status
        self._lot_number = lot_number
        self._manufacturer = manufacturer
        self._route = route
        self._site = site
        self._dose_quantity = dose_quantity

    @property
    def vaccine_name(self):
        return self._vaccine_name

    @property
    def cvx_code(self):
        return self._cvx_code

    @property
    def administration_date(self):
        return self._administration_date

    @property
    def status(self):
        return self._status

    @property
    def lot_number(self):
        return self._lot_number

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def route(self):
        return self._route

    @property
    def site(self):
        return self._site

    @property
    def dose_quantity(self):
        return self._dose_quantity


class TestImmunizationsSection:
    """Tests for ImmunizationsSection builder."""

    def test_immunizations_section_basic(self):
        """Test basic ImmunizationsSection creation."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_immunizations_section_has_template_id_r21(self):
        """Test ImmunizationsSection includes R2.1 template ID."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.2.1"
        assert template.get("extension") == "2015-08-01"

    def test_immunizations_section_has_template_id_r20(self):
        """Test ImmunizationsSection includes R2.0 template ID."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.2.1"
        assert template.get("extension") == "2014-06-09"

    def test_immunizations_section_has_code(self):
        """Test ImmunizationsSection includes section code."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "11369-6"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "History of Immunization Narrative"

    def test_immunizations_section_has_title(self):
        """Test ImmunizationsSection includes title."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization], title="My Immunizations")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Immunizations"

    def test_immunizations_section_default_title(self):
        """Test ImmunizationsSection uses default title."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Immunizations"

    def test_immunizations_section_has_narrative(self):
        """Test ImmunizationsSection includes narrative text."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_immunizations_section_narrative_table(self):
        """Test narrative includes HTML table."""
        immunization = MockImmunization(
            vaccine_name="Influenza vaccine",
            administration_date=date(2023, 9, 1),
        )
        section = ImmunizationsSection([immunization])
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
        assert len(ths) == 5  # Vaccine, Date, Status, Lot Number, Manufacturer

    def test_immunizations_section_narrative_content(self):
        """Test narrative contains immunization data."""
        immunization = MockImmunization(
            vaccine_name="COVID-19 vaccine",
            cvx_code="208",
            administration_date=date(2023, 6, 15),
            status="completed",
            lot_number="ABC123",
            manufacturer="Pfizer Inc.",
        )
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 5

        # Check vaccine name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "COVID-19 vaccine"
        assert content.get("ID") == "immunization-1"

        # Check administration date
        assert tds[1].text == "2023-06-15"

        # Check status
        assert tds[2].text == "Completed"

        # Check lot number
        assert tds[3].text == "ABC123"

        # Check manufacturer
        assert tds[4].text == "Pfizer Inc."

    def test_immunizations_section_narrative_without_lot_number(self):
        """Test narrative shows 'Not recorded' when lot number missing."""
        immunization = MockImmunization(lot_number=None)
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check lot number shows "Not recorded"
        assert tds[3].text == "Not recorded"

    def test_immunizations_section_narrative_without_manufacturer(self):
        """Test narrative shows 'Not recorded' when manufacturer missing."""
        immunization = MockImmunization(manufacturer=None)
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check manufacturer shows "Not recorded"
        assert tds[4].text == "Not recorded"

    def test_immunizations_section_narrative_multiple_immunizations(self):
        """Test narrative with multiple immunizations."""
        immunizations = [
            MockImmunization(vaccine_name="Influenza vaccine", cvx_code="141"),
            MockImmunization(vaccine_name="COVID-19 vaccine", cvx_code="208"),
            MockImmunization(vaccine_name="Tetanus vaccine", cvx_code="35"),
        ]
        section = ImmunizationsSection(immunizations)
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

        assert content1.get("ID") == "immunization-1"
        assert content2.get("ID") == "immunization-2"
        assert content3.get("ID") == "immunization-3"

    def test_immunizations_section_empty_narrative(self):
        """Test narrative when no immunizations."""
        section = ImmunizationsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No known immunizations"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_immunizations_section_has_entries(self):
        """Test ImmunizationsSection includes entry elements."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_immunizations_section_entry_has_substance_administration(self):
        """Test entry contains substanceAdministration element."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"

    def test_immunizations_section_multiple_entries(self):
        """Test ImmunizationsSection with multiple immunizations."""
        immunizations = [
            MockImmunization(vaccine_name="Influenza vaccine", cvx_code="141"),
            MockImmunization(vaccine_name="COVID-19 vaccine", cvx_code="208"),
        ]
        section = ImmunizationsSection(immunizations)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has a substanceAdministration
        for entry in entries:
            sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
            assert sub_admin is not None

    def test_immunizations_section_to_string(self):
        """Test ImmunizationsSection serialization."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "11369-6" in xml  # Section code
        assert "Immunization" in xml

    def test_immunizations_section_structure_order(self):
        """Test that section elements are in correct order."""
        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])
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


class TestImmunizationsSectionIntegration:
    """Integration tests for ImmunizationsSection."""

    def test_complete_immunizations_section(self):
        """Test creating a complete immunizations section."""
        immunizations = [
            MockImmunization(
                vaccine_name="Influenza vaccine, seasonal",
                cvx_code="141",
                administration_date=date(2023, 9, 15),
                status="completed",
                lot_number="ABC123",
                manufacturer="Sanofi Pasteur",
            ),
            MockImmunization(
                vaccine_name="COVID-19 vaccine",
                cvx_code="208",
                administration_date=date(2023, 6, 1),
                status="completed",
                lot_number="XYZ789",
                manufacturer="Pfizer Inc.",
            ),
            MockImmunization(
                vaccine_name="Tetanus and diphtheria toxoids",
                cvx_code="139",
                administration_date=date(2022, 3, 10),
                status="completed",
            ),
        ]

        section = ImmunizationsSection(immunizations, title="Immunization History")
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

        immunization = MockImmunization()
        section = ImmunizationsSection([immunization])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None
