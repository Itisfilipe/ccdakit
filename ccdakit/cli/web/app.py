"""Flask web application for ccdakit UI."""

import logging
import tempfile
from pathlib import Path
from typing import Optional

from flask import Flask, jsonify, render_template, request

from ccdakit.cli.commands.compare import _compare_documents, _extract_comparison_data
from ccdakit.validators.schematron import SchematronValidator
from ccdakit.validators.xsd import XSDValidator


logger = logging.getLogger(__name__)


# Global validator cache to avoid recreating validators for each request
# This saves significant memory (62MB+ per validator) on the 512MB server
_xsd_validator_cache: Optional[XSDValidator] = None
_schematron_validator_cache: Optional[SchematronValidator] = None


def get_xsd_validator() -> XSDValidator:
    """Get or create cached XSD validator."""
    global _xsd_validator_cache
    if _xsd_validator_cache is None:
        _xsd_validator_cache = XSDValidator()
    return _xsd_validator_cache


def get_schematron_validator() -> SchematronValidator:
    """Get or create cached Schematron validator."""
    global _schematron_validator_cache
    if _schematron_validator_cache is None:
        _schematron_validator_cache = SchematronValidator()
    return _schematron_validator_cache


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max file size

    # Page Routes
    @app.route("/")
    def index():
        """Home page."""
        return render_template("home.html", active_page="home")

    @app.route("/validate")
    def validate_page():
        """Validate page."""
        return render_template("validate.html", active_page="validate")

    @app.route("/generate")
    def generate_page():
        """Generate page."""
        return render_template("generate.html", active_page="generate")

    @app.route("/convert")
    def convert_page():
        """Convert page."""
        return render_template("convert.html", active_page="convert")

    @app.route("/compare")
    def compare_page():
        """Compare page."""
        return render_template("compare.html", active_page="compare")

    @app.route("/api/validate", methods=["POST"])
    def api_validate():
        """Validate a C-CDA document."""
        # Handle file upload or textarea content
        content = None
        if "file" in request.files and request.files["file"].filename:
            file = request.files["file"]
            content = file.read()
            logger.debug("Received file: %s, size: %d bytes", file.filename, len(content))
        elif "content" in request.form and request.form["content"]:
            content = request.form["content"].encode("utf-8")
            logger.debug("Received textarea content, size: %d bytes", len(content))
        else:
            return jsonify({"error": "No file or content provided"}), 400

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)

        try:
            # Run validation
            results = {}

            # Check if validators are enabled (checkboxes send "on" when checked)
            run_xsd = request.form.get("xsd") == "on"
            run_schematron = request.form.get("schematron") == "on"

            logger.debug("XSD checkbox: %s, Run XSD: %s", request.form.get("xsd"), run_xsd)
            logger.debug(
                "Schematron checkbox: %s, Run Schematron: %s",
                request.form.get("schematron"),
                run_schematron,
            )

            # If neither is checked, run both by default
            if not run_xsd and not run_schematron:
                run_xsd = True
                run_schematron = True
                logger.debug("No validators specified, running both by default")

            if run_xsd:
                logger.debug("Running XSD validation...")
                validator = get_xsd_validator()
                xsd_result = validator.validate(tmp_path)
                results["xsd"] = xsd_result.to_dict()
                logger.debug(
                    "XSD validation complete: valid=%s, errors=%d",
                    xsd_result.is_valid,
                    len(xsd_result.errors),
                )

            if run_schematron:
                logger.debug("Running Schematron validation...")
                validator = get_schematron_validator()
                schematron_result = validator.validate(tmp_path)
                results["schematron"] = schematron_result.to_dict()
                logger.debug(
                    "Schematron validation complete: valid=%s, errors=%d",
                    schematron_result.is_valid,
                    len(schematron_result.errors),
                )

            logger.debug("Returning %d validation results", len(results))
            return jsonify(results)

        except Exception as e:
            logger.exception("Validation error: %s", e)
            return jsonify({"error": str(e)}), 500

        finally:
            # Clean up temp file
            tmp_path.unlink(missing_ok=True)

    @app.route("/api/generate", methods=["POST"])
    def api_generate():
        """Generate a sample C-CDA document."""
        data = request.get_json()
        document_type = data.get("document_type", "ccd")
        sections = data.get("sections", [])

        try:
            from ccdakit.cli.commands.generate import _generate_document

            doc = _generate_document(document_type, sections)
            xml_string = doc.to_xml_string(pretty=True)

            return jsonify({"xml": xml_string})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/convert", methods=["POST"])
    def api_convert():
        """Convert C-CDA XML to HTML using XSLT."""
        # Handle file upload or textarea content
        content = None
        if "file" in request.files and request.files["file"].filename:
            file = request.files["file"]
            content = file.read()
        elif "content" in request.form and request.form["content"]:
            content = request.form["content"].encode("utf-8")
        else:
            return jsonify({"error": "No file or content provided"}), 400

        from ccdakit.cli.commands.convert import _transform_with_official_stylesheet

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                tmp.write(content)
                tmp_path = Path(tmp.name)

            # Transform using official HL7 CDA stylesheet
            html_content = _transform_with_official_stylesheet(tmp_path)

            # Clean up
            tmp_path.unlink(missing_ok=True)

            return jsonify({"html": html_content})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/compare", methods=["POST"])
    def api_compare():
        """Compare two C-CDA documents."""
        from lxml import etree

        # Handle first document
        content1 = None
        name1 = "Document 1"
        if "file1" in request.files and request.files["file1"].filename:
            file1 = request.files["file1"]
            content1 = file1.read()
            name1 = file1.filename
        elif "content1" in request.form and request.form["content1"]:
            content1 = request.form["content1"].encode("utf-8")
        else:
            return jsonify({"error": "First document not provided"}), 400

        # Handle second document
        content2 = None
        name2 = "Document 2"
        if "file2" in request.files and request.files["file2"].filename:
            file2 = request.files["file2"]
            content2 = file2.read()
            name2 = file2.filename
        elif "content2" in request.form and request.form["content2"]:
            content2 = request.form["content2"].encode("utf-8")
        else:
            return jsonify({"error": "Second document not provided"}), 400

        try:
            tree1 = etree.fromstring(content1)
            tree2 = etree.fromstring(content2)

            data1 = _extract_comparison_data(tree1)
            data2 = _extract_comparison_data(tree2)

            comparison = _compare_documents(data1, data2)

            return jsonify(
                {
                    "comparison": comparison,
                    "file1_name": name1,
                    "file2_name": name2,
                }
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
