"""Past Medical History Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.problem import ProblemProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PastMedicalHistorySection(CDAElement):
    """
    Builder for C-CDA Past Medical History Section.

    This section contains a record of the patient's past complaints, problems,
    and diagnoses. It contains data from the patient's past up to the patient's
    current complaint or reason for seeking medical care.

    Includes narrative (HTML table) and structured entries with Problem Observations.
    Supports both R2.1 (2015-08-01) and R2.0 versions.

    Conformance:
    - Template ID: 2.16.840.1.113883.10.20.22.2.20
    - Code: 11348-0 (History of Past Illness) from LOINC
    - Contains: Problem Observation entries (optional, 0..*)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.20",
                extension="2015-08-01",
                description="Past Medical History Section (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.20",
                extension=None,  # R2.0 may not have extension
                description="Past Medical History Section R2.0",
            ),
        ],
    }

    def __init__(
        self,
        problems: Sequence[ProblemProtocol],
        title: str = "Past Medical History",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PastMedicalHistorySection builder.

        Args:
            problems: List of problems satisfying ProblemProtocol
            title: Section title (default: "Past Medical History")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.problems = problems
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Past Medical History Section XML element.

        Conformance:
        - CONF:1198-7828: SHALL contain templateId
        - CONF:1198-10390: templateId/@root="2.16.840.1.113883.10.20.22.2.20"
        - CONF:1198-32536: templateId/@extension="2015-08-01" (R2.1)
        - CONF:1198-15474: SHALL contain code
        - CONF:1198-15475: code/@code="11348-0"
        - CONF:1198-30831: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        - CONF:1198-7830: SHALL contain title
        - CONF:1198-7831: SHALL contain text
        - CONF:1198-8791: MAY contain entries
        - CONF:1198-15476: entry SHALL contain Problem Observation

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1198-7828, CONF:1198-10390, CONF:1198-32536)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15474, CONF:1198-15475, CONF:1198-30831)
        # 11348-0 = History of Past Illness (LOINC)
        code_elem = Code(
            code="11348-0",
            system="LOINC",
            display_name="History of Past Illness",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-7830)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1198-7831)
        self._add_narrative(section)

        # Add entries with Problem Observations (CONF:1198-8791, CONF:1198-15476)
        for problem in self.problems:
            self._add_entry(section, problem)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        The narrative provides human-readable content for the section.
        When no problems are present, displays "No past medical history".

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.problems:
            # No problems - add "No past medical history" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No past medical history"
            return

        # Create table for problems
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Problem", "Code", "Status", "Onset Date", "Resolved Date"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, problem in enumerate(self.problems, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Problem name (with ID reference for linking)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"pmh-problem-{idx}",
            )
            content.text = problem.name

            # Code with system
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            td_code.text = f"{problem.code} ({problem.code_system})"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = problem.status.capitalize()

            # Onset date
            td_onset = etree.SubElement(tr, f"{{{NS}}}td")
            if problem.onset_date:
                td_onset.text = problem.onset_date.strftime("%Y-%m-%d")
            else:
                td_onset.text = "Unknown"

            # Resolved date
            td_resolved = etree.SubElement(tr, f"{{{NS}}}td")
            if problem.resolved_date:
                td_resolved.text = problem.resolved_date.strftime("%Y-%m-%d")
            else:
                # Show different text based on status
                if problem.status.lower() == "active":
                    td_resolved.text = "Ongoing"
                elif problem.status.lower() == "resolved":
                    td_resolved.text = "Unknown"
                else:
                    td_resolved.text = "-"

    def _add_entry(self, section: etree._Element, problem: ProblemProtocol) -> None:
        """
        Add entry element with Problem Observation.

        Per the spec (CONF:1198-8791, CONF:1198-15476), each entry SHALL contain
        a Problem Observation. Unlike the Problems Section which wraps observations
        in a Problem Concern Act, the Past Medical History Section typically contains
        Problem Observations directly.

        Args:
            section: section element
            problem: Problem data
        """
        # Create entry element (CONF:1198-8791)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Problem Observation (CONF:1198-15476)
        obs_builder = ProblemObservation(problem, version=self.version)
        entry.append(obs_builder.to_element())
