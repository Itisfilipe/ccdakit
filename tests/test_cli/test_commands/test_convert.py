"""Tests for the convert CLI command."""

from pathlib import Path
from unittest.mock import patch

import pytest
from lxml import etree
from typer.testing import CliRunner

from ccdakit.cli.__main__ import app


runner = CliRunner()


@pytest.fixture
def sample_ccda_file(tmp_path):
    """Create a sample C-CDA XML file for testing."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test C-CDA Document</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <id extension="12345" root="2.16.840.1.113883.4.1"/>
            <patient>
                <name>
                    <given>John</given>
                    <family>Doe</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Problems</title>
                    <text>
                        <paragraph>Patient has hypertension.</paragraph>
                    </text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""
    xml_file = tmp_path / "test_ccda.xml"
    xml_file.write_text(xml_content)
    return xml_file


@pytest.fixture
def invalid_xml_file(tmp_path):
    """Create an invalid XML file."""
    xml_file = tmp_path / "invalid.xml"
    xml_file.write_text("not valid xml <unclosed>")
    return xml_file


class TestConvertCommand:
    """Test suite for the convert command."""

    def test_convert_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["convert", "--help"])
        assert result.exit_code == 0
        assert "Convert a C-CDA XML document to human-readable HTML" in result.stdout
        assert "--to" in result.stdout
        assert "--output" in result.stdout
        assert "--template" in result.stdout

    def test_convert_missing_file(self):
        """Test conversion with a nonexistent file."""
        result = runner.invoke(app, ["convert", "/nonexistent/file.xml"])
        assert result.exit_code == 1
        assert "File not found" in result.stdout

    def test_convert_invalid_xml(self, invalid_xml_file):
        """Test conversion with an invalid XML file."""
        result = runner.invoke(app, ["convert", str(invalid_xml_file)])
        assert result.exit_code == 1
        assert "Error parsing XML" in result.stdout

    def test_convert_unsupported_format(self, sample_ccda_file):
        """Test conversion to an unsupported format."""
        result = runner.invoke(
            app,
            ["convert", str(sample_ccda_file), "--to", "pdf"],
        )
        assert result.exit_code == 1
        assert "Unsupported format" in result.stdout

    def test_convert_to_html_default(self, sample_ccda_file):
        """Test conversion to HTML with default template."""
        result = runner.invoke(app, ["convert", str(sample_ccda_file)])

        assert result.exit_code == 0
        assert "Converted successfully" in result.stdout

        # Check that HTML file was created
        html_file = sample_ccda_file.with_suffix(".html")
        assert html_file.exists()

        # Verify HTML content
        html_content = html_file.read_text()
        assert "<!DOCTYPE html>" in html_content or "<html" in html_content
        assert "Test C-CDA Document" in html_content
        assert "John" in html_content
        assert "Doe" in html_content

    def test_convert_custom_output_path(self, sample_ccda_file, tmp_path):
        """Test conversion with custom output path."""
        output_file = tmp_path / "custom_output.html"

        result = runner.invoke(
            app,
            ["convert", str(sample_ccda_file), "--output", str(output_file)],
        )

        assert result.exit_code == 0
        assert output_file.exists()
        assert output_file.name in result.stdout

    def test_convert_minimal_template(self, sample_ccda_file):
        """Test conversion with minimal template."""
        result = runner.invoke(
            app,
            ["convert", str(sample_ccda_file), "--template", "minimal"],
        )

        assert result.exit_code == 0

        html_file = sample_ccda_file.with_suffix(".html")
        assert html_file.exists()
        html_content = html_file.read_text()
        assert "<html" in html_content

    @patch("ccdakit.cli.commands.convert._transform_with_official_stylesheet")
    def test_convert_official_template(self, mock_official_transform, sample_ccda_file):
        """Test conversion with official HL7 template."""
        mock_official_transform.return_value = "<html><body>Official Template Output</body></html>"

        result = runner.invoke(
            app,
            ["convert", str(sample_ccda_file), "--template", "official"],
        )

        assert result.exit_code == 0
        mock_official_transform.assert_called_once()

        html_file = sample_ccda_file.with_suffix(".html")
        assert html_file.exists()
        html_content = html_file.read_text()
        assert "Official Template Output" in html_content

    def test_convert_preserves_sections(self, sample_ccda_file):
        """Test that conversion preserves section content."""
        result = runner.invoke(app, ["convert", str(sample_ccda_file)])

        assert result.exit_code == 0

        html_file = sample_ccda_file.with_suffix(".html")
        html_content = html_file.read_text()

        # Check that section title and content are preserved
        assert "Problems" in html_content
        assert "hypertension" in html_content

    def test_convert_preserves_patient_info(self, sample_ccda_file):
        """Test that conversion preserves patient information."""
        result = runner.invoke(app, ["convert", str(sample_ccda_file)])

        assert result.exit_code == 0

        html_file = sample_ccda_file.with_suffix(".html")
        html_content = html_file.read_text()

        # Check patient information
        assert "John" in html_content
        assert "Doe" in html_content
        assert "Male" in html_content

    @patch("ccdakit.cli.commands.convert._transform_with_custom_stylesheet")
    def test_convert_transformation_error(self, mock_transform, sample_ccda_file):
        """Test handling of transformation errors."""
        mock_transform.side_effect = Exception("Transformation failed")

        result = runner.invoke(app, ["convert", str(sample_ccda_file)])

        assert result.exit_code == 1
        assert "Error during transformation" in result.stdout

    def test_convert_write_error(self, sample_ccda_file, tmp_path):
        """Test handling of file write errors."""
        # Try to write to a directory that doesn't exist
        output_file = tmp_path / "nonexistent" / "output.html"

        result = runner.invoke(
            app,
            ["convert", str(sample_ccda_file), "--output", str(output_file)],
        )

        assert result.exit_code == 1
        assert "Error writing file" in result.stdout

    def test_convert_complex_ccda(self, tmp_path):
        """Test conversion of a more complex C-CDA document."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Complex Document</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <id extension="12345" root="2.16.840.1.113883.4.1"/>
            <patient>
                <name>
                    <given>Jane</given>
                    <family>Smith</family>
                </name>
                <administrativeGenderCode code="F" displayName="Female"/>
                <birthTime value="19900615"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Medications</title>
                    <text>
                        <table>
                            <thead>
                                <tr>
                                    <th>Medication</th>
                                    <th>Dose</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Aspirin</td>
                                    <td>81mg daily</td>
                                </tr>
                            </tbody>
                        </table>
                    </text>
                </section>
            </component>
            <component>
                <section>
                    <title>Allergies</title>
                    <text>
                        <list>
                            <item>Penicillin</item>
                            <item>Peanuts</item>
                        </list>
                    </text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "complex.xml"
        xml_file.write_text(xml_content)

        result = runner.invoke(app, ["convert", str(xml_file)])

        assert result.exit_code == 0

        html_file = xml_file.with_suffix(".html")
        assert html_file.exists()
        html_content = html_file.read_text()

        # Verify complex content is preserved
        assert "Jane" in html_content
        assert "Smith" in html_content
        assert "Medications" in html_content
        assert "Allergies" in html_content
        assert "Aspirin" in html_content
        assert "Penicillin" in html_content

    def test_convert_overwrite_existing_output(self, sample_ccda_file):
        """Test that conversion overwrites existing output files."""
        html_file = sample_ccda_file.with_suffix(".html")
        html_file.write_text("old content")

        result = runner.invoke(app, ["convert", str(sample_ccda_file)])

        assert result.exit_code == 0
        html_content = html_file.read_text()
        assert "old content" not in html_content
        assert "John" in html_content

    def test_convert_multiple_sections(self, tmp_path):
        """Test conversion with multiple nested sections."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Multi-Section Document</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Test</given>
                    <family>Patient</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Main Section</title>
                    <text><paragraph>Main content</paragraph></text>
                    <component>
                        <section>
                            <title>Subsection</title>
                            <text><paragraph>Nested content</paragraph></text>
                        </section>
                    </component>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "nested.xml"
        xml_file.write_text(xml_content)

        result = runner.invoke(app, ["convert", str(xml_file)])

        assert result.exit_code == 0
        html_file = xml_file.with_suffix(".html")
        html_content = html_file.read_text()

        assert "Main Section" in html_content
        assert "Subsection" in html_content
        assert "Main content" in html_content
        assert "Nested content" in html_content


class TestConvertIntegration:
    """Integration tests using real example files."""

    def test_convert_real_ccd_example(self):
        """Test conversion with a real CCD example file."""
        example_file = Path("/Users/filipe/Code/pyccda/examples/ccd_example.xml")

        if not example_file.exists():
            pytest.skip("Example file not found")

        result = runner.invoke(app, ["convert", str(example_file)])

        # Should run without crashing
        assert "Converting:" in result.stdout

        # If successful, check HTML was created
        if result.exit_code == 0:
            html_file = example_file.with_suffix(".html")
            assert html_file.exists()
            # Clean up
            html_file.unlink()

    def test_convert_real_discharge_summary(self):
        """Test conversion with a real discharge summary file."""
        example_file = Path("/Users/filipe/Code/pyccda/examples/discharge_summary_example.xml")

        if not example_file.exists():
            pytest.skip("Example file not found")

        result = runner.invoke(app, ["convert", str(example_file)])

        assert "Converting:" in result.stdout

        if result.exit_code == 0:
            html_file = example_file.with_suffix(".html")
            assert html_file.exists()
            # Clean up
            html_file.unlink()


class TestXSLTTemplates:
    """Test XSLT template functionality."""

    def test_custom_stylesheet_valid_xml(self, sample_ccda_file):
        """Test custom stylesheet with valid XML."""
        from ccdakit.cli.commands.convert import _transform_with_custom_stylesheet

        html_output = _transform_with_custom_stylesheet(sample_ccda_file)

        assert html_output is not None
        assert "<html" in html_output
        assert "John" in html_output
        assert "Doe" in html_output

    def test_custom_stylesheet_preserves_structure(self, sample_ccda_file):
        """Test that custom stylesheet preserves document structure."""
        from ccdakit.cli.commands.convert import _transform_with_custom_stylesheet

        html_output = _transform_with_custom_stylesheet(sample_ccda_file)

        # Parse HTML to verify structure
        html_tree = etree.HTML(html_output)
        assert html_tree is not None

        # Check for key elements
        title = html_tree.find(".//title")
        assert title is not None

    @patch("ccdakit.utils.xslt.transform_cda_to_html")
    def test_official_stylesheet_success(self, mock_transform, sample_ccda_file):
        """Test official stylesheet transformation succeeds."""
        from ccdakit.cli.commands.convert import _transform_with_official_stylesheet

        mock_transform.return_value = "<html><body>Official Output</body></html>"

        result = _transform_with_official_stylesheet(sample_ccda_file)

        assert result == "<html><body>Official Output</body></html>"
        mock_transform.assert_called_once_with(sample_ccda_file)

    @patch("ccdakit.utils.xslt.download_cda_stylesheet")
    @patch("ccdakit.utils.xslt.transform_cda_to_html")
    def test_official_stylesheet_downloads_when_missing(
        self, mock_transform, mock_download, sample_ccda_file
    ):
        """Test official stylesheet downloads when not found (covers lines 77-89)."""
        from ccdakit.cli.commands.convert import _transform_with_official_stylesheet

        # First call raises FileNotFoundError, second call succeeds
        mock_transform.side_effect = [
            FileNotFoundError("Stylesheet not found"),
            "<html><body>Downloaded and transformed</body></html>",
        ]

        result = _transform_with_official_stylesheet(sample_ccda_file)

        # Should have downloaded and then transformed
        mock_download.assert_called_once()
        assert mock_transform.call_count == 2
        assert result == "<html><body>Downloaded and transformed</body></html>"

    @patch("ccdakit.utils.xslt.download_cda_stylesheet")
    @patch("ccdakit.utils.xslt.transform_cda_to_html")
    def test_official_stylesheet_download_messages(
        self, mock_transform, mock_download, sample_ccda_file, capsys
    ):
        """Test that download messages are displayed."""
        from ccdakit.cli.commands.convert import _transform_with_official_stylesheet

        mock_transform.side_effect = [
            FileNotFoundError("Stylesheet not found"),
            "<html><body>Success</body></html>",
        ]

        _transform_with_official_stylesheet(sample_ccda_file)

        # The function should call download_cda_stylesheet
        mock_download.assert_called_once()

    @patch("ccdakit.utils.xslt.transform_cda_to_html")
    def test_official_stylesheet_transformation_error(self, mock_transform, sample_ccda_file):
        """Test handling of transformation errors with official stylesheet."""
        from ccdakit.cli.commands.convert import _transform_with_official_stylesheet

        mock_transform.side_effect = etree.XSLTApplyError("XSLT error")

        with pytest.raises(etree.XSLTApplyError):
            _transform_with_official_stylesheet(sample_ccda_file)

    def test_custom_stylesheet_with_special_characters(self, tmp_path):
        """Test custom stylesheet handles special characters."""
        from ccdakit.cli.commands.convert import _transform_with_custom_stylesheet

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test Special Characters</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Patrick</given>
                    <family>Smith</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Test Section</title>
                    <text><paragraph>Content with ampersand and quotes test</paragraph></text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "special_chars.xml"
        xml_file.write_text(xml_content)

        result = _transform_with_custom_stylesheet(xml_file)

        assert result is not None
        assert "Patrick" in result
        assert "Smith" in result
        # HTML entities should be handled properly

    def test_custom_stylesheet_with_tables(self, tmp_path):
        """Test custom stylesheet renders tables correctly."""
        from ccdakit.cli.commands.convert import _transform_with_custom_stylesheet

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Table Test</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>John</given>
                    <family>Doe</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Lab Results</title>
                    <text>
                        <table>
                            <thead>
                                <tr>
                                    <th>Test</th>
                                    <th>Result</th>
                                    <th>Units</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Glucose</td>
                                    <td>95</td>
                                    <td>mg/dL</td>
                                </tr>
                                <tr>
                                    <td>Cholesterol</td>
                                    <td>180</td>
                                    <td>mg/dL</td>
                                </tr>
                            </tbody>
                        </table>
                    </text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "table_test.xml"
        xml_file.write_text(xml_content)

        result = _transform_with_custom_stylesheet(xml_file)

        # Verify table elements are rendered
        assert "<table" in result
        assert "<thead" in result
        assert "<tbody" in result
        assert "Glucose" in result
        assert "Cholesterol" in result


class TestConvertEdgeCases:
    """Test edge cases and error conditions."""

    def test_convert_empty_document(self, tmp_path):
        """Test conversion of minimal valid C-CDA document."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Empty Document</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Test</given>
                    <family>Patient</family>
                </name>
                <administrativeGenderCode displayName="Unknown"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody/>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "empty.xml"
        xml_file.write_text(xml_content)

        result = runner.invoke(app, ["convert", str(xml_file)])

        assert result.exit_code == 0
        html_file = xml_file.with_suffix(".html")
        assert html_file.exists()

    def test_convert_with_utf8_characters(self, tmp_path):
        """Test conversion with UTF-8 special characters."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Document with Special Characters: Café, naïve, façade</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>José</given>
                    <family>García</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Notes</title>
                    <text><paragraph>Patient prefers café au lait ☕</paragraph></text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "utf8.xml"
        xml_file.write_text(xml_content, encoding="utf-8")

        result = runner.invoke(app, ["convert", str(xml_file)])

        assert result.exit_code == 0
        html_file = xml_file.with_suffix(".html")
        html_content = html_file.read_text(encoding="utf-8")
        # UTF-8 characters should be preserved
        assert "José" in html_content or "Jos" in html_content

    def test_convert_readonly_directory(self, sample_ccda_file, tmp_path, monkeypatch):
        """Test handling when output directory is read-only."""
        # This test simulates permission errors
        output_file = tmp_path / "readonly_output.html"

        # Mock Path.write_text to raise PermissionError
        original_write_text = Path.write_text

        def mock_write_text(self, *args, **kwargs):
            if self.name == "readonly_output.html":
                raise PermissionError("Permission denied")
            return original_write_text(self, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", mock_write_text)

        result = runner.invoke(
            app,
            ["convert", str(sample_ccda_file), "--output", str(output_file)],
        )

        assert result.exit_code == 1
        assert "Error writing file" in result.stdout

    def test_convert_with_content_styling(self, tmp_path):
        """Test conversion preserves content styling (bold, italics)."""
        from ccdakit.cli.commands.convert import _transform_with_custom_stylesheet

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Styled Content</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Test</given>
                    <family>Patient</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Clinical Notes</title>
                    <text>
                        <paragraph>
                            <content styleCode="Bold">Important:</content>
                            <content styleCode="Italics">Please review</content>
                        </paragraph>
                    </text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "styled.xml"
        xml_file.write_text(xml_content)

        result = _transform_with_custom_stylesheet(xml_file)

        # Check for bold and italic tags
        assert "<strong>" in result or "<b>" in result
        assert "<em>" in result or "<i>" in result

    def test_convert_with_lists(self, tmp_path):
        """Test conversion preserves list structures."""
        from ccdakit.cli.commands.convert import _transform_with_custom_stylesheet

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>List Test</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Test</given>
                    <family>Patient</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Medications</title>
                    <text>
                        <list>
                            <item>Aspirin 81mg daily</item>
                            <item>Lisinopril 10mg daily</item>
                            <item>Metformin 500mg twice daily</item>
                        </list>
                    </text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "list_test.xml"
        xml_file.write_text(xml_content)

        result = _transform_with_custom_stylesheet(xml_file)

        # Check for list elements
        assert "<ul>" in result
        assert "<li>" in result
        assert "Aspirin" in result
        assert "Lisinopril" in result
        assert "Metformin" in result

    def test_convert_with_line_breaks(self, tmp_path):
        """Test conversion preserves line breaks."""
        from ccdakit.cli.commands.convert import _transform_with_custom_stylesheet

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Line Break Test</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Test</given>
                    <family>Patient</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Instructions</title>
                    <text>
                        <paragraph>
                            First line<br/>
                            Second line<br/>
                            Third line
                        </paragraph>
                    </text>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "linebreak_test.xml"
        xml_file.write_text(xml_content)

        result = _transform_with_custom_stylesheet(xml_file)

        # Check for br tags
        assert "<br" in result


class TestConvertPerformance:
    """Test performance and scalability."""

    def test_convert_large_document(self, tmp_path):
        """Test conversion of a large C-CDA document."""
        # Create a document with many sections
        sections = []
        for i in range(50):
            sections.append(f"""
            <component>
                <section>
                    <title>Section {i}</title>
                    <text>
                        <paragraph>Content for section {i}</paragraph>
                        <table>
                            <thead>
                                <tr><th>Column 1</th><th>Column 2</th></tr>
                            </thead>
                            <tbody>
                                <tr><td>Data {i}-1</td><td>Data {i}-2</td></tr>
                                <tr><td>Data {i}-3</td><td>Data {i}-4</td></tr>
                            </tbody>
                        </table>
                    </text>
                </section>
            </component>
            """)

        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Large Document</title>
    <effectiveTime value="20231022"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Test</given>
                    <family>Patient</family>
                </name>
                <administrativeGenderCode displayName="Male"/>
                <birthTime value="19800101"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            {"".join(sections)}
        </structuredBody>
    </component>
</ClinicalDocument>"""

        xml_file = tmp_path / "large.xml"
        xml_file.write_text(xml_content)

        result = runner.invoke(app, ["convert", str(xml_file)])

        assert result.exit_code == 0
        html_file = xml_file.with_suffix(".html")
        assert html_file.exists()

        # Verify content is present
        html_content = html_file.read_text()
        assert "Section 0" in html_content
        assert "Section 49" in html_content
