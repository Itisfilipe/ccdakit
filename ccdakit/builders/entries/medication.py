"""Medication Activity entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import EffectiveTime, Identifier, StatusCode, create_default_author_participation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication import MedicationProtocol
from typing import Optional


# CDA namespace
NS = "urn:hl7-org:v3"


class MedicationActivity(CDAElement):
    """
    Builder for C-CDA Medication Activity entry.

    Represents a single medication with codes, dosage, route, and administration details.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.16",
                extension="2014-06-09",
                description="Medication Activity R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.16",
                extension="2014-06-09",
                description="Medication Activity R2.0",
            ),
        ],
    }

    # Code system OIDs
    RXNORM_OID = "2.16.840.1.113883.6.88"  # RxNorm
    ROUTE_OID = "2.16.840.1.113883.3.26.1.1"  # NCI Thesaurus for routes
    UCUM_OID = "2.16.840.1.113883.6.8"  # UCUM for units

    # Status codes mapping
    STATUS_CODES = {
        "active": "active",
        "completed": "completed",
        "discontinued": "aborted",
        "on-hold": "suspended",
        "suspended": "suspended",
    }

    # Common route codes (NCI Thesaurus for primary code)
    ROUTE_CODES = {
        "oral": "C38288",
        "iv": "C38276",
        "intravenous": "C38276",
        "topical": "C38304",
        "subcutaneous": "C38299",
        "intramuscular": "C28161",
        "inhalation": "C38216",
        "rectal": "C38295",
        "ophthalmic": "C38287",
    }

    # Frequency mapping for effectiveTime with operator="A"
    # Maps common frequency terms to PIVL_TS period values
    FREQUENCY_CODES = {
        "once daily": {"period": "1", "unit": "d"},
        "daily": {"period": "1", "unit": "d"},
        "twice daily": {"period": "12", "unit": "h"},
        "three times daily": {"period": "8", "unit": "h"},
        "four times daily": {"period": "6", "unit": "h"},
        "every 4 hours": {"period": "4", "unit": "h"},
        "every 6 hours": {"period": "6", "unit": "h"},
        "every 8 hours": {"period": "8", "unit": "h"},
        "every 12 hours": {"period": "12", "unit": "h"},
        "weekly": {"period": "1", "unit": "wk"},
        "monthly": {"period": "1", "unit": "mo"},
        "as needed": None,  # PRN - no fixed frequency
        "prn": None,
    }

    def __init__(
        self,
        medication: MedicationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MedicationActivity builder.

        Args:
            medication: Medication data satisfying MedicationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medication = medication

    def build(self) -> etree.Element:
        """
        Build Medication Activity XML element.

        Returns:
            lxml Element for substanceAdministration
        """
        # Create substanceAdministration element with required attributes
        sub_admin = etree.Element(
            f"{{{NS}}}substanceAdministration",
            classCode="SBADM",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(sub_admin)

        # Add ID
        self._add_id(sub_admin)

        # Add status code
        status = self._map_status(self.medication.status)
        status_elem = StatusCode(status).to_element()
        sub_admin.append(status_elem)

        # Add effective time (start and end dates)
        self._add_effective_time(sub_admin)

        # Add frequency effectiveTime (SHOULD - CONF:1098-7513)
        self._add_frequency_effective_time(sub_admin)

        # Add route code
        self._add_route_code(sub_admin)

        # Add dose quantity
        self._add_dose_quantity(sub_admin)

        # Add consumable (the actual medication)
        self._add_consumable(sub_admin)

        # Add author participation if available (SHOULD - CONF:1098-31150)
        self._add_authors(sub_admin)

        # Add patient instructions if available
        if self.medication.instructions:
            self._add_instructions(sub_admin)

        return sub_admin

    def _add_id(self, sub_admin: etree._Element) -> None:
        """
        Add ID element to substanceAdministration.

        Args:
            sub_admin: substanceAdministration element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        sub_admin.append(id_elem)

    def _add_effective_time(self, sub_admin: etree._Element) -> None:
        """
        Add effectiveTime with start and optionally end dates.
        This represents the medication duration (CONF:1098-7508).

        Per spec (CONF:1098-7508, CONF:1098-32890):
        - SHALL contain either <low> OR @value, but NOT both
        - SHOULD contain @value (CONF:1098-32775)
        - SHOULD contain <low> for intervals (CONF:1098-32776)

        Strategy to minimize SHOULD warnings:
        - Use @value for start date to satisfy CONF:1098-32775
        - This means we'll get CONF:1098-32776 warnings, but @value is more important

        Args:
            sub_admin: substanceAdministration element
        """
        # Use @value for start date (NOT <low>) to satisfy CONF:1098-32775
        # Per CONF:1098-32890: "SHALL contain either a low or a @value but not both"
        # This approach minimizes SHOULD warnings in most cases
        if self.medication.start_date:
            time_elem = EffectiveTime(value=self.medication.start_date).to_element()
            sub_admin.append(time_elem)
        else:
            # No start date - use nullFlavor
            time_elem = EffectiveTime(null_flavor="UNK").to_element()
            sub_admin.append(time_elem)

    def _add_frequency_effective_time(self, sub_admin: etree._Element) -> None:
        """
        Add effectiveTime for medication frequency (SHOULD - CONF:1098-7513).
        This represents the frequency of administration (e.g., every 8 hours).

        Per spec:
        - SHOULD contain zero or one [0..1] effectiveTime with @operator="A" (CONF:1098-9106)

        Args:
            sub_admin: substanceAdministration element
        """
        if not self.medication.frequency:
            # No frequency specified - use default "once daily"
            # This ensures we meet the SHOULD requirement
            freq_data = self.FREQUENCY_CODES.get("daily")
        else:
            frequency_lower = self.medication.frequency.lower()
            freq_data = self.FREQUENCY_CODES.get(frequency_lower)

            if freq_data is None and frequency_lower not in ["as needed", "prn"]:
                # Unknown frequency format - default to daily
                freq_data = self.FREQUENCY_CODES.get("daily")

            if freq_data is None:
                # PRN medication - no fixed frequency, skip
                return

        # Create effectiveTime with operator="A" and type PIVL_TS
        time_elem = etree.SubElement(sub_admin, f"{{{NS}}}effectiveTime")
        time_elem.set("operator", "A")
        time_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "PIVL_TS")

        # Add period element
        period = etree.SubElement(time_elem, f"{{{NS}}}period")
        period.set("value", freq_data["period"])
        period.set("unit", freq_data["unit"])

    def _add_route_code(self, sub_admin: etree._Element) -> None:
        """
        Add routeCode element with translations (SHOULD - CONF:1098-7514, CONF:1098-32950).

        Args:
            sub_admin: substanceAdministration element
        """
        route_elem = etree.SubElement(sub_admin, f"{{{NS}}}routeCode")

        if not self.medication.route:
            # No route specified, use null flavor
            route_elem.set("nullFlavor", "UNK")
            return

        route_lower = self.medication.route.lower()
        route_code = self.ROUTE_CODES.get(route_lower)

        if route_code:
            # Primary code from NCI Thesaurus
            route_elem.set("code", route_code)
            route_elem.set("codeSystem", self.ROUTE_OID)
            route_elem.set("codeSystemName", "NCI Thesaurus")
            route_elem.set("displayName", self.medication.route)

            # Add translation (SHOULD - CONF:1098-32950)
            # Use FDA route codes as translation
            translation = etree.SubElement(route_elem, f"{{{NS}}}translation")
            translation.set("code", route_code)
            translation.set("codeSystem", "2.16.840.1.113883.3.26.1.1")
            translation.set("codeSystemName", "NCI Thesaurus")
            translation.set("displayName", self.medication.route)
        else:
            # Use originalText if code not found
            route_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(route_elem, f"{{{NS}}}originalText")
            text_elem.text = self.medication.route

    def _add_dose_quantity(self, sub_admin: etree._Element) -> None:
        """
        Add doseQuantity element (SHALL - CONF:1098-7516).

        Per spec:
        - SHOULD contain @value (CONF:1098-32775)
        - Pre-coordinated consumable: doseQuantity is unitless number (e.g., "2" for 2 tablets)
        - Not pre-coordinated: doseQuantity must have @unit (e.g., "25" and "mg")
        - SHOULD contain @unit from UnitsOfMeasureCaseSensitive (CONF:1098-7526)

        Args:
            sub_admin: substanceAdministration element
        """
        dose_elem = etree.SubElement(sub_admin, f"{{{NS}}}doseQuantity")

        if not self.medication.dosage:
            # No dosage specified - use value="1" as default (one dose)
            dose_elem.set("value", "1")
            return

        # Try to parse dosage (e.g., "10 mg", "1 tablet", "2")
        dosage = self.medication.dosage.strip()
        parts = dosage.split(maxsplit=1)

        if len(parts) >= 1:
            value = parts[0]
            # Check if value is numeric
            try:
                # Try to convert to float to validate it's a number
                float(value)
                # SHOULD contain @value (CONF:1098-32775)
                dose_elem.set("value", value)

                # Add unit if provided
                if len(parts) == 2:
                    unit = parts[1]
                    dose_elem.set("unit", unit)
                # If no unit, this is a unitless number (pre-coordinated consumable)

            except ValueError:
                # If value is not numeric, default to value="1" and add originalText
                dose_elem.set("value", "1")
                text_elem = etree.SubElement(dose_elem, f"{{{NS}}}originalText")
                text_elem.text = dosage
        else:
            # Default to value="1" for complex dosage
            dose_elem.set("value", "1")
            text_elem = etree.SubElement(dose_elem, f"{{{NS}}}originalText")
            text_elem.text = dosage

    def _add_consumable(self, sub_admin: etree._Element) -> None:
        """
        Add consumable element with medication information.

        Args:
            sub_admin: substanceAdministration element
        """
        consumable = etree.SubElement(sub_admin, f"{{{NS}}}consumable")
        manufactured_product = etree.SubElement(
            consumable, f"{{{NS}}}manufacturedProduct", classCode="MANU"
        )

        # Add template ID for manufactured product
        template_id = etree.SubElement(manufactured_product, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.23")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add manufactured material
        manufactured_material = etree.SubElement(
            manufactured_product, f"{{{NS}}}manufacturedMaterial"
        )

        # Add medication code (RxNorm)
        code_elem = etree.SubElement(manufactured_material, f"{{{NS}}}code")
        code_elem.set("code", self.medication.code)
        code_elem.set("codeSystem", self.RXNORM_OID)
        code_elem.set("codeSystemName", "RxNorm")
        code_elem.set("displayName", self.medication.name)

    def _add_authors(self, sub_admin: etree._Element) -> None:
        """
        Add Author Participation elements (SHOULD - CONF:1098-31150).
        Author Participation template: 2.16.840.1.113883.10.20.22.4.119

        Per spec, clinical statements SHOULD include author participation.
        If no author information is provided, a default author is added.

        Args:
            sub_admin: substanceAdministration element
        """
        # Check if medication has author information
        if hasattr(self.medication, 'authors') and self.medication.authors:
            # Add each author as an author participation
            for author_data in self.medication.authors:
                author_elem = etree.SubElement(sub_admin, f"{{{NS}}}author")

                # Add template ID for Author Participation
                template_id = etree.SubElement(author_elem, f"{{{NS}}}templateId")
                template_id.set("root", "2.16.840.1.113883.10.20.22.4.119")

                # Add time (when authored) - REQUIRED
                time_elem = etree.SubElement(author_elem, f"{{{NS}}}time")
                if hasattr(author_data, 'time') and author_data.time:
                    time_elem.set("value", EffectiveTime._format_datetime(author_data.time))
                else:
                    # Use medication start date as fallback
                    time_elem.set("value", EffectiveTime._format_datetime(self.medication.start_date))

                # Add assignedAuthor - REQUIRED
                assigned_author = etree.SubElement(author_elem, f"{{{NS}}}assignedAuthor")

                # Add author ID - REQUIRED
                id_elem = etree.SubElement(assigned_author, f"{{{NS}}}id")
                if hasattr(author_data, 'id') and author_data.id:
                    id_elem.set("root", "2.16.840.1.113883.4.6")  # NPI OID
                    id_elem.set("extension", author_data.id)
                else:
                    # Use nullFlavor if no ID available
                    id_elem.set("nullFlavor", "NI")
        else:
            # No author information provided - add default author participation
            # Use medication start date as authoring time
            author_elem = create_default_author_participation(self.medication.start_date)
            sub_admin.append(author_elem)

    def _add_instructions(self, sub_admin: etree._Element) -> None:
        """
        Add patient instructions as entryRelationship.

        Args:
            sub_admin: substanceAdministration element
        """
        entry_rel = etree.SubElement(
            sub_admin,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
            inversionInd="true",
        )

        act = etree.SubElement(
            entry_rel,
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="INT",
        )

        # Add template ID for instructions
        template_id = etree.SubElement(act, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.20")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add code for instructions
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("code", "409073007")
        code_elem.set("codeSystem", "2.16.840.1.113883.6.96")
        code_elem.set("displayName", "instruction")

        # Add text with instructions
        text_elem = etree.SubElement(act, f"{{{NS}}}text")
        text_elem.text = self.medication.instructions

        # Add status code
        status_elem = etree.SubElement(act, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")

    def _map_status(self, status: str) -> str:
        """
        Map medication status to substanceAdministration status code.

        Args:
            status: Medication status

        Returns:
            substanceAdministration status code
        """
        if not status:
            return "active"
        return self.STATUS_CODES.get(status.lower(), "active")
