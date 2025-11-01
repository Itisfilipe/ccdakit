"""RecordTarget builder for patient demographics in CDA header."""

from lxml import etree

from ccdakit.builders.common import Code, Identifier
from ccdakit.builders.demographics import Address, Telecom
from ccdakit.core.base import CDAElement
from ccdakit.protocols.patient import PatientProtocol


# CDA namespace for element creation
NS = "urn:hl7-org:v3"


class RecordTarget(CDAElement):
    """Builder for CDA RecordTarget (patient demographics)."""

    # Standard OID for SSN
    SSN_OID = "2.16.840.1.113883.4.1"

    # Administrative Gender codes
    GENDER_CODES = {
        "M": ("M", "Male"),
        "F": ("F", "Female"),
        "UN": ("UN", "Undifferentiated"),
    }

    def __init__(self, patient: PatientProtocol, **kwargs):
        """
        Initialize RecordTarget builder.

        Args:
            patient: Patient data satisfying PatientProtocol
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.patient = patient

    def build(self) -> etree.Element:
        """
        Build recordTarget XML element.

        Returns:
            lxml Element for recordTarget
        """
        record_target = etree.Element(f"{{{NS}}}recordTarget")

        # Create patientRole
        patient_role = etree.SubElement(record_target, f"{{{NS}}}patientRole")

        # Add patient identifiers
        self._add_identifiers(patient_role)

        # Add addresses
        for addr_data in self.patient.addresses:
            addr_builder = Address(addr_data, use="home")
            patient_role.append(addr_builder.to_element())

        # Add telecoms
        for telecom_data in self.patient.telecoms:
            telecom_builder = Telecom(telecom_data)
            patient_role.append(telecom_builder.to_element())

        # Add patient element
        patient_elem = etree.SubElement(patient_role, f"{{{NS}}}patient")

        # Add name
        self._add_name(patient_elem)

        # Add administrative gender
        self._add_gender(patient_elem)

        # Add birth time
        self._add_birth_time(patient_elem)

        # Add maritalStatusCode (SHOULD per CONF:1198-5303)
        # Note: Must come AFTER birthTime but BEFORE raceCode per XSD schema
        self._add_marital_status(patient_elem)

        # Add race (REQUIRED per CONF:1198-5322)
        # Patient SHALL contain exactly one [1..1] raceCode
        if self.patient.race:
            race_code = Code(
                code=self.patient.race,
                system="2.16.840.1.113883.6.238",  # CDC Race and Ethnicity
                display_name="Race",
            )
        else:
            # Default to "Unknown" race if not provided (2131-1 = Other Race)
            race_code = Code(
                code="2131-1",  # Other Race from Race Category value set
                system="2.16.840.1.113883.6.238",  # CDC Race and Ethnicity
                display_name="Other Race",
            )
        race_elem = race_code.to_element()
        race_elem.tag = f"{{{NS}}}raceCode"
        patient_elem.append(race_elem)

        # Add ethnicity (if available)
        if self.patient.ethnicity:
            eth_code = Code(
                code=self.patient.ethnicity,
                system="2.16.840.1.113883.6.238",  # CDC Race and Ethnicity
                display_name="Ethnicity",
            )
            eth_elem = eth_code.to_element()
            eth_elem.tag = f"{{{NS}}}ethnicGroupCode"
            patient_elem.append(eth_elem)

        # Add language (SHOULD per CONF:1198-5406)
        # Note: Must come AFTER maritalStatusCode, raceCode, ethnicGroupCode per XSD schema
        # Always add languageCommunication to meet SHOULD requirement
        if self.patient.language:
            self._add_language(patient_elem)
        else:
            # Add default language (English) to meet SHOULD requirement
            self._add_default_language(patient_elem)

        return record_target

    def _add_identifiers(self, patient_role: etree._Element) -> None:
        """
        Add patient identifiers to patientRole.

        Args:
            patient_role: patientRole element
        """
        # Add SSN if available
        if self.patient.ssn:
            ssn_id = Identifier(root=self.SSN_OID, extension=self.patient.ssn)
            patient_role.append(ssn_id.to_element())
        else:
            # Add null flavor if no identifiers
            null_id = Identifier(root="", null_flavor="NI")
            patient_role.append(null_id.to_element())

    def _add_name(self, patient_elem: etree._Element) -> None:
        """
        Add patient name to patient element.

        Args:
            patient_elem: patient element
        """
        name = etree.SubElement(patient_elem, f"{{{NS}}}name")

        # Add given name (first name)
        given = etree.SubElement(name, f"{{{NS}}}given")
        given.text = self.patient.first_name

        # Add middle name if available
        if self.patient.middle_name:
            middle = etree.SubElement(name, f"{{{NS}}}given")
            middle.text = self.patient.middle_name

        # Add family name (last name)
        family = etree.SubElement(name, f"{{{NS}}}family")
        family.text = self.patient.last_name

    def _add_gender(self, patient_elem: etree._Element) -> None:
        """
        Add administrative gender to patient element.

        Args:
            patient_elem: patient element
        """
        gender_info = self.GENDER_CODES.get(self.patient.sex, (self.patient.sex, None))
        code, display = gender_info

        gender_code = Code(
            code=code,
            system="2.16.840.1.113883.5.1",  # AdministrativeGender
            display_name=display,
        )
        gender_elem = gender_code.to_element()
        gender_elem.tag = f"{{{NS}}}administrativeGenderCode"
        patient_elem.append(gender_elem)

    def _add_birth_time(self, patient_elem: etree._Element) -> None:
        """
        Add birth time to patient element.

        Args:
            patient_elem: patient element
        """
        birth_time = etree.SubElement(patient_elem, f"{{{NS}}}birthTime")
        birth_time.set("value", self.patient.date_of_birth.strftime("%Y%m%d"))

    def _add_marital_status(self, patient_elem: etree._Element) -> None:
        """
        Add marital status code to patient element.

        Per C-CDA spec (CONF:1198-5303):
        - Patient SHOULD contain zero or one [0..1] maritalStatusCode

        Args:
            patient_elem: patient element
        """
        # Check if patient has marital_status attribute
        marital_status = getattr(self.patient, 'marital_status', None)

        if marital_status:
            # Use provided marital status
            marital_code = Code(
                code=marital_status,
                system="2.16.840.1.113883.5.2",  # MaritalStatus
                display_name="Marital Status",
            )
        else:
            # Default to "Unknown" to meet SHOULD requirement
            marital_code = Code(
                code="UNK",
                system="2.16.840.1.113883.5.2",  # MaritalStatus
                display_name="Unknown",
            )

        marital_elem = marital_code.to_element()
        marital_elem.tag = f"{{{NS}}}maritalStatusCode"
        patient_elem.append(marital_elem)

    def _add_language(self, patient_elem: etree._Element) -> None:
        """
        Add language communication to patient element.

        Per C-CDA spec (CONF:1198-9965):
        - languageCommunication SHOULD contain zero or one [0..1] proficiencyLevelCode

        Args:
            patient_elem: patient element
        """
        lang_comm = etree.SubElement(patient_elem, f"{{{NS}}}languageCommunication")

        lang_code = etree.SubElement(lang_comm, f"{{{NS}}}languageCode")
        lang_code.set("code", self.patient.language)

        # Add proficiencyLevelCode (SHOULD per CONF:1198-9965)
        # Default to "Good" proficiency level
        proficiency = etree.SubElement(lang_comm, f"{{{NS}}}proficiencyLevelCode")
        proficiency.set("code", "G")  # Good
        proficiency.set("codeSystem", "2.16.840.1.113883.5.61")  # LanguageAbilityProficiency
        proficiency.set("displayName", "Good")

        # Add preference indicator (true for primary language)
        pref = etree.SubElement(lang_comm, f"{{{NS}}}preferenceInd")
        pref.set("value", "true")

    def _add_default_language(self, patient_elem: etree._Element) -> None:
        """
        Add default language communication (English) when patient language not specified.

        Per C-CDA spec (CONF:1198-5406):
        - patient SHOULD contain zero or more [0..*] languageCommunication

        Args:
            patient_elem: patient element
        """
        lang_comm = etree.SubElement(patient_elem, f"{{{NS}}}languageCommunication")

        lang_code = etree.SubElement(lang_comm, f"{{{NS}}}languageCode")
        lang_code.set("code", "en")  # English

        # Add proficiencyLevelCode (SHOULD per CONF:1198-9965)
        proficiency = etree.SubElement(lang_comm, f"{{{NS}}}proficiencyLevelCode")
        proficiency.set("code", "G")  # Good
        proficiency.set("codeSystem", "2.16.840.1.113883.5.61")  # LanguageAbilityProficiency
        proficiency.set("displayName", "Good")

        # Add preference indicator
        pref = etree.SubElement(lang_comm, f"{{{NS}}}preferenceInd")
        pref.set("value", "true")
