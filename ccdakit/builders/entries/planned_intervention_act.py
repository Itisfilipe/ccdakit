"""Planned Intervention Act entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.intervention import PlannedInterventionProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedInterventionAct(CDAElement):
    """
    Builder for C-CDA Planned Intervention Act (V2) entry.

    Represents a planned intervention (moodCode=INT, ARQ, PRMS, PRP, or RQO).
    This is a wrapper for planned intervention-type activities considered parts of
    the same intervention. All interventions referenced in a Planned Intervention Act
    must have moodCodes indicating they are planned (have not yet occurred).

    Template ID: 2.16.840.1.113883.10.20.22.4.146
    Release: 2015-08-01

    Conformance Rules:
    - SHALL contain classCode="ACT" (CONF:1198-32678)
    - SHALL contain moodCode from Planned Intervention moodCode value set (CONF:1198-32679)
    - SHALL contain at least one [1..*] id (CONF:1198-32681)
    - SHALL contain code="362956003" from SNOMED CT (CONF:1198-32654, CONF:1198-32682, CONF:1198-32683)
    - SHALL contain statusCode="active" (CONF:1198-32655, CONF:1198-32684)
    - SHALL contain at least one [1..*] entryRelationship with Goal reference (CONF:1198-32673)
    - SHOULD contain effectiveTime (CONF:1198-32723)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.146",
                extension="2015-08-01",
                description="Planned Intervention Act (V2)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.146",
                extension="2015-08-01",
                description="Planned Intervention Act (V2)",
            ),
        ],
    }

    # SNOMED CT OID
    SNOMED_OID = "2.16.840.1.113883.6.96"

    # Valid mood codes for planned interventions (Planned Intervention moodCode value set)
    VALID_MOOD_CODES = ["INT", "ARQ", "PRMS", "PRP", "RQO"]

    def __init__(
        self,
        intervention: PlannedInterventionProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedInterventionAct builder.

        Args:
            intervention: Planned intervention data satisfying PlannedInterventionProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.intervention = intervention

    def build(self) -> etree.Element:
        """
        Build Planned Intervention Act XML element.

        Returns:
            lxml Element for act
        """
        # Get mood code (default to INT if not specified or invalid)
        mood_code = self._get_mood_code()

        # Create act element with required attributes (CONF:1198-32678, CONF:1198-32679)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode=mood_code,
        )

        # Add template IDs (CONF:1198-32653, CONF:1198-32680, CONF:1198-32912)
        self.add_template_ids(act)

        # Add IDs (CONF:1198-32681) - SHALL contain at least one [1..*]
        self._add_ids(act)

        # Add code (CONF:1198-32654, CONF:1198-32682, CONF:1198-32683)
        # Fixed code: 362956003 = procedure / intervention (navigational concept)
        code_elem = Code(
            code="362956003",
            system="SNOMED",
            display_name="Procedure",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add statusCode (CONF:1198-32655, CONF:1198-32684)
        # For planned interventions, status SHALL be "active"
        status_elem = StatusCode("active").to_element()
        act.append(status_elem)

        # Add effectiveTime (CONF:1198-32723) - SHOULD contain
        self._add_effective_time(act)

        # Add entryRelationship for goal reference (CONF:1198-32673) - SHALL contain at least one [1..*]
        self._add_goal_reference(act)

        return act

    def _get_mood_code(self) -> str:
        """
        Get mood code from intervention protocol, defaulting to INT.

        Returns:
            Valid mood code
        """
        if hasattr(self.intervention, "mood_code") and self.intervention.mood_code:
            mood = self.intervention.mood_code.upper()
            if mood in self.VALID_MOOD_CODES:
                return mood
        return "INT"  # Default to Intent

    def _add_ids(self, act: etree._Element) -> None:
        """
        Add ID elements to act.

        Args:
            act: act element
        """
        # Use provided ID or generate one
        if hasattr(self.intervention, "id") and self.intervention.id:
            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(self.intervention.id),
            ).to_element()
            act.append(id_elem)
        else:
            # Generate a UUID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            act.append(id_elem)

    def _add_effective_time(self, act: etree._Element) -> None:
        """
        Add effectiveTime element if available.

        Args:
            act: act element
        """
        # SHOULD contain effectiveTime (CONF:1198-32723)
        if hasattr(self.intervention, "effective_time") and self.intervention.effective_time:
            # For a single time point, use value attribute
            time_elem = etree.SubElement(act, f"{{{NS}}}effectiveTime")

            # Format the datetime/date
            eff_time = self.intervention.effective_time
            if hasattr(eff_time, "strftime"):
                # It's a date or datetime
                time_elem.set("value", eff_time.strftime("%Y%m%d"))
            else:
                time_elem.set("value", str(eff_time))

    def _add_goal_reference(self, act: etree._Element) -> None:
        """
        Add entryRelationship referencing Goal Observation.

        A Planned Intervention Act SHALL reference a Goal Observation using Entry Reference.
        (CONF:1198-32673, CONF:1198-32720, CONF:1198-32721, CONF:1198-32722)

        Args:
            act: act element
        """
        # This is REQUIRED for Planned Intervention Act
        if (
            not hasattr(self.intervention, "goal_reference_id")
            or not self.intervention.goal_reference_id
        ):
            # If no goal reference, create a placeholder with nullFlavor
            entry_rel = etree.SubElement(act, f"{{{NS}}}entryRelationship")
            entry_rel.set("typeCode", "RSON")

            ref_act = etree.SubElement(entry_rel, f"{{{NS}}}act")
            ref_act.set("classCode", "ACT")
            ref_act.set("moodCode", "EVN")

            # Add Entry Reference template ID
            template_id = etree.SubElement(ref_act, f"{{{NS}}}templateId")
            template_id.set("root", "2.16.840.1.113883.10.20.22.4.122")

            # Add id with nullFlavor
            id_elem = etree.SubElement(ref_act, f"{{{NS}}}id")
            id_elem.set("nullFlavor", "UNK")

            # Add code for Entry Reference
            code_elem = etree.SubElement(ref_act, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "NA")

            # Add statusCode
            status_elem = etree.SubElement(ref_act, f"{{{NS}}}statusCode")
            status_elem.set("code", "completed")
        else:
            # Create entryRelationship with typeCode="RSON" (Has reason)
            entry_rel = etree.SubElement(act, f"{{{NS}}}entryRelationship")
            entry_rel.set("typeCode", "RSON")

            # Create act element for Entry Reference template (2.16.840.1.113883.10.20.22.4.122)
            ref_act = etree.SubElement(entry_rel, f"{{{NS}}}act")
            ref_act.set("classCode", "ACT")
            ref_act.set("moodCode", "EVN")

            # Add Entry Reference template ID
            template_id = etree.SubElement(ref_act, f"{{{NS}}}templateId")
            template_id.set("root", "2.16.840.1.113883.10.20.22.4.122")

            # Add id element with reference to goal
            id_elem = etree.SubElement(ref_act, f"{{{NS}}}id")
            id_elem.set("root", str(self.intervention.goal_reference_id))

            # Add code for Entry Reference
            code_elem = etree.SubElement(ref_act, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "NA")

            # Add statusCode
            status_elem = etree.SubElement(ref_act, f"{{{NS}}}statusCode")
            status_elem.set("code", "completed")
