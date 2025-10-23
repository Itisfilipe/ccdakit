#!/usr/bin/env python3
"""Example of creating a Postoperative Diagnosis Section.

This example demonstrates how to create a C-CDA Postoperative Diagnosis Section
that records the diagnosis or diagnoses discovered or confirmed during surgery.

Template ID: 2.16.840.1.113883.10.20.22.2.35
Section Code: LOINC 10218-6 "Postoperative Diagnosis"
"""

from ccdakit.builders.sections.postoperative_diagnosis import (
    PostoperativeDiagnosisSection,
)
from ccdakit.core.base import CDAVersion


def main():
    """Generate example Postoperative Diagnosis Section."""
    print("=" * 70)
    print("Example 1: Simple Postoperative Diagnosis")
    print("=" * 70)

    # Create a simple postoperative diagnosis section
    section1 = PostoperativeDiagnosisSection(
        diagnosis_text="Appendicitis with periappendiceal abscess",
    )

    print(section1.to_string(pretty=True))
    print()

    print("=" * 70)
    print("Example 2: Postoperative Diagnosis with Multiple Findings")
    print("=" * 70)

    # Create a section with multiple diagnoses
    section2 = PostoperativeDiagnosisSection(
        diagnosis_text=(
            "1. Acute gangrenous cholecystitis with empyema\n"
            "2. Cholelithiasis with multiple stones\n"
            "3. Chronic inflammation of gallbladder wall\n"
            "4. Mild hepatic steatosis (incidental finding)"
        ),
        title="Postoperative Diagnosis",
    )

    print(section2.to_string(pretty=True))
    print()

    print("=" * 70)
    print("Example 3: Detailed Postoperative Diagnosis")
    print("=" * 70)

    # Create a section with detailed surgical findings
    section3 = PostoperativeDiagnosisSection(
        diagnosis_text=(
            "Acute perforated appendicitis with diffuse peritonitis, "
            "appendiceal abscess measuring 3.5cm in right lower quadrant, "
            "and reactive mesenteric lymphadenopathy. Incidental finding of "
            "Meckel's diverticulum in distal ileum, approximately 60cm from "
            "ileocecal valve."
        ),
    )

    print(section3.to_string(pretty=True))
    print()

    print("=" * 70)
    print("Example 4: Postoperative Diagnosis with R2.0 Version")
    print("=" * 70)

    # Create a section using C-CDA R2.0 version
    section4 = PostoperativeDiagnosisSection(
        diagnosis_text="Perforated gastric ulcer with peritonitis",
        version=CDAVersion.R2_0,
    )

    print(section4.to_string(pretty=True))
    print()

    print("=" * 70)
    print("Example 5: Diagnosis Same as Preoperative")
    print("=" * 70)

    # Create a section where diagnosis matches preoperative
    section5 = PostoperativeDiagnosisSection(
        diagnosis_text="Acute appendicitis (confirmed, same as preoperative diagnosis)",
    )

    print(section5.to_string(pretty=True))
    print()

    print("=" * 70)
    print("Example 6: Cancer Staging Information")
    print("=" * 70)

    # Create a section with cancer staging
    section6 = PostoperativeDiagnosisSection(
        diagnosis_text=(
            "Adenocarcinoma of the sigmoid colon, pT3N1M0, "
            "Stage IIIB (AJCC 8th edition)"
        ),
    )

    print(section6.to_string(pretty=True))
    print()

    print("=" * 70)
    print("Notes:")
    print("=" * 70)
    print("- This section is contained by Operative Note (V3)")
    print("- Template ID: 2.16.840.1.113883.10.20.22.2.35")
    print("- Section Code: LOINC 10218-6")
    print("- This is a narrative-only section (no structured entries)")
    print("- Often the postoperative diagnosis is the same as preoperative")
    print()


if __name__ == "__main__":
    main()
