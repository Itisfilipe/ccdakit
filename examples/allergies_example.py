"""Example of creating an Allergies and Intolerances Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.core.base import CDAVersion


class ExampleAllergy:
    """Example allergy data that satisfies the AllergyProtocol."""

    def __init__(
        self,
        allergen,
        allergen_code=None,
        allergen_code_system=None,
        allergy_type="allergy",
        reaction=None,
        severity=None,
        status="active",
        onset_date=None,
        resolution_date=None,
        clinical_status=None,
        criticality=None,
        negation_ind=None,
    ):
        self._allergen = allergen
        self._allergen_code = allergen_code
        self._allergen_code_system = allergen_code_system
        self._allergy_type = allergy_type
        self._reaction = reaction
        self._severity = severity
        self._status = status
        self._onset_date = onset_date
        self._resolution_date = resolution_date
        self._clinical_status = clinical_status
        self._criticality = criticality
        self._negation_ind = negation_ind

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

    @property
    def resolution_date(self):
        return self._resolution_date

    @property
    def clinical_status(self):
        return self._clinical_status

    @property
    def criticality(self):
        return self._criticality

    @property
    def negation_ind(self):
        return self._negation_ind


def main():
    """Create and display an Allergies and Intolerances Section example."""

    # Create sample allergies with different severities and reactions

    # Example 1: Severe allergy with high criticality
    penicillin_allergy = ExampleAllergy(
        allergen="Penicillin",
        allergen_code="70618",
        allergen_code_system="RxNorm",
        allergy_type="allergy",
        reaction="Anaphylaxis",
        severity="severe",
        status="active",
        onset_date=date(2015, 3, 10),
        clinical_status="active",
        criticality="high",
    )

    # Example 2: Moderate allergy with typical reaction
    peanut_allergy = ExampleAllergy(
        allergen="Peanuts",
        allergen_code="762952008",
        allergen_code_system="SNOMED CT",
        allergy_type="allergy",
        reaction="Hives",
        severity="moderate",
        status="active",
        onset_date=date(2010, 8, 22),
        clinical_status="active",
        criticality="high",
    )

    # Example 3: Mild allergy with low criticality
    latex_allergy = ExampleAllergy(
        allergen="Latex",
        allergen_code="111088007",
        allergen_code_system="SNOMED CT",
        allergy_type="allergy",
        reaction="Contact dermatitis",
        severity="mild",
        status="active",
        onset_date=date(2018, 11, 5),
        clinical_status="active",
        criticality="low",
    )

    # Create the Allergies Section
    section = AllergiesSection(
        allergies=[penicillin_allergy, peanut_allergy, latex_allergy],
        title="Allergies and Intolerances",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Allergies and Intolerances Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID (base): 2.16.840.1.113883.10.20.22.2.6")
    print("  - Template ID (entries required): 2.16.840.1.113883.10.20.22.2.6.1")
    print("  - Extension: 2015-08-01")
    print("  - Number of allergies: 3")
    print("\nAllergies:")
    print("  1. Penicillin (RxNorm: 70618)")
    print("     - Reaction: Anaphylaxis")
    print("     - Severity: Severe")
    print("     - Criticality: High")
    print("     - Onset: 2015-03-10")
    print("  2. Peanuts (SNOMED CT: 762952008)")
    print("     - Reaction: Hives")
    print("     - Severity: Moderate")
    print("     - Criticality: High")
    print("     - Onset: 2010-08-22")
    print("  3. Latex (SNOMED CT: 111088007)")
    print("     - Reaction: Contact dermatitis")
    print("     - Severity: Mild")
    print("     - Criticality: Low")
    print("     - Onset: 2018-11-05")
    print("\nConformance:")
    print("  - CONF:1198-7524: Template ID present (entries required)")
    print("  - CONF:1198-7425: Code 48765-2 (Allergies and adverse reactions Document)")
    print("  - CONF:1198-7427: Title present")
    print("  - CONF:1198-7428: Narrative text with table present")
    print("  - CONF:1198-7429: Allergy Concern Act entries present")


if __name__ == "__main__":
    main()
