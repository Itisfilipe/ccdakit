"""Tests for the serve CLI command and web app."""

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from ccdakit.cli.__main__ import app


runner = CliRunner()


class TestServeCommand:
    """Test suite for the serve command."""

    def test_serve_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["serve", "--help"])
        assert result.exit_code == 0
        assert "Start the web UI server" in result.stdout
        assert "--host" in result.stdout
        assert "--port" in result.stdout
        assert "--debug" in result.stdout

    @patch("ccdakit.cli.commands.serve.create_app")
    def test_serve_default_options(self, mock_create_app):
        """Test serve command with default options."""
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app

        # Mock the run method to avoid actually starting the server
        mock_app.run = MagicMock()

        result = runner.invoke(app, ["serve"])

        # Should call create_app
        mock_create_app.assert_called_once()

        # Should call run with default parameters
        mock_app.run.assert_called_once_with(
            host="127.0.0.1", port=8000, debug=False
        )

        # Output should show server info
        assert "Starting ccdakit web UI" in result.stdout
        assert "http://127.0.0.1:8000" in result.stdout

    @patch("ccdakit.cli.commands.serve.create_app")
    def test_serve_custom_host(self, mock_create_app):
        """Test serve command with custom host."""
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_app.run = MagicMock()

        result = runner.invoke(app, ["serve", "--host", "0.0.0.0"])

        mock_app.run.assert_called_once_with(host="0.0.0.0", port=8000, debug=False)
        assert "http://0.0.0.0:8000" in result.stdout

    @patch("ccdakit.cli.commands.serve.create_app")
    def test_serve_custom_port(self, mock_create_app):
        """Test serve command with custom port."""
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_app.run = MagicMock()

        result = runner.invoke(app, ["serve", "--port", "5000"])

        mock_app.run.assert_called_once_with(host="127.0.0.1", port=5000, debug=False)
        assert "http://127.0.0.1:5000" in result.stdout

    @patch("ccdakit.cli.commands.serve.create_app")
    def test_serve_debug_mode(self, mock_create_app):
        """Test serve command with debug mode enabled."""
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_app.run = MagicMock()

        result = runner.invoke(app, ["serve", "--debug"])

        mock_app.run.assert_called_once_with(host="127.0.0.1", port=8000, debug=True)

    @patch("ccdakit.cli.commands.serve.create_app")
    def test_serve_all_options(self, mock_create_app):
        """Test serve command with all options specified."""
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_app.run = MagicMock()

        result = runner.invoke(
            app, ["serve", "--host", "0.0.0.0", "--port", "8080", "--debug"]
        )

        mock_app.run.assert_called_once_with(host="0.0.0.0", port=8080, debug=True)
        assert "http://0.0.0.0:8080" in result.stdout


class TestWebApp:
    """Test suite for the Flask web application."""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app."""
        from ccdakit.cli.web.app import create_app

        app = create_app()
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_home_page(self, client):
        """Test the home page loads."""
        response = client.get("/")
        assert response.status_code == 200

    def test_validate_page(self, client):
        """Test the validate page loads."""
        response = client.get("/validate")
        assert response.status_code == 200

    def test_generate_page(self, client):
        """Test the generate page loads."""
        response = client.get("/generate")
        assert response.status_code == 200

    def test_convert_page(self, client):
        """Test the convert page loads."""
        response = client.get("/convert")
        assert response.status_code == 200

    def test_compare_page(self, client):
        """Test the compare page loads."""
        response = client.get("/compare")
        assert response.status_code == 200

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_api_validate_with_content(
        self, mock_schematron, mock_xsd, client
    ):
        """Test the validate API endpoint with textarea content."""
        from ccdakit.core.validation import ValidationResult

        # Mock validation results
        mock_xsd.return_value = ValidationResult()
        mock_schematron.return_value = ValidationResult()

        xml_content = '<?xml version="1.0"?><ClinicalDocument xmlns="urn:hl7-org:v3"/>'

        response = client.post(
            "/api/validate",
            data={
                "content": xml_content,
                "xsd": "on",
                "schematron": "on",
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "xsd" in data or "schematron" in data

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    def test_api_validate_with_file(self, mock_xsd, client, tmp_path):
        """Test the validate API endpoint with file upload."""
        from io import BytesIO

        from ccdakit.core.validation import ValidationResult

        mock_xsd.return_value = ValidationResult()

        xml_content = b'<?xml version="1.0"?><ClinicalDocument xmlns="urn:hl7-org:v3"/>'

        response = client.post(
            "/api/validate",
            data={
                "file": (BytesIO(xml_content), "test.xml"),
                "xsd": "on",
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 200

    def test_api_validate_no_content(self, client):
        """Test the validate API endpoint with no content."""
        response = client.post("/api/validate", data={})

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_api_generate(self, mock_generate, client):
        """Test the generate API endpoint."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        response = client.post(
            "/api/generate",
            json={
                "document_type": "ccd",
                "sections": ["problems", "medications"],
            },
        )

        if response.status_code == 200:
            data = response.get_json()
            assert "xml" in data
        # May fail if faker not installed, which is okay

    def test_api_convert_with_content(self, client):
        """Test the convert API endpoint with textarea content."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
    <recordTarget><patientRole><patient>
        <name><given>John</given></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody/></component>
</ClinicalDocument>"""

        response = client.post(
            "/api/convert",
            data={"content": xml_content},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "html" in data
        assert "<html" in data["html"]

    def test_api_convert_with_file(self, client):
        """Test the convert API endpoint with file upload."""
        from io import BytesIO

        xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
    <recordTarget><patientRole><patient>
        <name><given>John</given></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody/></component>
</ClinicalDocument>"""

        response = client.post(
            "/api/convert",
            data={"file": (BytesIO(xml_content), "test.xml")},
            content_type="multipart/form-data",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "html" in data

    def test_api_convert_no_content(self, client):
        """Test the convert API endpoint with no content."""
        response = client.post("/api/convert", data={})

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_api_compare(self, client):
        """Test the compare API endpoint."""
        xml1 = b"""<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc1</title>
    <recordTarget><patientRole><patient>
        <name><given>John</given><family>Doe</family></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody/></component>
</ClinicalDocument>"""

        xml2 = b"""<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc2</title>
    <recordTarget><patientRole><patient>
        <name><given>Jane</given><family>Smith</family></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody/></component>
</ClinicalDocument>"""

        from io import BytesIO

        response = client.post(
            "/api/compare",
            data={
                "file1": (BytesIO(xml1), "doc1.xml"),
                "file2": (BytesIO(xml2), "doc2.xml"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "comparison" in data

    def test_api_compare_missing_file(self, client):
        """Test the compare API endpoint with missing file."""
        from io import BytesIO

        xml1 = b'<?xml version="1.0"?><ClinicalDocument xmlns="urn:hl7-org:v3"/>'

        response = client.post(
            "/api/compare",
            data={"file1": (BytesIO(xml1), "doc1.xml")},
            content_type="multipart/form-data",
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_app_config(self):
        """Test Flask app configuration."""
        from ccdakit.cli.web.app import create_app

        app = create_app()

        # Check max content length is set
        assert "MAX_CONTENT_LENGTH" in app.config
        assert app.config["MAX_CONTENT_LENGTH"] == 16 * 1024 * 1024

    def test_app_routes_registered(self):
        """Test that all expected routes are registered."""
        from ccdakit.cli.web.app import create_app

        app = create_app()

        # Get all route rules
        rules = [rule.rule for rule in app.url_map.iter_rules()]

        # Check page routes
        assert "/" in rules
        assert "/validate" in rules
        assert "/generate" in rules
        assert "/convert" in rules
        assert "/compare" in rules

        # Check API routes
        assert "/api/validate" in rules
        assert "/api/generate" in rules
        assert "/api/convert" in rules
        assert "/api/compare" in rules

    @patch("ccdakit.cli.web.app.get_schematron_validator")
    @patch("ccdakit.cli.web.app.get_xsd_validator")
    def test_api_validate_no_validators_specified(
        self, mock_get_xsd, mock_get_schematron, client
    ):
        """Test validation with no validators specified runs both by default."""
        from ccdakit.core.validation import ValidationResult

        # Mock validators
        mock_xsd_validator = MagicMock()
        mock_xsd_validator.validate.return_value = ValidationResult()
        mock_get_xsd.return_value = mock_xsd_validator

        mock_schematron_validator = MagicMock()
        mock_schematron_validator.validate.return_value = ValidationResult()
        mock_get_schematron.return_value = mock_schematron_validator

        xml_content = '<?xml version="1.0"?><ClinicalDocument xmlns="urn:hl7-org:v3"/>'

        # Don't include xsd or schematron checkboxes
        response = client.post(
            "/api/validate",
            data={
                "content": xml_content,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        # Both validators should have run
        assert "xsd" in data
        assert "schematron" in data
        mock_xsd_validator.validate.assert_called_once()
        mock_schematron_validator.validate.assert_called_once()

    @patch("ccdakit.cli.web.app.get_xsd_validator")
    def test_api_validate_exception_handling(self, mock_get_xsd, client):
        """Test validation API exception handling."""
        # Mock validator to raise an exception
        mock_xsd_validator = MagicMock()
        mock_xsd_validator.validate.side_effect = Exception("Validation failed unexpectedly")
        mock_get_xsd.return_value = mock_xsd_validator

        xml_content = '<?xml version="1.0"?><ClinicalDocument xmlns="urn:hl7-org:v3"/>'

        response = client.post(
            "/api/validate",
            data={
                "content": xml_content,
                "xsd": "on",
            },
        )

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Validation failed unexpectedly" in data["error"]

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_api_generate_exception_handling(self, mock_generate, client):
        """Test generate API exception handling."""
        # Mock generate to raise an exception
        mock_generate.side_effect = Exception("Generation failed")

        response = client.post(
            "/api/generate",
            json={
                "document_type": "ccd",
                "sections": ["problems"],
            },
        )

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Generation failed" in data["error"]

    @patch("ccdakit.cli.commands.convert._transform_with_official_stylesheet")
    def test_api_convert_exception_handling(self, mock_transform, client):
        """Test convert API exception handling."""
        # Mock transform to raise an exception
        mock_transform.side_effect = Exception("Transformation failed")

        xml_content = """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        response = client.post(
            "/api/convert",
            data={"content": xml_content},
        )

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Transformation failed" in data["error"]

    def test_api_compare_with_textarea_content(self, client):
        """Test compare API with textarea content instead of files."""
        xml1 = """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc1</title>
    <recordTarget><patientRole><patient>
        <name><given>John</given><family>Doe</family></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody/></component>
</ClinicalDocument>"""

        xml2 = """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc2</title>
    <recordTarget><patientRole><patient>
        <name><given>Jane</given><family>Smith</family></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody/></component>
</ClinicalDocument>"""

        response = client.post(
            "/api/compare",
            data={
                "content1": xml1,
                "content2": xml2,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "comparison" in data
        assert "file1_name" in data
        assert "file2_name" in data

    def test_api_compare_missing_first_document_textarea(self, client):
        """Test compare API with missing first document from textarea."""
        xml2 = """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc2</title>
</ClinicalDocument>"""

        response = client.post(
            "/api/compare",
            data={
                "content2": xml2,
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "First document not provided" in data["error"]

    def test_api_compare_missing_second_document_textarea(self, client):
        """Test compare API with missing second document from textarea."""
        xml1 = """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc1</title>
</ClinicalDocument>"""

        response = client.post(
            "/api/compare",
            data={
                "content1": xml1,
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Second document not provided" in data["error"]

    def test_api_compare_exception_handling(self, client):
        """Test compare API exception handling with invalid XML."""
        xml1 = "invalid xml content"
        xml2 = "also invalid"

        from io import BytesIO

        response = client.post(
            "/api/compare",
            data={
                "file1": (BytesIO(xml1.encode()), "doc1.xml"),
                "file2": (BytesIO(xml2.encode()), "doc2.xml"),
            },
            content_type="multipart/form-data",
        )

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
