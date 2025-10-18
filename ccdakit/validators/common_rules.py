"""Library of common, reusable validation rules for C-CDA documents."""

from datetime import datetime
from typing import List, Optional, Set, cast

from lxml import etree

from ..core.validation import ValidationIssue, ValidationLevel
from .rules import ValidationRule


class UniqueIDRule(ValidationRule):
    """
    Validate that all IDs in the document are unique.

    C-CDA requires that ID elements within a document are unique
    to ensure proper referential integrity.

    Configuration:
        - level: Severity level for duplicate IDs (default: ERROR)
    """

    def __init__(self, level: ValidationLevel = ValidationLevel.ERROR):
        """Initialize unique ID rule."""
        super().__init__(
            name="unique_ids",
            description="Check that all IDs in the document are unique",
        )
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate ID uniqueness."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Collect all IDs
        id_elements = document.xpath("//cda:id[@root and @extension]", namespaces=ns)
        seen_ids: Set[str] = set()

        for id_elem in id_elements:
            root = id_elem.get("root", "")
            extension = id_elem.get("extension", "")
            id_combo = f"{root}^^{extension}"

            if id_combo in seen_ids:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Duplicate ID found: root={root}, extension={extension}",
                        code="duplicate_id",
                        location=f"//id[@root='{root}'][@extension='{extension}']",
                    )
                )
            else:
                seen_ids.add(id_combo)

        return issues


class TemplateIDPresenceRule(ValidationRule):
    """
    Validate that required template IDs are present.

    Each C-CDA document and clinical statement should have
    appropriate template IDs to indicate conformance.

    Configuration:
        - required_templates: List of required template OIDs
        - level: Severity level for missing templates (default: ERROR)
    """

    def __init__(
        self,
        required_templates: Optional[List[str]] = None,
        level: ValidationLevel = ValidationLevel.ERROR,
    ):
        """Initialize template ID presence rule."""
        super().__init__(
            name="template_id_presence",
            description="Check that required template IDs are present",
        )
        self.required_templates = required_templates or [
            "2.16.840.1.113883.10.20.22.1.1",  # US Realm Header
        ]
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate template ID presence."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Get all template IDs in document
        template_ids = cast(List[str], document.xpath("//cda:templateId/@root", namespaces=ns))

        for required_template in self.required_templates:
            if required_template not in template_ids:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Required template ID {required_template} is missing",
                        code="missing_template_id",
                        location="//templateId",
                    )
                )

        return issues


class PatientNameRule(ValidationRule):
    """
    Validate patient name is present and properly formatted.

    Patient name is required in C-CDA documents and should
    contain at least given and family names.

    Configuration:
        - require_given: Require given (first) name (default: True)
        - require_family: Require family (last) name (default: True)
        - level: Severity level for name issues (default: ERROR)
    """

    def __init__(
        self,
        require_given: bool = True,
        require_family: bool = True,
        level: ValidationLevel = ValidationLevel.ERROR,
    ):
        """Initialize patient name rule."""
        super().__init__(
            name="patient_name",
            description="Check that patient name is present and properly formatted",
        )
        self.require_given = require_given
        self.require_family = require_family
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate patient name."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find patient name
        patient_names = cast(
            List[etree._Element],
            document.xpath(
                "//cda:recordTarget/cda:patientRole/cda:patient/cda:name",
                namespaces=ns,
            ),
        )

        if not patient_names:
            issues.append(
                ValidationIssue(
                    level=self.level,
                    message="Patient name is missing",
                    code="missing_patient_name",
                    location="//recordTarget/patientRole/patient",
                )
            )
            return issues

        name = patient_names[0]

        if self.require_given:
            given_names = name.xpath("cda:given/text()", namespaces=ns)
            if not given_names or not any(g.strip() for g in given_names):
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message="Patient given (first) name is missing or empty",
                        code="missing_patient_given_name",
                        location="//recordTarget/patientRole/patient/name",
                    )
                )

        if self.require_family:
            family_names = name.xpath("cda:family/text()", namespaces=ns)
            if not family_names or not any(f.strip() for f in family_names):
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message="Patient family (last) name is missing or empty",
                        code="missing_patient_family_name",
                        location="//recordTarget/patientRole/patient/name",
                    )
                )

        return issues


class DocumentDateRule(ValidationRule):
    """
    Validate document effective time is present and reasonable.

    The document effectiveTime indicates when the document was created
    and should be within a reasonable range.

    Configuration:
        - allow_future: Allow future document dates (default: False)
        - max_years_past: Maximum years in the past (default: 50)
        - level: Severity level for date issues (default: ERROR)
    """

    def __init__(
        self,
        allow_future: bool = False,
        max_years_past: int = 50,
        level: ValidationLevel = ValidationLevel.ERROR,
    ):
        """Initialize document date rule."""
        super().__init__(
            name="document_date",
            description="Check that document effective time is present and reasonable",
        )
        self.allow_future = allow_future
        self.max_years_past = max_years_past
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate document date."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find document effectiveTime
        effective_times = cast(
            List[str],
            document.xpath("/cda:ClinicalDocument/cda:effectiveTime/@value", namespaces=ns),
        )

        if not effective_times:
            issues.append(
                ValidationIssue(
                    level=self.level,
                    message="Document effectiveTime is missing",
                    code="missing_document_date",
                    location="/ClinicalDocument",
                )
            )
            return issues

        time_str = effective_times[0]
        try:
            # Parse HL7 datetime format
            if len(time_str) < 8:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Invalid document date format: {time_str} (too short, expected at least 8 characters)",
                        code="invalid_document_date",
                        location="/ClinicalDocument/effectiveTime",
                    )
                )
                return issues

            date_part = time_str[:8]
            dt = datetime.strptime(date_part, "%Y%m%d")
            today = datetime.now()

            # Check if future
            if not self.allow_future and dt > today:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Document date {date_part} is in the future",
                        code="future_document_date",
                        location="/ClinicalDocument/effectiveTime",
                    )
                )

            # Check if too old
            years_diff = (today - dt).days / 365.25
            if years_diff > self.max_years_past:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Document date {date_part} is more than {self.max_years_past} years old",
                        code="document_date_too_old",
                        location="/ClinicalDocument/effectiveTime",
                    )
                )
        except ValueError:
            issues.append(
                ValidationIssue(
                    level=self.level,
                    message=f"Invalid document date format: {time_str}",
                    code="invalid_document_date",
                    location="/ClinicalDocument/effectiveTime",
                )
            )

        return issues


class AuthorPresenceRule(ValidationRule):
    """
    Validate that at least one author is present.

    C-CDA requires that documents have at least one author
    to identify who created the document.

    Configuration:
        - require_name: Require author to have a name (default: True)
        - level: Severity level for author issues (default: ERROR)
    """

    def __init__(
        self,
        require_name: bool = True,
        level: ValidationLevel = ValidationLevel.ERROR,
    ):
        """Initialize author presence rule."""
        super().__init__(
            name="author_presence",
            description="Check that at least one author is present",
        )
        self.require_name = require_name
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate author presence."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find authors
        authors = document.xpath("/cda:ClinicalDocument/cda:author", namespaces=ns)

        if not authors:
            issues.append(
                ValidationIssue(
                    level=self.level,
                    message="Document must have at least one author",
                    code="missing_author",
                    location="/ClinicalDocument",
                )
            )
            return issues

        if self.require_name:
            for idx, author in enumerate(authors, 1):
                names = author.xpath(
                    ".//cda:assignedAuthor/cda:assignedPerson/cda:name",
                    namespaces=ns,
                )
                if not names:
                    issues.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message=f"Author {idx} is missing a name",
                            code="missing_author_name",
                            location=f"/ClinicalDocument/author[{idx}]",
                        )
                    )

        return issues


class CustodianPresenceRule(ValidationRule):
    """
    Validate that a custodian is present.

    C-CDA requires documents to identify the organization
    responsible for maintaining the document.

    Configuration:
        - require_organization_name: Require org name (default: True)
        - level: Severity level for custodian issues (default: ERROR)
    """

    def __init__(
        self,
        require_organization_name: bool = True,
        level: ValidationLevel = ValidationLevel.ERROR,
    ):
        """Initialize custodian presence rule."""
        super().__init__(
            name="custodian_presence",
            description="Check that a custodian is present",
        )
        self.require_organization_name = require_organization_name
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate custodian presence."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find custodian
        custodians = cast(
            List[etree._Element],
            document.xpath("/cda:ClinicalDocument/cda:custodian", namespaces=ns),
        )

        if not custodians:
            issues.append(
                ValidationIssue(
                    level=self.level,
                    message="Document must have a custodian",
                    code="missing_custodian",
                    location="/ClinicalDocument",
                )
            )
            return issues

        if self.require_organization_name:
            org_names = custodians[0].xpath(
                ".//cda:representedCustodianOrganization/cda:name/text()",
                namespaces=ns,
            )
            if not org_names or not any(n.strip() for n in org_names):
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="Custodian organization name is missing or empty",
                        code="missing_custodian_name",
                        location="/ClinicalDocument/custodian",
                    )
                )

        return issues


class SectionCountRule(ValidationRule):
    """
    Validate minimum/maximum number of sections.

    Useful for ensuring documents have meaningful content.

    Configuration:
        - min_sections: Minimum number of sections (default: 1)
        - max_sections: Maximum number of sections (default: None)
        - level: Severity level for count issues (default: WARNING)
    """

    def __init__(
        self,
        min_sections: int = 1,
        max_sections: Optional[int] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """Initialize section count rule."""
        super().__init__(
            name="section_count",
            description=f"Check that document has at least {min_sections} sections",
        )
        self.min_sections = min_sections
        self.max_sections = max_sections
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate section count."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Count sections
        sections = document.xpath("//cda:section", namespaces=ns)
        count = len(sections)

        if count < self.min_sections:
            issues.append(
                ValidationIssue(
                    level=self.level,
                    message=f"Document has {count} sections, minimum is {self.min_sections}",
                    code="too_few_sections",
                    location="//component/structuredBody",
                )
            )

        if self.max_sections and count > self.max_sections:
            issues.append(
                ValidationIssue(
                    level=self.level,
                    message=f"Document has {count} sections, maximum is {self.max_sections}",
                    code="too_many_sections",
                    location="//component/structuredBody",
                )
            )

        return issues


class VitalSignRangeRule(ValidationRule):
    """
    Validate vital signs are within reasonable ranges.

    Checks common vital signs against clinical ranges to catch
    data entry errors or unit conversion issues.

    Configuration:
        - ranges: Dict of LOINC codes to (min, max) tuples
        - level: Severity level for out-of-range values (default: WARNING)
    """

    # Common vital sign LOINC codes and reasonable ranges
    DEFAULT_RANGES = {
        "8480-6": (50, 250),  # Systolic BP (mmHg)
        "8462-4": (30, 150),  # Diastolic BP (mmHg)
        "8867-4": (40, 200),  # Heart rate (bpm)
        "9279-1": (8, 40),  # Respiratory rate (breaths/min)
        "8310-5": (35.0, 42.0),  # Body temperature (Celsius)
        "8331-1": (90, 108),  # Oral temperature (F)
        "29463-7": (50, 500),  # Body weight (kg)
        "8302-2": (50, 250),  # Body height (cm)
    }

    def __init__(
        self,
        ranges: Optional[dict] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """Initialize vital sign range rule."""
        super().__init__(
            name="vital_sign_range",
            description="Check that vital signs are within reasonable ranges",
        )
        self.ranges = ranges or self.DEFAULT_RANGES
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate vital sign ranges."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find all observations
        observations = document.xpath("//cda:observation", namespaces=ns)

        for obs in observations:
            # Get observation code
            codes = obs.xpath("cda:code/@code", namespaces=ns)
            if not codes:
                continue

            code = codes[0]
            if code not in self.ranges:
                continue

            min_val, max_val = self.ranges[code]

            # Get observation value
            values = obs.xpath("cda:value/@value", namespaces=ns)
            if not values:
                continue

            try:
                value = float(values[0])
                if value < min_val or value > max_val:
                    code_display = obs.xpath("cda:code/@displayName", namespaces=ns)
                    display = code_display[0] if code_display else code

                    issues.append(
                        ValidationIssue(
                            level=self.level,
                            message=f"{display} value {value} is outside range [{min_val}, {max_val}]",
                            code="vital_sign_out_of_range",
                            location=f"//observation[code/@code='{code}']/value",
                        )
                    )
            except ValueError:
                # Invalid numeric value - skip
                pass

        return issues


class AllergyStatusRule(ValidationRule):
    """
    Validate allergy status codes are valid.

    Ensures allergy observations use proper status codes
    from the allowed value set.

    Configuration:
        - allowed_statuses: Set of allowed status codes
        - level: Severity level for invalid statuses (default: WARNING)
    """

    VALID_STATUSES = {
        "55561003",  # Active
        "73425007",  # Inactive
        "413322009",  # Resolved
    }

    def __init__(
        self,
        allowed_statuses: Optional[Set[str]] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """Initialize allergy status rule."""
        super().__init__(
            name="allergy_status",
            description="Check that allergy status codes are valid",
        )
        self.allowed_statuses = allowed_statuses or self.VALID_STATUSES
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate allergy statuses."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find allergy observations (template 2.16.840.1.113883.10.20.22.4.7)
        allergies = document.xpath(
            "//cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.22.4.7']",
            namespaces=ns,
        )

        for idx, allergy in enumerate(allergies, 1):
            status_codes = cast(
                List[str],
                allergy.xpath(
                    "cda:entryRelationship/cda:observation/cda:value/@code",
                    namespaces=ns,
                ),
            )

            if status_codes and status_codes[0] not in self.allowed_statuses:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Allergy {idx} has invalid status code: {status_codes[0]}",
                        code="invalid_allergy_status",
                        location=f"//observation[{idx}]/entryRelationship/observation/value",
                    )
                )

        return issues


class ProblemStatusRule(ValidationRule):
    """
    Validate problem status codes are valid.

    Ensures problem observations use proper status codes
    from the allowed value set.

    Configuration:
        - allowed_statuses: Set of allowed status codes
        - level: Severity level for invalid statuses (default: WARNING)
    """

    VALID_STATUSES = {
        "55561003",  # Active
        "73425007",  # Inactive
        "413322009",  # Resolved
    }

    def __init__(
        self,
        allowed_statuses: Optional[Set[str]] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """Initialize problem status rule."""
        super().__init__(
            name="problem_status",
            description="Check that problem status codes are valid",
        )
        self.allowed_statuses = allowed_statuses or self.VALID_STATUSES
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate problem statuses."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find problem observations (template 2.16.840.1.113883.10.20.22.4.4)
        problems = document.xpath(
            "//cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.22.4.4']",
            namespaces=ns,
        )

        for idx, problem in enumerate(problems, 1):
            status_codes = cast(
                List[str],
                problem.xpath(
                    "cda:entryRelationship/cda:observation/cda:value/@code",
                    namespaces=ns,
                ),
            )

            if status_codes and status_codes[0] not in self.allowed_statuses:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Problem {idx} has invalid status code: {status_codes[0]}",
                        code="invalid_problem_status",
                        location=f"//observation[{idx}]/entryRelationship/observation/value",
                    )
                )

        return issues


class ContactInfoPresenceRule(ValidationRule):
    """
    Validate that patient has contact information.

    Ensures patient record includes telecom (phone/email) and/or
    address information for patient communication.

    Configuration:
        - require_telecom: Require at least one telecom (default: True)
        - require_address: Require at least one address (default: True)
        - level: Severity level for missing contact info (default: WARNING)
    """

    def __init__(
        self,
        require_telecom: bool = True,
        require_address: bool = True,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """Initialize contact info presence rule."""
        super().__init__(
            name="contact_info_presence",
            description="Check that patient has contact information",
        )
        self.require_telecom = require_telecom
        self.require_address = require_address
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate contact info presence."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        patient_role = cast(
            List[etree._Element],
            document.xpath("//cda:recordTarget/cda:patientRole", namespaces=ns),
        )

        if not patient_role:
            return issues

        role = patient_role[0]

        if self.require_telecom:
            telecoms = role.xpath("cda:telecom", namespaces=ns)
            if not telecoms:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message="Patient is missing contact telecom (phone/email)",
                        code="missing_patient_telecom",
                        location="//recordTarget/patientRole",
                    )
                )

        if self.require_address:
            addresses = role.xpath("cda:addr", namespaces=ns)
            if not addresses:
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message="Patient is missing contact address",
                        code="missing_patient_address",
                        location="//recordTarget/patientRole",
                    )
                )

        return issues
