"""Protocol for nutrition data.

This module defines the protocols (interfaces) for nutrition objects.
Any object that implements these protocols can be passed to the nutrition builders.
"""

from datetime import date, datetime
from typing import Optional, Protocol, Sequence


class NutritionAssessmentProtocol(Protocol):
    """Protocol for a nutrition assessment observation.

    Defines the interface that nutrition assessment objects must implement to be
    used with the NutritionAssessment builder.

    Attributes:
        assessment_type: Type of nutrition assessment (e.g., "Diet followed", "Nutrition intake")
        code: SNOMED CT code for the assessment
        value: Assessment value/finding
        value_code: Optional SNOMED CT code for the value
        date: Date and time the assessment was made
    """

    assessment_type: str
    code: str
    value: str
    value_code: Optional[str]
    date: date | datetime


class NutritionalStatusProtocol(Protocol):
    """Protocol for a nutritional status observation.

    Defines the interface for nutritional status observations that describe
    the overall nutritional status of the patient.

    Attributes:
        status: Nutritional status description (e.g., "Well nourished", "Malnourished")
        status_code: Code for nutritional status from Nutritional Status value set
        date: Date and time when status was observed
        assessments: List of nutrition assessments supporting this status
    """

    status: str
    status_code: str
    date: date | datetime
    assessments: Sequence[NutritionAssessmentProtocol]
