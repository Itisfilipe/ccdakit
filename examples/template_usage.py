#!/usr/bin/env python3
"""
Example: Using Document Templates for Quick Start

This example demonstrates how to use the DocumentTemplates utility
to quickly generate C-CDA documents using pre-configured templates
with sample data.
"""

from datetime import datetime

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.builders.sections.vital_signs import VitalSignsSection
from ccdakit.core.base import CDAVersion
from ccdakit.utils.templates import DocumentTemplates


def example_minimal_template():
    """Example 1: Generate document using minimal CCD template."""
    print("\n" + "=" * 70)
    print("Example 1: Minimal CCD Template")
    print("=" * 70)

    # Load minimal template with sample data
    template = DocumentTemplates.minimal_ccd_template()

    print(f"\nTemplate loaded: {template['metadata']['title']}")
    print(f"Patient: {template['patient'].first_name} {template['patient'].last_name}")
    print(f"DOB: {template['patient'].date_of_birth}")

    # Create C-CDA document using template data
    doc = ClinicalDocument(
        patient=template["patient"],
        author=template["author"],
        custodian=template["custodian"],
        title="Minimal C-CDA Example",
        document_id="MIN-DOC-001",
        effective_time=datetime.now(),
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = doc.to_xml_string(pretty=True)

    print("\nDocument generated successfully!")
    print(f"Size: {len(xml_string):,} bytes")
    print("Preview (first 500 chars):")
    print("-" * 70)
    print(xml_string[:500])
    print("...")

    # Save to file
    output_file = "output_minimal_template.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")

    return xml_string


def example_full_template():
    """Example 2: Generate document using full CCD template."""
    print("\n" + "=" * 70)
    print("Example 2: Full CCD Template with All Sections")
    print("=" * 70)

    # Load full template with comprehensive sample data
    template = DocumentTemplates.full_ccd_template()

    print(f"\nTemplate loaded: {template['metadata']['title']}")
    print(f"Patient: {template['patient'].first_name} {template['patient'].last_name}")

    sections_data = template["sections"]
    print("\nClinical data loaded:")
    print(f"  - Problems: {len(sections_data['problems'])}")
    print(f"  - Medications: {len(sections_data['medications'])}")
    print(f"  - Allergies: {len(sections_data['allergies'])}")
    print(f"  - Immunizations: {len(sections_data['immunizations'])}")
    print(f"  - Vital Signs: {len(sections_data['vital_signs'])} organizers")
    print(f"  - Procedures: {len(sections_data['procedures'])}")
    print(f"  - Results: {len(sections_data['results'])} organizers")
    print(f"  - Encounters: {len(sections_data['encounters'])}")
    print(f"  - Social History: {len(sections_data['smoking_status'])} entries")

    # Build sections
    sections = []

    # Problems section
    problems_section = ProblemsSection(
        problems=sections_data["problems"],
        title="Problems",
        version=CDAVersion.R2_1,
    )
    sections.append(problems_section)

    # Medications section
    medications_section = MedicationsSection(
        medications=sections_data["medications"],
        title="Medications",
        version=CDAVersion.R2_1,
    )
    sections.append(medications_section)

    # Allergies section
    allergies_section = AllergiesSection(
        allergies=sections_data["allergies"],
        title="Allergies and Intolerances",
        version=CDAVersion.R2_1,
    )
    sections.append(allergies_section)

    # Immunizations section
    immunizations_section = ImmunizationsSection(
        immunizations=sections_data["immunizations"],
        title="Immunization History",
        version=CDAVersion.R2_1,
    )
    sections.append(immunizations_section)

    # Vital Signs section
    vital_signs_section = VitalSignsSection(
        vital_signs_organizers=sections_data["vital_signs"],
        title="Vital Signs",
        version=CDAVersion.R2_1,
    )
    sections.append(vital_signs_section)

    # Create complete document
    doc = ClinicalDocument(
        patient=template["patient"],
        author=template["author"],
        custodian=template["custodian"],
        sections=sections,
        title="Complete C-CDA with All Sections",
        document_id="FULL-DOC-001",
        effective_time=datetime.now(),
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = doc.to_xml_string(pretty=True)

    print("\nComplete document generated!")
    print(f"Size: {len(xml_string):,} bytes")
    print(f"Sections: {len(sections)}")

    # Save to file
    output_file = "output_full_template.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")

    return xml_string


def example_empty_template():
    """Example 3: Start with empty template and customize."""
    print("\n" + "=" * 70)
    print("Example 3: Empty Template for Discharge Summary")
    print("=" * 70)

    # Load empty discharge summary template
    template = DocumentTemplates.empty_template("discharge_summary")

    print(f"\nTemplate loaded: {template['metadata']['title']}")
    print(f"Document type: {template['metadata']['document_type']}")
    print(f"Template ID: {template['metadata']['template_id']}")

    # Customize patient data
    patient = template["patient"]
    patient.first_name = "Alice"
    patient.last_name = "Williams"
    patient.sex = "F"

    # Update address
    patient.addresses[0].street_lines = ["456 Hospital Avenue"]
    patient.addresses[0].city = "Cambridge"
    patient.addresses[0].state = "MA"
    patient.addresses[0].postal_code = "02139"

    print("\nCustomized patient:")
    print(f"  Name: {patient.first_name} {patient.last_name}")
    print(f"  Address: {patient.addresses[0].city}, {patient.addresses[0].state}")

    # Create document
    doc = ClinicalDocument(
        patient=template["patient"],
        author=template["author"],
        custodian=template["custodian"],
        title="Hospital Discharge Summary",
        document_id="DISCHARGE-001",
        effective_time=datetime.now(),
        version=CDAVersion.R2_1,
    )

    xml_string = doc.to_xml_string(pretty=True)

    print("\nDischarge summary generated!")
    print(f"Size: {len(xml_string):,} bytes")

    # Save to file
    output_file = "output_discharge_template.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")

    return xml_string


def example_list_templates():
    """Example 4: List all available templates."""
    print("\n" + "=" * 70)
    print("Example 4: List Available Templates")
    print("=" * 70)

    templates = DocumentTemplates.list_available_templates()

    print(f"\nFound {len(templates)} available templates:")
    for template_name in templates:
        print(f"  - {template_name}")

    print("\nYou can load any template using:")
    print("  DocumentTemplates.minimal_ccd_template()")
    print("  DocumentTemplates.full_ccd_template()")
    print("  DocumentTemplates.empty_template('discharge_summary')")
    print("  DocumentTemplates.empty_template('progress_note')")


def example_template_inspection():
    """Example 5: Inspect template structure."""
    print("\n" + "=" * 70)
    print("Example 5: Inspect Template Structure")
    print("=" * 70)

    template = DocumentTemplates.minimal_ccd_template()

    print("\nTemplate structure:")
    print(f"  Keys: {list(template.keys())}")

    print("\n  Patient attributes:")
    patient = template["patient"]
    for attr in dir(patient):
        if not attr.startswith("_"):
            value = getattr(patient, attr, None)
            if value is not None and not callable(value):
                print(f"    - {attr}: {value}")

    print("\n  Section types available:")
    sections = template["sections"]
    for section_name, section_data in sections.items():
        print(f"    - {section_name}: {len(section_data)} entries")

    print("\n  Metadata:")
    metadata = template["metadata"]
    for key, value in metadata.items():
        print(f"    - {key}: {value}")


def example_modify_template_data():
    """Example 6: Modify template data before generating document."""
    print("\n" + "=" * 70)
    print("Example 6: Modify Template Data")
    print("=" * 70)

    # Load template
    template = DocumentTemplates.minimal_ccd_template()

    print("\nOriginal patient data:")
    patient = template["patient"]
    print(f"  Name: {patient.first_name} {patient.last_name}")
    print(f"  DOB: {patient.date_of_birth}")
    print(f"  City: {patient.addresses[0].city}")

    # Modify patient data
    patient.first_name = "Michael"
    patient.last_name = "Chen"
    patient.addresses[0].city = "San Francisco"
    patient.addresses[0].state = "CA"
    patient.addresses[0].postal_code = "94102"

    print("\nModified patient data:")
    print(f"  Name: {patient.first_name} {patient.last_name}")
    print(f"  DOB: {patient.date_of_birth}")
    print(f"  City: {patient.addresses[0].city}")

    # Modify problem
    problem = template["sections"]["problems"][0]
    print(f"\nOriginal problem: {problem.name}")
    problem.name = "Type 2 Diabetes Mellitus"
    problem.code = "44054006"
    print(f"Modified problem: {problem.name}")

    # Create document with modified data
    doc = ClinicalDocument(
        patient=template["patient"],
        author=template["author"],
        custodian=template["custodian"],
        title="Modified Template Document",
        document_id="MOD-DOC-001",
        effective_time=datetime.now(),
        version=CDAVersion.R2_1,
    )

    xml_string = doc.to_xml_string(pretty=True)

    print("\nDocument with modifications generated!")
    print(f"Size: {len(xml_string):,} bytes")

    # Save to file
    output_file = "output_modified_template.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")


def main():
    """Run all template usage examples."""
    print("\n" + "=" * 70)
    print("ccdakit Template Usage Examples")
    print("=" * 70)
    print("\nThese examples demonstrate how to use pre-configured")
    print("templates to quickly generate C-CDA documents.")

    # Run examples
    example_minimal_template()
    example_full_template()
    example_empty_template()
    example_list_templates()
    example_template_inspection()
    example_modify_template_data()

    print("\n" + "=" * 70)
    print("All Examples Complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - output_minimal_template.xml")
    print("  - output_full_template.xml")
    print("  - output_discharge_template.xml")
    print("  - output_modified_template.xml")
    print("\nKey features demonstrated:")
    print("  - Loading pre-configured templates")
    print("  - Minimal vs. full templates")
    print("  - Empty templates for customization")
    print("  - Listing available templates")
    print("  - Inspecting template structure")
    print("  - Modifying template data")
    print("  - Generating C-CDA documents from templates")
    print("\nBenefits of using templates:")
    print("  - Instant working examples")
    print("  - No need to create data models from scratch")
    print("  - Easy customization of pre-configured data")
    print("  - Learning tool for understanding C-CDA structure")
    print("  - Rapid prototyping and testing")
    print()


if __name__ == "__main__":
    main()
