# Working with Sections

ccdakit provides 29 complete clinical section builders.

> **Note**: For a comprehensive guide to each section with HL7 background, see the [HL7/C-CDA Guide](hl7-guide/sections/index.md)

## Available Sections

### ProblemsSection

Diagnoses, conditions, and health concerns.

```python
from ccdakit import ProblemsSection, CDAVersion

section = ProblemsSection(
    problems=problems_list,
    version=CDAVersion.R2_1
)
```

**Required Protocol Properties**:
- `name: str` - Problem name
- `code: str` - SNOMED or ICD-10 code
- `code_system: str` - "SNOMED" or "ICD10"
- `status: str` - "active", "inactive", "resolved"
- `onset_date: Optional[date]` - When problem started

### MedicationsSection

Current and historical medications.

```python
from ccdakit import MedicationsSection

section = MedicationsSection(
    medications=meds_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `name: str` - Medication name
- `code: str` - RxNorm code
- `status: str` - "active", "completed", "discontinued"
- `dosage: str` - e.g., "10 mg"
- `route: str` - e.g., "oral"
- `frequency: str` - e.g., "twice daily"

### AllergiesSection

Allergies and intolerances.

```python
from ccdakit import AllergiesSection

section = AllergiesSection(
    allergies=allergies_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `allergen: str` - Allergen name
- `code: str` - RxNorm, UNII, or SNOMED code
- `code_system: str` - Code system used
- `type: str` - "allergy" or "intolerance"
- `status: str` - "active" or "inactive"
- `reaction: Optional[str]` - Reaction description
- `severity: Optional[str]` - "mild", "moderate", "severe"

### ImmunizationsSection

Vaccination history.

```python
from ccdakit import ImmunizationsSection

section = ImmunizationsSection(
    immunizations=immunizations_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `vaccine_name: str` - Vaccine name
- `cvx_code: str` - CVX code
- `administration_date: date` - When given
- `status: str` - "completed", "refused", "not given"

### VitalSignsSection

Vital signs measurements with organizers.

```python
from ccdakit import VitalSignsSection

section = VitalSignsSection(
    organizers=vital_organizers,
    version=CDAVersion.R2_1
)
```

Each organizer contains multiple vital signs from same observation time.

### ProceduresSection

Medical procedures performed.

```python
from ccdakit import ProceduresSection

section = ProceduresSection(
    procedures=procedures_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `name: str` - Procedure name
- `code: str` - CPT or SNOMED code
- `code_system: str` - "CPT" or "SNOMED"
- `date: date` - Procedure date
- `status: str` - "completed", "aborted"

### ResultsSection

Laboratory results and panels.

```python
from ccdakit import ResultsSection

section = ResultsSection(
    organizers=result_organizers,
    version=CDAVersion.R2_1
)
```

Supports lab panels with multiple results.

### SocialHistorySection

Social history observations including smoking status.

```python
from ccdakit import SocialHistorySection

section = SocialHistorySection(
    smoking_statuses=smoking_list,
    version=CDAVersion.R2_1
)
```

### EncountersSection

Healthcare encounters.

```python
from ccdakit import EncountersSection

section = EncountersSection(
    encounters=encounters_list,
    version=CDAVersion.R2_1
)
```

### PastMedicalHistorySection

Past complaints, problems, and diagnoses up to the current complaint.

```python
from ccdakit import PastMedicalHistorySection

section = PastMedicalHistorySection(
    problems=problems_list,
    version=CDAVersion.R2_1
)
```

**Required Protocol Properties**:
- `name: str` - Problem name
- `code: str` - SNOMED or ICD-10 code
- `code_system: str` - Code system identifier
- `status: str` - Problem status
- `onset_date: Optional[date]` - When problem started

### GoalsSection

Patient health and treatment goals.

```python
from ccdakit import GoalsSection

section = GoalsSection(
    goals=goals_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `description: str` - Goal description
- `status: str` - Goal status
- `start_date: Optional[date]` - When goal was set
- `target_date: Optional[date]` - Target completion date
- `value: Optional[str]` - Target value

### HealthConcernsSection

Health concerns requiring attention and management.

```python
from ccdakit import HealthConcernsSection

section = HealthConcernsSection(
    health_concerns=concerns_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `name: str` - Concern description
- `status: str` - "active", "inactive", "resolved"
- `effective_time_low: Optional[date]` - Start date
- `effective_time_high: Optional[date]` - End date
- `observations: list` - Related observations

### FunctionalStatusSection

Physical abilities including ADLs and IADLs.

```python
from ccdakit import FunctionalStatusSection

section = FunctionalStatusSection(
    organizers=functional_status_organizers,
    version=CDAVersion.R2_1
)
```

Each organizer groups functional status observations from the same assessment.

### MentalStatusSection

Psychological and mental competency observations.

```python
from ccdakit import MentalStatusSection

section = MentalStatusSection(
    observations=mental_status_observations,
    organizers=mental_status_organizers,
    version=CDAVersion.R2_1
)
```

Supports both individual observations and grouped organizers.

### AssessmentAndPlanSection

Clinician's conclusions and treatment plans.

```python
from ccdakit import AssessmentAndPlanSection

section = AssessmentAndPlanSection(
    items=assessment_plan_items,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `item_type: str` - "assessment" or "plan"
- `text: str` - Item description
- `planned_act: Optional` - Associated planned activity

### AdvanceDirectivesSection

Living wills, healthcare proxies, and resuscitation status.

```python
from ccdakit import AdvanceDirectivesSection

section = AdvanceDirectivesSection(
    directives=directives_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `directive_type: str` - Type of advance directive
- `directive_value: str` - Directive details
- `start_date: Optional[date]` - When directive becomes effective
- `custodian_name: Optional[str]` - Document custodian

### FamilyHistorySection

Family member health conditions and risk factors.

```python
from ccdakit import FamilyHistorySection

section = FamilyHistorySection(
    family_members=family_history_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `relationship_display_name: str` - Relationship to patient
- `subject: object` - Family member demographics
- `observations: list` - Health conditions

### MedicalEquipmentSection

Implanted and external medical devices and equipment.

```python
from ccdakit import MedicalEquipmentSection

section = MedicalEquipmentSection(
    equipment_list=equipment_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `name: str` - Equipment name
- `code: str` - Equipment code
- `code_system: str` - Code system
- `status: str` - "active", "completed"
- `date_supplied: Optional[date]` - Supply date

### PlanOfTreatmentSection

Pending orders, interventions, and planned activities.

```python
from ccdakit import PlanOfTreatmentSection

section = PlanOfTreatmentSection(
    planned_procedures=planned_procedures,
    planned_medications=planned_medications,
    planned_observations=planned_observations,
    version=CDAVersion.R2_1
)
```

Supports multiple types of planned activities with moodCode of INT (intent).

### HospitalDischargeInstructionsSection

Instructions provided at hospital discharge.

```python
from ccdakit import HospitalDischargeInstructionsSection

section = HospitalDischargeInstructionsSection(
    instructions=instructions_list,
    narrative_text="Follow discharge care plan.",
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `instruction_text: str` - Instruction content
- `instruction_category: Optional[str]` - Category (e.g., "Medications", "Diet")

### DischargeMedicationsSection

Medications to take or stop after discharge.

```python
from ccdakit import DischargeMedicationsSection

section = DischargeMedicationsSection(
    medications=discharge_meds_list,
    version=CDAVersion.R2_1
)
```

Uses same MedicationProtocol as MedicationsSection.

### PhysicalExamSection

Direct clinical observations and examination findings.

```python
from ccdakit import PhysicalExamSection

section = PhysicalExamSection(
    wound_observations=wound_observations,
    text="Physical exam findings...",
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `wound_type: str` - Type of wound
- `date: datetime` - Observation date
- `location: Optional[str]` - Body location
- `laterality: Optional[str]` - Left/right/bilateral

### ReasonForVisitSection

Provider's documentation of reason for visit.

```python
from ccdakit import ReasonForVisitSection

section = ReasonForVisitSection(
    reason_text="Annual physical examination",
    version=CDAVersion.R2_1
)
```

Simple narrative-only section without structured entries.

### ChiefComplaintAndReasonForVisitSection

Patient's chief complaint and provider's reason for visit.

```python
from ccdakit import ChiefComplaintAndReasonForVisitSection

section = ChiefComplaintAndReasonForVisitSection(
    chief_complaints=complaints_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `text: str` - Complaint or reason text

### NutritionSection

Diet, nutrition requirements, and nutritional status.

```python
from ccdakit import NutritionSection

section = NutritionSection(
    nutritional_statuses=nutrition_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `status: str` - Nutritional status
- `date: date` - Assessment date
- `assessments: list` - Nutrition assessments

### PayersSection

Insurance providers and coverage information.

```python
from ccdakit import PayersSection

section = PayersSection(
    payers=payers_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `payer_name: str` - Insurance company name
- `insurance_type: str` - Type of insurance
- `member_id: str` - Member identifier
- `start_date: Optional[date]` - Coverage start

### AdmissionMedicationsSection

Medications taken prior to and at admission.

```python
from ccdakit import AdmissionMedicationsSection

section = AdmissionMedicationsSection(
    medications=admission_meds_list,
    version=CDAVersion.R2_1
)
```

Uses same MedicationProtocol as MedicationsSection.

### InterventionsSection

Actions taken to achieve care goals and remove barriers.

```python
from ccdakit import InterventionsSection

section = InterventionsSection(
    interventions=interventions_list,
    planned_interventions=planned_interventions,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `description: str` - Intervention description
- `status: str` - Intervention status
- `effective_time: Optional[datetime]` - When performed

### HealthStatusEvaluationsSection

Outcomes of patient health status and care interventions.

```python
from ccdakit import HealthStatusEvaluationsAndOutcomesSection

section = HealthStatusEvaluationsAndOutcomesSection(
    outcomes=outcomes_list,
    version=CDAVersion.R2_1
)
```

**Required Properties**:
- `code: str` - Outcome code
- `display_name: str` - Outcome description
- `value: str` - Outcome value
- `effective_time: Optional[date]` - Assessment date

## Section Features

All sections automatically:

- Generate narrative HTML tables
- Validate required fields
- Handle version-specific requirements
- Support optional and required entries
- Include proper template IDs

## Next Steps

- [Protocols Reference](protocols.md)
- [Complete Examples](../examples/all-sections.md)
- [API Reference](../api/sections.md)
