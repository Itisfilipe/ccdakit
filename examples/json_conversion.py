#!/usr/bin/env python3
"""
Example: JSON/Dict to C-CDA Conversion

This example demonstrates how to use the DictToCCDAConverter to convert
JSON files and Python dictionaries into valid C-CDA R2.1 documents.

The converter supports:
- Loading C-CDA data from JSON files
- Converting Python dictionaries to C-CDA documents
- All major C-CDA sections (problems, medications, allergies, etc.)
- Automatic date/datetime conversion
- Flexible section configuration
"""

import json
from pathlib import Path

from ccdakit.utils.converters import DictToCCDAConverter


def example_1_minimal_json_file():
    """Example 1: Load minimal patient data from JSON file."""
    print("=" * 70)
    print("Example 1: Loading Minimal Patient from JSON File")
    print("=" * 70)

    # Load JSON file
    json_path = Path(__file__).parent / "json_data" / "minimal_patient.json"
    print(f"\nLoading: {json_path}")

    # Convert to C-CDA document
    doc = DictToCCDAConverter.from_json_file(json_path)

    # Generate XML
    xml = doc.to_xml_string(pretty=True)

    # Save output
    output_file = "output_minimal_from_json.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print("\nDocument Info:")
    print(f"  Title: {doc.title}")
    print(f"  Patient: {doc.patient.first_name} {doc.patient.last_name}")
    print(f"  DOB: {doc.patient.date_of_birth}")
    print(f"  Provider: Dr. {doc.author.first_name} {doc.author.last_name}")
    print(f"  Facility: {doc.custodian.name}")
    print(f"  Sections: {len(doc.sections)}")
    print(f"\nSaved to: {output_file}")
    print(f"Size: {len(xml):,} bytes")


def example_2_complete_json_file():
    """Example 2: Load complete patient record with all sections from JSON."""
    print("\n" + "=" * 70)
    print("Example 2: Loading Complete Patient Record from JSON File")
    print("=" * 70)

    # Load complete JSON file
    json_path = Path(__file__).parent / "json_data" / "complete_patient.json"
    print(f"\nLoading: {json_path}")

    # Convert to C-CDA document
    doc = DictToCCDAConverter.from_json_file(json_path)

    # Generate XML
    xml = doc.to_xml_string(pretty=True)

    # Save output
    output_file = "output_complete_from_json.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print("\nDocument Info:")
    print(f"  Title: {doc.title}")
    print(f"  Document ID: {doc.document_id}")
    print(f"  Patient: {doc.patient.first_name} {doc.patient.last_name}")
    print(f"  Sections: {len(doc.sections)}")
    print("\nSection Details:")
    for i, section in enumerate(doc.sections, 1):
        section_name = section.__class__.__name__
        print(f"    {i}. {section_name}")

    print(f"\nSaved to: {output_file}")
    print(f"Size: {len(xml):,} bytes")

    # Show XML preview
    print("\nXML Preview (first 1000 characters):")
    print("-" * 70)
    print(xml[:1000])
    print("...")


def example_3_dict_conversion():
    """Example 3: Convert Python dictionary directly to C-CDA."""
    print("\n" + "=" * 70)
    print("Example 3: Converting Python Dictionary to C-CDA")
    print("=" * 70)

    # Create patient data as Python dict
    patient_data = {
        "patient": {
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1985-08-22",
            "sex": "F",
            "addresses": [
                {
                    "street_lines": ["456 Oak Avenue"],
                    "city": "Cambridge",
                    "state": "MA",
                    "postal_code": "02139",
                    "country": "US",
                }
            ],
            "telecoms": [{"type": "phone", "value": "617-555-7890", "use": "mobile"}],
        },
        "author": {
            "first_name": "Robert",
            "last_name": "Johnson",
            "npi": "5555555555",
            "addresses": [],
            "telecoms": [],
        },
        "custodian": {
            "name": "Cambridge Medical Center",
            "npi": "9999999999",
            "oid_root": "2.16.840.1.113883.3.EXAMPLE2",
            "addresses": [],
            "telecoms": [],
        },
        "document": {
            "title": "Patient Summary - Dict Example",
            "document_id": "DICT-EXAMPLE-001",
        },
        "sections": [
            {
                "type": "problems",
                "title": "Active Problems",
                "data": [
                    {
                        "name": "Migraine",
                        "code": "37796009",
                        "code_system": "SNOMED",
                        "status": "active",
                        "onset_date": "2020-03-15",
                    },
                    {
                        "name": "Seasonal Allergies",
                        "code": "367498001",
                        "code_system": "SNOMED",
                        "status": "active",
                        "onset_date": "2015-01-01",
                    },
                ],
            },
            {
                "type": "medications",
                "title": "Current Medications",
                "data": [
                    {
                        "name": "Sumatriptan 50mg oral tablet",
                        "code": "106517",
                        "dosage": "50 mg",
                        "route": "oral",
                        "frequency": "as needed",
                        "start_date": "2020-04-01",
                        "status": "active",
                        "instructions": "Take at first sign of migraine",
                    }
                ],
            },
        ],
    }

    # Convert to C-CDA document
    print("\nConverting dictionary to C-CDA document...")
    doc = DictToCCDAConverter.from_dict(patient_data)

    # Generate XML
    xml = doc.to_xml_string(pretty=True)

    # Save output
    output_file = "output_from_dict.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print("\nDocument Info:")
    print(f"  Title: {doc.title}")
    print(f"  Patient: {doc.patient.first_name} {doc.patient.last_name}")
    print(f"  Sections: {len(doc.sections)}")
    print(f"\nSaved to: {output_file}")
    print(f"Size: {len(xml):,} bytes")


def example_4_incremental_sections():
    """Example 4: Build document incrementally by adding sections."""
    print("\n" + "=" * 70)
    print("Example 4: Building Document with Incremental Sections")
    print("=" * 70)

    # Base patient data
    base_data = {
        "patient": {
            "first_name": "Michael",
            "last_name": "Brown",
            "date_of_birth": "1992-11-10",
            "sex": "M",
            "addresses": [],
            "telecoms": [],
        },
        "author": {
            "first_name": "Sarah",
            "last_name": "Williams",
            "npi": "7777777777",
            "addresses": [],
            "telecoms": [],
        },
        "custodian": {
            "name": "General Hospital",
            "npi": "8888888888",
            "oid_root": "2.16.840.1.113883.3.EXAMPLE3",
            "addresses": [],
            "telecoms": [],
        },
        "sections": [],
    }

    # Add problems section
    print("\nAdding Problems section...")
    base_data["sections"].append(
        {
            "type": "problems",
            "data": [
                {
                    "name": "Asthma",
                    "code": "195967001",
                    "code_system": "SNOMED",
                    "status": "active",
                    "onset_date": "2010-05-01",
                }
            ],
        }
    )

    # Add medications section
    print("Adding Medications section...")
    base_data["sections"].append(
        {
            "type": "medications",
            "data": [
                {
                    "name": "Albuterol inhaler",
                    "code": "745752",
                    "dosage": "90 mcg",
                    "route": "inhalation",
                    "frequency": "as needed",
                    "start_date": "2010-06-01",
                    "status": "active",
                }
            ],
        }
    )

    # Add vital signs section
    print("Adding Vital Signs section...")
    base_data["sections"].append(
        {
            "type": "vital_signs",
            "data": [
                {
                    "date": "2024-01-15T14:00:00",
                    "vital_signs": [
                        {
                            "type": "Peak Expiratory Flow Rate",
                            "code": "33452-4",
                            "value": "450",
                            "unit": "L/min",
                            "date": "2024-01-15T14:00:00",
                        }
                    ],
                }
            ],
        }
    )

    # Convert to C-CDA document
    print("\nConverting to C-CDA document...")
    doc = DictToCCDAConverter.from_dict(base_data)

    # Generate XML
    xml = doc.to_xml_string(pretty=True)

    # Save output
    output_file = "output_incremental_sections.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print("\nDocument Info:")
    print(f"  Patient: {doc.patient.first_name} {doc.patient.last_name}")
    print(f"  Total Sections: {len(doc.sections)}")
    for i, section in enumerate(doc.sections, 1):
        print(f"    {i}. {section.__class__.__name__}")

    print(f"\nSaved to: {output_file}")
    print(f"Size: {len(xml):,} bytes")


def example_5_read_and_modify():
    """Example 5: Read JSON, modify, and generate new document."""
    print("\n" + "=" * 70)
    print("Example 5: Reading, Modifying, and Regenerating Document")
    print("=" * 70)

    # Load existing JSON
    json_path = Path(__file__).parent / "json_data" / "minimal_patient.json"
    print(f"\nLoading: {json_path}")

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Modify the data
    print("\nModifying patient data...")
    data["patient"]["first_name"] = "Jennifer"
    data["patient"]["last_name"] = "Modified"
    data["document"]["title"] = "Modified Patient Summary"
    data["document"]["document_id"] = "MODIFIED-DOC-001"

    # Add a problems section
    print("Adding new Problems section...")
    data["sections"] = [
        {
            "type": "problems",
            "title": "New Problems Added",
            "data": [
                {
                    "name": "Hypothyroidism",
                    "code": "40930008",
                    "code_system": "SNOMED",
                    "status": "active",
                    "onset_date": "2023-01-01",
                }
            ],
        }
    ]

    # Convert to C-CDA
    print("Converting modified data to C-CDA...")
    doc = DictToCCDAConverter.from_dict(data)

    # Generate XML
    xml = doc.to_xml_string(pretty=True)

    # Save output
    output_file = "output_modified.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print("\nModified Document Info:")
    print(f"  Title: {doc.title}")
    print(f"  Patient: {doc.patient.first_name} {doc.patient.last_name}")
    print(f"  Document ID: {doc.document_id}")
    print(f"  Sections: {len(doc.sections)}")

    print(f"\nSaved to: {output_file}")
    print(f"Size: {len(xml):,} bytes")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("ccdakit: JSON/Dict to C-CDA Conversion Examples")
    print("=" * 70)
    print("\nThis example demonstrates various ways to convert JSON/dict data")
    print("into valid C-CDA R2.1 XML documents using DictToCCDAConverter.")

    # Run examples
    example_1_minimal_json_file()
    example_2_complete_json_file()
    example_3_dict_conversion()
    example_4_incremental_sections()
    example_5_read_and_modify()

    # Summary
    print("\n" + "=" * 70)
    print("Examples Complete!")
    print("=" * 70)
    print("\nGenerated Files:")
    print("  1. output_minimal_from_json.xml")
    print("  2. output_complete_from_json.xml")
    print("  3. output_from_dict.xml")
    print("  4. output_incremental_sections.xml")
    print("  5. output_modified.xml")

    print("\nKey Features Demonstrated:")
    print("  - Loading C-CDA data from JSON files")
    print("  - Converting Python dictionaries to C-CDA documents")
    print("  - Supporting all major sections (problems, medications, etc.)")
    print("  - Automatic date/datetime string conversion")
    print("  - Flexible document configuration")
    print("  - Modifying and regenerating documents")

    print("\nJSON Format:")
    print("  - See examples/json_data/minimal_patient.json for minimal example")
    print("  - See examples/json_data/complete_patient.json for comprehensive example")

    print("\nNext Steps:")
    print("  - Validate generated XML with: python examples/validate_ccda.py")
    print("  - Customize JSON files for your use case")
    print("  - Integrate with your data sources (EHR, FHIR, databases)")
    print("  - Use DictToCCDAConverter in your applications")
    print()


if __name__ == "__main__":
    main()
