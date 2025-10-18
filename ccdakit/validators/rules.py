"""Custom validation rules engine for organization-specific business logic."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union, cast

from lxml import etree

from ..core.validation import ValidationIssue, ValidationLevel, ValidationResult


class ValidationRule(ABC):
    """
    Base class for custom validation rules.

    Example:
        class MyCustomRule(ValidationRule):
            def __init__(self):
                super().__init__(
                    name="my_custom_rule",
                    description="Validates custom business logic"
                )

            def validate(self, document: etree._Element) -> List[ValidationIssue]:
                issues = []
                # Implement validation logic
                return issues
    """

    def __init__(self, name: str, description: str):
        """
        Initialize validation rule.

        Args:
            name: Unique identifier for the rule
            description: Human-readable description of what the rule checks
        """
        self.name = name
        self.description = description

    @abstractmethod
    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """
        Apply rule to document.

        Args:
            document: Parsed C-CDA XML document element

        Returns:
            List of validation issues found (empty list if valid)
        """
        raise NotImplementedError(f"Rule '{self.name}' must implement validate()")

    def __repr__(self) -> str:
        """String representation of rule."""
        return f"<ValidationRule: {self.name}>"


class RulesEngine:
    """
    Engine for running custom validation rules.

    The RulesEngine allows you to compose multiple validation rules
    and run them against C-CDA documents.

    Example:
        engine = RulesEngine()
        engine.add_rule(RequiredSectionsRule(["problems", "medications"]))
        engine.add_rule(DateConsistencyRule())

        result = engine.validate(document)
        if not result.is_valid:
            print(f"Found {len(result.errors)} errors")
    """

    def __init__(self):
        """Initialize rules engine with empty rule set."""
        self._rules: List[ValidationRule] = []

    def add_rule(self, rule: ValidationRule) -> None:
        """
        Add validation rule to engine.

        Args:
            rule: ValidationRule instance to add

        Raises:
            TypeError: If rule is not a ValidationRule instance
        """
        if not isinstance(rule, ValidationRule):
            raise TypeError(f"Expected ValidationRule, got {type(rule).__name__}")
        self._rules.append(rule)

    def remove_rule(self, name: str) -> bool:
        """
        Remove validation rule by name.

        Args:
            name: Name of the rule to remove

        Returns:
            True if rule was removed, False if not found
        """
        initial_count = len(self._rules)
        self._rules = [r for r in self._rules if r.name != name]
        return len(self._rules) < initial_count

    def get_rule(self, name: str) -> Optional[ValidationRule]:
        """
        Get rule by name.

        Args:
            name: Name of the rule to retrieve

        Returns:
            ValidationRule if found, None otherwise
        """
        for rule in self._rules:
            if rule.name == name:
                return rule
        return None

    def list_rules(self) -> List[str]:
        """
        Get list of all rule names.

        Returns:
            List of rule names in order they were added
        """
        return [rule.name for rule in self._rules]

    def validate(self, document: Union[etree._Element, str, bytes, Path]) -> ValidationResult:
        """
        Run all rules against document.

        Args:
            document: Document to validate. Can be:
                - etree._Element: Parsed XML element
                - str: XML string or file path
                - bytes: XML bytes
                - Path: Path to XML file

        Returns:
            ValidationResult with all issues categorized by level

        Raises:
            FileNotFoundError: If file path doesn't exist
            etree.XMLSyntaxError: If document is not well-formed XML
        """
        # Parse document if needed
        doc_element = self._parse_document(document)

        # Collect all issues from all rules
        all_issues: List[ValidationIssue] = []
        for rule in self._rules:
            try:
                issues = rule.validate(doc_element)
                all_issues.extend(issues)
            except Exception as e:
                # If rule throws an exception, add it as an error
                all_issues.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message=f"Rule '{rule.name}' failed: {str(e)}",
                        code=f"rule_error_{rule.name}",
                    )
                )

        # Categorize issues by level
        errors = [i for i in all_issues if i.level == ValidationLevel.ERROR]
        warnings = [i for i in all_issues if i.level == ValidationLevel.WARNING]
        infos = [i for i in all_issues if i.level == ValidationLevel.INFO]

        return ValidationResult(errors=errors, warnings=warnings, infos=infos)

    def _parse_document(self, document: Union[etree._Element, str, bytes, Path]) -> etree._Element:
        """
        Parse document into an lxml Element.

        Args:
            document: Document in various formats

        Returns:
            Parsed XML element

        Raises:
            FileNotFoundError: If file path doesn't exist
            etree.XMLSyntaxError: If document is not well-formed XML
        """
        if isinstance(document, etree._Element):
            return document

        if isinstance(document, Path):
            if not document.exists():
                raise FileNotFoundError(f"File not found: {document}")
            return etree.parse(str(document)).getroot()

        if isinstance(document, str):
            # Try as file path first
            path = Path(document)
            if path.exists():
                return etree.parse(str(path)).getroot()
            # Otherwise parse as XML string
            return etree.fromstring(document.encode("utf-8"))

        if isinstance(document, bytes):
            return etree.fromstring(document)

        raise TypeError(
            f"Unsupported document type: {type(document)}. "
            "Expected etree._Element, str, bytes, or Path"
        )

    def __len__(self) -> int:
        """Get number of rules in engine."""
        return len(self._rules)

    def __repr__(self) -> str:
        """String representation of engine."""
        return f"<RulesEngine: {len(self._rules)} rules>"


# Example custom rules


class RequiredSectionsRule(ValidationRule):
    """
    Validate that required sections are present in the document.

    This rule checks that the document contains all specified section codes.
    Useful for ensuring documents meet organizational requirements.

    Example:
        # Require problems and medications sections
        rule = RequiredSectionsRule(
            required_sections=["11450-4", "10160-0"],  # LOINC codes
            section_names={"11450-4": "Problems", "10160-0": "Medications"}
        )
    """

    def __init__(
        self,
        required_sections: List[str],
        section_names: Optional[dict] = None,
        level: ValidationLevel = ValidationLevel.ERROR,
    ):
        """
        Initialize required sections rule.

        Args:
            required_sections: List of section LOINC codes that must be present
            section_names: Optional mapping of codes to human-readable names
            level: Severity level for missing sections (ERROR or WARNING)
        """
        super().__init__(
            name="required_sections",
            description=f"Check that required sections are present: {', '.join(required_sections)}",
        )
        self.required_sections = required_sections
        self.section_names = section_names or {}
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate required sections are present."""
        issues = []

        # Define namespace
        ns = {"cda": "urn:hl7-org:v3"}

        # Find all section codes in document
        sections = cast(List[str], document.xpath("//cda:section/cda:code/@code", namespaces=ns))

        # Check each required section
        for required_code in self.required_sections:
            if required_code not in sections:
                section_name = self.section_names.get(required_code, required_code)
                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"Required section '{section_name}' (code: {required_code}) is missing",
                        code="missing_required_section",
                        location="//section/code",
                    )
                )

        return issues


class MedicationDosageRule(ValidationRule):
    """
    Validate medication dosages are within reasonable ranges.

    This rule checks that medication dosages fall within configurable
    acceptable ranges to catch data entry errors.

    Example:
        rule = MedicationDosageRule(
            max_dosage=1000.0,  # Maximum single dose
            min_dosage=0.01     # Minimum single dose
        )
    """

    def __init__(
        self,
        max_dosage: float = 10000.0,
        min_dosage: float = 0.001,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """
        Initialize medication dosage rule.

        Args:
            max_dosage: Maximum reasonable dosage value
            min_dosage: Minimum reasonable dosage value
            level: Severity level for dosage issues
        """
        super().__init__(
            name="medication_dosage",
            description=f"Check medication dosages are between {min_dosage} and {max_dosage}",
        )
        self.max_dosage = max_dosage
        self.min_dosage = min_dosage
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate medication dosages."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find all medication dosage values
        dosages = document.xpath(
            "//cda:substanceAdministration/cda:doseQuantity/@value",
            namespaces=ns,
        )

        for idx, dosage_str in enumerate(dosages, 1):
            try:
                dosage = float(dosage_str)
                if dosage > self.max_dosage:
                    issues.append(
                        ValidationIssue(
                            level=self.level,
                            message=f"Medication dosage {dosage} exceeds maximum of {self.max_dosage}",
                            code="dosage_too_high",
                            location=f"//substanceAdministration[{idx}]/doseQuantity",
                        )
                    )
                elif dosage < self.min_dosage:
                    issues.append(
                        ValidationIssue(
                            level=self.level,
                            message=f"Medication dosage {dosage} below minimum of {self.min_dosage}",
                            code="dosage_too_low",
                            location=f"//substanceAdministration[{idx}]/doseQuantity",
                        )
                    )
            except ValueError:
                issues.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message=f"Invalid dosage value: '{dosage_str}' (not a number)",
                        code="invalid_dosage_format",
                        location=f"//substanceAdministration[{idx}]/doseQuantity",
                    )
                )

        return issues


class DateConsistencyRule(ValidationRule):
    """
    Validate dates are logically consistent.

    This rule checks that dates in the document are in proper chronological
    order and within reasonable bounds (e.g., not in the future).

    Example:
        rule = DateConsistencyRule(
            allow_future_dates=False,
            max_years_past=150
        )
    """

    def __init__(
        self,
        allow_future_dates: bool = False,
        max_years_past: int = 150,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """
        Initialize date consistency rule.

        Args:
            allow_future_dates: Whether to allow dates in the future
            max_years_past: Maximum years in the past allowed
            level: Severity level for date issues
        """
        super().__init__(
            name="date_consistency",
            description="Check that dates are logically consistent and within reasonable bounds",
        )
        self.allow_future_dates = allow_future_dates
        self.max_years_past = max_years_past
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate date consistency."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        from datetime import datetime

        today = datetime.now()

        # Find all effectiveTime elements with values
        times = document.xpath("//cda:effectiveTime/@value", namespaces=ns)

        for time_str in times:
            try:
                # Parse HL7 datetime format (YYYYMMDD or YYYYMMDDHHmmss)
                if len(time_str) >= 8:
                    date_part = time_str[:8]
                    dt = datetime.strptime(date_part, "%Y%m%d")

                    # Check if future date
                    if not self.allow_future_dates and dt > today:
                        issues.append(
                            ValidationIssue(
                                level=self.level,
                                message=f"Date {date_part} is in the future",
                                code="future_date",
                                location="//effectiveTime",
                            )
                        )

                    # Check if too far in past
                    years_diff = (today - dt).days / 365.25
                    if years_diff > self.max_years_past:
                        issues.append(
                            ValidationIssue(
                                level=self.level,
                                message=f"Date {date_part} is more than {self.max_years_past} years in the past",
                                code="date_too_old",
                                location="//effectiveTime",
                            )
                        )
            except ValueError:
                # Invalid date format - just skip, XSD validator will catch this
                pass

        return issues


class CodeSystemConsistencyRule(ValidationRule):
    """
    Validate codes use correct code systems.

    This rule ensures that codes are from their expected code systems
    based on the element type.

    Example:
        rule = CodeSystemConsistencyRule(
            expected_systems={
                "problem": "2.16.840.1.113883.6.96",  # SNOMED CT
                "medication": "2.16.840.1.113883.6.88"  # RxNorm
            }
        )
    """

    def __init__(
        self,
        expected_systems: Optional[dict] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """
        Initialize code system consistency rule.

        Args:
            expected_systems: Mapping of element types to expected OIDs
            level: Severity level for code system issues
        """
        super().__init__(
            name="code_system_consistency",
            description="Check that codes use correct code systems",
        )
        self.expected_systems = expected_systems or {
            "problem": "2.16.840.1.113883.6.96",  # SNOMED CT
            "allergy": "2.16.840.1.113883.6.96",  # SNOMED CT
            "medication": "2.16.840.1.113883.6.88",  # RxNorm
            "procedure": "2.16.840.1.113883.6.96",  # SNOMED CT or CPT
        }
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate code system usage."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Check problem codes (in observation acts)
        if "problem" in self.expected_systems:
            expected_oid = self.expected_systems["problem"]
            problem_codes = document.xpath(
                "//cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.22.4.4']/cda:value/@codeSystem",
                namespaces=ns,
            )
            for idx, code_system in enumerate(problem_codes, 1):
                if code_system != expected_oid:
                    issues.append(
                        ValidationIssue(
                            level=self.level,
                            message=f"Problem code uses code system {code_system}, expected {expected_oid} (SNOMED CT)",
                            code="incorrect_code_system",
                            location=f"//observation[{idx}]/value",
                        )
                    )

        return issues


class NarrativePresenceRule(ValidationRule):
    """
    Validate that sections have narrative text.

    C-CDA requires that each section contains human-readable text
    in addition to structured entries.

    Example:
        rule = NarrativePresenceRule(
            require_narrative=True,
            min_length=10
        )
    """

    def __init__(
        self,
        require_narrative: bool = True,
        min_length: int = 1,
        level: ValidationLevel = ValidationLevel.WARNING,
    ):
        """
        Initialize narrative presence rule.

        Args:
            require_narrative: Whether to require narrative text
            min_length: Minimum length of narrative text
            level: Severity level for missing narrative
        """
        super().__init__(
            name="narrative_presence",
            description="Check that sections have narrative text",
        )
        self.require_narrative = require_narrative
        self.min_length = min_length
        self.level = level

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Validate narrative presence."""
        issues = []
        ns = {"cda": "urn:hl7-org:v3"}

        # Find all sections
        sections = document.xpath("//cda:section", namespaces=ns)

        for idx, section in enumerate(sections, 1):
            # Check if section has text element
            text_elements = section.xpath("cda:text", namespaces=ns)

            if not text_elements and self.require_narrative:
                # Get section title or code for better error message
                title = section.xpath("cda:title/text()", namespaces=ns)
                title_str = title[0] if title else f"Section {idx}"

                issues.append(
                    ValidationIssue(
                        level=self.level,
                        message=f"{title_str} is missing narrative text",
                        code="missing_narrative",
                        location=f"//section[{idx}]",
                    )
                )
            elif text_elements:
                # Check narrative length
                text_content = etree.tostring(
                    text_elements[0], method="text", encoding="unicode"
                ).strip()

                if len(text_content) < self.min_length:
                    title = section.xpath("cda:title/text()", namespaces=ns)
                    title_str = title[0] if title else f"Section {idx}"

                    issues.append(
                        ValidationIssue(
                            level=self.level,
                            message=f"{title_str} narrative text is too short (min: {self.min_length} chars)",
                            code="narrative_too_short",
                            location=f"//section[{idx}]/text",
                        )
                    )

        return issues
