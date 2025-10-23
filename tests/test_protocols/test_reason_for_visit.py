"""Tests for reason for visit protocol."""

from ccdakit.protocols.reason_for_visit import ReasonForVisitProtocol


class MockReasonForVisit:
    """Test implementation of ReasonForVisitProtocol."""

    def __init__(self, reason_text: str):
        """Initialize with reason text.

        Args:
            reason_text: The reason for visit text
        """
        self._reason_text = reason_text

    @property
    def reason_text(self) -> str:
        return self._reason_text


def test_reason_for_visit_protocol_basic():
    """Test basic ReasonForVisitProtocol implementation."""
    reason_text = "Follow-up visit for hypertension"

    reason = MockReasonForVisit(reason_text)

    assert reason.reason_text == reason_text
    assert len(reason.reason_text) > 0


def test_reason_for_visit_protocol_satisfaction():
    """Test that MockReasonForVisit satisfies ReasonForVisitProtocol."""
    reason_text = "Annual physical exam"

    reason = MockReasonForVisit(reason_text)

    # This should not raise an error
    def accepts_reason(r: ReasonForVisitProtocol) -> str:
        return r.reason_text

    result = accepts_reason(reason)
    assert result == reason_text


def test_reason_for_visit_acute_complaint():
    """Test reason for visit with acute complaint."""
    acute_reason = "Evaluation of chest pain that started this morning"

    reason = MockReasonForVisit(acute_reason)

    assert "chest pain" in reason.reason_text.lower()
    assert len(reason.reason_text) > 0


def test_reason_for_visit_chronic_disease_followup():
    """Test reason for visit for chronic disease follow-up."""
    followup_reason = "Follow-up visit for type 2 diabetes mellitus and hypertension management"

    reason = MockReasonForVisit(followup_reason)

    assert "follow-up" in reason.reason_text.lower()
    assert "diabetes" in reason.reason_text.lower()
    assert "hypertension" in reason.reason_text.lower()


def test_reason_for_visit_preventive_care():
    """Test reason for visit for preventive care."""
    preventive_reasons = [
        "Annual physical examination",
        "Well-child check-up",
        "Routine health maintenance visit",
        "Annual wellness visit for Medicare patient",
    ]

    for text in preventive_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_specific_symptoms():
    """Test reason for visit with specific symptoms."""
    symptom_based_reasons = [
        "Evaluation of persistent headache for past 3 days",
        "Shortness of breath with exertion",
        "Abdominal pain and nausea since last night",
        "Fever and cough for 2 days",
    ]

    for text in symptom_based_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_procedure_related():
    """Test reason for visit for procedure or test."""
    procedure_reasons = [
        "Pre-operative clearance for upcoming surgery",
        "Post-operative follow-up after appendectomy",
        "Review of recent lab results",
        "Discuss imaging findings from recent CT scan",
    ]

    for text in procedure_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_medication_related():
    """Test reason for visit for medication management."""
    medication_reason = "Medication refill and review of blood pressure medications"

    reason = MockReasonForVisit(medication_reason)

    assert "medication" in reason.reason_text.lower()
    assert "blood pressure" in reason.reason_text.lower()


def test_reason_for_visit_multiple_concerns():
    """Test reason for visit with multiple concerns."""
    multi_concern_reason = (
        "Patient presents for multiple concerns including: 1) Follow-up of diabetes, "
        "2) Evaluation of new onset knee pain, 3) Discussion of recent lab abnormalities"
    )

    reason = MockReasonForVisit(multi_concern_reason)

    assert "multiple concerns" in reason.reason_text.lower()
    assert "diabetes" in reason.reason_text.lower()
    assert "knee pain" in reason.reason_text.lower()
    assert "lab abnormalities" in reason.reason_text.lower()


def test_reason_for_visit_referral_related():
    """Test reason for visit from referral."""
    referral_reason = "Referral from primary care for evaluation of persistent joint pain"

    reason = MockReasonForVisit(referral_reason)

    assert "referral" in reason.reason_text.lower()
    assert "joint pain" in reason.reason_text.lower()


def test_reason_for_visit_emergency_presentation():
    """Test reason for visit for emergency presentation."""
    emergency_reasons = [
        "Sudden onset severe headache with vision changes",
        "Chest pain with radiation to left arm",
        "Difficulty breathing and wheezing",
        "Uncontrolled bleeding after injury",
    ]

    for text in emergency_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_screening():
    """Test reason for visit for screening."""
    screening_reasons = [
        "Routine colonoscopy screening",
        "Annual mammogram screening",
        "Diabetes screening based on family history",
        "Cardiovascular risk assessment",
    ]

    for text in screening_reasons:
        reason = MockReasonForVisit(text)
        assert "screening" in reason.reason_text.lower() or "assessment" in reason.reason_text.lower()


def test_reason_for_visit_consultation():
    """Test reason for visit for specialist consultation."""
    consultation_reason = (
        "Cardiology consultation for evaluation of new onset atrial fibrillation "
        "discovered during routine examination"
    )

    reason = MockReasonForVisit(consultation_reason)

    assert "consultation" in reason.reason_text.lower()
    assert "cardiology" in reason.reason_text.lower()


def test_reason_for_visit_administrative():
    """Test reason for visit for administrative purposes."""
    admin_reasons = [
        "Completion of disability paperwork",
        "Work clearance examination",
        "Sports physical for school athletics",
        "Medical clearance for travel",
    ]

    for text in admin_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_behavioral_health():
    """Test reason for visit for behavioral health concerns."""
    behavioral_reasons = [
        "Evaluation for depression and anxiety symptoms",
        "Follow-up for medication management of bipolar disorder",
        "Initial consultation for therapy referral",
    ]

    for text in behavioral_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_protocol_type_checking():
    """Test that type hints work correctly with ReasonForVisitProtocol."""

    def process_reason(r: ReasonForVisitProtocol) -> dict:
        """Process reason for visit and return summary."""
        return {
            "text_length": len(r.reason_text),
            "has_content": len(r.reason_text) > 0,
            "first_50_chars": r.reason_text[:50] if len(r.reason_text) >= 50 else r.reason_text,
        }

    reason = MockReasonForVisit("Patient presents for evaluation of chronic lower back pain")
    result = process_reason(reason)

    assert result["text_length"] > 0
    assert result["has_content"] is True
    assert len(result["first_50_chars"]) <= 50


def test_reason_for_visit_detailed_narrative():
    """Test reason for visit with detailed narrative."""
    detailed_reason = """
    Patient presents as a new patient to establish care. Has multiple chronic conditions
    including type 2 diabetes, hypertension, and hyperlipidemia. Also requesting evaluation
    of recent onset fatigue and weight changes. Patient has not seen a physician in over
    2 years and needs comprehensive health assessment and medication review.
    """

    reason = MockReasonForVisit(detailed_reason.strip())

    assert "new patient" in reason.reason_text.lower()
    assert "diabetes" in reason.reason_text.lower()
    assert "hypertension" in reason.reason_text.lower()
    assert len(reason.reason_text) > 100


def test_reason_for_visit_injury_related():
    """Test reason for visit for injury evaluation."""
    injury_reasons = [
        "Evaluation of ankle injury sustained during basketball game yesterday",
        "Follow-up for healing of wrist fracture",
        "Assessment of laceration requiring possible suture removal",
    ]

    for text in injury_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_womens_health():
    """Test reason for visit for women's health concerns."""
    womens_health_reasons = [
        "Annual gynecological examination",
        "Prenatal visit - second trimester",
        "Evaluation of irregular menstrual periods",
        "Discussion of contraceptive options",
    ]

    for text in womens_health_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


def test_reason_for_visit_pediatric():
    """Test reason for visit for pediatric concerns."""
    pediatric_reasons = [
        "6-month well-child check with vaccinations",
        "Evaluation of fever and ear pain in 3-year-old",
        "School physical examination",
        "Follow-up for asthma management",
    ]

    for text in pediatric_reasons:
        reason = MockReasonForVisit(text)
        assert len(reason.reason_text) > 0


class MinimalReasonForVisit:
    """Minimal implementation with just required property."""

    @property
    def reason_text(self) -> str:
        return "Routine visit"


def test_minimal_reason_for_visit_protocol():
    """Test that minimal implementation satisfies ReasonForVisitProtocol."""
    minimal_reason = MinimalReasonForVisit()

    # Should satisfy protocol with just the required property
    def accepts_reason(r: ReasonForVisitProtocol) -> bool:
        return len(r.reason_text) > 0

    result = accepts_reason(minimal_reason)
    assert result is True
    assert minimal_reason.reason_text == "Routine visit"


def test_minimal_reason_satisfaction():
    """Test that MinimalReasonForVisit satisfies ReasonForVisitProtocol."""
    reason = MinimalReasonForVisit()

    def get_reason_text(r: ReasonForVisitProtocol) -> str:
        return r.reason_text

    result = get_reason_text(reason)
    assert result == "Routine visit"
