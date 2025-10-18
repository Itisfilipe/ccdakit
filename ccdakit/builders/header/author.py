"""Author builder for CDA header."""

from lxml import etree

from ccdakit.builders.common import Identifier
from ccdakit.builders.demographics import Address, Telecom
from ccdakit.core.base import CDAElement
from ccdakit.protocols.author import AuthorProtocol, OrganizationProtocol


# CDA namespace for element creation
NS = "urn:hl7-org:v3"


class Author(CDAElement):
    """Builder for CDA Author."""

    # Standard OID for NPI
    NPI_OID = "2.16.840.1.113883.4.6"

    def __init__(self, author: AuthorProtocol, **kwargs):
        """
        Initialize Author builder.

        Args:
            author: Author data satisfying AuthorProtocol
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.author = author

    def build(self) -> etree.Element:
        """
        Build author XML element.

        Returns:
            lxml Element for author
        """
        author_elem = etree.Element(f"{{{NS}}}author")

        # Add time (when authored)
        time = etree.SubElement(author_elem, f"{{{NS}}}time")
        time.set("value", self.author.time.strftime("%Y%m%d%H%M%S"))

        # Create assignedAuthor
        assigned_author = etree.SubElement(author_elem, f"{{{NS}}}assignedAuthor")

        # Add identifiers (NPI if available)
        self._add_identifiers(assigned_author)

        # Add addresses
        for addr_data in self.author.addresses:
            addr_builder = Address(addr_data, use="work")
            assigned_author.append(addr_builder.to_element())

        # Add telecoms
        for telecom_data in self.author.telecoms:
            telecom_builder = Telecom(telecom_data)
            assigned_author.append(telecom_builder.to_element())

        # Add assignedPerson
        assigned_person = etree.SubElement(assigned_author, f"{{{NS}}}assignedPerson")
        self._add_name(assigned_person)

        # Add representedOrganization if available
        if self.author.organization:
            self._add_organization(assigned_author)

        return author_elem

    def _add_identifiers(self, assigned_author: etree._Element) -> None:
        """
        Add author identifiers to assignedAuthor.

        Args:
            assigned_author: assignedAuthor element
        """
        if self.author.npi:
            npi_id = Identifier(root=self.NPI_OID, extension=self.author.npi)
            assigned_author.append(npi_id.to_element())
        else:
            # Add null flavor if no identifiers
            null_id = Identifier(root="", null_flavor="NI")
            assigned_author.append(null_id.to_element())

    def _add_name(self, assigned_person: etree._Element) -> None:
        """
        Add author name to assignedPerson.

        Args:
            assigned_person: assignedPerson element
        """
        name = etree.SubElement(assigned_person, f"{{{NS}}}name")

        # Add given name (first name)
        given = etree.SubElement(name, f"{{{NS}}}given")
        given.text = self.author.first_name

        # Add middle name if available
        if self.author.middle_name:
            middle = etree.SubElement(name, f"{{{NS}}}given")
            middle.text = self.author.middle_name

        # Add family name (last name)
        family = etree.SubElement(name, f"{{{NS}}}family")
        family.text = self.author.last_name

    def _add_organization(self, assigned_author: etree._Element) -> None:
        """
        Add represented organization to assignedAuthor.

        Args:
            assigned_author: assignedAuthor element
        """
        org = self.author.organization
        assert org is not None
        rep_org = etree.SubElement(assigned_author, f"{{{NS}}}representedOrganization")

        # Add organization identifier (NPI if available)
        if org.npi:
            npi_id = Identifier(root=self.NPI_OID, extension=org.npi)
            rep_org.append(npi_id.to_element())
        elif org.oid_root:
            org_id = Identifier(root=org.oid_root)
            rep_org.append(org_id.to_element())

        # Add organization name
        name = etree.SubElement(rep_org, f"{{{NS}}}name")
        name.text = org.name

        # Add organization addresses
        for addr_data in org.addresses:
            addr_builder = Address(addr_data, use="work")
            rep_org.append(addr_builder.to_element())

        # Add organization telecoms
        for telecom_data in org.telecoms:
            telecom_builder = Telecom(telecom_data)
            rep_org.append(telecom_builder.to_element())


class Custodian(CDAElement):
    """Builder for CDA Custodian (document custodian organization)."""

    # Standard OID for NPI
    NPI_OID = "2.16.840.1.113883.4.6"

    def __init__(self, organization: OrganizationProtocol, **kwargs):
        """
        Initialize Custodian builder.

        Args:
            organization: Organization data satisfying OrganizationProtocol
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.organization = organization

    def build(self) -> etree.Element:
        """
        Build custodian XML element.

        Returns:
            lxml Element for custodian
        """
        custodian = etree.Element(f"{{{NS}}}custodian")

        # Create assignedCustodian
        assigned_custodian = etree.SubElement(custodian, f"{{{NS}}}assignedCustodian")

        # Create representedCustodianOrganization
        rep_org = etree.SubElement(assigned_custodian, f"{{{NS}}}representedCustodianOrganization")

        # Add organization identifier (NPI if available)
        if self.organization.npi:
            npi_id = Identifier(root=self.NPI_OID, extension=self.organization.npi)
            rep_org.append(npi_id.to_element())
        elif self.organization.oid_root:
            org_id = Identifier(root=self.organization.oid_root)
            rep_org.append(org_id.to_element())
        else:
            # Add null flavor if no identifiers
            null_id = Identifier(root="", null_flavor="NI")
            rep_org.append(null_id.to_element())

        # Add organization name
        name = etree.SubElement(rep_org, f"{{{NS}}}name")
        name.text = self.organization.name

        # Add organization telecom
        for telecom_data in self.organization.telecoms:
            telecom_builder = Telecom(telecom_data)
            rep_org.append(telecom_builder.to_element())

        # Add organization address
        for addr_data in self.organization.addresses:
            addr_builder = Address(addr_data, use="work")
            rep_org.append(addr_builder.to_element())

        return custodian
