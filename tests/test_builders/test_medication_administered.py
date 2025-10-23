"""Tests for Medication Administered Activity entry builder."""

from datetime import datetime

from lxml import etree

from ccdakit.builders.entries.medication_administered_entry import (
    MedicationAdministeredActivity,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockMedicationAdministered:
    """Mock administered medication for testing."""

    def __init__(
        self,
        name="Acetaminophen 325mg oral tablet",
        code="197806",
        administration_time=datetime(2023, 10, 15, 14, 30),
        administration_end_time=None,
        dose="325 mg",
        route="oral",
        rate=None,
        site=None,
        status="completed",
        performer=None,
        indication=None,
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._administration_time = administration_time
        self._administration_end_time = administration_end_time
        self._dose = dose
        self._route = route
        self._rate = rate
        self._site = site
        self._status = status
        self._performer = performer
        self._indication = indication
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def administration_time(self):
        return self._administration_time

    @property
    def administration_end_time(self):
        return self._administration_end_time

    @property
    def dose(self):
        return self._dose

    @property
    def route(self):
        return self._route

    @property
    def rate(self):
        return self._rate

    @property
    def site(self):
        return self._site

    @property
    def status(self):
        return self._status

    @property
    def performer(self):
        return self._performer

    @property
    def indication(self):
        return self._indication

    @property
    def instructions(self):
        return self._instructions


class TestMedicationAdministeredActivity:
    """Tests for MedicationAdministeredActivity builder."""

    def test_medication_administered_basic(self):
        """Test basic MedicationAdministeredActivity creation."""
        med = MockMedicationAdministered()
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        assert local_name(elem) == "substanceAdministration"
        assert elem.get("classCode") == "SBADM"
        assert elem.get("moodCode") == "EVN"

    def test_medication_administered_has_template_id_r21(self):
        """Test MedicationAdministeredActivity includes R2.1 template ID."""
        med = MockMedicationAdministered()
        activity = MedicationAdministeredActivity(med, version=CDAVersion.R2_1)
        elem = activity.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert template.get("extension") == "2014-06-09"

    def test_medication_administered_has_template_id_r20(self):
        """Test MedicationAdministeredActivity includes R2.0 template ID."""
        med = MockMedicationAdministered()
        activity = MedicationAdministeredActivity(med, version=CDAVersion.R2_0)
        elem = activity.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert template.get("extension") == "2014-06-09"

    def test_medication_administered_has_id(self):
        """Test MedicationAdministeredActivity has ID element."""
        med = MockMedicationAdministered()
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_medication_administered_has_status_code(self):
        """Test MedicationAdministeredActivity has statusCode element."""
        med = MockMedicationAdministered(status="completed")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_medication_administered_status_mapping(self):
        """Test different status code mappings."""
        test_cases = [
            ("completed", "completed"),
            ("active", "active"),
            ("held", "held"),
            ("aborted", "aborted"),
            ("suspended", "suspended"),
        ]

        for input_status, expected_status in test_cases:
            med = MockMedicationAdministered(status=input_status)
            activity = MedicationAdministeredActivity(med)
            elem = activity.to_element()

            status = elem.find(f"{{{NS}}}statusCode")
            assert status.get("code") == expected_status

    def test_medication_administered_status_default(self):
        """Test MedicationAdministeredActivity default status."""
        med = MockMedicationAdministered(status=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "completed"

    def test_medication_administered_effective_time_point(self):
        """Test MedicationAdministeredActivity effectiveTime as single point."""
        med = MockMedicationAdministered(
            administration_time=datetime(2023, 10, 15, 14, 30),
            administration_end_time=None,
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("value") == "202310151430"

    def test_medication_administered_effective_time_interval(self):
        """Test MedicationAdministeredActivity effectiveTime as interval."""
        med = MockMedicationAdministered(
            administration_time=datetime(2023, 10, 15, 14, 30),
            administration_end_time=datetime(2023, 10, 15, 15, 30),
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        xsi_type = time_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "IVL_TS"

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "202310151430"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "202310151530"

    def test_medication_administered_route_code_oral(self):
        """Test MedicationAdministeredActivity routeCode for oral route."""
        med = MockMedicationAdministered(route="oral")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        route_code = elem.find(f"{{{NS}}}routeCode")
        assert route_code is not None
        assert route_code.get("code") == "C38288"
        assert route_code.get("codeSystem") == "2.16.840.1.113883.3.26.1.1"
        assert route_code.get("displayName") == "oral"

    def test_medication_administered_route_code_iv(self):
        """Test MedicationAdministeredActivity routeCode for IV route."""
        med = MockMedicationAdministered(route="iv")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        route_code = elem.find(f"{{{NS}}}routeCode")
        assert route_code is not None
        assert route_code.get("code") == "C38276"

    def test_medication_administered_route_code_unknown(self):
        """Test MedicationAdministeredActivity routeCode for unknown route."""
        med = MockMedicationAdministered(route="some-unknown-route")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        route_code = elem.find(f"{{{NS}}}routeCode")
        assert route_code is not None
        assert route_code.get("nullFlavor") == "OTH"

        original_text = route_code.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "some-unknown-route"

    def test_medication_administered_route_code_empty(self):
        """Test MedicationAdministeredActivity routeCode when route is None."""
        med = MockMedicationAdministered(route=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        route_code = elem.find(f"{{{NS}}}routeCode")
        assert route_code is not None
        assert route_code.get("nullFlavor") == "UNK"

    def test_medication_administered_dose_quantity_with_units(self):
        """Test MedicationAdministeredActivity doseQuantity with value and unit."""
        med = MockMedicationAdministered(dose="325 mg")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        dose_qty = elem.find(f"{{{NS}}}doseQuantity")
        assert dose_qty is not None
        assert dose_qty.get("value") == "325"
        assert dose_qty.get("unit") == "mg"

    def test_medication_administered_dose_quantity_tablets(self):
        """Test MedicationAdministeredActivity doseQuantity with tablets."""
        med = MockMedicationAdministered(dose="2 tablets")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        dose_qty = elem.find(f"{{{NS}}}doseQuantity")
        assert dose_qty is not None
        assert dose_qty.get("value") == "2"
        assert dose_qty.get("unit") == "tablets"

    def test_medication_administered_dose_quantity_complex(self):
        """Test MedicationAdministeredActivity doseQuantity with complex dose."""
        med = MockMedicationAdministered(dose="Take 1-2 tablets as needed")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        dose_qty = elem.find(f"{{{NS}}}doseQuantity")
        assert dose_qty is not None

        original_text = dose_qty.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Take 1-2 tablets as needed"

    def test_medication_administered_dose_quantity_non_numeric_value(self):
        """Test MedicationAdministeredActivity doseQuantity with non-numeric value."""
        med = MockMedicationAdministered(dose="variable mg")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        dose_qty = elem.find(f"{{{NS}}}doseQuantity")
        assert dose_qty is not None

        # Should use originalText when value is not numeric
        original_text = dose_qty.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "variable mg"

    def test_medication_administered_dose_quantity_single_word(self):
        """Test MedicationAdministeredActivity doseQuantity with single word."""
        med = MockMedicationAdministered(dose="PRN")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        dose_qty = elem.find(f"{{{NS}}}doseQuantity")
        assert dose_qty is not None

        # Should use originalText when only one word
        original_text = dose_qty.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "PRN"

    def test_medication_administered_dose_quantity_empty(self):
        """Test MedicationAdministeredActivity doseQuantity when dose is None."""
        med = MockMedicationAdministered(dose=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        dose_qty = elem.find(f"{{{NS}}}doseQuantity")
        assert dose_qty is not None
        assert dose_qty.get("nullFlavor") == "UNK"

    def test_medication_administered_rate_quantity(self):
        """Test MedicationAdministeredActivity rateQuantity for IV infusion."""
        med = MockMedicationAdministered(
            route="iv",
            rate="100 mL/hr",
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        rate_qty = elem.find(f"{{{NS}}}rateQuantity")
        assert rate_qty is not None
        assert rate_qty.get("value") == "100"
        assert rate_qty.get("unit") == "mL/hr"

    def test_medication_administered_rate_quantity_complex(self):
        """Test MedicationAdministeredActivity rateQuantity with complex rate."""
        med = MockMedicationAdministered(rate="Titrate to effect")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        rate_qty = elem.find(f"{{{NS}}}rateQuantity")
        assert rate_qty is not None

        original_text = rate_qty.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Titrate to effect"

    def test_medication_administered_rate_quantity_non_numeric_value(self):
        """Test MedicationAdministeredActivity rateQuantity with non-numeric value."""
        med = MockMedicationAdministered(rate="variable mL/hr")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        rate_qty = elem.find(f"{{{NS}}}rateQuantity")
        assert rate_qty is not None

        # Should use originalText when value is not numeric
        original_text = rate_qty.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "variable mL/hr"

    def test_medication_administered_rate_quantity_single_word(self):
        """Test MedicationAdministeredActivity rateQuantity with single word."""
        med = MockMedicationAdministered(rate="Bolus")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        rate_qty = elem.find(f"{{{NS}}}rateQuantity")
        assert rate_qty is not None

        # Should use originalText when only one word
        original_text = rate_qty.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Bolus"

    def test_medication_administered_no_rate(self):
        """Test MedicationAdministeredActivity without rate."""
        med = MockMedicationAdministered(rate=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        rate_qty = elem.find(f"{{{NS}}}rateQuantity")
        assert rate_qty is None

    def test_medication_administered_approach_site_code(self):
        """Test MedicationAdministeredActivity approachSiteCode."""
        med = MockMedicationAdministered(site="left arm")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        site_code = elem.find(f"{{{NS}}}approachSiteCode")
        assert site_code is not None
        assert site_code.get("nullFlavor") == "OTH"

        original_text = site_code.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "left arm"

    def test_medication_administered_no_site(self):
        """Test MedicationAdministeredActivity without site."""
        med = MockMedicationAdministered(site=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        site_code = elem.find(f"{{{NS}}}approachSiteCode")
        assert site_code is None

    def test_medication_administered_consumable(self):
        """Test MedicationAdministeredActivity consumable element."""
        med = MockMedicationAdministered(
            name="Acetaminophen 325mg oral tablet",
            code="197806",
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

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
        material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")
        assert material is not None

        # Check code
        code = material.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "197806"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.88"
        assert code.get("displayName") == "Acetaminophen 325mg oral tablet"

    def test_medication_administered_consumable_r21_template(self):
        """Test MedicationAdministeredActivity consumable with R2.1 template extension."""
        med = MockMedicationAdministered()
        activity = MedicationAdministeredActivity(med, version=CDAVersion.R2_1)
        elem = activity.to_element()

        consumable = elem.find(f"{{{NS}}}consumable")
        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        template = manufactured_product.find(f"{{{NS}}}templateId")

        assert template.get("extension") == "2014-06-09"

    def test_medication_administered_performer(self):
        """Test MedicationAdministeredActivity performer element."""
        med = MockMedicationAdministered(performer="Dr. Jane Smith, RN")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        performer = elem.find(f"{{{NS}}}performer")
        assert performer is not None

        assigned_entity = performer.find(f"{{{NS}}}assignedEntity")
        assert assigned_entity is not None

        # Check ID
        id_elem = assigned_entity.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("nullFlavor") == "UNK"

        # Check assigned person
        assigned_person = assigned_entity.find(f"{{{NS}}}assignedPerson")
        assert assigned_person is not None

        name = assigned_person.find(f"{{{NS}}}name")
        assert name is not None
        assert name.text == "Dr. Jane Smith, RN"

    def test_medication_administered_no_performer(self):
        """Test MedicationAdministeredActivity without performer."""
        med = MockMedicationAdministered(performer=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        performer = elem.find(f"{{{NS}}}performer")
        assert performer is None

    def test_medication_administered_instructions(self):
        """Test MedicationAdministeredActivity with patient instructions."""
        med = MockMedicationAdministered(
            instructions="Administer over 15 minutes"
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        # Find instruction entryRelationship
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        instruction_rel = None
        for er in entry_rels:
            if er.get("typeCode") == "SUBJ":
                instruction_rel = er
                break

        assert instruction_rel is not None
        assert instruction_rel.get("inversionInd") == "true"

        # Check act
        act = instruction_rel.find(f"{{{NS}}}act")
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

        # Check text
        text = act.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Administer over 15 minutes"

        # Check status
        status = act.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_medication_administered_no_instructions(self):
        """Test MedicationAdministeredActivity without instructions."""
        med = MockMedicationAdministered(instructions=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        # Should not have SUBJ entryRelationship for instructions
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        instruction_rels = [er for er in entry_rels if er.get("typeCode") == "SUBJ"]
        assert len(instruction_rels) == 0

    def test_medication_administered_indication(self):
        """Test MedicationAdministeredActivity with indication."""
        med = MockMedicationAdministered(indication="Pain management")
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        # Find indication entryRelationship
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        indication_rel = None
        for er in entry_rels:
            if er.get("typeCode") == "RSON":
                indication_rel = er
                break

        assert indication_rel is not None

        # Check observation
        obs = indication_rel.find(f"{{{NS}}}observation")
        assert obs is not None
        assert obs.get("classCode") == "OBS"
        assert obs.get("moodCode") == "EVN"

        # Check template ID
        template = obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.19"

        # Check ID
        id_elem = obs.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("nullFlavor") == "UNK"

        # Check code
        code = obs.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "404684003"

        # Check text
        text = obs.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Pain management"

        # Check status
        status = obs.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_medication_administered_no_indication(self):
        """Test MedicationAdministeredActivity without indication."""
        med = MockMedicationAdministered(indication=None)
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        # Should not have RSON entryRelationship for indication
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        indication_rels = [er for er in entry_rels if er.get("typeCode") == "RSON"]
        assert len(indication_rels) == 0

    def test_medication_administered_complete(self):
        """Test MedicationAdministeredActivity with all optional elements."""
        med = MockMedicationAdministered(
            name="Ondansetron 4mg injection",
            code="312086",
            administration_time=datetime(2023, 10, 15, 14, 30),
            administration_end_time=datetime(2023, 10, 15, 14, 45),
            dose="4 mg",
            route="iv",
            rate="100 mL/hr",
            site="left antecubital fossa",
            status="completed",
            performer="Dr. Jane Smith, RN",
            indication="Nausea",
            instructions="Push slowly over 2 minutes",
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}routeCode") is not None
        assert elem.find(f"{{{NS}}}doseQuantity") is not None
        assert elem.find(f"{{{NS}}}rateQuantity") is not None
        assert elem.find(f"{{{NS}}}approachSiteCode") is not None
        assert elem.find(f"{{{NS}}}consumable") is not None
        assert elem.find(f"{{{NS}}}performer") is not None

        # Check entryRelationships
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 2  # instructions + indication

    def test_medication_administered_minimal(self):
        """Test MedicationAdministeredActivity with minimal required elements."""
        med = MockMedicationAdministered(
            name="Acetaminophen 325mg",
            code="197806",
            dose="325 mg",
            route="oral",
            performer=None,
            indication=None,
            instructions=None,
            rate=None,
            site=None,
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}routeCode") is not None
        assert elem.find(f"{{{NS}}}doseQuantity") is not None
        assert elem.find(f"{{{NS}}}consumable") is not None

        # Verify optional elements are absent
        assert elem.find(f"{{{NS}}}rateQuantity") is None
        assert elem.find(f"{{{NS}}}approachSiteCode") is None
        assert elem.find(f"{{{NS}}}performer") is None
        assert len(elem.findall(f"{{{NS}}}entryRelationship")) == 0

    def test_medication_administered_to_string(self):
        """Test MedicationAdministeredActivity serialization."""
        med = MockMedicationAdministered()
        activity = MedicationAdministeredActivity(med)
        xml = activity.to_string(pretty=False)

        assert "<substanceAdministration" in xml or ":substanceAdministration" in xml
        assert "classCode" in xml
        assert "SBADM" in xml
        assert "Acetaminophen" in xml

    def test_medication_administered_element_order(self):
        """Test that elements are in correct order."""
        med = MockMedicationAdministered(
            performer="Dr. Jane Smith",
            indication="Pain",
            instructions="Administer over 15 minutes",
        )
        activity = MedicationAdministeredActivity(med)
        elem = activity.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "id" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "routeCode" in names
        assert "doseQuantity" in names
        assert "consumable" in names
        assert "performer" in names
        assert names.count("entryRelationship") == 2  # instructions + indication
