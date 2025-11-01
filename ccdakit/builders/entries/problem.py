"""Problem Observation entry builder for C-CDA documents."""

from typing import Optional

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode, create_default_author_participation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.author import AuthorProtocol
from ccdakit.protocols.problem import ProblemProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ProblemObservation(CDAElement):
    """
    Builder for C-CDA Problem Observation entry.

    Represents a single problem/diagnosis with codes, dates, and status.
    Supports both R2.1 V4 (2022-06-01) and R2.0 (2014-06-09) versions.

    Per C-CDA 2.1 specification:
    - effectiveTime/low is REQUIRED (SHALL contain)
    - statusCode is always "completed" (observation of a problem is completed)
    - Author Participation SHOULD be included
    """

    # Template IDs for different versions
    # Note: V4 (2022-06-01) conforms to V3 (2015-08-01), so both templates are included
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.4",
                extension="2022-06-01",
                description="Problem Observation V4 (R2.1)",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.4",
                extension="2015-08-01",
                description="Problem Observation V3 (conforms to)",
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
        author: Optional[AuthorProtocol] = None,
        **kwargs,
    ):
        """
        Initialize ProblemObservation builder.

        Args:
            problem: Problem data satisfying ProblemProtocol
            version: C-CDA version (R2.1 or R2.0)
            author: Optional author participation (SHOULD be included per spec)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.problem = problem
        self.author = author

    def build(self) -> etree.Element:
        """
        Build Problem Observation XML element.

        Returns:
            lxml Element for observation

        Raises:
            ValueError: If onset_date (effectiveTime/low) is missing for R2.1
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

        # Add problem type code (CONF:4515-9045)
        # SHALL contain exactly one code, which SHOULD be selected from
        # ValueSet Problem Type (SNOMEDCT) 2.16.840.1.113883.3.88.12.3221.7.2
        # Using 55607006 = "Problem" (SNOMED CT)
        code_elem = Code(
            code="55607006",
            system="SNOMED",
            display_name="Problem",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add status code
        # Per C-CDA specification, Problem Observation statusCode SHALL be "completed"
        # because it represents a completed observation of a problem (even if problem is active)
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effective time (onset and resolved dates)
        # SHALL contain effectiveTime with low (CONF:4515-9050, CONF:4515-15603)
        self._add_effective_time(observation)

        # Add value (the actual problem code)
        self._add_value(observation)

        # Add author participation (SHOULD per CONF:4515-31147)
        # Always add author participation to meet SHOULD requirement
        self._add_author(observation)

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

        Per C-CDA 2.1 spec (CONF:4515-9050, CONF:4515-15603):
        - SHALL contain exactly one effectiveTime
        - This effectiveTime SHALL contain exactly one low (onset date)
        - This effectiveTime MAY contain zero or one high (resolution date)

        Args:
            observation: observation element

        Raises:
            ValueError: If onset_date is missing for R2.1
        """
        # For R2.1, onset_date (low) is REQUIRED
        if self.version == CDAVersion.R2_1 and not self.problem.onset_date:
            raise ValueError(
                "Problem Observation in C-CDA R2.1 SHALL contain "
                "effectiveTime/low (onset date). Please provide onset_date."
            )

        # Build effectiveTime with low and optional high
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

    def _add_author(self, observation: etree._Element) -> None:
        """
        Add Author Participation to the observation.

        Per C-CDA 2.1 spec (CONF:4515-31147):
        - Problem Observation SHOULD contain zero or more Author Participation

        This creates an author element with:
        - templateId (2.16.840.1.113883.10.20.22.4.119)
        - time (when authored)
        - assignedAuthor with id

        Args:
            observation: observation element
        """
        if self.author:
            # Import here to avoid circular dependency
            from ccdakit.builders.header.author import Author

            # Create author participation using the Author builder
            author_builder = Author(self.author)
            author_elem = author_builder.to_element()

            # Add template ID for Author Participation (2.16.840.1.113883.10.20.22.4.119)
            template_id = etree.Element(f"{{{NS}}}templateId")
            template_id.set("root", "2.16.840.1.113883.10.20.22.4.119")
            # Insert templateId as first child of author element
            author_elem.insert(0, template_id)

            observation.append(author_elem)
        else:
            # No author provided - add default author participation
            # Use onset date as authoring time
            author_elem = create_default_author_participation(self.problem.onset_date)
            observation.append(author_elem)

    def _map_status(self, status: str) -> str:
        """
        Map problem status to observation status code.

        Args:
            status: Problem status

        Returns:
            Observation status code
        """
        return self.STATUS_CODES.get(status.lower(), "active")
