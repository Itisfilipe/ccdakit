"""Physical Exam Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.physical_exam import LongitudinalCareWoundObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.physical_exam import WoundObservationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PhysicalExamSection(CDAElement):
    """
    Builder for C-CDA Physical Exam Section (V3).

    The section includes direct observations made by a clinician. The examination
    may include the use of simple instruments and may also describe simple maneuvers
    performed directly on the patient's body.

    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Conforms to:
    - Physical Exam Section (V3): 2.16.840.1.113883.10.20.2.10:2015-08-01
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.2.10",
                extension="2015-08-01",
                description="Physical Exam Section (V3)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.2.10",
                extension="2015-08-01",
                description="Physical Exam Section (V3)",
            ),
        ],
    }

    def __init__(
        self,
        wound_observations: Optional[Sequence[WoundObservationProtocol]] = None,
        title: str = "Physical Exam",
        text: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PhysicalExamSection builder.

        Args:
            wound_observations: Optional list of wound observations
            title: Section title (default: "Physical Exam")
            text: Optional narrative text content
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.wound_observations = wound_observations or []
        self.title = title
        self.text = text

    def build(self) -> etree.Element:
        """
        Build Physical Exam Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template ID (CONF:1198-7806, CONF:1198-10465, CONF:1198-32587)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15397, CONF:1198-15398, CONF:1198-30931)
        code_elem = Code(
            code="29545-1",
            system="LOINC",
            display_name="Physical Findings",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-7808)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1198-7809)
        self._add_narrative(section)

        # Add entries with Wound Observations (CONF:1198-31926, CONF:1198-31927)
        for wound_obs in self.wound_observations:
            self._add_entry(section, wound_obs)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element (CONF:1198-7809).

        Args:
            section: section element
        """
        # Create text element
        text_elem = etree.SubElement(section, f"{{{NS}}}text")

        if self.text:
            # Use provided narrative text
            text_elem.text = self.text
        elif not self.wound_observations:
            # No observations - add default paragraph
            paragraph = etree.SubElement(text_elem, f"{{{NS}}}paragraph")
            paragraph.text = "No physical exam findings recorded"
        else:
            # Create table for wound observations
            table = etree.SubElement(text_elem, f"{{{NS}}}table", border="1", width="100%")

            # Table header
            thead = etree.SubElement(table, f"{{{NS}}}thead")
            tr = etree.SubElement(thead, f"{{{NS}}}tr")

            headers = [
                "Date/Time",
                "Wound Type",
                "Location",
                "Laterality",
            ]
            for header_text in headers:
                th = etree.SubElement(tr, f"{{{NS}}}th")
                th.text = header_text

            # Table body
            tbody = etree.SubElement(table, f"{{{NS}}}tbody")

            for obs_idx, wound_obs in enumerate(self.wound_observations, start=1):
                tr = etree.SubElement(tbody, f"{{{NS}}}tr")

                # Date/Time
                td_date = etree.SubElement(tr, f"{{{NS}}}td")
                if hasattr(wound_obs.date, 'strftime'):
                    td_date.text = wound_obs.date.strftime("%Y-%m-%d %H:%M")
                else:
                    td_date.text = str(wound_obs.date)

                # Wound Type (with ID reference)
                td_type = etree.SubElement(tr, f"{{{NS}}}td")
                content = etree.SubElement(
                    td_type,
                    f"{{{NS}}}content",
                    ID=f"wound-{obs_idx}",
                )
                content.text = wound_obs.wound_type

                # Location
                td_location = etree.SubElement(tr, f"{{{NS}}}td")
                if wound_obs.location:
                    td_location.text = wound_obs.location
                else:
                    td_location.text = "-"

                # Laterality
                td_laterality = etree.SubElement(tr, f"{{{NS}}}td")
                if wound_obs.laterality:
                    td_laterality.text = wound_obs.laterality
                else:
                    td_laterality.text = "-"

    def _add_entry(self, section: etree._Element, wound_obs: WoundObservationProtocol) -> None:
        """
        Add entry element with Wound Observation (CONF:1198-31926, CONF:1198-31927).

        Args:
            section: section element
            wound_obs: Wound observation data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Wound Observation
        observation_builder = LongitudinalCareWoundObservation(wound_obs, version=self.version)
        entry.append(observation_builder.to_element())
