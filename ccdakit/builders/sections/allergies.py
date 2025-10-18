"""Allergies Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code, StatusCode
from ccdakit.builders.entries.allergy import AllergyObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.allergy import AllergyProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AllergiesSection(CDAElement):
    """
    Builder for C-CDA Allergies and Intolerances Section.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.6.1",
                extension="2015-08-01",
                description="Allergies and Intolerances Section (entries required) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.6.1",
                extension="2015-08-01",
                description="Allergies and Intolerances Section (entries required) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        allergies: Sequence[AllergyProtocol],
        title: str = "Allergies and Intolerances",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AllergiesSection builder.

        Args:
            allergies: List of allergies satisfying AllergyProtocol
            title: Section title (default: "Allergies and Intolerances")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.allergies = allergies
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Allergies and Intolerances Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (48765-2 = Allergies and adverse reactions Document)
        code_elem = Code(
            code="48765-2",
            system="LOINC",
            display_name="Allergies and adverse reactions Document",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Allergy Concern Acts
        for allergy in self.allergies:
            self._add_entry(section, allergy)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.allergies:
            # No allergies - add "No known allergies" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No known allergies"
            return

        # Create table for allergies
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Allergen",
            "Type",
            "Reaction",
            "Severity",
            "Status",
            "Onset Date",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, allergy in enumerate(self.allergies, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Allergen name (with ID reference)
            td_allergen = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_allergen,
                f"{{{NS}}}content",
                ID=f"allergy-{idx}",
            )
            content.text = allergy.allergen

            # Type
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            td_type.text = allergy.allergy_type.capitalize()

            # Reaction
            td_reaction = etree.SubElement(tr, f"{{{NS}}}td")
            td_reaction.text = allergy.reaction if allergy.reaction else "Not specified"

            # Severity
            td_severity = etree.SubElement(tr, f"{{{NS}}}td")
            td_severity.text = (
                allergy.severity.capitalize() if allergy.severity else "Not specified"
            )

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = allergy.status.capitalize()

            # Onset date
            td_onset = etree.SubElement(tr, f"{{{NS}}}td")
            if allergy.onset_date:
                td_onset.text = allergy.onset_date.strftime("%Y-%m-%d")
            else:
                td_onset.text = "Unknown"

    def _add_entry(self, section: etree._Element, allergy: AllergyProtocol) -> None:
        """
        Add entry element with Allergy Concern Act and Observation.

        Args:
            section: section element
            allergy: Allergy data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create Allergy Concern Act (wrapper for observations)
        act = etree.SubElement(
            entry,
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template ID for Allergy Concern Act
        template_id = etree.SubElement(act, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.30")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2015-08-01")

        # Add ID
        import uuid

        id_elem = etree.SubElement(act, f"{{{NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))

        # Add code
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("code", "CONC")
        code_elem.set("codeSystem", "2.16.840.1.113883.5.6")
        code_elem.set("displayName", "Concern")

        # Add status code (active or completed based on allergy status)
        status = "active" if allergy.status.lower() == "active" else "completed"
        status_elem = StatusCode(status).to_element()
        act.append(status_elem)

        # Add effective time (low = onset date, high = resolved date if resolved)
        time_elem = etree.SubElement(act, f"{{{NS}}}effectiveTime")
        if allergy.onset_date:
            low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
            low_elem.set("value", allergy.onset_date.strftime("%Y%m%d"))
        if status == "completed":
            # If resolved, add high element (could use current date or specific resolved date)
            high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
            high_elem.set("nullFlavor", "UNK")

        # Add entryRelationship with Allergy Observation
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
        )

        # Create and add Allergy Observation
        allergy_builder = AllergyObservation(allergy, version=self.version)
        entry_rel.append(allergy_builder.to_element())
