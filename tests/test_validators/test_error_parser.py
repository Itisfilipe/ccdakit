"""Tests for Schematron error parser."""

from ccdakit.validators.error_parser import ParsedError, SchematronErrorParser


class TestSchematronErrorParser:
    """Test suite for SchematronErrorParser."""

    def test_simplify_xpath_basic(self):
        """Test simplifying basic XPath."""
        xpath = "/*[local-name()='ClinicalDocument']/*[local-name()='component']"
        result = SchematronErrorParser.simplify_xpath(xpath)
        assert result == "ClinicalDocument > component"

    def test_simplify_xpath_with_position(self):
        """Test simplifying XPath with position predicates."""
        xpath = "/*[local-name()='ClinicalDocument'][1]/*[local-name()='component'][2]"
        result = SchematronErrorParser.simplify_xpath(xpath)
        assert result == "ClinicalDocument[1] > component[2]"

    def test_simplify_xpath_with_namespace(self):
        """Test simplifying XPath with namespace predicate."""
        xpath = "/*[local-name()='ClinicalDocument' and namespace-uri()='urn:hl7-org:v3']"
        result = SchematronErrorParser.simplify_xpath(xpath)
        assert result == "ClinicalDocument"

    def test_simplify_xpath_empty(self):
        """Test simplifying empty XPath."""
        result = SchematronErrorParser.simplify_xpath("")
        assert result == ""

    def test_simplify_xpath_no_predicates(self):
        """Test simplifying XPath without local-name predicates."""
        xpath = "/root/element"
        result = SchematronErrorParser.simplify_xpath(xpath)
        # Should handle this gracefully
        assert isinstance(result, str)

    def test_extract_template_id_found(self):
        """Test extracting template ID from error message."""
        message = 'Error: templateId with @root="2.16.840.1.113883.10.20.22.4.7" is required'
        result = SchematronErrorParser.extract_template_id(message)
        assert result == "2.16.840.1.113883.10.20.22.4.7"

    def test_extract_template_id_not_found(self):
        """Test extracting template ID when not present."""
        message = "Error: some validation error without template"
        result = SchematronErrorParser.extract_template_id(message)
        assert result is None

    def test_extract_conf_number_with_parentheses(self):
        """Test extracting CONF number with parentheses."""
        message = "SHALL contain exactly one (CONF:1098-8583)"
        result = SchematronErrorParser.extract_conf_number(message)
        assert result == "1098-8583"

    def test_extract_conf_number_without_parentheses(self):
        """Test extracting CONF number without parentheses."""
        message = "SHALL contain CONF:1098-8583"
        result = SchematronErrorParser.extract_conf_number(message)
        assert result == "1098-8583"

    def test_extract_conf_number_not_found(self):
        """Test extracting CONF number when not present."""
        message = "Error without CONF number"
        result = SchematronErrorParser.extract_conf_number(message)
        assert result is None

    def test_extract_requirement_with_shall(self):
        """Test extracting requirement starting with SHALL."""
        message = "ERROR at /path: SHALL contain exactly one [1..1] templateId"
        result = SchematronErrorParser.extract_requirement(message)
        assert "SHALL contain exactly one" in result

    def test_extract_requirement_with_should(self):
        """Test extracting requirement starting with SHOULD."""
        message = "ERROR at /path: SHOULD contain at least one value"
        result = SchematronErrorParser.extract_requirement(message)
        assert "SHOULD contain" in result

    def test_extract_xpath_from_error(self):
        """Test extracting XPath from error message."""
        message = "ERROR at /*[local-name()='ClinicalDocument']: Some error message"
        result = SchematronErrorParser.extract_xpath(message)
        assert "local-name" in result

    def test_extract_xpath_from_warning(self):
        """Test extracting XPath from warning message."""
        message = "WARNING at /some/path: Warning message"
        result = SchematronErrorParser.extract_xpath(message)
        assert "/some/path" in result

    def test_determine_severity_error(self):
        """Test determining severity for error."""
        message = "ERROR at /path: error message"
        result = SchematronErrorParser.determine_severity(message)
        assert result == "error"

    def test_determine_severity_warning(self):
        """Test determining severity for warning."""
        message = "WARNING at /path: warning message"
        result = SchematronErrorParser.determine_severity(message)
        assert result == "warning"

    def test_determine_severity_default(self):
        """Test determining severity defaults to error."""
        message = "Some message without prefix"
        result = SchematronErrorParser.determine_severity(message)
        assert result == "error"

    def test_generate_suggestions_with_template_id(self):
        """Test generating suggestions with template ID."""
        parsed = ParsedError(
            original_message="Error",
            simplified_path="path",
            full_xpath="/xpath",
            requirement="SHALL contain templateId with @root=\"2.16.840.1.113883.10.20.22.4.7\"",
            template_id="2.16.840.1.113883.10.20.22.4.7",
            conf_number=None,
            template_name="Allergy Observation",
            severity="error",
            suggestions=[],
        )

        suggestions = SchematronErrorParser.generate_suggestions(parsed)
        assert len(suggestions) > 0
        assert any("templateId" in s for s in suggestions)
        assert any("2.16.840.1.113883.10.20.22.4.7" in s for s in suggestions)

    def test_generate_suggestions_cardinality_exactly_one(self):
        """Test generating suggestions for cardinality exactly one."""
        parsed = ParsedError(
            original_message="Error",
            simplified_path="path",
            full_xpath="/xpath",
            requirement="SHALL contain exactly one [1..1] code element",
            template_id=None,
            conf_number=None,
            template_name=None,
            severity="error",
            suggestions=[],
        )

        suggestions = SchematronErrorParser.generate_suggestions(parsed)
        assert any("exactly once" in s for s in suggestions)

    def test_generate_suggestions_cardinality_at_least_one(self):
        """Test generating suggestions for cardinality at least one."""
        parsed = ParsedError(
            original_message="Error",
            simplified_path="path",
            full_xpath="/xpath",
            requirement="SHALL contain at least one [1..*] entry",
            template_id=None,
            conf_number=None,
            template_name=None,
            severity="error",
            suggestions=[],
        )

        suggestions = SchematronErrorParser.generate_suggestions(parsed)
        assert any("at least one" in s.lower() for s in suggestions)

    def test_generate_suggestions_with_documentation_link(self):
        """Test generating suggestions includes documentation link."""
        parsed = ParsedError(
            original_message="Error",
            simplified_path="path",
            full_xpath="/xpath",
            requirement="Error in template",
            template_id="2.16.840.1.113883.10.20.22.4.4",
            conf_number=None,
            template_name="Vital Signs Observation",
            severity="error",
            suggestions=[],
        )

        suggestions = SchematronErrorParser.generate_suggestions(parsed)
        assert any("docs.ccdakit.com" in s for s in suggestions)

    def test_generate_suggestions_fallback_docs_link(self):
        """Test generating suggestions includes fallback docs link."""
        parsed = ParsedError(
            original_message="Error",
            simplified_path="path",
            full_xpath="/xpath",
            requirement="Some error",
            template_id=None,
            conf_number=None,
            template_name=None,
            severity="error",
            suggestions=[],
        )

        suggestions = SchematronErrorParser.generate_suggestions(parsed)
        assert any("docs.ccdakit.com" in s for s in suggestions)

    def test_generate_suggestions_with_attributes(self):
        """Test generating suggestions extracts attribute values."""
        parsed = ParsedError(
            original_message="Error",
            simplified_path="path",
            full_xpath="/xpath",
            requirement='SHALL have @code="12345" and @codeSystem="SNOMED"',
            template_id=None,
            conf_number=None,
            template_name=None,
            severity="error",
            suggestions=[],
        )

        suggestions = SchematronErrorParser.generate_suggestions(parsed)
        assert any("code" in s and "12345" in s for s in suggestions)

    def test_parse_error_complete(self):
        """Test parsing complete error message."""
        error_message = (
            'ERROR at /*[local-name()=\'ClinicalDocument\']: '
            'SHALL contain exactly one [1..1] templateId with @root="2.16.840.1.113883.10.20.22.4.7" '
            '(CONF:1098-8583) [SCHEMATRON]'
        )

        result = SchematronErrorParser.parse_error(error_message)

        assert isinstance(result, ParsedError)
        assert result.original_message == error_message
        assert result.severity == "error"
        assert result.template_id == "2.16.840.1.113883.10.20.22.4.7"
        assert result.conf_number == "1098-8583"
        assert len(result.suggestions) > 0

    def test_parse_errors_multiple(self):
        """Test parsing multiple error messages."""
        messages = [
            "ERROR at /path1: Error 1",
            "WARNING at /path2: Warning 1",
            "ERROR at /path3: Error 2",
        ]

        results = SchematronErrorParser.parse_errors(messages)

        assert len(results) == 3
        assert all(isinstance(r, ParsedError) for r in results)
        assert results[0].severity == "error"
        assert results[1].severity == "warning"
        assert results[2].severity == "error"

    def test_parsed_error_to_dict(self):
        """Test converting ParsedError to dictionary."""
        parsed = ParsedError(
            original_message="Error message",
            simplified_path="ClinicalDocument > section",
            full_xpath="/xpath",
            requirement="SHALL contain something",
            template_id="1.2.3.4",
            conf_number="1098-123",
            template_name="Test Template",
            severity="error",
            suggestions=["Fix this", "Try that"],
        )

        result = parsed.to_dict()

        assert isinstance(result, dict)
        assert result["original_message"] == "Error message"
        assert result["simplified_path"] == "ClinicalDocument > section"
        assert result["template_id"] == "1.2.3.4"
        assert result["conf_number"] == "1098-123"
        assert result["severity"] == "error"
        assert len(result["suggestions"]) == 2
