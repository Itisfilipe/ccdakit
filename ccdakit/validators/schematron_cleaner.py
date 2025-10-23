"""Utility for cleaning HL7 C-CDA Schematron files to be compatible with lxml.

The official HL7 C-CDA R2.1 Schematron file contains IDREF errors - it references
pattern IDs that don't exist in the document. This causes lxml's strict ISO
Schematron parser to fail validation.

This module provides utilities to clean the Schematron file by removing invalid
pattern references, making it compatible with lxml while preserving all actual
validation rules.
"""

import logging
from pathlib import Path
from typing import Optional, Set, Tuple

from lxml import etree


logger = logging.getLogger(__name__)


class SchematronCleaner:
    """
    Cleans HL7 C-CDA Schematron files to fix IDREF errors.

    The official HL7 Schematron file references patterns that don't exist,
    causing lxml's strict parser to fail. This cleaner removes those invalid
    references while preserving all actual validation rules.
    """

    # Schematron namespace
    SCH_NS = "http://purl.oclc.org/dsdl/schematron"

    def __init__(self, schematron_path: Path):
        """
        Initialize cleaner with path to Schematron file.

        Args:
            schematron_path: Path to the Schematron file to clean
        """
        self.schematron_path = Path(schematron_path)
        if not self.schematron_path.exists():
            raise FileNotFoundError(f"Schematron file not found: {schematron_path}")

    def clean(self, output_path: Optional[Path] = None, quiet: bool = False) -> Tuple[Path, dict]:
        """
        Clean the Schematron file by removing invalid pattern references.

        Args:
            output_path: Path for cleaned file. If None, uses same directory
                with '_cleaned' suffix.
            quiet: If True, suppress logging output

        Returns:
            Tuple of (output_path, stats_dict) where stats_dict contains:
                - 'total_patterns': Total patterns defined
                - 'total_references': Total pattern references in phases
                - 'invalid_references': Number of invalid references removed
                - 'errors_phase_cleaned': References removed from errors phase
                - 'warnings_phase_cleaned': References removed from warnings phase

        Raises:
            FileNotFoundError: If schematron file doesn't exist
            etree.XMLSyntaxError: If schematron file is malformed
        """
        # Parse Schematron file
        tree = etree.parse(str(self.schematron_path))
        root = tree.getroot()

        # Find all actual pattern IDs that exist
        actual_patterns = self._find_actual_patterns(root)

        if not quiet:
            logger.info(f"Found {len(actual_patterns)} actual patterns in Schematron")

        # Clean phases by removing invalid references
        stats = {
            "total_patterns": len(actual_patterns),
            "total_references": 0,
            "invalid_references": 0,
            "errors_phase_cleaned": 0,
            "warnings_phase_cleaned": 0,
        }

        for phase in root.findall(f".//{{{self.SCH_NS}}}phase"):
            phase_id = phase.get("id", "unknown")
            removed = self._clean_phase(phase, actual_patterns)
            stats["invalid_references"] += removed

            if phase_id == "errors":
                stats["errors_phase_cleaned"] = removed
            elif phase_id == "warnings":
                stats["warnings_phase_cleaned"] = removed

            if not quiet and removed > 0:
                logger.info(f"Removed {removed} invalid pattern references from phase '{phase_id}'")

        # Count remaining references
        for phase in root.findall(f".//{{{self.SCH_NS}}}phase"):
            refs = phase.findall(f"{{{self.SCH_NS}}}active")
            stats["total_references"] += len(refs)

        # Add comment to document explaining it was cleaned
        self._add_cleaning_comment(root)

        # Determine output path
        if output_path is None:
            output_path = self.schematron_path.parent / (
                self.schematron_path.stem + "_cleaned" + self.schematron_path.suffix
            )
        output_path = Path(output_path)

        # Write cleaned file
        tree.write(
            str(output_path),
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
        )

        if not quiet:
            logger.info(f"Cleaned Schematron saved to: {output_path}")
            logger.info(
                f"Summary: {stats['total_patterns']} patterns, "
                f"{stats['total_references']} valid references, "
                f"{stats['invalid_references']} invalid references removed"
            )

        return output_path, stats

    def _find_actual_patterns(self, root: etree._Element) -> Set[str]:
        """
        Find all pattern IDs that actually exist in the Schematron.

        Args:
            root: Root element of Schematron document

        Returns:
            Set of pattern IDs that are defined
        """
        patterns = set()

        # Find all <sch:pattern> elements and extract their IDs
        for pattern in root.findall(f".//{{{self.SCH_NS}}}pattern"):
            pattern_id = pattern.get("id")
            if pattern_id:
                patterns.add(pattern_id)

        return patterns

    def _clean_phase(self, phase: etree._Element, actual_patterns: Set[str]) -> int:
        """
        Remove invalid pattern references from a phase.

        Args:
            phase: Phase element to clean
            actual_patterns: Set of valid pattern IDs

        Returns:
            Number of invalid references removed
        """
        removed_count = 0

        # Find all <sch:active pattern="..."/> elements
        active_elements = phase.findall(f"{{{self.SCH_NS}}}active")

        for active in active_elements:
            pattern_ref = active.get("pattern")
            if pattern_ref and pattern_ref not in actual_patterns:
                # This reference points to a non-existent pattern - remove it
                phase.remove(active)
                removed_count += 1

        return removed_count

    def _add_cleaning_comment(self, root: etree._Element) -> None:
        """
        Add a comment to the document explaining it was auto-cleaned.

        Args:
            root: Root element of Schematron document
        """
        comment_text = """

    This file has been automatically processed to fix IDREF errors.

    The original HL7 C-CDA R2.1 Schematron file contains references to patterns
    that don't exist, which causes lxml's strict ISO Schematron parser to fail.

    This cleaned version has invalid pattern references removed from the phase
    definitions, making it compatible with lxml while preserving all actual
    validation rules.

    Original file: HL7_CCDA_R2.1.sch
    Source: https://github.com/HL7/CDA-ccda-2.1
    Cleaning tool: ccdakit.validators.schematron_cleaner

    """
        comment = etree.Comment(comment_text)

        # Insert comment as first child
        root.insert(0, comment)


def clean_schematron_file(
    schematron_path: Path, output_path: Optional[Path] = None, quiet: bool = False
) -> Tuple[Path, dict]:
    """
    Convenience function to clean a Schematron file.

    Args:
        schematron_path: Path to Schematron file to clean
        output_path: Path for cleaned file (default: same dir with '_cleaned' suffix)
        quiet: If True, suppress logging output

    Returns:
        Tuple of (output_path, stats_dict)

    Example:
        >>> from pathlib import Path
        >>> from ccdakit.validators.schematron_cleaner import clean_schematron_file
        >>>
        >>> input_file = Path("schemas/schematron/HL7_CCDA_R2.1.sch")
        >>> output_file, stats = clean_schematron_file(input_file)
        >>> print(f"Removed {stats['invalid_references']} invalid references")
    """
    cleaner = SchematronCleaner(schematron_path)
    return cleaner.clean(output_path=output_path, quiet=quiet)
