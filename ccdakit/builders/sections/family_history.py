"""Family History Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.family_member_history import FamilyHistoryOrganizer
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.family_history import FamilyMemberHistoryProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class FamilyHistorySection(CDAElement):
    """
    Builder for C-CDA Family History Section.

    This section contains data defining the patient's genetic relatives in terms
    of possible or relevant health risk factors that have a potential impact on
    the patient's healthcare risk profile.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Conformance: 2.16.840.1.113883.10.20.22.2.15 (Family History Section V3)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.15",
                extension="2015-08-01",
                description="Family History Section (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.15",
                extension="2015-08-01",
                description="Family History Section (V3) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        family_members: Sequence[FamilyMemberHistoryProtocol],
        title: str = "Family History",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize FamilyHistorySection builder.

        Args:
            family_members: List of family members satisfying FamilyMemberHistoryProtocol
            title: Section title (default: "Family History")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.family_members = family_members
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Family History Section XML element.

        Returns:
            lxml Element for section

        Conformance Rules:
            - CONF:1198-7932: SHALL contain templateId
            - CONF:1198-10388: templateId/@root="2.16.840.1.113883.10.20.22.2.15"
            - CONF:1198-32607: templateId/@extension="2015-08-01"
            - CONF:1198-15469: SHALL contain code
            - CONF:1198-15470: code/@code="10157-6"
            - CONF:1198-32481: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
            - CONF:1198-7934: SHALL contain title
            - CONF:1198-7935: SHALL contain text
            - CONF:1198-32430: MAY contain entry
            - CONF:1198-32431: entry SHALL contain Family History Organizer
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1198-7932, CONF:1198-10388, CONF:1198-32607)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15469, CONF:1198-15470, CONF:1198-32481)
        code_elem = Code(
            code="10157-6",
            system="LOINC",
            display_name="Family History",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-7934)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1198-7935)
        self._add_narrative(section)

        # Add entries with Family History Organizers (CONF:1198-32430, CONF:1198-32431)
        for family_member in self.family_members:
            self._add_entry(section, family_member)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.family_members:
            # No family history - add "No known family history" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No known family history"
            return

        # Create table for family history
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Family Member",
            "Gender",
            "Relationship",
            "Condition",
            "Age at Onset",
            "Status",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, family_member in enumerate(self.family_members, start=1):
            # Each family member can have multiple observations
            observations = family_member.observations
            if not observations:
                # Add row for family member with no observations
                self._add_family_member_row(
                    tbody, idx, family_member, None, first_row=True
                )
            else:
                # Add row for each observation
                for obs_idx, observation in enumerate(observations):
                    self._add_family_member_row(
                        tbody,
                        idx,
                        family_member,
                        observation,
                        first_row=(obs_idx == 0),
                    )

    def _add_family_member_row(
        self,
        tbody: etree._Element,
        member_idx: int,
        family_member: FamilyMemberHistoryProtocol,
        observation,
        first_row: bool,
    ) -> None:
        """
        Add a table row for a family member observation.

        Args:
            tbody: Table body element
            member_idx: Family member index
            family_member: Family member data
            observation: Observation data (or None)
            first_row: Whether this is the first row for this family member
        """
        tr = etree.SubElement(tbody, f"{{{NS}}}tr")

        # Family member name/ID (with ID reference, only on first row)
        td_member = etree.SubElement(tr, f"{{{NS}}}td")
        if first_row:
            content = etree.SubElement(
                td_member,
                f"{{{NS}}}content",
                ID=f"family-member-{member_idx}",
            )
            content.text = f"Family Member {member_idx}"
        else:
            # Empty cell or just text for continuation rows
            td_member.text = ""

        # Gender (only on first row)
        td_gender = etree.SubElement(tr, f"{{{NS}}}td")
        if first_row and family_member.subject and family_member.subject.administrative_gender_code:
            gender_map = {
                "M": "Male",
                "F": "Female",
                "UN": "Undifferentiated",
            }
            td_gender.text = gender_map.get(
                family_member.subject.administrative_gender_code, "Unknown"
            )
        elif first_row:
            td_gender.text = "Unknown"
        else:
            td_gender.text = ""

        # Relationship (only on first row)
        td_relationship = etree.SubElement(tr, f"{{{NS}}}td")
        if first_row:
            td_relationship.text = family_member.relationship_display_name
        else:
            td_relationship.text = ""

        # Condition
        td_condition = etree.SubElement(tr, f"{{{NS}}}td")
        if observation:
            td_condition.text = observation.condition_name
        else:
            td_condition.text = "No conditions documented"

        # Age at onset
        td_age = etree.SubElement(tr, f"{{{NS}}}td")
        if observation and observation.age_at_onset is not None:
            td_age.text = f"{observation.age_at_onset} years"
        elif observation:
            td_age.text = "Unknown"
        else:
            td_age.text = ""

        # Status (deceased or living)
        td_status = etree.SubElement(tr, f"{{{NS}}}td")
        if first_row:
            if family_member.subject and family_member.subject.deceased_ind:
                if family_member.subject.deceased_time:
                    td_status.text = f"Deceased ({family_member.subject.deceased_time.strftime('%Y-%m-%d')})"
                else:
                    td_status.text = "Deceased"
            elif first_row:
                td_status.text = "Living"
            else:
                td_status.text = ""
        else:
            td_status.text = ""

    def _add_entry(
        self, section: etree._Element, family_member: FamilyMemberHistoryProtocol
    ) -> None:
        """
        Add entry element with Family History Organizer.

        Args:
            section: section element
            family_member: Family member data

        Conformance: CONF:1198-32430, CONF:1198-32431
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Family History Organizer (CONF:1198-32431)
        organizer_builder = FamilyHistoryOrganizer(family_member, version=self.version)
        entry.append(organizer_builder.to_element())
