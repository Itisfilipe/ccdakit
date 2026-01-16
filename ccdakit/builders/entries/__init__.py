"""Entry-level builders for C-CDA documents."""

from ccdakit.builders.entries.admission_diagnosis_entry import (
    HospitalAdmissionDiagnosis,
)
from ccdakit.builders.entries.admission_medication import AdmissionMedication
from ccdakit.builders.entries.advance_directive import AdvanceDirectiveObservation
from ccdakit.builders.entries.allergy import AllergyObservation
from ccdakit.builders.entries.anesthesia_entry import AnesthesiaProcedure
from ccdakit.builders.entries.complication_entry import ComplicationObservation
from ccdakit.builders.entries.coverage_activity import CoverageActivity, PolicyActivity
from ccdakit.builders.entries.discharge_diagnosis_entry import (
    HospitalDischargeDiagnosis,
)
from ccdakit.builders.entries.discharge_medication import DischargeMedication
from ccdakit.builders.entries.encounter import EncounterActivity
from ccdakit.builders.entries.entry_reference import EntryReference
from ccdakit.builders.entries.family_member_history import (
    FamilyHistoryObservation,
    FamilyHistoryOrganizer,
)
from ccdakit.builders.entries.functional_status import (
    FunctionalStatusObservation,
    FunctionalStatusOrganizer,
)
from ccdakit.builders.entries.goal import GoalObservation
from ccdakit.builders.entries.health_concern import HealthConcernAct
from ccdakit.builders.entries.immunization import ImmunizationActivity
from ccdakit.builders.entries.instruction import Instruction
from ccdakit.builders.entries.intervention_act import InterventionAct
from ccdakit.builders.entries.medical_equipment import (
    MedicalEquipmentOrganizer,
    NonMedicinalSupplyActivity,
)
from ccdakit.builders.entries.medication import MedicationActivity
from ccdakit.builders.entries.medication_administered_entry import (
    MedicationAdministeredActivity,
)
from ccdakit.builders.entries.mental_status import (
    MentalStatusObservation,
    MentalStatusOrganizer,
)
from ccdakit.builders.entries.nutrition_assessment import NutritionAssessment
from ccdakit.builders.entries.nutritional_status import NutritionalStatusObservation
from ccdakit.builders.entries.outcome_observation import OutcomeObservation
from ccdakit.builders.entries.physical_exam import LongitudinalCareWoundObservation
from ccdakit.builders.entries.planned_act import PlannedAct
from ccdakit.builders.entries.planned_encounter import PlannedEncounter
from ccdakit.builders.entries.planned_immunization import PlannedImmunization
from ccdakit.builders.entries.planned_intervention_act import PlannedInterventionAct
from ccdakit.builders.entries.planned_medication import PlannedMedication
from ccdakit.builders.entries.planned_observation import PlannedObservation
from ccdakit.builders.entries.planned_procedure import PlannedProcedure
from ccdakit.builders.entries.planned_supply import PlannedSupply
from ccdakit.builders.entries.preoperative_diagnosis_entry import (
    PreoperativeDiagnosisEntry,
)
from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.builders.entries.procedure import ProcedureActivity
from ccdakit.builders.entries.progress_toward_goal import ProgressTowardGoalObservation
from ccdakit.builders.entries.result import ResultObservation, ResultOrganizer
from ccdakit.builders.entries.smoking_status import SmokingStatusObservation
from ccdakit.builders.entries.vital_signs import VitalSignObservation, VitalSignsOrganizer


__all__ = [
    # Admission entries
    "AdmissionMedication",
    "HospitalAdmissionDiagnosis",
    # Advance directive entries
    "AdvanceDirectiveObservation",
    # Allergy entries
    "AllergyObservation",
    # Anesthesia entries
    "AnesthesiaProcedure",
    # Complication entries
    "ComplicationObservation",
    # Coverage/payer entries
    "CoverageActivity",
    "PolicyActivity",
    # Discharge entries
    "DischargeMedication",
    "HospitalDischargeDiagnosis",
    # Encounter entries
    "EncounterActivity",
    # Entry reference
    "EntryReference",
    # Family history entries
    "FamilyHistoryObservation",
    "FamilyHistoryOrganizer",
    # Functional status entries
    "FunctionalStatusObservation",
    "FunctionalStatusOrganizer",
    # Goal entries
    "GoalObservation",
    # Health concern entries
    "HealthConcernAct",
    # Immunization entries
    "ImmunizationActivity",
    # Instruction entries
    "Instruction",
    # Intervention entries
    "InterventionAct",
    # Medical equipment entries
    "MedicalEquipmentOrganizer",
    "NonMedicinalSupplyActivity",
    # Medication entries
    "MedicationActivity",
    "MedicationAdministeredActivity",
    # Mental status entries
    "MentalStatusObservation",
    "MentalStatusOrganizer",
    # Nutrition entries
    "NutritionAssessment",
    "NutritionalStatusObservation",
    # Outcome observation entries
    "OutcomeObservation",
    # Physical exam entries
    "LongitudinalCareWoundObservation",
    # Planned activity entries
    "PlannedAct",
    "PlannedEncounter",
    "PlannedImmunization",
    "PlannedInterventionAct",
    "PlannedMedication",
    "PlannedObservation",
    "PlannedProcedure",
    "PlannedSupply",
    # Preoperative diagnosis entries
    "PreoperativeDiagnosisEntry",
    # Problem entries
    "ProblemObservation",
    # Procedure entries
    "ProcedureActivity",
    # Progress toward goal entries
    "ProgressTowardGoalObservation",
    # Result entries
    "ResultObservation",
    "ResultOrganizer",
    # Smoking status entries
    "SmokingStatusObservation",
    # Vital signs entries
    "VitalSignObservation",
    "VitalSignsOrganizer",
]
