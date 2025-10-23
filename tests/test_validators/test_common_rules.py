"""Tests for common validation rules library."""

from lxml import etree

from ccdakit.core.validation import ValidationLevel
from ccdakit.validators.common_rules import (
    AllergyStatusRule,
    AuthorPresenceRule,
    ContactInfoPresenceRule,
    CustodianPresenceRule,
    DocumentDateRule,
    PatientNameRule,
    ProblemStatusRule,
    SectionCountRule,
    TemplateIDPresenceRule,
    UniqueIDRule,
    VitalSignRangeRule,
)


class TestUniqueIDRule:
    """Test suite for UniqueIDRule."""

    def test_all_ids_unique(self):
        """Test when all IDs are unique."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <id root="1.2.3.4" extension="123" />
            <id root="1.2.3.4" extension="456" />
            <id root="5.6.7.8" extension="123" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = UniqueIDRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_duplicate_ids(self):
        """Test when IDs are duplicated."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <id root="1.2.3.4" extension="123" />
            <id root="1.2.3.4" extension="123" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = UniqueIDRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "Duplicate ID" in issues[0].message


class TestTemplateIDPresenceRule:
    """Test suite for TemplateIDPresenceRule."""

    def test_required_template_present(self):
        """Test when required template is present."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <templateId root="2.16.840.1.113883.10.20.22.1.1" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = TemplateIDPresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_required_template_missing(self):
        """Test when required template is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <templateId root="9.9.9.9.9" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = TemplateIDPresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "missing" in issues[0].message.lower()


class TestPatientNameRule:
    """Test suite for PatientNameRule."""

    def test_complete_patient_name(self):
        """Test patient with complete name."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <recordTarget>
                <patientRole>
                    <patient>
                        <name>
                            <given>John</given>
                            <family>Doe</family>
                        </name>
                    </patient>
                </patientRole>
            </recordTarget>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = PatientNameRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_missing_patient_name(self):
        """Test when patient name is completely missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <recordTarget>
                <patientRole>
                    <patient>
                    </patient>
                </patientRole>
            </recordTarget>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = PatientNameRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "Patient name is missing" in issues[0].message

    def test_missing_given_name(self):
        """Test when given name is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <recordTarget>
                <patientRole>
                    <patient>
                        <name>
                            <family>Doe</family>
                        </name>
                    </patient>
                </patientRole>
            </recordTarget>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = PatientNameRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "given" in issues[0].message.lower()

    def test_missing_family_name(self):
        """Test when family name is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <recordTarget>
                <patientRole>
                    <patient>
                        <name>
                            <given>John</given>
                        </name>
                    </patient>
                </patientRole>
            </recordTarget>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = PatientNameRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "family" in issues[0].message.lower()


class TestDocumentDateRule:
    """Test suite for DocumentDateRule."""

    def test_valid_document_date(self):
        """Test with valid document date."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="20200101" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DocumentDateRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_missing_document_date(self):
        """Test when document date is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DocumentDateRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "missing" in issues[0].message.lower()

    def test_future_document_date(self):
        """Test future document date when not allowed."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="29991231" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DocumentDateRule(allow_future=False)
        issues = rule.validate(doc)
        assert len(issues) >= 1
        future_issues = [i for i in issues if "future" in i.message.lower()]
        assert len(future_issues) == 1

    def test_invalid_date_format(self):
        """Test invalid date format."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="invalid" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DocumentDateRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "invalid" in issues[0].message.lower()

    def test_document_date_too_old(self):
        """Test document date exceeds max years past."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="19000101" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DocumentDateRule(max_years_past=50)
        issues = rule.validate(doc)
        assert len(issues) >= 1
        old_issues = [i for i in issues if "years old" in i.message.lower()]
        assert len(old_issues) == 1

    def test_invalid_date_format_too_short(self):
        """Test date string that's too short."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <effectiveTime value="2020" />
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = DocumentDateRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "too short" in issues[0].message.lower()


class TestAuthorPresenceRule:
    """Test suite for AuthorPresenceRule."""

    def test_author_present_with_name(self):
        """Test author present with name."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <author>
                <assignedAuthor>
                    <assignedPerson>
                        <name>
                            <given>Jane</given>
                            <family>Smith</family>
                        </name>
                    </assignedPerson>
                </assignedAuthor>
            </author>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = AuthorPresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_author_missing(self):
        """Test when author is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = AuthorPresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "author" in issues[0].message.lower()

    def test_author_without_name(self):
        """Test author without name."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <author>
                <assignedAuthor>
                    <id root="1.2.3.4" />
                </assignedAuthor>
            </author>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = AuthorPresenceRule(require_name=True)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert issues[0].level == ValidationLevel.WARNING
        assert "name" in issues[0].message.lower()


class TestCustodianPresenceRule:
    """Test suite for CustodianPresenceRule."""

    def test_custodian_present_with_name(self):
        """Test custodian present with organization name."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <custodian>
                <assignedCustodian>
                    <representedCustodianOrganization>
                        <name>Test Hospital</name>
                    </representedCustodianOrganization>
                </assignedCustodian>
            </custodian>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = CustodianPresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_custodian_missing(self):
        """Test when custodian is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = CustodianPresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "custodian" in issues[0].message.lower()

    def test_custodian_without_name(self):
        """Test custodian without organization name."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <custodian>
                <assignedCustodian>
                    <representedCustodianOrganization>
                        <id root="1.2.3.4" />
                    </representedCustodianOrganization>
                </assignedCustodian>
            </custodian>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = CustodianPresenceRule(require_organization_name=True)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert issues[0].level == ValidationLevel.WARNING
        assert "name" in issues[0].message.lower()

    def test_custodian_with_empty_name(self):
        """Test custodian with empty organization name."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <custodian>
                <assignedCustodian>
                    <representedCustodianOrganization>
                        <name>   </name>
                    </representedCustodianOrganization>
                </assignedCustodian>
            </custodian>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = CustodianPresenceRule(require_organization_name=True)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert issues[0].level == ValidationLevel.WARNING
        assert "empty" in issues[0].message.lower()


class TestSectionCountRule:
    """Test suite for SectionCountRule."""

    def test_section_count_within_range(self):
        """Test section count within min/max range."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <structuredBody>
                    <component><section /></component>
                    <component><section /></component>
                    <component><section /></component>
                </structuredBody>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = SectionCountRule(min_sections=1, max_sections=10)
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_too_few_sections(self):
        """Test when section count below minimum."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = SectionCountRule(min_sections=3)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "minimum" in issues[0].message.lower()

    def test_too_many_sections(self):
        """Test when section count exceeds maximum."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <structuredBody>
                    <component><section /></component>
                    <component><section /></component>
                    <component><section /></component>
                </structuredBody>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = SectionCountRule(max_sections=2)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "maximum" in issues[0].message.lower()


class TestVitalSignRangeRule:
    """Test suite for VitalSignRangeRule."""

    def test_vital_sign_in_range(self):
        """Test vital sign within normal range."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <code code="8480-6" />
                            <value value="120" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = VitalSignRangeRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_vital_sign_out_of_range(self):
        """Test vital sign outside normal range."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <code code="8480-6" />
                            <value value="300" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = VitalSignRangeRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "outside range" in issues[0].message.lower()

    def test_custom_ranges(self):
        """Test with custom vital sign ranges."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <code code="TEST-1" />
                            <value value="50" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = VitalSignRangeRule(ranges={"TEST-1": (0, 100)})
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_vital_sign_no_code(self):
        """Test vital sign without code attribute."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <value value="120" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = VitalSignRangeRule()
        issues = rule.validate(doc)
        assert len(issues) == 0  # Should skip observations without code

    def test_vital_sign_unknown_code(self):
        """Test vital sign with code not in range dict."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <code code="UNKNOWN-123" />
                            <value value="120" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = VitalSignRangeRule()
        issues = rule.validate(doc)
        assert len(issues) == 0  # Should skip unknown codes

    def test_vital_sign_no_value(self):
        """Test vital sign without value attribute."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <code code="8480-6" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = VitalSignRangeRule()
        issues = rule.validate(doc)
        assert len(issues) == 0  # Should skip observations without value

    def test_vital_sign_invalid_numeric_value(self):
        """Test vital sign with non-numeric value."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <code code="8480-6" displayName="Blood Pressure" />
                            <value value="not-a-number" />
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = VitalSignRangeRule()
        issues = rule.validate(doc)
        assert len(issues) == 0  # Should skip invalid numeric values


class TestAllergyStatusRule:
    """Test suite for AllergyStatusRule."""

    def test_valid_allergy_status(self):
        """Test allergy with valid status code."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <templateId root="2.16.840.1.113883.10.20.22.4.7" />
                            <entryRelationship>
                                <observation>
                                    <value code="55561003" />
                                </observation>
                            </entryRelationship>
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = AllergyStatusRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_invalid_allergy_status(self):
        """Test allergy with invalid status code."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <templateId root="2.16.840.1.113883.10.20.22.4.7" />
                            <entryRelationship>
                                <observation>
                                    <value code="99999999" />
                                </observation>
                            </entryRelationship>
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = AllergyStatusRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "invalid status" in issues[0].message.lower()


class TestProblemStatusRule:
    """Test suite for ProblemStatusRule."""

    def test_valid_problem_status(self):
        """Test problem with valid status code."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <templateId root="2.16.840.1.113883.10.20.22.4.4" />
                            <entryRelationship>
                                <observation>
                                    <value code="55561003" />
                                </observation>
                            </entryRelationship>
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = ProblemStatusRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_invalid_problem_status(self):
        """Test problem with invalid status code."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <component>
                <section>
                    <entry>
                        <observation>
                            <templateId root="2.16.840.1.113883.10.20.22.4.4" />
                            <entryRelationship>
                                <observation>
                                    <value code="99999999" />
                                </observation>
                            </entryRelationship>
                        </observation>
                    </entry>
                </section>
            </component>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = ProblemStatusRule()
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "invalid status" in issues[0].message.lower()


class TestContactInfoPresenceRule:
    """Test suite for ContactInfoPresenceRule."""

    def test_complete_contact_info(self):
        """Test patient with complete contact info."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <recordTarget>
                <patientRole>
                    <telecom value="tel:555-1234" />
                    <addr>
                        <streetAddressLine>123 Main St</streetAddressLine>
                    </addr>
                </patientRole>
            </recordTarget>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = ContactInfoPresenceRule()
        issues = rule.validate(doc)
        assert len(issues) == 0

    def test_missing_telecom(self):
        """Test when telecom is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <recordTarget>
                <patientRole>
                    <addr>
                        <streetAddressLine>123 Main St</streetAddressLine>
                    </addr>
                </patientRole>
            </recordTarget>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = ContactInfoPresenceRule(require_telecom=True)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "telecom" in issues[0].message.lower()

    def test_missing_address(self):
        """Test when address is missing."""
        xml = """<?xml version="1.0"?>
        <ClinicalDocument xmlns="urn:hl7-org:v3">
            <recordTarget>
                <patientRole>
                    <telecom value="tel:555-1234" />
                </patientRole>
            </recordTarget>
        </ClinicalDocument>"""
        doc = etree.fromstring(xml.encode("utf-8"))

        rule = ContactInfoPresenceRule(require_address=True)
        issues = rule.validate(doc)
        assert len(issues) == 1
        assert "address" in issues[0].message.lower()
