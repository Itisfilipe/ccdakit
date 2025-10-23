"""Tests for Plan of Treatment Section builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.plan_of_treatment import PlanOfTreatmentSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPersistentID:
    """Mock persistent ID for testing."""

    @property
    def root(self):
        return "2.16.840.1.113883.19.5.99999.1"

    @property
    def extension(self):
        return "PLAN-123"


class MockPlannedObservation:
    """Mock planned observation for testing."""

    def __init__(
        self,
        description="Lab test for glucose",
        code="2339-0",
        code_system="LOINC",
        planned_date=date(2024, 12, 15),
        status="active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedProcedure:
    """Mock planned procedure for testing."""

    def __init__(
        self,
        description="Appendectomy",
        code="80146002",
        code_system="SNOMED",
        planned_date=date(2024, 12, 20),
        status="active",
        body_site="Appendix",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._body_site = body_site
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def body_site(self):
        return self._body_site

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedEncounter:
    """Mock planned encounter for testing."""

    def __init__(
        self,
        description="Follow-up visit",
        code="99213",
        code_system="CPT",
        planned_date=date(2024, 11, 30),
        status="active",
        encounter_type="Office Visit",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._encounter_type = encounter_type
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def encounter_type(self):
        return self._encounter_type

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedAct:
    """Mock planned act for testing."""

    def __init__(
        self,
        description="Patient education",
        code="311401005",
        code_system="SNOMED",
        planned_date=date(2024, 12, 1),
        status="active",
        mood_code="INT",
        id_root="2.16.840.1.113883.19.5.99999.1",
        id_extension="ACT-123",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._mood_code = mood_code
        self._id_root = id_root
        self._id_extension = id_extension
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def display_name(self):
        """Alias for description."""
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def mood_code(self):
        return self._mood_code

    @property
    def id_root(self):
        return self._id_root

    @property
    def id_extension(self):
        return self._id_extension

    @property
    def effective_time(self):
        """Alias for planned_date."""
        return self._planned_date

    @property
    def instructions(self):
        """Optional instructions."""
        return None

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedMedication:
    """Mock planned medication for testing."""

    def __init__(
        self,
        description="Lisinopril 10mg",
        code="314076",
        code_system="RxNorm",
        planned_date=date(2024, 11, 25),
        status="active",
        dose="10",
        route="Oral",
        frequency="Daily",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._dose = dose
        self._route = route
        self._frequency = frequency
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def dose(self):
        return self._dose

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedSupply:
    """Mock planned supply for testing."""

    def __init__(
        self,
        description="Wheelchair",
        code="58938008",
        code_system="SNOMED",
        planned_date=date(2024, 12, 5),
        status="active",
        quantity="1",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._quantity = quantity
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def quantity(self):
        return self._quantity

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedImmunization:
    """Mock planned immunization for testing."""

    def __init__(
        self,
        description="Influenza vaccine",
        code="141",
        code_system="CVX",
        vaccine_code="141",
        planned_date=date(2024, 11, 28),
        status="active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._vaccine_code = vaccine_code
        self._planned_date = planned_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def vaccine_code(self):
        return self._vaccine_code

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockInstruction:
    """Mock instruction for testing."""

    def __init__(
        self,
        instruction_text="Take medication with food",
        persistent_id=None,
    ):
        self._instruction_text = instruction_text
        self._persistent_id = persistent_id

    @property
    def instruction_text(self):
        return self._instruction_text

    @property
    def persistent_id(self):
        return self._persistent_id


class TestPlanOfTreatmentSection:
    """Tests for PlanOfTreatmentSection builder."""

    def test_plan_of_treatment_section_basic(self):
        """Test basic PlanOfTreatmentSection creation."""
        section = PlanOfTreatmentSection()
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_plan_of_treatment_section_has_template_id_r21(self):
        """Test PlanOfTreatmentSection includes R2.1 template ID."""
        section = PlanOfTreatmentSection(version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.10"
        assert template.get("extension") == "2015-08-01"

    def test_plan_of_treatment_section_has_template_id_r20(self):
        """Test PlanOfTreatmentSection includes R2.0 template ID."""
        section = PlanOfTreatmentSection(version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.10"
        assert template.get("extension") == "2014-06-09"

    def test_plan_of_treatment_section_has_code(self):
        """Test PlanOfTreatmentSection includes code element."""
        section = PlanOfTreatmentSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "18776-5"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code.get("displayName") == "Plan of Treatment"

    def test_plan_of_treatment_section_has_title(self):
        """Test PlanOfTreatmentSection includes title element."""
        section = PlanOfTreatmentSection(title="Treatment Plan")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Treatment Plan"

    def test_plan_of_treatment_section_has_text(self):
        """Test PlanOfTreatmentSection includes text element."""
        section = PlanOfTreatmentSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_plan_of_treatment_section_empty_narrative(self):
        """Test narrative when no planned activities."""
        section = PlanOfTreatmentSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No planned activities"

    def test_plan_of_treatment_section_with_observation(self):
        """Test section with planned observation."""
        obs = MockPlannedObservation()
        section = PlanOfTreatmentSection(planned_observations=[obs])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        observation = entries[0].find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("moodCode") == "INT"

    def test_plan_of_treatment_section_with_procedure(self):
        """Test section with planned procedure."""
        proc = MockPlannedProcedure()
        section = PlanOfTreatmentSection(planned_procedures=[proc])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        procedure = entries[0].find(f"{{{NS}}}procedure")
        assert procedure is not None
        assert procedure.get("moodCode") == "INT"

    def test_plan_of_treatment_section_with_encounter(self):
        """Test section with planned encounter."""
        enc = MockPlannedEncounter()
        section = PlanOfTreatmentSection(planned_encounters=[enc])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        encounter = entries[0].find(f"{{{NS}}}encounter")
        assert encounter is not None
        assert encounter.get("moodCode") == "INT"

    def test_plan_of_treatment_section_with_act(self):
        """Test section with planned act."""
        act = MockPlannedAct()
        section = PlanOfTreatmentSection(planned_acts=[act])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        act_elem = entries[0].find(f"{{{NS}}}act")
        assert act_elem is not None
        assert act_elem.get("moodCode") == "INT"

    def test_plan_of_treatment_section_with_medication(self):
        """Test section with planned medication."""
        med = MockPlannedMedication()
        section = PlanOfTreatmentSection(planned_medications=[med])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        sub_admin = entries[0].find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("moodCode") == "INT"

    def test_plan_of_treatment_section_with_supply(self):
        """Test section with planned supply."""
        supply = MockPlannedSupply()
        section = PlanOfTreatmentSection(planned_supplies=[supply])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        supply_elem = entries[0].find(f"{{{NS}}}supply")
        assert supply_elem is not None
        assert supply_elem.get("moodCode") == "INT"

    def test_plan_of_treatment_section_with_immunization(self):
        """Test section with planned immunization."""
        immunization = MockPlannedImmunization()
        section = PlanOfTreatmentSection(planned_immunizations=[immunization])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        sub_admin = entries[0].find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("moodCode") == "INT"

    def test_plan_of_treatment_section_with_instruction(self):
        """Test section with instruction."""
        instruction = MockInstruction()
        section = PlanOfTreatmentSection(instructions=[instruction])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        act = entries[0].find(f"{{{NS}}}act")
        assert act is not None
        text = act.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Take medication with food"

    def test_plan_of_treatment_section_with_multiple_activities(self):
        """Test section with multiple types of planned activities."""
        obs = MockPlannedObservation()
        proc = MockPlannedProcedure()
        enc = MockPlannedEncounter()
        act = MockPlannedAct()
        med = MockPlannedMedication()
        supply = MockPlannedSupply()
        immunization = MockPlannedImmunization()
        instruction = MockInstruction()

        section = PlanOfTreatmentSection(
            planned_observations=[obs],
            planned_procedures=[proc],
            planned_encounters=[enc],
            planned_acts=[act],
            planned_medications=[med],
            planned_supplies=[supply],
            planned_immunizations=[immunization],
            instructions=[instruction],
        )
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 8

    def test_plan_of_treatment_section_narrative_table(self):
        """Test narrative table generation."""
        obs = MockPlannedObservation()
        proc = MockPlannedProcedure()

        section = PlanOfTreatmentSection(
            planned_observations=[obs],
            planned_procedures=[proc],
        )
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None

        # Check table headers
        thead = table.find(f"{{{NS}}}thead")
        assert thead is not None
        headers = thead.findall(f".//{{{NS}}}th")
        assert len(headers) == 5
        assert headers[0].text == "Type"
        assert headers[1].text == "Description"
        assert headers[2].text == "Code"
        assert headers[3].text == "Status"
        assert headers[4].text == "Planned Date"

        # Check table rows
        tbody = table.find(f"{{{NS}}}tbody")
        assert tbody is not None
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 2

    def test_plan_of_treatment_section_with_persistent_id(self):
        """Test planned observation with persistent ID."""
        pid = MockPersistentID()
        obs = MockPlannedObservation(persistent_id=pid)
        section = PlanOfTreatmentSection(planned_observations=[obs])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem.get("root") == "2.16.840.1.113883.19.5.99999.1"
        assert id_elem.get("extension") == "PLAN-123"

    def test_plan_of_treatment_section_observation_without_code(self):
        """Test planned observation without code uses nullFlavor."""
        obs = MockPlannedObservation(code=None)
        section = PlanOfTreatmentSection(planned_observations=[obs])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code.get("nullFlavor") == "UNK"

    def test_plan_of_treatment_section_procedure_with_body_site(self):
        """Test planned procedure includes body site."""
        proc = MockPlannedProcedure(body_site="Right Knee")
        section = PlanOfTreatmentSection(planned_procedures=[proc])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        procedure = entry.find(f"{{{NS}}}procedure")
        target_site = procedure.find(f"{{{NS}}}targetSiteCode")

        assert target_site is not None
        assert target_site.get("displayName") == "Right Knee"

    def test_plan_of_treatment_section_medication_with_details(self):
        """Test planned medication includes dose and route."""
        med = MockPlannedMedication(dose="20", route="Intravenous")
        section = PlanOfTreatmentSection(planned_medications=[med])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        sub_admin = entry.find(f"{{{NS}}}substanceAdministration")

        dose = sub_admin.find(f"{{{NS}}}doseQuantity")
        assert dose is not None
        assert dose.get("value") == "20"

        route = sub_admin.find(f"{{{NS}}}routeCode")
        assert route is not None
        assert route.get("displayName") == "Intravenous"

    def test_plan_of_treatment_section_supply_with_quantity(self):
        """Test planned supply includes quantity."""
        supply = MockPlannedSupply(quantity="2")
        section = PlanOfTreatmentSection(planned_supplies=[supply])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        supply_elem = entry.find(f"{{{NS}}}supply")
        quantity = supply_elem.find(f"{{{NS}}}quantity")

        assert quantity is not None
        assert quantity.get("value") == "2"

    def test_plan_of_treatment_section_to_string(self):
        """Test PlanOfTreatmentSection serialization."""
        obs = MockPlannedObservation()
        section = PlanOfTreatmentSection(planned_observations=[obs])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "18776-5" in xml
        assert "Plan of Treatment" in xml

    def test_plan_of_treatment_section_status_mapping(self):
        """Test status code mapping for different statuses."""
        obs_active = MockPlannedObservation(status="active")
        obs_cancelled = MockPlannedObservation(status="cancelled")
        obs_completed = MockPlannedObservation(status="completed")

        section = PlanOfTreatmentSection(
            planned_observations=[obs_active, obs_cancelled, obs_completed]
        )
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

        # Check status codes
        for entry in entries:
            observation = entry.find(f"{{{NS}}}observation")
            status = observation.find(f"{{{NS}}}statusCode")
            assert status is not None
            assert status.get("code") in ["active", "cancelled", "completed"]

    def test_plan_of_treatment_section_without_planned_date(self):
        """Test planned activity without planned date."""
        obs = MockPlannedObservation(planned_date=None)
        section = PlanOfTreatmentSection(planned_observations=[obs])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        # effectiveTime should not be present when no planned date
        assert eff_time is None

    def test_plan_of_treatment_section_structure_order(self):
        """Test that elements are in correct order per C-CDA spec."""
        obs = MockPlannedObservation()
        section = PlanOfTreatmentSection(planned_observations=[obs])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        # Verify templateId comes before code
        assert names.index("templateId") < names.index("code")
        # Verify code comes before title
        assert names.index("code") < names.index("title")
        # Verify title comes before text
        assert names.index("title") < names.index("text")
        # Verify text comes before entry
        assert names.index("text") < names.index("entry")


class TestPlanOfTreatmentSectionIntegration:
    """Integration tests for PlanOfTreatmentSection."""

    def test_comprehensive_plan_of_treatment(self):
        """Test a comprehensive plan of treatment with all activity types."""
        obs1 = MockPlannedObservation(
            description="Hemoglobin A1c test",
            code="4548-4",
            code_system="LOINC",
        )
        obs2 = MockPlannedObservation(
            description="Lipid panel",
            code="24331-1",
            code_system="LOINC",
        )

        proc = MockPlannedProcedure(
            description="Colonoscopy",
            code="73761001",
            code_system="SNOMED",
            body_site="Colon",
        )

        enc = MockPlannedEncounter(
            description="Annual physical exam",
            code="99385",
            code_system="CPT",
        )

        act = MockPlannedAct(
            description="Diabetes self-management education",
            code="385800002",
            code_system="SNOMED",
        )

        med = MockPlannedMedication(
            description="Metformin 500mg",
            code="860975",
            code_system="RxNorm",
            dose="500",
            route="Oral",
            frequency="Twice daily",
        )

        supply = MockPlannedSupply(
            description="Blood glucose meter",
            code="43252007",
            code_system="SNOMED",
            quantity="1",
        )

        immunization = MockPlannedImmunization(
            description="Pneumococcal vaccine",
            code="33",
            vaccine_code="33",
        )

        instruction = MockInstruction(instruction_text="Monitor blood glucose daily before meals")

        section = PlanOfTreatmentSection(
            planned_observations=[obs1, obs2],
            planned_procedures=[proc],
            planned_encounters=[enc],
            planned_acts=[act],
            planned_medications=[med],
            planned_supplies=[supply],
            planned_immunizations=[immunization],
            instructions=[instruction],
            title="Comprehensive Treatment Plan",
        )

        elem = section.to_element()

        # Verify section structure
        assert local_name(elem) == "section"

        # Verify all entries are present
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 9

        # Verify narrative table
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None

        tbody = table.find(f"{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 9

    def test_multiple_observations_with_different_codes(self):
        """Test multiple observations with different coding systems."""
        obs_loinc = MockPlannedObservation(
            description="Glucose test",
            code="2339-0",
            code_system="LOINC",
        )
        obs_snomed = MockPlannedObservation(
            description="Blood pressure monitoring",
            code="252076005",
            code_system="SNOMED",
        )

        section = PlanOfTreatmentSection(planned_observations=[obs_loinc, obs_snomed])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check first observation uses LOINC
        obs1 = entries[0].find(f"{{{NS}}}observation")
        code1 = obs1.find(f"{{{NS}}}code")
        assert code1.get("code") == "2339-0"
        assert code1.get("codeSystem") == "2.16.840.1.113883.6.1"

        # Check second observation uses SNOMED
        obs2 = entries[1].find(f"{{{NS}}}observation")
        code2 = obs2.find(f"{{{NS}}}code")
        assert code2.get("code") == "252076005"
        assert code2.get("codeSystem") == "2.16.840.1.113883.6.96"

    def test_narrative_with_instruction_text(self):
        """Test narrative properly displays instruction text."""
        instruction = MockInstruction(instruction_text="Take medication 30 minutes before meals")

        section = PlanOfTreatmentSection(instructions=[instruction])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Type cell
        assert cells[0].text == "Instruction"

        # Description cell (should contain instruction text)
        content = cells[1].find(f"{{{NS}}}content")
        assert content.text == "Take medication 30 minutes before meals"

    def test_corner_case_empty_lists(self):
        """Test section with empty lists (corner case)."""
        section = PlanOfTreatmentSection(
            planned_observations=[],
            planned_procedures=[],
            planned_encounters=[],
        )
        elem = section.to_element()

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Should have "No planned activities" message
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No planned activities"

    def test_corner_case_all_null_codes(self):
        """Test section with all activities having null codes."""
        obs = MockPlannedObservation(code=None)
        proc = MockPlannedProcedure(code=None)
        enc = MockPlannedEncounter(code=None)

        section = PlanOfTreatmentSection(
            planned_observations=[obs],
            planned_procedures=[proc],
            planned_encounters=[enc],
        )
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

        # All should have nullFlavor on code
        for entry in entries:
            child = entry[0]  # First child (observation/procedure/encounter)
            code = child.find(f"{{{NS}}}code")
            assert code.get("nullFlavor") == "UNK"

    def test_corner_case_all_null_dates(self):
        """Test section with all activities having null planned dates."""
        obs = MockPlannedObservation(planned_date=None)
        proc = MockPlannedProcedure(planned_date=None)
        enc = MockPlannedEncounter(planned_date=None)

        section = PlanOfTreatmentSection(
            planned_observations=[obs],
            planned_procedures=[proc],
            planned_encounters=[enc],
        )
        elem = section.to_element()

        # Verify narrative shows "Not specified" for dates
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")

        for row in rows:
            cells = row.findall(f"{{{NS}}}td")
            date_cell = cells[4]  # Planned Date column
            assert date_cell.text == "Not specified"
