"""Tests for allergy protocols."""

from datetime import date
from typing import Optional

from ccdakit.protocols.allergy import AllergyProtocol


class MockAllergy:
    """Test implementation of AllergyProtocol."""

    def __init__(
        self,
        allergen: str = "Penicillin",
        allergen_code: Optional[str] = "7980",
        allergen_code_system: Optional[str] = "RxNorm",
        allergy_type: str = "allergy",
        reaction: Optional[str] = "Hives",
        severity: Optional[str] = "moderate",
        status: str = "active",
        onset_date: Optional[date] = None,
    ):
        self._allergen = allergen
        self._allergen_code = allergen_code
        self._allergen_code_system = allergen_code_system
        self._allergy_type = allergy_type
        self._reaction = reaction
        self._severity = severity
        self._status = status
        self._onset_date = onset_date

    @property
    def allergen(self):
        return self._allergen

    @property
    def allergen_code(self):
        return self._allergen_code

    @property
    def allergen_code_system(self):
        return self._allergen_code_system

    @property
    def allergy_type(self):
        return self._allergy_type

    @property
    def reaction(self):
        return self._reaction

    @property
    def severity(self):
        return self._severity

    @property
    def status(self):
        return self._status

    @property
    def onset_date(self):
        return self._onset_date


def test_allergy_protocol_required_fields():
    """Test AllergyProtocol required fields."""
    allergy = MockAllergy()

    assert allergy.allergen == "Penicillin"
    assert allergy.allergy_type == "allergy"
    assert allergy.status == "active"


def test_allergy_protocol_with_codes():
    """Test AllergyProtocol with allergen codes."""
    allergy = MockAllergy(
        allergen="Penicillin",
        allergen_code="7980",
        allergen_code_system="RxNorm",
    )

    assert allergy.allergen_code == "7980"
    assert allergy.allergen_code_system == "RxNorm"


def test_allergy_protocol_with_reaction():
    """Test AllergyProtocol with reaction information."""
    allergy = MockAllergy(reaction="Hives", severity="moderate")

    assert allergy.reaction == "Hives"
    assert allergy.severity == "moderate"


def test_allergy_protocol_with_onset_date():
    """Test AllergyProtocol with onset date."""
    onset = date(2020, 5, 15)
    allergy = MockAllergy(onset_date=onset)

    assert allergy.onset_date == onset


def test_allergy_protocol_satisfaction():
    """Test that MockAllergy satisfies AllergyProtocol."""
    allergy = MockAllergy()

    def accepts_allergy(a: AllergyProtocol) -> str:
        return f"{a.allergen} ({a.allergy_type})"

    result = accepts_allergy(allergy)
    assert result == "Penicillin (allergy)"


def test_allergy_penicillin():
    """Test allergy to penicillin."""
    allergy = MockAllergy(
        allergen="Penicillin",
        allergen_code="7980",
        allergen_code_system="RxNorm",
        allergy_type="allergy",
        reaction="Hives",
        severity="moderate",
    )

    assert allergy.allergen == "Penicillin"
    assert allergy.allergy_type == "allergy"
    assert allergy.reaction == "Hives"


def test_allergy_peanuts():
    """Test allergy to peanuts."""
    allergy = MockAllergy(
        allergen="Peanuts",
        allergen_code="256349002",
        allergen_code_system="SNOMED CT",
        allergy_type="allergy",
        reaction="Anaphylaxis",
        severity="severe",
    )

    assert allergy.allergen == "Peanuts"
    assert allergy.reaction == "Anaphylaxis"
    assert allergy.severity == "severe"


def test_allergy_latex():
    """Test allergy to latex."""
    allergy = MockAllergy(
        allergen="Latex",
        allergen_code="111088007",
        allergen_code_system="SNOMED CT",
        allergy_type="allergy",
        reaction="Contact dermatitis",
        severity="mild",
    )

    assert allergy.allergen == "Latex"
    assert allergy.reaction == "Contact dermatitis"
    assert allergy.severity == "mild"


def test_intolerance_lactose():
    """Test lactose intolerance."""
    intolerance = MockAllergy(
        allergen="Lactose",
        allergen_code="47703008",
        allergen_code_system="SNOMED CT",
        allergy_type="intolerance",
        reaction="Nausea",
        severity="mild",
    )

    assert intolerance.allergen == "Lactose"
    assert intolerance.allergy_type == "intolerance"
    assert intolerance.reaction == "Nausea"


def test_allergy_severity_mild():
    """Test allergy with mild severity."""
    allergy = MockAllergy(severity="mild")

    assert allergy.severity == "mild"


def test_allergy_severity_moderate():
    """Test allergy with moderate severity."""
    allergy = MockAllergy(severity="moderate")

    assert allergy.severity == "moderate"


def test_allergy_severity_severe():
    """Test allergy with severe severity."""
    allergy = MockAllergy(severity="severe")

    assert allergy.severity == "severe"


def test_allergy_severity_fatal():
    """Test allergy with fatal severity."""
    allergy = MockAllergy(severity="fatal")

    assert allergy.severity == "fatal"


def test_allergy_status_active():
    """Test active allergy."""
    allergy = MockAllergy(status="active")

    assert allergy.status == "active"


def test_allergy_status_resolved():
    """Test resolved allergy."""
    allergy = MockAllergy(status="resolved")

    assert allergy.status == "resolved"


def test_allergy_without_reaction():
    """Test allergy without reaction information."""
    allergy = MockAllergy(reaction=None)

    assert allergy.reaction is None


def test_allergy_without_severity():
    """Test allergy without severity information."""
    allergy = MockAllergy(severity=None)

    assert allergy.severity is None


def test_allergy_without_onset_date():
    """Test allergy without onset date."""
    allergy = MockAllergy(onset_date=None)

    assert allergy.onset_date is None


class MinimalAllergy:
    """Minimal implementation with only required fields."""

    @property
    def allergen(self):
        return "Shellfish"

    @property
    def allergen_code(self):
        return None

    @property
    def allergen_code_system(self):
        return None

    @property
    def allergy_type(self):
        return "allergy"

    @property
    def reaction(self):
        return None

    @property
    def severity(self):
        return None

    @property
    def status(self):
        return "active"

    @property
    def onset_date(self):
        return None


def test_minimal_allergy_protocol():
    """Test that minimal implementation satisfies AllergyProtocol."""
    allergy = MinimalAllergy()

    assert allergy.allergen == "Shellfish"
    assert allergy.allergy_type == "allergy"
    assert allergy.status == "active"
    assert allergy.allergen_code is None
    assert allergy.allergen_code_system is None
    assert allergy.reaction is None
    assert allergy.severity is None
    assert allergy.onset_date is None


def test_allergy_with_rxnorm_code():
    """Test allergy with RxNorm code."""
    allergy = MockAllergy(
        allergen="Aspirin",
        allergen_code="1191",
        allergen_code_system="RxNorm",
    )

    assert allergy.allergen_code == "1191"
    assert allergy.allergen_code_system == "RxNorm"


def test_allergy_with_snomed_code():
    """Test allergy with SNOMED CT code."""
    allergy = MockAllergy(
        allergen="Bee venom",
        allergen_code="288328004",
        allergen_code_system="SNOMED CT",
    )

    assert allergy.allergen_code == "288328004"
    assert allergy.allergen_code_system == "SNOMED CT"


def test_allergy_with_unii_code():
    """Test allergy with UNII code."""
    allergy = MockAllergy(
        allergen="Sulfonamide",
        allergen_code="0N7609K889",
        allergen_code_system="UNII",
    )

    assert allergy.allergen_code == "0N7609K889"
    assert allergy.allergen_code_system == "UNII"


def test_allergy_anaphylaxis_reaction():
    """Test allergy with anaphylaxis reaction."""
    allergy = MockAllergy(
        allergen="Peanuts",
        reaction="Anaphylaxis",
        severity="fatal",
    )

    assert allergy.reaction == "Anaphylaxis"
    assert allergy.severity == "fatal"


def test_allergy_complete_example():
    """Test allergy with complete information."""
    allergy = MockAllergy(
        allergen="Penicillin",
        allergen_code="7980",
        allergen_code_system="RxNorm",
        allergy_type="allergy",
        reaction="Hives",
        severity="moderate",
        status="active",
        onset_date=date(2015, 6, 10),
    )

    assert allergy.allergen == "Penicillin"
    assert allergy.allergen_code == "7980"
    assert allergy.allergen_code_system == "RxNorm"
    assert allergy.allergy_type == "allergy"
    assert allergy.reaction == "Hives"
    assert allergy.severity == "moderate"
    assert allergy.status == "active"
    assert allergy.onset_date == date(2015, 6, 10)


def test_allergy_type_checking():
    """Test that AllergyProtocol enforces correct types."""
    allergy = MockAllergy(onset_date=date(2020, 5, 15))

    assert isinstance(allergy.allergen, str)
    assert isinstance(allergy.allergy_type, str)
    assert isinstance(allergy.status, str)
    assert isinstance(allergy.onset_date, date)


def test_allergy_without_codes():
    """Test allergy with only text description (no codes)."""
    allergy = MockAllergy(
        allergen="Eggs",
        allergen_code=None,
        allergen_code_system=None,
        reaction="Nausea and vomiting",
    )

    assert allergy.allergen == "Eggs"
    assert allergy.allergen_code is None
    assert allergy.allergen_code_system is None
    assert allergy.reaction == "Nausea and vomiting"


def test_allergy_lifecycle():
    """Test allergy through its lifecycle."""
    # Active allergy
    active = MockAllergy(
        allergen="Codeine",
        allergy_type="allergy",
        reaction="Nausea",
        status="active",
        onset_date=date(2020, 1, 1),
    )

    assert active.status == "active"

    # Resolved allergy
    resolved = MockAllergy(
        allergen="Codeine",
        allergy_type="allergy",
        reaction="Nausea",
        status="resolved",
        onset_date=date(2020, 1, 1),
    )

    assert resolved.status == "resolved"


def test_intolerance_vs_allergy():
    """Test distinguishing between intolerance and allergy."""
    allergy = MockAllergy(
        allergen="Peanuts",
        allergy_type="allergy",
        reaction="Anaphylaxis",
    )

    intolerance = MockAllergy(
        allergen="Lactose",
        allergy_type="intolerance",
        reaction="Bloating",
    )

    assert allergy.allergy_type == "allergy"
    assert intolerance.allergy_type == "intolerance"


def test_allergy_protocol_interface():
    """Test that AllergyProtocol has expected interface."""
    # Import to ensure coverage
    from ccdakit.protocols.allergy import AllergyProtocol

    # Verify protocol has expected attributes
    assert hasattr(AllergyProtocol, 'allergen')
    assert hasattr(AllergyProtocol, 'allergen_code')
    assert hasattr(AllergyProtocol, 'allergy_type')
    assert hasattr(AllergyProtocol, 'reaction')
    assert hasattr(AllergyProtocol, 'severity')
    assert hasattr(AllergyProtocol, 'status')

    # Verify docstrings exist
    assert AllergyProtocol.__doc__ is not None
    assert 'Allergy/Intolerance data contract' in AllergyProtocol.__doc__
