"""Parser for Schematron validation errors to make them more human-readable."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class ParsedError:
    """Parsed Schematron validation error with enhanced readability."""

    # Original error message
    original_message: str

    # Simplified location path (e.g., "ClinicalDocument > component > section[2] > entry[1]")
    simplified_path: str

    # Full XPath for technical reference
    full_xpath: str

    # Error description (the SHALL/SHOULD requirement)
    requirement: str

    # Template ID if found
    template_id: str | None

    # CONF number if found
    conf_number: str | None

    # Template name/description if available
    template_name: str | None

    # Severity level
    severity: str  # "error" or "warning"

    # Suggestions for fixing
    suggestions: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "original_message": self.original_message,
            "simplified_path": self.simplified_path,
            "full_xpath": self.full_xpath,
            "requirement": self.requirement,
            "template_id": self.template_id,
            "conf_number": self.conf_number,
            "template_name": self.template_name,
            "severity": self.severity,
            "suggestions": self.suggestions,
        }


class SchematronErrorParser:
    """Parser for Schematron validation errors."""

    # Common template names for quick lookup with documentation links
    # Comprehensive mapping of C-CDA R2.1 template IDs to documentation
    TEMPLATE_INFO = {
        # === SECTIONS ===
        # Core Clinical Sections
        "2.16.840.1.113883.10.20.22.2.1": {
            "name": "Medications Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#medications-section",
        },
        "2.16.840.1.113883.10.20.22.2.5": {
            "name": "Problems Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#problems-section",
        },
        "2.16.840.1.113883.10.20.22.2.6": {
            "name": "Allergies Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#allergies-section",
        },
        "2.16.840.1.113883.10.20.22.2.2": {
            "name": "Immunizations Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#immunizations-section",
        },
        "2.16.840.1.113883.10.20.22.2.4": {
            "name": "Vital Signs Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#vital-signs-section",
        },
        "2.16.840.1.113883.10.20.22.2.7": {
            "name": "Procedures Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#procedures-section",
        },
        "2.16.840.1.113883.10.20.22.2.3": {
            "name": "Results Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#results-section",
        },
        "2.16.840.1.113883.10.20.22.2.17": {
            "name": "Social History Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#social-history-section",
        },
        "2.16.840.1.113883.10.20.22.2.22": {
            "name": "Encounters Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#encounters-section",
        },
        # Patient History & Assessments
        "2.16.840.1.113883.10.20.22.2.15": {
            "name": "Family History Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#family-history-section",
        },
        "2.16.840.1.113883.10.20.22.2.20": {
            "name": "Past Medical History Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#past-medical-history-section",
        },
        "2.16.840.1.113883.10.20.22.2.56": {
            "name": "Health Status Evaluations Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#health-status-evaluations-section",
        },
        "2.16.840.1.113883.10.20.22.2.10": {
            "name": "Physical Exam Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#physical-exam-section",
        },
        "2.16.840.1.113883.10.20.22.2.14": {
            "name": "Functional Status Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#functional-status-section",
        },
        "2.16.840.1.113883.10.20.22.2.18": {
            "name": "Mental Status Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#mental-status-section",
        },
        # Care Planning & Goals
        "2.16.840.1.113883.10.20.22.2.60": {
            "name": "Goals Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#goals-section",
        },
        "2.16.840.1.113883.10.20.22.2.10": {
            "name": "Plan of Treatment Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#plan-of-treatment-section",
        },
        "2.16.840.1.113883.10.20.22.2.9": {
            "name": "Assessment and Plan Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#assessment-and-plan-section",
        },
        "2.16.840.1.113883.10.20.22.2.58": {
            "name": "Health Concerns Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#health-concerns-section",
        },
        "2.16.840.1.113883.10.20.21.2.3": {
            "name": "Interventions Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#interventions-section",
        },
        "2.16.840.1.113883.10.20.22.2.45": {
            "name": "Instructions Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#instructions-section",
        },
        # Hospital & Admission
        "2.16.840.1.113883.10.20.22.2.43": {
            "name": "Admission Diagnosis Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#admission-diagnosis-section",
        },
        "2.16.840.1.113883.10.20.22.2.44": {
            "name": "Admission Medications Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#admission-medications-section",
        },
        "2.16.840.1.113883.10.20.22.2.25": {
            "name": "Anesthesia Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#anesthesia-section",
        },
        "1.3.6.1.4.1.19376.1.5.3.1.3.5": {
            "name": "Hospital Course Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#hospital-course-section",
        },
        "2.16.840.1.113883.10.20.22.2.12": {
            "name": "Reason for Visit Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#reason-for-visit-section",
        },
        "2.16.840.1.113883.10.20.22.2.13": {
            "name": "Chief Complaint and Reason for Visit Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#chief-complaint-reason-for-visit-section",
        },
        # Discharge & Summary
        "2.16.840.1.113883.10.20.22.2.24": {
            "name": "Discharge Diagnosis Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#discharge-diagnosis-section",
        },
        "2.16.840.1.113883.10.20.22.2.11": {
            "name": "Discharge Medications Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#discharge-medications-section",
        },
        "2.16.840.1.113883.10.20.22.2.16": {
            "name": "Hospital Discharge Studies Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#hospital-discharge-studies-section",
        },
        "2.16.840.1.113883.10.20.22.2.41": {
            "name": "Hospital Discharge Instructions Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#hospital-discharge-instructions-section",
        },
        # Surgical & Operative
        "2.16.840.1.113883.10.20.22.2.34": {
            "name": "Preoperative Diagnosis Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#preoperative-diagnosis-section",
        },
        "2.16.840.1.113883.10.20.22.2.35": {
            "name": "Postoperative Diagnosis Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#postoperative-diagnosis-section",
        },
        "2.16.840.1.113883.10.20.22.2.37": {
            "name": "Complications Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#complications-section",
        },
        # Other Sections
        "2.16.840.1.113883.10.20.22.2.21": {
            "name": "Advance Directives Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#advance-directives-section",
        },
        "2.16.840.1.113883.10.20.22.2.23": {
            "name": "Medical Equipment Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#medical-equipment-section",
        },
        "2.16.840.1.113883.10.20.22.2.38": {
            "name": "Medications Administered Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#medications-administered-section",
        },
        "2.16.840.1.113883.10.20.22.2.57": {
            "name": "Nutrition Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#nutrition-section",
        },
        "2.16.840.1.113883.10.20.22.2.18": {
            "name": "Payers Section",
            "doc_url": "https://docs.ccdakit.com/api/sections/#payers-section",
        },
        # === ENTRIES ===
        # Allergy entries
        "2.16.840.1.113883.10.20.22.4.30": {
            "name": "Allergy Concern Act",
            "doc_url": "https://docs.ccdakit.com/api/sections/#allergies-section",
        },
        "2.16.840.1.113883.10.20.22.4.7": {
            "name": "Allergy Observation",
            "doc_url": "https://docs.ccdakit.com/api/sections/#allergies-section",
        },
        # Problem entries
        "2.16.840.1.113883.10.20.22.4.3": {
            "name": "Problem Concern Act",
            "doc_url": "https://docs.ccdakit.com/api/sections/#problems-section",
        },
        "2.16.840.1.113883.10.20.22.4.4": {
            "name": "Problem Observation",
            "doc_url": "https://docs.ccdakit.com/api/sections/#problems-section",
        },
        # Medication entries
        "2.16.840.1.113883.10.20.22.4.16": {
            "name": "Medication Activity",
            "doc_url": "https://docs.ccdakit.com/api/sections/#medications-section",
        },
        # Vital Signs entries
        "2.16.840.1.113883.10.20.22.4.26": {
            "name": "Vital Signs Organizer",
            "doc_url": "https://docs.ccdakit.com/api/sections/#vital-signs-section",
        },
        "2.16.840.1.113883.10.20.22.4.27": {
            "name": "Vital Signs Observation",
            "doc_url": "https://docs.ccdakit.com/api/sections/#vital-signs-section",
        },
        # Procedure entries
        "2.16.840.1.113883.10.20.22.4.12": {
            "name": "Procedure Activity Act",
            "doc_url": "https://docs.ccdakit.com/api/sections/#procedures-section",
        },
        "2.16.840.1.113883.10.20.22.4.14": {
            "name": "Procedure Activity Procedure",
            "doc_url": "https://docs.ccdakit.com/api/sections/#procedures-section",
        },
        # Result entries
        "2.16.840.1.113883.10.20.22.4.1": {
            "name": "Result Organizer",
            "doc_url": "https://docs.ccdakit.com/api/sections/#results-section",
        },
        "2.16.840.1.113883.10.20.22.4.2": {
            "name": "Result Observation",
            "doc_url": "https://docs.ccdakit.com/api/sections/#results-section",
        },
        # Immunization entries
        "2.16.840.1.113883.10.20.22.4.52": {
            "name": "Immunization Activity",
            "doc_url": "https://docs.ccdakit.com/api/sections/#immunizations-section",
        },
        # Encounter entries
        "2.16.840.1.113883.10.20.22.4.49": {
            "name": "Encounter Activity",
            "doc_url": "https://docs.ccdakit.com/api/sections/#encounters-section",
        },
        # Common/Shared entries
        "2.16.840.1.113883.10.20.22.4.119": {
            "name": "Author Participation",
            "doc_url": "https://docs.ccdakit.com/guides/hl7-guide/#author",
        },
        "2.16.840.1.113883.10.20.22.4.121": {
            "name": "Caregiver Characteristics",
            "doc_url": "https://docs.ccdakit.com/guides/hl7-guide/",
        },
    }

    @staticmethod
    def simplify_xpath(xpath: str) -> str:
        """
        Convert verbose XPath with namespace predicates to simplified readable path.

        Example:
        /*[local-name()='ClinicalDocument']/*[local-name()='component'][1]
        -> ClinicalDocument > component[1]
        """
        if not xpath:
            return ""

        # Pattern to match: *[local-name()='ElementName' and namespace-uri()='...']
        # or just: *[local-name()='ElementName']
        # Using non-greedy matching and handling both single and double quotes
        pattern = r"\*\[local-name\(\)=['\"]([^'\"]+)['\"](?:\s+and\s+namespace-uri\(\)=['\"][^'\"]*['\"])?\]"

        # Split by / to process each segment
        segments = xpath.split("/")
        path_parts = []

        for segment in segments:
            if not segment or segment == "*":
                continue

            # Extract element name
            match = re.search(pattern, segment)
            if match:
                element_name = match.group(1)

                # Check for position predicate (appears after the predicate block)
                # Pattern: ][1] or ][2] etc.
                position_match = re.search(r"\]\[(\d+)\]", segment)
                if position_match:
                    element_name += f"[{position_match.group(1)}]"

                path_parts.append(element_name)
            else:
                # If no match, try to extract any meaningful text
                # This handles simpler XPath expressions
                cleaned = re.sub(r"\[.*?\]", "", segment).strip()
                if cleaned and cleaned != "*":
                    path_parts.append(cleaned)

        return " > ".join(path_parts) if path_parts else xpath

    @staticmethod
    def extract_template_id(message: str) -> str | None:
        """Extract template ID from error message."""
        # Pattern: @root="2.16.840.1.113883..."
        match = re.search(r'@root="([\d.]+)"', message)
        return match.group(1) if match else None

    @staticmethod
    def extract_conf_number(message: str) -> str | None:
        """Extract CONF number from error message."""
        # Pattern: CONF:1098-8583 or (CONF:1098-8583)
        match = re.search(r"\(CONF:([0-9-]+)\)", message) or re.search(r"CONF:([0-9-]+)", message)
        return match.group(1) if match else None

    @staticmethod
    def extract_requirement(message: str) -> str:
        """Extract the SHALL/SHOULD requirement from the error message."""
        # Pattern: ERROR at <xpath>: <requirement> [SCHEMATRON_...]
        # The requirement typically starts with SHALL, SHOULD, MAY, or other keywords
        # Look for ": " followed by these keywords

        # Find the last occurrence of ': ' before the requirement starts
        # The requirement typically starts with SHALL, SHOULD, MAY, etc.
        match = re.search(
            r":\s+((?:SHALL|SHOULD|MAY|MUST|This).*?)(?:\s*\[SCHEMATRON|$)",
            message,
            re.DOTALL | re.IGNORECASE,
        )
        if match:
            return match.group(1).strip()

        # Fallback: try to extract everything after "ERROR at ... :"
        # by looking for the pattern that closes the XPath (the last ']' before ':')
        match = re.search(r"\]:\s+(.+?)(?:\s*\[SCHEMATRON|$)", message, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Last fallback: just remove the prefix and suffix
        cleaned = re.sub(r"^(ERROR|WARNING)\s+at\s+.*?:\s*", "", message)
        cleaned = re.sub(r"\s*\[SCHEMATRON[^\]]*\]\s*$", "", cleaned)
        return cleaned.strip()

    @staticmethod
    def extract_xpath(message: str) -> str:
        """Extract XPath from error message."""
        # Pattern: ERROR at /xpath/here: message
        # The XPath ends at ": " (colon followed by space)
        match = re.match(r"^(?:ERROR|WARNING)\s+at\s+(.*?):\s+", message, re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def determine_severity(message: str) -> str:
        """Determine if error or warning."""
        if message.startswith("WARNING"):
            return "warning"
        return "error"

    @staticmethod
    def generate_suggestions(parsed_error: ParsedError) -> list[str]:
        """Generate helpful suggestions based on the error."""
        suggestions = []

        requirement_lower = parsed_error.requirement.lower()

        # Template ID suggestions
        if "templateid" in requirement_lower:
            if parsed_error.template_id:
                template_name = parsed_error.template_name or "this template"
                suggestions.append(
                    f'Add a <templateId> element with root="{parsed_error.template_id}" to identify {template_name}'
                )
            else:
                suggestions.append(
                    "Add the required <templateId> element with the specified @root attribute"
                )

        # Cardinality suggestions
        if "exactly one [1..1]" in requirement_lower:
            suggestions.append("Ensure this element appears exactly once (no more, no less)")
        elif "at least one [1..*]" in requirement_lower:
            suggestions.append("Add at least one instance of this element")
        elif "[0..1]" in requirement_lower:
            suggestions.append("This element is optional but can appear at most once")

        # Code system suggestions
        if "valueset" in requirement_lower or "code system" in requirement_lower:
            suggestions.append(
                "Check that the code value comes from the specified value set or code system"
            )

        # Attribute suggestions
        if "@" in parsed_error.requirement:
            attr_matches = re.findall(r'@(\w+)="([^"]+)"', parsed_error.requirement)
            for attr_name, attr_value in attr_matches:
                suggestions.append(f'Set attribute {attr_name}="{attr_value}"')

        # Add documentation link if available
        if parsed_error.template_id:
            template_info = SchematronErrorParser.TEMPLATE_INFO.get(parsed_error.template_id)
            if template_info and template_info.get("doc_url"):
                suggestions.append(f"See documentation: {template_info['doc_url']}")

        # Fallback to docs home if no specific link
        if not any("docs.ccdakit.com" in s for s in suggestions):
            suggestions.append("See C-CDA guide: https://docs.ccdakit.com/guides/hl7-guide/")

        return suggestions

    @classmethod
    def parse_error(cls, error_message: str) -> ParsedError:
        """
        Parse a Schematron error message into structured components.

        Args:
            error_message: The raw error message from Schematron validation

        Returns:
            ParsedError with all extracted information
        """
        # Extract components
        xpath = cls.extract_xpath(error_message)
        simplified_path = cls.simplify_xpath(xpath)
        requirement = cls.extract_requirement(error_message)
        template_id = cls.extract_template_id(error_message)
        conf_number = cls.extract_conf_number(error_message)
        severity = cls.determine_severity(error_message)

        # Get template info if available
        template_info = cls.TEMPLATE_INFO.get(template_id) if template_id else None
        template_name = template_info["name"] if template_info else None

        # Create parsed error
        parsed = ParsedError(
            original_message=error_message,
            simplified_path=simplified_path or "Document root",
            full_xpath=xpath,
            requirement=requirement,
            template_id=template_id,
            conf_number=conf_number,
            template_name=template_name,
            severity=severity,
            suggestions=[],
        )

        # Generate suggestions
        parsed.suggestions = cls.generate_suggestions(parsed)

        return parsed

    @classmethod
    def parse_errors(cls, error_messages: list[str]) -> list[ParsedError]:
        """
        Parse multiple error messages.

        Args:
            error_messages: List of raw error messages

        Returns:
            List of ParsedError objects
        """
        return [cls.parse_error(msg) for msg in error_messages]
