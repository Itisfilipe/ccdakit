"""Convert command implementation using XSLT transformation."""

import sys
from pathlib import Path
from typing import Optional

from lxml import etree
from rich.console import Console


console = Console()


def convert_command(
    file_path: Path,
    to: str = "html",
    output: Optional[Path] = None,
    template: str = "minimal",
) -> None:
    """
    Convert a C-CDA XML document to human-readable format using XSLT.

    Args:
        file_path: Path to the C-CDA XML file
        to: Target format (currently only 'html')
        output: Output file path
        template: XSLT template to use ('official' for HL7 CDA stylesheet, 'minimal' for custom)
    """
    # Validate file exists
    if not file_path.exists():
        console.print(f"[red]Error:[/red] File not found: {file_path}")
        sys.exit(1)

    if to != "html":
        console.print(f"[red]Error:[/red] Unsupported format: {to}")
        console.print("Currently only 'html' format is supported.")
        sys.exit(1)

    # Parse XML to validate it
    console.print(f"[cyan]Converting:[/cyan] {file_path.name}")
    try:
        etree.parse(str(file_path))
    except etree.XMLSyntaxError as e:
        console.print(f"[red]Error parsing XML:[/red] {e}")
        sys.exit(1)

    # Perform XSLT transformation
    console.print("[dim]Applying XSLT transformation...[/dim]")
    try:
        if template == "official":
            # Use official HL7 CDA stylesheet
            html_content = _transform_with_official_stylesheet(file_path)
        else:
            # Use custom minimal stylesheet
            html_content = _transform_with_custom_stylesheet(file_path)
    except Exception as e:
        console.print(f"[red]Error during transformation:[/red] {e}")
        sys.exit(1)

    # Determine output path
    if output is None:
        output = file_path.with_suffix(".html")

    # Write to file
    try:
        output.write_text(html_content)
        console.print("[green]✓[/green] Converted successfully!")
        console.print(f"[green]Output:[/green] {output.absolute()}")
        console.print("[dim]Open in browser to view the rendered document[/dim]")
    except Exception as e:
        console.print(f"[red]Error writing file:[/red] {e}")
        sys.exit(1)


def _transform_with_official_stylesheet(xml_path: Path) -> str:
    """Transform using official HL7 CDA stylesheet from github.com/HL7/CDA-core-xsl."""
    from ccdakit.utils.xslt import transform_cda_to_html

    try:
        return transform_cda_to_html(xml_path)
    except FileNotFoundError:
        console.print(
            "[yellow]Note:[/yellow] Downloading official HL7 CDA stylesheet (one-time setup)..."
        )
        console.print("[dim]Source: https://github.com/HL7/CDA-core-xsl[/dim]")
        from ccdakit.utils.xslt import download_cda_stylesheet

        download_cda_stylesheet()
        return transform_cda_to_html(xml_path)


def _transform_with_custom_stylesheet(xml_path: Path) -> str:
    """Transform using custom minimal XSLT stylesheet."""
    # Create a simple custom XSLT for minimal output
    xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:cda="urn:hl7-org:v3"
    xmlns:sdtc="urn:hl7-org:sdtc">

<xsl:output method="html" encoding="UTF-8" indent="yes"/>

<xsl:template match="/">
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title><xsl:value-of select="cda:ClinicalDocument/cda:title"/></title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .header .meta {
            opacity: 0.9;
            font-size: 14px;
        }
        .patient-info {
            background: #f8f9fa;
            padding: 25px 30px;
            border-bottom: 2px solid #e9ecef;
        }
        .patient-info h2 {
            font-size: 20px;
            margin-bottom: 15px;
            color: #495057;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        .info-item {
            display: flex;
            flex-direction: column;
        }
        .info-label {
            font-size: 12px;
            text-transform: uppercase;
            color: #6c757d;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .info-value {
            font-size: 15px;
            color: #212529;
        }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 35px;
            page-break-inside: avoid;
        }
        .section:last-child {
            margin-bottom: 0;
        }
        .section-title {
            font-size: 22px;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #667eea;
        }
        .section-content {
            padding: 15px 0;
        }
        .narrative {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        table th {
            background: #667eea;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: 600;
        }
        table td {
            padding: 10px;
            border-bottom: 1px solid #e9ecef;
        }
        table tr:hover {
            background: #f8f9fa;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #6c757d;
            font-size: 13px;
            border-top: 1px solid #e9ecef;
        }
        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><xsl:value-of select="cda:ClinicalDocument/cda:title"/></h1>
            <div class="meta">
                Document Date: <xsl:call-template name="format-date">
                    <xsl:with-param name="date" select="cda:ClinicalDocument/cda:effectiveTime/@value"/>
                </xsl:call-template>
            </div>
        </div>

        <div class="patient-info">
            <h2>Patient Information</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Name</div>
                    <div class="info-value">
                        <xsl:value-of select="cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:name/cda:given"/>
                        <xsl:text> </xsl:text>
                        <xsl:value-of select="cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:name/cda:family"/>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">Gender</div>
                    <div class="info-value">
                        <xsl:value-of select="cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:administrativeGenderCode/@displayName"/>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">Date of Birth</div>
                    <div class="info-value">
                        <xsl:call-template name="format-date">
                            <xsl:with-param name="date" select="cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:patient/cda:birthTime/@value"/>
                        </xsl:call-template>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">MRN</div>
                    <div class="info-value">
                        <xsl:value-of select="cda:ClinicalDocument/cda:recordTarget/cda:patientRole/cda:id/@extension"/>
                    </div>
                </div>
            </div>
        </div>

        <div class="content">
            <xsl:apply-templates select="cda:ClinicalDocument/cda:component/cda:structuredBody/cda:component/cda:section"/>
        </div>

        <div class="footer">
            Generated by ccdakit CLI
        </div>
    </div>
</body>
</html>
</xsl:template>

<xsl:template match="cda:section">
    <div class="section">
        <h2 class="section-title">
            <xsl:value-of select="cda:title"/>
        </h2>
        <div class="section-content">
            <xsl:if test="cda:text">
                <div class="narrative">
                    <xsl:apply-templates select="cda:text" mode="narrative"/>
                </div>
            </xsl:if>
            <xsl:apply-templates select="cda:component/cda:section"/>
        </div>
    </div>
</xsl:template>

<xsl:template match="cda:text" mode="narrative">
    <xsl:apply-templates mode="narrative"/>
</xsl:template>

<xsl:template match="cda:table" mode="narrative">
    <table>
        <xsl:apply-templates select="cda:thead" mode="narrative"/>
        <xsl:apply-templates select="cda:tbody" mode="narrative"/>
    </table>
</xsl:template>

<xsl:template match="cda:thead" mode="narrative">
    <thead>
        <xsl:apply-templates mode="narrative"/>
    </thead>
</xsl:template>

<xsl:template match="cda:tbody" mode="narrative">
    <tbody>
        <xsl:apply-templates mode="narrative"/>
    </tbody>
</xsl:template>

<xsl:template match="cda:tr" mode="narrative">
    <tr>
        <xsl:apply-templates mode="narrative"/>
    </tr>
</xsl:template>

<xsl:template match="cda:th" mode="narrative">
    <th>
        <xsl:apply-templates mode="narrative"/>
    </th>
</xsl:template>

<xsl:template match="cda:td" mode="narrative">
    <td>
        <xsl:apply-templates mode="narrative"/>
    </td>
</xsl:template>

<xsl:template match="cda:paragraph" mode="narrative">
    <p>
        <xsl:apply-templates mode="narrative"/>
    </p>
</xsl:template>

<xsl:template match="cda:list" mode="narrative">
    <ul>
        <xsl:apply-templates mode="narrative"/>
    </ul>
</xsl:template>

<xsl:template match="cda:item" mode="narrative">
    <li>
        <xsl:apply-templates mode="narrative"/>
    </li>
</xsl:template>

<xsl:template match="cda:content" mode="narrative">
    <xsl:choose>
        <xsl:when test="@styleCode='Bold'">
            <strong><xsl:apply-templates mode="narrative"/></strong>
        </xsl:when>
        <xsl:when test="@styleCode='Italics'">
            <em><xsl:apply-templates mode="narrative"/></em>
        </xsl:when>
        <xsl:otherwise>
            <xsl:apply-templates mode="narrative"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="cda:br" mode="narrative">
    <br/>
</xsl:template>

<xsl:template name="format-date">
    <xsl:param name="date"/>
    <xsl:choose>
        <xsl:when test="string-length($date) >= 8">
            <xsl:variable name="year" select="substring($date, 1, 4)"/>
            <xsl:variable name="month" select="substring($date, 5, 2)"/>
            <xsl:variable name="day" select="substring($date, 7, 2)"/>
            <xsl:value-of select="concat($month, '/', $day, '/', $year)"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$date"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>"""

    # Parse XML and XSLT
    xml_doc = etree.parse(str(xml_path))
    xslt_doc = etree.fromstring(xslt_content.encode("utf-8"))
    transform = etree.XSLT(xslt_doc)

    # Apply transformation
    result = transform(xml_doc)

    return str(result)
