"""Tests for DischargeMedication entry builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.entries.discharge_medication import DischargeMedication
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockMedication:
    """Mock medication for testing."""

    def __init__(
        self,
        name="Lisinopril 10mg oral tablet",
        code="314076",
        dosage="10 mg",
        route="oral",
        frequency="once daily",
        start_date=date(2023, 1, 1),
        end_date=None,
        status="active",
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date
        self._end_date = end_date
        self._status = status
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dosage(self):
        return self._dosage

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def instructions(self):
        return self._instructions


class TestDischargeMedication:
    """Tests for DischargeMedication entry builder."""

    def test_discharge_medication_basic(self):
        """Test basic DischargeMedication creation."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        # CONF:1198-7689, CONF:1198-7690
        assert local_name(elem) == "act"
        assert elem.get("classCode") == "ACT"
        assert elem.get("moodCode") == "EVN"

    def test_discharge_medication_has_template_id_r21(self):
        """Test DischargeMedication includes R2.1 template ID."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication, version=CDAVersion.R2_1)
        elem = discharge_med.to_element()

        # CONF:1198-16760, CONF:1198-16761, CONF:1198-32513
        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.35"
        assert template.get("extension") == "2016-03-01"

    def test_discharge_medication_has_template_id_r20(self):
        """Test DischargeMedication includes R2.0 template ID."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication, version=CDAVersion.R2_0)
        elem = discharge_med.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.35"
        assert template.get("extension") == "2016-03-01"

    def test_discharge_medication_has_code(self):
        """Test DischargeMedication includes correct code."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        # CONF:1198-7691, CONF:1198-19161, CONF:1198-32159
        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10183-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Hospital discharge medication"

    def test_discharge_medication_code_has_translation(self):
        """Test code includes required translation."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        code = elem.find(f"{{{NS}}}code")

        # CONF:1198-32952, CONF:1198-32953, CONF:1198-32954
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75311-1"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert translation.get("displayName") == "Discharge Medication"

    def test_discharge_medication_has_status_code(self):
        """Test DischargeMedication has completed status."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        # CONF:1198-32779, CONF:1198-32780
        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_discharge_medication_has_entry_relationship(self):
        """Test DischargeMedication has entryRelationship."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        # CONF:1198-7692, CONF:1198-7693
        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

    def test_discharge_medication_contains_medication_activity(self):
        """Test entryRelationship contains Medication Activity."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        # CONF:1198-15525
        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"
        assert sub_admin.get("moodCode") == "EVN"

    def test_discharge_medication_activity_has_template_id(self):
        """Test Medication Activity has correct template ID."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication, version=CDAVersion.R2_1)
        elem = discharge_med.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")

        template = sub_admin.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert template.get("extension") == "2014-06-09"

    def test_discharge_medication_activity_has_medication_data(self):
        """Test Medication Activity contains medication information."""
        medication = MockMedication(
            name="Metformin 500mg",
            code="860975",
            dosage="500 mg",
            route="oral",
        )
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")

        # Check consumable
        consumable = sub_admin.find(f"{{{NS}}}consumable")
        assert consumable is not None

        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")
        code_elem = manufactured_material.find(f"{{{NS}}}code")

        assert code_elem.get("code") == "860975"
        assert code_elem.get("codeSystem") == "2.16.840.1.113883.6.88"  # RxNorm
        assert code_elem.get("displayName") == "Metformin 500mg"

    def test_discharge_medication_structure_order(self):
        """Test that act elements are in correct order."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "code" in names
        assert "statusCode" in names
        assert "entryRelationship" in names

        # Check order
        assert names.index("templateId") < names.index("code")
        assert names.index("code") < names.index("statusCode")
        assert names.index("statusCode") < names.index("entryRelationship")

    def test_discharge_medication_to_string(self):
        """Test DischargeMedication serialization."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication)
        xml = discharge_med.to_string(pretty=False)

        assert "<act" in xml or ":act" in xml
        assert "10183-2" in xml  # Code
        assert "75311-1" in xml  # Translation code
        assert "completed" in xml  # Status


class TestDischargeMedicationIntegration:
    """Integration tests for DischargeMedication."""

    def test_complete_discharge_medication(self):
        """Test creating a complete discharge medication entry."""
        medication = MockMedication(
            name="Lisinopril 10mg oral tablet",
            code="314076",
            dosage="10 mg",
            route="oral",
            frequency="once daily",
            start_date=date(2023, 12, 1),
            status="active",
            instructions="Take in the morning",
        )

        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        # Verify act structure
        assert local_name(elem) == "act"
        assert elem.get("classCode") == "ACT"
        assert elem.get("moodCode") == "EVN"

        # Verify template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.35"

        # Verify code
        code = elem.find(f"{{{NS}}}code")
        assert code.get("code") == "10183-2"

        # Verify translation
        translation = code.find(f"{{{NS}}}translation")
        assert translation.get("code") == "75311-1"

        # Verify statusCode
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "completed"

        # Verify entryRelationship
        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        assert entry_rel.get("typeCode") == "SUBJ"

        # Verify Medication Activity
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None

        # Verify medication details in Medication Activity
        consumable = sub_admin.find(f"{{{NS}}}consumable")
        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")
        med_code = manufactured_material.find(f"{{{NS}}}code")

        assert med_code.get("code") == "314076"
        assert med_code.get("displayName") == "Lisinopril 10mg oral tablet"

    def test_discharge_medication_with_instructions(self):
        """Test discharge medication with patient instructions."""
        medication = MockMedication(
            name="Metformin 500mg",
            code="860975",
            instructions="Take with food",
        )

        discharge_med = DischargeMedication(medication)
        elem = discharge_med.to_element()

        # Find Medication Activity
        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")

        # Check for instructions entryRelationship in Medication Activity
        instr_entry_rel = sub_admin.find(
            f".//{{{NS}}}entryRelationship[@typeCode='SUBJ'][@inversionInd='true']"
        )
        assert instr_entry_rel is not None

        instr_act = instr_entry_rel.find(f"{{{NS}}}act")
        assert instr_act is not None

        text = instr_act.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Take with food"

    def test_discharge_medication_r20_version(self):
        """Test discharge medication with R2.0 version."""
        medication = MockMedication()
        discharge_med = DischargeMedication(medication, version=CDAVersion.R2_0)
        elem = discharge_med.to_element()

        # Check act template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.35"
        assert template.get("extension") == "2016-03-01"

        # Check Medication Activity template ID
        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
        med_template = sub_admin.find(f"{{{NS}}}templateId")

        assert med_template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert med_template.get("extension") == "2014-06-09"

    def test_discharge_medication_various_statuses(self):
        """Test discharge medication with various medication statuses."""
        statuses = ["active", "completed", "discontinued"]

        for status in statuses:
            medication = MockMedication(status=status)
            discharge_med = DischargeMedication(medication)
            elem = discharge_med.to_element()

            # Act status should always be "completed" regardless of medication status
            act_status = elem.find(f"{{{NS}}}statusCode")
            assert act_status.get("code") == "completed"

            # But Medication Activity status should reflect the actual status
            entry_rel = elem.find(f"{{{NS}}}entryRelationship")
            sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
            med_status = sub_admin.find(f"{{{NS}}}statusCode")

            # Map medication status to substanceAdministration status
            expected_status = {
                "active": "active",
                "completed": "completed",
                "discontinued": "aborted",
            }[status]

            assert med_status.get("code") == expected_status
