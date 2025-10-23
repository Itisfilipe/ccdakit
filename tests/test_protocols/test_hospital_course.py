"""Tests for hospital course protocol."""

from ccdakit.protocols.hospital_course import HospitalCourseProtocol


class MockHospitalCourse:
    """Test implementation of HospitalCourseProtocol."""

    def __init__(self, course_text: str):
        """Initialize with course text.

        Args:
            course_text: The hospital course narrative text
        """
        self._course_text = course_text

    @property
    def course_text(self) -> str:
        return self._course_text


def test_hospital_course_protocol_basic():
    """Test basic HospitalCourseProtocol implementation."""
    course_text = (
        "The patient was admitted on 03/15/2024 with acute exacerbation of COPD. "
        "Initial treatment included supplemental oxygen, nebulizer treatments, and "
        "IV corticosteroids. By hospital day 2, the patient showed improvement with "
        "decreased work of breathing. The patient was discharged on 03/18/2024 in "
        "stable condition."
    )

    hospital_course = MockHospitalCourse(course_text)

    assert hospital_course.course_text == course_text
    assert len(hospital_course.course_text) > 0


def test_hospital_course_protocol_satisfaction():
    """Test that MockHospitalCourse satisfies HospitalCourseProtocol."""
    course_text = (
        "Patient admitted for acute cholecystitis. Underwent laparoscopic "
        "cholecystectomy on hospital day 2 without complications. Post-operative "
        "recovery was uneventful. Pain controlled with oral analgesics. Tolerating "
        "regular diet. Discharged home on hospital day 4."
    )

    hospital_course = MockHospitalCourse(course_text)

    # This should not raise an error
    def accepts_hospital_course(hc: HospitalCourseProtocol) -> str:
        return hc.course_text

    result = accepts_hospital_course(hospital_course)
    assert result == course_text


def test_hospital_course_detailed_narrative():
    """Test hospital course with detailed multi-day narrative."""
    detailed_course = """
    Hospital Day 1 (03/15/2024):
    Patient admitted through ED with chief complaint of chest pain. Initial EKG showed
    ST elevation in leads V2-V4. Emergent cardiac catheterization revealed 95% stenosis
    of LAD. Successful PCI with drug-eluting stent placement. Post-procedure monitoring
    in CCU with stable vital signs.

    Hospital Day 2 (03/16/2024):
    Patient remained hemodynamically stable. Cardiac enzymes trending down. Echo showed
    LVEF of 45% with mild hypokinesis of anterior wall. Started on optimal medical
    therapy including aspirin, clopidogrel, statin, beta-blocker, and ACE inhibitor.
    Transferred to telemetry unit.

    Hospital Day 3 (03/17/2024):
    Continued to improve. No chest pain or arrhythmias. Cardiac rehabilitation
    consultation completed. Patient education provided regarding lifestyle modifications
    and medication compliance. Discharge planning initiated.

    Hospital Day 4 (03/18/2024):
    Patient ambulating without difficulty. Vital signs stable. Discharge prescriptions
    written. Follow-up appointments scheduled with cardiology and primary care. Patient
    discharged home in stable condition with family member present.
    """

    hospital_course = MockHospitalCourse(detailed_course.strip())

    assert "Hospital Day 1" in hospital_course.course_text
    assert "Hospital Day 2" in hospital_course.course_text
    assert "Hospital Day 3" in hospital_course.course_text
    assert "Hospital Day 4" in hospital_course.course_text
    assert "discharged home" in hospital_course.course_text.lower()


def test_hospital_course_with_complications():
    """Test hospital course that includes complications."""
    course_with_complications = (
        "Patient admitted for elective left total knee arthroplasty on 04/10/2024. "
        "Surgery completed without immediate complications. Post-operative day 1, "
        "patient developed fever to 38.5C. Blood cultures obtained and broad-spectrum "
        "antibiotics initiated. Cultures returned positive for MRSA. Antibiotics "
        "adjusted to vancomycin based on sensitivities. Infectious disease consulted. "
        "Repeat cultures negative after 48 hours of appropriate therapy. Patient's "
        "fever resolved and surgical site showed no signs of infection. Physical "
        "therapy progressing well. Discharged on hospital day 7 with 4-week course "
        "of IV vancomycin via PICC line with home health nursing arranged."
    )

    hospital_course = MockHospitalCourse(course_with_complications)

    assert "complications" in hospital_course.course_text
    assert "antibiotics" in hospital_course.course_text.lower()
    assert "discharged" in hospital_course.course_text.lower()


def test_hospital_course_brief_stay():
    """Test hospital course for brief hospitalization."""
    brief_course = (
        "Patient admitted for observation following syncopal episode. Telemetry "
        "monitoring showed no arrhythmias. Orthostatic vital signs negative. "
        "Laboratory studies within normal limits. Echocardiogram showed normal LV "
        "function. Patient remained asymptomatic throughout stay. Discharged after "
        "24-hour observation period with cardiology follow-up."
    )

    hospital_course = MockHospitalCourse(brief_course)

    assert hospital_course.course_text == brief_course
    assert "observation" in hospital_course.course_text.lower()


def test_hospital_course_multiple_procedures():
    """Test hospital course with multiple procedures and interventions."""
    multi_procedure_course = (
        "Patient admitted 05/01/2024 with acute pancreatitis. Initial CT scan showed "
        "pancreatic edema without necrosis. NPO status maintained with IV hydration "
        "and pain control. Hospital day 2, patient developed respiratory distress "
        "requiring intubation and ICU transfer. ARDS protocol initiated. Hospital "
        "day 4, repeat CT showed developing necrotizing pancreatitis. IR-guided "
        "drainage catheter placed with 200mL purulent fluid removed. Cultures sent. "
        "Hospital day 7, patient successfully extubated. Transferred back to floor. "
        "Drain output decreasing. Started clear liquid diet. Hospital day 10, drain "
        "removed. Tolerating regular diet. Pain well-controlled on oral medications. "
        "Discharged home hospital day 12 with outpatient surgery follow-up."
    )

    hospital_course = MockHospitalCourse(multi_procedure_course)

    assert "admitted" in hospital_course.course_text.lower()
    assert "procedures" in hospital_course.course_text.lower() or "catheter" in hospital_course.course_text.lower()
    assert "discharged" in hospital_course.course_text.lower()


def test_hospital_course_protocol_type_checking():
    """Test that type hints work correctly with HospitalCourseProtocol."""

    def process_hospital_course(hc: HospitalCourseProtocol) -> dict:
        """Process hospital course and return summary."""
        return {
            "text_length": len(hc.course_text),
            "has_content": len(hc.course_text) > 0,
            "first_50_chars": hc.course_text[:50] if len(hc.course_text) >= 50 else hc.course_text,
        }

    course = MockHospitalCourse("Patient admitted and discharged same day for minor procedure.")
    result = process_hospital_course(course)

    assert result["text_length"] > 0
    assert result["has_content"] is True
    assert len(result["first_50_chars"]) <= 50


def test_hospital_course_with_consultations():
    """Test hospital course that includes specialist consultations."""
    course_with_consults = (
        "Patient admitted for pneumonia and COPD exacerbation. Pulmonology consulted "
        "for assistance with ventilator management. Recommendations included "
        "low-tidal volume ventilation and early spontaneous breathing trials. "
        "Infectious disease consulted regarding antibiotic selection given multi-drug "
        "resistant organism history. Recommended meropenem and vancomycin. Nephrology "
        "consulted for acute kidney injury. Recommended gentle hydration and avoidance "
        "of nephrotoxic agents. Patient gradually improved with multidisciplinary care. "
        "Successfully extubated hospital day 5. Renal function returned to baseline. "
        "Discharged hospital day 8 on oral antibiotics to complete 14-day course."
    )

    hospital_course = MockHospitalCourse(course_with_consults)

    assert "consulted" in hospital_course.course_text.lower()
    assert "discharged" in hospital_course.course_text.lower()
    assert len(hospital_course.course_text) > 100


class MinimalHospitalCourse:
    """Minimal implementation with just required property."""

    @property
    def course_text(self) -> str:
        return "Patient admitted and discharged."


def test_minimal_hospital_course_protocol():
    """Test that minimal implementation satisfies HospitalCourseProtocol."""
    minimal_course = MinimalHospitalCourse()

    # Should satisfy protocol with just the required property
    def accepts_course(hc: HospitalCourseProtocol) -> bool:
        return len(hc.course_text) > 0

    result = accepts_course(minimal_course)
    assert result is True
    assert minimal_course.course_text == "Patient admitted and discharged."
