"""Problem Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.problem import ProblemProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ProblemObservation(CDAElement):
    """
    Builder for C-CDA Problem Observation entry.

    Represents a single problem/diagnosis with codes, dates, and status.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.4",
                extension="2015-08-01",
                description="Problem Observation R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.4",
                extension="2014-06-09",
                description="Problem Observation R2.0",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"
    ICD10_OID = "2.16.840.1.113883.6.90"
    PROBLEM_TYPE_OID = "2.16.840.1.113883.6.96"  # SNOMED for problem type

    # Status codes mapping
    STATUS_CODES = {
        "active": "active",
        "inactive": "inactive",
        "resolved": "completed",
        "completed": "completed",
    }

    def __init__(
        self,
        problem: ProblemProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ProblemObservation builder.

        Args:
            problem: Problem data satisfying ProblemProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.problem = problem

    def build(self) -> etree.Element:
        """
        Build Problem Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element with required attributes
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(observation)

        # Add IDs
        self._add_ids(observation)

        # Add problem type code (55607006 = Problem)
        code_elem = Code(
            code="55607006",
            system="SNOMED",
            display_name="Problem",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add status code
        status = self._map_status(self.problem.status)
        status_elem = StatusCode(status).to_element()
        observation.append(status_elem)

        # Add effective time (onset and resolved dates)
        self._add_effective_time(observation)

        # Add value (the actual problem code)
        self._add_value(observation)

        return observation

    def _add_ids(self, observation: etree._Element) -> None:
        """
        Add ID elements to observation.

        Args:
            observation: observation element
        """
        # Add persistent ID if available
        if self.problem.persistent_id:
            pid = self.problem.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            observation.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            observation.append(id_elem)

    def _add_effective_time(self, observation: etree._Element) -> None:
        """
        Add effectiveTime with onset and optionally resolved dates.

        Args:
            observation: observation element
        """
        if self.problem.onset_date or self.problem.resolved_date:
            time_elem = EffectiveTime(
                low=self.problem.onset_date,
                high=self.problem.resolved_date,
            ).to_element()
            observation.append(time_elem)

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with problem code.

        Args:
            observation: observation element
        """
        # Determine code system OID
        code_system = self.problem.code_system.upper()
        if "SNOMED" in code_system:
            system_oid = self.SNOMED_OID
            system_name = "SNOMED CT"
        elif "ICD" in code_system or "ICD-10" in code_system:
            system_oid = self.ICD10_OID
            system_name = "ICD-10-CM"
        else:
            # Default to SNOMED
            system_oid = self.SNOMED_OID
            system_name = self.problem.code_system

        # Create value element as CD (Concept Descriptor)
        value = etree.SubElement(
            observation,
            f"{{{NS}}}value",
        )
        value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")
        value.set("code", self.problem.code)
        value.set("codeSystem", system_oid)
        value.set("codeSystemName", system_name)
        value.set("displayName", self.problem.name)

    def _map_status(self, status: str) -> str:
        """
        Map problem status to observation status code.

        Args:
            status: Problem status

        Returns:
            Observation status code
        """
        return self.STATUS_CODES.get(status.lower(), "active")
