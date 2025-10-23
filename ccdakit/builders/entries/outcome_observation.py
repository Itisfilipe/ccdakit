"""Outcome Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Identifier, StatusCode
from ccdakit.builders.entries.entry_reference import EntryReference
from ccdakit.builders.entries.progress_toward_goal import ProgressTowardGoalObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.health_status_evaluation import OutcomeObservationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class OutcomeObservation(CDAElement):
    """
    Builder for C-CDA Outcome Observation entry.

    This template represents the outcome of care resulting from the interventions
    used to treat the patient. In the Care Planning workflow, the judgment about
    how well the person is progressing towards the goal is based on the
    observations made about the status of the patient with respect to interventions
    performed in the pursuit of achieving that goal.

    Template ID: 2.16.840.1.113883.10.20.22.4.144

    Conformance Rules:
    - SHALL contain classCode="OBS" (CONF:1098-31219)
    - SHALL contain moodCode="EVN" (CONF:1098-31220)
    - SHALL contain at least one [1..*] id (CONF:1098-31223)
    - SHALL contain code from LOINC (CONF:1098-32746)
    - SHOULD contain value (CONF:1098-32747)
    - SHOULD contain Progress Toward Goal Observation (CONF:1098-31427, CONF:1098-31428, CONF:1098-31429, CONF:1098-31430)
    - SHOULD contain Entry Reference to Goal (CONF:1098-31224, CONF:1098-31225, CONF:1098-32465, CONF:1098-32461)
    - MAY contain Entry Reference to Interventions (CONF:1098-31688, CONF:1098-31689, CONF:1098-31690, CONF:1098-32462)
    - SHALL contain at least one entryRelationship (CONF:1098-32782)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.144",
                extension=None,
                description="Outcome Observation",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.144",
                extension=None,
                description="Outcome Observation",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"
    SNOMED_OID = "2.16.840.1.113883.6.96"
    UCUM_OID = "2.16.840.1.113883.6.8"

    def __init__(
        self,
        outcome: OutcomeObservationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize OutcomeObservation builder.

        Args:
            outcome: Outcome data satisfying OutcomeObservationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.outcome = outcome

    def build(self) -> etree.Element:
        """
        Build Outcome Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element with required attributes (CONF:1098-31219, CONF:1098-31220)
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template ID (CONF:1098-31221, CONF:1098-31222)
        self.add_template_ids(observation)

        # Add IDs (CONF:1098-31223) - SHALL contain at least one [1..*]
        self._add_ids(observation)

        # Add code (CONF:1098-32746) - SHOULD be from LOINC
        self._add_code(observation)

        # Add statusCode - required by CDA RIM, typically "completed"
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effectiveTime if available
        self._add_effective_time(observation)

        # Add value (CONF:1098-32747) - SHOULD contain
        self._add_value(observation)

        # Add author if available (CONF:1098-31553)
        self._add_author(observation)

        # Add entryRelationship for goal reference (CONF:1098-31224, CONF:1098-31225, CONF:1098-32465)
        # This is SHOULD contain, but helps satisfy CONF:1098-32782 (SHALL contain at least one entryRelationship)
        self._add_goal_reference(observation)

        # Add entryRelationship for progress toward goal (CONF:1098-31427, CONF:1098-31428, CONF:1098-31429, CONF:1098-31430)
        # This is SHOULD contain, also helps satisfy CONF:1098-32782
        self._add_progress_toward_goal(observation)

        # Add entryRelationship for intervention references (CONF:1098-31688, CONF:1098-31689, CONF:1098-31690)
        # This is MAY contain
        self._add_intervention_references(observation)

        return observation

    def _add_ids(self, observation: etree._Element) -> None:
        """
        Add ID elements to observation.

        Args:
            observation: observation element
        """
        # Use provided ID or generate one
        if hasattr(self.outcome, "id") and self.outcome.id:
            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(self.outcome.id),
            ).to_element()
            observation.append(id_elem)
        else:
            # Generate a UUID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            observation.append(id_elem)

    def _add_code(self, observation: etree._Element) -> None:
        """
        Add code element for observation type.

        Code SHOULD be from LOINC (CONF:1098-32746).

        Args:
            observation: observation element
        """
        # Use provided code or default to a generic observation code
        if self.outcome.code and self.outcome.code_system:
            # Determine code system OID
            code_system = self.outcome.code_system.upper()
            if "LOINC" in code_system:
                system_oid = self.LOINC_OID
                system_name = "LOINC"
            elif "SNOMED" in code_system:
                system_oid = self.SNOMED_OID
                system_name = "SNOMED CT"
            else:
                system_oid = self.outcome.code_system
                system_name = self.outcome.code_system

            code_elem = etree.SubElement(observation, f"{{{NS}}}code")
            code_elem.set("code", self.outcome.code)
            code_elem.set("codeSystem", system_oid)
            if system_name:
                code_elem.set("codeSystemName", system_name)
            if self.outcome.display_name:
                code_elem.set("displayName", self.outcome.display_name)
        else:
            # Default: use a generic outcome code
            code_elem = etree.SubElement(observation, f"{{{NS}}}code")
            code_elem.set("code", "ASSERTION")
            code_elem.set("codeSystem", "2.16.840.1.113883.5.4")
            code_elem.set("displayName", "Assertion")

    def _add_effective_time(self, observation: etree._Element) -> None:
        """
        Add effectiveTime element if available.

        Args:
            observation: observation element
        """
        if hasattr(self.outcome, "effective_time") and self.outcome.effective_time:
            time_elem = etree.SubElement(observation, f"{{{NS}}}effectiveTime")
            # Format the datetime/date
            eff_time = self.outcome.effective_time
            if hasattr(eff_time, "strftime"):
                time_elem.set("value", eff_time.strftime("%Y%m%d"))
            else:
                time_elem.set("value", str(eff_time))

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with observation result.

        SHOULD contain value (CONF:1098-32747).

        Args:
            observation: observation element
        """
        if hasattr(self.outcome, "value") and self.outcome.value:
            if hasattr(self.outcome, "value_unit") and self.outcome.value_unit:
                # Physical Quantity (PQ) with unit
                value = etree.SubElement(observation, f"{{{NS}}}value")
                value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "PQ")
                value.set("value", str(self.outcome.value))
                value.set("unit", self.outcome.value_unit)
            else:
                # String or coded value
                value = etree.SubElement(observation, f"{{{NS}}}value")
                value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "ST")
                value.text = str(self.outcome.value)

    def _add_author(self, observation: etree._Element) -> None:
        """
        Add author participation if available.

        SHOULD contain Author Participation (CONF:1098-31553).

        Args:
            observation: observation element
        """
        # Check if author information is available
        has_author = (
            hasattr(self.outcome, "author_name")
            and self.outcome.author_name
            or hasattr(self.outcome, "author_time")
            and self.outcome.author_time
        )

        if has_author:
            author_elem = etree.SubElement(observation, f"{{{NS}}}author")

            # Add time if available
            if hasattr(self.outcome, "author_time") and self.outcome.author_time:
                time_elem = etree.SubElement(author_elem, f"{{{NS}}}time")
                if hasattr(self.outcome.author_time, "strftime"):
                    time_elem.set("value", self.outcome.author_time.strftime("%Y%m%d%H%M%S"))
                else:
                    time_elem.set("value", str(self.outcome.author_time))

            # Add assignedAuthor
            assigned_author = etree.SubElement(author_elem, f"{{{NS}}}assignedAuthor")

            # Add id
            id_elem = etree.SubElement(assigned_author, f"{{{NS}}}id")
            id_elem.set("nullFlavor", "NI")

            # Add assignedPerson if name available
            if hasattr(self.outcome, "author_name") and self.outcome.author_name:
                assigned_person = etree.SubElement(assigned_author, f"{{{NS}}}assignedPerson")
                name_elem = etree.SubElement(assigned_person, f"{{{NS}}}name")
                name_elem.text = self.outcome.author_name

    def _add_goal_reference(self, observation: etree._Element) -> None:
        """
        Add entryRelationship referencing Goal Observation.

        SHOULD contain Entry Reference to Goal Observation using typeCode="GEVL"
        (CONF:1098-31224, CONF:1098-31225, CONF:1098-32465, CONF:1098-32461).

        Args:
            observation: observation element
        """
        if hasattr(self.outcome, "goal_reference_id") and self.outcome.goal_reference_id:
            # Create entryRelationship with typeCode="GEVL" (Evaluates goal)
            entry_rel = etree.SubElement(observation, f"{{{NS}}}entryRelationship")
            entry_rel.set("typeCode", "GEVL")

            # Create Entry Reference
            entry_ref = EntryReference(
                reference_id=self.outcome.goal_reference_id,
                version=self.version,
            )
            entry_rel.append(entry_ref.to_element())

    def _add_progress_toward_goal(self, observation: etree._Element) -> None:
        """
        Add entryRelationship with Progress Toward Goal Observation.

        SHOULD contain Progress Toward Goal Observation
        (CONF:1098-31427, CONF:1098-31428, CONF:1098-31429, CONF:1098-31430).

        Args:
            observation: observation element
        """
        if hasattr(self.outcome, "progress_toward_goal") and self.outcome.progress_toward_goal:
            # Create entryRelationship with typeCode="SPRT" (Has support)
            entry_rel = etree.SubElement(observation, f"{{{NS}}}entryRelationship")
            entry_rel.set("typeCode", "SPRT")
            entry_rel.set("inversionInd", "true")  # CONF:1098-31429

            # Create Progress Toward Goal Observation
            progress_obs = ProgressTowardGoalObservation(
                progress=self.outcome.progress_toward_goal,
                version=self.version,
            )
            entry_rel.append(progress_obs.to_element())

    def _add_intervention_references(self, observation: etree._Element) -> None:
        """
        Add entryRelationship elements referencing Intervention Acts.

        MAY contain Entry Reference to Intervention Acts using typeCode="RSON"
        (CONF:1098-31688, CONF:1098-31689, CONF:1098-31690, CONF:1098-32462).

        Args:
            observation: observation element
        """
        if (
            hasattr(self.outcome, "intervention_reference_ids")
            and self.outcome.intervention_reference_ids
        ):
            for intervention_id in self.outcome.intervention_reference_ids:
                # Create entryRelationship with typeCode="RSON" (Has reason)
                entry_rel = etree.SubElement(observation, f"{{{NS}}}entryRelationship")
                entry_rel.set("typeCode", "RSON")

                # Create Entry Reference
                entry_ref = EntryReference(
                    reference_id=intervention_id,
                    version=self.version,
                )
                entry_rel.append(entry_ref.to_element())
