# CLI Tool Guide

ccdakit provides a powerful command-line interface for working with C-CDA documents. The CLI offers tools for validation, document generation, format conversion, comparison, and a web-based UI.

## Installation

After installing ccdakit, the `ccdakit` command will be available in your terminal:

```bash
pip install ccdakit
# or
uv pip install ccdakit
```

## Commands Overview

```bash
$ ccdakit --help

CLI tool for working with HL7 C-CDA clinical documents

Commands:
  validate   Validate a C-CDA document using XSD and/or Schematron rules
  generate   Generate a sample C-CDA document for testing
  convert    Convert a C-CDA XML document to human-readable HTML
  compare    Compare two C-CDA documents and highlight differences
  serve      Start the web UI server for interactive C-CDA operations
  version    Show the ccdakit version
```

## Validate Command

Validate C-CDA documents against XSD schemas and Schematron rules.

### Basic Usage

```bash
# Validate with both XSD and Schematron (default)
ccdakit validate document.xml

# Validate with XSD only
ccdakit validate document.xml --no-schematron

# Validate with Schematron only
ccdakit validate document.xml --no-xsd
```

### Output Formats

```bash
# Text output (default)
ccdakit validate document.xml

# JSON output
ccdakit validate document.xml --output-format json

# HTML report
ccdakit validate document.xml --output-format html
```

### Example Output

```
════════════════════════════════════════════════════════════════════════════════
Validation Summary
════════════════════════════════════════════════════════════════════════════════
XSD: PASSED
  Errors: 0, Warnings: 0

SCHEMATRON: PASSED
  Errors: 0, Warnings: 0

════════════════════════════════════════════════════════════════════════════════
✓ Document is valid!
════════════════════════════════════════════════════════════════════════════════
```

## Generate Command

Generate sample C-CDA documents with realistic test data for development and testing.

### Basic Usage

```bash
# Generate a Continuity of Care Document (CCD)
ccdakit generate ccd

# Generate a Discharge Summary
ccdakit generate discharge-summary

# Specify output file
ccdakit generate ccd --output my_document.xml
```

### Selecting Sections

```bash
# Include specific sections
ccdakit generate ccd --sections "problems,medications,allergies"

# Interactive mode - prompts for section selection
ccdakit generate ccd --interactive
```

### Available Sections

**Core Clinical Sections:**
- `problems` - Problems Section
- `medications` - Medications Section
- `allergies` - Allergies and Intolerances Section
- `immunizations` - Immunizations Section
- `vital-signs` - Vital Signs Section
- `procedures` - Procedures Section
- `results` - Results Section
- `social-history` - Social History Section
- `encounters` - Encounters Section

**Extended Clinical Sections:**
- `goals` - Goals Section
- `functional-status` - Functional Status Section
- `mental-status` - Mental Status Section
- `family-history` - Family History Section
- `health-concerns` - Health Concerns Section
- `health-status-evaluations` - Health Status Evaluations and Outcomes Section
- `past-medical-history` - Past Medical History Section
- `physical-exam` - Physical Exam Section
- `assessment-and-plan` - Assessment and Plan Section

**Specialized/Administrative Sections:**
- `plan-of-treatment` - Plan of Treatment Section
- `advance-directives` - Advance Directives Section
- `medical-equipment` - Medical Equipment Section
- `admission-medications` - Admission Medications Section
- `discharge-medications` - Discharge Medications Section
- `hospital-discharge-instructions` - Hospital Discharge Instructions Section
- `payers` - Payers Section
- `nutrition` - Nutrition Section
- `reason-for-visit` - Reason for Visit Section
- `chief-complaint-reason-for-visit` - Chief Complaint and Reason for Visit Section
- `interventions` - Interventions Section

**Hospital and Surgical Sections:**
- `admission-diagnosis` - Admission Diagnosis Section
- `discharge-diagnosis` - Discharge Diagnosis Section
- `hospital-course` - Hospital Course Section
- `instructions` - Instructions Section
- `anesthesia` - Anesthesia Section
- `postoperative-diagnosis` - Postoperative Diagnosis Section
- `preoperative-diagnosis` - Preoperative Diagnosis Section
- `complications` - Complications Section
- `discharge-studies` - Hospital Discharge Studies Summary Section
- `medications-administered` - Medications Administered Section

### Example

```bash
$ ccdakit generate ccd --output test.xml

╭─────────────────────────────────────────╮
│ Generating: Continuity of Care Document │
╰─────────────────────────────────────────╯

Generating test data...

✓ Document generated successfully!
Output: test.xml

════════════════════════════════════════════════════════════════════════════════
Document Summary
════════════════════════════════════════════════════════════════════════════════
Sections included: 3
  • Problems Section
  • Medications Section
  • Allergies and Intolerances Section

Use the 'validate' command to check document compliance:
  ccdakit validate test.xml
════════════════════════════════════════════════════════════════════════════════
```

## Convert Command

Convert C-CDA XML documents to human-readable HTML format using **XSLT transformation**. This ensures proper rendering of all C-CDA elements according to the CDA specification.

### Basic Usage

```bash
# Convert to HTML using XSLT transformation (uses minimal template by default)
ccdakit convert document.xml

# Use official HL7 CDA stylesheet
ccdakit convert document.xml --template official

# Specify output file
ccdakit convert document.xml --output report.html
```

### XSLT Templates

The convert command supports two XSLT templates:

**1. `minimal` (default)** - Custom stylesheet with modern design:
- Clean, modern layout with gradient headers
- Simplified design focused on readability
- Mobile-responsive with professional CSS styling
- Proper rendering of all C-CDA elements
- Print-friendly layout

**2. `official`** - Official HL7 CDA stylesheet from [HL7/CDA-core-xsl](https://github.com/HL7/CDA-core-xsl):
- Industry-standard HL7 rendering
- Used by validators and healthcare systems
- XHTML 1.0 Strict output
- Auto-downloads on first use (includes dependencies)
- Follows HL7 specifications exactly

### Example

```bash
$ ccdakit convert test.xml

Converting: test.xml
Applying XSLT transformation...
✓ Converted successfully!
Output: test.html
Open in browser to view the rendered document
```

### How It Works

The conversion uses **XSLT (Extensible Stylesheet Language Transformations)** to properly transform C-CDA XML to HTML. This is the standard approach for rendering C-CDA documents and ensures:

- All narrative blocks are rendered correctly
- Tables, lists, and formatted text are preserved
- Medical terminology and codes are displayed properly
- Document structure follows C-CDA semantics
- Output is identical to what healthcare validators produce

The generated HTML includes:
- Patient demographics in a clean, readable format
- All document sections with proper styling
- Narrative text with tables rendered as HTML tables
- Color-coded headers and sections
- Responsive design for viewing on any device
- Print-friendly layout

## Compare Command

Compare two C-CDA documents and identify differences.

### Basic Usage

```bash
# Compare two documents (text output)
ccdakit compare document1.xml document2.xml

# Generate HTML comparison report
ccdakit compare document1.xml document2.xml --format html

# Specify output file
ccdakit compare document1.xml document2.xml --output comparison.html
```

### What Gets Compared

- Patient demographics
- Document metadata
- Sections present in each document
- Entry counts in each section

### Example Output

```
════════════════════════════════════════════════════════════════════════════════
Document Comparison Report
════════════════════════════════════════════════════════════════════════════════

✓ Patient demographics are identical

Sections with Different Entry Counts:
┌────────────────────────────────┬─────────────────┬─────────────────┐
│ Section                        │ File 1 Entries  │ File 2 Entries  │
├────────────────────────────────┼─────────────────┼─────────────────┤
│ Medications Section            │ 5               │ 7               │
│ Problems Section               │ 3               │ 4               │
└────────────────────────────────┴─────────────────┴─────────────────┘

════════════════════════════════════════════════════════════════════════════════
Found 2 differences
════════════════════════════════════════════════════════════════════════════════
```

## Serve Command

Start a web-based UI for interactive C-CDA operations.

### Basic Usage

```bash
# Start server on default port (8000)
ccdakit serve

# Specify custom host and port
ccdakit serve --host 0.0.0.0 --port 5000

# Enable debug mode
ccdakit serve --debug
```

### Web UI Features

Once the server is running, open your browser to `http://localhost:8000` to access:

1. **Validate Tool**
   - Drag-and-drop XML file upload
   - Real-time validation with XSD and Schematron
   - Visual display of errors and warnings

2. **Generate Tool**
   - Interactive form for document generation
   - Select document type and sections
   - Download generated XML

3. **Convert Tool**
   - Upload XML and view as HTML
   - Download HTML version
   - In-browser preview

4. **Compare Tool**
   - Upload two documents
   - View side-by-side comparison
   - Highlight differences

### Example

```bash
$ ccdakit serve

Starting ccdakit web UI...
Server: http://127.0.0.1:8000
Press Ctrl+C to stop the server

 * Serving Flask app 'app'
 * Running on http://127.0.0.1:8000
```

## Version Command

Display the installed ccdakit version:

```bash
$ ccdakit version
ccdakit version 0.1.0a1
```

## Common Workflows

### Development Workflow

```bash
# 1. Generate a test document
ccdakit generate ccd --output test.xml

# 2. Validate the document
ccdakit validate test.xml

# 3. Convert to HTML for review
ccdakit convert test.xml
```

### Quality Assurance Workflow

```bash
# 1. Validate before and after changes
ccdakit validate original.xml > before.txt
ccdakit validate modified.xml > after.txt

# 2. Compare documents
ccdakit compare original.xml modified.xml --format html

# 3. Review HTML comparison report in browser
```

### Testing Workflow

```bash
# 1. Start web UI for interactive testing
ccdakit serve

# 2. Use browser to:
#    - Generate test documents with different sections
#    - Validate against schemas
#    - View human-readable HTML output
```

## Tips and Best Practices

1. **Use the web UI for exploratory work**: The `serve` command provides an intuitive interface perfect for learning and experimentation.

2. **Automate with the CLI**: Use the command-line tools in scripts and CI/CD pipelines for automated validation and testing.

3. **Generate test data early**: Create sample documents during development to test integrations before real data is available.

4. **Validate frequently**: Run validation after each significant change to catch errors early.

5. **Compare for regression testing**: Use the compare command to ensure new changes don't accidentally modify existing data.

## Troubleshooting

### Command Not Found

If `ccdakit` command is not found after installation:

```bash
# Reinstall in development mode
pip install -e .

# Or ensure your Python scripts directory is in PATH
export PATH="$PATH:$(python -m site --user-base)/bin"
```

### Validation Schemas Not Found

The first time you run validation, schemas may need to be downloaded:

- **XSD schemas**: Download manually from HL7 and place in `schemas/` directory
- **Schematron files**: Auto-downloaded on first use (one-time ~63MB download)

### Import Errors

For test data generation, install the optional faker dependency:

```bash
pip install 'ccdakit[test-data]'
# or
pip install faker>=20.0.0
```

## Next Steps

- See the [Validation Guide](validation.md) for advanced validation techniques
- Check the [API Reference](../api/index.md) for programmatic usage
- Explore [Examples](../../examples/) for more use cases
