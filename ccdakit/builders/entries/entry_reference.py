"""Entry Reference builder for C-CDA documents."""

from lxml import etree

from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig


# CDA namespace
NS = "urn:hl7-org:v3"


class EntryReference(CDAElement):
    """
    Builder for C-CDA Entry Reference.

    This template represents the act of referencing another entry in the same
    CDA document instance. Its purpose is to remove the need to repeat the
    complete XML representation of the referred entry when relating one entry
    to another.

    Template ID: 2.16.840.1.113883.10.20.22.4.122

    Conformance Rules:
    - SHALL contain classCode="ACT" (CONF:1098-31485)
    - SHALL contain moodCode="EVN" (CONF:1098-31486)
    - SHALL contain at least one [1..*] id (CONF:1098-31489)
    - SHALL contain code with nullFlavor="NP" (CONF:1098-31490, CONF:1098-31491)
    - SHALL contain statusCode (CONF:1098-31498)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.122",
                extension=None,
                description="Entry Reference",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.122",
                extension=None,
                description="Entry Reference",
            ),
        ],
    }

    def __init__(
        self,
        reference_id: str,
        reference_root: str = None,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize EntryReference builder.

        Args:
            reference_id: ID (extension) of the entry being referenced
            reference_root: Root OID for the ID (optional, uses default if not provided)
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.reference_id = reference_id
        self.reference_root = reference_root or "2.16.840.1.113883.19"

    def build(self) -> etree.Element:
        """
        Build Entry Reference XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1098-31485, CONF:1098-31486)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template ID (CONF:1098-31487, CONF:1098-31488)
        self.add_template_ids(act)

        # Add id element(s) (CONF:1098-31489) - SHALL contain at least one [1..*]
        id_elem = etree.SubElement(act, f"{{{NS}}}id")
        id_elem.set("root", self.reference_root)
        id_elem.set("extension", str(self.reference_id))

        # Add code with nullFlavor="NP" (CONF:1098-31490, CONF:1098-31491)
        # NP = Not Present (the value is not present in the message)
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("nullFlavor", "NP")

        # Add statusCode (CONF:1098-31498)
        # MAY contain @code="completed" (CONF:1098-31499)
        status_elem = etree.SubElement(act, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")

        return act
