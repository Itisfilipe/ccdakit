"""Test data generators for C-CDA documents.

This module provides utilities to generate realistic test data for C-CDA
documents using the Faker library. The generators produce clinically realistic
data with proper medical codes (SNOMED, RxNorm, CVX, LOINC, etc.).

Example:
    generator = SampleDataGenerator(seed=42)  # Reproducible data
    patient = generator.generate_patient()
    problems = [generator.generate_problem() for _ in range(3)]
    full_record = generator.generate_complete_patient_record()
"""

import random  # noqa: S311  # Not used for cryptographic purposes
from typing import Any, Optional


try:
    from faker import Faker
except ImportError as e:
    raise ImportError(
        "The 'faker' library is required for test data generation. "
        "Install it with: pip install 'ccdakit[test-data]' or 'pip install faker>=20.0.0'"
    ) from e


class SampleDataGenerator:
    """Generate realistic sample data for C-CDA documents.

    This class provides methods to generate various types of clinical data
    including patient demographics, problems, medications, allergies, vital signs,
    and immunizations. All generated data includes appropriate medical terminology
    codes (SNOMED CT, RxNorm, CVX, LOINC, etc.).

    Attributes:
        faker: Faker instance for generating realistic data
        seed: Random seed for reproducibility (optional)

    Example:
        # Generate reproducible sample data
        gen = SampleDataGenerator(seed=42)
        patient = gen.generate_patient()
        print(f"Patient: {patient['first_name']} {patient['last_name']}")

        # Generate a complete patient record
        record = gen.generate_complete_patient_record()
        print(f"Generated {len(record['problems'])} problems")
    """

    # Common clinical problems with SNOMED CT codes
    COMMON_PROBLEMS = [
        ("Essential Hypertension", "59621000", "SNOMED"),
        ("Type 2 Diabetes Mellitus", "44054006", "SNOMED"),
        ("Hyperlipidemia", "55822004", "SNOMED"),
        ("Gastroesophageal Reflux Disease", "235595009", "SNOMED"),
        ("Asthma", "195967001", "SNOMED"),
        ("Chronic Obstructive Pulmonary Disease", "13645005", "SNOMED"),
        ("Coronary Artery Disease", "53741008", "SNOMED"),
        ("Atrial Fibrillation", "49436004", "SNOMED"),
        ("Hypothyroidism", "40930008", "SNOMED"),
        ("Osteoarthritis", "396275006", "SNOMED"),
        ("Major Depressive Disorder", "370143000", "SNOMED"),
        ("Generalized Anxiety Disorder", "21897009", "SNOMED"),
        ("Chronic Kidney Disease", "709044004", "SNOMED"),
        ("Benign Prostatic Hyperplasia", "266569009", "SNOMED"),
        ("Sleep Apnea", "78275009", "SNOMED"),
        ("Migraine", "37796009", "SNOMED"),
        ("Obesity", "414915002", "SNOMED"),
        ("Anemia", "271737000", "SNOMED"),
        ("Osteoporosis", "64859006", "SNOMED"),
        ("Peripheral Neuropathy", "42658009", "SNOMED"),
    ]

    # Common medications with RxNorm codes
    COMMON_MEDICATIONS = [
        ("Lisinopril 10 MG Oral Tablet", "314076", "RxNorm", "10 mg", "oral", "once daily"),
        ("Metformin 500 MG Oral Tablet", "860975", "RxNorm", "500 mg", "oral", "twice daily"),
        ("Atorvastatin 20 MG Oral Tablet", "617318", "RxNorm", "20 mg", "oral", "once daily"),
        ("Amlodipine 5 MG Oral Tablet", "197361", "RxNorm", "5 mg", "oral", "once daily"),
        (
            "Omeprazole 20 MG Delayed Release Oral Capsule",
            "198014",
            "RxNorm",
            "20 mg",
            "oral",
            "once daily",
        ),
        (
            "Levothyroxine Sodium 0.1 MG Oral Tablet",
            "966224",
            "RxNorm",
            "0.1 mg",
            "oral",
            "once daily",
        ),
        (
            "Metoprolol Succinate 50 MG Extended Release Oral Tablet",
            "866436",
            "RxNorm",
            "50 mg",
            "oral",
            "once daily",
        ),
        ("Sertraline 50 MG Oral Tablet", "312940", "RxNorm", "50 mg", "oral", "once daily"),
        (
            "Albuterol 0.09 MG/ACTUAT Metered Dose Inhaler",
            "745752",
            "RxNorm",
            "2 puffs",
            "inhaled",
            "as needed",
        ),
        (
            "Gabapentin 300 MG Oral Capsule",
            "105029",
            "RxNorm",
            "300 mg",
            "oral",
            "three times daily",
        ),
        ("Warfarin Sodium 5 MG Oral Tablet", "855333", "RxNorm", "5 mg", "oral", "once daily"),
        ("Furosemide 40 MG Oral Tablet", "310429", "RxNorm", "40 mg", "oral", "once daily"),
        (
            "Aspirin 81 MG Delayed Release Oral Tablet",
            "243670",
            "RxNorm",
            "81 mg",
            "oral",
            "once daily",
        ),
        (
            "Insulin Glargine 100 UNT/ML Injectable Solution",
            "261551",
            "RxNorm",
            "20 units",
            "subcutaneous",
            "once daily at bedtime",
        ),
    ]

    # Common allergens with codes
    COMMON_ALLERGENS = [
        ("Penicillin", "7980", "RxNorm", "allergy", "Rash", "moderate"),
        ("Sulfonamides", "10180", "RxNorm", "allergy", "Hives", "mild"),
        ("Shellfish", "227037002", "SNOMED", "allergy", "Anaphylaxis", "severe"),
        ("Peanuts", "256349002", "SNOMED", "allergy", "Swelling", "moderate"),
        ("Latex", "111088007", "SNOMED", "allergy", "Contact dermatitis", "mild"),
        ("Bee venom", "288328004", "SNOMED", "allergy", "Anaphylaxis", "severe"),
        ("Eggs", "102263004", "SNOMED", "allergy", "Nausea", "mild"),
        ("Codeine", "2670", "RxNorm", "intolerance", "Nausea", "moderate"),
        ("Aspirin", "1191", "RxNorm", "intolerance", "Stomach upset", "mild"),
        ("Ibuprofen", "5640", "RxNorm", "intolerance", "Rash", "mild"),
    ]

    # Common vaccines with CVX codes
    COMMON_VACCINES = [
        ("Influenza vaccine", "141", "Seasonal flu vaccine", "Intramuscular", "Left deltoid"),
        ("Pneumococcal conjugate vaccine", "133", "Prevnar 13", "Intramuscular", "Left deltoid"),
        ("Tetanus and diphtheria toxoids", "139", "Td vaccine", "Intramuscular", "Right deltoid"),
        ("Zoster vaccine live", "121", "Shingles vaccine", "Subcutaneous", "Upper arm"),
        ("Hepatitis B vaccine", "08", "Hep B vaccine", "Intramuscular", "Left deltoid"),
        (
            "Measles, mumps and rubella virus vaccine",
            "03",
            "MMR vaccine",
            "Subcutaneous",
            "Upper arm",
        ),
        ("COVID-19 vaccine, mRNA", "208", "COVID-19 vaccine", "Intramuscular", "Left deltoid"),
        ("Hepatitis A vaccine", "83", "Hep A vaccine", "Intramuscular", "Right deltoid"),
    ]

    # Vital signs with LOINC codes
    VITAL_SIGNS_TYPES = [
        ("Blood Pressure Systolic", "8480-6", "mm[Hg]", 110, 140),
        ("Blood Pressure Diastolic", "8462-4", "mm[Hg]", 70, 90),
        ("Heart Rate", "8867-4", "bpm", 60, 100),
        ("Respiratory Rate", "9279-1", "breaths/min", 12, 20),
        ("Body Temperature", "8310-5", "Cel", 36.5, 37.2),
        ("Oxygen Saturation", "2708-6", "%", 95, 100),
        ("Body Height", "8302-2", "cm", 150, 190),
        ("Body Weight", "29463-7", "kg", 50, 100),
        ("Body Mass Index", "39156-5", "kg/m2", 18.5, 30),
    ]

    def __init__(self, seed: Optional[int] = None):
        """Initialize test data generator.

        Args:
            seed: Optional random seed for reproducible data generation.
                  If provided, all generated data will be deterministic.
        """
        self.seed = seed
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
        self.faker = Faker()

    def generate_address(self) -> "dict[str, Any]":
        """Generate a realistic address.

        Returns:
            Dictionary containing address fields compatible with AddressProtocol:
            - street_lines: List of street address lines
            - city: City name
            - state: State code (e.g., 'CA', 'NY')
            - postal_code: ZIP code
            - country: Country code (always 'US')
            - use: Address use code ('HP' for home, 'WP' for work)
        """
        return {
            "street_lines": [self.faker.street_address()],
            "city": self.faker.city(),
            "state": self.faker.state_abbr(),
            "postal_code": self.faker.zipcode(),
            "country": "US",
            "use": random.choice(["HP", "WP"]),  # Home or Work
        }

    def generate_telecom(self) -> "dict[str, Any]":
        """Generate a realistic telecom (contact method).

        Returns:
            Dictionary containing telecom fields compatible with TelecomProtocol:
            - type: Type of contact ('phone', 'email')
            - value: Contact value (phone number or email)
            - use: Use code ('HP', 'WP', 'MC')
        """
        contact_type = random.choice(["phone", "email"])
        if contact_type == "phone":
            return {
                "type": "phone",
                "value": f"tel:{self.faker.phone_number()}",
                "use": random.choice(["HP", "WP", "MC"]),  # Home, Work, Mobile
            }
        else:
            return {
                "type": "email",
                "value": f"mailto:{self.faker.email()}",
                "use": random.choice(["HP", "WP"]),
            }

    def generate_patient(self) -> "dict[str, Any]":
        """Generate realistic patient demographics.

        Returns:
            Dictionary containing patient demographic data compatible with PatientProtocol:
            - first_name: Patient's first name
            - last_name: Patient's last name
            - middle_name: Optional middle name
            - date_of_birth: Date of birth
            - sex: Administrative sex code ('M', 'F', or 'UN')
            - race: Optional race code (CDC Race and Ethnicity)
            - ethnicity: Optional ethnicity code
            - language: Optional language code (ISO 639-2)
            - ssn: Optional Social Security Number
            - addresses: List of addresses
            - telecoms: List of contact methods
            - marital_status: Optional marital status code
        """
        sex = random.choice(["M", "F"])
        min_age = 18
        max_age = 90

        # Generate age-appropriate first name
        if sex == "M":
            first_name = self.faker.first_name_male()
        else:
            first_name = self.faker.first_name_female()

        return {
            "first_name": first_name,
            "last_name": self.faker.last_name(),
            "middle_name": random.choice([self.faker.first_name()[:1], None]),
            "date_of_birth": self.faker.date_of_birth(minimum_age=min_age, maximum_age=max_age),
            "sex": sex,
            "race": random.choice(
                [
                    "2106-3",  # White
                    "2054-5",  # Black or African American
                    "2028-9",  # Asian
                    "1002-5",  # American Indian or Alaska Native
                    None,
                ]
            ),
            "ethnicity": random.choice(
                [
                    "2135-2",  # Hispanic or Latino
                    "2186-5",  # Not Hispanic or Latino
                    None,
                ]
            ),
            "language": random.choice(["en", "es", "fr", None]),
            "ssn": self.faker.ssn() if random.random() > 0.3 else None,
            "addresses": [self.generate_address()],
            "telecoms": [self.generate_telecom() for _ in range(random.randint(1, 3))],
            "marital_status": random.choice(
                ["M", "S", "D", "W", None]
            ),  # Married, Single, Divorced, Widowed
        }

    def generate_problem(self) -> "dict[str, Any]":
        """Generate a realistic clinical problem/condition.

        Returns:
            Dictionary containing problem data compatible with ProblemProtocol:
            - name: Human-readable problem name
            - code: Clinical code (SNOMED CT or ICD-10)
            - code_system: Code system name
            - status: Problem status ('active', 'inactive', or 'resolved')
            - onset_date: Date problem was identified
            - resolved_date: Optional date problem was resolved
            - persistent_id: None (can be added if needed)
        """
        problem = random.choice(self.COMMON_PROBLEMS)
        status = random.choice(
            ["active", "active", "active", "resolved"]
        )  # More likely to be active

        onset_date = self.faker.date_between(start_date="-5y", end_date="today")
        resolved_date = None
        if status == "resolved":
            resolved_date = self.faker.date_between(start_date=onset_date, end_date="today")

        return {
            "name": problem[0],
            "code": problem[1],
            "code_system": problem[2],
            "status": status,
            "onset_date": onset_date,
            "resolved_date": resolved_date,
            "persistent_id": None,
        }

    def generate_medication(self) -> "dict[str, Any]":
        """Generate a realistic medication.

        Returns:
            Dictionary containing medication data compatible with MedicationProtocol:
            - name: Medication name with strength and form
            - code: RxNorm code
            - dosage: Dosage amount
            - route: Route of administration
            - frequency: Frequency of administration
            - start_date: Date medication was started
            - end_date: Optional date medication was stopped
            - status: Medication status ('active', 'completed', or 'discontinued')
            - instructions: Optional patient instructions
        """
        med = random.choice(self.COMMON_MEDICATIONS)
        status = random.choice(["active", "active", "completed"])  # More likely to be active

        start_date = self.faker.date_between(start_date="-2y", end_date="today")
        end_date = None
        if status in ["completed", "discontinued"]:
            end_date = self.faker.date_between(start_date=start_date, end_date="today")

        return {
            "name": med[0],
            "code": med[1],
            "dosage": med[3],
            "route": med[4],
            "frequency": med[5],
            "start_date": start_date,
            "end_date": end_date,
            "status": status,
            "instructions": f"Take {med[3]} by {med[4]} route {med[5]}"
            if random.random() > 0.5
            else None,
        }

    def generate_allergy(self) -> "dict[str, Any]":
        """Generate a realistic allergy.

        Returns:
            Dictionary containing allergy data compatible with AllergyProtocol:
            - allergen: Allergen name
            - allergen_code: Code for the allergen
            - allergen_code_system: Code system (RxNorm or SNOMED)
            - allergy_type: Type ('allergy' or 'intolerance')
            - reaction: Optional reaction description
            - severity: Optional severity level
            - status: Status ('active' or 'resolved')
            - onset_date: Optional date allergy was identified
        """
        allergy = random.choice(self.COMMON_ALLERGENS)
        status = random.choice(
            ["active", "active", "active", "resolved"]
        )  # More likely to be active

        onset_date = None
        if random.random() > 0.3:
            onset_date = self.faker.date_between(start_date="-10y", end_date="today")

        return {
            "allergen": allergy[0],
            "allergen_code": allergy[1],
            "allergen_code_system": allergy[2],
            "allergy_type": allergy[3],
            "reaction": allergy[4],
            "severity": allergy[5],
            "status": status,
            "onset_date": onset_date,
        }

    def generate_vital_signs(self, count: Optional[int] = None) -> "dict[str, Any]":
        """Generate realistic vital signs readings.

        Args:
            count: Number of vital signs to generate. If None, generates 3-6 signs.

        Returns:
            Dictionary containing vital signs data compatible with VitalSignsOrganizerProtocol:
            - date: Date and time vital signs were taken
            - vital_signs: List of vital sign observations, each containing:
                - type: Type of vital sign
                - code: LOINC code
                - value: Measured value
                - unit: Unit of measurement
                - date: Same as organizer date
                - interpretation: Optional interpretation
        """
        if count is None:
            count = random.randint(3, 6)

        observation_date = self.faker.date_time_between(start_date="-1y", end_date="now")
        vital_signs_list = []

        # Select random vital signs
        selected_vitals = random.sample(
            self.VITAL_SIGNS_TYPES, min(count, len(self.VITAL_SIGNS_TYPES))
        )

        for vital in selected_vitals:
            name, loinc_code, unit, min_val, max_val = vital

            # Generate realistic value within range
            if unit in ["mm[Hg]", "bpm", "breaths/min", "cm", "kg"]:
                value = str(random.randint(int(min_val), int(max_val)))
            else:
                value = f"{random.uniform(min_val, max_val):.1f}"

            interpretation = None
            if random.random() > 0.7:
                interpretation = random.choice(["Normal", "High", "Low"])

            vital_signs_list.append(
                {
                    "type": name,
                    "code": loinc_code,
                    "value": value,
                    "unit": unit,
                    "date": observation_date,
                    "interpretation": interpretation,
                }
            )

        return {
            "date": observation_date,
            "vital_signs": vital_signs_list,
        }

    def generate_immunization(self) -> "dict[str, Any]":
        """Generate a realistic immunization record.

        Returns:
            Dictionary containing immunization data compatible with ImmunizationProtocol:
            - vaccine_name: Name of the vaccine
            - cvx_code: CVX code (CDC vaccine code)
            - administration_date: Date vaccine was administered
            - status: Status ('completed' or 'refused')
            - lot_number: Optional vaccine lot number
            - manufacturer: Optional manufacturer name
            - route: Route of administration
            - site: Body site where administered
            - dose_quantity: Optional dose quantity
        """
        vaccine = random.choice(self.COMMON_VACCINES)
        status = random.choice(
            ["completed", "completed", "completed", "refused"]
        )  # More likely completed

        admin_date = self.faker.date_between(start_date="-3y", end_date="today")

        lot_number = None
        manufacturer = None
        dose_quantity = None

        if status == "completed" and random.random() > 0.3:
            lot_number = self.faker.bothify(text="LOT###??##")
            manufacturer = random.choice(
                [
                    "Pfizer",
                    "Moderna",
                    "Merck",
                    "GlaxoSmithKline",
                    "Sanofi Pasteur",
                    "AstraZeneca",
                ]
            )
            dose_quantity = "0.5 mL" if random.random() > 0.5 else "1.0 mL"

        return {
            "vaccine_name": vaccine[0],
            "cvx_code": vaccine[1],
            "administration_date": admin_date,
            "status": status,
            "lot_number": lot_number,
            "manufacturer": manufacturer,
            "route": vaccine[3],
            "site": vaccine[4],
            "dose_quantity": dose_quantity,
        }

    def generate_complete_patient_record(
        self,
        num_problems: int = 3,
        num_medications: int = 2,
        num_allergies: int = 2,
        num_vital_signs_sets: int = 1,
        num_immunizations: int = 3,
    ) -> "dict[str, Any]":
        """Generate a complete patient record with all clinical data.

        This method generates a comprehensive patient record including demographics
        and all major clinical sections: problems, medications, allergies, vital signs,
        and immunizations.

        Args:
            num_problems: Number of problems to generate (default: 3)
            num_medications: Number of medications to generate (default: 2)
            num_allergies: Number of allergies to generate (default: 2)
            num_vital_signs_sets: Number of vital signs observation sets (default: 1)
            num_immunizations: Number of immunizations to generate (default: 3)

        Returns:
            Dictionary containing complete patient record:
            - patient: Patient demographic data
            - problems: List of clinical problems
            - medications: List of medications
            - allergies: List of allergies
            - vital_signs: List of vital signs observation sets
            - immunizations: List of immunizations
        """
        return {
            "patient": self.generate_patient(),
            "problems": [self.generate_problem() for _ in range(num_problems)],
            "medications": [self.generate_medication() for _ in range(num_medications)],
            "allergies": [self.generate_allergy() for _ in range(num_allergies)],
            "vital_signs": [self.generate_vital_signs() for _ in range(num_vital_signs_sets)],
            "immunizations": [self.generate_immunization() for _ in range(num_immunizations)],
        }
