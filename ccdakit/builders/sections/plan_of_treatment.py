"""Plan of Treatment Section builder for C-CDA documents."""

from typing import Optional, Sequence, Union

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.instruction import Instruction
from ccdakit.builders.entries.planned_act import PlannedAct
from ccdakit.builders.entries.planned_encounter import PlannedEncounter
from ccdakit.builders.entries.planned_immunization import PlannedImmunization
from ccdakit.builders.entries.planned_medication import PlannedMedication
from ccdakit.builders.entries.planned_observation import PlannedObservation
from ccdakit.builders.entries.planned_procedure import PlannedProcedure
from ccdakit.builders.entries.planned_supply import PlannedSupply
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import (
    InstructionProtocol,
    PlannedActProtocol,
    PlannedEncounterProtocol,
    PlannedImmunizationProtocol,
    PlannedMedicationProtocol,
    PlannedObservationProtocol,
    PlannedProcedureProtocol,
    PlannedSupplyProtocol,
)


# CDA namespace
NS = "urn:hl7-org:v3"

# Type alias for all planned activities
PlannedActivityType = Union[
    PlannedObservationProtocol,
    PlannedProcedureProtocol,
    PlannedEncounterProtocol,
    PlannedActProtocol,
    PlannedMedicationProtocol,
    PlannedSupplyProtocol,
    PlannedImmunizationProtocol,
    InstructionProtocol,
]


class PlanOfTreatmentSection(CDAElement):
    """
    Builder for C-CDA Plan of Treatment Section (V2).

    Includes narrative (HTML table) and structured entries for planned activities.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.2.10

    This section contains pending orders, interventions, encounters, services,
    and procedures for the patient. All entries use moodCode of INT (intent)
    or other prospective mood codes.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.10",
                extension="2014-06-09",
                description="Plan of Treatment Section (V2) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.10",
                extension="2014-06-09",
                description="Plan of Treatment Section (V2) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        planned_observations: Optional[Sequence[PlannedObservationProtocol]] = None,
        planned_procedures: Optional[Sequence[PlannedProcedureProtocol]] = None,
        planned_encounters: Optional[Sequence[PlannedEncounterProtocol]] = None,
        planned_acts: Optional[Sequence[PlannedActProtocol]] = None,
        planned_medications: Optional[Sequence[PlannedMedicationProtocol]] = None,
        planned_supplies: Optional[Sequence[PlannedSupplyProtocol]] = None,
        planned_immunizations: Optional[Sequence[PlannedImmunizationProtocol]] = None,
        instructions: Optional[Sequence[InstructionProtocol]] = None,
        title: str = "Plan of Treatment",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlanOfTreatmentSection builder.

        Args:
            planned_observations: List of planned observations
            planned_procedures: List of planned procedures
            planned_encounters: List of planned encounters
            planned_acts: List of planned acts
            planned_medications: List of planned medications
            planned_supplies: List of planned supplies
            planned_immunizations: List of planned immunizations
            instructions: List of instructions
            title: Section title (default: "Plan of Treatment")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.planned_observations = planned_observations or []
        self.planned_procedures = planned_procedures or []
        self.planned_encounters = planned_encounters or []
        self.planned_acts = planned_acts or []
        self.planned_medications = planned_medications or []
        self.planned_supplies = planned_supplies or []
        self.planned_immunizations = planned_immunizations or []
        self.instructions = instructions or []
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Plan of Treatment Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1098-7723, CONF:1098-10435, CONF:1098-32501)
        self.add_template_ids(section)

        # Add section code (CONF:1098-14749, CONF:1098-14750, CONF:1098-30813)
        code_elem = Code(
            code="18776-5",
            system="LOINC",
            display_name="Plan of Treatment",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1098-16986)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1098-7725)
        self._add_narrative(section)

        # Add entries for each type of planned activity
        # Planned Observations (CONF:1098-7726, CONF:1098-14751)
        for obs in self.planned_observations:
            self._add_entry(section, obs, PlannedObservation)

        # Planned Encounters (CONF:1098-8805, CONF:1098-30472)
        for enc in self.planned_encounters:
            self._add_entry(section, enc, PlannedEncounter)

        # Planned Acts (CONF:1098-8807, CONF:1098-30473)
        for act in self.planned_acts:
            self._add_entry(section, act, PlannedAct)

        # Planned Procedures (CONF:1098-8809, CONF:1098-30474)
        for proc in self.planned_procedures:
            self._add_entry(section, proc, PlannedProcedure)

        # Planned Medications (CONF:1098-8811, CONF:1098-30475)
        for med in self.planned_medications:
            self._add_entry(section, med, PlannedMedication)

        # Planned Supplies (CONF:1098-8813, CONF:1098-30476)
        for supply in self.planned_supplies:
            self._add_entry(section, supply, PlannedSupply)

        # Instructions (CONF:1098-14695, CONF:1098-31397)
        for instruction in self.instructions:
            self._add_entry(section, instruction, Instruction)

        # Planned Immunizations (CONF:1098-32353, CONF:1098-32354)
        for immunization in self.planned_immunizations:
            self._add_entry(section, immunization, PlannedImmunization)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        # Collect all activities
        all_activities = []

        for obs in self.planned_observations:
            all_activities.append(("Observation", obs))
        for proc in self.planned_procedures:
            all_activities.append(("Procedure", proc))
        for enc in self.planned_encounters:
            all_activities.append(("Encounter", enc))
        for act in self.planned_acts:
            all_activities.append(("Act", act))
        for med in self.planned_medications:
            all_activities.append(("Medication", med))
        for supply in self.planned_supplies:
            all_activities.append(("Supply", supply))
        for immunization in self.planned_immunizations:
            all_activities.append(("Immunization", immunization))
        for instruction in self.instructions:
            all_activities.append(("Instruction", instruction))

        if not all_activities:
            # No planned activities - add "No planned activities" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No planned activities"
            return

        # Create table for planned activities
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Type", "Description", "Code", "Status", "Planned Date"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, (activity_type, activity) in enumerate(all_activities, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Activity type
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            td_type.text = activity_type

            # Description (with ID reference)
            td_desc = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_desc,
                f"{{{NS}}}content",
                ID=f"planned-activity-{idx}",
            )
            # Check if it's an instruction by checking for instruction_text attribute
            if hasattr(activity, "instruction_text"):
                content.text = activity.instruction_text
            else:
                content.text = activity.description

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(activity, "code") and activity.code:
                code_system = getattr(activity, "code_system", "Unknown")
                td_code.text = f"{activity.code} ({code_system})"
            else:
                td_code.text = "N/A"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(activity, "status"):
                td_status.text = activity.status.capitalize()
            else:
                td_status.text = "N/A"

            # Planned date
            td_date = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(activity, "planned_date") and activity.planned_date:
                td_date.text = activity.planned_date.strftime("%Y-%m-%d")
            else:
                td_date.text = "Not specified"

    def _add_entry(
        self,
        section: etree._Element,
        activity: PlannedActivityType,
        builder_class: type,
    ) -> None:
        """
        Add entry element with planned activity.

        Args:
            section: section element
            activity: Planned activity data
            builder_class: Builder class to use for creating entry
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add activity element
        activity_builder = builder_class(activity, version=self.version)
        entry.append(activity_builder.to_element())
