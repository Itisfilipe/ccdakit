"""Nutrition Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.nutritional_status import NutritionalStatusObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.nutrition import NutritionalStatusProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class NutritionSection(CDAElement):
    """
    Builder for C-CDA Nutrition Section.

    Represents diet and nutrition information including special diet requirements
    and restrictions (e.g., texture modified diet, liquids only, enteral feeding).
    Also represents the overall nutritional status of the patient and nutrition
    assessment findings.

    Template: 2.16.840.1.113883.10.20.22.2.57
    Code: 61144-2 (Diet and nutrition) from LOINC

    Conformance Rules:
    - CONF:1098-30477: SHALL contain templateId
    - CONF:1098-30478: templateId/@root="2.16.840.1.113883.10.20.22.2.57"
    - CONF:1098-30318: SHALL contain code
    - CONF:1098-30319: code/@code="61144-2"
    - CONF:1098-30320: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
    - CONF:1098-31042: SHALL contain title
    - CONF:1098-31043: SHALL contain text
    - CONF:1098-30321: SHOULD contain zero or more [0..*] entry
    - CONF:1098-30322: entry SHALL contain Nutritional Status Observation

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 and R2.0 versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.57",
                extension=None,
                description="Nutrition Section",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.57",
                extension=None,
                description="Nutrition Section",
            ),
        ],
    }

    # LOINC code for nutrition section
    NUTRITION_CODE = "61144-2"
    NUTRITION_DISPLAY = "Diet and nutrition"

    def __init__(
        self,
        nutritional_statuses: Sequence[NutritionalStatusProtocol],
        title: str = "Nutrition",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize NutritionSection builder.

        Args:
            nutritional_statuses: List of nutritional status observations
            title: Section title (default: "Nutrition")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.nutritional_statuses = nutritional_statuses
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Nutrition Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1098-30477, CONF:1098-30478)
        self.add_template_ids(section)

        # Add section code (CONF:1098-30318, CONF:1098-30319, CONF:1098-30320)
        code_elem = Code(
            code=self.NUTRITION_CODE,
            system="LOINC",
            display_name=self.NUTRITION_DISPLAY,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1098-31042)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1098-31043)
        self._add_narrative(section)

        # Add entries with Nutritional Status Observations
        # (CONF:1098-30321, CONF:1098-30322)
        for status in self.nutritional_statuses:
            self._add_entry(section, status)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.nutritional_statuses:
            # No nutritional statuses - add "No nutrition information available" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No nutrition information available"
            return

        # Create table for nutritional status
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Nutritional Status",
            "Date Observed",
            "Assessment",
            "Value",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for status_idx, status in enumerate(self.nutritional_statuses, start=1):
            # First row for the nutritional status
            if status.assessments:
                # If there are assessments, show them in subsequent rows
                for assessment_idx, assessment in enumerate(status.assessments, start=1):
                    tr = etree.SubElement(tbody, f"{{{NS}}}tr")

                    if assessment_idx == 1:
                        # First assessment row includes status info
                        # Nutritional Status (with ID reference and rowspan)
                        td_status = etree.SubElement(
                            tr,
                            f"{{{NS}}}td",
                            rowspan=str(len(status.assessments)),
                        )
                        content = etree.SubElement(
                            td_status,
                            f"{{{NS}}}content",
                            ID=f"nutrition-status-{status_idx}",
                        )
                        content.text = status.status

                        # Date Observed (with rowspan)
                        td_date = etree.SubElement(
                            tr,
                            f"{{{NS}}}td",
                            rowspan=str(len(status.assessments)),
                        )
                        # Format date/datetime appropriately
                        if hasattr(status.date, "strftime"):
                            if hasattr(status.date, "hour"):
                                # It's a datetime
                                td_date.text = status.date.strftime("%Y-%m-%d %H:%M")
                            else:
                                # It's a date
                                td_date.text = status.date.strftime("%Y-%m-%d")
                        else:
                            td_date.text = str(status.date)

                    # Assessment
                    td_assessment = etree.SubElement(tr, f"{{{NS}}}td")
                    td_assessment.text = assessment.assessment_type

                    # Value
                    td_value = etree.SubElement(tr, f"{{{NS}}}td")
                    td_value.text = assessment.value
            else:
                # No assessments, just show status
                tr = etree.SubElement(tbody, f"{{{NS}}}tr")

                # Nutritional Status (with ID reference)
                td_status = etree.SubElement(tr, f"{{{NS}}}td")
                content = etree.SubElement(
                    td_status,
                    f"{{{NS}}}content",
                    ID=f"nutrition-status-{status_idx}",
                )
                content.text = status.status

                # Date Observed
                td_date = etree.SubElement(tr, f"{{{NS}}}td")
                if hasattr(status.date, "strftime"):
                    if hasattr(status.date, "hour"):
                        td_date.text = status.date.strftime("%Y-%m-%d %H:%M")
                    else:
                        td_date.text = status.date.strftime("%Y-%m-%d")
                else:
                    td_date.text = str(status.date)

                # Empty cells for assessment and value
                td_assessment = etree.SubElement(tr, f"{{{NS}}}td")
                td_assessment.text = "-"
                td_value = etree.SubElement(tr, f"{{{NS}}}td")
                td_value.text = "-"

    def _add_entry(self, section: etree._Element, status: NutritionalStatusProtocol) -> None:
        """
        Add entry element with Nutritional Status Observation.

        CONF:1098-30321: SHOULD contain zero or more [0..*] entry
        CONF:1098-30322: entry SHALL contain Nutritional Status Observation

        Args:
            section: section element
            status: Nutritional status data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Nutritional Status Observation (CONF:1098-30322)
        obs_builder = NutritionalStatusObservation(status, version=self.version)
        entry.append(obs_builder.to_element())
