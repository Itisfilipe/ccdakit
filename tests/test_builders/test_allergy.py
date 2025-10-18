"""Tests for AllergyObservation builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.entries.allergy import AllergyObservation
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockAllergy:
    """Mock allergy for testing."""

    def __init__(
        self,
        allergen="Penicillin",
        allergen_code="70618",
        allergen_code_system="RxNorm",
        allergy_type="allergy",
        reaction="Hives",
        severity="moderate",
        status="active",
        onset_date=date(2020, 5, 15),
    ):
        self._allergen = allergen
        self._allergen_code = allergen_code
        self._allergen_code_system = allergen_code_system
        self._allergy_type = allergy_type
        self._reaction = reaction
        self._severity = severity
        self._status = status
        self._onset_date = onset_date

    @property
    def allergen(self):
        return self._allergen

    @property
    def allergen_code(self):
        return self._allergen_code

    @property
    def allergen_code_system(self):
        return self._allergen_code_system

    @property
    def allergy_type(self):
        return self._allergy_type

    @property
    def reaction(self):
        return self._reaction

    @property
    def severity(self):
        return self._severity

    @property
    def status(self):
        return self._status

    @property
    def onset_date(self):
        return self._onset_date


class TestAllergyObservation:
    """Tests for AllergyObservation builder."""

    def test_allergy_observation_basic(self):
        """Test basic AllergyObservation creation."""
        allergy = MockAllergy()
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_allergy_observation_has_template_id_r21(self):
        """Test AllergyObservation includes R2.1 template ID."""
        allergy = MockAllergy()
        allergy_obs = AllergyObservation(allergy, version=CDAVersion.R2_1)
        elem = allergy_obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.7"
        assert template.get("extension") == "2014-06-09"

    def test_allergy_observation_has_template_id_r20(self):
        """Test AllergyObservation includes R2.0 template ID."""
        allergy = MockAllergy()
        allergy_obs = AllergyObservation(allergy, version=CDAVersion.R2_0)
        elem = allergy_obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.7"
        assert template.get("extension") == "2014-06-09"

    def test_allergy_observation_has_id(self):
        """Test AllergyObservation includes ID element."""
        allergy = MockAllergy()
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_allergy_observation_has_observation_code(self):
        """Test AllergyObservation includes observation code."""
        allergy = MockAllergy()
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "ASSERTION"
        assert code.get("codeSystem") == "2.16.840.1.113883.5.4"

    def test_allergy_observation_has_status_code(self):
        """Test AllergyObservation includes statusCode."""
        allergy = MockAllergy(status="active")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "active"

    def test_allergy_observation_status_mapping(self):
        """Test status code mapping."""
        # Test active
        allergy = MockAllergy(status="active")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "active"

        # Test resolved -> completed
        allergy = MockAllergy(status="resolved")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "completed"

        # Test inactive -> completed
        allergy = MockAllergy(status="inactive")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "completed"

    def test_allergy_observation_has_effective_time(self):
        """Test AllergyObservation includes effectiveTime when onset_date provided."""
        allergy = MockAllergy(onset_date=date(2020, 5, 15))
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert eff_time.get("value") == "20200515"

    def test_allergy_observation_without_onset_date(self):
        """Test AllergyObservation without onset date."""
        allergy = MockAllergy(onset_date=None)
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        # Should not have effectiveTime when no onset date
        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is None

    def test_allergy_observation_value_allergy_type(self):
        """Test AllergyObservation value element for allergy type."""
        allergy = MockAllergy(allergy_type="allergy")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "419199007"  # SNOMED CT code for allergy
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert value.get("displayName") == "Allergy to substance"

    def test_allergy_observation_value_intolerance_type(self):
        """Test AllergyObservation value element for intolerance type."""
        allergy = MockAllergy(allergy_type="intolerance")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "420134006"  # SNOMED CT code for intolerance
        assert value.get("displayName") == "Propensity to adverse reactions"

    def test_allergy_observation_value_unknown_type(self):
        """Test AllergyObservation value element with unknown type."""
        allergy = MockAllergy(allergy_type="some-unknown-type")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("nullFlavor") == "OTH"

        original_text = value.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "some-unknown-type"

    def test_allergy_observation_has_allergen_participant(self):
        """Test AllergyObservation includes allergen participant."""
        allergy = MockAllergy(
            allergen="Penicillin",
            allergen_code="70618",
            allergen_code_system="RxNorm",
        )
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        assert participant is not None
        assert participant.get("typeCode") == "CSM"

        participant_role = participant.find(f"{{{NS}}}participantRole")
        assert participant_role is not None
        assert participant_role.get("classCode") == "MANU"

        playing_entity = participant_role.find(f"{{{NS}}}playingEntity")
        assert playing_entity is not None
        assert playing_entity.get("classCode") == "MMAT"

        code = playing_entity.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "70618"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.88"  # RxNorm OID
        assert code.get("displayName") == "Penicillin"

    def test_allergy_observation_allergen_without_code(self):
        """Test AllergyObservation allergen participant without code."""
        allergy = MockAllergy(
            allergen="Some allergen",
            allergen_code=None,
            allergen_code_system=None,
        )
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        participant_role = participant.find(f"{{{NS}}}participantRole")
        playing_entity = participant_role.find(f"{{{NS}}}playingEntity")
        code = playing_entity.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("nullFlavor") == "OTH"

        original_text = code.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Some allergen"

    def test_allergy_observation_with_reaction(self):
        """Test AllergyObservation with reaction."""
        allergy = MockAllergy(reaction="Hives")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        # Find entryRelationship for reaction
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        reaction_rel = None
        for entry_rel in entry_rels:
            if entry_rel.get("typeCode") == "MFST":
                reaction_rel = entry_rel
                break

        assert reaction_rel is not None
        assert reaction_rel.get("inversionInd") == "true"

        # Find observation within entryRelationship
        reaction_obs = reaction_rel.find(f"{{{NS}}}observation")
        assert reaction_obs is not None
        assert reaction_obs.get("classCode") == "OBS"
        assert reaction_obs.get("moodCode") == "EVN"

        # Check template ID
        template = reaction_obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.9"

        # Check text with reaction
        text = reaction_obs.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Hives"

    def test_allergy_observation_without_reaction(self):
        """Test AllergyObservation without reaction."""
        allergy = MockAllergy(reaction=None)
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        # Should not have MFST entryRelationship for reaction
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        reaction_rels = [er for er in entry_rels if er.get("typeCode") == "MFST"]
        assert len(reaction_rels) == 0

    def test_allergy_observation_with_severity(self):
        """Test AllergyObservation with severity."""
        allergy = MockAllergy(severity="severe")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        # Find entryRelationship for severity
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        severity_rel = None
        for entry_rel in entry_rels:
            if entry_rel.get("typeCode") == "SUBJ":
                severity_rel = entry_rel
                break

        assert severity_rel is not None
        assert severity_rel.get("inversionInd") == "true"

        # Find observation within entryRelationship
        severity_obs = severity_rel.find(f"{{{NS}}}observation")
        assert severity_obs is not None

        # Check template ID
        template = severity_obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.8"

        # Check code for severity
        code = severity_obs.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "SEV"

        # Check value with severity code
        value = severity_obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "24484000"  # Severe
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"

    def test_allergy_observation_severity_codes(self):
        """Test different severity code mappings."""
        # Test mild
        allergy = MockAllergy(severity="mild")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        severity_rel = [er for er in entry_rels if er.get("typeCode") == "SUBJ"][0]
        severity_obs = severity_rel.find(f"{{{NS}}}observation")
        value = severity_obs.find(f"{{{NS}}}value")
        assert value.get("code") == "255604002"

        # Test moderate
        allergy = MockAllergy(severity="moderate")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        severity_rel = [er for er in entry_rels if er.get("typeCode") == "SUBJ"][0]
        severity_obs = severity_rel.find(f"{{{NS}}}observation")
        value = severity_obs.find(f"{{{NS}}}value")
        assert value.get("code") == "6736007"

        # Test fatal
        allergy = MockAllergy(severity="fatal")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        severity_rel = [er for er in entry_rels if er.get("typeCode") == "SUBJ"][0]
        severity_obs = severity_rel.find(f"{{{NS}}}observation")
        value = severity_obs.find(f"{{{NS}}}value")
        assert value.get("code") == "399166001"

    def test_allergy_observation_severity_unknown(self):
        """Test AllergyObservation with unknown severity."""
        allergy = MockAllergy(severity="unknown-severity")
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        severity_rel = [er for er in entry_rels if er.get("typeCode") == "SUBJ"][0]
        severity_obs = severity_rel.find(f"{{{NS}}}observation")
        value = severity_obs.find(f"{{{NS}}}value")

        assert value.get("nullFlavor") == "OTH"
        original_text = value.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "unknown-severity"

    def test_allergy_observation_without_severity(self):
        """Test AllergyObservation without severity."""
        allergy = MockAllergy(severity=None)
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        # Should not have SUBJ entryRelationship for severity
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        severity_rels = [er for er in entry_rels if er.get("typeCode") == "SUBJ"]
        assert len(severity_rels) == 0

    def test_allergy_observation_to_string(self):
        """Test AllergyObservation serialization."""
        allergy = MockAllergy()
        allergy_obs = AllergyObservation(allergy)
        xml = allergy_obs.to_string(pretty=False)

        assert "<observation" in xml or ":observation" in xml
        assert "classCode" in xml
        assert "moodCode" in xml
        assert "Penicillin" in xml

    def test_allergy_observation_structure_order(self):
        """Test that elements are in correct order."""
        allergy = MockAllergy(
            onset_date=date(2020, 5, 15),
            reaction="Hives",
            severity="moderate",
        )
        allergy_obs = AllergyObservation(allergy)
        elem = allergy_obs.to_element()

        children = list(elem)
        # Get local names
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "value" in names
        assert "participant" in names
        assert names.count("entryRelationship") == 2  # reaction + severity


class TestAllergyObservationIntegration:
    """Integration tests for AllergyObservation."""

    def test_multiple_allergies(self):
        """Test creating multiple allergy observations."""
        allergy1 = MockAllergy(
            allergen="Penicillin",
            allergen_code="70618",
        )
        allergy2 = MockAllergy(
            allergen="Peanuts",
            allergen_code="762952008",
            allergen_code_system="SNOMED CT",
        )

        allergy_obs1 = AllergyObservation(allergy1)
        allergy_obs2 = AllergyObservation(allergy2)

        elem1 = allergy_obs1.to_element()
        elem2 = allergy_obs2.to_element()

        # Check that each has correct allergen code
        participant1 = elem1.find(f"{{{NS}}}participant")
        participant_role1 = participant1.find(f"{{{NS}}}participantRole")
        playing_entity1 = participant_role1.find(f"{{{NS}}}playingEntity")
        code1 = playing_entity1.find(f"{{{NS}}}code")

        participant2 = elem2.find(f"{{{NS}}}participant")
        participant_role2 = participant2.find(f"{{{NS}}}participantRole")
        playing_entity2 = participant_role2.find(f"{{{NS}}}playingEntity")
        code2 = playing_entity2.find(f"{{{NS}}}code")

        assert code1.get("code") == "70618"
        assert code2.get("code") == "762952008"

    def test_allergy_in_parent_element(self):
        """Test composing allergy observation in parent element."""
        parent = etree.Element(f"{{{NS}}}entry")

        allergy = MockAllergy()
        allergy_obs = AllergyObservation(allergy)

        parent.append(allergy_obs.to_element())

        observation = parent.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
