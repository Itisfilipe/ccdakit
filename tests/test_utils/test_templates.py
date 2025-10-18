"""Tests for document templates."""

import json
from datetime import date, datetime

import pytest

from ccdakit.utils.templates import DocumentTemplates


class TestDocumentTemplates:
    """Test DocumentTemplates class."""

    def test_minimal_ccd_template(self):
        """Test minimal CCD template returns correct structure."""
        template = DocumentTemplates.minimal_ccd_template()

        # Check top-level keys
        assert "patient" in template
        assert "author" in template
        assert "custodian" in template
        assert "sections" in template
        assert "metadata" in template

        # Check metadata
        assert template["metadata"]["document_type"] == "ccd"
        assert "Minimal" in template["metadata"]["title"]

        # Check patient data
        patient = template["patient"]
        assert patient.first_name == "Jane"
        assert patient.last_name == "Doe"
        assert patient.sex == "F"
        assert isinstance(patient.date_of_birth, date)
        assert patient.date_of_birth == date(1980, 3, 15)

        # Check patient has addresses and telecoms
        assert len(patient.addresses) > 0
        assert len(patient.telecoms) > 0

        # Check address structure
        address = patient.addresses[0]
        assert hasattr(address, "street_lines")
        assert hasattr(address, "city")
        assert hasattr(address, "state")
        assert hasattr(address, "postal_code")
        assert address.city == "Boston"
        assert address.state == "MA"

        # Check telecom structure
        telecom = patient.telecoms[0]
        assert hasattr(telecom, "type")
        assert hasattr(telecom, "value")
        assert telecom.type == "phone"

        # Check author data
        author = template["author"]
        assert author.first_name == "John"
        assert author.last_name == "Smith"
        assert hasattr(author, "npi")
        assert hasattr(author, "time")
        assert isinstance(author.time, datetime)

        # Check author organization
        assert hasattr(author, "organization")
        org = author.organization
        assert org.name == "Community Health Center"
        assert hasattr(org, "npi")

        # Check custodian
        custodian = template["custodian"]
        assert custodian.name == "Community Health Center"
        assert hasattr(custodian, "addresses")
        assert hasattr(custodian, "telecoms")

        # Check sections
        sections = template["sections"]
        assert "problems" in sections
        assert len(sections["problems"]) > 0

        # Check problem structure
        problem = sections["problems"][0]
        assert hasattr(problem, "name")
        assert hasattr(problem, "code")
        assert hasattr(problem, "code_system")
        assert hasattr(problem, "status")
        assert problem.name == "Essential Hypertension"
        assert isinstance(problem.onset_date, date)

    def test_full_ccd_template(self):
        """Test full CCD template returns comprehensive structure."""
        template = DocumentTemplates.full_ccd_template()

        # Check top-level keys
        assert "patient" in template
        assert "author" in template
        assert "custodian" in template
        assert "sections" in template
        assert "metadata" in template

        # Check metadata
        assert template["metadata"]["document_type"] == "ccd"
        assert "Complete" in template["metadata"]["title"]

        # Check patient
        patient = template["patient"]
        assert patient.first_name == "Robert"
        assert patient.last_name == "Johnson"
        assert isinstance(patient.date_of_birth, date)

        # Check sections exist
        sections = template["sections"]
        assert "problems" in sections
        assert "medications" in sections
        assert "allergies" in sections
        assert "immunizations" in sections
        assert "vital_signs" in sections
        assert "procedures" in sections
        assert "results" in sections
        assert "encounters" in sections
        assert "smoking_status" in sections

        # Check problems
        assert len(sections["problems"]) >= 3
        problem = sections["problems"][0]
        assert hasattr(problem, "name")
        assert hasattr(problem, "code")
        assert hasattr(problem, "status")

        # Check medications
        assert len(sections["medications"]) >= 3
        med = sections["medications"][0]
        assert hasattr(med, "name")
        assert hasattr(med, "code")
        assert hasattr(med, "dosage")
        assert hasattr(med, "route")
        assert hasattr(med, "frequency")
        assert isinstance(med.start_date, date)

        # Check allergies
        assert len(sections["allergies"]) >= 2
        allergy = sections["allergies"][0]
        assert hasattr(allergy, "allergen")
        assert hasattr(allergy, "allergen_code")
        assert hasattr(allergy, "allergy_type")
        assert hasattr(allergy, "reaction")
        assert hasattr(allergy, "severity")

        # Check immunizations
        assert len(sections["immunizations"]) >= 3
        imm = sections["immunizations"][0]
        assert hasattr(imm, "vaccine_name")
        assert hasattr(imm, "cvx_code")
        assert isinstance(imm.administration_date, date)

        # Check vital signs
        assert len(sections["vital_signs"]) >= 1
        vs_org = sections["vital_signs"][0]
        assert hasattr(vs_org, "vital_signs")
        assert len(vs_org.vital_signs) >= 5
        vs = vs_org.vital_signs[0]
        assert hasattr(vs, "type")
        assert hasattr(vs, "code")
        assert hasattr(vs, "value")
        assert hasattr(vs, "unit")
        assert isinstance(vs.date, datetime)

        # Check procedures
        assert len(sections["procedures"]) >= 2
        proc = sections["procedures"][0]
        assert hasattr(proc, "name")
        assert hasattr(proc, "code")
        assert isinstance(proc.date, date)

        # Check results
        assert len(sections["results"]) >= 1
        result_org = sections["results"][0]
        assert hasattr(result_org, "results")
        assert len(result_org.results) >= 3
        result = result_org.results[0]
        assert hasattr(result, "name")
        assert hasattr(result, "code")
        assert hasattr(result, "value")
        assert hasattr(result, "unit")

        # Check encounters
        assert len(sections["encounters"]) >= 2
        enc = sections["encounters"][0]
        assert hasattr(enc, "name")
        assert hasattr(enc, "code")
        assert isinstance(enc.date, date)

        # Check smoking status
        assert len(sections["smoking_status"]) >= 1
        smoking = sections["smoking_status"][0]
        assert hasattr(smoking, "status")
        assert hasattr(smoking, "code")

    def test_empty_template_discharge_summary(self):
        """Test empty discharge summary template."""
        template = DocumentTemplates.empty_template("discharge_summary")

        # Check metadata
        assert template["metadata"]["document_type"] == "discharge_summary"
        assert "Discharge" in template["metadata"]["title"]

        # Check has required structure
        assert "patient" in template
        assert "author" in template
        assert "custodian" in template
        assert "sections" in template

        # Check sections are empty or minimal
        sections = template["sections"]
        assert isinstance(sections["problems"], list)
        assert isinstance(sections["medications"], list)

    def test_empty_template_progress_note(self):
        """Test empty progress note template."""
        template = DocumentTemplates.empty_template("progress_note")

        # Check metadata
        assert template["metadata"]["document_type"] == "progress_note"
        assert "Progress" in template["metadata"]["title"]

        # Check has required structure
        assert "patient" in template
        assert "author" in template
        assert "custodian" in template
        assert "sections" in template

    def test_empty_template_ccd(self):
        """Test empty CCD template (should return minimal)."""
        template = DocumentTemplates.empty_template("ccd")

        # Should be same as minimal
        assert template["metadata"]["document_type"] == "ccd"
        assert "patient" in template
        assert "sections" in template

    def test_empty_template_invalid_type(self):
        """Test empty template with invalid document type."""
        with pytest.raises(ValueError) as exc_info:
            DocumentTemplates.empty_template("invalid_type")

        assert "Unsupported document type" in str(exc_info.value)
        assert "invalid_type" in str(exc_info.value)

    def test_load_template_success(self):
        """Test loading a template file successfully."""
        data = DocumentTemplates._load_template("minimal_ccd.json")

        assert isinstance(data, dict)
        assert "patient" in data
        assert "metadata" in data

    def test_load_template_not_found(self):
        """Test loading non-existent template file."""
        with pytest.raises(FileNotFoundError):
            DocumentTemplates._load_template("nonexistent.json")

    def test_convert_dates_dict(self):
        """Test date conversion for dictionary."""
        data = {
            "date_of_birth": "1980-03-15",
            "onset_date": "2020-01-15",
            "time": "2024-01-15T10:30:00",
            "regular_field": "value",
        }

        result = DocumentTemplates._convert_dates(data)

        assert isinstance(result["date_of_birth"], date)
        assert result["date_of_birth"] == date(1980, 3, 15)
        assert isinstance(result["onset_date"], date)
        assert isinstance(result["time"], datetime)
        assert result["regular_field"] == "value"

    def test_convert_dates_nested_dict(self):
        """Test date conversion for nested dictionary."""
        data = {
            "patient": {
                "date_of_birth": "1980-03-15",
                "name": "John Doe",
            },
            "author": {
                "time": "2024-01-15T10:30:00",
            },
        }

        result = DocumentTemplates._convert_dates(data)

        assert isinstance(result["patient"]["date_of_birth"], date)
        assert isinstance(result["author"]["time"], datetime)

    def test_convert_dates_list(self):
        """Test date conversion for list."""
        data = [
            {"onset_date": "2020-01-15"},
            {"onset_date": "2021-03-20"},
        ]

        result = DocumentTemplates._convert_dates(data)

        assert isinstance(result[0]["onset_date"], date)
        assert isinstance(result[1]["onset_date"], date)

    def test_convert_dates_null_values(self):
        """Test date conversion with null values."""
        data = {
            "date_of_birth": None,
            "onset_date": "2020-01-15",
        }

        result = DocumentTemplates._convert_dates(data)

        assert result["date_of_birth"] is None
        assert isinstance(result["onset_date"], date)

    def test_convert_dates_invalid_format(self):
        """Test date conversion with invalid date format."""
        data = {
            "date_of_birth": "invalid-date",
            "regular_field": "value",
        }

        result = DocumentTemplates._convert_dates(data)

        # Should keep original value if conversion fails
        assert result["date_of_birth"] == "invalid-date"
        assert result["regular_field"] == "value"

    def test_create_simple_class(self):
        """Test creating simple class from dictionary."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
        }

        obj = DocumentTemplates._create_simple_class("Person", data)

        assert obj.first_name == "John"
        assert obj.last_name == "Doe"
        assert obj.age == 30
        assert "Person" in repr(obj)

    def test_hydrate_template_patient(self):
        """Test hydrating patient data."""
        template_data = {
            "patient": {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1980-03-15",
                "addresses": [
                    {
                        "street_lines": ["123 Main St"],
                        "city": "Boston",
                        "state": "MA",
                        "postal_code": "02101",
                        "country": "US",
                    }
                ],
                "telecoms": [
                    {
                        "type": "phone",
                        "value": "617-555-1234",
                        "use": "home",
                    }
                ],
            }
        }

        result = DocumentTemplates._hydrate_template(template_data)

        patient = result["patient"]
        assert patient.first_name == "John"
        assert isinstance(patient.date_of_birth, date)
        assert len(patient.addresses) == 1
        assert patient.addresses[0].city == "Boston"
        assert len(patient.telecoms) == 1
        assert patient.telecoms[0].type == "phone"

    def test_hydrate_template_sections(self):
        """Test hydrating sections data."""
        template_data = {
            "sections": {
                "problems": [
                    {
                        "name": "Hypertension",
                        "code": "59621000",
                        "code_system": "SNOMED",
                        "status": "active",
                        "onset_date": "2020-01-15",
                    }
                ],
                "medications": [
                    {
                        "name": "Lisinopril",
                        "code": "314076",
                        "dosage": "10 mg",
                        "route": "oral",
                        "frequency": "daily",
                        "start_date": "2020-02-01",
                        "status": "active",
                    }
                ],
            }
        }

        result = DocumentTemplates._hydrate_template(template_data)

        sections = result["sections"]
        assert "problems" in sections
        assert len(sections["problems"]) == 1
        problem = sections["problems"][0]
        assert problem.name == "Hypertension"
        assert isinstance(problem.onset_date, date)

        assert "medications" in sections
        assert len(sections["medications"]) == 1
        med = sections["medications"][0]
        assert med.name == "Lisinopril"
        assert isinstance(med.start_date, date)

    def test_list_available_templates(self):
        """Test listing available template files."""
        templates = DocumentTemplates.list_available_templates()

        assert isinstance(templates, list)
        assert "minimal_ccd" in templates
        assert "full_ccd" in templates
        assert "discharge_summary" in templates
        assert "progress_note" in templates

        # Should be sorted
        assert templates == sorted(templates)

    def test_template_dir_exists(self):
        """Test that template directory exists."""
        assert DocumentTemplates.TEMPLATE_DIR.exists()
        assert DocumentTemplates.TEMPLATE_DIR.is_dir()

    def test_all_template_files_valid_json(self):
        """Test that all template files are valid JSON."""
        for template_file in DocumentTemplates.TEMPLATE_DIR.glob("*.json"):
            with open(template_file, encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
                assert "metadata" in data
                assert "patient" in data

    def test_minimal_template_has_all_required_fields(self):
        """Test minimal template has all required fields."""
        data = DocumentTemplates._load_template("minimal_ccd.json")

        # Check patient required fields
        patient = data["patient"]
        required_patient_fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "sex",
            "addresses",
            "telecoms",
        ]
        for field in required_patient_fields:
            assert field in patient, f"Missing required patient field: {field}"

        # Check author required fields
        author = data["author"]
        required_author_fields = ["first_name", "last_name", "npi", "time", "organization"]
        for field in required_author_fields:
            assert field in author, f"Missing required author field: {field}"

        # Check custodian required fields
        custodian = data["custodian"]
        required_custodian_fields = ["name", "npi", "addresses", "telecoms"]
        for field in required_custodian_fields:
            assert field in custodian, f"Missing required custodian field: {field}"

    def test_full_template_comprehensive_coverage(self):
        """Test full template has comprehensive section coverage."""
        data = DocumentTemplates._load_template("full_ccd.json")

        sections = data["sections"]
        expected_sections = [
            "problems",
            "medications",
            "allergies",
            "immunizations",
            "vital_signs",
            "procedures",
            "results",
            "encounters",
            "smoking_status",
        ]

        for section in expected_sections:
            assert section in sections, f"Missing section: {section}"
            assert isinstance(sections[section], list), f"Section {section} should be a list"
            assert len(sections[section]) > 0, f"Section {section} should have data"

    def test_date_fields_are_iso_format_in_json(self):
        """Test that date fields in JSON templates are in ISO format."""
        data = DocumentTemplates._load_template("minimal_ccd.json")

        # Check patient date of birth
        dob = data["patient"]["date_of_birth"]
        assert isinstance(dob, str)
        # Should parse without error
        datetime.fromisoformat(dob)

        # Check problem onset date
        if "problems" in data["sections"] and len(data["sections"]["problems"]) > 0:
            onset = data["sections"]["problems"][0]["onset_date"]
            if onset is not None:
                assert isinstance(onset, str)
                datetime.fromisoformat(onset)

    def test_template_metadata_structure(self):
        """Test that all templates have proper metadata structure."""
        for template_name in ["minimal_ccd", "full_ccd", "discharge_summary", "progress_note"]:
            data = DocumentTemplates._load_template(f"{template_name}.json")

            metadata = data["metadata"]
            assert "title" in metadata
            assert "description" in metadata
            assert "document_type" in metadata
            assert "template_id" in metadata

            # Template ID should be valid OID
            template_id = metadata["template_id"]
            assert template_id.startswith("2.16.840.1.113883.")

    def test_hydrate_preserves_all_data(self):
        """Test that hydration preserves all data without loss."""
        original = DocumentTemplates._load_template("minimal_ccd.json")
        hydrated = DocumentTemplates._hydrate_template(original)

        # Check patient data preserved
        assert hydrated["patient"].first_name == original["patient"]["first_name"]
        assert hydrated["patient"].last_name == original["patient"]["last_name"]

        # Check metadata preserved
        assert hydrated["metadata"]["title"] == original["metadata"]["title"]

    def test_empty_template_has_placeholder_values(self):
        """Test that empty templates have placeholder values."""
        template = DocumentTemplates.empty_template("discharge_summary")

        patient = template["patient"]
        # Placeholder values should be in brackets or generic
        assert "[" in patient.first_name or "Patient" in patient.first_name

    def test_vital_signs_organizer_structure(self):
        """Test vital signs organizer has correct nested structure."""
        template = DocumentTemplates.full_ccd_template()

        vs_org = template["sections"]["vital_signs"][0]
        assert hasattr(vs_org, "date")
        assert hasattr(vs_org, "vital_signs")
        assert isinstance(vs_org.vital_signs, list)
        assert len(vs_org.vital_signs) > 0

        # Check individual vital sign
        vs = vs_org.vital_signs[0]
        assert hasattr(vs, "type")
        assert hasattr(vs, "code")
        assert hasattr(vs, "value")
        assert hasattr(vs, "unit")

    def test_results_organizer_structure(self):
        """Test results organizer has correct nested structure."""
        template = DocumentTemplates.full_ccd_template()

        result_org = template["sections"]["results"][0]
        assert hasattr(result_org, "date")
        assert hasattr(result_org, "results")
        assert isinstance(result_org.results, list)
        assert len(result_org.results) > 0

        # Check individual result
        result = result_org.results[0]
        assert hasattr(result, "name")
        assert hasattr(result, "code")
        assert hasattr(result, "value")
        assert hasattr(result, "unit")
