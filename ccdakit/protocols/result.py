"""Protocol for lab results and diagnostic test results.

This module defines the protocols (interfaces) for lab result objects.
Any object that implements these protocols can be passed to the result builders.
"""

from datetime import date, datetime
from typing import Optional, Protocol, Sequence


class ResultObservationProtocol(Protocol):
    """Protocol for a single lab result observation.

    Defines the interface that result observation objects must implement to be
    used with the ResultObservation builder.

    Attributes:
        test_name: Name of the test (e.g., "Glucose", "Hemoglobin")
        test_code: LOINC code for the test
        value: Measured value (numeric or text)
        unit: Unit of measurement (e.g., "mg/dL", "g/dL"). Optional for coded/text values.
        status: Status of the result (e.g., "completed", "preliminary", "final")
        effective_time: Date and time the test was performed
        value_type: Type of value - "PQ" (physical quantity), "CD" (coded), or "ST" (string).
                   Defaults to "PQ" if unit is provided, otherwise "ST".
        interpretation: Optional interpretation code (e.g., "N" for normal, "H" for high, "L" for low)
        reference_range_low: Optional lower bound of reference range
        reference_range_high: Optional upper bound of reference range
        reference_range_unit: Optional unit for reference range (should match value unit)
    """

    test_name: str
    test_code: str
    value: str
    unit: Optional[str]
    status: str
    effective_time: date | datetime
    value_type: Optional[str]
    interpretation: Optional[str]
    reference_range_low: Optional[str]
    reference_range_high: Optional[str]
    reference_range_unit: Optional[str]


class ResultOrganizerProtocol(Protocol):
    """Protocol for a group of related lab results (e.g., a lab panel).

    Defines the interface for a result organizer that groups related test results.

    Attributes:
        panel_name: Name of the panel (e.g., "Complete Blood Count", "Basic Metabolic Panel")
        panel_code: LOINC code for the panel
        status: Status of the organizer (e.g., "completed", "active")
        effective_time: Date and time when the panel was collected/performed
        results: Sequence of result observations in this panel
    """

    panel_name: str
    panel_code: str
    status: str
    effective_time: date | datetime
    results: Sequence[ResultObservationProtocol]
