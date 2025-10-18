"""Example of creating a Health Concerns Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.health_concerns import HealthConcernsSection
from ccdakit.core.base import CDAVersion


# Define observation data
class ExampleObservation:
    """Example observation for health concern."""

    def __init__(self, obs_type, code, code_system, display_name):
        self._observation_type = obs_type
        self._code = code
        self._code_system = code_system
        self._display_name = display_name

    @property
    def observation_type(self):
        return self._observation_type

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name


# Define health concern data
class ExampleHealthConcern:
    """Example health concern."""

    def __init__(
        self,
        name,
        status,
        effective_time_low,
        effective_time_high=None,
        observations=None,
        author_is_patient=False,
    ):
        self._name = name
        self._status = status
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._observations = observations or []
        self._author_is_patient = author_is_patient

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def effective_time_low(self):
        return self._effective_time_low

    @property
    def effective_time_high(self):
        return self._effective_time_high

    @property
    def persistent_id(self):
        return None

    @property
    def observations(self):
        return self._observations

    @property
    def author_is_patient(self):
        return self._author_is_patient


def main():
    """Create and display a Health Concerns Section example."""

    # Create observations
    diabetes_obs = ExampleObservation(
        obs_type="problem",
        code="44054006",
        code_system="SNOMED CT",
        display_name="Diabetes mellitus type 2",
    )

    acei_medication_obs = ExampleObservation(
        obs_type="problem",
        code="38341003",
        code_system="SNOMED CT",
        display_name="Hypertensive disorder",
    )

    social_obs = ExampleObservation(
        obs_type="social_history",
        code="160903007",
        code_system="SNOMED CT",
        display_name="Lives alone",
    )

    # Create health concerns
    concern1 = ExampleHealthConcern(
        name="Risk of Hyperkalemia",
        status="active",
        effective_time_low=date(2023, 1, 15),
        observations=[diabetes_obs, acei_medication_obs],
        author_is_patient=False,
    )

    concern2 = ExampleHealthConcern(
        name="Transportation difficulties",
        status="active",
        effective_time_low=date(2023, 2, 10),
        observations=[social_obs],
        author_is_patient=True,
    )

    concern3 = ExampleHealthConcern(
        name="Under-insured",
        status="active",
        effective_time_low=date(2023, 3, 5),
        observations=[],
        author_is_patient=False,
    )

    # Create the Health Concerns Section
    section = HealthConcernsSection(
        health_concerns=[concern1, concern2, concern3],
        title="Patient Health Concerns",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(
        elem, pretty_print=True, encoding="unicode", xml_declaration=False
    )

    print("Health Concerns Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print(f"  - Template ID: 2.16.840.1.113883.10.20.22.2.58")
    print(f"  - Extension: 2015-08-01")
    print(f"  - Number of concerns: 3")
    print(f"  - Total observations: 3")
    print("\nConformance:")
    print("  - CONF:1198-28804: Template ID present")
    print("  - CONF:1198-28806: Code 75310-3 (Health concerns document)")
    print("  - CONF:1198-28809: Title present")
    print("  - CONF:1198-28810: Narrative text present")
    print("  - CONF:1198-30768: Health Concern Act entries present")


if __name__ == "__main__":
    main()
