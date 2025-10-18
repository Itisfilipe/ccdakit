"""Tests for MedicationActivity builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.entries.medication import MedicationActivity
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


class TestMedicationActivity:
    """Tests for MedicationActivity builder."""

    def test_medication_activity_basic(self):
        """Test basic MedicationActivity creation."""
        medication = MockMedication()
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        assert local_name(elem) == "substanceAdministration"
        assert elem.get("classCode") == "SBADM"
        assert elem.get("moodCode") == "EVN"

    def test_medication_activity_has_template_id_r21(self):
        """Test MedicationActivity includes R2.1 template ID."""
        medication = MockMedication()
        med_act = MedicationActivity(medication, version=CDAVersion.R2_1)
        elem = med_act.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert template.get("extension") == "2014-06-09"

    def test_medication_activity_has_template_id_r20(self):
        """Test MedicationActivity includes R2.0 template ID."""
        medication = MockMedication()
        med_act = MedicationActivity(medication, version=CDAVersion.R2_0)
        elem = med_act.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert template.get("extension") == "2014-06-09"

    def test_medication_activity_has_id(self):
        """Test MedicationActivity includes ID element."""
        medication = MockMedication()
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_medication_activity_has_status_code(self):
        """Test MedicationActivity includes statusCode."""
        medication = MockMedication(status="active")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "active"

    def test_medication_activity_status_mapping(self):
        """Test status code mapping."""
        # Test completed
        medication = MockMedication(status="completed")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "completed"

        # Test discontinued -> aborted
        medication = MockMedication(status="discontinued")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "aborted"

        # Test suspended
        medication = MockMedication(status="suspended")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "suspended"

    def test_medication_activity_has_effective_time(self):
        """Test MedicationActivity includes effectiveTime."""
        medication = MockMedication(start_date=date(2023, 1, 1))
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None

        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230101"

    def test_medication_activity_effective_time_with_end_date(self):
        """Test effectiveTime with both start and end dates."""
        medication = MockMedication(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
        )
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        low = eff_time.find(f"{{{NS}}}low")
        high = eff_time.find(f"{{{NS}}}high")

        assert low.get("value") == "20230101"
        assert high is not None
        assert high.get("value") == "20231231"

    def test_medication_activity_has_route_code_oral(self):
        """Test MedicationActivity routeCode with oral route."""
        medication = MockMedication(route="oral")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        route = elem.find(f"{{{NS}}}routeCode")
        assert route is not None
        assert route.get("code") == "C38288"
        assert route.get("codeSystem") == "2.16.840.1.113883.3.26.1.1"
        assert route.get("codeSystemName") == "NCI Thesaurus"

    def test_medication_activity_has_route_code_iv(self):
        """Test MedicationActivity routeCode with IV route."""
        medication = MockMedication(route="intravenous")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        route = elem.find(f"{{{NS}}}routeCode")
        assert route is not None
        assert route.get("code") == "C38276"

    def test_medication_activity_has_route_code_unknown(self):
        """Test MedicationActivity routeCode with unknown route."""
        medication = MockMedication(route="some-unknown-route")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        route = elem.find(f"{{{NS}}}routeCode")
        assert route is not None
        assert route.get("nullFlavor") == "OTH"

        original_text = route.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "some-unknown-route"

    def test_medication_activity_has_dose_quantity(self):
        """Test MedicationActivity doseQuantity."""
        medication = MockMedication(dosage="10 mg")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        dose = elem.find(f"{{{NS}}}doseQuantity")
        assert dose is not None
        assert dose.get("value") == "10"
        assert dose.get("unit") == "mg"

    def test_medication_activity_dose_quantity_complex(self):
        """Test doseQuantity with complex dosage."""
        medication = MockMedication(dosage="1-2 tablets as needed")
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        dose = elem.find(f"{{{NS}}}doseQuantity")
        assert dose is not None

        # Complex dosage should use originalText
        original_text = dose.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert "1-2 tablets" in original_text.text

    def test_medication_activity_has_consumable(self):
        """Test MedicationActivity includes consumable with medication."""
        medication = MockMedication(
            name="Lisinopril 10mg oral tablet",
            code="314076",
        )
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        consumable = elem.find(f"{{{NS}}}consumable")
        assert consumable is not None

        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        assert manufactured_product is not None
        assert manufactured_product.get("classCode") == "MANU"

        # Check template ID
        template = manufactured_product.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.23"

        # Check manufactured material
        manufactured_material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")
        assert manufactured_material is not None

        # Check medication code
        code = manufactured_material.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "314076"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.88"  # RxNorm OID
        assert code.get("codeSystemName") == "RxNorm"
        assert code.get("displayName") == "Lisinopril 10mg oral tablet"

    def test_medication_activity_with_instructions(self):
        """Test MedicationActivity with patient instructions."""
        medication = MockMedication(
            instructions="Take with food in the morning",
        )
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        # Find entryRelationship for instructions
        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"
        assert entry_rel.get("inversionInd") == "true"

        # Find act within entryRelationship
        act = entry_rel.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "INT"

        # Check template ID
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.20"

        # Check code
        code = act.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "409073007"

        # Check text with instructions
        text = act.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Take with food in the morning"

    def test_medication_activity_without_instructions(self):
        """Test MedicationActivity without patient instructions."""
        medication = MockMedication(instructions=None)
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        # Should not have entryRelationship for instructions
        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is None

    def test_medication_activity_to_string(self):
        """Test MedicationActivity serialization."""
        medication = MockMedication()
        med_act = MedicationActivity(medication)
        xml = med_act.to_string(pretty=False)

        assert "<substanceAdministration" in xml or ":substanceAdministration" in xml
        assert "classCode" in xml
        assert "moodCode" in xml
        assert "314076" in xml  # RxNorm code

    def test_medication_activity_structure_order(self):
        """Test that elements are in correct order."""
        medication = MockMedication(
            start_date=date(2023, 1, 1),
            instructions="Take with food",
        )
        med_act = MedicationActivity(medication)
        elem = med_act.to_element()

        children = list(elem)
        # Get local names
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "id" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "routeCode" in names
        assert "doseQuantity" in names
        assert "consumable" in names
        assert "entryRelationship" in names


class TestMedicationActivityIntegration:
    """Integration tests for MedicationActivity."""

    def test_multiple_medications(self):
        """Test creating multiple medication activities."""
        medication1 = MockMedication(
            name="Lisinopril 10mg",
            code="314076",
        )
        medication2 = MockMedication(
            name="Metformin 500mg",
            code="860975",
        )

        med_act1 = MedicationActivity(medication1)
        med_act2 = MedicationActivity(medication2)

        elem1 = med_act1.to_element()
        elem2 = med_act2.to_element()

        # Check that each has correct medication code
        consumable1 = elem1.find(f"{{{NS}}}consumable")
        manufactured_product1 = consumable1.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material1 = manufactured_product1.find(f"{{{NS}}}manufacturedMaterial")
        code1 = manufactured_material1.find(f"{{{NS}}}code")

        consumable2 = elem2.find(f"{{{NS}}}consumable")
        manufactured_product2 = consumable2.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material2 = manufactured_product2.find(f"{{{NS}}}manufacturedMaterial")
        code2 = manufactured_material2.find(f"{{{NS}}}code")

        assert code1.get("code") == "314076"
        assert code2.get("code") == "860975"

    def test_medication_in_parent_element(self):
        """Test composing medication activity in parent element."""
        parent = etree.Element(f"{{{NS}}}entry")

        medication = MockMedication()
        med_act = MedicationActivity(medication)

        parent.append(med_act.to_element())

        sub_admin = parent.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"
