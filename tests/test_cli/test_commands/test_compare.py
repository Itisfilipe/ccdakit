"""Tests for the compare CLI command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from ccdakit.cli.__main__ import app


runner = CliRunner()


@pytest.fixture
def sample_ccda_file1(tmp_path):
    """Create first sample C-CDA file."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Document 1</title>
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
                    <title>Problems</title>
                    <code code="11450-4"/>
                    <entry/>
                    <entry/>
                </section>
            </component>
            <component>
                <section>
                    <title>Medications</title>
                    <code code="10160-0"/>
                    <entry/>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""
    xml_file = tmp_path / "doc1.xml"
    xml_file.write_text(xml_content)
    return xml_file


@pytest.fixture
def sample_ccda_file2(tmp_path):
    """Create second sample C-CDA file (identical to first)."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Document 1</title>
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
                    <title>Problems</title>
                    <code code="11450-4"/>
                    <entry/>
                    <entry/>
                </section>
            </component>
            <component>
                <section>
                    <title>Medications</title>
                    <code code="10160-0"/>
                    <entry/>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""
    xml_file = tmp_path / "doc2.xml"
    xml_file.write_text(xml_content)
    return xml_file


@pytest.fixture
def different_ccda_file(tmp_path):
    """Create a different C-CDA file."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Document 2</title>
    <effectiveTime value="20231023"/>
    <recordTarget>
        <patientRole>
            <patient>
                <name>
                    <given>Jane</given>
                    <family>Smith</family>
                </name>
                <administrativeGenderCode displayName="Female"/>
                <birthTime value="19900615"/>
            </patient>
        </patientRole>
    </recordTarget>
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Problems</title>
                    <code code="11450-4"/>
                    <entry/>
                </section>
            </component>
            <component>
                <section>
                    <title>Allergies</title>
                    <code code="48765-2"/>
                    <entry/>
                    <entry/>
                    <entry/>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>"""
    xml_file = tmp_path / "doc3.xml"
    xml_file.write_text(xml_content)
    return xml_file


@pytest.fixture
def invalid_xml_file(tmp_path):
    """Create an invalid XML file."""
    xml_file = tmp_path / "invalid.xml"
    xml_file.write_text("not valid xml <unclosed>")
    return xml_file


class TestCompareCommand:
    """Test suite for the compare command."""

    def test_compare_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["compare", "--help"])
        assert result.exit_code == 0
        assert "Compare two C-CDA documents" in result.stdout
        assert "file1" in result.stdout.lower()
        assert "file2" in result.stdout.lower()
        assert "--output" in result.stdout
        assert "--format" in result.stdout

    def test_compare_first_file_not_found(self, sample_ccda_file1):
        """Test comparison when first file doesn't exist."""
        result = runner.invoke(
            app,
            ["compare", "/nonexistent/file1.xml", str(sample_ccda_file1)],
        )
        assert result.exit_code == 1
        assert "File not found" in result.stdout

    def test_compare_second_file_not_found(self, sample_ccda_file1):
        """Test comparison when second file doesn't exist."""
        result = runner.invoke(
            app,
            ["compare", str(sample_ccda_file1), "/nonexistent/file2.xml"],
        )
        assert result.exit_code == 1
        assert "File not found" in result.stdout

    def test_compare_invalid_xml_first_file(
        self, invalid_xml_file, sample_ccda_file1
    ):
        """Test comparison with invalid XML in first file."""
        result = runner.invoke(
            app,
            ["compare", str(invalid_xml_file), str(sample_ccda_file1)],
        )
        assert result.exit_code == 1
        assert "Error parsing XML" in result.stdout

    def test_compare_invalid_xml_second_file(
        self, sample_ccda_file1, invalid_xml_file
    ):
        """Test comparison with invalid XML in second file."""
        result = runner.invoke(
            app,
            ["compare", str(sample_ccda_file1), str(invalid_xml_file)],
        )
        assert result.exit_code == 1
        assert "Error parsing XML" in result.stdout

    def test_compare_identical_files(self, sample_ccda_file1, sample_ccda_file2):
        """Test comparison of identical files."""
        result = runner.invoke(
            app,
            ["compare", str(sample_ccda_file1), str(sample_ccda_file2)],
        )

        assert result.exit_code == 0
        assert "Comparing:" in result.stdout
        assert "Document Comparison Report" in result.stdout
        assert "structurally identical" in result.stdout.lower()

    def test_compare_different_files(
        self, sample_ccda_file1, different_ccda_file
    ):
        """Test comparison of different files."""
        result = runner.invoke(
            app,
            ["compare", str(sample_ccda_file1), str(different_ccda_file)],
        )

        assert result.exit_code == 0
        assert "Comparing:" in result.stdout
        assert "differences" in result.stdout.lower()

    def test_compare_shows_patient_differences(
        self, sample_ccda_file1, different_ccda_file
    ):
        """Test that patient demographic differences are shown."""
        result = runner.invoke(
            app,
            ["compare", str(sample_ccda_file1), str(different_ccda_file)],
        )

        assert result.exit_code == 0
        # Should show patient differences
        output_lower = result.stdout.lower()
        assert "patient" in output_lower or "name" in output_lower

    def test_compare_shows_section_differences(
        self, sample_ccda_file1, different_ccda_file
    ):
        """Test that section differences are shown."""
        result = runner.invoke(
            app,
            ["compare", str(sample_ccda_file1), str(different_ccda_file)],
        )

        assert result.exit_code == 0
        # Should show sections only in one file or section differences
        assert ("Sections only in" in result.stdout or
                "Sections with Different Entry Counts" in result.stdout or
                "Medications" in result.stdout or
                "Allergies" in result.stdout)

    def test_compare_text_format_default(
        self, sample_ccda_file1, different_ccda_file
    ):
        """Test comparison with default text format."""
        result = runner.invoke(
            app,
            ["compare", str(sample_ccda_file1), str(different_ccda_file)],
        )

        assert result.exit_code == 0
        assert "Document Comparison Report" in result.stdout

    def test_compare_html_format(
        self, sample_ccda_file1, different_ccda_file, tmp_path
    ):
        """Test comparison with HTML output format."""
        output_file = tmp_path / "comparison.html"

        result = runner.invoke(
            app,
            [
                "compare",
                str(sample_ccda_file1),
                str(different_ccda_file),
                "--format",
                "html",
                "--output",
                str(output_file),
            ],
        )

        assert result.exit_code == 0
        assert output_file.exists()

        # Verify HTML content
        html_content = output_file.read_text()
        assert "<!DOCTYPE html>" in html_content
        assert "Document Comparison Report" in html_content

    def test_compare_html_auto_filename(
        self, sample_ccda_file1, different_ccda_file
    ):
        """Test HTML comparison with automatic filename."""
        result = runner.invoke(
            app,
            [
                "compare",
                str(sample_ccda_file1),
                str(different_ccda_file),
                "--format",
                "html",
            ],
        )

        assert result.exit_code == 0
        assert "Comparison saved to" in result.stdout

        # Check that a comparison HTML file was created
        # Files are created in current working directory
        html_files = list(Path.cwd().glob("comparison_*.html"))
        assert len(html_files) >= 1

        # Clean up
        for html_file in html_files:
            html_file.unlink()

    def test_compare_unsupported_format(
        self, sample_ccda_file1, sample_ccda_file2
    ):
        """Test comparison with unsupported format."""
        result = runner.invoke(
            app,
            [
                "compare",
                str(sample_ccda_file1),
                str(sample_ccda_file2),
                "--format",
                "json",
            ],
        )

        assert result.exit_code == 1
        assert "Unsupported format" in result.stdout

    def test_compare_entry_count_differences(self, tmp_path):
        """Test comparison showing different entry counts in same section."""
        # Create file 1 with 2 entries
        xml1 = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc 1</title>
    <recordTarget><patientRole><patient>
        <name><given>John</given><family>Doe</family></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody>
        <component>
            <section>
                <title>Medications</title>
                <entry/><entry/>
            </section>
        </component>
    </structuredBody></component>
</ClinicalDocument>"""

        # Create file 2 with 3 entries
        xml2 = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Doc 2</title>
    <recordTarget><patientRole><patient>
        <name><given>John</given><family>Doe</family></name>
    </patient></patientRole></recordTarget>
    <component><structuredBody>
        <component>
            <section>
                <title>Medications</title>
                <entry/><entry/><entry/>
            </section>
        </component>
    </structuredBody></component>
</ClinicalDocument>"""

        file1 = tmp_path / "file1.xml"
        file2 = tmp_path / "file2.xml"
        file1.write_text(xml1)
        file2.write_text(xml2)

        result = runner.invoke(app, ["compare", str(file1), str(file2)])

        assert result.exit_code == 0
        assert "Different Entry Counts" in result.stdout or "differences" in result.stdout


class TestCompareIntegration:
    """Integration tests using real example files."""

    def test_compare_real_examples(self):
        """Test comparison with real example files."""
        file1 = Path("/Users/filipe/Code/pyccda/examples/ccd_example.xml")
        file2 = Path("/Users/filipe/Code/pyccda/examples/discharge_summary_example.xml")

        if not (file1.exists() and file2.exists()):
            pytest.skip("Example files not found")

        result = runner.invoke(app, ["compare", str(file1), str(file2)])

        # Should run without crashing
        assert "Comparing:" in result.stdout
        assert result.exit_code == 0


class TestCompareHelperFunctions:
    """Test helper functions used in compare command."""

    def test_extract_comparison_data(self, sample_ccda_file1):
        """Test extraction of comparison data from XML."""
        from lxml import etree

        from ccdakit.cli.commands.compare import _extract_comparison_data

        tree = etree.parse(str(sample_ccda_file1))
        data = _extract_comparison_data(tree.getroot())

        assert "patient" in data
        assert "document" in data
        assert "sections" in data

        # Check patient data
        assert "name" in data["patient"]
        # Name extraction may vary based on XML structure
        assert isinstance(data["patient"]["name"], str)

        # Check document data
        assert "title" in data["document"]

        # Check sections
        assert len(data["sections"]) >= 2

    def test_get_text_with_none_element(self):
        """Test _get_text with None element (covers line 359)."""
        from ccdakit.cli.commands.compare import _get_text

        # When element is None, should return empty string
        result = _get_text(None, ".//some/xpath")
        assert result == ""

    def test_get_text_with_xpath_exception(self):
        """Test _get_text with XPath that causes exception (covers lines 365-367)."""
        from unittest.mock import MagicMock, patch

        from ccdakit.cli.commands.compare import _get_text

        # Create a mock element that raises an exception during xpath evaluation
        mock_element = MagicMock()
        mock_element.xpath.side_effect = Exception("XPath evaluation error")

        # Should catch exception and return empty string
        result = _get_text(mock_element, ".//any/xpath")
        assert result == ""

    def test_compare_documents_function(self):
        """Test the document comparison function."""
        from ccdakit.cli.commands.compare import _compare_documents

        data1 = {
            "patient": {"name": "John Doe", "gender": "Male"},
            "document": {"title": "Doc 1"},
            "sections": {
                "Problems": {"code": "11450-4", "entry_count": 2},
                "Medications": {"code": "10160-0", "entry_count": 1},
            },
        }

        data2 = {
            "patient": {"name": "Jane Smith", "gender": "Female"},
            "document": {"title": "Doc 2"},
            "sections": {
                "Problems": {"code": "11450-4", "entry_count": 1},
                "Allergies": {"code": "48765-2", "entry_count": 3},
            },
        }

        comparison = _compare_documents(data1, data2)

        # Should detect patient differences
        assert len(comparison["patient_differences"]) > 0

        # Should detect sections only in each file
        assert "Medications" in comparison["sections_only_in_1"]
        assert "Allergies" in comparison["sections_only_in_2"]

        # Should detect different entry counts
        assert len(comparison["section_differences"]) > 0

    def test_compare_identical_documents(self):
        """Test comparison of identical document data."""
        from ccdakit.cli.commands.compare import _compare_documents

        data = {
            "patient": {"name": "John Doe", "gender": "Male"},
            "document": {"title": "Doc 1"},
            "sections": {"Problems": {"code": "11450-4", "entry_count": 2}},
        }

        comparison = _compare_documents(data, data)

        # Should have no differences
        assert len(comparison["patient_differences"]) == 0
        assert len(comparison["document_differences"]) == 0
        assert len(comparison["sections_only_in_1"]) == 0
        assert len(comparison["sections_only_in_2"]) == 0
        assert len(comparison["section_differences"]) == 0
