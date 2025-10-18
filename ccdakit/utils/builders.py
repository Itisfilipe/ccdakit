"""Simplified fluent API builders for C-CDA data models.

This module provides builder classes with fluent APIs for creating
patient data and clinical data that satisfy the protocol requirements.
These builders simplify data creation and reduce boilerplate code.

Example:
    >>> patient = (
    ...     SimplePatientBuilder()
    ...     .name("John", "Doe", "Q")
    ...     .birth_date(date(1970, 5, 15))
    ...     .gender("M")
    ...     .address("123 Main St", "Boston", "MA", "02101")
    ...     .phone("617-555-1234", "home")
    ...     .build()
    ... )
"""

from datetime import date, datetime
from typing import Any, Dict, Optional, Union


class SimplePatientBuilder:
    """Fluent API for building patient data that satisfies PatientProtocol.

    This builder creates dictionary-based patient data with a fluent interface.
    The resulting dictionary can be converted to a class instance that satisfies
    the PatientProtocol.

    Example:
        >>> patient = (
        ...     SimplePatientBuilder()
        ...     .name("John", "Doe", "Q")
        ...     .birth_date(date(1970, 5, 15))
        ...     .gender("M")
        ...     .race("2106-3")  # White (CDC Race Code)
        ...     .ethnicity("2186-5")  # Not Hispanic or Latino
        ...     .language("eng")
        ...     .ssn("123-45-6789")
        ...     .marital_status("M")  # Married
        ...     .address("123 Main St", "Boston", "MA", "02101")
        ...     .phone("617-555-1234", "home")
        ...     .email("john.doe@example.com", "home")
        ...     .build()
        ... )
    """

    def __init__(self) -> None:
        """Initialize the patient builder."""
        self._data: Dict[str, Any] = {
            "addresses": [],
            "telecoms": [],
        }

    def name(self, first: str, last: str, middle: Optional[str] = None) -> "SimplePatientBuilder":
        """Set patient name.

        Args:
            first: First name
            last: Last name
            middle: Middle name or initial (optional)

        Returns:
            Self for method chaining
        """
        self._data["first_name"] = first
        self._data["last_name"] = last
        if middle is not None:
            self._data["middle_name"] = middle
        return self

    def birth_date(self, birth_date: date) -> "SimplePatientBuilder":
        """Set date of birth.

        Args:
            birth_date: Patient's date of birth

        Returns:
            Self for method chaining
        """
        self._data["date_of_birth"] = birth_date
        return self

    def gender(self, sex: str) -> "SimplePatientBuilder":
        """Set administrative sex.

        Args:
            sex: Administrative sex code ('M', 'F', or 'UN')

        Returns:
            Self for method chaining
        """
        self._data["sex"] = sex
        return self

    def race(self, race_code: str) -> "SimplePatientBuilder":
        """Set race code.

        Args:
            race_code: CDC Race and Ethnicity code (e.g., '2106-3' for White)

        Returns:
            Self for method chaining
        """
        self._data["race"] = race_code
        return self

    def ethnicity(self, ethnicity_code: str) -> "SimplePatientBuilder":
        """Set ethnicity code.

        Args:
            ethnicity_code: CDC Race and Ethnicity code (e.g., '2186-5' for Not Hispanic or Latino)

        Returns:
            Self for method chaining
        """
        self._data["ethnicity"] = ethnicity_code
        return self

    def language(self, language_code: str) -> "SimplePatientBuilder":
        """Set preferred language.

        Args:
            language_code: ISO 639-2 language code (e.g., 'eng' for English)

        Returns:
            Self for method chaining
        """
        self._data["language"] = language_code
        return self

    def ssn(self, ssn: str) -> "SimplePatientBuilder":
        """Set Social Security Number or national ID.

        Args:
            ssn: Social Security Number or national ID

        Returns:
            Self for method chaining
        """
        self._data["ssn"] = ssn
        return self

    def marital_status(self, status: str) -> "SimplePatientBuilder":
        """Set marital status.

        Args:
            status: HL7 MaritalStatus code (e.g., 'M' for Married, 'S' for Single)

        Returns:
            Self for method chaining
        """
        self._data["marital_status"] = status
        return self

    def address(
        self,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        country: str = "US",
        street2: Optional[str] = None,
    ) -> "SimplePatientBuilder":
        """Add an address.

        Args:
            street: Street address line 1
            city: City name
            state: State/province code (e.g., 'MA', 'CA')
            zip_code: ZIP/postal code
            country: Country code (ISO 3166-1 alpha-2, default: 'US')
            street2: Street address line 2 (optional)

        Returns:
            Self for method chaining
        """
        street_lines = [street]
        if street2:
            street_lines.append(street2)

        address_data = {
            "street_lines": street_lines,
            "city": city,
            "state": state,
            "postal_code": zip_code,
            "country": country,
        }
        self._data["addresses"].append(address_data)
        return self

    def phone(self, number: str, use: str = "home") -> "SimplePatientBuilder":
        """Add a phone number.

        Args:
            number: Phone number
            use: Use code ('home', 'work', 'mobile')

        Returns:
            Self for method chaining
        """
        telecom_data = {"type": "phone", "value": number, "use": use}
        self._data["telecoms"].append(telecom_data)
        return self

    def email(self, email: str, use: str = "home") -> "SimplePatientBuilder":
        """Add an email address.

        Args:
            email: Email address
            use: Use code ('home', 'work')

        Returns:
            Self for method chaining
        """
        telecom_data = {"type": "email", "value": email, "use": use}
        self._data["telecoms"].append(telecom_data)
        return self

    def build(self) -> Dict[str, Any]:
        """Build patient data dictionary.

        Returns:
            Dictionary containing all patient data
        """
        return self._data.copy()


class SimpleProblemBuilder:
    """Fluent API for building problem/condition data that satisfies ProblemProtocol.

    Example:
        >>> problem = (
        ...     SimpleProblemBuilder()
        ...     .name("Essential Hypertension")
        ...     .code("59621000", "SNOMED")
        ...     .status("active")
        ...     .onset_date(date(2018, 5, 10))
        ...     .build()
        ... )
    """

    def __init__(self) -> None:
        """Initialize the problem builder."""
        self._data: Dict[str, Any] = {}

    def name(self, problem_name: str) -> "SimpleProblemBuilder":
        """Set problem name.

        Args:
            problem_name: Human-readable problem name

        Returns:
            Self for method chaining
        """
        self._data["name"] = problem_name
        return self

    def code(self, code: str, code_system: str) -> "SimpleProblemBuilder":
        """Set problem code and code system.

        Args:
            code: Problem code (SNOMED CT or ICD-10)
            code_system: Code system name ('SNOMED' or 'ICD-10')

        Returns:
            Self for method chaining
        """
        self._data["code"] = code
        self._data["code_system"] = code_system
        return self

    def status(self, status: str) -> "SimpleProblemBuilder":
        """Set problem status.

        Args:
            status: Status ('active', 'inactive', 'resolved')

        Returns:
            Self for method chaining
        """
        self._data["status"] = status
        return self

    def onset_date(self, onset: date) -> "SimpleProblemBuilder":
        """Set onset date.

        Args:
            onset: Date problem was identified/started

        Returns:
            Self for method chaining
        """
        self._data["onset_date"] = onset
        return self

    def resolved_date(self, resolved: date) -> "SimpleProblemBuilder":
        """Set resolved date.

        Args:
            resolved: Date problem was resolved

        Returns:
            Self for method chaining
        """
        self._data["resolved_date"] = resolved
        return self

    def persistent_id(self, root: str, extension: str) -> "SimpleProblemBuilder":
        """Set persistent identifier.

        Args:
            root: OID or UUID identifying the assigning authority
            extension: Unique identifier within the root's namespace

        Returns:
            Self for method chaining
        """
        self._data["persistent_id"] = {"root": root, "extension": extension}
        return self

    def build(self) -> Dict[str, Any]:
        """Build problem data dictionary.

        Returns:
            Dictionary containing all problem data
        """
        return self._data.copy()


class SimpleMedicationBuilder:
    """Fluent API for building medication data that satisfies MedicationProtocol.

    Example:
        >>> medication = (
        ...     SimpleMedicationBuilder()
        ...     .name("Lisinopril 10mg oral tablet")
        ...     .code("314076")  # RxNorm code
        ...     .dosage("10 mg")
        ...     .route("oral")
        ...     .frequency("once daily")
        ...     .start_date(date(2018, 6, 1))
        ...     .status("active")
        ...     .instructions("Take in the morning")
        ...     .build()
        ... )
    """

    def __init__(self) -> None:
        """Initialize the medication builder."""
        self._data: Dict[str, Any] = {}

    def name(self, medication_name: str) -> "SimpleMedicationBuilder":
        """Set medication name.

        Args:
            medication_name: Human-readable medication name

        Returns:
            Self for method chaining
        """
        self._data["name"] = medication_name
        return self

    def code(self, rxnorm_code: str) -> "SimpleMedicationBuilder":
        """Set RxNorm code.

        Args:
            rxnorm_code: RxNorm code for the medication

        Returns:
            Self for method chaining
        """
        self._data["code"] = rxnorm_code
        return self

    def dosage(self, dosage_amount: str) -> "SimpleMedicationBuilder":
        """Set dosage.

        Args:
            dosage_amount: Dosage amount (e.g., "10 mg", "1 tablet")

        Returns:
            Self for method chaining
        """
        self._data["dosage"] = dosage_amount
        return self

    def route(self, route_of_admin: str) -> "SimpleMedicationBuilder":
        """Set route of administration.

        Args:
            route_of_admin: Route (e.g., "oral", "IV", "topical")

        Returns:
            Self for method chaining
        """
        self._data["route"] = route_of_admin
        return self

    def frequency(self, freq: str) -> "SimpleMedicationBuilder":
        """Set frequency of administration.

        Args:
            freq: Frequency (e.g., "twice daily", "every 6 hours")

        Returns:
            Self for method chaining
        """
        self._data["frequency"] = freq
        return self

    def start_date(self, start: date) -> "SimpleMedicationBuilder":
        """Set start date.

        Args:
            start: Date medication was started

        Returns:
            Self for method chaining
        """
        self._data["start_date"] = start
        return self

    def end_date(self, end: date) -> "SimpleMedicationBuilder":
        """Set end date.

        Args:
            end: Date medication was stopped

        Returns:
            Self for method chaining
        """
        self._data["end_date"] = end
        return self

    def status(self, status: str) -> "SimpleMedicationBuilder":
        """Set medication status.

        Args:
            status: Status ('active', 'completed', 'discontinued')

        Returns:
            Self for method chaining
        """
        self._data["status"] = status
        return self

    def instructions(self, patient_instructions: str) -> "SimpleMedicationBuilder":
        """Set patient instructions.

        Args:
            patient_instructions: Instructions for patient

        Returns:
            Self for method chaining
        """
        self._data["instructions"] = patient_instructions
        return self

    def build(self) -> Dict[str, Any]:
        """Build medication data dictionary.

        Returns:
            Dictionary containing all medication data
        """
        return self._data.copy()


class SimpleAllergyBuilder:
    """Fluent API for building allergy/intolerance data that satisfies AllergyProtocol.

    Example:
        >>> allergy = (
        ...     SimpleAllergyBuilder()
        ...     .allergen("Penicillin")
        ...     .allergen_code("7980", "RxNorm")
        ...     .allergy_type("allergy")
        ...     .reaction("Hives")
        ...     .severity("moderate")
        ...     .status("active")
        ...     .onset_date(date(2010, 3, 15))
        ...     .build()
        ... )
    """

    def __init__(self) -> None:
        """Initialize the allergy builder."""
        self._data: Dict[str, Any] = {}

    def allergen(self, allergen_name: str) -> "SimpleAllergyBuilder":
        """Set allergen name.

        Args:
            allergen_name: Human-readable allergen name

        Returns:
            Self for method chaining
        """
        self._data["allergen"] = allergen_name
        return self

    def allergen_code(self, code: str, code_system: str) -> "SimpleAllergyBuilder":
        """Set allergen code.

        Args:
            code: Allergen code
            code_system: Code system ('RxNorm', 'UNII', or 'SNOMED')

        Returns:
            Self for method chaining
        """
        self._data["allergen_code"] = code
        self._data["allergen_code_system"] = code_system
        return self

    def allergy_type(self, allergy_type: str) -> "SimpleAllergyBuilder":
        """Set allergy type.

        Args:
            allergy_type: Type ('allergy' or 'intolerance')

        Returns:
            Self for method chaining
        """
        self._data["allergy_type"] = allergy_type
        return self

    def reaction(self, reaction_desc: str) -> "SimpleAllergyBuilder":
        """Set reaction/manifestation.

        Args:
            reaction_desc: Reaction description (e.g., "Hives", "Anaphylaxis")

        Returns:
            Self for method chaining
        """
        self._data["reaction"] = reaction_desc
        return self

    def severity(self, severity_level: str) -> "SimpleAllergyBuilder":
        """Set severity.

        Args:
            severity_level: Severity ('mild', 'moderate', 'severe', or 'fatal')

        Returns:
            Self for method chaining
        """
        self._data["severity"] = severity_level
        return self

    def status(self, status: str) -> "SimpleAllergyBuilder":
        """Set allergy status.

        Args:
            status: Status ('active' or 'resolved')

        Returns:
            Self for method chaining
        """
        self._data["status"] = status
        return self

    def onset_date(self, onset: date) -> "SimpleAllergyBuilder":
        """Set onset date.

        Args:
            onset: Date when allergy was first identified

        Returns:
            Self for method chaining
        """
        self._data["onset_date"] = onset
        return self

    def build(self) -> Dict[str, Any]:
        """Build allergy data dictionary.

        Returns:
            Dictionary containing all allergy data
        """
        return self._data.copy()


class SimpleImmunizationBuilder:
    """Fluent API for building immunization data that satisfies ImmunizationProtocol.

    Example:
        >>> immunization = (
        ...     SimpleImmunizationBuilder()
        ...     .vaccine("Influenza vaccine, seasonal", "141")
        ...     .administration_date(date(2023, 9, 15))
        ...     .status("completed")
        ...     .lot_number("ABC123456")
        ...     .manufacturer("Sanofi Pasteur")
        ...     .route("intramuscular")
        ...     .site("left deltoid")
        ...     .dose_quantity("0.5 mL")
        ...     .build()
        ... )
    """

    def __init__(self) -> None:
        """Initialize the immunization builder."""
        self._data: Dict[str, Any] = {}

    def vaccine(self, vaccine_name: str, cvx_code: str) -> "SimpleImmunizationBuilder":
        """Set vaccine name and CVX code.

        Args:
            vaccine_name: Name of the vaccine
            cvx_code: CVX code (CDC vaccine code system)

        Returns:
            Self for method chaining
        """
        self._data["vaccine_name"] = vaccine_name
        self._data["cvx_code"] = cvx_code
        return self

    def administration_date(self, admin_date: Union[date, datetime]) -> "SimpleImmunizationBuilder":
        """Set administration date.

        Args:
            admin_date: Date vaccine was administered

        Returns:
            Self for method chaining
        """
        self._data["administration_date"] = admin_date
        return self

    def status(self, status: str) -> "SimpleImmunizationBuilder":
        """Set immunization status.

        Args:
            status: Status (e.g., "completed", "refused")

        Returns:
            Self for method chaining
        """
        self._data["status"] = status
        return self

    def lot_number(self, lot: str) -> "SimpleImmunizationBuilder":
        """Set vaccine lot number.

        Args:
            lot: Vaccine lot number

        Returns:
            Self for method chaining
        """
        self._data["lot_number"] = lot
        return self

    def manufacturer(self, mfr: str) -> "SimpleImmunizationBuilder":
        """Set vaccine manufacturer.

        Args:
            mfr: Manufacturer name

        Returns:
            Self for method chaining
        """
        self._data["manufacturer"] = mfr
        return self

    def route(self, route_of_admin: str) -> "SimpleImmunizationBuilder":
        """Set route of administration.

        Args:
            route_of_admin: Route (e.g., "intramuscular", "oral")

        Returns:
            Self for method chaining
        """
        self._data["route"] = route_of_admin
        return self

    def site(self, body_site: str) -> "SimpleImmunizationBuilder":
        """Set body site where vaccine was administered.

        Args:
            body_site: Body site (e.g., "left deltoid")

        Returns:
            Self for method chaining
        """
        self._data["site"] = body_site
        return self

    def dose_quantity(self, dose: str) -> "SimpleImmunizationBuilder":
        """Set dose quantity.

        Args:
            dose: Dose quantity and unit (e.g., "0.5 mL")

        Returns:
            Self for method chaining
        """
        self._data["dose_quantity"] = dose
        return self

    def build(self) -> Dict[str, Any]:
        """Build immunization data dictionary.

        Returns:
            Dictionary containing all immunization data
        """
        return self._data.copy()


# Due to length, I'll create a separate file part for the remaining builders


class SimpleVitalSignBuilder:
    """Fluent API for building vital sign observation data that satisfies VitalSignProtocol."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def observation(self, type_name: str, loinc_code: str) -> "SimpleVitalSignBuilder":
        self._data["type"] = type_name
        self._data["code"] = loinc_code
        return self

    def value(self, measurement: str, unit: str) -> "SimpleVitalSignBuilder":
        self._data["value"] = measurement
        self._data["unit"] = unit
        return self

    def date(self, observation_date: Union[date, datetime]) -> "SimpleVitalSignBuilder":
        self._data["date"] = observation_date
        return self

    def interpretation(self, interp: str) -> "SimpleVitalSignBuilder":
        self._data["interpretation"] = interp
        return self

    def build(self) -> Dict[str, Any]:
        return self._data.copy()


class SimpleVitalSignsOrganizerBuilder:
    """Fluent API for building vital signs organizer data."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {"vital_signs": []}

    def date(self, observation_date: Union[date, datetime]) -> "SimpleVitalSignsOrganizerBuilder":
        self._data["date"] = observation_date
        return self

    def add_vital_sign(self, vital_sign_data: Dict[str, Any]) -> "SimpleVitalSignsOrganizerBuilder":
        self._data["vital_signs"].append(vital_sign_data)
        return self

    def build(self) -> Dict[str, Any]:
        return self._data.copy()


class SimpleProcedureBuilder:
    """Fluent API for building procedure data."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def name(self, procedure_name: str) -> "SimpleProcedureBuilder":
        self._data["name"] = procedure_name
        return self

    def code(self, code: str, code_system: str) -> "SimpleProcedureBuilder":
        self._data["code"] = code
        self._data["code_system"] = code_system
        return self

    def date(self, procedure_date: Union[date, datetime]) -> "SimpleProcedureBuilder":
        self._data["date"] = procedure_date
        return self

    def status(self, status: str) -> "SimpleProcedureBuilder":
        self._data["status"] = status
        return self

    def target_site(
        self, site_name: str, site_code: Optional[str] = None
    ) -> "SimpleProcedureBuilder":
        self._data["target_site"] = site_name
        if site_code:
            self._data["target_site_code"] = site_code
        return self

    def performer(self, performer_name: str) -> "SimpleProcedureBuilder":
        self._data["performer_name"] = performer_name
        return self

    def build(self) -> Dict[str, Any]:
        return self._data.copy()


class SimpleResultObservationBuilder:
    """Fluent API for building result observation data."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def test(self, test_name: str, loinc_code: str) -> "SimpleResultObservationBuilder":
        self._data["test_name"] = test_name
        self._data["test_code"] = loinc_code
        return self

    def value(
        self, result_value: str, unit: Optional[str] = None
    ) -> "SimpleResultObservationBuilder":
        self._data["value"] = result_value
        if unit is not None:
            self._data["unit"] = unit
        return self

    def status(self, status: str) -> "SimpleResultObservationBuilder":
        self._data["status"] = status
        return self

    def effective_time(self, test_date: Union[date, datetime]) -> "SimpleResultObservationBuilder":
        self._data["effective_time"] = test_date
        return self

    def value_type(self, val_type: str) -> "SimpleResultObservationBuilder":
        self._data["value_type"] = val_type
        return self

    def interpretation(self, interp: str) -> "SimpleResultObservationBuilder":
        self._data["interpretation"] = interp
        return self

    def reference_range(self, low: str, high: str, unit: str) -> "SimpleResultObservationBuilder":
        self._data["reference_range_low"] = low
        self._data["reference_range_high"] = high
        self._data["reference_range_unit"] = unit
        return self

    def build(self) -> Dict[str, Any]:
        return self._data.copy()


class SimpleResultOrganizerBuilder:
    """Fluent API for building result organizer data."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {"results": []}

    def panel(self, panel_name: str, loinc_code: str) -> "SimpleResultOrganizerBuilder":
        self._data["panel_name"] = panel_name
        self._data["panel_code"] = loinc_code
        return self

    def status(self, status: str) -> "SimpleResultOrganizerBuilder":
        self._data["status"] = status
        return self

    def effective_time(self, panel_date: Union[date, datetime]) -> "SimpleResultOrganizerBuilder":
        self._data["effective_time"] = panel_date
        return self

    def add_result(self, result_data: Dict[str, Any]) -> "SimpleResultOrganizerBuilder":
        self._data["results"].append(result_data)
        return self

    def build(self) -> Dict[str, Any]:
        return self._data.copy()


class SimpleEncounterBuilder:
    """Fluent API for building encounter data."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def encounter_type(
        self, type_name: str, code: str, code_system: str
    ) -> "SimpleEncounterBuilder":
        self._data["encounter_type"] = type_name
        self._data["code"] = code
        self._data["code_system"] = code_system
        return self

    def date(self, encounter_date: Union[date, datetime]) -> "SimpleEncounterBuilder":
        self._data["date"] = encounter_date
        return self

    def end_date(self, encounter_end: Union[date, datetime]) -> "SimpleEncounterBuilder":
        self._data["end_date"] = encounter_end
        return self

    def location(self, location_name: str) -> "SimpleEncounterBuilder":
        self._data["location"] = location_name
        return self

    def performer(self, performer_name: str) -> "SimpleEncounterBuilder":
        self._data["performer_name"] = performer_name
        return self

    def discharge_disposition(self, disposition: str) -> "SimpleEncounterBuilder":
        self._data["discharge_disposition"] = disposition
        return self

    def build(self) -> Dict[str, Any]:
        return self._data.copy()


class SimpleSmokingStatusBuilder:
    """Fluent API for building smoking status data."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def status(self, status_desc: str, snomed_code: str) -> "SimpleSmokingStatusBuilder":
        self._data["smoking_status"] = status_desc
        self._data["code"] = snomed_code
        return self

    def date(self, observation_date: Union[date, datetime]) -> "SimpleSmokingStatusBuilder":
        self._data["date"] = observation_date
        return self

    def build(self) -> Dict[str, Any]:
        return self._data.copy()


# Convenience functions
def patient_builder() -> SimplePatientBuilder:
    return SimplePatientBuilder()


def problem_builder() -> SimpleProblemBuilder:
    return SimpleProblemBuilder()


def medication_builder() -> SimpleMedicationBuilder:
    return SimpleMedicationBuilder()


def allergy_builder() -> SimpleAllergyBuilder:
    return SimpleAllergyBuilder()


def immunization_builder() -> SimpleImmunizationBuilder:
    return SimpleImmunizationBuilder()


def vital_sign_builder() -> SimpleVitalSignBuilder:
    return SimpleVitalSignBuilder()


def vital_signs_organizer_builder() -> SimpleVitalSignsOrganizerBuilder:
    return SimpleVitalSignsOrganizerBuilder()


def procedure_builder() -> SimpleProcedureBuilder:
    return SimpleProcedureBuilder()


def result_observation_builder() -> SimpleResultObservationBuilder:
    return SimpleResultObservationBuilder()


def result_organizer_builder() -> SimpleResultOrganizerBuilder:
    return SimpleResultOrganizerBuilder()


def encounter_builder() -> SimpleEncounterBuilder:
    return SimpleEncounterBuilder()


def smoking_status_builder() -> SimpleSmokingStatusBuilder:
    return SimpleSmokingStatusBuilder()
