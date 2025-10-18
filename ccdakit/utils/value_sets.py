"""Value set registry and utilities for C-CDA value sets."""

import json
from pathlib import Path
from typing import Any, Optional


class ValueSetRegistry:
    """
    Central registry for C-CDA value sets with validation and lookup capabilities.

    This class provides utilities for working with healthcare value sets,
    including validation, display name lookup, and value set management.
    Value sets define the allowed codes for specific clinical concepts.
    """

    # Common C-CDA value sets with codes and display names
    # Based on HL7 C-CDA R2.1 specification and companion guides

    # Problem/Condition Status - ActStatus value set (2.16.840.1.113883.1.11.15933)
    PROBLEM_STATUS = {
        "55561003": {"display": "Active", "system": "SNOMED"},
        "73425007": {"display": "Inactive", "system": "SNOMED"},
        "413322009": {"display": "Resolved", "system": "SNOMED"},
    }

    # Allergy Status - AllergyIntoleranceStatusValue Set (2.16.840.1.113883.3.88.12.3221.6.2)
    ALLERGY_STATUS = {
        "55561003": {"display": "Active", "system": "SNOMED"},
        "73425007": {"display": "Resolved", "system": "SNOMED"},
        "inactive": {"display": "Inactive", "system": "ActStatus"},
    }

    # Medication Status - Medication Clinical Drug (2.16.840.1.113883.3.88.12.80.20)
    MEDICATION_STATUS = {
        "55561003": {"display": "Active", "system": "SNOMED"},
        "completed": {"display": "Completed", "system": "ActStatus"},
        "aborted": {"display": "Discontinued", "system": "ActStatus"},
        "suspended": {"display": "On hold", "system": "ActStatus"},
    }

    # Observation Interpretation - ObservationInterpretation (2.16.840.1.113883.5.83)
    OBSERVATION_INTERPRETATION = {
        "N": {"display": "Normal", "system": "ObservationInterpretation"},
        "L": {"display": "Low", "system": "ObservationInterpretation"},
        "H": {"display": "High", "system": "ObservationInterpretation"},
        "LL": {"display": "Critical low", "system": "ObservationInterpretation"},
        "HH": {"display": "Critical high", "system": "ObservationInterpretation"},
        "A": {"display": "Abnormal", "system": "ObservationInterpretation"},
        "<": {"display": "Off scale low", "system": "ObservationInterpretation"},
        ">": {"display": "Off scale high", "system": "ObservationInterpretation"},
    }

    # Problem Type - Problem Type Value Set (2.16.840.1.113883.3.88.12.3221.7.2)
    PROBLEM_TYPE = {
        "55607006": {"display": "Problem", "system": "SNOMED"},
        "404684003": {"display": "Clinical finding", "system": "SNOMED"},
        "409586006": {"display": "Complaint", "system": "SNOMED"},
        "282291009": {"display": "Diagnosis", "system": "SNOMED"},
        "64572001": {"display": "Condition", "system": "SNOMED"},
    }

    # Allergy Severity - AllergyIntoleranceSeverity (2.16.840.1.113883.3.88.12.3221.6.8)
    ALLERGY_SEVERITY = {
        "255604002": {"display": "Mild", "system": "SNOMED"},
        "6736007": {"display": "Moderate", "system": "SNOMED"},
        "24484000": {"display": "Severe", "system": "SNOMED"},
        "399166001": {"display": "Fatal", "system": "SNOMED"},
    }

    # Allergy Reaction Type - AllergyIntoleranceType (2.16.840.1.113883.3.88.12.3221.6.2)
    ALLERGY_REACTION_TYPE = {
        "419511003": {"display": "Propensity to adverse reactions to drug", "system": "SNOMED"},
        "418038007": {
            "display": "Propensity to adverse reactions to substance",
            "system": "SNOMED",
        },
        "419199007": {"display": "Allergy to substance", "system": "SNOMED"},
        "418471000": {"display": "Propensity to adverse reactions to food", "system": "SNOMED"},
    }

    # Smoking Status - Smoking Status Value Set (2.16.840.1.113883.11.20.9.38)
    SMOKING_STATUS = {
        "449868002": {"display": "Current every day smoker", "system": "SNOMED"},
        "428041000124106": {"display": "Current some day smoker", "system": "SNOMED"},
        "8517006": {"display": "Former smoker", "system": "SNOMED"},
        "266919005": {"display": "Never smoker", "system": "SNOMED"},
        "77176002": {"display": "Smoker, current status unknown", "system": "SNOMED"},
        "266927001": {"display": "Unknown if ever smoked", "system": "SNOMED"},
        "428071000124103": {"display": "Current Heavy tobacco smoker", "system": "SNOMED"},
        "428061000124105": {"display": "Current Light tobacco smoker", "system": "SNOMED"},
    }

    # Encounter Type - Encounter Type Value Set (2.16.840.1.113883.3.88.12.80.32)
    ENCOUNTER_TYPE = {
        "AMB": {"display": "Ambulatory", "system": "ActCode"},
        "EMER": {"display": "Emergency", "system": "ActCode"},
        "FLD": {"display": "Field", "system": "ActCode"},
        "HH": {"display": "Home health", "system": "ActCode"},
        "IMP": {"display": "Inpatient encounter", "system": "ActCode"},
        "ACUTE": {"display": "Inpatient acute", "system": "ActCode"},
        "NONAC": {"display": "Inpatient non-acute", "system": "ActCode"},
        "OBSENC": {"display": "Observation encounter", "system": "ActCode"},
        "PRENC": {"display": "Pre-admission", "system": "ActCode"},
        "SS": {"display": "Short stay", "system": "ActCode"},
        "VR": {"display": "Virtual", "system": "ActCode"},
    }

    # Lab Result Status - ResultStatus (2.16.840.1.113883.11.20.9.39)
    LAB_RESULT_STATUS = {
        "completed": {"display": "Completed", "system": "ActStatus"},
        "active": {"display": "Active", "system": "ActStatus"},
        "aborted": {"display": "Aborted", "system": "ActStatus"},
        "held": {"display": "Held", "system": "ActStatus"},
    }

    # Procedure Status - ProcedureActStatus (2.16.840.1.113883.11.20.9.22)
    PROCEDURE_STATUS = {
        "completed": {"display": "Completed", "system": "ActStatus"},
        "active": {"display": "Active", "system": "ActStatus"},
        "aborted": {"display": "Aborted", "system": "ActStatus"},
        "held": {"display": "Held", "system": "ActStatus"},
        "new": {"display": "New", "system": "ActStatus"},
        "suspended": {"display": "Suspended", "system": "ActStatus"},
        "cancelled": {"display": "Cancelled", "system": "ActStatus"},
        "obsolete": {"display": "Obsolete", "system": "ActStatus"},
    }

    # Immunization Status - ImmunizationStatus (2.16.840.1.113883.11.20.9.41)
    IMMUNIZATION_STATUS = {
        "completed": {"display": "Completed", "system": "ActStatus"},
        "active": {"display": "Active", "system": "ActStatus"},
        "aborted": {"display": "Aborted", "system": "ActStatus"},
        "held": {"display": "Held", "system": "ActStatus"},
    }

    # Vital Sign Result Type - Vital Sign Result Type (2.16.840.1.113883.3.88.12.80.62)
    VITAL_SIGN_RESULT_TYPE = {
        "8310-5": {"display": "Body temperature", "system": "LOINC"},
        "8867-4": {"display": "Heart rate", "system": "LOINC"},
        "9279-1": {"display": "Respiratory rate", "system": "LOINC"},
        "8480-6": {"display": "Systolic blood pressure", "system": "LOINC"},
        "8462-4": {"display": "Diastolic blood pressure", "system": "LOINC"},
        "8287-5": {"display": "Head circumference", "system": "LOINC"},
        "8302-2": {"display": "Body height", "system": "LOINC"},
        "8306-3": {"display": "Body height (lying)", "system": "LOINC"},
        "29463-7": {"display": "Body weight", "system": "LOINC"},
        "39156-5": {"display": "Body mass index", "system": "LOINC"},
        "2710-2": {"display": "Oxygen saturation", "system": "LOINC"},
    }

    # Administrative Gender - AdministrativeGender (2.16.840.1.113883.5.1)
    ADMINISTRATIVE_GENDER = {
        "M": {"display": "Male", "system": "AdministrativeGender"},
        "F": {"display": "Female", "system": "AdministrativeGender"},
        "UN": {"display": "Undifferentiated", "system": "AdministrativeGender"},
    }

    # Marital Status - MaritalStatus (2.16.840.1.113883.5.2)
    MARITAL_STATUS = {
        "A": {"display": "Annulled", "system": "MaritalStatus"},
        "D": {"display": "Divorced", "system": "MaritalStatus"},
        "I": {"display": "Interlocutory", "system": "MaritalStatus"},
        "L": {"display": "Legally Separated", "system": "MaritalStatus"},
        "M": {"display": "Married", "system": "MaritalStatus"},
        "P": {"display": "Polygamous", "system": "MaritalStatus"},
        "S": {"display": "Never Married", "system": "MaritalStatus"},
        "T": {"display": "Domestic partner", "system": "MaritalStatus"},
        "W": {"display": "Widowed", "system": "MaritalStatus"},
    }

    # Null Flavor - NullFlavor (2.16.840.1.113883.5.1008)
    NULL_FLAVOR = {
        "NI": {"display": "No information", "system": "NullFlavor"},
        "NA": {"display": "Not applicable", "system": "NullFlavor"},
        "UNK": {"display": "Unknown", "system": "NullFlavor"},
        "ASKU": {"display": "Asked but unknown", "system": "NullFlavor"},
        "NAV": {"display": "Temporarily unavailable", "system": "NullFlavor"},
        "NASK": {"display": "Not asked", "system": "NullFlavor"},
        "MSK": {"display": "Masked", "system": "NullFlavor"},
        "OTH": {"display": "Other", "system": "NullFlavor"},
        "NINF": {"display": "Negative infinity", "system": "NullFlavor"},
        "PINF": {"display": "Positive infinity", "system": "NullFlavor"},
    }

    # Route of Administration - RouteOfAdministration (2.16.840.1.113883.5.112)
    ROUTE_OF_ADMINISTRATION = {
        "C38216": {"display": "Auricular (otic)", "system": "NCI"},
        "C38193": {"display": "Buccal", "system": "NCI"},
        "C38633": {"display": "Cutaneous", "system": "NCI"},
        "C38205": {"display": "Dental", "system": "NCI"},
        "C38238": {"display": "Inhalation", "system": "NCI"},
        "C38276": {"display": "Intramuscular injection", "system": "NCI"},
        "C38279": {"display": "Intravenous", "system": "NCI"},
        "C38288": {"display": "Nasal", "system": "NCI"},
        "C38289": {"display": "Nasogastric", "system": "NCI"},
        "C38299": {"display": "Ophthalmic", "system": "NCI"},
        "C38304": {"display": "Oral", "system": "NCI"},
        "C38676": {"display": "Rectal", "system": "NCI"},
        "C38308": {"display": "Subcutaneous", "system": "NCI"},
        "C38300": {"display": "Sublingual", "system": "NCI"},
        "C38305": {"display": "Topical", "system": "NCI"},
        "C38273": {"display": "Transdermal", "system": "NCI"},
    }

    # Discharge Disposition - DischargeDisposition (2.16.840.1.113883.12.112)
    DISCHARGE_DISPOSITION = {
        "01": {"display": "Discharged to home or self care", "system": "DischargeDisposition"},
        "02": {
            "display": "Discharged/transferred to a short-term general hospital",
            "system": "DischargeDisposition",
        },
        "03": {
            "display": "Discharged/transferred to skilled nursing facility",
            "system": "DischargeDisposition",
        },
        "04": {
            "display": "Discharged/transferred to an intermediate care facility",
            "system": "DischargeDisposition",
        },
        "05": {
            "display": "Discharged/transferred to another type of institution",
            "system": "DischargeDisposition",
        },
        "06": {
            "display": "Discharged/transferred to home under care of organized home health service",
            "system": "DischargeDisposition",
        },
        "07": {"display": "Left against medical advice", "system": "DischargeDisposition"},
        "20": {"display": "Expired", "system": "DischargeDisposition"},
        "21": {
            "display": "Discharged/transferred to court/law enforcement",
            "system": "DischargeDisposition",
        },
    }

    # Registry mapping value set names to their definitions
    VALUE_SETS = {
        "PROBLEM_STATUS": {
            "oid": "2.16.840.1.113883.1.11.15933",
            "name": "Problem Status",
            "description": "Status of a problem or condition (active, inactive, resolved)",
            "codes": PROBLEM_STATUS,
        },
        "ALLERGY_STATUS": {
            "oid": "2.16.840.1.113883.3.88.12.3221.6.2",
            "name": "Allergy Status",
            "description": "Status of an allergy or intolerance",
            "codes": ALLERGY_STATUS,
        },
        "MEDICATION_STATUS": {
            "oid": "2.16.840.1.113883.3.88.12.80.20",
            "name": "Medication Status",
            "description": "Status of a medication (active, completed, discontinued)",
            "codes": MEDICATION_STATUS,
        },
        "OBSERVATION_INTERPRETATION": {
            "oid": "2.16.840.1.113883.5.83",
            "name": "Observation Interpretation",
            "description": "Interpretation of an observation result (normal, high, low, critical)",
            "codes": OBSERVATION_INTERPRETATION,
        },
        "PROBLEM_TYPE": {
            "oid": "2.16.840.1.113883.3.88.12.3221.7.2",
            "name": "Problem Type",
            "description": "Type of problem (problem, diagnosis, complaint, etc.)",
            "codes": PROBLEM_TYPE,
        },
        "ALLERGY_SEVERITY": {
            "oid": "2.16.840.1.113883.3.88.12.3221.6.8",
            "name": "Allergy Severity",
            "description": "Severity of an allergic reaction (mild, moderate, severe, fatal)",
            "codes": ALLERGY_SEVERITY,
        },
        "ALLERGY_REACTION_TYPE": {
            "oid": "2.16.840.1.113883.3.88.12.3221.6.2",
            "name": "Allergy Reaction Type",
            "description": "Type of allergic reaction or intolerance",
            "codes": ALLERGY_REACTION_TYPE,
        },
        "SMOKING_STATUS": {
            "oid": "2.16.840.1.113883.11.20.9.38",
            "name": "Smoking Status",
            "description": "Patient's smoking status",
            "codes": SMOKING_STATUS,
        },
        "ENCOUNTER_TYPE": {
            "oid": "2.16.840.1.113883.3.88.12.80.32",
            "name": "Encounter Type",
            "description": "Type of healthcare encounter",
            "codes": ENCOUNTER_TYPE,
        },
        "LAB_RESULT_STATUS": {
            "oid": "2.16.840.1.113883.11.20.9.39",
            "name": "Lab Result Status",
            "description": "Status of a laboratory result",
            "codes": LAB_RESULT_STATUS,
        },
        "PROCEDURE_STATUS": {
            "oid": "2.16.840.1.113883.11.20.9.22",
            "name": "Procedure Status",
            "description": "Status of a procedure",
            "codes": PROCEDURE_STATUS,
        },
        "IMMUNIZATION_STATUS": {
            "oid": "2.16.840.1.113883.11.20.9.41",
            "name": "Immunization Status",
            "description": "Status of an immunization",
            "codes": IMMUNIZATION_STATUS,
        },
        "VITAL_SIGN_RESULT_TYPE": {
            "oid": "2.16.840.1.113883.3.88.12.80.62",
            "name": "Vital Sign Result Type",
            "description": "Types of vital sign measurements",
            "codes": VITAL_SIGN_RESULT_TYPE,
        },
        "ADMINISTRATIVE_GENDER": {
            "oid": "2.16.840.1.113883.5.1",
            "name": "Administrative Gender",
            "description": "Administrative gender (M, F, UN)",
            "codes": ADMINISTRATIVE_GENDER,
        },
        "MARITAL_STATUS": {
            "oid": "2.16.840.1.113883.5.2",
            "name": "Marital Status",
            "description": "Marital status",
            "codes": MARITAL_STATUS,
        },
        "NULL_FLAVOR": {
            "oid": "2.16.840.1.113883.5.1008",
            "name": "Null Flavor",
            "description": "Reasons for missing information",
            "codes": NULL_FLAVOR,
        },
        "ROUTE_OF_ADMINISTRATION": {
            "oid": "2.16.840.1.113883.5.112",
            "name": "Route of Administration",
            "description": "Routes for medication administration",
            "codes": ROUTE_OF_ADMINISTRATION,
        },
        "DISCHARGE_DISPOSITION": {
            "oid": "2.16.840.1.113883.12.112",
            "name": "Discharge Disposition",
            "description": "Patient discharge disposition",
            "codes": DISCHARGE_DISPOSITION,
        },
    }

    @staticmethod
    def validate_code(value_set: str, code: str) -> bool:
        """
        Validate that a code exists in a specific value set.

        Args:
            value_set: Name of the value set (e.g., "PROBLEM_STATUS")
            code: Code to validate

        Returns:
            True if code is valid for the value set, False otherwise

        Example:
            >>> ValueSetRegistry.validate_code("PROBLEM_STATUS", "55561003")
            True
            >>> ValueSetRegistry.validate_code("PROBLEM_STATUS", "invalid")
            False
        """
        vs = ValueSetRegistry.VALUE_SETS.get(value_set)
        if not vs:
            return False

        codes = vs.get("codes", {})
        return code in codes

    @staticmethod
    def get_display_name(value_set: str, code: str) -> Optional[str]:
        """
        Get the display name for a code in a value set.

        Args:
            value_set: Name of the value set
            code: Code to look up

        Returns:
            Display name string if found, None otherwise

        Example:
            >>> ValueSetRegistry.get_display_name("PROBLEM_STATUS", "55561003")
            'Active'
            >>> ValueSetRegistry.get_display_name("PROBLEM_STATUS", "invalid")
            None
        """
        vs = ValueSetRegistry.VALUE_SETS.get(value_set)
        if not vs:
            return None

        codes = vs.get("codes", {})
        code_info = codes.get(code)
        if code_info:
            return code_info.get("display")
        return None

    @staticmethod
    def get_code_system(value_set: str, code: str) -> Optional[str]:
        """
        Get the code system for a code in a value set.

        Args:
            value_set: Name of the value set
            code: Code to look up

        Returns:
            Code system name if found, None otherwise

        Example:
            >>> ValueSetRegistry.get_code_system("PROBLEM_STATUS", "55561003")
            'SNOMED'
        """
        vs = ValueSetRegistry.VALUE_SETS.get(value_set)
        if not vs:
            return None

        codes = vs.get("codes", {})
        code_info = codes.get(code)
        if code_info:
            return code_info.get("system")
        return None

    @staticmethod
    def get_code_info(value_set: str, code: str) -> Optional[dict]:
        """
        Get complete information for a code in a value set.

        Args:
            value_set: Name of the value set
            code: Code to look up

        Returns:
            Dictionary with 'display' and 'system' keys if found, None otherwise

        Example:
            >>> info = ValueSetRegistry.get_code_info("PROBLEM_STATUS", "55561003")
            >>> info["display"]
            'Active'
            >>> info["system"]
            'SNOMED'
        """
        vs = ValueSetRegistry.VALUE_SETS.get(value_set)
        if not vs:
            return None

        codes = vs.get("codes", {})
        return codes.get(code)

    @staticmethod
    def get_value_set(name: str) -> Optional["dict[str, Any]"]:
        """
        Get complete value set definition.

        Args:
            name: Value set name

        Returns:
            Dictionary with value set metadata and codes if found, None otherwise

        Example:
            >>> vs = ValueSetRegistry.get_value_set("PROBLEM_STATUS")
            >>> vs["oid"]
            '2.16.840.1.113883.1.11.15933'
            >>> len(vs["codes"])
            3
        """
        return ValueSetRegistry.VALUE_SETS.get(name)

    @staticmethod
    def get_value_set_by_oid(oid: str) -> Optional["dict[str, Any]"]:
        """
        Get value set definition by OID.

        Args:
            oid: Value set OID

        Returns:
            Dictionary with value set metadata and codes if found, None otherwise

        Example:
            >>> vs = ValueSetRegistry.get_value_set_by_oid("2.16.840.1.113883.1.11.15933")
            >>> vs["name"]
            'Problem Status'
        """
        for _name, vs in ValueSetRegistry.VALUE_SETS.items():
            if vs.get("oid") == oid:
                return vs
        return None

    @staticmethod
    def list_value_sets() -> "list[str]":
        """
        Get list of all available value set names.

        Returns:
            List of value set names

        Example:
            >>> value_sets = ValueSetRegistry.list_value_sets()
            >>> "PROBLEM_STATUS" in value_sets
            True
            >>> len(value_sets)
            18
        """
        return list(ValueSetRegistry.VALUE_SETS.keys())

    @staticmethod
    def get_codes(value_set: str) -> "list[str]":
        """
        Get all valid codes for a value set.

        Args:
            value_set: Name of the value set

        Returns:
            List of valid codes, empty list if value set not found

        Example:
            >>> codes = ValueSetRegistry.get_codes("ADMINISTRATIVE_GENDER")
            >>> "M" in codes
            True
            >>> "F" in codes
            True
        """
        vs = ValueSetRegistry.VALUE_SETS.get(value_set)
        if not vs:
            return []

        codes = vs.get("codes", {})
        return list(codes.keys())

    @staticmethod
    def search_by_display(
        value_set: str, display_text: str, case_sensitive: bool = False
    ) -> "list[str]":
        """
        Search for codes by display name.

        Args:
            value_set: Name of the value set
            display_text: Display text to search for (partial match supported)
            case_sensitive: Whether search is case-sensitive (default: False)

        Returns:
            List of matching codes

        Example:
            >>> codes = ValueSetRegistry.search_by_display("PROBLEM_STATUS", "active")
            >>> "55561003" in codes
            True
        """
        vs = ValueSetRegistry.VALUE_SETS.get(value_set)
        if not vs:
            return []

        codes = vs.get("codes", {})
        matching_codes = []

        search_text = display_text if case_sensitive else display_text.lower()

        for code, info in codes.items():
            display = info.get("display", "")
            compare_display = display if case_sensitive else display.lower()

            if search_text in compare_display:
                matching_codes.append(code)

        return matching_codes

    @staticmethod
    def load_from_json(file_path: str) -> dict:
        """
        Load value set from JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            Dictionary with value set data

        Example JSON format:
            {
                "oid": "2.16.840.1.113883.1.11.15933",
                "name": "Custom Value Set",
                "description": "Description of the value set",
                "codes": {
                    "code1": {"display": "Display 1", "system": "SNOMED"},
                    "code2": {"display": "Display 2", "system": "LOINC"}
                }
            }
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Value set file not found: {file_path}")

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_to_json(value_set_name: str, file_path: str) -> None:
        """
        Save value set to JSON file.

        Args:
            value_set_name: Name of the value set to save
            file_path: Path where JSON file should be saved

        Raises:
            ValueError: If value set not found
        """
        vs = ValueSetRegistry.VALUE_SETS.get(value_set_name)
        if not vs:
            raise ValueError(f"Value set not found: {value_set_name}")

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(vs, f, indent=2)
