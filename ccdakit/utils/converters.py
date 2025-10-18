"""Converters for transforming dictionary/JSON data into C-CDA documents.

This module provides utilities to convert dictionary and JSON data structures
into properly formatted C-CDA documents using the pyccda builders.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.builders.sections.encounters import EncountersSection
from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.builders.sections.procedures import ProceduresSection
from ccdakit.builders.sections.results import ResultsSection
from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.builders.sections.vital_signs import VitalSignsSection
from ccdakit.core.base import CDAVersion


class DictToCCDAConverter:
    """Convert dictionary/JSON data to C-CDA documents.

    This converter supports a flexible JSON/dict format that maps to pyccda's
    protocol-based builders. The expected format includes patient demographics,
    author information, custodian organization, and clinical sections.

    Example:
        >>> converter = DictToCCDAConverter()
        >>> data = {
        ...     "patient": {...},
        ...     "author": {...},
        ...     "custodian": {...},
        ...     "sections": [
        ...         {"type": "problems", "data": [...]},
        ...         {"type": "medications", "data": [...]},
        ...     ],
        ... }
        >>> document = converter.from_dict(data)
        >>> xml = document.to_xml_string()
    """

    # Map section types to their builders
    SECTION_BUILDERS = {
        "problems": ProblemsSection,
        "medications": MedicationsSection,
        "allergies": AllergiesSection,
        "immunizations": ImmunizationsSection,
        "vital_signs": VitalSignsSection,
        "procedures": ProceduresSection,
        "results": ResultsSection,
        "encounters": EncountersSection,
        "social_history": SocialHistorySection,
    }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> ClinicalDocument:
        """Convert dictionary to C-CDA document.

        Expected format:
        {
            "patient": {
                "first_name": "John",
                "last_name": "Doe",
                "middle_name": "Q",
                "date_of_birth": "1970-05-15",  # ISO format
                "sex": "M",
                "race": "2106-3",
                "ethnicity": "2186-5",
                "language": "eng",
                "ssn": "123-45-6789",
                "marital_status": "M",
                "addresses": [...],
                "telecoms": [...]
            },
            "author": {
                "first_name": "Alice",
                "last_name": "Smith",
                "middle_name": "M",
                "npi": "9876543210",
                "time": "2024-01-15T10:30:00",  # ISO format
                "addresses": [...],
                "telecoms": [...],
                "organization": {...}
            },
            "custodian": {
                "name": "Community Health Center",
                "npi": "1234567890",
                "tin": null,
                "oid_root": "2.16.840.1.113883.3.EXAMPLE",
                "addresses": [...],
                "telecoms": [...]
            },
            "document": {
                "title": "Patient Clinical Summary",
                "document_id": "DOC-123",
                "effective_time": "2024-01-15T14:30:00",
                "version": "R2_1"
            },
            "sections": [
                {
                    "type": "problems",
                    "title": "Problem List",
                    "data": [...]
                },
                {
                    "type": "medications",
                    "title": "Medications",
                    "data": [...]
                }
            ]
        }

        Args:
            data: Dictionary containing patient, author, custodian, and sections data

        Returns:
            ClinicalDocument instance ready to generate XML

        Raises:
            ValueError: If required fields are missing or invalid
            KeyError: If expected dictionary keys are not found
        """
        # Validate required top-level keys
        required_keys = ["patient", "author", "custodian"]
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

        # Convert patient data
        patient = DictToCCDAConverter._dict_to_patient(data["patient"])

        # Convert author data
        author = DictToCCDAConverter._dict_to_author(data["author"])

        # Convert custodian data
        custodian = DictToCCDAConverter._dict_to_organization(data["custodian"])

        # Get document metadata
        doc_metadata = data.get("document", {})
        title = doc_metadata.get("title", "Clinical Summary")
        document_id = doc_metadata.get("document_id")
        effective_time = doc_metadata.get("effective_time")
        if effective_time and isinstance(effective_time, str):
            effective_time = datetime.fromisoformat(effective_time)
        version_str = doc_metadata.get("version", "R2_1")
        version = CDAVersion[version_str] if isinstance(version_str, str) else version_str

        # Build sections if provided
        sections = []
        if "sections" in data:
            sections = DictToCCDAConverter._build_sections(data["sections"], version)

        # Create and return document
        return ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=sections,
            document_id=document_id,
            title=title,
            effective_time=effective_time,
            version=version,
        )

    @staticmethod
    def from_json_file(filepath: Union[str, Path]) -> ClinicalDocument:
        """Load JSON file and convert to C-CDA document.

        Args:
            filepath: Path to JSON file containing C-CDA data

        Returns:
            ClinicalDocument instance

        Raises:
            FileNotFoundError: If file does not exist
            json.JSONDecodeError: If file contains invalid JSON
            ValueError: If JSON structure is invalid
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"JSON file not found: {filepath}")

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        return DictToCCDAConverter.from_dict(data)

    @staticmethod
    def to_dict(document: ClinicalDocument) -> Dict[str, Any]:
        """Convert C-CDA document to dictionary.

        Note: This provides a basic conversion of document metadata.
        Full round-trip conversion (XML -> dict) is not yet implemented.

        Args:
            document: ClinicalDocument instance

        Returns:
            Dictionary representation of document metadata
        """
        return {
            "document": {
                "title": document.title,
                "document_id": document.document_id,
                "effective_time": document.effective_time.isoformat()
                if document.effective_time
                else None,
                "version": document.version.name,
            },
            "sections": len(document.sections),
        }

    # Helper methods for converting data structures

    @staticmethod
    def _dict_to_patient(data: Dict[str, Any]) -> object:
        """Convert dictionary to Patient object."""

        class Patient:
            def __init__(self, data: Dict[str, Any]):
                self.first_name = data["first_name"]
                self.last_name = data["last_name"]
                self.middle_name = data.get("middle_name")
                # Convert date string to date object
                dob = data["date_of_birth"]
                if isinstance(dob, str):
                    self.date_of_birth = datetime.fromisoformat(dob).date()
                else:
                    self.date_of_birth = dob
                self.sex = data["sex"]
                self.race = data.get("race")
                self.ethnicity = data.get("ethnicity")
                self.language = data.get("language")
                self.ssn = data.get("ssn")
                self.marital_status = data.get("marital_status")
                # Convert addresses
                self.addresses = [
                    DictToCCDAConverter._dict_to_address(addr) for addr in data.get("addresses", [])
                ]
                # Convert telecoms
                self.telecoms = [
                    DictToCCDAConverter._dict_to_telecom(tel) for tel in data.get("telecoms", [])
                ]

        return Patient(data)

    @staticmethod
    def _dict_to_address(data: Dict[str, Any]) -> object:
        """Convert dictionary to Address object."""

        class Address:
            def __init__(self, data: Dict[str, Any]):
                self.street_lines = data.get("street_lines", [])
                self.city = data["city"]
                self.state = data["state"]
                self.postal_code = data["postal_code"]
                self.country = data.get("country", "US")

        return Address(data)

    @staticmethod
    def _dict_to_telecom(data: Dict[str, Any]) -> object:
        """Convert dictionary to Telecom object."""

        class Telecom:
            def __init__(self, data: Dict[str, Any]):
                self.type = data["type"]
                self.value = data["value"]
                self.use = data.get("use")

        return Telecom(data)

    @staticmethod
    def _dict_to_organization(data: Dict[str, Any]) -> object:
        """Convert dictionary to Organization object."""

        class Organization:
            def __init__(self, data: Dict[str, Any]):
                self.name = data["name"]
                self.npi = data.get("npi")
                self.tin = data.get("tin")
                self.oid_root = data.get("oid_root")
                self.addresses = [
                    DictToCCDAConverter._dict_to_address(addr) for addr in data.get("addresses", [])
                ]
                self.telecoms = [
                    DictToCCDAConverter._dict_to_telecom(tel) for tel in data.get("telecoms", [])
                ]

        return Organization(data)

    @staticmethod
    def _dict_to_author(data: Dict[str, Any]) -> object:
        """Convert dictionary to Author object."""

        class Author:
            def __init__(self, data: Dict[str, Any]):
                self.first_name = data["first_name"]
                self.last_name = data["last_name"]
                self.middle_name = data.get("middle_name")
                self.npi = data.get("npi")
                # Convert time string to datetime
                time_val = data.get("time")
                if time_val:
                    if isinstance(time_val, str):
                        self.time = datetime.fromisoformat(time_val)
                    else:
                        self.time = time_val
                else:
                    self.time = datetime.now()
                self.addresses = [
                    DictToCCDAConverter._dict_to_address(addr) for addr in data.get("addresses", [])
                ]
                self.telecoms = [
                    DictToCCDAConverter._dict_to_telecom(tel) for tel in data.get("telecoms", [])
                ]
                # Convert organization if present
                org_data = data.get("organization")
                self.organization = (
                    DictToCCDAConverter._dict_to_organization(org_data) if org_data else None
                )

        return Author(data)

    @staticmethod
    def _build_sections(sections_data: List[Dict[str, Any]], version: CDAVersion) -> List:
        """Build section objects from section data.

        Args:
            sections_data: List of section dictionaries
            version: C-CDA version to use

        Returns:
            List of section builder instances
        """
        sections = []
        for section_def in sections_data:
            section_type = section_def.get("type")
            if not section_type:
                raise ValueError("Section missing 'type' field")

            if section_type not in DictToCCDAConverter.SECTION_BUILDERS:
                raise ValueError(f"Unknown section type: {section_type}")

            section_title = section_def.get("title")
            section_data = section_def.get("data", [])

            # Convert section data to appropriate objects
            converted_data = DictToCCDAConverter._convert_section_data(section_type, section_data)

            # Get the section builder class
            builder_class = DictToCCDAConverter.SECTION_BUILDERS[section_type]

            # Create section with appropriate parameters
            section_params = {"version": version}
            if section_title:
                section_params["title"] = section_title

            # Different sections use different parameter names for their data
            if section_type == "problems":
                section_params["problems"] = converted_data
            elif section_type == "medications":
                section_params["medications"] = converted_data
            elif section_type == "allergies":
                section_params["allergies"] = converted_data
            elif section_type == "immunizations":
                section_params["immunizations"] = converted_data
            elif section_type == "vital_signs":
                section_params["vital_signs_organizers"] = converted_data
            elif section_type == "procedures":
                section_params["procedures"] = converted_data
            elif section_type == "results":
                section_params["result_organizers"] = converted_data
            elif section_type == "encounters":
                section_params["encounters"] = converted_data
            elif section_type == "social_history":
                section_params["smoking_statuses"] = converted_data

            section = builder_class(**section_params)
            sections.append(section)

        return sections

    @staticmethod
    def _convert_section_data(section_type: str, data: List[Dict[str, Any]]) -> List:
        """Convert section data to appropriate protocol objects.

        Args:
            section_type: Type of section (problems, medications, etc.)
            data: List of dictionaries containing section data

        Returns:
            List of protocol-compliant objects
        """
        converters = {
            "problems": DictToCCDAConverter._dict_to_problem,
            "medications": DictToCCDAConverter._dict_to_medication,
            "allergies": DictToCCDAConverter._dict_to_allergy,
            "immunizations": DictToCCDAConverter._dict_to_immunization,
            "vital_signs": DictToCCDAConverter._dict_to_vital_signs_organizer,
            "procedures": DictToCCDAConverter._dict_to_procedure,
            "results": DictToCCDAConverter._dict_to_result_organizer,
            "encounters": DictToCCDAConverter._dict_to_encounter,
            "social_history": DictToCCDAConverter._dict_to_smoking_status,
        }

        converter = converters.get(section_type)
        if not converter:
            raise ValueError(f"No converter for section type: {section_type}")

        return [converter(item) for item in data]

    @staticmethod
    def _dict_to_problem(data: Dict[str, Any]) -> object:
        """Convert dictionary to Problem object."""

        class Problem:
            def __init__(self, data: Dict[str, Any]):
                self.name = data["name"]
                self.code = data["code"]
                self.code_system = data["code_system"]
                self.status = data.get("status", "active")
                # Convert date strings
                onset = data.get("onset_date")
                self.onset_date = (
                    datetime.fromisoformat(onset).date() if isinstance(onset, str) else onset
                )
                resolved = data.get("resolved_date")
                self.resolved_date = (
                    datetime.fromisoformat(resolved).date()
                    if isinstance(resolved, str)
                    else resolved
                )
                self.persistent_id = None

        return Problem(data)

    @staticmethod
    def _dict_to_medication(data: Dict[str, Any]) -> object:
        """Convert dictionary to Medication object."""

        class Medication:
            def __init__(self, data: Dict[str, Any]):
                self.name = data["name"]
                self.code = data["code"]
                self.dosage = data["dosage"]
                self.route = data["route"]
                self.frequency = data["frequency"]
                # Convert date strings
                start = data["start_date"]
                self.start_date = (
                    datetime.fromisoformat(start).date() if isinstance(start, str) else start
                )
                end = data.get("end_date")
                self.end_date = datetime.fromisoformat(end).date() if isinstance(end, str) else end
                self.status = data.get("status", "active")
                self.instructions = data.get("instructions")

        return Medication(data)

    @staticmethod
    def _dict_to_allergy(data: Dict[str, Any]) -> object:
        """Convert dictionary to Allergy object."""

        class Allergy:
            def __init__(self, data: Dict[str, Any]):
                self.allergen = data["allergen"]
                self.allergen_code = data.get("allergen_code")
                self.allergen_code_system = data.get("allergen_code_system")
                self.allergy_type = data.get("allergy_type", "allergy")
                self.reaction = data.get("reaction")
                self.severity = data.get("severity")
                self.status = data.get("status", "active")
                onset = data.get("onset_date")
                self.onset_date = (
                    datetime.fromisoformat(onset).date() if isinstance(onset, str) else onset
                )

        return Allergy(data)

    @staticmethod
    def _dict_to_immunization(data: Dict[str, Any]) -> object:
        """Convert dictionary to Immunization object."""

        class Immunization:
            def __init__(self, data: Dict[str, Any]):
                self.vaccine_name = data["vaccine_name"]
                self.cvx_code = data["cvx_code"]
                admin_date = data["administration_date"]
                self.administration_date = (
                    datetime.fromisoformat(admin_date).date()
                    if isinstance(admin_date, str)
                    else admin_date
                )
                self.status = data.get("status", "completed")
                self.lot_number = data.get("lot_number")
                self.manufacturer = data.get("manufacturer")
                self.route = data.get("route")
                self.site = data.get("site")
                self.dose_quantity = data.get("dose_quantity")

        return Immunization(data)

    @staticmethod
    def _dict_to_vital_signs_organizer(data: Dict[str, Any]) -> object:
        """Convert dictionary to VitalSignsOrganizer object."""

        class VitalSignsOrganizer:
            def __init__(self, data: Dict[str, Any]):
                organizer_date = data["date"]
                self.date = (
                    datetime.fromisoformat(organizer_date)
                    if isinstance(organizer_date, str)
                    else organizer_date
                )
                self.vital_signs = [
                    DictToCCDAConverter._dict_to_vital_sign(vs)
                    for vs in data.get("vital_signs", [])
                ]

        return VitalSignsOrganizer(data)

    @staticmethod
    def _dict_to_vital_sign(data: Dict[str, Any]) -> object:
        """Convert dictionary to VitalSign object."""

        class VitalSign:
            def __init__(self, data: Dict[str, Any]):
                self.type = data["type"]
                self.code = data["code"]
                self.value = data["value"]
                self.unit = data["unit"]
                vs_date = data["date"]
                self.date = datetime.fromisoformat(vs_date) if isinstance(vs_date, str) else vs_date
                self.interpretation = data.get("interpretation")

        return VitalSign(data)

    @staticmethod
    def _dict_to_procedure(data: Dict[str, Any]) -> object:
        """Convert dictionary to Procedure object."""

        class Procedure:
            def __init__(self, data: Dict[str, Any]):
                self.name = data["name"]
                self.code = data["code"]
                self.code_system = data["code_system"]
                proc_date = data.get("date")
                self.date = (
                    datetime.fromisoformat(proc_date).date()
                    if isinstance(proc_date, str) and proc_date
                    else proc_date
                )
                self.status = data.get("status", "completed")
                self.target_site = data.get("target_site")
                self.target_site_code = data.get("target_site_code")
                self.performer_name = data.get("performer_name")

        return Procedure(data)

    @staticmethod
    def _dict_to_result_organizer(data: Dict[str, Any]) -> object:
        """Convert dictionary to ResultOrganizer object."""

        class ResultOrganizer:
            def __init__(self, data: Dict[str, Any]):
                # Map to protocol properties
                self.panel_name = data.get("name", data.get("panel_name", ""))
                self.panel_code = data.get("code", data.get("panel_code", ""))
                org_date = data.get("date", data.get("effective_time"))
                self.effective_time = (
                    datetime.fromisoformat(org_date) if isinstance(org_date, str) else org_date
                )
                self.status = data.get("status", "completed")
                self.results = [
                    DictToCCDAConverter._dict_to_result(r) for r in data.get("results", [])
                ]

        return ResultOrganizer(data)

    @staticmethod
    def _dict_to_result(data: Dict[str, Any]) -> object:
        """Convert dictionary to Result object."""

        class Result:
            def __init__(self, data: Dict[str, Any]):
                # Map to protocol properties
                self.test_name = data.get("name", data.get("test_name", ""))
                self.test_code = data.get("code", data.get("test_code", ""))
                self.value = data["value"]
                self.unit = data.get("unit")
                result_date = data.get("date", data.get("effective_time"))
                self.effective_time = (
                    datetime.fromisoformat(result_date)
                    if isinstance(result_date, str)
                    else result_date
                )
                self.status = data.get("status", "completed")
                self.value_type = data.get("value_type")
                self.interpretation = data.get("interpretation")
                # Parse reference range
                ref_range = data.get("reference_range")
                if ref_range and isinstance(ref_range, str):
                    # Try to parse "low-high unit" format
                    parts = ref_range.split()
                    if len(parts) >= 2 and "-" in parts[0]:
                        range_parts = parts[0].split("-")
                        if len(range_parts) == 2:
                            self.reference_range_low = range_parts[0]
                            self.reference_range_high = range_parts[1]
                            self.reference_range_unit = (
                                " ".join(parts[1:]) if len(parts) > 1 else self.unit
                            )
                        else:
                            self.reference_range_low = None
                            self.reference_range_high = None
                            self.reference_range_unit = None
                    else:
                        self.reference_range_low = None
                        self.reference_range_high = None
                        self.reference_range_unit = None
                else:
                    self.reference_range_low = data.get("reference_range_low")
                    self.reference_range_high = data.get("reference_range_high")
                    self.reference_range_unit = data.get("reference_range_unit")

        return Result(data)

    @staticmethod
    def _dict_to_encounter(data: Dict[str, Any]) -> object:
        """Convert dictionary to Encounter object."""

        class Encounter:
            def __init__(self, data: Dict[str, Any]):
                # Map to protocol properties
                self.encounter_type = data.get("type", data.get("encounter_type", ""))
                self.code = data["code"]
                self.code_system = data.get("code_system", "CPT")
                # Support both 'date' and 'start_date'
                start = data.get("start_date", data.get("date"))
                self.date = (
                    datetime.fromisoformat(start).date() if isinstance(start, str) else start
                )
                end = data.get("end_date")
                self.end_date = (
                    datetime.fromisoformat(end).date() if isinstance(end, str) and end else end
                )
                self.location = data.get("location")
                self.performer_name = data.get("performer", data.get("performer_name"))
                self.discharge_disposition = data.get("discharge_disposition")

        return Encounter(data)

    @staticmethod
    def _dict_to_smoking_status(data: Dict[str, Any]) -> object:
        """Convert dictionary to SmokingStatus object."""

        class SmokingStatus:
            def __init__(self, data: Dict[str, Any]):
                # Map to protocol properties
                self.smoking_status = data.get("status", data.get("smoking_status", ""))
                self.code = data["code"]
                obs_date = data["date"]
                self.date = (
                    datetime.fromisoformat(obs_date) if isinstance(obs_date, str) else obs_date
                )

        return SmokingStatus(data)
