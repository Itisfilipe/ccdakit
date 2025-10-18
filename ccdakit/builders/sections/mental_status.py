"""Mental Status Section builder for C-CDA documents."""

from typing import Sequence
from lxml import etree

from ccdakit.builders.common import Code, StatusCode
from ccdakit.builders.entries.mental_status import (
    MentalStatusObservation,
    MentalStatusOrganizer,
)
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.mental_status import (
    MentalStatusObservationProtocol,
    MentalStatusOrganizerProtocol,
)


# CDA namespace
NS = "urn:hl7-org:v3"


class MentalStatusSection(CDAElement):
    """
    Builder for C-CDA Mental Status Section (V2).

    Contains observations and evaluations related to a patient's psychological
    and mental competency including appearance, attitude, behavior, mood and affect,
    speech and language, thought process, thought content, perception, cognition,
    insight and judgment.

    Template ID: 2.16.840.1.113883.10.20.22.2.56
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Includes narrative (HTML table) and structured entries.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.56",
                extension="2015-08-01",
                description="Mental Status Section (V2) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.56",
                extension="2015-08-01",
                description="Mental Status Section (V2) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        observations: Sequence[MentalStatusObservationProtocol] = None,
        organizers: Sequence[MentalStatusOrganizerProtocol] = None,
        title: str = "Mental Status",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MentalStatusSection builder.

        Args:
            observations: List of mental status observations (optional)
            organizers: List of mental status organizers (optional)
            title: Section title (default: "Mental Status")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement

        Note:
            Either observations or organizers (or both) should be provided.
            If neither is provided, the section will show "No mental status observations recorded."
        """
        super().__init__(version=version, **kwargs)
        self.observations = observations or []
        self.organizers = organizers or []
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Mental Status Section XML element.

        Returns:
            lxml Element for section

        CONF Rules Implemented:
            - CONF:1198-28293, CONF:1198-28294, CONF:1198-32793: templateId
            - CONF:1198-28295, CONF:1198-28296, CONF:1198-30826: code=10190-7 (LOINC)
            - CONF:1198-28297: title [1..1]
            - CONF:1198-28298: text [1..1]
            - CONF:1198-28301, CONF:1198-28302: entry with Mental Status Organizer [0..*]
            - CONF:1198-28305, CONF:1198-28306: entry with Mental Status Observation [0..*]
            - CONF:1198-28313, CONF:1198-28314: entry with Assessment Scale Observation [0..*]
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # CONF:1198-28293, CONF:1198-28294, CONF:1198-32793: Add template IDs
        self.add_template_ids(section)

        # CONF:1198-28295, CONF:1198-28296, CONF:1198-30826: Add section code
        code_elem = Code(
            code="10190-7",
            system="LOINC",
            display_name="Mental Status",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # CONF:1198-28297: Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # CONF:1198-28298: Add narrative text (HTML table)
        self._add_narrative(section)

        # CONF:1198-28301, CONF:1198-28302: Add entries with Mental Status Organizers
        for organizer in self.organizers:
            self._add_organizer_entry(section, organizer)

        # CONF:1198-28305, CONF:1198-28306: Add entries with Mental Status Observations
        for observation in self.observations:
            self._add_observation_entry(section, observation)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        # Check if we have any data to display
        if not self.observations and not self.organizers:
            # No mental status data - add "No observations recorded" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No mental status observations recorded"
            return

        # Create table for mental status observations
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Category", "Finding/Value", "Date", "Status"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        # Add observations from organizers (grouped)
        idx = 1
        for organizer in self.organizers:
            for obs in organizer.observations:
                self._add_observation_row(tbody, obs, organizer.category, idx)
                idx += 1

        # Add standalone observations
        for obs in self.observations:
            category = obs.category if obs.category else "General"
            self._add_observation_row(tbody, obs, category, idx)
            idx += 1

    def _add_observation_row(
        self,
        tbody: etree._Element,
        obs: MentalStatusObservationProtocol,
        category: str,
        idx: int,
    ) -> None:
        """
        Add a single observation row to the narrative table.

        Args:
            tbody: table body element
            obs: observation data
            category: category name
            idx: row index for ID
        """
        tr = etree.SubElement(tbody, f"{{{NS}}}tr")

        # Category
        td_category = etree.SubElement(tr, f"{{{NS}}}td")
        td_category.text = category

        # Finding/Value (with ID reference)
        td_value = etree.SubElement(tr, f"{{{NS}}}td")
        content = etree.SubElement(
            td_value,
            f"{{{NS}}}content",
            ID=f"mental-status-{idx}",
        )
        content.text = obs.value

        # Date
        td_date = etree.SubElement(tr, f"{{{NS}}}td")
        obs_date = obs.observation_date
        if obs_date:
            td_date.text = obs_date.strftime("%Y-%m-%d")
        else:
            td_date.text = "Unknown"

        # Status
        td_status = etree.SubElement(tr, f"{{{NS}}}td")
        td_status.text = obs.status.capitalize() if obs.status else "Completed"

    def _add_organizer_entry(
        self,
        section: etree._Element,
        organizer: MentalStatusOrganizerProtocol,
    ) -> None:
        """
        Add entry element with Mental Status Organizer.

        Args:
            section: section element
            organizer: organizer data
        """
        # CONF:1198-28301, CONF:1198-28302
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Mental Status Organizer
        organizer_builder = MentalStatusOrganizer(organizer, version=self.version)
        entry.append(organizer_builder.to_element())

    def _add_observation_entry(
        self,
        section: etree._Element,
        observation: MentalStatusObservationProtocol,
    ) -> None:
        """
        Add entry element with Mental Status Observation.

        Args:
            section: section element
            observation: observation data
        """
        # CONF:1198-28305, CONF:1198-28306
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Mental Status Observation
        obs_builder = MentalStatusObservation(observation, version=self.version)
        entry.append(obs_builder.to_element())
