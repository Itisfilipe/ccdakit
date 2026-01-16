"""Example of creating a Results Section with lab results."""

from datetime import datetime

from lxml import etree

from ccdakit.builders.sections.results import ResultsSection
from ccdakit.core.base import CDAVersion


# ============================================================================
# Step 1: Create mock data classes that satisfy the protocols
# ============================================================================


class LabResult:
    """Mock lab result observation that satisfies ResultObservationProtocol."""

    def __init__(
        self,
        test_name,
        test_code,
        value,
        unit=None,
        status="completed",
        effective_time=None,
        value_type=None,
        interpretation=None,
        reference_range_low=None,
        reference_range_high=None,
        reference_range_unit=None,
    ):
        self._test_name = test_name
        self._test_code = test_code
        self._value = value
        self._unit = unit
        self._status = status
        self._effective_time = effective_time or datetime.now()
        self._value_type = value_type
        self._interpretation = interpretation
        self._reference_range_low = reference_range_low
        self._reference_range_high = reference_range_high
        self._reference_range_unit = reference_range_unit

    @property
    def test_name(self):
        return self._test_name

    @property
    def test_code(self):
        return self._test_code

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def value_type(self):
        return self._value_type

    @property
    def interpretation(self):
        return self._interpretation

    @property
    def reference_range_low(self):
        return self._reference_range_low

    @property
    def reference_range_high(self):
        return self._reference_range_high

    @property
    def reference_range_unit(self):
        return self._reference_range_unit


class LabPanel:
    """Mock lab panel organizer that satisfies ResultOrganizerProtocol."""

    def __init__(self, panel_name, panel_code, status, effective_time, results):
        self._panel_name = panel_name
        self._panel_code = panel_code
        self._status = status
        self._effective_time = effective_time
        self._results = results

    @property
    def panel_name(self):
        return self._panel_name

    @property
    def panel_code(self):
        return self._panel_code

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def results(self):
        return self._results


# ============================================================================
# Step 2: Create sample lab result data
# ============================================================================


def create_complete_blood_count():
    """Create a Complete Blood Count (CBC) panel with results."""

    test_date = datetime(2023, 10, 15, 10, 30)

    results = [
        LabResult(
            test_name="Hemoglobin",
            test_code="718-7",  # LOINC code
            value="14.5",
            unit="g/dL",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="12.0",
            reference_range_high="16.0",
            reference_range_unit="g/dL",
        ),
        LabResult(
            test_name="Hematocrit",
            test_code="4544-3",  # LOINC code
            value="42.5",
            unit="%",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="36.0",
            reference_range_high="48.0",
            reference_range_unit="%",
        ),
        LabResult(
            test_name="White Blood Cells",
            test_code="6690-2",  # LOINC code
            value="7.2",
            unit="10*3/uL",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="4.5",
            reference_range_high="11.0",
            reference_range_unit="10*3/uL",
        ),
        LabResult(
            test_name="Platelets",
            test_code="777-3",  # LOINC code
            value="250",
            unit="10*3/uL",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="150",
            reference_range_high="400",
            reference_range_unit="10*3/uL",
        ),
        LabResult(
            test_name="Red Blood Cells",
            test_code="789-8",  # LOINC code
            value="4.8",
            unit="10*6/uL",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="4.2",
            reference_range_high="5.9",
            reference_range_unit="10*6/uL",
        ),
    ]

    return LabPanel(
        panel_name="Complete Blood Count",
        panel_code="58410-2",  # LOINC code for CBC panel
        status="completed",
        effective_time=test_date,
        results=results,
    )


def create_basic_metabolic_panel():
    """Create a Basic Metabolic Panel (BMP) with results."""

    test_date = datetime(2023, 10, 15, 10, 30)

    results = [
        LabResult(
            test_name="Glucose",
            test_code="2345-7",  # LOINC code
            value="105",
            unit="mg/dL",
            status="completed",
            effective_time=test_date,
            interpretation="High",
            reference_range_low="70",
            reference_range_high="100",
            reference_range_unit="mg/dL",
        ),
        LabResult(
            test_name="Sodium",
            test_code="2951-2",  # LOINC code
            value="140",
            unit="mmol/L",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="136",
            reference_range_high="145",
            reference_range_unit="mmol/L",
        ),
        LabResult(
            test_name="Potassium",
            test_code="2823-3",  # LOINC code
            value="4.2",
            unit="mmol/L",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="3.5",
            reference_range_high="5.0",
            reference_range_unit="mmol/L",
        ),
        LabResult(
            test_name="Chloride",
            test_code="2075-0",  # LOINC code
            value="102",
            unit="mmol/L",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="98",
            reference_range_high="107",
            reference_range_unit="mmol/L",
        ),
        LabResult(
            test_name="Carbon Dioxide",
            test_code="2028-9",  # LOINC code
            value="25",
            unit="mmol/L",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="23",
            reference_range_high="29",
            reference_range_unit="mmol/L",
        ),
        LabResult(
            test_name="Blood Urea Nitrogen",
            test_code="3094-0",  # LOINC code
            value="18",
            unit="mg/dL",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="7",
            reference_range_high="20",
            reference_range_unit="mg/dL",
        ),
        LabResult(
            test_name="Creatinine",
            test_code="2160-0",  # LOINC code
            value="1.0",
            unit="mg/dL",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="0.7",
            reference_range_high="1.3",
            reference_range_unit="mg/dL",
        ),
        LabResult(
            test_name="Calcium",
            test_code="17861-6",  # LOINC code
            value="9.5",
            unit="mg/dL",
            status="completed",
            effective_time=test_date,
            interpretation="Normal",
            reference_range_low="8.5",
            reference_range_high="10.5",
            reference_range_unit="mg/dL",
        ),
    ]

    return LabPanel(
        panel_name="Basic Metabolic Panel",
        panel_code="51990-0",  # LOINC code for BMP
        status="completed",
        effective_time=test_date,
        results=results,
    )


# ============================================================================
# Step 3: Build the section and display output
# ============================================================================


def main():
    """Create and display a Results Section example."""

    print("\n" + "=" * 80)
    print("Results Section Example - Lab Results")
    print("=" * 80)

    # Create lab panels with results
    cbc_panel = create_complete_blood_count()
    bmp_panel = create_basic_metabolic_panel()

    print(f"\nPanel 1: {cbc_panel.panel_name}")
    print(f"  - Tests: {len(cbc_panel.results)}")
    print(f"  - Date: {cbc_panel.effective_time.strftime('%Y-%m-%d %H:%M')}")

    print(f"\nPanel 2: {bmp_panel.panel_name}")
    print(f"  - Tests: {len(bmp_panel.results)}")
    print(f"  - Date: {bmp_panel.effective_time.strftime('%Y-%m-%d %H:%M')}")

    # Create the Results Section with both panels
    section = ResultsSection(
        result_organizers=[cbc_panel, bmp_panel],
        title="Laboratory Results",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode")

    print("\n" + "=" * 80)
    print("Generated C-CDA Results Section (R2.1):")
    print("=" * 80)
    print(xml_string)

    # Show summary information
    print("\n" + "=" * 80)
    print("Summary:")
    print("=" * 80)
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.3.1")
    print("  - Extension: 2015-08-01")
    print("  - Section Code: 30954-2 (LOINC)")
    print(f"  - Section Title: {section.title}")
    print("  - Number of Organizers (Panels): 2")
    print(f"  - Total Tests: {len(cbc_panel.results) + len(bmp_panel.results)}")

    print("\nPanel Details:")
    print(f"  1. {cbc_panel.panel_name} ({cbc_panel.panel_code})")
    for i, result in enumerate(cbc_panel.results, 1):
        interp = result.interpretation or "N/A"
        print(f"     {i}. {result.test_name}: {result.value} {result.unit} [{interp}]")

    print(f"\n  2. {bmp_panel.panel_name} ({bmp_panel.panel_code})")
    for i, result in enumerate(bmp_panel.results, 1):
        interp = result.interpretation or "N/A"
        print(f"     {i}. {result.test_name}: {result.value} {result.unit} [{interp}]")

    print("\nKey Conformance Requirements (C-CDA R2.1):")
    print("  - CONF:1198-7109: SHALL contain templateId 2.16.840.1.113883.10.20.22.2.3.1")
    print("  - CONF:1198-7111: SHALL contain code 30954-2 (LOINC)")
    print("  - CONF:1198-7112: SHALL contain title")
    print("  - CONF:1198-7113: SHALL contain text (narrative)")
    print("  - CONF:1198-7114: SHALL contain at least one entry (Result Organizer)")
    print("  - CONF:1198-14823: Result Organizer SHALL contain component observations")

    print("\nFeatures Demonstrated:")
    print("  - Multiple result organizers (lab panels)")
    print("  - Multiple observations per organizer")
    print("  - LOINC codes for tests and panels")
    print("  - Physical quantity values with units")
    print("  - Interpretation codes (Normal, High, Low)")
    print("  - Reference ranges (low/high values)")
    print("  - Narrative HTML table with all results")
    print("  - Proper C-CDA R2.1 structure and templates")

    print("\nValidation:")
    print("  - This section can be validated using:")
    print("    * ONC C-CDA Validator (https://site.healthit.gov/sandbox-ccda/ccda-validator)")
    print("    * NIST validation tools")
    print("    * ccdakit's built-in Schematron validator")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
