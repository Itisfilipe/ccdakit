"""Tests for custom validation rules engine."""

from pathlib import Path

import pytest
from lxml import etree

from ccdakit.core.validation import ValidationIssue, ValidationLevel, ValidationResult
from ccdakit.validators.rule_builder import FunctionBasedRule, RuleBuilder
from ccdakit.validators.rules import (
    CodeSystemConsistencyRule,
    DateConsistencyRule,
    MedicationDosageRule,
    NarrativePresenceRule,
    RequiredSectionsRule,
    RulesEngine,
    ValidationRule,
)


class TestValidationRule:
    """Test suite for ValidationRule base class."""

    def test_validation_rule_init(self):
        """Test ValidationRule initialization."""

        class TestRule(ValidationRule):
            def validate(self, document):
                return []

        rule = TestRule("test_rule", "Test description")
        assert rule.name == "test_rule"
        assert rule.description == "Test description"

    def test_validation_rule_repr(self):
        """Test ValidationRule string representation."""

        class TestRule(ValidationRule):
            def validate(self, document):
                return []

        rule = TestRule("test_rule", "Test description")
        assert repr(rule) == "<ValidationRule: test_rule>"

    def test_validation_rule_must_implement_validate(self):
        """Test that validate method must be implemented."""

        class IncompleteRule(ValidationRule):
            pass

        # Should not be able to instantiate abstract class without implementing validate
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteRule("incomplete", "Missing validate")


class TestRulesEngine:
    """Test suite for RulesEngine."""

    @pytest.fixture
    def engine(self):
        """Create empty rules engine."""
        return RulesEngine()

    @pytest.fixture
    def simple_rule(self):
        """Create a simple test rule."""

        class SimpleRule(ValidationRule):
            def validate(self, document):
                return []

        return SimpleRule("simple", "Simple test rule")

    @pytest.fixture
    def failing_rule(self):
        """Create a rule that always fails."""

        class FailingRule(ValidationRule):
            def validate(self, document):
                return [
                    ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message="Test error",
                        code="test_error",
                    )
                ]

        return FailingRule("failing", "Always fails")

    @pytest.fixture
    def warning_rule(self):
        """Create a rule that produces warnings."""

        class WarningRule(ValidationRule):
            def validate(self, document):
                return [
                    ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message="Test warning",
                        code="test_warning",
                    )
                ]

        return WarningRule("warning", "Produces warnings")

    @pytest.fixture
    def sample_document(self):
        """Create sample XML document."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <section>
                <title>Test Section</title>
            </section>
        </ClinicalDocument>"""
        return etree.fromstring(xml.encode("utf-8"))

    def test_engine_init(self, engine):
        """Test RulesEngine initialization."""
        assert len(engine) == 0
        assert engine.list_rules() == []

    def test_add_rule(self, engine, simple_rule):
        """Test adding rule to engine."""
        engine.add_rule(simple_rule)
        assert len(engine) == 1
        assert engine.list_rules() == ["simple"]

    def test_add_multiple_rules(self, engine, simple_rule, failing_rule):
        """Test adding multiple rules."""
        engine.add_rule(simple_rule)
        engine.add_rule(failing_rule)
        assert len(engine) == 2
        assert engine.list_rules() == ["simple", "failing"]

    def test_add_invalid_rule_raises_error(self, engine):
        """Test adding non-ValidationRule raises TypeError."""
        with pytest.raises(TypeError, match="Expected ValidationRule"):
            engine.add_rule("not a rule")

    def test_remove_rule_exists(self, engine, simple_rule):
        """Test removing existing rule."""
        engine.add_rule(simple_rule)
        assert len(engine) == 1

        removed = engine.remove_rule("simple")
        assert removed is True
        assert len(engine) == 0

    def test_remove_rule_not_exists(self, engine):
        """Test removing non-existent rule."""
        removed = engine.remove_rule("nonexistent")
        assert removed is False

    def test_get_rule_exists(self, engine, simple_rule):
        """Test getting existing rule."""
        engine.add_rule(simple_rule)
        rule = engine.get_rule("simple")
        assert rule is simple_rule

    def test_get_rule_not_exists(self, engine):
        """Test getting non-existent rule."""
        rule = engine.get_rule("nonexistent")
        assert rule is None

    def test_validate_no_rules(self, engine, sample_document):
        """Test validation with no rules."""
        result = engine.validate(sample_document)
        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_passing_rules(self, engine, simple_rule, sample_document):
        """Test validation with passing rules."""
        engine.add_rule(simple_rule)
        result = engine.validate(sample_document)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_failing_rules(self, engine, failing_rule, sample_document):
        """Test validation with failing rules."""
        engine.add_rule(failing_rule)
        result = engine.validate(sample_document)
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].message == "Test error"

    def test_validate_mixed_rules(
        self, engine, simple_rule, failing_rule, warning_rule, sample_document
    ):
        """Test validation with mixed rules."""
        engine.add_rule(simple_rule)
        engine.add_rule(failing_rule)
        engine.add_rule(warning_rule)

        result = engine.validate(sample_document)
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert len(result.warnings) == 1

    def test_validate_from_string(self, engine, simple_rule):
        """Test validation from XML string."""
        xml_string = '<?xml version="1.0"?><root></root>'
        engine.add_rule(simple_rule)
        result = engine.validate(xml_string)
        assert result.is_valid is True

    def test_validate_from_bytes(self, engine, simple_rule):
        """Test validation from bytes."""
        xml_bytes = b'<?xml version="1.0"?><root></root>'
        engine.add_rule(simple_rule)
        result = engine.validate(xml_bytes)
        assert result.is_valid is True

    def test_validate_from_file(self, engine, simple_rule, tmp_path):
        """Test validation from file path."""
        file_path = tmp_path / "test.xml"
        file_path.write_text('<?xml version="1.0"?><root></root>')

        engine.add_rule(simple_rule)
        result = engine.validate(file_path)
        assert result.is_valid is True

    def test_validate_from_string_file_path(self, engine, simple_rule, tmp_path):
        """Test validation from string file path."""
        file_path = tmp_path / "test.xml"
        file_path.write_text('<?xml version="1.0"?><root></root>')

        engine.add_rule(simple_rule)
        # Pass as string, not Path object
        result = engine.validate(str(file_path))
        assert result.is_valid is True

    def test_validate_invalid_xml(self, engine, simple_rule):
        """Test validation with invalid XML."""
        with pytest.raises(etree.XMLSyntaxError):
            engine.validate("<invalid>xml")

    def test_validate_nonexistent_file(self, engine, simple_rule):
        """Test validation with nonexistent file."""
        with pytest.raises(FileNotFoundError):
            engine.validate(Path("/nonexistent/file.xml"))

    def test_validate_rule_exception_handling(self, engine, sample_document):
        """Test that rule exceptions are captured."""

        class ExceptionRule(ValidationRule):
            def validate(self, document):
                raise ValueError("Test exception")

        engine.add_rule(ExceptionRule("exception", "Throws exception"))
        result = engine.validate(sample_document)

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "failed: Test exception" in result.errors[0].message

    def test_repr(self, engine, simple_rule):
        """Test RulesEngine string representation."""
        assert repr(engine) == "<RulesEngine: 0 rules>"
        engine.add_rule(simple_rule)
        assert repr(engine) == "<RulesEngine: 1 rules>"


class TestRequiredSectionsRule:
    """Test suite for RequiredSectionsRule."""

    @pytest.fixture
    def document_with_sections(self):
        """Create document with sections."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <structuredBody>
                    <component>
                        <section>
                            <code code="11450-4" />
                        </section>
                    </component>
                    <component>
                        <section>
                            <code code="10160-0" />
                        </section>
                    </component>
                </structuredBody>
            </component>
        </ClinicalDocument>"""
        return etree.fromstring(xml.encode("utf-8"))

    def test_all_required_sections_present(self, document_with_sections):
        """Test when all required sections are present."""
        rule = RequiredSectionsRule(["11450-4", "10160-0"])
        issues = rule.validate(document_with_sections)
        assert len(issues) == 0

    def test_missing_required_section(self, document_with_sections):
        """Test when required section is missing."""
        rule = RequiredSectionsRule(["11450-4", "10160-0", "12345-6"])
        issues = rule.validate(document_with_sections)
        assert len(issues) == 1
        assert "12345-6" in issues[0].message

    def test_section_names_mapping(self, document_with_sections):
        """Test section names are used in error messages."""
        rule = RequiredSectionsRule(["12345-6"], section_names={"12345-6": "Test Section"})
        issues = rule.validate(document_with_sections)
        assert len(issues) == 1
        assert "Test Section" in issues[0].message

    def test_warning_level(self, document_with_sections):
        """Test using warning level instead of error."""
        rule = RequiredSectionsRule(["12345-6"], level=ValidationLevel.WARNING)
        issues = rule.validate(document_with_sections)
        assert len(issues) == 1
        assert issues[0].level == ValidationLevel.WARNING


class TestMedicationDosageRule:
    """Test suite for MedicationDosageRule."""

    @pytest.fixture
    def document_with_medications(self):
        """Create document with medication dosages."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <substanceAdministration>
                            <doseQuantity value="50.0" />
                        </substanceAdministration>
                    </entry>
                    <entry>
                        <substanceAdministration>
                            <doseQuantity value="100.0" />
                        </substanceAdministration>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        return etree.fromstring(xml.encode("utf-8"))

    def test_valid_dosages(self, document_with_medications):
        """Test when all dosages are valid."""
        rule = MedicationDosageRule(min_dosage=1.0, max_dosage=200.0)
        issues = rule.validate(document_with_medications)
        assert len(issues) == 0

    def test_dosage_too_high(self):
        """Test when dosage exceeds maximum."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <substanceAdministration>
                <doseQuantity value="20000.0" />
            </substanceAdministration>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = MedicationDosageRule(max_dosage=10000.0)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "exceeds maximum" in issues[0].message

    def test_dosage_too_low(self):
        """Test when dosage below minimum."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <substanceAdministration>
                <doseQuantity value="0.0001" />
            </substanceAdministration>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = MedicationDosageRule(min_dosage=0.001)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "below minimum" in issues[0].message

    def test_invalid_dosage_format(self):
        """Test when dosage is not a number."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <substanceAdministration>
                <doseQuantity value="not_a_number" />
            </substanceAdministration>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = MedicationDosageRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert issues[0].level == ValidationLevel.ERROR
        assert "not a number" in issues[0].message


class TestDateConsistencyRule:
    """Test suite for DateConsistencyRule."""

    def test_valid_past_date(self):
        """Test with valid past date."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="20200101" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DateConsistencyRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_future_date_not_allowed(self):
        """Test future date when not allowed."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="29991231" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DateConsistencyRule(allow_future_dates=False)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "future" in issues[0].message.lower()

    def test_future_date_allowed(self):
        """Test future date when allowed."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="29991231" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DateConsistencyRule(allow_future_dates=True)
        issues = rule.validate(doc)
        # Should only flag if too old, not if future
        future_issues = [i for i in issues if "future" in i.message.lower()]
        assert len(future_issues) == 0

    def test_date_too_old(self):
        """Test date exceeds maximum years past."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="18000101" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DateConsistencyRule(max_years_past=150)
        issues = rule.validate(doc)
        assert len(issues) >= 1
        old_issues = [i for i in issues if "years in the past" in i.message]
        assert len(old_issues) == 1

    def test_invalid_date_format_skipped(self):
        """Test that invalid date formats are skipped."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="invalid-date" />
            <effectiveTime value="2020-01-15" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DateConsistencyRule()
        issues = rule.validate(doc)
        # Should not crash, just skip invalid date
        # The dash-formatted date is also invalid for HL7 format
        assert isinstance(issues, list)


class TestCodeSystemConsistencyRule:
    """Test suite for CodeSystemConsistencyRule."""

    def test_correct_code_system(self):
        """Test with correct code system."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <templateId root="2.16.840.1.113883.10.20.22.4.4" />
                            <value codeSystem="2.16.840.1.113883.6.96" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = CodeSystemConsistencyRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_incorrect_code_system(self):
        """Test with incorrect code system."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <templateId root="2.16.840.1.113883.10.20.22.4.4" />
                            <value codeSystem="9.9.9.9.9" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = CodeSystemConsistencyRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "incorrect_code_system" in issues[0].code


class TestNarrativePresenceRule:
    """Test suite for NarrativePresenceRule."""

    def test_section_with_narrative(self):
        """Test section with proper narrative."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <title>Problems</title>
                    <text>Patient has hypertension.</text>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = NarrativePresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_section_missing_narrative(self):
        """Test section without narrative."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <title>Problems</title>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = NarrativePresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "missing narrative" in issues[0].message.lower()

    def test_narrative_too_short(self):
        """Test narrative below minimum length."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <title>Problems</title>
                    <text>Hi</text>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = NarrativePresenceRule(min_length=10)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "too short" in issues[0].message


class TestRuleBuilder:
    """Test suite for RuleBuilder."""

    @pytest.fixture
    def sample_document(self):
        """Create sample document."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <section>
                <code code="11450-4" />
            </section>
            <section>
                <code code="10160-0" />
            </section>
        </ClinicalDocument>"""
        return etree.fromstring(xml.encode("utf-8"))

    def test_create_passing_rule(self, sample_document):
        """Test creating rule with passing predicate."""
        rule = RuleBuilder.create(
            "has_sections",
            "Check document has sections",
            lambda doc: len(doc.xpath("//cda:section", namespaces={"cda": "urn:hl7-org:v3"})) > 0,
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 0

    def test_create_failing_rule(self, sample_document):
        """Test creating rule with failing predicate."""
        rule = RuleBuilder.create(
            "has_ten_sections",
            "Check document has 10 sections",
            lambda doc: len(doc.xpath("//cda:section", namespaces={"cda": "urn:hl7-org:v3"})) >= 10,
            error_message="Document should have at least 10 sections",
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 1
        assert "at least 10 sections" in issues[0].message

    def test_xpath_exists_found(self, sample_document):
        """Test xpath_exists when element exists."""
        rule = RuleBuilder.xpath_exists(
            "has_section",
            "//cda:section",
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 0

    def test_xpath_exists_not_found(self, sample_document):
        """Test xpath_exists when element doesn't exist."""
        rule = RuleBuilder.xpath_exists(
            "has_patient",
            "//cda:patient",
            error_message="Patient is required",
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 1
        assert "Patient is required" in issues[0].message

    def test_xpath_count_min(self, sample_document):
        """Test xpath_count with minimum."""
        rule = RuleBuilder.xpath_count(
            "min_sections",
            "//cda:section",
            min_count=2,
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 0

    def test_xpath_count_min_failed(self, sample_document):
        """Test xpath_count minimum not met."""
        rule = RuleBuilder.xpath_count(
            "min_sections",
            "//cda:section",
            min_count=5,
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 1
        assert "minimum is 5" in issues[0].message

    def test_xpath_count_max(self, sample_document):
        """Test xpath_count with maximum."""
        rule = RuleBuilder.xpath_count(
            "max_sections",
            "//cda:section",
            max_count=10,
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 0

    def test_xpath_count_max_failed(self, sample_document):
        """Test xpath_count maximum exceeded."""
        rule = RuleBuilder.xpath_count(
            "max_sections",
            "//cda:section",
            max_count=1,
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 1
        assert "maximum is 1" in issues[0].message

    def test_xpath_count_exact(self, sample_document):
        """Test xpath_count with exact count."""
        rule = RuleBuilder.xpath_count(
            "exact_sections",
            "//cda:section",
            exact_count=2,
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 0

    def test_xpath_count_exact_failed(self, sample_document):
        """Test xpath_count exact count not met."""
        rule = RuleBuilder.xpath_count(
            "exact_sections",
            "//cda:section",
            exact_count=5,
        )

        issues = rule.validate(sample_document)
        assert len(issues) == 1
        assert "expected exactly 5" in issues[0].message

    def test_xpath_value_matches(self):
        """Test xpath_value_matches with matching pattern."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="20200101" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = RuleBuilder.xpath_value_matches(
            "valid_date",
            "//cda:effectiveTime/@value",
            r"^\d{8}$",
        )

        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_xpath_value_matches_failed(self):
        """Test xpath_value_matches with non-matching pattern."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="invalid" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = RuleBuilder.xpath_value_matches(
            "valid_date",
            "//cda:effectiveTime/@value",
            r"^\d{8}$",
        )

        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "does not match pattern" in issues[0].message

    def test_xpath_value_in_set(self):
        """Test xpath_value_in_set with valid value."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <patient>
                <administrativeGenderCode code="M" />
            </patient>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = RuleBuilder.xpath_value_in_set(
            "valid_gender",
            "//cda:administrativeGenderCode/@code",
            allowed_values={"M", "F", "UN"},
        )

        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_xpath_value_in_set_failed(self):
        """Test xpath_value_in_set with invalid value."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <patient>
                <administrativeGenderCode code="X" />
            </patient>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = RuleBuilder.xpath_value_in_set(
            "valid_gender",
            "//cda:administrativeGenderCode/@code",
            allowed_values={"M", "F", "UN"},
        )

        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "not in allowed set" in issues[0].message

    def test_composite_all_must_pass(self, sample_document):
        """Test composite rule where all must pass."""
        rule1 = RuleBuilder.xpath_exists("has_section", "//cda:section")
        rule2 = RuleBuilder.xpath_count("min_sections", "//cda:section", min_count=1)

        composite = RuleBuilder.composite(
            "complete_check",
            "Check section presence and count",
            rules=[rule1, rule2],
            all_must_pass=True,
        )

        issues = composite.validate(sample_document)
        assert len(issues) == 0

    def test_composite_all_must_pass_one_fails(self, sample_document):
        """Test composite rule when one sub-rule fails."""
        rule1 = RuleBuilder.xpath_exists("has_section", "//cda:section")
        rule2 = RuleBuilder.xpath_count("too_many_sections", "//cda:section", min_count=10)

        composite = RuleBuilder.composite(
            "complete_check",
            "Check section presence and count",
            rules=[rule1, rule2],
            all_must_pass=True,
        )

        issues = composite.validate(sample_document)
        assert len(issues) == 1  # One sub-rule failed

    def test_composite_at_least_one_all_fail(self, sample_document):
        """Test composite rule where all sub-rules fail."""
        # Both rules should fail
        rule1 = RuleBuilder.xpath_exists("has_patient", "//cda:patient")
        rule2 = RuleBuilder.xpath_count("too_many_sections", "//cda:section", min_count=10)

        composite = RuleBuilder.composite(
            "flexible_check",
            "At least one check must pass",
            rules=[rule1, rule2],
            all_must_pass=False,
        )

        issues = composite.validate(sample_document)
        assert len(issues) == 1  # All rules failed
        assert "none of the" in issues[0].message.lower()

    def test_xpath_count_description_with_exact(self):
        """Test xpath_count builds correct description with exact count."""
        rule = RuleBuilder.xpath_count(
            "exact_sections",
            "//cda:section",
            exact_count=5,
        )

        assert "exactly 5" in rule.description

    def test_xpath_count_description_with_min_only(self):
        """Test xpath_count builds correct description with min only."""
        rule = RuleBuilder.xpath_count(
            "min_sections",
            "//cda:section",
            min_count=3,
        )

        assert "min 3" in rule.description

    def test_xpath_count_description_with_max_only(self):
        """Test xpath_count builds correct description with max only."""
        rule = RuleBuilder.xpath_count(
            "max_sections",
            "//cda:section",
            max_count=10,
        )

        assert "max 10" in rule.description


class TestFunctionBasedRule:
    """Test suite for FunctionBasedRule."""

    def test_function_returning_none(self):
        """Test function that returns None (valid)."""

        def check_func(doc):
            return None

        rule = FunctionBasedRule("test", "Test rule", check_func)
        doc = etree.Element("root")
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_function_returning_single_issue(self):
        """Test function that returns single ValidationIssue."""

        def check_func(doc):
            return ValidationIssue(
                level=ValidationLevel.ERROR,
                message="Error found",
            )

        rule = FunctionBasedRule("test", "Test rule", check_func)
        doc = etree.Element("root")
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert issues[0].message == "Error found"

    def test_function_returning_list_of_issues(self):
        """Test function that returns list of ValidationIssues."""

        def check_func(doc):
            return [
                ValidationIssue(level=ValidationLevel.ERROR, message="Error 1"),
                ValidationIssue(level=ValidationLevel.WARNING, message="Warning 1"),
            ]

        rule = FunctionBasedRule("test", "Test rule", check_func)
        doc = etree.Element("root")
        issues = rule.validate(doc)
        assert len(issues) == 2

    def test_function_returning_invalid_type(self):
        """Test function that returns invalid type."""

        def check_func(doc):
            return "invalid"

        rule = FunctionBasedRule("test", "Test rule", check_func)
        doc = etree.Element("root")

        with pytest.raises(TypeError, match="must return None, ValidationIssue"):
            rule.validate(doc)
