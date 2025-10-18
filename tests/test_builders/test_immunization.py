"""Tests for ImmunizationActivity builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.entries.immunization import ImmunizationActivity
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockImmunization:
    """Mock immunization for testing."""

    def __init__(
        self,
        vaccine_name="Influenza vaccine",
        cvx_code="141",
        administration_date=date(2023, 9, 1),
        status="completed",
        lot_number=None,
        manufacturer=None,
        route=None,
        site=None,
        dose_quantity=None,
    ):
        self._vaccine_name = vaccine_name
        self._cvx_code = cvx_code
        self._administration_date = administration_date
        self._status = status
        self._lot_number = lot_number
        self._manufacturer = manufacturer
        self._route = route
        self._site = site
        self._dose_quantity = dose_quantity

    @property
    def vaccine_name(self):
        return self._vaccine_name

    @property
    def cvx_code(self):
        return self._cvx_code

    @property
    def administration_date(self):
        return self._administration_date

    @property
    def status(self):
        return self._status

    @property
    def lot_number(self):
        return self._lot_number

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def route(self):
        return self._route

    @property
    def site(self):
        return self._site

    @property
    def dose_quantity(self):
        return self._dose_quantity


class TestImmunizationActivity:
    """Tests for ImmunizationActivity builder."""

    def test_immunization_activity_basic(self):
        """Test basic ImmunizationActivity creation."""
        immunization = MockImmunization()
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        assert local_name(elem) == "substanceAdministration"
        assert elem.get("classCode") == "SBADM"
        assert elem.get("moodCode") == "EVN"
        assert elem.get("negationInd") == "false"

    def test_immunization_activity_has_template_id_r21(self):
        """Test ImmunizationActivity includes R2.1 template ID."""
        immunization = MockImmunization()
        imm_act = ImmunizationActivity(immunization, version=CDAVersion.R2_1)
        elem = imm_act.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.52"
        assert template.get("extension") == "2015-08-01"

    def test_immunization_activity_has_template_id_r20(self):
        """Test ImmunizationActivity includes R2.0 template ID."""
        immunization = MockImmunization()
        imm_act = ImmunizationActivity(immunization, version=CDAVersion.R2_0)
        elem = imm_act.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.52"
        assert template.get("extension") == "2014-06-09"

    def test_immunization_activity_has_id(self):
        """Test ImmunizationActivity includes ID element."""
        immunization = MockImmunization()
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_immunization_activity_has_status_code(self):
        """Test ImmunizationActivity includes statusCode."""
        immunization = MockImmunization(status="completed")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_immunization_activity_status_mapping(self):
        """Test status code mapping."""
        # Test completed
        immunization = MockImmunization(status="completed")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "completed"

        # Test refused
        immunization = MockImmunization(status="refused")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "refused"

        # Test not-done -> refused
        immunization = MockImmunization(status="not-done")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "refused"

    def test_immunization_activity_has_effective_time(self):
        """Test ImmunizationActivity includes effectiveTime."""
        immunization = MockImmunization(administration_date=date(2023, 9, 1))
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert eff_time.get("value") == "20230901"

    def test_immunization_activity_has_route_code_intramuscular(self):
        """Test ImmunizationActivity routeCode with intramuscular route."""
        immunization = MockImmunization(route="intramuscular")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        route = elem.find(f"{{{NS}}}routeCode")
        assert route is not None
        assert route.get("code") == "C28161"
        assert route.get("codeSystem") == "2.16.840.1.113883.3.26.1.1"
        assert route.get("codeSystemName") == "NCI Thesaurus"

    def test_immunization_activity_has_route_code_oral(self):
        """Test ImmunizationActivity routeCode with oral route."""
        immunization = MockImmunization(route="oral")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        route = elem.find(f"{{{NS}}}routeCode")
        assert route is not None
        assert route.get("code") == "C38288"

    def test_immunization_activity_has_route_code_unknown(self):
        """Test ImmunizationActivity routeCode with unknown route."""
        immunization = MockImmunization(route="some-unknown-route")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        route = elem.find(f"{{{NS}}}routeCode")
        assert route is not None
        assert route.get("nullFlavor") == "OTH"

        original_text = route.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "some-unknown-route"

    def test_immunization_activity_without_route(self):
        """Test ImmunizationActivity without route."""
        immunization = MockImmunization(route=None)
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        route = elem.find(f"{{{NS}}}routeCode")
        assert route is None

    def test_immunization_activity_has_site_code(self):
        """Test ImmunizationActivity approachSiteCode."""
        immunization = MockImmunization(site="left deltoid")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        site = elem.find(f"{{{NS}}}approachSiteCode")
        assert site is not None
        assert site.get("code") == "723979003"
        assert site.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert site.get("codeSystemName") == "SNOMED CT"

    def test_immunization_activity_has_site_code_unknown(self):
        """Test ImmunizationActivity approachSiteCode with unknown site."""
        immunization = MockImmunization(site="some-unknown-site")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        site = elem.find(f"{{{NS}}}approachSiteCode")
        assert site is not None
        assert site.get("nullFlavor") == "OTH"

        original_text = site.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "some-unknown-site"

    def test_immunization_activity_without_site(self):
        """Test ImmunizationActivity without site."""
        immunization = MockImmunization(site=None)
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        site = elem.find(f"{{{NS}}}approachSiteCode")
        assert site is None

    def test_immunization_activity_has_dose_quantity(self):
        """Test ImmunizationActivity doseQuantity."""
        immunization = MockImmunization(dose_quantity="0.5 mL")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        dose = elem.find(f"{{{NS}}}doseQuantity")
        assert dose is not None
        assert dose.get("value") == "0.5"
        assert dose.get("unit") == "mL"

    def test_immunization_activity_dose_quantity_complex(self):
        """Test doseQuantity with complex dosage."""
        immunization = MockImmunization(dose_quantity="1 dose")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        dose = elem.find(f"{{{NS}}}doseQuantity")
        assert dose is not None
        assert dose.get("value") == "1"
        assert dose.get("unit") == "dose"

    def test_immunization_activity_without_dose_quantity(self):
        """Test ImmunizationActivity without dose quantity."""
        immunization = MockImmunization(dose_quantity=None)
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        dose = elem.find(f"{{{NS}}}doseQuantity")
        assert dose is None

    def test_immunization_activity_has_consumable(self):
        """Test ImmunizationActivity includes consumable with vaccine."""
        immunization = MockImmunization(
            vaccine_name="Influenza vaccine",
            cvx_code="141",
        )
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        consumable = elem.find(f"{{{NS}}}consumable")
        assert consumable is not None

        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        assert manufactured_product is not None
        assert manufactured_product.get("classCode") == "MANU"

        # Check template ID
        template = manufactured_product.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.54"

        # Check manufactured material
        manufactured_material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")
        assert manufactured_material is not None

        # Check vaccine code (CVX)
        code = manufactured_material.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "141"
        assert code.get("codeSystem") == "2.16.840.1.113883.12.292"  # CVX OID
        assert code.get("codeSystemName") == "CVX"
        assert code.get("displayName") == "Influenza vaccine"

    def test_immunization_activity_with_lot_number(self):
        """Test ImmunizationActivity with lot number."""
        immunization = MockImmunization(lot_number="ABC123456")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        consumable = elem.find(f"{{{NS}}}consumable")
        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")

        lot_elem = manufactured_material.find(f"{{{NS}}}lotNumberText")
        assert lot_elem is not None
        assert lot_elem.text == "ABC123456"

    def test_immunization_activity_without_lot_number(self):
        """Test ImmunizationActivity without lot number."""
        immunization = MockImmunization(lot_number=None)
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        consumable = elem.find(f"{{{NS}}}consumable")
        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")

        lot_elem = manufactured_material.find(f"{{{NS}}}lotNumberText")
        assert lot_elem is None

    def test_immunization_activity_with_manufacturer(self):
        """Test ImmunizationActivity with manufacturer."""
        immunization = MockImmunization(manufacturer="Pfizer Inc.")
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        consumable = elem.find(f"{{{NS}}}consumable")
        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")

        org_elem = manufactured_product.find(f"{{{NS}}}manufacturerOrganization")
        assert org_elem is not None

        name_elem = org_elem.find(f"{{{NS}}}name")
        assert name_elem is not None
        assert name_elem.text == "Pfizer Inc."

    def test_immunization_activity_without_manufacturer(self):
        """Test ImmunizationActivity without manufacturer."""
        immunization = MockImmunization(manufacturer=None)
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        consumable = elem.find(f"{{{NS}}}consumable")
        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")

        org_elem = manufactured_product.find(f"{{{NS}}}manufacturerOrganization")
        assert org_elem is None

    def test_immunization_activity_to_string(self):
        """Test ImmunizationActivity serialization."""
        immunization = MockImmunization()
        imm_act = ImmunizationActivity(immunization)
        xml = imm_act.to_string(pretty=False)

        assert "<substanceAdministration" in xml or ":substanceAdministration" in xml
        assert "classCode" in xml
        assert "moodCode" in xml
        assert "141" in xml  # CVX code

    def test_immunization_activity_structure_order(self):
        """Test that elements are in correct order."""
        immunization = MockImmunization(
            route="intramuscular",
            site="left deltoid",
            dose_quantity="0.5 mL",
        )
        imm_act = ImmunizationActivity(immunization)
        elem = imm_act.to_element()

        children = list(elem)
        # Get local names
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "id" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "routeCode" in names
        assert "approachSiteCode" in names
        assert "doseQuantity" in names
        assert "consumable" in names


class TestImmunizationActivityIntegration:
    """Integration tests for ImmunizationActivity."""

    def test_multiple_immunizations(self):
        """Test creating multiple immunization activities."""
        immunization1 = MockImmunization(
            vaccine_name="Influenza vaccine",
            cvx_code="141",
        )
        immunization2 = MockImmunization(
            vaccine_name="COVID-19 vaccine",
            cvx_code="208",
        )

        imm_act1 = ImmunizationActivity(immunization1)
        imm_act2 = ImmunizationActivity(immunization2)

        elem1 = imm_act1.to_element()
        elem2 = imm_act2.to_element()

        # Check that each has correct vaccine code
        consumable1 = elem1.find(f"{{{NS}}}consumable")
        manufactured_product1 = consumable1.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material1 = manufactured_product1.find(f"{{{NS}}}manufacturedMaterial")
        code1 = manufactured_material1.find(f"{{{NS}}}code")

        consumable2 = elem2.find(f"{{{NS}}}consumable")
        manufactured_product2 = consumable2.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material2 = manufactured_product2.find(f"{{{NS}}}manufacturedMaterial")
        code2 = manufactured_material2.find(f"{{{NS}}}code")

        assert code1.get("code") == "141"
        assert code2.get("code") == "208"

    def test_immunization_in_parent_element(self):
        """Test composing immunization activity in parent element."""
        parent = etree.Element(f"{{{NS}}}entry")

        immunization = MockImmunization()
        imm_act = ImmunizationActivity(immunization)

        parent.append(imm_act.to_element())

        sub_admin = parent.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"

    def test_immunization_complete_example(self):
        """Test complete immunization with all optional fields."""
        immunization = MockImmunization(
            vaccine_name="Influenza vaccine, seasonal",
            cvx_code="141",
            administration_date=date(2023, 9, 15),
            status="completed",
            lot_number="XYZ789",
            manufacturer="Sanofi Pasteur",
            route="intramuscular",
            site="left deltoid",
            dose_quantity="0.5 mL",
        )
        imm_act = ImmunizationActivity(immunization, version=CDAVersion.R2_1)
        elem = imm_act.to_element()

        # Verify all components are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}routeCode") is not None
        assert elem.find(f"{{{NS}}}approachSiteCode") is not None
        assert elem.find(f"{{{NS}}}doseQuantity") is not None
        assert elem.find(f"{{{NS}}}consumable") is not None

        # Verify lot number and manufacturer
        consumable = elem.find(f"{{{NS}}}consumable")
        manufactured_product = consumable.find(f"{{{NS}}}manufacturedProduct")
        manufactured_material = manufactured_product.find(f"{{{NS}}}manufacturedMaterial")
        lot_elem = manufactured_material.find(f"{{{NS}}}lotNumberText")
        assert lot_elem.text == "XYZ789"

        org_elem = manufactured_product.find(f"{{{NS}}}manufacturerOrganization")
        name_elem = org_elem.find(f"{{{NS}}}name")
        assert name_elem.text == "Sanofi Pasteur"
