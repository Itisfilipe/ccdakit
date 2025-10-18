"""Pre-configured document templates with sample data for quick document generation."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class DocumentTemplates:
    """Pre-configured templates for quick document generation."""

    TEMPLATE_DIR = Path(__file__).parent / "templates"

    @staticmethod
    def _load_template(filename: str) -> Dict[str, Any]:
        """
        Load a JSON template file.

        Args:
            filename: Name of the template file (e.g., 'minimal_ccd.json')

        Returns:
            Dictionary containing template data

        Raises:
            FileNotFoundError: If template file doesn't exist
            json.JSONDecodeError: If template file is invalid JSON
        """
        template_path = DocumentTemplates.TEMPLATE_DIR / filename
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        with open(template_path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _convert_dates(data: Any) -> Any:
        """
        Recursively convert ISO date strings to date/datetime objects.

        Args:
            data: Data structure (dict, list, or primitive)

        Returns:
            Data structure with dates converted to date/datetime objects
        """
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if key in (
                    "date_of_birth",
                    "onset_date",
                    "resolved_date",
                    "start_date",
                    "end_date",
                ):
                    # Convert to date object
                    if value and isinstance(value, str):
                        try:
                            result[key] = datetime.fromisoformat(value).date()
                        except (ValueError, AttributeError):
                            result[key] = value
                    else:
                        result[key] = value
                elif key in ("time", "date", "administration_date", "effective_time"):
                    # Convert to datetime object
                    if value and isinstance(value, str):
                        try:
                            result[key] = datetime.fromisoformat(value)
                        except (ValueError, AttributeError):
                            result[key] = value
                    else:
                        result[key] = value
                else:
                    result[key] = DocumentTemplates._convert_dates(value)
            return result
        elif isinstance(data, list):
            return [DocumentTemplates._convert_dates(item) for item in data]
        else:
            return data

    @staticmethod
    def _create_simple_class(name: str, data: Dict[str, Any]) -> Any:
        """
        Create a simple class instance from a dictionary.

        Args:
            name: Name for the class
            data: Dictionary of attributes

        Returns:
            Class instance with attributes set from data
        """

        class SimpleClass:
            """Simple class to hold template data."""

            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            def __repr__(self):
                attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
                return f"{name}({attrs})"

        return SimpleClass(**data)

    @staticmethod
    def _hydrate_template(template_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert template data into protocol-compliant objects.

        Args:
            template_data: Raw template data from JSON

        Returns:
            Dictionary with data converted to protocol-compliant objects
        """
        result = {}

        # Convert dates
        template_data = DocumentTemplates._convert_dates(template_data)

        # Convert patient
        if "patient" in template_data:
            patient_data = template_data["patient"]

            # Convert addresses
            if "addresses" in patient_data:
                addresses = []
                for addr in patient_data["addresses"]:
                    addresses.append(DocumentTemplates._create_simple_class("Address", addr))
                patient_data["addresses"] = addresses

            # Convert telecoms
            if "telecoms" in patient_data:
                telecoms = []
                for tc in patient_data["telecoms"]:
                    telecoms.append(DocumentTemplates._create_simple_class("Telecom", tc))
                patient_data["telecoms"] = telecoms

            result["patient"] = DocumentTemplates._create_simple_class("Patient", patient_data)

        # Convert author
        if "author" in template_data:
            author_data = template_data["author"]

            # Convert addresses
            if "addresses" in author_data:
                addresses = []
                for addr in author_data["addresses"]:
                    addresses.append(DocumentTemplates._create_simple_class("Address", addr))
                author_data["addresses"] = addresses

            # Convert telecoms
            if "telecoms" in author_data:
                telecoms = []
                for tc in author_data["telecoms"]:
                    telecoms.append(DocumentTemplates._create_simple_class("Telecom", tc))
                author_data["telecoms"] = telecoms

            # Convert organization
            if "organization" in author_data:
                org_data = author_data["organization"]

                # Convert org addresses
                if "addresses" in org_data:
                    addresses = []
                    for addr in org_data["addresses"]:
                        addresses.append(DocumentTemplates._create_simple_class("Address", addr))
                    org_data["addresses"] = addresses

                # Convert org telecoms
                if "telecoms" in org_data:
                    telecoms = []
                    for tc in org_data["telecoms"]:
                        telecoms.append(DocumentTemplates._create_simple_class("Telecom", tc))
                    org_data["telecoms"] = telecoms

                author_data["organization"] = DocumentTemplates._create_simple_class(
                    "Organization", org_data
                )

            result["author"] = DocumentTemplates._create_simple_class("Author", author_data)

        # Convert custodian
        if "custodian" in template_data:
            custodian_data = template_data["custodian"]

            # Convert addresses
            if "addresses" in custodian_data:
                addresses = []
                for addr in custodian_data["addresses"]:
                    addresses.append(DocumentTemplates._create_simple_class("Address", addr))
                custodian_data["addresses"] = addresses

            # Convert telecoms
            if "telecoms" in custodian_data:
                telecoms = []
                for tc in custodian_data["telecoms"]:
                    telecoms.append(DocumentTemplates._create_simple_class("Telecom", tc))
                custodian_data["telecoms"] = telecoms

            result["custodian"] = DocumentTemplates._create_simple_class(
                "Organization", custodian_data
            )

        # Convert sections data
        if "sections" in template_data:
            sections = {}

            # Problems
            if "problems" in template_data["sections"]:
                problems = []
                for prob in template_data["sections"]["problems"]:
                    problems.append(DocumentTemplates._create_simple_class("Problem", prob))
                sections["problems"] = problems

            # Medications
            if "medications" in template_data["sections"]:
                medications = []
                for med in template_data["sections"]["medications"]:
                    medications.append(DocumentTemplates._create_simple_class("Medication", med))
                sections["medications"] = medications

            # Allergies
            if "allergies" in template_data["sections"]:
                allergies = []
                for allergy in template_data["sections"]["allergies"]:
                    allergies.append(DocumentTemplates._create_simple_class("Allergy", allergy))
                sections["allergies"] = allergies

            # Immunizations
            if "immunizations" in template_data["sections"]:
                immunizations = []
                for imm in template_data["sections"]["immunizations"]:
                    immunizations.append(
                        DocumentTemplates._create_simple_class("Immunization", imm)
                    )
                sections["immunizations"] = immunizations

            # Vital Signs
            if "vital_signs" in template_data["sections"]:
                vital_signs = []
                for vs_org in template_data["sections"]["vital_signs"]:
                    # Convert individual vital signs within organizer
                    if "vital_signs" in vs_org:
                        signs = []
                        for vs in vs_org["vital_signs"]:
                            signs.append(DocumentTemplates._create_simple_class("VitalSign", vs))
                        vs_org["vital_signs"] = signs
                    vital_signs.append(
                        DocumentTemplates._create_simple_class("VitalSignsOrganizer", vs_org)
                    )
                sections["vital_signs"] = vital_signs

            # Procedures
            if "procedures" in template_data["sections"]:
                procedures = []
                for proc in template_data["sections"]["procedures"]:
                    procedures.append(DocumentTemplates._create_simple_class("Procedure", proc))
                sections["procedures"] = procedures

            # Results
            if "results" in template_data["sections"]:
                results = []
                for result_org in template_data["sections"]["results"]:
                    # Convert individual results within organizer
                    if "results" in result_org:
                        res_list = []
                        for res in result_org["results"]:
                            res_list.append(DocumentTemplates._create_simple_class("Result", res))
                        result_org["results"] = res_list
                    results.append(
                        DocumentTemplates._create_simple_class("ResultOrganizer", result_org)
                    )
                sections["results"] = results

            # Encounters
            if "encounters" in template_data["sections"]:
                encounters = []
                for enc in template_data["sections"]["encounters"]:
                    encounters.append(DocumentTemplates._create_simple_class("Encounter", enc))
                sections["encounters"] = encounters

            # Social History
            if "smoking_status" in template_data["sections"]:
                smoking_status = []
                for ss in template_data["sections"]["smoking_status"]:
                    smoking_status.append(
                        DocumentTemplates._create_simple_class("SmokingStatus", ss)
                    )
                sections["smoking_status"] = smoking_status

            result["sections"] = sections

        # Copy metadata
        if "metadata" in template_data:
            result["metadata"] = template_data["metadata"]

        return result

    @staticmethod
    def minimal_ccd_template() -> Dict[str, Any]:
        """
        Return minimal CCD structure with placeholder data.

        Returns a minimal but complete C-CDA document with:
        - Patient demographics
        - Single author
        - Custodian organization
        - Basic problem list section

        Returns:
            Dictionary containing patient, author, custodian, and sections data

        Example:
            >>> template = DocumentTemplates.minimal_ccd_template()
            >>> patient = template["patient"]
            >>> print(patient.first_name)
            'Jane'
        """
        template_data = DocumentTemplates._load_template("minimal_ccd.json")
        return DocumentTemplates._hydrate_template(template_data)

    @staticmethod
    def full_ccd_template() -> Dict[str, Any]:
        """
        Return fully populated CCD example with all sections.

        Returns a comprehensive C-CDA document with:
        - Complete patient demographics
        - Author with full contact information
        - Custodian organization
        - All major clinical sections:
          - Problems
          - Medications
          - Allergies
          - Immunizations
          - Vital Signs
          - Procedures
          - Results
          - Encounters
          - Social History

        Returns:
            Dictionary containing complete patient record with all sections

        Example:
            >>> template = DocumentTemplates.full_ccd_template()
            >>> problems = template["sections"]["problems"]
            >>> print(len(problems))
            3
        """
        template_data = DocumentTemplates._load_template("full_ccd.json")
        return DocumentTemplates._hydrate_template(template_data)

    @staticmethod
    def empty_template(document_type: str) -> Dict[str, Any]:
        """
        Return empty template for specified document type.

        Provides a skeleton structure with minimal required fields for:
        - discharge_summary: Hospital discharge documentation
        - progress_note: Clinical progress notes
        - ccd: Continuity of Care Document

        Args:
            document_type: Type of document ('discharge_summary', 'progress_note', 'ccd')

        Returns:
            Dictionary with empty/placeholder structure for the document type

        Raises:
            ValueError: If document_type is not supported

        Example:
            >>> template = DocumentTemplates.empty_template("discharge_summary")
            >>> metadata = template["metadata"]
            >>> print(metadata["title"])
            'Hospital Discharge Summary'
        """
        valid_types = {
            "discharge_summary": "discharge_summary.json",
            "progress_note": "progress_note.json",
            "ccd": "minimal_ccd.json",
        }

        if document_type not in valid_types:
            raise ValueError(
                f"Unsupported document type: {document_type}. "
                f"Valid types: {', '.join(valid_types.keys())}"
            )

        filename = valid_types[document_type]
        template_data = DocumentTemplates._load_template(filename)
        return DocumentTemplates._hydrate_template(template_data)

    @staticmethod
    def list_available_templates() -> List[str]:
        """
        List all available template files.

        Returns:
            List of template filenames without extensions

        Example:
            >>> templates = DocumentTemplates.list_available_templates()
            >>> print(templates)
            ['minimal_ccd', 'full_ccd', 'discharge_summary', 'progress_note']
        """
        if not DocumentTemplates.TEMPLATE_DIR.exists():
            return []

        templates = []
        for file in DocumentTemplates.TEMPLATE_DIR.glob("*.json"):
            templates.append(file.stem)

        return sorted(templates)
