"""Health Status Evaluations and Outcomes Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.outcome_observation import OutcomeObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.health_status_evaluation import OutcomeObservationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class HealthStatusEvaluationsAndOutcomesSection(CDAElement):
    """
    Builder for C-CDA Health Status Evaluations and Outcomes Section.

    This section represents outcomes of the patient's health status. These assessed
    outcomes are represented as statuses, at points in time. It also includes
    outcomes of care from the interventions used to treat the patient, related to
    established care plan goals and/or interventions.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 and R2.0 versions.

    Template ID: 2.16.840.1.113883.10.20.22.2.61

    Conformance Rules:
    - MAY contain nullFlavor="NI" (CONF:1098-32821)
    - SHALL contain templateId (CONF:1098-29578, CONF:1098-29579)
    - SHALL contain code="11383-7" (CONF:1098-29580, CONF:1098-29581, CONF:1098-29582)
    - SHALL contain title (CONF:1098-29589)
    - SHALL contain text (CONF:1098-29590)
    - SHALL contain at least one [1..*] entry with Outcome Observation (CONF:1098-31227, CONF:1098-31228)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.61",
                extension=None,
                description="Health Status Evaluations and Outcomes Section",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.61",
                extension=None,
                description="Health Status Evaluations and Outcomes Section",
            ),
        ],
    }

    def __init__(
        self,
        outcomes: Sequence[OutcomeObservationProtocol],
        title: str = "Health Status Evaluations and Outcomes",
        version: CDAVersion = CDAVersion.R2_1,
        null_flavor: str = None,
        **kwargs,
    ):
        """
        Initialize HealthStatusEvaluationsAndOutcomesSection builder.

        Args:
            outcomes: List of outcomes satisfying OutcomeObservationProtocol
            title: Section title (default: "Health Status Evaluations and Outcomes")
            version: C-CDA version (R2.1 or R2.0)
            null_flavor: Optional null flavor (e.g., "NI" for no information)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.outcomes = outcomes
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Health Status Evaluations and Outcomes Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add null flavor if specified (CONF:1098-32821)
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1098-29578, CONF:1098-29579)
        self.add_template_ids(section)

        # Add section code (CONF:1098-29580, CONF:1098-29581, CONF:1098-29582)
        # 11383-7 = Patient Problem Outcome (LOINC)
        code_elem = Code(
            code="11383-7",
            system="LOINC",
            display_name="Patient Problem Outcome",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1098-29589)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1098-29590)
        self._add_narrative(section)

        # Add entries with Outcome Observations (CONF:1098-31227, CONF:1098-31228)
        # SHALL contain at least one [1..*] entry
        if self.outcomes:
            for outcome in self.outcomes:
                self._add_entry(section, outcome)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.outcomes:
            # No outcomes - add "No outcomes documented" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No health status evaluations or outcomes documented"
            return

        # Create table for outcomes
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Outcome", "Value", "Date", "Progress Toward Goal"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, outcome in enumerate(self.outcomes, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Outcome description (with ID reference)
            td_desc = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_desc,
                f"{{{NS}}}content",
                ID=f"outcome-{idx}",
            )
            # Use display name or code
            if outcome.display_name:
                content.text = outcome.display_name
            elif outcome.code:
                content.text = f"Outcome: {outcome.code}"
            else:
                content.text = "Outcome observation"

            # Value
            td_value = etree.SubElement(tr, f"{{{NS}}}td")
            if outcome.value:
                if hasattr(outcome, "value_unit") and outcome.value_unit:
                    td_value.text = f"{outcome.value} {outcome.value_unit}"
                else:
                    td_value.text = str(outcome.value)
            else:
                td_value.text = "Not specified"

            # Effective time
            td_time = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(outcome, "effective_time") and outcome.effective_time:
                if hasattr(outcome.effective_time, "strftime"):
                    td_time.text = outcome.effective_time.strftime("%Y-%m-%d")
                else:
                    td_time.text = str(outcome.effective_time)
            else:
                td_time.text = "Not specified"

            # Progress toward goal
            td_progress = etree.SubElement(tr, f"{{{NS}}}td")
            if (
                hasattr(outcome, "progress_toward_goal")
                and outcome.progress_toward_goal
                and hasattr(outcome.progress_toward_goal, "achievement_display_name")
            ):
                td_progress.text = outcome.progress_toward_goal.achievement_display_name or "Progress documented"
            else:
                td_progress.text = "Not specified"

    def _add_entry(self, section: etree._Element, outcome: OutcomeObservationProtocol) -> None:
        """
        Add entry element with Outcome Observation.

        Args:
            section: section element
            outcome: Outcome data
        """
        # Create entry element (SHALL contain at least one entry - CONF:1098-31227)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Outcome Observation (CONF:1098-31228)
        obs_builder = OutcomeObservation(outcome, version=self.version)
        entry.append(obs_builder.to_element())
