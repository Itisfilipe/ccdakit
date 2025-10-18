# Health Status Evaluations and Outcomes Section

**OID:** 2.16.840.1.113883.10.20.22.2.61
**Version:** (No extension)
**Badge:** Specialized Section

## Overview

The Health Status Evaluations and Outcomes Section represents outcomes of the patient's health status. These assessed outcomes are represented as statuses at points in time. It also includes outcomes of care from the interventions used to treat the patient, related to established care plan goals and/or interventions.

This section is used to document how the patient is progressing toward their health goals and the effectiveness of care interventions. It provides objective measures of health status changes over time.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.61
- **Extension:** None
- **Conformance:** MAY
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 11383-7 "Patient Problem Outcome"

## Protocol Requirements

### OutcomeObservationProtocol
```python
from typing import Protocol, Optional
from datetime import date

class ProgressTowardGoal(Protocol):
    achievement_display_name: str  # Progress description (e.g., "Improving", "Met Goal")

class OutcomeObservationProtocol(Protocol):
    code: str                                    # Outcome code
    display_name: str                            # Outcome description
    value: str                                   # Outcome value/result
    value_unit: Optional[str]                    # Unit of measurement
    effective_time: Optional[date]               # When outcome was assessed
    progress_toward_goal: Optional[ProgressTowardGoal]  # Goal achievement status
```

## Code Example

### Basic Health Status Outcomes
```python
from ccdakit import HealthStatusEvaluationsAndOutcomesSection, CDAVersion
from datetime import date

# Define health status outcomes
outcomes = [
    {
        "code": "77137-4",
        "display_name": "Blood pressure goal attainment",
        "value": "Goal met",
        "value_unit": None,
        "effective_time": date(2025, 1, 15),
        "progress_toward_goal": {
            "achievement_display_name": "Goal Met"
        }
    },
    {
        "code": "77141-6",
        "display_name": "HbA1c goal attainment",
        "value": "Improving",
        "value_unit": None,
        "effective_time": date(2025, 1, 15),
        "progress_toward_goal": {
            "achievement_display_name": "Improving"
        }
    }
]

section = HealthStatusEvaluationsAndOutcomesSection(
    outcomes=outcomes,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Outcomes with Measurements
```python
from ccdakit import HealthStatusEvaluationsAndOutcomesSection, CDAVersion
from datetime import date

# Include specific measurement values
outcomes = [
    {
        "code": "8480-6",
        "display_name": "Systolic Blood Pressure",
        "value": "128",
        "value_unit": "mm[Hg]",
        "effective_time": date(2025, 1, 18),
        "progress_toward_goal": {
            "achievement_display_name": "Goal Met"
        }
    },
    {
        "code": "4548-4",
        "display_name": "Hemoglobin A1c",
        "value": "7.2",
        "value_unit": "%",
        "effective_time": date(2025, 1, 10),
        "progress_toward_goal": {
            "achievement_display_name": "Improving"
        }
    },
    {
        "code": "29463-7",
        "display_name": "Body Weight",
        "value": "82",
        "value_unit": "kg",
        "effective_time": date(2025, 1, 18),
        "progress_toward_goal": {
            "achievement_display_name": "Goal Met"
        }
    }
]

section = HealthStatusEvaluationsAndOutcomesSection(
    outcomes=outcomes,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Functional Status Outcomes
```python
from ccdakit import HealthStatusEvaluationsAndOutcomesSection, CDAVersion
from datetime import date

# Document functional improvement outcomes
outcomes = [
    {
        "code": "83254-9",
        "display_name": "Ability to walk independently",
        "value": "Improved from baseline",
        "value_unit": None,
        "effective_time": date(2025, 1, 20),
        "progress_toward_goal": {
            "achievement_display_name": "Improving"
        }
    },
    {
        "code": "83242-4",
        "display_name": "Activities of daily living independence",
        "value": "Modified independent",
        "value_unit": None,
        "effective_time": date(2025, 1, 20),
        "progress_toward_goal": {
            "achievement_display_name": "Improving"
        }
    }
]

section = HealthStatusEvaluationsAndOutcomesSection(
    outcomes=outcomes,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Comprehensive Outcome Tracking
```python
from ccdakit import HealthStatusEvaluationsAndOutcomesSection, CDAVersion
from datetime import date

# Track multiple outcomes across different domains
outcomes = [
    # Clinical outcomes
    {
        "code": "8480-6",
        "display_name": "Systolic Blood Pressure - Goal Attainment",
        "value": "132",
        "value_unit": "mm[Hg]",
        "effective_time": date(2025, 1, 15),
        "progress_toward_goal": {
            "achievement_display_name": "Goal Met"
        }
    },
    {
        "code": "4548-4",
        "display_name": "Hemoglobin A1c - Diabetes Control",
        "value": "6.8",
        "value_unit": "%",
        "effective_time": date(2025, 1, 12),
        "progress_toward_goal": {
            "achievement_display_name": "Goal Met"
        }
    },
    # Functional outcomes
    {
        "code": "83254-9",
        "display_name": "Walking Distance - Mobility Goal",
        "value": "Can walk 100 meters without rest",
        "value_unit": None,
        "effective_time": date(2025, 1, 18),
        "progress_toward_goal": {
            "achievement_display_name": "Improving"
        }
    },
    # Quality of life outcomes
    {
        "code": "72514-3",
        "display_name": "Pain severity - Pain Management Goal",
        "value": "3",
        "value_unit": "on 0-10 scale",
        "effective_time": date(2025, 1, 18),
        "progress_toward_goal": {
            "achievement_display_name": "Improving"
        }
    },
    # Behavioral outcomes
    {
        "code": "72166-2",
        "display_name": "Tobacco use status - Smoking Cessation Goal",
        "value": "Former smoker",
        "value_unit": None,
        "effective_time": date(2025, 1, 15),
        "progress_toward_goal": {
            "achievement_display_name": "Goal Met"
        }
    }
]

section = HealthStatusEvaluationsAndOutcomesSection(
    outcomes=outcomes,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Health Status Evaluations and Outcomes Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.61.html)

## Best Practices

1. **Link to Goals**: Always relate outcomes to specific health goals when possible to demonstrate progress.

2. **Use Standard Codes**: Use LOINC codes for outcome observations to ensure interoperability.

3. **Include Measurements**: When possible, include actual measurement values with units, not just qualitative assessments.

4. **Document Trends**: Track outcomes over time to show progression (improving, worsening, stable).

5. **Be Objective**: Focus on measurable, objective outcomes rather than subjective opinions.

6. **Multiple Domains**: Document outcomes across all relevant domains (clinical, functional, quality of life, behavioral).

7. **Timestamp Assessments**: Always include the date when the outcome was assessed.

8. **Coordinate with Care Plan**: Outcomes should align with goals documented in the Goals section and interventions in the Interventions section.

9. **Update Regularly**: Reassess and document outcomes at regular intervals appropriate to the condition.

10. **Document Both Success and Challenges**: Include outcomes showing both goal achievement and areas where goals are not being met.

## Progress Toward Goal Values

Common values for progress_toward_goal.achievement_display_name:

- **Goal Met**: Target outcome has been achieved
- **Improving**: Moving in positive direction toward goal
- **Worsening**: Moving away from goal achievement
- **Stable**: No significant change in status
- **Unable to Assess**: Cannot determine progress at this time
- **Goal Not Met**: Target not achieved by expected timeframe
- **Goal Modified**: Original goal changed based on patient status
- **Goal Discontinued**: Goal no longer relevant or appropriate

## Outcome Observation Types

### Clinical Outcomes
- Lab values (HbA1c, lipids, kidney function)
- Vital signs (blood pressure, weight, heart rate)
- Symptom scores (pain scales, depression scales)
- Disease-specific measures (COPD assessment, heart failure functional class)

### Functional Outcomes
- Activities of daily living (ADL) status
- Instrumental activities of daily living (IADL) status
- Mobility assessments
- Fall risk assessments
- Cognitive function measures

### Quality of Life Outcomes
- Patient-reported outcome measures
- Satisfaction scores
- Quality of life scales
- Pain and symptom burden

### Behavioral Outcomes
- Medication adherence rates
- Lifestyle modifications (diet, exercise, smoking)
- Self-management behaviors
- Healthcare utilization patterns

### Safety Outcomes
- Adverse events
- Hospital readmissions
- Emergency department visits
- Falls or other safety incidents

## Linking Outcomes to Care Plan Components

Outcomes should demonstrate the effectiveness of:
- **Goals**: Progress toward achieving stated health goals
- **Interventions**: Impact of interventions performed
- **Medications**: Therapeutic effectiveness of medications
- **Procedures**: Results of procedures performed

This comprehensive documentation creates a clear picture of care quality and patient progress over time.
