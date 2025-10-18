# Nutrition Section

**OID:** 2.16.840.1.113883.10.20.22.2.57
**Version:** (No extension)
**Badge:** Specialized Section

## Overview

The Nutrition Section represents diet and nutrition information including special diet requirements and restrictions (such as texture-modified diet, liquids only, or enteral feeding). It also represents the overall nutritional status of the patient and nutrition assessment findings.

This section is particularly important for patients with special dietary needs, those at risk for malnutrition, and those receiving nutrition support therapy.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.57
- **Extension:** None
- **Conformance:** MAY
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 61144-2 "Diet and nutrition"

## Protocol Requirements

### NutritionalStatusProtocol
```python
from typing import Protocol, Optional, List
from datetime import date, datetime

class NutritionAssessment(Protocol):
    assessment_type: str  # Type of assessment (e.g., "BMI", "Weight", "Albumin Level")
    value: str           # Assessment value

class NutritionalStatusProtocol(Protocol):
    status: str                      # Nutritional status (e.g., "Well nourished", "Malnourished")
    date: Union[date, datetime]     # Date of assessment
    assessments: List[NutritionAssessment]  # List of specific nutrition assessments
```

## Code Example

### Basic Nutritional Status
```python
from ccdakit import NutritionSection, CDAVersion
from datetime import date

# Define nutritional status observations
nutritional_statuses = [
    {
        "status": "Well nourished",
        "date": date(2025, 1, 15),
        "assessments": [
            {
                "assessment_type": "BMI",
                "value": "23.5 kg/m2"
            },
            {
                "assessment_type": "Weight",
                "value": "68 kg"
            }
        ]
    }
]

section = NutritionSection(
    nutritional_statuses=nutritional_statuses,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Multiple Nutrition Assessments
```python
from ccdakit import NutritionSection, CDAVersion
from datetime import date

nutritional_statuses = [
    {
        "status": "Moderate malnutrition",
        "date": date(2025, 1, 10),
        "assessments": [
            {
                "assessment_type": "BMI",
                "value": "17.8 kg/m2"
            },
            {
                "assessment_type": "Weight",
                "value": "52 kg"
            },
            {
                "assessment_type": "Albumin Level",
                "value": "2.8 g/dL"
            },
            {
                "assessment_type": "Dietary Intake",
                "value": "Poor - consuming less than 50% of meals"
            }
        ]
    }
]

section = NutritionSection(
    nutritional_statuses=nutritional_statuses,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Tracking Nutritional Status Over Time
```python
from ccdakit import NutritionSection, CDAVersion
from datetime import date

# Multiple status assessments showing progression
nutritional_statuses = [
    {
        "status": "Malnourished",
        "date": date(2025, 1, 1),
        "assessments": [
            {
                "assessment_type": "Weight",
                "value": "50 kg"
            },
            {
                "assessment_type": "BMI",
                "value": "17.2 kg/m2"
            }
        ]
    },
    {
        "status": "Improving nutritional status",
        "date": date(2025, 1, 15),
        "assessments": [
            {
                "assessment_type": "Weight",
                "value": "52 kg"
            },
            {
                "assessment_type": "BMI",
                "value": "17.9 kg/m2"
            }
        ]
    }
]

section = NutritionSection(
    nutritional_statuses=nutritional_statuses,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Special Dietary Needs
```python
from ccdakit import NutritionSection, CDAVersion
from datetime import date

nutritional_statuses = [
    {
        "status": "At nutritional risk - requires modified diet",
        "date": date(2025, 1, 20),
        "assessments": [
            {
                "assessment_type": "Diet Order",
                "value": "Mechanical soft diet"
            },
            {
                "assessment_type": "Fluid Consistency",
                "value": "Nectar thick liquids"
            },
            {
                "assessment_type": "Caloric Needs",
                "value": "2000 kcal/day"
            },
            {
                "assessment_type": "Protein Requirements",
                "value": "1.2 g/kg/day"
            }
        ]
    }
]

section = NutritionSection(
    nutritional_statuses=nutritional_statuses,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Nutrition Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.57.html)

## Best Practices

1. **Complete Assessment**: Document comprehensive nutritional assessments including BMI, weight, albumin levels, and dietary intake.

2. **Track Over Time**: Document serial assessments to show trends in nutritional status, especially for at-risk patients.

3. **Include Diet Orders**: Document current diet orders and texture modifications (e.g., pureed, mechanical soft).

4. **Specify Restrictions**: Clearly document dietary restrictions (e.g., low-sodium, diabetic, renal diet).

5. **Fluid Consistency**: For patients with dysphagia, document required fluid consistency (thin, nectar, honey, pudding).

6. **Caloric Requirements**: Include calculated caloric and protein requirements when relevant.

7. **Risk Factors**: Document risk factors for malnutrition (poor intake, weight loss, medical conditions).

8. **Supplementation**: Document nutritional supplements, enteral nutrition, or parenteral nutrition if applicable.

9. **Interdisciplinary Input**: Incorporate input from registered dietitians and nutritionists when available.

10. **Functional Impact**: Note how nutritional status affects function (e.g., "weakness limiting mobility").

## Common Nutritional Status Values

- **Well nourished**: Patient meeting nutritional needs
- **At risk for malnutrition**: Factors present that could lead to malnutrition
- **Mild malnutrition**: Some nutritional deficits present
- **Moderate malnutrition**: Significant nutritional deficits
- **Severe malnutrition**: Critical nutritional deficits requiring intervention
- **Overweight/Obese**: Excess body weight
- **Improving nutritional status**: Responding to interventions

## Common Assessment Types

- **BMI**: Body Mass Index (kg/m2)
- **Weight**: Current weight with trend
- **Albumin Level**: Serum albumin (g/dL)
- **Prealbumin**: More sensitive marker for acute changes
- **Dietary Intake**: Percentage of meals consumed
- **Diet Order**: Type of diet prescribed
- **Fluid Consistency**: Required liquid thickness
- **Caloric Needs**: Daily caloric requirements
- **Protein Requirements**: Daily protein needs (g/kg/day)
- **Swallowing Assessment**: Dysphagia screening results
- **Enteral Nutrition**: Type and rate of tube feeding
- **Parenteral Nutrition**: TPN formulation and rate
