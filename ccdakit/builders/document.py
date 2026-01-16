"""ClinicalDocument top-level builder."""

import uuid
from datetime import datetime
from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code, Identifier
from ccdakit.builders.header.author import Author, Custodian
from ccdakit.builders.header.record_target import RecordTarget
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.core.config import get_config
from ccdakit.protocols.author import AuthorProtocol, OrganizationProtocol
from ccdakit.protocols.patient import PatientProtocol


class ClinicalDocument(CDAElement):
    """Top-level C-CDA Clinical Document builder."""

    # C-CDA R2.1 templates
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.1",
                extension="2015-08-01",
                description="C-CDA R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.1",
                extension="2014-06-09",
                description="C-CDA R2.0",
            ),
        ],
    }

    # XML Namespaces
    NAMESPACES = {
        None: "urn:hl7-org:v3",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "sdtc": "urn:hl7-org:sdtc",
    }

    # Default namespace URI for element creation
    NS = "urn:hl7-org:v3"

    def __init__(
        self,
        patient: PatientProtocol,
        author: AuthorProtocol,
        custodian: OrganizationProtocol,
        sections: Optional[Sequence[CDAElement]] = None,
        document_id: Optional[str] = None,
        title: str = "Clinical Summary",
        effective_time: Optional[datetime] = None,
        **kwargs,
    ):
        """
        Initialize ClinicalDocument builder.

        Args:
            patient: Patient data satisfying PatientProtocol
            author: Author data satisfying AuthorProtocol
            custodian: Custodian organization data satisfying OrganizationProtocol
            sections: List of section builders (optional)
            document_id: Document UUID (generated if not provided)
            title: Document title
            effective_time: Document creation time (current time if not provided)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.patient = patient
        self.author = author
        self.custodian = custodian
        self.sections = sections or []
        self.document_id = document_id or str(uuid.uuid4())
        self.title = title
        self.effective_time = effective_time or datetime.now()

    def build(self) -> etree.Element:
        """
        Build ClinicalDocument XML element.

        Returns:
            lxml Element for ClinicalDocument
        """
        # Create root element with namespaces
        doc = etree.Element(f"{{{self.NS}}}ClinicalDocument", nsmap=self.NAMESPACES)

        # Add realmCode (US)
        realm = etree.SubElement(doc, f"{{{self.NS}}}realmCode")
        realm.set("code", "US")

        # Add typeId (CDA Release 2)
        type_id = etree.SubElement(doc, f"{{{self.NS}}}typeId")
        type_id.set("root", "2.16.840.1.113883.1.3")
        type_id.set("extension", "POCD_HD000040")

        # Add templateIds
        self.add_template_ids(doc)

        # Add document id
        doc_id = Identifier(root=self._get_document_id_root(), extension=self.document_id)
        doc.append(doc_id.to_element())

        # Add code (document type)
        self._add_document_code(doc)

        # Add title
        title_elem = etree.SubElement(doc, f"{{{self.NS}}}title")
        title_elem.text = self.title

        # Add effectiveTime (with timezone for precision per CONF:81-10130)
        # Import here to avoid circular import with common module
        from ccdakit.builders.common import EffectiveTime

        effective_time_elem = etree.SubElement(doc, f"{{{self.NS}}}effectiveTime")
        effective_time_elem.set("value", EffectiveTime._format_datetime(self.effective_time))

        # Add confidentialityCode
        conf_code = Code(code="N", system="2.16.840.1.113883.5.25")  # Confidentiality
        conf_elem = conf_code.to_element()
        conf_elem.tag = f"{{{self.NS}}}confidentialityCode"
        doc.append(conf_elem)

        # Add languageCode
        lang = etree.SubElement(doc, f"{{{self.NS}}}languageCode")
        lang.set("code", "en-US")

        # Add recordTarget (patient)
        record_target = RecordTarget(self.patient, version=self.version)
        doc.append(record_target.to_element())

        # Add author
        author_builder = Author(self.author, version=self.version)
        doc.append(author_builder.to_element())

        # Add custodian
        custodian_builder = Custodian(self.custodian, version=self.version)
        doc.append(custodian_builder.to_element())

        # Add legalAuthenticator (SHOULD per CONF:1198-5579)
        self._add_legal_authenticator(doc)

        # Add component (body)
        if self.sections:
            self._add_body(doc)

        return doc

    def _get_document_id_root(self) -> str:
        """
        Get document ID root from config or use default.

        Returns:
            Document ID root OID
        """
        try:
            config = get_config()
            if config.document_id_root:
                return config.document_id_root
        except RuntimeError:
            pass

        # Default document ID root
        return "2.16.840.1.113883.19.5"

    def _add_document_code(self, doc: etree._Element) -> None:
        """
        Add document type code to document.

        Args:
            doc: ClinicalDocument element
        """
        # LOINC code for Clinical Summary
        doc_code = Code(
            code="34133-9",
            system="LOINC",
            display_name="Summarization of Episode Note",
        )
        code_elem = doc_code.to_element()
        doc.append(code_elem)

    def _add_legal_authenticator(self, doc: etree._Element) -> None:
        """
        Add legalAuthenticator to document.

        Per C-CDA spec (CONF:1198-5579):
        - ClinicalDocument SHOULD contain zero or one [0..1] legalAuthenticator

        The legalAuthenticator is responsible for the accuracy of the document
        content. Uses the document author as the legal authenticator.

        Args:
            doc: ClinicalDocument element
        """
        # Import here to avoid circular import with common module
        from ccdakit.builders.common import EffectiveTime

        # Create legalAuthenticator element
        legal_auth = etree.SubElement(doc, f"{{{self.NS}}}legalAuthenticator")

        # Add time (when authenticated - use effective time)
        time = etree.SubElement(legal_auth, f"{{{self.NS}}}time")
        time.set("value", EffectiveTime._format_datetime(self.effective_time))

        # Add signatureCode (signed)
        sig_code = etree.SubElement(legal_auth, f"{{{self.NS}}}signatureCode")
        sig_code.set("code", "S")  # Signed

        # Add assignedEntity
        assigned_entity = etree.SubElement(legal_auth, f"{{{self.NS}}}assignedEntity")

        # Add ID (use NPI if available)
        id_elem = etree.SubElement(assigned_entity, f"{{{self.NS}}}id")
        if self.author.npi:
            id_elem.set("root", "2.16.840.1.113883.4.6")  # NPI OID
            id_elem.set("extension", self.author.npi)
        else:
            id_elem.set("nullFlavor", "NI")

        # Add addresses (SHALL per CONF:1198-5589)
        # Import here to avoid circular import with demographics module
        from ccdakit.builders.demographics import Address

        for addr_data in self.author.addresses:
            addr_builder = Address(addr_data, use="work")
            assigned_entity.append(addr_builder.to_element())

        # Add telecoms (SHALL per CONF:1198-5595)
        # Import here to avoid circular import with demographics module
        from ccdakit.builders.demographics import Telecom

        for telecom_data in self.author.telecoms:
            telecom_builder = Telecom(telecom_data)
            assigned_entity.append(telecom_builder.to_element())

        # Add assignedPerson with name
        assigned_person = etree.SubElement(assigned_entity, f"{{{self.NS}}}assignedPerson")
        name = etree.SubElement(assigned_person, f"{{{self.NS}}}name")

        # Add given name
        given = etree.SubElement(name, f"{{{self.NS}}}given")
        given.text = self.author.first_name

        # Add family name
        family = etree.SubElement(name, f"{{{self.NS}}}family")
        family.text = self.author.last_name

    def _add_body(self, doc: etree._Element) -> None:
        """
        Add structured body with sections to document.

        Args:
            doc: ClinicalDocument element
        """
        # Create component
        component = etree.SubElement(doc, f"{{{self.NS}}}component")

        # Create structuredBody
        structured_body = etree.SubElement(component, f"{{{self.NS}}}structuredBody")

        # Add each section wrapped in a component
        for section_builder in self.sections:
            section_component = etree.SubElement(structured_body, f"{{{self.NS}}}component")
            section_elem = section_builder.to_element()
            section_component.append(section_elem)

    def to_xml_string(self, pretty: bool = True) -> str:
        """
        Convert to XML string with declaration.

        Args:
            pretty: Whether to pretty-print XML

        Returns:
            Complete XML document with declaration
        """
        elem = self.to_element()

        xml_bytes = etree.tostring(
            elem,
            pretty_print=pretty,
            xml_declaration=True,
            encoding="UTF-8",
        )

        # Clean whitespace from elements that should not have text content
        # This is required for XSD validation - elements with complex type
        # that only contain child elements cannot have text content (including whitespace)
        if pretty:
            xml_str = xml_bytes.decode("UTF-8")
            xml_str = self._clean_element_only_whitespace(xml_str)
            return xml_str

        return xml_bytes.decode("UTF-8")

    def _clean_element_only_whitespace(self, xml_str: str) -> str:
        """
        Clean whitespace from elements that should not have text content.

        This is required for XSD validation. Elements with complex types that only contain
        child elements (like effectiveTime with IVL_TS type) cannot have text content,
        including whitespace from pretty-printing.

        Args:
            xml_str: XML string to clean

        Returns:
            Cleaned XML string
        """
        import re

        # Pattern to match effectiveTime elements with low/high children
        # Captures: opening tag, content with low/high, closing tag
        # Removes whitespace between opening tag and first child, and between children
        pattern = r'(<effectiveTime[^>]*>)\s*(<low[^>]*/>)\s*(<high[^>]*/>)\s*(</effectiveTime>)'
        xml_str = re.sub(pattern, r'\1\2\3\4', xml_str)

        # Also handle name elements with given/family
        pattern = r'(<name[^>]*>)\s*(<given[^>]*>.*?</given>)\s*(<family[^>]*>.*?</family>)\s*(</name>)'
        xml_str = re.sub(pattern, r'\1\2\3\4', xml_str)

        # Handle addr elements
        pattern = r'(<addr[^>]*>)\s*(<streetAddressLine[^>]*>.*?</streetAddressLine>)\s*(<city[^>]*>.*?</city>)\s*(<state[^>]*>.*?</state>)\s*(<postalCode[^>]*>.*?</postalCode>)\s*(</addr>)'
        xml_str = re.sub(pattern, r'\1\2\3\4\5\6', xml_str)

        return xml_str
