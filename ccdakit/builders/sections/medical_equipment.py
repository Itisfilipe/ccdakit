"""Medical Equipment Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.medical_equipment import (
    MedicalEquipmentOrganizer,
    NonMedicinalSupplyActivity,
)
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medical_equipment import MedicalEquipmentProtocol


# CDA namespace
NS = "urn:hl7-org:v3"

# TODO: Add support for Procedure Activity Procedure entries (CONF:1098-31885)
# for representing implanted devices. Currently only supports:
# - Medical Equipment Organizer (CONF:1098-7948)
# - Non-Medicinal Supply Activity (CONF:1098-31125)


class MedicalEquipmentSection(CDAElement):
    """
    Builder for C-CDA Medical Equipment Section.

    Defines a patient's implanted and external health and medical devices and equipment.
    Lists any pertinent durable medical equipment (DME) used to help maintain the
    patient's health status.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 and R2.0 versions (both use 2014-06-09 extension).
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.23",
                extension="2014-06-09",
                description="Medical Equipment Section V2",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.23",
                extension="2014-06-09",
                description="Medical Equipment Section V2",
            ),
        ],
    }

    def __init__(
        self,
        equipment_list: Sequence[MedicalEquipmentProtocol],
        title: str = "Medical Equipment",
        use_organizer: bool = False,
        organizer_start_date: Optional[object] = None,
        organizer_end_date: Optional[object] = None,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MedicalEquipmentSection builder.

        Args:
            equipment_list: List of medical equipment items satisfying MedicalEquipmentProtocol
            title: Section title (default: "Medical Equipment")
            use_organizer: If True, wrap equipment in Medical Equipment Organizer
            organizer_start_date: Start date if using organizer
            organizer_end_date: End date if using organizer
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.equipment_list = equipment_list
        self.title = title
        self.use_organizer = use_organizer
        self.organizer_start_date = organizer_start_date
        self.organizer_end_date = organizer_end_date

    def build(self) -> etree.Element:
        """
        Build Medical Equipment Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1098-7944, CONF:1098-10404, CONF:1098-32523)
        self.add_template_ids(section)

        # Add section code (CONF:1098-15381, CONF:1098-15382, CONF:1098-30828)
        code_elem = Code(
            code="46264-8",  # CONF:1098-15382
            system="LOINC",  # CONF:1098-30828
            display_name="Medical Equipment",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1098-7946)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1098-7947)
        self._add_narrative(section)

        # Add entries
        if self.use_organizer and self.equipment_list:
            # Add Medical Equipment Organizer (CONF:1098-7948, CONF:1098-30351)
            self._add_organizer_entry(section)
        else:
            # Add individual Non-Medicinal Supply Activity entries (CONF:1098-31125, CONF:1098-31861)
            for equipment in self.equipment_list:
                self._add_supply_entry(section, equipment)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.equipment_list:
            # No equipment - add "No medical equipment recorded" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No medical equipment recorded"
            return

        # Create table for equipment
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Equipment",
            "Code",
            "Date Supplied",
            "Date End",
            "Quantity",
            "Status",
            "Manufacturer",
            "Model/Serial",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, equipment in enumerate(self.equipment_list, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Equipment name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"equipment-{idx}",
            )
            content.text = equipment.name

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            if equipment.code and equipment.code_system:
                td_code.text = f"{equipment.code} ({equipment.code_system})"
            else:
                td_code.text = "-"

            # Date supplied
            td_date_start = etree.SubElement(tr, f"{{{NS}}}td")
            if equipment.date_supplied:
                if hasattr(equipment.date_supplied, "hour"):
                    td_date_start.text = equipment.date_supplied.strftime("%Y-%m-%d %H:%M")
                else:
                    td_date_start.text = equipment.date_supplied.strftime("%Y-%m-%d")
            else:
                td_date_start.text = "-"

            # Date end
            td_date_end = etree.SubElement(tr, f"{{{NS}}}td")
            if equipment.date_end:
                if hasattr(equipment.date_end, "hour"):
                    td_date_end.text = equipment.date_end.strftime("%Y-%m-%d %H:%M")
                else:
                    td_date_end.text = equipment.date_end.strftime("%Y-%m-%d")
            else:
                td_date_end.text = "-"

            # Quantity
            td_quantity = etree.SubElement(tr, f"{{{NS}}}td")
            if equipment.quantity is not None:
                td_quantity.text = str(equipment.quantity)
            else:
                td_quantity.text = "-"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = equipment.status.capitalize()

            # Manufacturer
            td_manufacturer = etree.SubElement(tr, f"{{{NS}}}td")
            if equipment.manufacturer:
                td_manufacturer.text = equipment.manufacturer
            else:
                td_manufacturer.text = "-"

            # Model/Serial
            td_model = etree.SubElement(tr, f"{{{NS}}}td")
            parts = []
            if equipment.model_number:
                parts.append(f"Model: {equipment.model_number}")
            if equipment.serial_number:
                parts.append(f"S/N: {equipment.serial_number}")
            if parts:
                td_model.text = ", ".join(parts)
            else:
                td_model.text = "-"

    def _add_supply_entry(
        self, section: etree._Element, equipment: MedicalEquipmentProtocol
    ) -> None:
        """
        Add entry element with Non-Medicinal Supply Activity (CONF:1098-31125, CONF:1098-31861).

        Args:
            section: section element
            equipment: Medical equipment data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Non-Medicinal Supply Activity
        supply_builder = NonMedicinalSupplyActivity(equipment, version=self.version)
        entry.append(supply_builder.to_element())

    def _add_organizer_entry(self, section: etree._Element) -> None:
        """
        Add entry element with Medical Equipment Organizer (CONF:1098-7948, CONF:1098-30351).

        Args:
            section: section element
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Medical Equipment Organizer
        organizer_builder = MedicalEquipmentOrganizer(
            equipment_list=self.equipment_list,
            status="completed",
            date_start=self.organizer_start_date,
            date_end=self.organizer_end_date,
            version=self.version,
        )
        entry.append(organizer_builder.to_element())
