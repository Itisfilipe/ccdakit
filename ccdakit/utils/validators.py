"""Data validation utilities for C-CDA documents.

This module provides pre-build validation utilities to catch errors early
and ensure data quality before creating C-CDA documents.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from ccdakit.core.validation import ValidationIssue, ValidationLevel, ValidationResult
from ccdakit.utils.code_systems import CodeSystemRegistry


class DataValidator:
    """Validate data before building C-CDA elements.

    This class provides static methods to validate various types of clinical data
    before passing them to C-CDA builders. Each validator checks:
    - Required fields are present
    - Data types are correct (date vs datetime, str vs int)
    - Code formats are valid
    - Date logic is sound (e.g., resolved_date > onset_date)
    - Ranges are reasonable (vital signs, lab values)
    - References are valid (code systems exist)
    """

    # Valid status values for different clinical data types
    VALID_PROBLEM_STATUS = {"active", "inactive", "resolved"}
    VALID_MEDICATION_STATUS = {"active", "completed", "discontinued", "on-hold"}
    VALID_ALLERGY_STATUS = {"active", "resolved", "inactive"}
    VALID_ALLERGY_TYPE = {"allergy", "intolerance"}
    VALID_ALLERGY_SEVERITY = {"mild", "moderate", "severe", "fatal"}
    VALID_PROCEDURE_STATUS = {"completed", "active", "aborted", "cancelled"}
    VALID_RESULT_STATUS = {"completed", "preliminary", "final", "amended", "corrected"}
    VALID_IMMUNIZATION_STATUS = {"completed", "refused", "not-done"}
    VALID_SEX = {"M", "F", "UN"}
    VALID_TELECOM_TYPES = {"phone", "email", "fax", "url"}
    VALID_TELECOM_USE = {"HP", "WP", "MC", "H", "W"}  # Home, Work, Mobile, etc.

    # Valid value types for results
    VALID_VALUE_TYPES = {"PQ", "CD", "ST"}  # Physical Quantity, Coded, String

    @staticmethod
    def validate_patient_data(patient: Dict[str, Any]) -> ValidationResult:
        """Validate patient demographic data.

        Args:
            patient: Dictionary containing patient data

        Returns:
            ValidationResult with any validation issues found

        Example:
            >>> patient = {
            ...     "first_name": "John",
            ...     "last_name": "Doe",
            ...     "date_of_birth": date(1980, 1, 1),
            ...     "sex": "M",
            ... }
            >>> result = DataValidator.validate_patient_data(patient)
            >>> result.is_valid
            True
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["first_name", "last_name", "date_of_birth", "sex"]
        missing = DataValidator.validate_required_fields(patient, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        # If required fields are missing, return early
        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate data types
        if not isinstance(patient.get("first_name"), str):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="first_name must be a string",
                    code="INVALID_TYPE",
                )
            )

        if not isinstance(patient.get("last_name"), str):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="last_name must be a string",
                    code="INVALID_TYPE",
                )
            )

        # Validate date of birth
        dob = patient.get("date_of_birth")
        if dob is not None:
            if not isinstance(dob, date):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="date_of_birth must be a date object",
                        code="INVALID_TYPE",
                    )
                )
            elif dob > date.today():
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="date_of_birth cannot be in the future",
                        code="INVALID_DATE",
                    )
                )
            elif dob < date(1900, 1, 1):
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="date_of_birth is before 1900, please verify",
                        code="SUSPICIOUS_DATE",
                    )
                )

        # Validate sex
        sex = patient.get("sex")
        if sex is not None and sex not in DataValidator.VALID_SEX:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"sex must be one of {DataValidator.VALID_SEX}, got '{sex}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate optional fields
        if "addresses" in patient:
            if not isinstance(patient["addresses"], list):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="addresses must be a list",
                        code="INVALID_TYPE",
                    )
                )
            else:
                for i, addr in enumerate(patient["addresses"]):
                    addr_result = DataValidator._validate_address(addr)
                    for issue in addr_result.errors:
                        errors.append(
                            ValidationIssue(
                                level=issue.level,
                                message=f"Address {i}: {issue.message}",
                                code=issue.code,
                            )
                        )

        if "telecoms" in patient:
            if not isinstance(patient["telecoms"], list):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="telecoms must be a list",
                        code="INVALID_TYPE",
                    )
                )
            else:
                for i, telecom in enumerate(patient["telecoms"]):
                    telecom_result = DataValidator._validate_telecom(telecom)
                    for issue in telecom_result.errors:
                        errors.append(
                            ValidationIssue(
                                level=issue.level,
                                message=f"Telecom {i}: {issue.message}",
                                code=issue.code,
                            )
                        )

        # Validate race/ethnicity codes if provided
        if "race" in patient and patient["race"] is not None:
            if not DataValidator.validate_code_system("Race"):
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="Could not validate race code system",
                        code="UNKNOWN_CODE_SYSTEM",
                    )
                )

        if "ethnicity" in patient and patient["ethnicity"] is not None:
            if not DataValidator.validate_code_system("Ethnicity"):
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="Could not validate ethnicity code system",
                        code="UNKNOWN_CODE_SYSTEM",
                    )
                )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_problem_data(problem: Dict[str, Any]) -> ValidationResult:
        """Validate problem/diagnosis data.

        Args:
            problem: Dictionary containing problem data

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["name", "code", "code_system", "status"]
        missing = DataValidator.validate_required_fields(problem, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate data types
        if not isinstance(problem.get("name"), str):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="name must be a string",
                    code="INVALID_TYPE",
                )
            )

        if not isinstance(problem.get("code"), str):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="code must be a string",
                    code="INVALID_TYPE",
                )
            )

        # Validate code system
        code_system = problem.get("code_system")
        if code_system and not DataValidator.validate_code_system(code_system):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"Unknown code system: {code_system}",
                    code="UNKNOWN_CODE_SYSTEM",
                )
            )

        # Validate code format
        code = problem.get("code")
        if code and code_system:
            if not DataValidator.validate_code(code, code_system):
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message=f"Code '{code}' does not match expected format for {code_system}",
                        code="INVALID_CODE_FORMAT",
                    )
                )

        # Validate status
        status = problem.get("status")
        if status and status not in DataValidator.VALID_PROBLEM_STATUS:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"status must be one of {DataValidator.VALID_PROBLEM_STATUS}, got '{status}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate dates
        onset = problem.get("onset_date")
        resolved = problem.get("resolved_date")

        if onset is not None and not isinstance(onset, date):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="onset_date must be a date object",
                    code="INVALID_TYPE",
                )
            )

        if resolved is not None and not isinstance(resolved, date):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="resolved_date must be a date object",
                    code="INVALID_TYPE",
                )
            )

        # Validate date logic
        if onset and resolved:
            if not DataValidator.validate_date_range(onset, resolved):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="resolved_date must be after onset_date",
                        code="INVALID_DATE_RANGE",
                    )
                )

        # Validate status consistency
        if status == "resolved" and not resolved:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message="Problem marked as resolved but no resolved_date provided",
                    code="INCONSISTENT_DATA",
                )
            )

        if status != "resolved" and resolved:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message="Problem has resolved_date but status is not 'resolved'",
                    code="INCONSISTENT_DATA",
                )
            )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_medication_data(medication: Dict[str, Any]) -> ValidationResult:
        """Validate medication data.

        Args:
            medication: Dictionary containing medication data

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["name", "code", "dosage", "route", "frequency", "start_date", "status"]
        missing = DataValidator.validate_required_fields(medication, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate code (should be RxNorm)
        code = medication.get("code")
        if code and not DataValidator.validate_code(code, "RxNorm"):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"Code '{code}' does not match expected RxNorm format",
                    code="INVALID_CODE_FORMAT",
                )
            )

        # Validate status
        status = medication.get("status")
        if status and status not in DataValidator.VALID_MEDICATION_STATUS:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"status must be one of {DataValidator.VALID_MEDICATION_STATUS}, got '{status}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate dates
        start = medication.get("start_date")
        end = medication.get("end_date")

        if start is not None and not isinstance(start, date):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="start_date must be a date object",
                    code="INVALID_TYPE",
                )
            )

        if end is not None and not isinstance(end, date):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="end_date must be a date object",
                    code="INVALID_TYPE",
                )
            )

        if start and end:
            if not DataValidator.validate_date_range(start, end):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="end_date must be after start_date",
                        code="INVALID_DATE_RANGE",
                    )
                )

        # Validate status consistency
        if status in ["completed", "discontinued"] and not end:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"Medication status is '{status}' but no end_date provided",
                    code="INCONSISTENT_DATA",
                )
            )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_allergy_data(allergy: Dict[str, Any]) -> ValidationResult:
        """Validate allergy/intolerance data.

        Args:
            allergy: Dictionary containing allergy data

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["allergen", "allergy_type", "status"]
        missing = DataValidator.validate_required_fields(allergy, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate allergy type
        allergy_type = allergy.get("allergy_type")
        if allergy_type and allergy_type not in DataValidator.VALID_ALLERGY_TYPE:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"allergy_type must be one of {DataValidator.VALID_ALLERGY_TYPE}, got '{allergy_type}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate status
        status = allergy.get("status")
        if status and status not in DataValidator.VALID_ALLERGY_STATUS:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"status must be one of {DataValidator.VALID_ALLERGY_STATUS}, got '{status}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate severity if provided
        severity = allergy.get("severity")
        if severity and severity not in DataValidator.VALID_ALLERGY_SEVERITY:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"severity should be one of {DataValidator.VALID_ALLERGY_SEVERITY}, got '{severity}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate code system if code is provided
        if "allergen_code" in allergy and allergy["allergen_code"]:
            code_system = allergy.get("allergen_code_system")
            if not code_system:
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="allergen_code provided but allergen_code_system is missing",
                        code="MISSING_FIELD",
                    )
                )
            elif not DataValidator.validate_code_system(code_system):
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message=f"Unknown code system: {code_system}",
                        code="UNKNOWN_CODE_SYSTEM",
                    )
                )

        # Validate onset date
        onset = allergy.get("onset_date")
        if onset is not None:
            if not isinstance(onset, date):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="onset_date must be a date object",
                        code="INVALID_TYPE",
                    )
                )
            elif onset > date.today():
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="onset_date is in the future",
                        code="SUSPICIOUS_DATE",
                    )
                )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_immunization_data(immunization: Dict[str, Any]) -> ValidationResult:
        """Validate immunization data.

        Args:
            immunization: Dictionary containing immunization data

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["vaccine_name", "cvx_code", "administration_date", "status"]
        missing = DataValidator.validate_required_fields(immunization, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate CVX code format
        cvx_code = immunization.get("cvx_code")
        if cvx_code and not DataValidator.validate_code(cvx_code, "CVX"):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"cvx_code '{cvx_code}' does not match expected CVX format",
                    code="INVALID_CODE_FORMAT",
                )
            )

        # Validate status
        status = immunization.get("status")
        if status and status not in DataValidator.VALID_IMMUNIZATION_STATUS:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"status must be one of {DataValidator.VALID_IMMUNIZATION_STATUS}, got '{status}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate administration date
        admin_date = immunization.get("administration_date")
        if admin_date is not None:
            if not isinstance(admin_date, (date, datetime)):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="administration_date must be a date or datetime object",
                        code="INVALID_TYPE",
                    )
                )
            else:
                # Convert to date for comparison
                check_date = admin_date.date() if isinstance(admin_date, datetime) else admin_date
                if check_date > date.today():
                    warnings.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message="administration_date is in the future",
                            code="SUSPICIOUS_DATE",
                        )
                    )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_vital_signs_data(vital_signs: Dict[str, Any]) -> ValidationResult:
        """Validate vital signs data.

        Args:
            vital_signs: Dictionary containing vital signs data (organizer with vital_signs list)

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields for organizer
        required = ["date", "vital_signs"]
        missing = DataValidator.validate_required_fields(vital_signs, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate date
        vs_date = vital_signs.get("date")
        if vs_date is not None and not isinstance(vs_date, (date, datetime)):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="date must be a date or datetime object",
                    code="INVALID_TYPE",
                )
            )

        # Validate vital signs list
        vs_list = vital_signs.get("vital_signs")
        if not isinstance(vs_list, list):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="vital_signs must be a list",
                    code="INVALID_TYPE",
                )
            )
            return ValidationResult(errors=errors, warnings=warnings)

        if len(vs_list) == 0:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message="vital_signs list is empty",
                    code="EMPTY_LIST",
                )
            )

        # Validate each vital sign
        for i, vs in enumerate(vs_list):
            vs_result = DataValidator._validate_single_vital_sign(vs)
            for issue in vs_result.errors:
                errors.append(
                    ValidationIssue(
                        level=issue.level,
                        message=f"Vital sign {i}: {issue.message}",
                        code=issue.code,
                    )
                )
            for issue in vs_result.warnings:
                warnings.append(
                    ValidationIssue(
                        level=issue.level,
                        message=f"Vital sign {i}: {issue.message}",
                        code=issue.code,
                    )
                )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_procedure_data(procedure: Dict[str, Any]) -> ValidationResult:
        """Validate procedure data.

        Args:
            procedure: Dictionary containing procedure data

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["name", "code", "code_system", "status"]
        missing = DataValidator.validate_required_fields(procedure, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate code system
        code_system = procedure.get("code_system")
        if code_system and not DataValidator.validate_code_system(code_system):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"Unknown code system: {code_system}",
                    code="UNKNOWN_CODE_SYSTEM",
                )
            )

        # Validate status
        status = procedure.get("status")
        if status and status not in DataValidator.VALID_PROCEDURE_STATUS:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"status must be one of {DataValidator.VALID_PROCEDURE_STATUS}, got '{status}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate date
        proc_date = procedure.get("date")
        if proc_date is not None:
            if not isinstance(proc_date, (date, datetime)):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="date must be a date or datetime object",
                        code="INVALID_TYPE",
                    )
                )
            else:
                # Convert to date for comparison
                check_date = proc_date.date() if isinstance(proc_date, datetime) else proc_date
                if check_date > date.today():
                    warnings.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message="Procedure date is in the future",
                            code="SUSPICIOUS_DATE",
                        )
                    )

        # Validate target site code if provided
        if "target_site_code" in procedure and procedure["target_site_code"]:
            if not procedure.get("target_site"):
                warnings.append(
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="target_site_code provided but target_site name is missing",
                        code="MISSING_FIELD",
                    )
                )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_result_data(result: Dict[str, Any]) -> ValidationResult:
        """Validate lab result data.

        Args:
            result: Dictionary containing result organizer data with results list

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields for organizer
        required = ["panel_name", "panel_code", "status", "effective_time", "results"]
        missing = DataValidator.validate_required_fields(result, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate panel code (should be LOINC)
        panel_code = result.get("panel_code")
        if panel_code and not DataValidator.validate_code(panel_code, "LOINC"):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"panel_code '{panel_code}' does not match expected LOINC format",
                    code="INVALID_CODE_FORMAT",
                )
            )

        # Validate status
        status = result.get("status")
        if status and status not in DataValidator.VALID_RESULT_STATUS:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"status must be one of {DataValidator.VALID_RESULT_STATUS}, got '{status}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate effective time
        effective_time = result.get("effective_time")
        if effective_time is not None and not isinstance(effective_time, (date, datetime)):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="effective_time must be a date or datetime object",
                    code="INVALID_TYPE",
                )
            )

        # Validate results list
        results_list = result.get("results")
        if not isinstance(results_list, (list, tuple)):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="results must be a list or tuple",
                    code="INVALID_TYPE",
                )
            )
            return ValidationResult(errors=errors, warnings=warnings)

        if len(results_list) == 0:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message="results list is empty",
                    code="EMPTY_LIST",
                )
            )

        # Validate each result observation
        for i, obs in enumerate(results_list):
            obs_result = DataValidator._validate_result_observation(obs)
            for issue in obs_result.errors:
                errors.append(
                    ValidationIssue(
                        level=issue.level, message=f"Result {i}: {issue.message}", code=issue.code
                    )
                )
            for issue in obs_result.warnings:
                warnings.append(
                    ValidationIssue(
                        level=issue.level, message=f"Result {i}: {issue.message}", code=issue.code
                    )
                )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_encounter_data(encounter: Dict[str, Any]) -> ValidationResult:
        """Validate encounter data.

        Args:
            encounter: Dictionary containing encounter data

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["encounter_type", "code", "code_system"]
        missing = DataValidator.validate_required_fields(encounter, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate code system
        code_system = encounter.get("code_system")
        if code_system and not DataValidator.validate_code_system(code_system):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"Unknown code system: {code_system}",
                    code="UNKNOWN_CODE_SYSTEM",
                )
            )

        # Validate date
        enc_date = encounter.get("date")
        if enc_date is not None:
            if not isinstance(enc_date, (date, datetime)):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="date must be a date or datetime object",
                        code="INVALID_TYPE",
                    )
                )

        # Validate end date
        end_date = encounter.get("end_date")
        if end_date is not None:
            if not isinstance(end_date, (date, datetime)):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="end_date must be a date or datetime object",
                        code="INVALID_TYPE",
                    )
                )

            # Validate date range if both dates present
            if enc_date and end_date:
                if not DataValidator.validate_date_range(enc_date, end_date):
                    errors.append(
                        ValidationIssue(
                            level=ValidationLevel.ERROR,
                            message="end_date must be after date",
                            code="INVALID_DATE_RANGE",
                        )
                    )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def validate_smoking_status_data(smoking_status: Dict[str, Any]) -> ValidationResult:
        """Validate smoking status data.

        Args:
            smoking_status: Dictionary containing smoking status data

        Returns:
            ValidationResult with any validation issues found
        """
        errors = []
        warnings = []

        # Check required fields
        required = ["smoking_status", "code", "date"]
        missing = DataValidator.validate_required_fields(smoking_status, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate code (should be SNOMED from smoking status value set)
        code = smoking_status.get("code")
        if code and not DataValidator.validate_code(code, "SNOMED"):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"code '{code}' does not match expected SNOMED format",
                    code="INVALID_CODE_FORMAT",
                )
            )

        # Validate date
        ss_date = smoking_status.get("date")
        if ss_date is not None:
            if not isinstance(ss_date, (date, datetime)):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="date must be a date or datetime object",
                        code="INVALID_TYPE",
                    )
                )
            else:
                # Convert to date for comparison
                check_date = ss_date.date() if isinstance(ss_date, datetime) else ss_date
                if check_date > date.today():
                    warnings.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message="Smoking status date is in the future",
                            code="SUSPICIOUS_DATE",
                        )
                    )

        return ValidationResult(errors=errors, warnings=warnings)

    # Helper methods

    @staticmethod
    def validate_code(code: str, system: str) -> bool:
        """Validate code format for system.

        Args:
            code: Code value to validate
            system: Code system name

        Returns:
            True if code format is valid for the system, False otherwise
        """
        return CodeSystemRegistry.validate_code_format(code, system)

    @staticmethod
    def validate_date_range(start: date, end: Optional[date]) -> bool:
        """Validate date range is logical.

        Args:
            start: Start date
            end: End date (can be None)

        Returns:
            True if date range is valid (end >= start or end is None), False otherwise
        """
        if end is None:
            return True

        # Handle datetime objects
        if isinstance(start, datetime) and isinstance(end, datetime):
            return end >= start

        # Handle mixed date/datetime
        start_date = start.date() if isinstance(start, datetime) else start
        end_date = end.date() if isinstance(end, datetime) else end

        return end_date >= start_date

    @staticmethod
    def validate_code_system(system: str) -> bool:
        """Validate code system exists in registry.

        Args:
            system: Code system name

        Returns:
            True if code system is registered, False otherwise
        """
        return CodeSystemRegistry.get_oid(system) is not None

    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required: List[str]) -> List[str]:
        """Validate required fields are present in data.

        Args:
            data: Data dictionary to validate
            required: List of required field names

        Returns:
            List of missing field names (empty if all present)
        """
        missing = []
        for field in required:
            if field not in data or data[field] is None or data[field] == "":
                missing.append(field)
        return missing

    # Private helper methods for nested validations

    @staticmethod
    def _validate_address(address: Dict[str, Any]) -> ValidationResult:
        """Validate address data."""
        errors = []

        required = ["city", "state", "postal_code", "country"]
        missing = DataValidator.validate_required_fields(address, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        # Validate street_lines if present
        if "street_lines" in address:
            street_lines = address["street_lines"]
            if not isinstance(street_lines, list):
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="street_lines must be a list",
                        code="INVALID_TYPE",
                    )
                )
            elif len(street_lines) > 4:
                errors.append(
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="street_lines can have at most 4 lines",
                        code="INVALID_VALUE",
                    )
                )

        return ValidationResult(errors=errors)

    @staticmethod
    def _validate_telecom(telecom: Dict[str, Any]) -> ValidationResult:
        """Validate telecom data."""
        errors = []
        warnings = []

        required = ["type", "value"]
        missing = DataValidator.validate_required_fields(telecom, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        # Validate type
        telecom_type = telecom.get("type")
        if telecom_type and telecom_type not in DataValidator.VALID_TELECOM_TYPES:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"type must be one of {DataValidator.VALID_TELECOM_TYPES}, got '{telecom_type}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate use if present
        use = telecom.get("use")
        if use and use not in DataValidator.VALID_TELECOM_USE:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"use should be one of {DataValidator.VALID_TELECOM_USE}, got '{use}'",
                    code="INVALID_VALUE",
                )
            )

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def _validate_single_vital_sign(vital_sign: Dict[str, Any]) -> ValidationResult:
        """Validate a single vital sign observation."""
        errors = []
        warnings = []

        required = ["type", "code", "value", "unit"]
        missing = DataValidator.validate_required_fields(vital_sign, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate code (should be LOINC)
        code = vital_sign.get("code")
        if code and not DataValidator.validate_code(code, "LOINC"):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"code '{code}' does not match expected LOINC format",
                    code="INVALID_CODE_FORMAT",
                )
            )

        # Validate value is numeric for common vital signs
        value = vital_sign.get("value")
        vs_type = vital_sign.get("type", "").lower()

        # Try to parse value as float for validation
        try:
            numeric_value = float(value)

            # Reasonable range checks for common vital signs
            if "blood pressure" in vs_type or "bp" in vs_type:
                if numeric_value < 40 or numeric_value > 300:
                    warnings.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message=f"Blood pressure value {numeric_value} is outside typical range (40-300)",
                            code="OUT_OF_RANGE",
                        )
                    )
            elif "heart rate" in vs_type or "pulse" in vs_type:
                if numeric_value < 20 or numeric_value > 250:
                    warnings.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message=f"Heart rate value {numeric_value} is outside typical range (20-250)",
                            code="OUT_OF_RANGE",
                        )
                    )
            elif "temperature" in vs_type or "temp" in vs_type:
                # Check both Celsius and Fahrenheit
                if numeric_value < 90:  # Likely Fahrenheit
                    if numeric_value < 90 or numeric_value > 110:
                        warnings.append(
                            ValidationIssue(
                                level=ValidationLevel.WARNING,
                                message=f"Temperature value {numeric_value}°F is outside typical range (90-110)",
                                code="OUT_OF_RANGE",
                            )
                        )
                else:  # Likely Celsius
                    if numeric_value < 30 or numeric_value > 45:
                        warnings.append(
                            ValidationIssue(
                                level=ValidationLevel.WARNING,
                                message=f"Temperature value {numeric_value}°C is outside typical range (30-45)",
                                code="OUT_OF_RANGE",
                            )
                        )
            elif "respiratory" in vs_type or "respiration" in vs_type:
                if numeric_value < 5 or numeric_value > 60:
                    warnings.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message=f"Respiratory rate value {numeric_value} is outside typical range (5-60)",
                            code="OUT_OF_RANGE",
                        )
                    )
            elif "oxygen" in vs_type or "spo2" in vs_type or "o2" in vs_type:
                if numeric_value < 50 or numeric_value > 100:
                    warnings.append(
                        ValidationIssue(
                            level=ValidationLevel.WARNING,
                            message=f"Oxygen saturation value {numeric_value} is outside typical range (50-100)",
                            code="OUT_OF_RANGE",
                        )
                    )
        except (ValueError, TypeError):
            # Value is not numeric, which is okay for some vital signs
            pass

        return ValidationResult(errors=errors, warnings=warnings)

    @staticmethod
    def _validate_result_observation(observation: Dict[str, Any]) -> ValidationResult:
        """Validate a single result observation."""
        errors = []
        warnings = []

        required = ["test_name", "test_code", "value", "status", "effective_time"]
        missing = DataValidator.validate_required_fields(observation, required)
        errors.extend(
            [
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Missing required field: {field}",
                    code="MISSING_FIELD",
                )
                for field in missing
            ]
        )

        if missing:
            return ValidationResult(errors=errors, warnings=warnings)

        # Validate test code (should be LOINC)
        test_code = observation.get("test_code")
        if test_code and not DataValidator.validate_code(test_code, "LOINC"):
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message=f"test_code '{test_code}' does not match expected LOINC format",
                    code="INVALID_CODE_FORMAT",
                )
            )

        # Validate status
        status = observation.get("status")
        if status and status not in DataValidator.VALID_RESULT_STATUS:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"status must be one of {DataValidator.VALID_RESULT_STATUS}, got '{status}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate effective time
        effective_time = observation.get("effective_time")
        if effective_time is not None and not isinstance(effective_time, (date, datetime)):
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message="effective_time must be a date or datetime object",
                    code="INVALID_TYPE",
                )
            )

        # Validate value_type if provided
        value_type = observation.get("value_type")
        if value_type and value_type not in DataValidator.VALID_VALUE_TYPES:
            errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"value_type must be one of {DataValidator.VALID_VALUE_TYPES}, got '{value_type}'",
                    code="INVALID_VALUE",
                )
            )

        # Validate reference range consistency
        ref_low = observation.get("reference_range_low")
        ref_high = observation.get("reference_range_high")
        ref_unit = observation.get("reference_range_unit")

        if (ref_low or ref_high) and not ref_unit:
            warnings.append(
                ValidationIssue(
                    level=ValidationLevel.WARNING,
                    message="Reference range provided but reference_range_unit is missing",
                    code="MISSING_FIELD",
                )
            )

        if ref_low and ref_high:
            try:
                low = float(ref_low)
                high = float(ref_high)
                if low >= high:
                    errors.append(
                        ValidationIssue(
                            level=ValidationLevel.ERROR,
                            message=f"reference_range_low ({low}) must be less than reference_range_high ({high})",
                            code="INVALID_RANGE",
                        )
                    )
            except (ValueError, TypeError):
                pass  # Non-numeric ranges are okay

        return ValidationResult(errors=errors, warnings=warnings)
