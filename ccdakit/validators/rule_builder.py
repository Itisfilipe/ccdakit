"""Rule builder utility for creating custom validation rules without subclassing."""

from typing import Callable, List, Optional, cast

from lxml import etree

from ..core.validation import ValidationIssue, ValidationLevel
from .rules import ValidationRule


class FunctionBasedRule(ValidationRule):
    """
    Validation rule based on a callable function.

    This allows creating simple rules without subclassing ValidationRule.

    Example:
        def check_title(doc):
            ns = {"cda": "urn:hl7-org:v3"}
            titles = doc.xpath("//cda:title/text()", namespaces=ns)
            if not titles:
                return ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message="Document is missing title",
                    code="missing_title"
                )
            return None

        rule = FunctionBasedRule("has_title", "Check document has title", check_title)
    """

    def __init__(
        self,
        name: str,
        description: str,
        func: Callable[[etree._Element], Optional[ValidationIssue | List[ValidationIssue]]],
    ):
        """
        Initialize function-based rule.

        Args:
            name: Unique identifier for the rule
            description: Human-readable description
            func: Function that takes document and returns ValidationIssue(s) or None
        """
        super().__init__(name, description)
        self.func = func

    def validate(self, document: etree._Element) -> List[ValidationIssue]:
        """Apply function to document."""
        result = self.func(document)

        if result is None:
            return []
        elif isinstance(result, ValidationIssue):
            return [result]
        elif isinstance(result, list):
            return result
        else:
            raise TypeError(
                f"Rule function must return None, ValidationIssue, or List[ValidationIssue], "
                f"got {type(result).__name__}"
            )


class RuleBuilder:
    """
    Fluent API for building validation rules.

    Provides convenient methods for creating common validation rules
    without writing full classes.

    Example:
        # Simple lambda rule
        rule = RuleBuilder.create(
            "section_count",
            "Check minimum sections",
            lambda doc: len(doc.xpath("//cda:section", namespaces={"cda": "urn:hl7-org:v3"})) >= 3
        )

        # XPath-based rule
        rule = RuleBuilder.xpath_exists(
            "patient_id",
            "//cda:recordTarget/cda:patientRole/cda:id",
            error_message="Patient ID is missing"
        )

        # XPath count rule
        rule = RuleBuilder.xpath_count(
            "min_sections",
            "//cda:section",
            min_count=2,
            error_message="Document must have at least 2 sections"
        )
    """

    @staticmethod
    def create(
        name: str,
        description: str,
        predicate: Callable[[etree._Element], bool],
        error_message: str = "Validation failed",
        level: ValidationLevel = ValidationLevel.ERROR,
        code: Optional[str] = None,
    ) -> ValidationRule:
        """
        Create rule from a boolean predicate function.

        Args:
            name: Rule name
            description: Rule description
            predicate: Function that returns True if valid, False if invalid
            error_message: Message to show when validation fails
            level: Severity level
            code: Error code

        Returns:
            ValidationRule instance

        Example:
            rule = RuleBuilder.create(
                "has_sections",
                "Document must have sections",
                lambda doc: len(doc.xpath("//cda:section", namespaces={"cda": "urn:hl7-org:v3"})) > 0,
                error_message="Document has no sections"
            )
        """

        def validation_func(document: etree._Element) -> Optional[ValidationIssue]:
            is_valid = predicate(document)
            if not is_valid:
                return ValidationIssue(
                    level=level,
                    message=error_message,
                    code=code or f"rule_{name}",
                )
            return None

        return FunctionBasedRule(name, description, validation_func)

    @staticmethod
    def xpath_exists(
        name: str,
        xpath: str,
        error_message: Optional[str] = None,
        level: ValidationLevel = ValidationLevel.ERROR,
        namespaces: Optional[dict] = None,
    ) -> ValidationRule:
        """
        Create rule that checks if XPath returns at least one result.

        Args:
            name: Rule name
            xpath: XPath expression
            error_message: Message when XPath returns no results
            level: Severity level
            namespaces: XML namespaces (defaults to {"cda": "urn:hl7-org:v3"})

        Returns:
            ValidationRule instance

        Example:
            rule = RuleBuilder.xpath_exists(
                "has_patient_id",
                "//cda:recordTarget/cda:patientRole/cda:id",
                error_message="Patient ID is required"
            )
        """
        ns = namespaces or {"cda": "urn:hl7-org:v3"}
        error_msg = error_message or f"XPath '{xpath}' returned no results"

        def validation_func(document: etree._Element) -> Optional[ValidationIssue]:
            results = document.xpath(xpath, namespaces=ns)
            if not results:
                return ValidationIssue(
                    level=level,
                    message=error_msg,
                    code=f"xpath_not_found_{name}",
                    location=xpath,
                )
            return None

        return FunctionBasedRule(name, f"Check XPath exists: {xpath}", validation_func)

    @staticmethod
    def xpath_count(
        name: str,
        xpath: str,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None,
        exact_count: Optional[int] = None,
        error_message: Optional[str] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
        namespaces: Optional[dict] = None,
    ) -> ValidationRule:
        """
        Create rule that checks XPath result count.

        Args:
            name: Rule name
            xpath: XPath expression
            min_count: Minimum expected count
            max_count: Maximum expected count
            exact_count: Exact expected count
            error_message: Custom error message
            level: Severity level
            namespaces: XML namespaces

        Returns:
            ValidationRule instance

        Example:
            rule = RuleBuilder.xpath_count(
                "section_count",
                "//cda:section",
                min_count=2,
                max_count=20,
                error_message="Document should have 2-20 sections"
            )
        """
        ns = namespaces or {"cda": "urn:hl7-org:v3"}

        def validation_func(document: etree._Element) -> Optional[ValidationIssue]:
            results = document.xpath(xpath, namespaces=ns)
            count = len(results)

            if exact_count is not None and count != exact_count:
                msg = (
                    error_message
                    or f"XPath '{xpath}' returned {count} results, expected exactly {exact_count}"
                )
                return ValidationIssue(
                    level=level,
                    message=msg,
                    code=f"xpath_count_mismatch_{name}",
                    location=xpath,
                )

            if min_count is not None and count < min_count:
                msg = (
                    error_message
                    or f"XPath '{xpath}' returned {count} results, minimum is {min_count}"
                )
                return ValidationIssue(
                    level=level,
                    message=msg,
                    code=f"xpath_count_too_low_{name}",
                    location=xpath,
                )

            if max_count is not None and count > max_count:
                msg = (
                    error_message
                    or f"XPath '{xpath}' returned {count} results, maximum is {max_count}"
                )
                return ValidationIssue(
                    level=level,
                    message=msg,
                    code=f"xpath_count_too_high_{name}",
                    location=xpath,
                )

            return None

        desc = f"Check XPath count: {xpath}"
        if exact_count:
            desc += f" (exactly {exact_count})"
        elif min_count and max_count:
            desc += f" ({min_count}-{max_count})"
        elif min_count:
            desc += f" (min {min_count})"
        elif max_count:
            desc += f" (max {max_count})"

        return FunctionBasedRule(name, desc, validation_func)

    @staticmethod
    def xpath_value_matches(
        name: str,
        xpath: str,
        pattern: str,
        error_message: Optional[str] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
        namespaces: Optional[dict] = None,
    ) -> ValidationRule:
        """
        Create rule that checks XPath result matches a regex pattern.

        Args:
            name: Rule name
            xpath: XPath expression
            pattern: Regex pattern to match
            error_message: Custom error message
            level: Severity level
            namespaces: XML namespaces

        Returns:
            ValidationRule instance

        Example:
            rule = RuleBuilder.xpath_value_matches(
                "valid_date_format",
                "//cda:effectiveTime/@value",
                r"^\\d{8}$",
                error_message="Date must be in YYYYMMDD format"
            )
        """
        import re

        ns = namespaces or {"cda": "urn:hl7-org:v3"}
        regex = re.compile(pattern)

        def validation_func(document: etree._Element) -> List[ValidationIssue]:
            results = document.xpath(xpath, namespaces=ns)
            issues = []

            for idx, value in enumerate(results, 1):
                text = str(value)
                if not regex.match(text):
                    msg = (
                        error_message
                        or f"Value '{text}' at {xpath}[{idx}] does not match pattern '{pattern}'"
                    )
                    issues.append(
                        ValidationIssue(
                            level=level,
                            message=msg,
                            code=f"xpath_value_mismatch_{name}",
                            location=f"{xpath}[{idx}]",
                        )
                    )

            return issues

        return FunctionBasedRule(
            name, f"Check XPath value matches pattern: {xpath}", validation_func
        )

    @staticmethod
    def xpath_value_in_set(
        name: str,
        xpath: str,
        allowed_values: set | list,
        error_message: Optional[str] = None,
        level: ValidationLevel = ValidationLevel.WARNING,
        namespaces: Optional[dict] = None,
    ) -> ValidationRule:
        """
        Create rule that checks XPath results are in allowed set.

        Args:
            name: Rule name
            xpath: XPath expression
            allowed_values: Set or list of allowed values
            error_message: Custom error message
            level: Severity level
            namespaces: XML namespaces

        Returns:
            ValidationRule instance

        Example:
            rule = RuleBuilder.xpath_value_in_set(
                "valid_gender",
                "//cda:patient/cda:administrativeGenderCode/@code",
                allowed_values={"M", "F", "UN"},
                error_message="Gender code must be M, F, or UN"
            )
        """
        ns = namespaces or {"cda": "urn:hl7-org:v3"}
        allowed_set = set(allowed_values)

        def validation_func(document: etree._Element) -> List[ValidationIssue]:
            results = cast(List[str], document.xpath(xpath, namespaces=ns))
            issues = []

            for idx, value in enumerate(results, 1):
                text = str(value)
                if text not in allowed_set:
                    msg = (
                        error_message
                        or f"Value '{text}' at {xpath}[{idx}] not in allowed set: {allowed_set}"
                    )
                    issues.append(
                        ValidationIssue(
                            level=level,
                            message=msg,
                            code=f"xpath_value_not_allowed_{name}",
                            location=f"{xpath}[{idx}]",
                        )
                    )

            return issues

        return FunctionBasedRule(
            name, f"Check XPath value in allowed set: {xpath}", validation_func
        )

    @staticmethod
    def composite(
        name: str,
        description: str,
        rules: List[ValidationRule],
        all_must_pass: bool = True,
    ) -> ValidationRule:
        """
        Create composite rule that combines multiple rules.

        Args:
            name: Rule name
            description: Rule description
            rules: List of rules to combine
            all_must_pass: If True, all rules must pass. If False, at least one must pass.

        Returns:
            ValidationRule instance

        Example:
            rule = RuleBuilder.composite(
                "patient_info",
                "Patient must have name and ID",
                rules=[
                    RuleBuilder.xpath_exists("name", "//cda:patient/cda:name"),
                    RuleBuilder.xpath_exists("id", "//cda:patientRole/cda:id")
                ],
                all_must_pass=True
            )
        """

        def validation_func(document: etree._Element) -> List[ValidationIssue]:
            all_issues = []

            for rule in rules:
                issues = rule.validate(document)
                all_issues.extend(issues)

            if all_must_pass:
                # Return all issues
                return all_issues
            else:
                # At least one must pass - if all have issues, return them
                if len(all_issues) == sum(len(r.validate(document)) for r in rules):
                    # All rules failed
                    return [
                        ValidationIssue(
                            level=ValidationLevel.ERROR,
                            message=f"Composite rule '{name}' failed: none of the {len(rules)} sub-rules passed",
                            code=f"composite_all_failed_{name}",
                        )
                    ]
                return []

        return FunctionBasedRule(name, description, validation_func)
