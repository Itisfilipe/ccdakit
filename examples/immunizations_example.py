"""Example of creating an Immunizations Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.core.base import CDAVersion


# Define immunization data class
class ExampleImmunization:
    """Example immunization for demonstration."""

    def __init__(
        self,
        vaccine_name,
        cvx_code,
        administration_date,
        status="completed",
        lot_number=None,
        manufacturer=None,
        route=None,
        site=None,
        dose_quantity=None,
    ):
        self._vaccine_name = vaccine_name
        self._cvx_code = cvx_code
        self._administration_date = administration_date
        self._status = status
        self._lot_number = lot_number
        self._manufacturer = manufacturer
        self._route = route
        self._site = site
        self._dose_quantity = dose_quantity

    @property
    def vaccine_name(self):
        return self._vaccine_name

    @property
    def cvx_code(self):
        return self._cvx_code

    @property
    def administration_date(self):
        return self._administration_date

    @property
    def status(self):
        return self._status

    @property
    def lot_number(self):
        return self._lot_number

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def route(self):
        return self._route

    @property
    def site(self):
        return self._site

    @property
    def dose_quantity(self):
        return self._dose_quantity


def main():
    """Create and display an Immunizations Section example."""

    # Create sample immunizations
    influenza = ExampleImmunization(
        vaccine_name="Influenza vaccine, seasonal, injectable",
        cvx_code="141",  # CVX code for seasonal influenza vaccine
        administration_date=date(2023, 9, 15),
        status="completed",
        lot_number="FLU2023-ABC123",
        manufacturer="Sanofi Pasteur Inc.",
        route="Intramuscular",
        site="Left deltoid",
        dose_quantity="0.5 mL",
    )

    covid19 = ExampleImmunization(
        vaccine_name="COVID-19, mRNA, LNP-S, PF, 30 mcg/0.3 mL dose",
        cvx_code="208",  # CVX code for Pfizer-BioNTech COVID-19 vaccine
        administration_date=date(2023, 6, 1),
        status="completed",
        lot_number="CV19-XYZ789",
        manufacturer="Pfizer Inc.",
        route="Intramuscular",
        site="Left deltoid",
        dose_quantity="0.3 mL",
    )

    tetanus = ExampleImmunization(
        vaccine_name="Tetanus and diphtheria toxoids - preservative free",
        cvx_code="139",  # CVX code for Td vaccine
        administration_date=date(2022, 3, 10),
        status="completed",
        lot_number="TD2022-456DEF",
        manufacturer="Mass Biologics",
        route="Intramuscular",
        site="Right deltoid",
        dose_quantity="0.5 mL",
    )

    # Create the Immunizations Section
    section = ImmunizationsSection(
        immunizations=[influenza, covid19, tetanus],
        title="Immunization History",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Immunizations Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.2.1")
    print("  - Extension: 2015-08-01")
    print("  - Section Code: 11369-6 (History of Immunization Narrative)")
    print("  - Number of immunizations: 3")
    print("\nImmunizations:")
    print(f"  1. {influenza.vaccine_name}")
    print(f"     - CVX Code: {influenza.cvx_code}")
    print(f"     - Date: {influenza.administration_date}")
    print(f"     - Lot: {influenza.lot_number}")
    print(f"     - Manufacturer: {influenza.manufacturer}")
    print(f"  2. {covid19.vaccine_name}")
    print(f"     - CVX Code: {covid19.cvx_code}")
    print(f"     - Date: {covid19.administration_date}")
    print(f"     - Lot: {covid19.lot_number}")
    print(f"     - Manufacturer: {covid19.manufacturer}")
    print(f"  3. {tetanus.vaccine_name}")
    print(f"     - CVX Code: {tetanus.cvx_code}")
    print(f"     - Date: {tetanus.administration_date}")
    print(f"     - Lot: {tetanus.lot_number}")
    print(f"     - Manufacturer: {tetanus.manufacturer}")
    print("\nConformance:")
    print("  - Template IDs for both entries required and optional versions")
    print("  - Code 11369-6 from LOINC (History of Immunization Narrative)")
    print("  - Title element present")
    print("  - Narrative text with HTML table")
    print("  - Immunization Activity entries with CVX codes")
    print("  - Administration dates, lot numbers, and manufacturers included")


if __name__ == "__main__":
    main()
