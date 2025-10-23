"""Intervention Act entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.intervention import InterventionProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class InterventionAct(CDAElement):
    """
    Builder for C-CDA Intervention Act (V2) entry.

    Represents an intervention that has occurred (moodCode=EVN).
    This is a wrapper for intervention-type activities considered parts of
    the same intervention. All interventions referenced in an Intervention Act
    must have a moodCode of EVN (event).

    Template ID: 2.16.840.1.113883.10.20.22.4.131
    Release: 2015-08-01

    Conformance Rules:
    - SHALL contain classCode="ACT" (CONF:1198-30971)
    - SHALL contain moodCode="EVN" (CONF:1198-30972)
    - SHALL contain at least one [1..*] id (CONF:1198-30975)
    - SHALL contain code="362956003" from SNOMED CT (CONF:1198-30976, CONF:1198-30977, CONF:1198-30978)
    - SHALL contain statusCode="completed" (CONF:1198-30979, CONF:1198-32316)
    - SHOULD contain effectiveTime (CONF:1198-31624)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.131",
                extension="2015-08-01",
                description="Intervention Act (V2)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.131",
                extension="2015-08-01",
                description="Intervention Act (V2)",
            ),
        ],
    }

    # SNOMED CT OID
    SNOMED_OID = "2.16.840.1.113883.6.96"

    def __init__(
        self,
        intervention: InterventionProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize InterventionAct builder.

        Args:
            intervention: Intervention data satisfying InterventionProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.intervention = intervention

    def build(self) -> etree.Element:
        """
        Build Intervention Act XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1198-30971, CONF:1198-30972)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",  # EVN = Event (occurred)
        )

        # Add template IDs (CONF:1198-30973, CONF:1198-30974, CONF:1198-32916)
        self.add_template_ids(act)

        # Add IDs (CONF:1198-30975) - SHALL contain at least one [1..*]
        self._add_ids(act)

        # Add code (CONF:1198-30976, CONF:1198-30977, CONF:1198-30978)
        # Fixed code: 362956003 = procedure / intervention (navigational concept)
        code_elem = Code(
            code="362956003",
            system="SNOMED",
            display_name="Procedure",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add statusCode (CONF:1198-30979, CONF:1198-32316)
        # For EVN mood, status SHALL be "completed"
        status_elem = StatusCode("completed").to_element()
        act.append(status_elem)

        # Add effectiveTime (CONF:1198-31624) - SHOULD contain
        self._add_effective_time(act)

        # Add entryRelationship for goal reference if present (CONF:1198-31621, CONF:1198-31622, CONF:1198-31623)
        self._add_goal_reference(act)

        return act

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
        # SHOULD contain effectiveTime (CONF:1198-31624)
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

        An Intervention Act SHOULD reference a Goal Observation using Entry Reference.
        (CONF:1198-31621, CONF:1198-31622, CONF:1198-31623, CONF:1198-32459)

        Args:
            act: act element
        """
        if hasattr(self.intervention, "goal_reference_id") and self.intervention.goal_reference_id:
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
