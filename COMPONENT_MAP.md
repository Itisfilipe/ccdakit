# C-CDA Component Map

This document tracks all C-CDA components and their codependencies for the ccdakit project.

## Quick Stats

| Category | Implemented | Total | Coverage |
|----------|-------------|-------|----------|
| Sections | 39 | 82+ | 47.6% |
| ONC Core Sections | 8 | 8 | 100% |
| Protocols | 39 | 39 | 100% |
| Protocol Classes Exported | 62 | 62 | 100% |
| Entry Builders | 48 | 48 | 100% |
| Section Tests | 39 | 39 | 100% |
| Section Docs | 39 | 39 | 100% |
| Examples | 39 | 39 | 100% |

---

## Component Legend

Each section has the following codependencies:

| Icon | Component | Path Pattern |
|------|-----------|--------------|
| 📦 | Section Builder | `ccdakit/builders/sections/{name}.py` |
| 🔌 | Protocol | `ccdakit/protocols/{name}.py` |
| 🧩 | Entry Builder(s) | `ccdakit/builders/entries/{name}.py` |
| 🧪 | Tests | `tests/test_builders/test_{name}_section.py` |
| 📖 | Documentation | `docs/guides/hl7-guide/sections/{name}-section.md` |
| 📚 | Reference | `references/C-CDA_2.1/templates/{oid}.html` |
| 💻 | Example | `examples/{name}_example.py` |
| 🌐 | CLI/Web | Exposed via `ccdakit` CLI commands |

### Status Indicators

- ✅ Complete
- ⚠️ Partial/Needs Review
- ❌ Missing
- 🔄 In Progress

---

## Core Clinical Sections (ONC Required)

These 8 sections fulfill the ONC 2015 Edition certification requirements.

### 1. Allergies Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/allergies.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/allergy.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/allergy.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_allergies_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/allergies-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.6.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 2. Medications Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/medications.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/medication.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/medication.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_medications_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/medications-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.1.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 3. Problems Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/problems.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/problem.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/problem.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_problems_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/problems-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.5.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 4. Procedures Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/procedures.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/procedure.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/procedure.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_procedures_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/procedures-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.7.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 5. Results Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/results.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/result.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/result.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_results_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/results-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.3.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 6. Vital Signs Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/vital_signs.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/vital_signs.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/vital_signs.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_vital_signs_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/vital-signs-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.4.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 7. Immunizations Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/immunizations.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/immunization.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/immunization.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_immunizations_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/immunizations-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.2.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 8. Encounters Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/encounters.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/encounter.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/encounter.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_encounters_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/encounters-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.22.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

---

## Extended Clinical Sections

### 9. Social History Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/social_history.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/social_history.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/smoking_status.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_social_history_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/social-history-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.17` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 10. Family History Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/family_history.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/family_history.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/family_member_history.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_family_history_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/family-history-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.15` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 11. Functional Status Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/functional_status.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/functional_status.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/functional_status.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_functional_status_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/functional-status-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.14` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 12. Mental Status Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/mental_status.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/mental_status.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/mental_status.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_mental_status_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/mental-status-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.56` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 13. Goals Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/goals.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/goal.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/goal.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_goals_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/goals-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.60` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 14. Health Concerns Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/health_concerns.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/health_concern.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/health_concern.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_health_concerns_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/health-concerns-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.58` |
| 💻 Example | ✅ | `examples/health_concerns_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 15. Health Status Evaluations Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/health_status_evaluations.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/health_status_evaluation.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/outcome_observation.py`, `progress_toward_goal.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_health_status_evaluations_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/health-status-evaluations-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.61` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 16. Physical Exam Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/physical_exam.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/physical_exam.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/physical_exam.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_physical_exam_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/physical-exam-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.2.10` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 17. Assessment and Plan Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/assessment_and_plan.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/assessment_and_plan.py` |
| 🧩 Entry | ✅ | Reuses `PlannedAct` entry builder |
| 🧪 Tests | ✅ | `tests/test_builders/test_assessment_and_plan_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/assessment-and-plan-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.9` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 18. Past Medical History Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/past_medical_history.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/past_medical_history.py` |
| 🧩 Entry | ✅ | Reuses `ProblemObservation` entry builder |
| 🧪 Tests | ✅ | `tests/test_builders/test_past_medical_history_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/past-medical-history-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.20` |
| 💻 Example | ✅ | `examples/past_medical_history_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

---

## Specialized/Administrative Sections

### 19. Plan of Treatment Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/plan_of_treatment.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/plan_of_treatment.py` |
| 🧩 Entry | ✅ | Multiple planned entries in `ccdakit/builders/entries/planned_*.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_plan_of_treatment_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/plan-of-treatment-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.10` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 20. Interventions Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/interventions.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/intervention.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/intervention_act.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_interventions_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/interventions-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.21.2.3` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 21. Medical Equipment Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/medical_equipment.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/medical_equipment.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/medical_equipment.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_medical_equipment_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/medical-equipment-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.23` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 22. Advance Directives Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/advance_directives.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/advance_directive.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/advance_directive.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_advance_directives_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/advance-directives-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.21.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 23. Payers Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/payers.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/payer.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/coverage_activity.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_payers_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/payers-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.18` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 24. Nutrition Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/nutrition.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/nutrition.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/nutrition_assessment.py`, `nutritional_status.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_nutrition_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/nutrition-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.57` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 25. Reason for Visit Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/reason_for_visit.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/reason_for_visit.py` |
| 🧩 Entry | ✅ | Narrative-only section (per C-CDA spec) |
| 🧪 Tests | ✅ | `tests/test_builders/test_reason_for_visit_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/reason-for-visit-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.12` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 26. Chief Complaint and Reason for Visit Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/chief_complaint_reason_for_visit.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/chief_complaint.py` |
| 🧩 Entry | ✅ | Narrative-only section (per C-CDA spec) |
| 🧪 Tests | ✅ | `tests/test_builders/test_chief_complaint_reason_for_visit_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/chief-complaint-reason-for-visit-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.13` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

---

## Medication Variant Sections

### 27. Admission Medications Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/admission_medications.py` |
| 🔌 Protocol | ✅ | Reuses `MedicationProtocol` from `medication.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/admission_medication.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_admission_medications_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/admission-medications-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.44` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 28. Discharge Medications Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/discharge_medications.py` |
| 🔌 Protocol | ✅ | Reuses `MedicationProtocol` from `medication.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/discharge_medication.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_discharge_medications_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/discharge-medications-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.11.1` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

---

## Hospital/Surgical Sections

### 29. Admission Diagnosis Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/admission_diagnosis.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/admission_diagnosis.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/admission_diagnosis_entry.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_admission_diagnosis_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/admission-diagnosis-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.43` |
| 💻 Example | ✅ | `examples/admission_diagnosis_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 30. Discharge Diagnosis Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/discharge_diagnosis.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/discharge_diagnosis.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/discharge_diagnosis_entry.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_discharge_diagnosis_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/discharge-diagnosis-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.24` |
| 💻 Example | ✅ | `examples/discharge_diagnosis_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 31. Preoperative Diagnosis Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/preoperative_diagnosis.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/preoperative_diagnosis.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/preoperative_diagnosis_entry.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_preoperative_diagnosis_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/preoperative-diagnosis-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.34` |
| 💻 Example | ✅ | `examples/preoperative_diagnosis_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 32. Postoperative Diagnosis Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/postoperative_diagnosis.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/postoperative_diagnosis.py` |
| 🧩 Entry | ✅ | Reuses `ProblemObservation` entry builder |
| 🧪 Tests | ✅ | `tests/test_builders/test_postoperative_diagnosis_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/postoperative-diagnosis-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.35` |
| 💻 Example | ✅ | `examples/postoperative_diagnosis_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 33. Anesthesia Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/anesthesia.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/anesthesia.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/anesthesia_entry.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_sections/test_anesthesia.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/anesthesia-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.25` |
| 💻 Example | ✅ | `examples/anesthesia_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 34. Complications Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/complications.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/complication.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/complication_entry.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_complications_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/complications-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.37` |
| 💻 Example | ✅ | `examples/complications_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 35. Medications Administered Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/medications_administered.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/medication_administered.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/medication_administered_entry.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_medications_administered_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/medications-administered-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.38` |
| 💻 Example | ✅ | `examples/medications_administered_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 36. Hospital Course Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/hospital_course.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/hospital_course.py` |
| 🧩 Entry | ✅ | Narrative-only section (per C-CDA spec) |
| 🧪 Tests | ✅ | `tests/test_builders/test_hospital_course_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/hospital-course-section.md` |
| 📚 Reference | ✅ | Template ID: `1.3.6.1.4.1.19376.1.5.3.1.3.5` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 37. Hospital Discharge Instructions Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/hospital_discharge_instructions.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/discharge_instructions.py` |
| 🧩 Entry | ✅ | Narrative-only section (per C-CDA spec) |
| 🧪 Tests | ✅ | `tests/test_builders/test_hospital_discharge_instructions_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/hospital-discharge-instructions-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.41` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 38. Hospital Discharge Studies Summary Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/discharge_studies.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/discharge_studies.py` |
| 🧩 Entry | ✅ | Reuses `ResultOrganizer` entry builder |
| 🧪 Tests | ✅ | `tests/test_builders/test_discharge_studies_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/hospital-discharge-studies-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.16` |
| 💻 Example | ✅ | `examples/discharge_studies_example.py` |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

### 39. Instructions Section

| Component | Status | Path/Notes |
|-----------|--------|------------|
| 📦 Builder | ✅ | `ccdakit/builders/sections/instructions.py` |
| 🔌 Protocol | ✅ | `ccdakit/protocols/instruction.py` |
| 🧩 Entry | ✅ | `ccdakit/builders/entries/instruction.py` |
| 🧪 Tests | ✅ | `tests/test_builders/test_instructions_section.py` |
| 📖 Docs | ✅ | `docs/guides/hl7-guide/sections/instructions-section.md` |
| 📚 Reference | ✅ | Template ID: `2.16.840.1.113883.10.20.22.2.45` |
| 💻 Example | ✅ | Standalone example available |
| 🌐 CLI/Web | ✅ | Available via `generate`, `from_json` |

---

## Gap Analysis Summary

### Missing Examples (29 sections)

The following implemented sections lack standalone example files:

| # | Section | Priority |
|---|---------|----------|
| 1 | Allergies | High (ONC Core) |
| 2 | Medications | High (ONC Core) |
| 3 | Problems | High (ONC Core) |
| 4 | Procedures | High (ONC Core) |
| 5 | Results | High (ONC Core) |
| 6 | Vital Signs | High (ONC Core) |
| 7 | Immunizations | High (ONC Core) |
| 8 | Encounters | High (ONC Core) |
| 9 | Social History | Medium |
| 10 | Family History | Medium |
| 11 | Functional Status | Medium |
| 12 | Mental Status | Medium |
| 13 | Goals | Medium |
| 14 | Health Status Evaluations | Medium |
| 15 | Physical Exam | Medium |
| 16 | Assessment and Plan | Medium |
| 17 | Plan of Treatment | Medium |
| 18 | Interventions | Medium |
| 19 | Medical Equipment | Medium |
| 20 | Advance Directives | Medium |
| 21 | Payers | Low |
| 22 | Nutrition | Low |
| 23 | Reason for Visit | Low |
| 24 | Chief Complaint | Low |
| 25 | Admission Medications | Low |
| 26 | Discharge Medications | Low |
| 27 | Hospital Course | Low |
| 28 | Hospital Discharge Instructions | Low |
| 29 | Instructions | Low |

### Sections with Partial Entry Support (6 sections)

These sections reuse entries from other sections or are narrative-only:

| Section | Notes |
|---------|-------|
| Assessment and Plan | Uses Problem/PlannedAct entries |
| Past Medical History | Uses Problem entries |
| Postoperative Diagnosis | Uses Problem entries |
| Reason for Visit | Narrative-only |
| Chief Complaint | Narrative-only |
| Hospital Course | Narrative-only |
| Hospital Discharge Instructions | Narrative-only |
| Hospital Discharge Studies | Uses Result entries |

---

## Non-Section Components

### Header Components

| Component | Builder | Protocol | Tests | Docs |
|-----------|---------|----------|-------|------|
| Author | ✅ `header/author.py` | ✅ `author.py` | ✅ | ✅ |
| Custodian | ✅ `header/author.py` | ✅ `author.py` | ✅ | ✅ |
| RecordTarget (Patient) | ✅ `header/record_target.py` | ✅ `patient.py` | ✅ | ✅ |

### Document Types

| Document Type | Builder | Tests | Docs |
|---------------|---------|-------|------|
| Clinical Document (base) | ✅ `document.py` | ✅ | ✅ |
| Continuity of Care Document (CCD) | ✅ `documents/ccd.py` | ✅ | ✅ |
| Discharge Summary | ✅ `documents/discharge_summary.py` | ✅ | ✅ |

### Validators

| Validator | Implementation | Tests |
|-----------|----------------|-------|
| XSD Validator | ✅ `validators/xsd.py` | ✅ |
| Schematron Validator | ✅ `validators/schematron.py` | ✅ |
| Custom Rules | ✅ `validators/rules.py` | ✅ |

### CLI Commands

| Command | Implementation | Docs |
|---------|----------------|------|
| `validate` | ✅ | ✅ |
| `generate` | ✅ | ✅ |
| `convert` | ✅ | ✅ |
| `compare` | ✅ | ✅ |
| `serve` (Web UI) | ✅ | ✅ |
| `from_json` | ✅ | ✅ |
| `list_sections` | ✅ | ✅ |
| `list_entries` | ✅ | ✅ |
| `list_code_systems` | ✅ | ✅ |
| `list_templates` | ✅ | ✅ |
| `list_protocols` | ✅ | ✅ |
| `download_schemas` | ✅ | ✅ |
| `version` | ✅ | ✅ |

---

## Future Sections (Not Yet Implemented)

Based on C-CDA 2.1 specification, the following sections are candidates for future implementation:

| Section | Template ID | Priority |
|---------|-------------|----------|
| Care Team Section | 2.16.840.1.113883.10.20.22.2.500 | Medium |
| Care Planning Section | - | Medium |
| Disposition Section | - | Low |
| History of Present Illness | 1.3.6.1.4.1.19376.1.5.3.1.3.4 | Medium |
| Review of Systems | 1.3.6.1.4.1.19376.1.5.3.1.3.18 | Medium |
| General Status | 2.16.840.1.113883.10.20.2.5 | Low |
| Procedure Description | - | Low |
| Procedure Estimated Blood Loss | - | Low |
| Procedure Findings | - | Low |
| Procedure Implants | - | Low |
| Operative Note Fluids | - | Low |
| Operative Note Surgical Procedure | - | Low |
| Planned Procedure | - | Low |
| Assessment Section | 2.16.840.1.113883.10.20.22.2.8 | Medium |
| Subjective Section | - | Low |
| Objective Section | - | Low |

---

## Maintenance Checklist

When adding or modifying a section, ensure all codependencies are addressed:

- [ ] Section builder in `ccdakit/builders/sections/`
- [ ] Protocol in `ccdakit/protocols/`
- [ ] Entry builder(s) in `ccdakit/builders/entries/` (if applicable)
- [ ] Export in `ccdakit/builders/sections/__init__.py`
- [ ] Unit tests in `tests/test_builders/test_{section}_section.py`
- [ ] Integration tests (Schematron validation)
- [ ] Documentation in `docs/guides/hl7-guide/sections/{section}-section.md`
- [ ] Example in `examples/{section}_example.py`
- [ ] Reference checked against `references/C-CDA_2.1/templates/{oid}.html`
- [ ] CLI/Web exposure verified

---

## Recent Fixes (2026-01-16)

The following issues were identified and fixed:

1. **Protocol Exports**: Updated `ccdakit/protocols/__init__.py` to export all 62 protocol classes from 39 protocol files. Previously missing exports for:
   - `AdvanceDirectiveProtocol`
   - `AssessmentAndPlanItemProtocol`, `PlannedActProtocol`
   - `FamilyHistoryObservationProtocol`, `FamilyMemberHistoryProtocol`, `FamilyMemberSubjectProtocol`
   - `HealthConcernObservationProtocol`, `HealthConcernProtocol`
   - `ImmunizationProtocol`
   - `InterventionProtocol`, `PlannedInterventionProtocol`, `InterventionActivityProtocol`
   - `MedicalEquipmentProtocol`
   - `MentalStatusObservationProtocol`, `MentalStatusOrganizerProtocol`
   - `NutritionAssessmentProtocol`, `NutritionalStatusProtocol`
   - `PlannedActivityProtocol`, `PlannedObservationProtocol`, `PlannedProcedureProtocol`, `PlannedEncounterProtocol`, `PlannedMedicationProtocol`, `PlannedSupplyProtocol`, `PlannedImmunizationProtocol`
   - `ReasonForVisitProtocol`
   - `VitalSignProtocol`, `VitalSignsOrganizerProtocol`

2. **Entry Builder Exports**: Updated `ccdakit/builders/entries/__init__.py` to export all 48 entry builder classes. Previously missing exports for:
   - `AdvanceDirectiveObservation`
   - `EntryReference`
   - `FamilyHistoryObservation`, `FamilyHistoryOrganizer`
   - `HealthConcernAct`
   - `ImmunizationActivity`
   - `Instruction`
   - `InterventionAct`
   - `MedicalEquipmentOrganizer`, `NonMedicinalSupplyActivity`
   - `MedicationAdministeredActivity`
   - `MentalStatusObservation`, `MentalStatusOrganizer`
   - `NutritionAssessment`, `NutritionalStatusObservation`
   - `OutcomeObservation`
   - `PlannedAct`, `PlannedEncounter`, `PlannedImmunization`, `PlannedInterventionAct`, `PlannedMedication`, `PlannedObservation`, `PlannedProcedure`, `PlannedSupply`
   - `ProgressTowardGoalObservation`
   - `VitalSignObservation`, `VitalSignsOrganizer`

3. **Duplicate Export Removed**: Removed duplicate `DischargeDiagnosisProtocol` entry from protocols `__init__.py`.

4. **Section Tests**: Corrected count from 38 to 39 - the Anesthesia section test exists in `tests/test_builders/test_sections/test_anesthesia.py`.

5. **Section Examples**: Created 29 missing standalone example files (now 39/39 = 100%):
   - ONC Core: `allergies_example.py`, `medications_example.py`, `problems_example.py`, `procedures_example.py`, `results_example.py`, `vital_signs_example.py`, `immunizations_example.py`, `encounters_example.py`
   - Extended: `social_history_example.py`, `family_history_example.py`, `functional_status_example.py`, `mental_status_example.py`, `goals_example.py`, `health_status_evaluations_example.py`, `physical_exam_example.py`, `assessment_and_plan_example.py`, `plan_of_treatment_example.py`, `interventions_example.py`, `medical_equipment_example.py`, `advance_directives_example.py`, `payers_example.py`, `nutrition_example.py`
   - Narrative-only: `reason_for_visit_example.py`, `chief_complaint_example.py`, `hospital_course_example.py`, `hospital_discharge_instructions_example.py`
   - Discharge: `admission_medications_example.py`, `discharge_medications_example.py`, `instructions_example.py`

---

*Last updated: 2026-01-16*
*Generated by component mapping analysis*
