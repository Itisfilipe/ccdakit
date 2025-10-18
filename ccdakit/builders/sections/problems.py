"""Problems Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code, StatusCode
from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.problem import ProblemProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ProblemsSection(CDAElement):
    """
    Builder for C-CDA Problems Section.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.5.1",
                extension="2015-08-01",
                description="Problems Section (entries required) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.5.1",
                extension="2014-06-09",
                description="Problems Section (entries required) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        problems: Sequence[ProblemProtocol],
        title: str = "Problems",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ProblemsSection builder.

        Args:
            problems: List of problems satisfying ProblemProtocol
            title: Section title (default: "Problems")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.problems = problems
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Problems Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (11450-4 = Problem List)
        code_elem = Code(
            code="11450-4",
            system="LOINC",
            display_name="Problem List",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Problem Concern Acts
        for problem in self.problems:
            self._add_entry(section, problem)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.problems:
            # No problems - add "No known problems" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No known problems"
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

            # Problem name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"problem-{idx}",
            )
            content.text = problem.name

            # Code
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
                td_resolved.text = "Ongoing" if problem.status == "active" else "Unknown"

    def _add_entry(self, section: etree._Element, problem: ProblemProtocol) -> None:
        """
        Add entry element with Problem Concern Act and Observation.

        Args:
            section: section element
            problem: Problem data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create Problem Concern Act (wrapper for observations)
        act = etree.SubElement(
            entry,
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template ID for Problem Concern Act
        template_id = etree.SubElement(act, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.3")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2015-08-01")
        elif self.version == CDAVersion.R2_0:
            template_id.set("extension", "2014-06-09")

        # Add ID
        import uuid

        id_elem = etree.SubElement(act, f"{{{NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))

        # Add code (CONC = Concern)
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("code", "CONC")
        code_elem.set("codeSystem", "2.16.840.1.113883.5.6")
        code_elem.set("displayName", "Concern")

        # Add status code (active or completed based on problem status)
        status = "active" if problem.status.lower() == "active" else "completed"
        status_elem = StatusCode(status).to_element()
        act.append(status_elem)

        # Add effective time (low = onset date, high = resolved date if resolved)
        time_elem = etree.SubElement(act, f"{{{NS}}}effectiveTime")
        if problem.onset_date:
            low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
            low_elem.set("value", problem.onset_date.strftime("%Y%m%d"))
        else:
            # If no onset date, use nullFlavor
            low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
            low_elem.set("nullFlavor", "UNK")

        if status == "completed":
            # If resolved, add high element
            high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
            if problem.resolved_date:
                high_elem.set("value", problem.resolved_date.strftime("%Y%m%d"))
            else:
                high_elem.set("nullFlavor", "UNK")

        # Add entryRelationship with Problem Observation
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
        )

        # Create and add Problem Observation
        obs_builder = ProblemObservation(problem, version=self.version)
        entry_rel.append(obs_builder.to_element())
