"""Tests for dictionary/JSON to C-CDA converters."""

import json
import tempfile
from datetime import date, datetime
from pathlib import Path

import pytest

from ccdakit.builders.document import ClinicalDocument
from ccdakit.core.base import CDAVersion
from ccdakit.utils.converters import DictToCCDAConverter


class TestDictToCCDAConverter:
    """Tests for DictToCCDAConverter."""

    @pytest.fixture
    def minimal_patient_data(self):
        """Minimal patient data for testing."""
        return {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1970-05-15",
            "sex": "M",
            "addresses": [],
            "telecoms": [],
        }

    @pytest.fixture
    def full_patient_data(self):
        """Complete patient data for testing."""
        return {
            "first_name": "John",
            "last_name": "Doe",
            "middle_name": "Q",
            "date_of_birth": "1970-05-15",
            "sex": "M",
            "race": "2106-3",
            "ethnicity": "2186-5",
            "language": "eng",
            "ssn": "123-45-6789",
            "marital_status": "M",
            "addresses": [
                {
                    "street_lines": ["123 Main St", "Apt 4B"],
                    "city": "Boston",
                    "state": "MA",
                    "postal_code": "02101",
                    "country": "US",
                }
            ],
            "telecoms": [
                {"type": "phone", "value": "617-555-1234", "use": "home"},
                {"type": "email", "value": "john.doe@example.com", "use": "home"},
            ],
        }

    @pytest.fixture
    def author_data(self):
        """Author data for testing."""
        return {
            "first_name": "Alice",
            "last_name": "Smith",
            "middle_name": "M",
            "npi": "9876543210",
            "time": "2024-01-15T10:30:00",
            "addresses": [
                {
                    "street_lines": ["456 Medical Plaza"],
                    "city": "Boston",
                    "state": "MA",
                    "postal_code": "02115",
                    "country": "US",
                }
            ],
            "telecoms": [{"type": "phone", "value": "617-555-5555", "use": "work"}],
            "organization": {
                "name": "Community Health Center",
                "npi": "1234567890",
                "oid_root": "2.16.840.1.113883.3.EXAMPLE",
                "addresses": [
                    {
                        "street_lines": ["789 Hospital Rd"],
                        "city": "Boston",
                        "state": "MA",
                        "postal_code": "02115",
                        "country": "US",
                    }
                ],
                "telecoms": [{"type": "phone", "value": "617-555-9999", "use": "work"}],
            },
        }

    @pytest.fixture
    def custodian_data(self):
        """Custodian organization data for testing."""
        return {
            "name": "Community Health Center",
            "npi": "1234567890",
            "tin": "12-3456789",
            "oid_root": "2.16.840.1.113883.3.EXAMPLE",
            "addresses": [
                {
                    "street_lines": ["789 Hospital Rd"],
                    "city": "Boston",
                    "state": "MA",
                    "postal_code": "02115",
                    "country": "US",
                }
            ],
            "telecoms": [{"type": "phone", "value": "617-555-9999", "use": "work"}],
        }

    @pytest.fixture
    def minimal_document_data(self, minimal_patient_data, author_data, custodian_data):
        """Minimal document data without sections."""
        return {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
        }

    @pytest.fixture
    def problems_data(self):
        """Sample problems data."""
        return [
            {
                "name": "Essential Hypertension",
                "code": "59621000",
                "code_system": "SNOMED",
                "status": "active",
                "onset_date": "2018-05-10",
            },
            {
                "name": "Type 2 Diabetes",
                "code": "44054006",
                "code_system": "SNOMED",
                "status": "active",
                "onset_date": "2019-03-15",
            },
            {
                "name": "Acute Bronchitis",
                "code": "10509002",
                "code_system": "SNOMED",
                "status": "resolved",
                "onset_date": "2023-01-05",
                "resolved_date": "2023-02-01",
            },
        ]

    @pytest.fixture
    def medications_data(self):
        """Sample medications data."""
        return [
            {
                "name": "Lisinopril 10mg oral tablet",
                "code": "314076",
                "dosage": "10 mg",
                "route": "oral",
                "frequency": "once daily",
                "start_date": "2018-06-01",
                "status": "active",
                "instructions": "Take in the morning",
            },
            {
                "name": "Metformin 500mg oral tablet",
                "code": "860975",
                "dosage": "500 mg",
                "route": "oral",
                "frequency": "twice daily",
                "start_date": "2019-04-01",
                "status": "active",
            },
        ]

    @pytest.fixture
    def allergies_data(self):
        """Sample allergies data."""
        return [
            {
                "allergen": "Penicillin",
                "allergen_code": "7980",
                "allergen_code_system": "RxNorm",
                "allergy_type": "allergy",
                "reaction": "Hives",
                "severity": "moderate",
                "status": "active",
                "onset_date": "2015-03-20",
            }
        ]

    @pytest.fixture
    def immunizations_data(self):
        """Sample immunizations data."""
        return [
            {
                "vaccine_name": "Influenza vaccine, seasonal",
                "cvx_code": "141",
                "administration_date": "2023-09-15",
                "status": "completed",
                "lot_number": "ABC123456",
                "manufacturer": "Sanofi Pasteur",
                "route": "intramuscular",
                "site": "left deltoid",
                "dose_quantity": "0.5 mL",
            }
        ]

    @pytest.fixture
    def vital_signs_data(self):
        """Sample vital signs data."""
        return [
            {
                "date": "2023-10-15T10:30:00",
                "vital_signs": [
                    {
                        "type": "Heart Rate",
                        "code": "8867-4",
                        "value": "72",
                        "unit": "bpm",
                        "date": "2023-10-15T10:30:00",
                        "interpretation": "Normal",
                    },
                    {
                        "type": "Systolic Blood Pressure",
                        "code": "8480-6",
                        "value": "120",
                        "unit": "mm[Hg]",
                        "date": "2023-10-15T10:30:00",
                        "interpretation": "Normal",
                    },
                ],
            }
        ]

    @pytest.fixture
    def procedures_data(self):
        """Sample procedures data."""
        return [
            {
                "name": "Appendectomy",
                "code": "80146002",
                "code_system": "SNOMED",
                "date": "2022-06-15",
                "status": "completed",
                "target_site": "Appendix",
            }
        ]

    @pytest.fixture
    def results_data(self):
        """Sample results data."""
        return [
            {
                "name": "Complete Blood Count",
                "code": "58410-2",
                "code_system": "LOINC",
                "date": "2023-10-15T09:00:00",
                "status": "completed",
                "results": [
                    {
                        "name": "Hemoglobin",
                        "code": "718-7",
                        "code_system": "LOINC",
                        "value": "14.5",
                        "unit": "g/dL",
                        "date": "2023-10-15T09:00:00",
                        "interpretation": "Normal",
                        "reference_range": "13.5-17.5 g/dL",
                    }
                ],
            }
        ]

    @pytest.fixture
    def encounters_data(self):
        """Sample encounters data."""
        return [
            {
                "type": "Office Visit",
                "code": "99213",
                "code_system": "CPT",
                "start_date": "2023-10-15",
                "status": "completed",
                "location": "Community Health Center",
                "performer": "Dr. Alice Smith",
            }
        ]

    @pytest.fixture
    def social_history_data(self):
        """Sample social history data."""
        return [
            {
                "status": "Former smoker",
                "code": "8517006",
                "code_system": "SNOMED",
                "date": "2023-10-15T10:30:00",
            }
        ]

    def test_from_dict_minimal_document(self, minimal_document_data):
        """Test creating document from minimal dict."""
        doc = DictToCCDAConverter.from_dict(minimal_document_data)

        assert isinstance(doc, ClinicalDocument)
        assert doc.patient.first_name == "John"
        assert doc.patient.last_name == "Doe"
        assert doc.patient.date_of_birth == date(1970, 5, 15)
        assert doc.patient.sex == "M"
        assert doc.author.first_name == "Alice"
        assert doc.author.last_name == "Smith"
        assert doc.custodian.name == "Community Health Center"
        assert len(doc.sections) == 0

    def test_from_dict_full_patient(self, full_patient_data, author_data, custodian_data):
        """Test creating document with full patient demographics."""
        data = {
            "patient": full_patient_data,
            "author": author_data,
            "custodian": custodian_data,
        }
        doc = DictToCCDAConverter.from_dict(data)

        patient = doc.patient
        assert patient.first_name == "John"
        assert patient.middle_name == "Q"
        assert patient.last_name == "Doe"
        assert patient.date_of_birth == date(1970, 5, 15)
        assert patient.sex == "M"
        assert patient.race == "2106-3"
        assert patient.ethnicity == "2186-5"
        assert patient.language == "eng"
        assert patient.ssn == "123-45-6789"
        assert patient.marital_status == "M"
        assert len(patient.addresses) == 1
        assert patient.addresses[0].city == "Boston"
        assert len(patient.telecoms) == 2
        assert patient.telecoms[0].type == "phone"

    def test_from_dict_with_problems_section(
        self, minimal_patient_data, author_data, custodian_data, problems_data
    ):
        """Test creating document with problems section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "problems", "title": "Problem List", "data": problems_data}],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        # Can generate XML without errors
        xml = doc.to_xml_string()
        assert "Problem List" in xml
        assert "Essential Hypertension" in xml

    def test_from_dict_with_medications_section(
        self, minimal_patient_data, author_data, custodian_data, medications_data
    ):
        """Test creating document with medications section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "medications", "title": "Medications", "data": medications_data}],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Medications" in xml
        assert "Lisinopril" in xml

    def test_from_dict_with_allergies_section(
        self, minimal_patient_data, author_data, custodian_data, allergies_data
    ):
        """Test creating document with allergies section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "allergies", "title": "Allergies", "data": allergies_data}],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Allergies" in xml
        assert "Penicillin" in xml

    def test_from_dict_with_immunizations_section(
        self, minimal_patient_data, author_data, custodian_data, immunizations_data
    ):
        """Test creating document with immunizations section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [
                {"type": "immunizations", "title": "Immunizations", "data": immunizations_data}
            ],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Immunizations" in xml
        assert "Influenza vaccine" in xml

    def test_from_dict_with_vital_signs_section(
        self, minimal_patient_data, author_data, custodian_data, vital_signs_data
    ):
        """Test creating document with vital signs section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "vital_signs", "title": "Vital Signs", "data": vital_signs_data}],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Vital Signs" in xml
        assert "Heart Rate" in xml

    def test_from_dict_with_procedures_section(
        self, minimal_patient_data, author_data, custodian_data, procedures_data
    ):
        """Test creating document with procedures section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "procedures", "title": "Procedures", "data": procedures_data}],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Procedures" in xml
        assert "Appendectomy" in xml

    def test_from_dict_with_results_section(
        self, minimal_patient_data, author_data, custodian_data, results_data
    ):
        """Test creating document with results section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "results", "title": "Lab Results", "data": results_data}],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Lab Results" in xml
        assert "Complete Blood Count" in xml

    def test_from_dict_with_encounters_section(
        self, minimal_patient_data, author_data, custodian_data, encounters_data
    ):
        """Test creating document with encounters section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "encounters", "title": "Encounters", "data": encounters_data}],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Encounters" in xml
        assert "Office Visit" in xml

    def test_from_dict_with_social_history_section(
        self, minimal_patient_data, author_data, custodian_data, social_history_data
    ):
        """Test creating document with social history section."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [
                {"type": "social_history", "title": "Social History", "data": social_history_data}
            ],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 1
        xml = doc.to_xml_string()
        assert "Social History" in xml

    def test_from_dict_with_multiple_sections(
        self,
        minimal_patient_data,
        author_data,
        custodian_data,
        problems_data,
        medications_data,
        allergies_data,
    ):
        """Test creating document with multiple sections."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [
                {"type": "problems", "title": "Problem List", "data": problems_data},
                {"type": "medications", "title": "Medications", "data": medications_data},
                {"type": "allergies", "title": "Allergies", "data": allergies_data},
            ],
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert len(doc.sections) == 3
        xml = doc.to_xml_string()
        assert "Problem List" in xml
        assert "Medications" in xml
        assert "Allergies" in xml
        assert "Essential Hypertension" in xml
        assert "Lisinopril" in xml
        assert "Penicillin" in xml

    def test_from_dict_with_document_metadata(
        self, minimal_patient_data, author_data, custodian_data
    ):
        """Test creating document with custom metadata."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "document": {
                "title": "Custom Patient Summary",
                "document_id": "DOC-12345",
                "effective_time": "2024-01-15T14:30:00",
                "version": "R2_1",
            },
        }
        doc = DictToCCDAConverter.from_dict(data)

        assert doc.title == "Custom Patient Summary"
        assert doc.document_id == "DOC-12345"
        assert doc.effective_time == datetime(2024, 1, 15, 14, 30, 0)
        assert doc.version == CDAVersion.R2_1

    def test_from_dict_missing_patient(self, author_data, custodian_data):
        """Test error when patient data is missing."""
        data = {"author": author_data, "custodian": custodian_data}
        with pytest.raises(ValueError, match="Missing required keys.*patient"):
            DictToCCDAConverter.from_dict(data)

    def test_from_dict_missing_author(self, minimal_patient_data, custodian_data):
        """Test error when author data is missing."""
        data = {"patient": minimal_patient_data, "custodian": custodian_data}
        with pytest.raises(ValueError, match="Missing required keys.*author"):
            DictToCCDAConverter.from_dict(data)

    def test_from_dict_missing_custodian(self, minimal_patient_data, author_data):
        """Test error when custodian data is missing."""
        data = {"patient": minimal_patient_data, "author": author_data}
        with pytest.raises(ValueError, match="Missing required keys.*custodian"):
            DictToCCDAConverter.from_dict(data)

    def test_from_dict_unknown_section_type(
        self, minimal_patient_data, author_data, custodian_data
    ):
        """Test error with unknown section type."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"type": "unknown_section", "data": []}],
        }
        with pytest.raises(ValueError, match="Unknown section type"):
            DictToCCDAConverter.from_dict(data)

    def test_from_dict_section_missing_type(
        self, minimal_patient_data, author_data, custodian_data
    ):
        """Test error when section is missing type field."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [{"data": []}],
        }
        with pytest.raises(ValueError, match="Section missing 'type' field"):
            DictToCCDAConverter.from_dict(data)

    def test_from_json_file(self, minimal_document_data):
        """Test loading document from JSON file."""
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(minimal_document_data, f)
            temp_path = f.name

        try:
            doc = DictToCCDAConverter.from_json_file(temp_path)
            assert isinstance(doc, ClinicalDocument)
            assert doc.patient.first_name == "John"
            assert doc.patient.last_name == "Doe"
        finally:
            Path(temp_path).unlink()

    def test_from_json_file_not_found(self):
        """Test error when JSON file does not exist."""
        with pytest.raises(FileNotFoundError):
            DictToCCDAConverter.from_json_file("/nonexistent/path/file.json")

    def test_from_json_file_invalid_json(self):
        """Test error with invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                DictToCCDAConverter.from_json_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_to_dict(self, minimal_document_data):
        """Test converting document to dictionary."""
        doc = DictToCCDAConverter.from_dict(minimal_document_data)
        result = DictToCCDAConverter.to_dict(doc)

        assert "document" in result
        assert result["document"]["title"] == "Clinical Summary"
        assert "document_id" in result["document"]
        assert "effective_time" in result["document"]
        assert result["document"]["version"] == "R2_1"
        assert result["sections"] == 0

    def test_date_conversion_from_string(self, minimal_patient_data, author_data, custodian_data):
        """Test that date strings are properly converted to date objects."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [
                {
                    "type": "problems",
                    "data": [
                        {
                            "name": "Test Problem",
                            "code": "12345",
                            "code_system": "SNOMED",
                            "status": "active",
                            "onset_date": "2020-01-15",
                        }
                    ],
                }
            ],
        }
        doc = DictToCCDAConverter.from_dict(data)
        xml = doc.to_xml_string()
        assert "Test Problem" in xml

    def test_patient_date_of_birth_already_date_object(self, author_data, custodian_data):
        """Test patient with date_of_birth as date object."""
        from datetime import date

        data = {
            "patient": {
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": date(1985, 6, 15),  # Already a date object
                "sex": "F",
                "addresses": [],
                "telecoms": [],
            },
            "author": author_data,
            "custodian": custodian_data,
        }
        doc = DictToCCDAConverter.from_dict(data)
        assert doc.patient.date_of_birth == date(1985, 6, 15)

    def test_datetime_conversion_from_string(
        self, minimal_patient_data, author_data, custodian_data
    ):
        """Test that datetime strings are properly converted to datetime objects."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [
                {
                    "type": "vital_signs",
                    "data": [
                        {
                            "date": "2023-10-15T10:30:00",
                            "vital_signs": [
                                {
                                    "type": "Heart Rate",
                                    "code": "8867-4",
                                    "value": "72",
                                    "unit": "bpm",
                                    "date": "2023-10-15T10:30:00",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        doc = DictToCCDAConverter.from_dict(data)
        xml = doc.to_xml_string()
        assert "Heart Rate" in xml

    def test_author_without_organization(self, minimal_patient_data, custodian_data):
        """Test author without organization."""
        author_data = {
            "first_name": "Bob",
            "last_name": "Jones",
            "npi": "1111111111",
            "addresses": [],
            "telecoms": [],
        }
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
        }
        doc = DictToCCDAConverter.from_dict(data)
        assert doc.author.first_name == "Bob"
        assert doc.author.organization is None

    def test_empty_sections_list(self, minimal_patient_data, author_data, custodian_data):
        """Test document with empty sections list."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [],
        }
        doc = DictToCCDAConverter.from_dict(data)
        assert len(doc.sections) == 0

    def test_section_without_title(self, minimal_patient_data, author_data, custodian_data):
        """Test section without custom title."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [
                {
                    "type": "problems",
                    "data": [
                        {
                            "name": "Test",
                            "code": "123",
                            "code_system": "SNOMED",
                            "status": "active",
                            "onset_date": "2020-01-01",
                        }
                    ],
                }
            ],
        }
        doc = DictToCCDAConverter.from_dict(data)
        assert len(doc.sections) == 1
        # Default title should be used
        xml = doc.to_xml_string()
        assert "Problem" in xml

    def test_optional_fields_in_medication(self, minimal_patient_data, author_data, custodian_data):
        """Test medication with optional fields omitted."""
        data = {
            "patient": minimal_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "sections": [
                {
                    "type": "medications",
                    "data": [
                        {
                            "name": "Test Med",
                            "code": "123",
                            "dosage": "10 mg",
                            "route": "oral",
                            "frequency": "daily",
                            "start_date": "2020-01-01",
                            # No end_date, no instructions
                        }
                    ],
                }
            ],
        }
        doc = DictToCCDAConverter.from_dict(data)
        xml = doc.to_xml_string()
        assert "Test Med" in xml

    def test_comprehensive_document(
        self,
        full_patient_data,
        author_data,
        custodian_data,
        problems_data,
        medications_data,
        allergies_data,
        immunizations_data,
        vital_signs_data,
    ):
        """Test creating a comprehensive document with all supported sections."""
        data = {
            "patient": full_patient_data,
            "author": author_data,
            "custodian": custodian_data,
            "document": {
                "title": "Comprehensive Patient Summary",
                "document_id": "DOC-COMPREHENSIVE-001",
                "effective_time": "2024-01-15T14:30:00",
                "version": "R2_1",
            },
            "sections": [
                {"type": "problems", "title": "Problem List", "data": problems_data},
                {"type": "medications", "title": "Medications", "data": medications_data},
                {"type": "allergies", "title": "Allergies", "data": allergies_data},
                {"type": "immunizations", "title": "Immunizations", "data": immunizations_data},
                {"type": "vital_signs", "title": "Vital Signs", "data": vital_signs_data},
            ],
        }

        doc = DictToCCDAConverter.from_dict(data)

        # Verify document structure
        assert doc.title == "Comprehensive Patient Summary"
        assert doc.document_id == "DOC-COMPREHENSIVE-001"
        assert len(doc.sections) == 5

        # Verify patient data
        assert doc.patient.first_name == "John"
        assert doc.patient.middle_name == "Q"
        assert doc.patient.last_name == "Doe"
        assert len(doc.patient.addresses) == 1
        assert len(doc.patient.telecoms) == 2

        # Verify XML generation
        xml = doc.to_xml_string()
        assert "Comprehensive Patient Summary" in xml
        assert "Problem List" in xml
        assert "Medications" in xml
        assert "Allergies" in xml
        assert "Essential Hypertension" in xml
        assert "Lisinopril" in xml
        assert "Penicillin" in xml
        assert "Influenza vaccine" in xml
        assert "Heart Rate" in xml

        # Verify it's valid XML (handle both single and double quotes)
        assert xml.startswith("<?xml version=") and "encoding=" in xml
        assert "ClinicalDocument" in xml
