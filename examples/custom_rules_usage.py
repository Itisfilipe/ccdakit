"""
Example demonstrating custom validation rules usage.

This example shows:
1. Using built-in validation rules
2. Creating custom validation rules
3. Using the RuleBuilder for simple rules
4. Combining multiple rules
5. Organization-specific validation scenarios
"""

from datetime import date

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.entries import AllergyEntry, MedicationEntry, ProblemEntry
from ccdakit.builders.header import AuthorBuilder, CustodianBuilder, PatientBuilder
from ccdakit.builders.sections import (
    AllergiesSection,
    MedicationsSection,
    ProblemsSection,
)
from ccdakit.core.base import CDAVersion
from ccdakit.core.validation import ValidationIssue, ValidationLevel
from ccdakit.validators import common_rules
from ccdakit.validators.rule_builder import RuleBuilder
from ccdakit.validators.rules import (
    DateConsistencyRule,
    MedicationDosageRule,
    NarrativePresenceRule,
    RequiredSectionsRule,
    RulesEngine,
    ValidationRule,
)


def example_1_built_in_rules():
    """Example 1: Using built-in validation rules."""
    print("=" * 80)
    print("Example 1: Using Built-in Validation Rules")
    print("=" * 80)

    # Create a simple document
    patient = PatientBuilder(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1980, 1, 1),
        sex="M",
    ).build()

    author = AuthorBuilder(first_name="Jane", last_name="Smith", time=date(2024, 1, 15)).build()

    custodian = CustodianBuilder(name="Test Hospital").build()

    doc = ClinicalDocument(
        patient=patient,
        author=author,
        custodian=custodian,
        version=CDAVersion.R2_1,
    )

    # Add problems section
    problem = ProblemEntry(
        problem_name="Essential Hypertension",
        problem_code="59621000",
        problem_code_system="SNOMED",
        onset_date=date(2020, 1, 1),
        status="active",
    ).build()

    problems_section = ProblemsSection(entries=[problem])
    doc.add_section(problems_section.build())

    # Build XML
    xml_element = doc.build()

    # Create rules engine with built-in rules
    engine = RulesEngine()

    # Add various built-in rules
    engine.add_rule(common_rules.UniqueIDRule())
    engine.add_rule(common_rules.PatientNameRule())
    engine.add_rule(common_rules.DocumentDateRule())
    engine.add_rule(common_rules.AuthorPresenceRule())
    engine.add_rule(common_rules.CustodianPresenceRule())
    engine.add_rule(common_rules.SectionCountRule(min_sections=1))

    print(f"\nRunning {len(engine)} built-in validation rules...")
    result = engine.validate(xml_element)

    print(f"\nValidation Result: {'PASSED' if result.is_valid else 'FAILED'}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    print()


def example_2_custom_rule_class():
    """Example 2: Creating custom validation rule by subclassing."""
    print("=" * 80)
    print("Example 2: Creating Custom Validation Rule (Subclassing)")
    print("=" * 80)

    # Define a custom organization-specific rule
    class OrganizationSpecificRule(ValidationRule):
        """Custom rule: All problems must have onset dates."""

        def __init__(self):
            super().__init__(
                name="problem_onset_required",
                description="All problems must have onset dates (org policy)",
            )

        def validate(self, document):
            issues = []
            ns = {"cda": "urn:hl7-org:v3"}

            # Find all problem observations
            problems = document.xpath(
                "//cda:observation[cda:templateId/@root='2.16.840.1.113883.10.20.22.4.4']",
                namespaces=ns,
            )

            for idx, problem in enumerate(problems, 1):
                # Check for effectiveTime with low value
                onset_dates = problem.xpath("cda:effectiveTime/cda:low/@value", namespaces=ns)

                if not onset_dates:
                    issues.append(
                        ValidationIssue(
                            level=ValidationLevel.ERROR,
                            message=f"Problem {idx} is missing onset date (required by organization policy)",
                            code="missing_problem_onset",
                            location=f"//observation[{idx}]/effectiveTime",
                        )
                    )

            return issues

    # Create document
    patient = PatientBuilder(
        first_name="Jane", last_name="Smith", date_of_birth=date(1990, 5, 15), sex="F"
    ).build()

    author = AuthorBuilder(first_name="Dr", last_name="Jones", time=date(2024, 1, 15)).build()

    custodian = CustodianBuilder(name="Acme Hospital").build()

    doc = ClinicalDocument(
        patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
    )

    # Add problem WITHOUT onset date (will fail validation)
    problem = ProblemEntry(
        problem_name="Type 2 Diabetes",
        problem_code="44054006",
        problem_code_system="SNOMED",
        status="active",
    ).build()

    problems_section = ProblemsSection(entries=[problem])
    doc.add_section(problems_section.build())

    xml_element = doc.build()

    # Validate with custom rule
    engine = RulesEngine()
    engine.add_rule(OrganizationSpecificRule())

    print("\nRunning custom organization-specific rule...")
    result = engine.validate(xml_element)

    print(f"\nValidation Result: {'PASSED' if result.is_valid else 'FAILED'}")
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

    print()


def example_3_rule_builder():
    """Example 3: Using RuleBuilder for simple rules."""
    print("=" * 80)
    print("Example 3: Using RuleBuilder for Simple Rules")
    print("=" * 80)

    # Create document
    patient = PatientBuilder(
        first_name="Bob", last_name="Johnson", date_of_birth=date(1975, 3, 20), sex="M"
    ).build()

    author = AuthorBuilder(first_name="Dr", last_name="Williams", time=date(2024, 1, 15)).build()

    custodian = CustodianBuilder(name="City Hospital").build()

    doc = ClinicalDocument(
        patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
    )

    # Add multiple sections
    problem = ProblemEntry(
        problem_name="Asthma",
        problem_code="195967001",
        problem_code_system="SNOMED",
        onset_date=date(2015, 6, 1),
        status="active",
    ).build()

    medication = MedicationEntry(
        medication_name="Albuterol Inhaler",
        medication_code="745752",
        medication_code_system="RxNorm",
        dosage_value=2.0,
        dosage_unit="puffs",
        route_code="C38216",
        frequency="Q4H PRN",
    ).build()

    doc.add_section(ProblemsSection(entries=[problem]).build())
    doc.add_section(MedicationsSection(entries=[medication]).build())

    xml_element = doc.build()

    # Create rules using RuleBuilder
    engine = RulesEngine()

    # Rule 1: Check document has at least 2 sections
    engine.add_rule(
        RuleBuilder.xpath_count(
            "min_sections",
            "//cda:section",
            min_count=2,
            error_message="Document must have at least 2 sections",
        )
    )

    # Rule 2: Check patient has ID
    engine.add_rule(
        RuleBuilder.xpath_exists(
            "patient_id",
            "//cda:recordTarget/cda:patientRole/cda:id",
            error_message="Patient must have an ID",
        )
    )

    # Rule 3: Check document title exists
    engine.add_rule(
        RuleBuilder.xpath_exists(
            "document_title",
            "/cda:ClinicalDocument/cda:title",
            error_message="Document must have a title",
        )
    )

    # Rule 4: Simple predicate rule
    engine.add_rule(
        RuleBuilder.create(
            "has_content",
            "Document must have sections",
            lambda doc: len(doc.xpath("//cda:section", namespaces={"cda": "urn:hl7-org:v3"})) > 0,
            error_message="Document has no clinical content",
        )
    )

    print(f"\nRunning {len(engine)} RuleBuilder-created rules...")
    result = engine.validate(xml_element)

    print(f"\nValidation Result: {'PASSED' if result.is_valid else 'FAILED'}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    print()


def example_4_combined_rules():
    """Example 4: Combining multiple rule types."""
    print("=" * 80)
    print("Example 4: Combining Multiple Rule Types")
    print("=" * 80)

    # Create comprehensive document
    patient = PatientBuilder(
        first_name="Alice",
        last_name="Brown",
        date_of_birth=date(1985, 7, 10),
        sex="F",
    ).build()

    author = AuthorBuilder(first_name="Dr", last_name="Taylor", time=date(2024, 1, 15)).build()

    custodian = CustodianBuilder(name="Memorial Hospital").build()

    doc = ClinicalDocument(
        patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
    )

    # Add sections
    problem = ProblemEntry(
        problem_name="Hypertension",
        problem_code="59621000",
        problem_code_system="SNOMED",
        onset_date=date(2018, 3, 1),
        status="active",
    ).build()

    medication = MedicationEntry(
        medication_name="Lisinopril 10mg",
        medication_code="314076",
        medication_code_system="RxNorm",
        dosage_value=10.0,
        dosage_unit="mg",
        route_code="C38288",
        frequency="QD",
    ).build()

    allergy = AllergyEntry(
        allergen="Penicillin",
        allergen_code="91936005",
        allergen_code_system="SNOMED",
        reaction="Rash",
        reaction_code="271807003",
        severity="Moderate",
        status="active",
    ).build()

    doc.add_section(ProblemsSection(entries=[problem]).build())
    doc.add_section(MedicationsSection(entries=[medication]).build())
    doc.add_section(AllergiesSection(entries=[allergy]).build())

    xml_element = doc.build()

    # Create comprehensive validation engine
    engine = RulesEngine()

    # 1. Add common built-in rules
    engine.add_rule(common_rules.UniqueIDRule())
    engine.add_rule(common_rules.PatientNameRule())
    engine.add_rule(common_rules.DocumentDateRule())
    engine.add_rule(common_rules.AuthorPresenceRule())
    engine.add_rule(common_rules.CustodianPresenceRule())

    # 2. Add section-specific rules
    engine.add_rule(
        RequiredSectionsRule(
            required_sections=["11450-4", "10160-0", "48765-2"],
            section_names={
                "11450-4": "Problems",
                "10160-0": "Medications",
                "48765-2": "Allergies",
            },
            level=ValidationLevel.WARNING,
        )
    )

    # 3. Add clinical rules
    engine.add_rule(MedicationDosageRule(min_dosage=0.1, max_dosage=1000.0))
    engine.add_rule(DateConsistencyRule(allow_future_dates=False))
    engine.add_rule(NarrativePresenceRule(min_length=5))

    # 4. Add RuleBuilder rules
    engine.add_rule(
        RuleBuilder.xpath_count(
            "adequate_sections",
            "//cda:section",
            min_count=3,
            error_message="Document should have at least 3 clinical sections",
            level=ValidationLevel.WARNING,
        )
    )

    print(f"\nRunning {len(engine)} combined validation rules...")
    print("\nRules:")
    for rule_name in engine.list_rules():
        print(f"  - {rule_name}")

    result = engine.validate(xml_element)

    print(f"\nValidation Result: {'PASSED' if result.is_valid else 'FAILED'}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")
    print(f"Info: {len(result.infos)}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    print()


def example_5_organization_workflow():
    """Example 5: Complete organization-specific validation workflow."""
    print("=" * 80)
    print("Example 5: Organization-Specific Validation Workflow")
    print("=" * 80)

    # Scenario: Hospital requires specific validation for discharge summaries
    # - Must have problems, medications, and discharge instructions
    # - All medications must have dosages
    # - All problems must have status
    # - Patient must have contact info
    # - No future dates allowed

    patient = PatientBuilder(
        first_name="Charlie",
        last_name="Davis",
        date_of_birth=date(1960, 11, 5),
        sex="M",
    ).build()

    author = AuthorBuilder(first_name="Dr", last_name="Martinez", time=date(2024, 1, 15)).build()

    custodian = CustodianBuilder(name="County Hospital").build()

    doc = ClinicalDocument(
        patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
    )

    # Add clinical content
    problem = ProblemEntry(
        problem_name="Congestive Heart Failure",
        problem_code="42343007",
        problem_code_system="SNOMED",
        onset_date=date(2020, 5, 1),
        status="active",
    ).build()

    medication = MedicationEntry(
        medication_name="Furosemide 40mg",
        medication_code="310429",
        medication_code_system="RxNorm",
        dosage_value=40.0,
        dosage_unit="mg",
        route_code="C38288",
        frequency="BID",
    ).build()

    doc.add_section(ProblemsSection(entries=[problem]).build())
    doc.add_section(MedicationsSection(entries=[medication]).build())

    xml_element = doc.build()

    # Create organization-specific validation suite
    print("\nCreating 'County Hospital Discharge Summary' validation suite...")

    discharge_engine = RulesEngine()

    # Required sections for discharge summary
    discharge_engine.add_rule(
        RequiredSectionsRule(
            required_sections=["11450-4", "10160-0"],
            section_names={"11450-4": "Problems", "10160-0": "Medications"},
            level=ValidationLevel.ERROR,
        )
    )

    # Patient information requirements
    discharge_engine.add_rule(common_rules.PatientNameRule())
    discharge_engine.add_rule(
        common_rules.ContactInfoPresenceRule(
            require_telecom=True, require_address=True, level=ValidationLevel.WARNING
        )
    )

    # Document requirements
    discharge_engine.add_rule(common_rules.DocumentDateRule(allow_future=False))
    discharge_engine.add_rule(common_rules.AuthorPresenceRule(require_name=True))
    discharge_engine.add_rule(common_rules.CustodianPresenceRule())

    # Clinical content requirements
    discharge_engine.add_rule(MedicationDosageRule(min_dosage=0.001, max_dosage=5000.0))
    discharge_engine.add_rule(common_rules.ProblemStatusRule())
    discharge_engine.add_rule(NarrativePresenceRule(min_length=10))

    # Data quality checks
    discharge_engine.add_rule(common_rules.UniqueIDRule())
    discharge_engine.add_rule(DateConsistencyRule(allow_future_dates=False))

    print(f"\nValidation suite has {len(discharge_engine)} rules")
    print("\nRunning validation...")

    result = discharge_engine.validate(xml_element)

    print(f"\nValidation Result: {'PASSED' if result.is_valid else 'FAILED'}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")

    if result.errors:
        print("\nErrors (Must Fix):")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print("\nWarnings (Should Fix):")
        for warning in result.warnings:
            print(f"  - {warning}")

    # Show how to save/reuse validation configuration
    print("\n" + "=" * 80)
    print("Tip: Save this validation configuration for reuse across documents")
    print("=" * 80)
    print("\nYou can:")
    print("1. Create a factory function that returns a configured RulesEngine")
    print("2. Store rule configurations in JSON/YAML")
    print("3. Create validation profiles for different document types")
    print("4. Share validation suites across your organization")
    print()


if __name__ == "__main__":
    """Run all examples."""
    example_1_built_in_rules()
    example_2_custom_rule_class()
    example_3_rule_builder()
    example_4_combined_rules()
    example_5_organization_workflow()

    print("=" * 80)
    print("All Examples Complete!")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Review CUSTOM_RULES_GUIDE.md for detailed documentation")
    print("2. Create your own organization-specific validation rules")
    print("3. Combine rules into validation profiles")
    print("4. Integrate validation into your C-CDA generation workflow")
    print()
