"""Tests for SocialHistorySection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockSmokingStatus:
    """Mock smoking status for testing."""

    def __init__(
        self,
        smoking_status="Current every day smoker",
        code="449868002",
        date=date(2023, 10, 1),
    ):
        self._smoking_status = smoking_status
        self._code = code
        self._date = date

    @property
    def smoking_status(self):
        return self._smoking_status

    @property
    def code(self):
        return self._code

    @property
    def date(self):
        return self._date


class TestSocialHistorySection:
    """Tests for SocialHistorySection builder."""

    def test_social_history_section_basic(self):
        """Test basic SocialHistorySection creation."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_social_history_section_has_template_id_r21(self):
        """Test SocialHistorySection includes R2.1 template ID."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses, version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.17"
        assert template.get("extension") == "2015-08-01"

    def test_social_history_section_has_template_id_r20(self):
        """Test SocialHistorySection includes R2.0 template ID."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses, version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.17"
        assert template.get("extension") == "2015-08-01"

    def test_social_history_section_has_code(self):
        """Test SocialHistorySection includes section code."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "29762-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Social History"

    def test_social_history_section_has_title(self):
        """Test SocialHistorySection includes title."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses, title="Patient Social History")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Social History"

    def test_social_history_section_default_title(self):
        """Test SocialHistorySection uses default title."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Social History"

    def test_social_history_section_has_narrative(self):
        """Test SocialHistorySection includes narrative text."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_social_history_section_narrative_table(self):
        """Test narrative includes HTML table."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
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
        assert len(ths) == 3  # Social History Type, Status, Date Observed

    def test_social_history_section_narrative_content(self):
        """Test narrative contains smoking status data."""
        statuses = [
            MockSmokingStatus(
                smoking_status="Current every day smoker",
                code="449868002",
                date=date(2023, 10, 15),
            )
        ]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 3

        # Check social history type
        assert tds[0].text == "Smoking Status"

        # Check smoking status with ID
        content = tds[1].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Current every day smoker"
        assert content.get("ID") == "smoking-status-1"

        # Check date observed
        assert tds[2].text == "2023-10-15"

    def test_social_history_section_narrative_content_with_datetime(self):
        """Test narrative shows date with time when datetime provided."""
        statuses = [
            MockSmokingStatus(
                smoking_status="Never smoker",
                code="266919005",
                date=datetime(2023, 10, 15, 14, 30),
            )
        ]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check date shows time
        assert tds[2].text == "2023-10-15 14:30"

    def test_social_history_section_narrative_multiple_statuses(self):
        """Test narrative with multiple smoking statuses."""
        statuses = [
            MockSmokingStatus(
                smoking_status="Current every day smoker",
                code="449868002",
                date=date(2023, 10, 1),
            ),
            MockSmokingStatus(
                smoking_status="Former smoker",
                code="8517006",
                date=date(2023, 10, 15),
            ),
            MockSmokingStatus(
                smoking_status="Never smoker",
                code="266919005",
                date=date(2023, 10, 20),
            ),
        ]
        section = SocialHistorySection(statuses)
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

        assert content1.get("ID") == "smoking-status-1"
        assert content2.get("ID") == "smoking-status-2"
        assert content3.get("ID") == "smoking-status-3"

        # Check status display names
        assert content1.text == "Current every day smoker"
        assert content2.text == "Former smoker"
        assert content3.text == "Never smoker"

    def test_social_history_section_empty_narrative(self):
        """Test narrative when no smoking statuses."""
        section = SocialHistorySection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No social history information available"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_social_history_section_has_entries(self):
        """Test SocialHistorySection includes entry elements."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_social_history_section_entry_has_observation(self):
        """Test entry contains observation element."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        assert obs is not None
        assert obs.get("classCode") == "OBS"
        assert obs.get("moodCode") == "EVN"

    def test_social_history_section_multiple_entries(self):
        """Test SocialHistorySection with multiple statuses."""
        statuses = [
            MockSmokingStatus(),
            MockSmokingStatus(smoking_status="Former smoker", code="8517006"),
        ]
        section = SocialHistorySection(statuses)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an observation
        for entry in entries:
            obs = entry.find(f"{{{NS}}}observation")
            assert obs is not None

    def test_social_history_section_to_string(self):
        """Test SocialHistorySection serialization."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "29762-2" in xml  # Section code
        assert "Social" in xml

    def test_social_history_section_structure_order(self):
        """Test that section elements are in correct order."""
        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)
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


class TestSocialHistorySectionIntegration:
    """Integration tests for SocialHistorySection."""

    def test_complete_social_history_section(self):
        """Test creating a complete social history section."""
        statuses = [
            MockSmokingStatus(
                smoking_status="Current every day smoker",
                code="449868002",
                date=date(2023, 10, 1),
            ),
            MockSmokingStatus(
                smoking_status="Former smoker",
                code="8517006",
                date=date(2023, 9, 15),
            ),
        ]

        section = SocialHistorySection(statuses, title="Patient Social History")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 2 rows (one per status)
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 2

        # Verify 2 entries (2 observations)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify each entry has correct structure
        for entry in entries:
            obs = entry.find(f"{{{NS}}}observation")
            assert obs is not None
            assert obs.get("classCode") == "OBS"
            assert obs.get("moodCode") == "EVN"

            # Verify observation has required elements
            assert obs.find(f"{{{NS}}}templateId") is not None
            assert obs.find(f"{{{NS}}}id") is not None
            assert obs.find(f"{{{NS}}}code") is not None
            assert obs.find(f"{{{NS}}}statusCode") is not None
            assert obs.find(f"{{{NS}}}effectiveTime") is not None
            assert obs.find(f"{{{NS}}}value") is not None

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        statuses = [MockSmokingStatus()]
        section = SocialHistorySection(statuses)

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_smoking_statuses(self):
        """Test section with all common smoking status types."""
        statuses = [
            MockSmokingStatus(
                smoking_status="Current every day smoker",
                code="449868002",
                date=date(2023, 10, 1),
            ),
            MockSmokingStatus(
                smoking_status="Current some day smoker",
                code="428041000124106",
                date=date(2023, 9, 15),
            ),
            MockSmokingStatus(
                smoking_status="Former smoker",
                code="8517006",
                date=date(2023, 8, 1),
            ),
            MockSmokingStatus(
                smoking_status="Never smoker",
                code="266919005",
                date=date(2023, 7, 1),
            ),
            MockSmokingStatus(
                smoking_status="Unknown if ever smoked",
                code="266927001",
                date=date(2023, 6, 1),
            ),
        ]

        section = SocialHistorySection(statuses, version=CDAVersion.R2_1)
        elem = section.to_element()

        # Verify all 5 statuses are in narrative
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 5

        # Verify all 5 statuses are in entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 5

        # Verify all value codes are present
        observations = [entry.find(f"{{{NS}}}observation") for entry in entries]
        values = [obs.find(f"{{{NS}}}value") for obs in observations]
        codes = [val.get("code") for val in values]

        assert "449868002" in codes  # Current every day smoker
        assert "428041000124106" in codes  # Current some day smoker
        assert "8517006" in codes  # Former smoker
        assert "266919005" in codes  # Never smoker
        assert "266927001" in codes  # Unknown if ever smoked
