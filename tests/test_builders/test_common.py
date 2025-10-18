"""Tests for common builders."""

from datetime import date, datetime

import pytest
from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class TestCode:
    """Tests for Code builder."""

    def test_code_with_named_system(self):
        """Test code with named code system."""
        code = Code(code="11450-4", system="LOINC", display_name="Problem List")
        elem = code.to_element()

        assert local_name(elem) == "code"
        assert elem.get("code") == "11450-4"
        assert elem.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert elem.get("codeSystemName") == "LOINC"
        assert elem.get("displayName") == "Problem List"

    def test_code_with_oid_system(self):
        """Test code with OID code system."""
        code = Code(code="12345", system="2.16.840.1.113883.3.CUSTOM", display_name="Custom")
        elem = code.to_element()

        assert elem.get("code") == "12345"
        assert elem.get("codeSystem") == "2.16.840.1.113883.3.CUSTOM"
        assert elem.get("codeSystemName") is None

    def test_code_without_display_name(self):
        """Test code without display name."""
        code = Code(code="44054006", system="SNOMED")
        elem = code.to_element()

        assert elem.get("code") == "44054006"
        assert elem.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert elem.get("displayName") is None

    def test_code_with_null_flavor(self):
        """Test code with null flavor."""
        code = Code(null_flavor="UNK")
        elem = code.to_element()

        assert elem.get("nullFlavor") == "UNK"
        assert elem.get("code") is None

    def test_code_missing_required_fields(self):
        """Test code raises error when required fields missing."""
        code = Code(code="12345")  # Missing system

        with pytest.raises(ValueError, match="code and system required"):
            code.to_element()

    def test_code_snomed_system(self):
        """Test code with SNOMED system."""
        code = Code(code="38341003", system="SNOMED", display_name="Hypertension")
        elem = code.to_element()

        assert elem.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert elem.get("codeSystemName") == "SNOMED"

    def test_code_icd10_system(self):
        """Test code with ICD-10 system."""
        code = Code(code="E11.9", system="ICD-10", display_name="Type 2 Diabetes")
        elem = code.to_element()

        assert elem.get("codeSystem") == "2.16.840.1.113883.6.90"
        assert elem.get("codeSystemName") == "ICD-10"

    def test_code_rxnorm_system(self):
        """Test code with RxNorm system."""
        code = Code(code="313782", system="RxNorm", display_name="Metformin")
        elem = code.to_element()

        assert elem.get("codeSystem") == "2.16.840.1.113883.6.88"

    def test_code_to_string(self):
        """Test code serialization to string."""
        code = Code(code="11450-4", system="LOINC")
        xml = code.to_string(pretty=False)

        assert ":code" in xml or "<code" in xml  # May have namespace prefix
        assert "11450-4" in xml
        assert "2.16.840.1.113883.6.1" in xml


class TestEffectiveTime:
    """Tests for EffectiveTime builder."""

    def test_effective_time_point(self):
        """Test effectiveTime with point in time."""
        dt = datetime(2023, 10, 17, 14, 30, 0)
        etime = EffectiveTime(value=dt)
        elem = etime.to_element()

        assert local_name(elem) == "effectiveTime"
        assert elem.get("value") == "20231017143000"

    def test_effective_time_date_only(self):
        """Test effectiveTime with date only."""
        d = date(2023, 10, 17)
        etime = EffectiveTime(value=d)
        elem = etime.to_element()

        assert elem.get("value") == "20231017"

    def test_effective_time_interval_with_both(self):
        """Test effectiveTime interval with both low and high."""
        low = date(2020, 1, 1)
        high = date(2023, 1, 1)
        etime = EffectiveTime(low=low, high=high)
        elem = etime.to_element()

        low_elem = elem.find(f"{{{NS}}}low")
        high_elem = elem.find(f"{{{NS}}}high")

        assert low_elem is not None
        assert low_elem.get("value") == "20200101"
        assert high_elem is not None
        assert high_elem.get("value") == "20230101"

    def test_effective_time_interval_ongoing(self):
        """Test effectiveTime interval for ongoing (no high)."""
        low = date(2020, 1, 1)
        etime = EffectiveTime(low=low)
        elem = etime.to_element()

        low_elem = elem.find(f"{{{NS}}}low")
        high_elem = elem.find(f"{{{NS}}}high")

        assert low_elem is not None
        assert low_elem.get("value") == "20200101"
        assert high_elem is not None
        assert high_elem.get("nullFlavor") == "UNK"

    def test_effective_time_with_null_flavor(self):
        """Test effectiveTime with null flavor."""
        etime = EffectiveTime(null_flavor="UNK")
        elem = etime.to_element()

        assert elem.get("nullFlavor") == "UNK"
        assert elem.find(f"{{{NS}}}low") is None
        assert elem.find(f"{{{NS}}}high") is None

    def test_effective_time_datetime_precision(self):
        """Test effectiveTime preserves datetime precision."""
        dt = datetime(2023, 12, 25, 15, 45, 30)
        etime = EffectiveTime(value=dt)
        elem = etime.to_element()

        assert elem.get("value") == "20231225154530"

    def test_effective_time_to_string(self):
        """Test effectiveTime serialization to string."""
        dt = date(2023, 10, 17)
        etime = EffectiveTime(value=dt)
        xml = etime.to_string(pretty=False)

        assert ":effectiveTime" in xml or "<effectiveTime" in xml  # May have namespace prefix
        assert "20231017" in xml


class TestIdentifier:
    """Tests for Identifier builder."""

    def test_identifier_with_extension(self):
        """Test identifier with root and extension."""
        ident = Identifier(root="2.16.840.1.113883.3.TEST", extension="12345")
        elem = ident.to_element()

        assert local_name(elem) == "id"
        assert elem.get("root") == "2.16.840.1.113883.3.TEST"
        assert elem.get("extension") == "12345"

    def test_identifier_without_extension(self):
        """Test identifier with only root."""
        ident = Identifier(root="2.16.840.1.113883.3.TEST")
        elem = ident.to_element()

        assert elem.get("root") == "2.16.840.1.113883.3.TEST"
        assert elem.get("extension") is None

    def test_identifier_with_null_flavor(self):
        """Test identifier with null flavor."""
        ident = Identifier(root="", null_flavor="NI")
        elem = ident.to_element()

        assert elem.get("nullFlavor") == "NI"
        assert elem.get("root") is None

    def test_identifier_uuid(self):
        """Test identifier with UUID."""
        uuid = "550e8400-e29b-41d4-a716-446655440000"
        ident = Identifier(root=uuid)
        elem = ident.to_element()

        assert elem.get("root") == uuid

    def test_identifier_to_string(self):
        """Test identifier serialization to string."""
        ident = Identifier(root="2.16.840.1.113883.3.TEST", extension="ABC123")
        xml = ident.to_string(pretty=False)

        assert ":id" in xml or "<id" in xml  # May have namespace prefix
        assert "2.16.840.1.113883.3.TEST" in xml
        assert "ABC123" in xml


class TestStatusCode:
    """Tests for StatusCode builder."""

    def test_status_code_completed(self):
        """Test statusCode with completed status."""
        status = StatusCode("completed")
        elem = status.to_element()

        assert local_name(elem) == "statusCode"
        assert elem.get("code") == "completed"

    def test_status_code_active(self):
        """Test statusCode with active status."""
        status = StatusCode("active")
        elem = status.to_element()

        assert elem.get("code") == "active"

    def test_status_code_to_string(self):
        """Test statusCode serialization to string."""
        status = StatusCode("completed")
        xml = status.to_string(pretty=False)

        assert ":statusCode" in xml or "<statusCode" in xml  # May have namespace prefix
        assert 'code="completed"' in xml


class TestCommonBuildersIntegration:
    """Integration tests for common builders."""

    def test_builders_with_version(self):
        """Test builders work with different CDA versions."""
        code_r21 = Code(code="11450-4", system="LOINC", version=CDAVersion.R2_1)
        code_r20 = Code(code="11450-4", system="LOINC", version=CDAVersion.R2_0)

        elem_r21 = code_r21.to_element()
        elem_r20 = code_r20.to_element()

        # Both should produce same output for Code (no version-specific logic)
        assert elem_r21.get("code") == elem_r20.get("code")

    def test_builders_compose_together(self):
        """Test that builders can be composed together."""
        # Create a mock observation structure
        observation = etree.Element("observation")

        # Add various common elements
        code = Code(code="55607006", system="SNOMED", display_name="Problem")
        observation.append(code.to_element())

        status = StatusCode("completed")
        observation.append(status.to_element())

        etime = EffectiveTime(low=date(2020, 1, 1))
        observation.append(etime.to_element())

        ident = Identifier(root="2.16.840.1.113883.3.TEST", extension="OBS-1")
        observation.append(ident.to_element())

        # Verify structure
        assert len(observation) == 4
        assert observation.find(f"{{{NS}}}code") is not None
        assert observation.find(f"{{{NS}}}statusCode") is not None
        assert observation.find(f"{{{NS}}}effectiveTime") is not None
        assert observation.find(f"{{{NS}}}id") is not None

    def test_null_flavor_consistency(self):
        """Test null flavor handling is consistent across builders."""
        code = Code(null_flavor="UNK")
        etime = EffectiveTime(null_flavor="UNK")
        ident = Identifier(root="", null_flavor="UNK")

        assert code.to_element().get("nullFlavor") == "UNK"
        assert etime.to_element().get("nullFlavor") == "UNK"
        assert ident.to_element().get("nullFlavor") == "UNK"
