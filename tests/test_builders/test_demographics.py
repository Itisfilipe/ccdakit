"""Tests for demographic builders (Address, Telecom)."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.demographics import Address, Telecom


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockAddress:
    """Mock address for testing."""

    def __init__(
        self,
        street_lines=None,
        city="Boston",
        state="MA",
        postal_code="02101",
        country="US",
    ):
        self._street_lines = street_lines or ["123 Main St"]
        self._city = city
        self._state = state
        self._postal_code = postal_code
        self._country = country

    @property
    def street_lines(self) -> Sequence[str]:
        return self._street_lines

    @property
    def city(self) -> str:
        return self._city

    @property
    def state(self) -> str:
        return self._state

    @property
    def postal_code(self) -> str:
        return self._postal_code

    @property
    def country(self) -> str:
        return self._country


class MockTelecom:
    """Mock telecom for testing."""

    def __init__(self, type_="phone", value="617-555-1234", use=None):
        self._type = type_
        self._value = value
        self._use = use

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> str:
        return self._value

    @property
    def use(self) -> Optional[str]:
        return self._use


class TestAddress:
    """Tests for Address builder."""

    def test_address_basic(self):
        """Test basic address building."""
        addr_data = MockAddress()
        addr = Address(addr_data)
        elem = addr.to_element()

        assert local_name(elem) == "addr"
        street = elem.find(f"{{{NS}}}streetAddressLine")
        assert street is not None
        assert street.text == "123 Main St"

        city = elem.find(f"{{{NS}}}city")
        assert city is not None
        assert city.text == "Boston"

        state = elem.find(f"{{{NS}}}state")
        assert state is not None
        assert state.text == "MA"

        postal = elem.find(f"{{{NS}}}postalCode")
        assert postal is not None
        assert postal.text == "02101"

        country = elem.find(f"{{{NS}}}country")
        assert country is not None
        assert country.text == "US"

    def test_address_with_multiple_street_lines(self):
        """Test address with multiple street lines."""
        addr_data = MockAddress(street_lines=["123 Main St", "Apt 4B", "Suite 200"])
        addr = Address(addr_data)
        elem = addr.to_element()

        streets = elem.findall(f"{{{NS}}}streetAddressLine")
        assert len(streets) == 3
        assert streets[0].text == "123 Main St"
        assert streets[1].text == "Apt 4B"
        assert streets[2].text == "Suite 200"

    def test_address_with_use_home(self):
        """Test address with home use code."""
        addr_data = MockAddress()
        addr = Address(addr_data, use="home")
        elem = addr.to_element()

        assert elem.get("use") == "HP"

    def test_address_with_use_work(self):
        """Test address with work use code."""
        addr_data = MockAddress()
        addr = Address(addr_data, use="work")
        elem = addr.to_element()

        assert elem.get("use") == "WP"

    def test_address_with_direct_hl7_code(self):
        """Test address with direct HL7 use code."""
        addr_data = MockAddress()
        addr = Address(addr_data, use="TMP")
        elem = addr.to_element()

        assert elem.get("use") == "TMP"

    def test_address_without_use(self):
        """Test address without use attribute."""
        addr_data = MockAddress()
        addr = Address(addr_data)
        elem = addr.to_element()

        assert elem.get("use") is None

    def test_address_to_string(self):
        """Test address serialization to string."""
        addr_data = MockAddress()
        addr = Address(addr_data)
        xml = addr.to_string(pretty=False)

        assert "<addr>" in xml or ":addr>" in xml  # May have namespace prefix
        assert "123 Main St" in xml
        assert "Boston" in xml
        assert "MA" in xml

    def test_address_structure_order(self):
        """Test that address elements are in correct order."""
        addr_data = MockAddress(street_lines=["Line 1", "Line 2"])
        addr = Address(addr_data)
        elem = addr.to_element()

        # Check order of child elements
        children = list(elem)
        assert local_name(children[0]) == "streetAddressLine"
        assert local_name(children[1]) == "streetAddressLine"
        assert local_name(children[2]) == "city"
        assert local_name(children[3]) == "state"
        assert local_name(children[4]) == "postalCode"
        assert local_name(children[5]) == "country"


class TestTelecom:
    """Tests for Telecom builder."""

    def test_telecom_phone(self):
        """Test telecom with phone number."""
        tel_data = MockTelecom(type_="phone", value="617-555-1234")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert local_name(elem) == "telecom"
        assert elem.get("value") == "tel:617-555-1234"

    def test_telecom_phone_with_use_home(self):
        """Test phone with home use code."""
        tel_data = MockTelecom(type_="phone", value="617-555-1234", use="home")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("value") == "tel:617-555-1234"
        assert elem.get("use") == "HP"

    def test_telecom_phone_with_use_work(self):
        """Test phone with work use code."""
        tel_data = MockTelecom(type_="phone", value="617-555-5678", use="work")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("value") == "tel:617-555-5678"
        assert elem.get("use") == "WP"

    def test_telecom_phone_with_use_mobile(self):
        """Test phone with mobile use code."""
        tel_data = MockTelecom(type_="phone", value="617-555-9999", use="mobile")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("use") == "MC"

    def test_telecom_email(self):
        """Test telecom with email address."""
        tel_data = MockTelecom(type_="email", value="john@example.com")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("value") == "mailto:john@example.com"

    def test_telecom_email_with_use(self):
        """Test email with use code."""
        tel_data = MockTelecom(type_="email", value="work@example.com", use="work")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("value") == "mailto:work@example.com"
        assert elem.get("use") == "WP"

    def test_telecom_fax(self):
        """Test telecom with fax number."""
        tel_data = MockTelecom(type_="fax", value="617-555-1235")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("value") == "tel:617-555-1235"

    def test_telecom_url_with_protocol(self):
        """Test telecom with URL including protocol."""
        tel_data = MockTelecom(type_="url", value="https://example.com")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("value") == "https://example.com"

    def test_telecom_url_without_protocol(self):
        """Test telecom with URL without protocol."""
        tel_data = MockTelecom(type_="url", value="example.com")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("value") == "http://example.com"

    def test_telecom_without_use(self):
        """Test telecom without use attribute."""
        tel_data = MockTelecom(type_="phone", value="617-555-1234")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("use") is None

    def test_telecom_with_direct_hl7_code(self):
        """Test telecom with direct HL7 use code."""
        tel_data = MockTelecom(type_="phone", value="617-555-1234", use="EC")
        tel = Telecom(tel_data)
        elem = tel.to_element()

        assert elem.get("use") == "EC"

    def test_telecom_to_string(self):
        """Test telecom serialization to string."""
        tel_data = MockTelecom(type_="phone", value="617-555-1234", use="home")
        tel = Telecom(tel_data)
        xml = tel.to_string(pretty=False)

        assert "<telecom" in xml or ":telecom" in xml  # May have namespace prefix
        assert "tel:617-555-1234" in xml
        assert "HP" in xml

    def test_telecom_case_insensitive_type(self):
        """Test that telecom type is case insensitive."""
        tel_data_upper = MockTelecom(type_="PHONE", value="617-555-1234")
        tel_data_mixed = MockTelecom(type_="Phone", value="617-555-1234")

        tel_upper = Telecom(tel_data_upper)
        tel_mixed = Telecom(tel_data_mixed)

        assert tel_upper.to_element().get("value") == "tel:617-555-1234"
        assert tel_mixed.to_element().get("value") == "tel:617-555-1234"


class TestDemographicsIntegration:
    """Integration tests for demographic builders."""

    def test_multiple_addresses(self):
        """Test building multiple addresses."""
        home_addr = MockAddress(city="Boston", state="MA")
        work_addr = MockAddress(city="Cambridge", state="MA")

        home = Address(home_addr, use="home")
        work = Address(work_addr, use="work")

        home_elem = home.to_element()
        work_elem = work.to_element()

        assert home_elem.get("use") == "HP"
        assert home_elem.find(f"{{{NS}}}city").text == "Boston"

        assert work_elem.get("use") == "WP"
        assert work_elem.find(f"{{{NS}}}city").text == "Cambridge"

    def test_multiple_telecoms(self):
        """Test building multiple telecom entries."""
        phone = MockTelecom(type_="phone", value="617-555-1234", use="home")
        email = MockTelecom(type_="email", value="john@example.com", use="work")

        phone_builder = Telecom(phone)
        email_builder = Telecom(email)

        phone_elem = phone_builder.to_element()
        email_elem = email_builder.to_element()

        assert phone_elem.get("value") == "tel:617-555-1234"
        assert phone_elem.get("use") == "HP"

        assert email_elem.get("value") == "mailto:john@example.com"
        assert email_elem.get("use") == "WP"

    def test_compose_in_parent_element(self):
        """Test composing addresses and telecoms in parent element."""
        parent = etree.Element(f"{{{NS}}}patient")

        # Add address
        addr_data = MockAddress()
        addr = Address(addr_data, use="home")
        parent.append(addr.to_element())

        # Add telecoms
        phone_data = MockTelecom(type_="phone", value="617-555-1234", use="home")
        email_data = MockTelecom(type_="email", value="john@example.com")

        phone = Telecom(phone_data)
        email = Telecom(email_data)

        parent.append(phone.to_element())
        parent.append(email.to_element())

        # Verify structure
        assert parent.find(f"{{{NS}}}addr") is not None
        telecoms = parent.findall(f"{{{NS}}}telecom")
        assert len(telecoms) == 2
