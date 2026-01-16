"""Protocol definitions for C-CDA data contracts."""

from ccdakit.protocols.admission_diagnosis import AdmissionDiagnosisProtocol
from ccdakit.protocols.advance_directive import AdvanceDirectiveProtocol
from ccdakit.protocols.allergy import AllergyProtocol
from ccdakit.protocols.anesthesia import AnesthesiaProtocol
from ccdakit.protocols.assessment_and_plan import (
    AssessmentAndPlanItemProtocol,
    PlannedActProtocol,
)
from ccdakit.protocols.author import AuthorProtocol, OrganizationProtocol
from ccdakit.protocols.chief_complaint import ChiefComplaintProtocol
from ccdakit.protocols.complication import ComplicationProtocol
from ccdakit.protocols.discharge_diagnosis import DischargeDiagnosisProtocol
from ccdakit.protocols.discharge_instructions import DischargeInstructionProtocol
from ccdakit.protocols.discharge_studies import (
    DischargeStudyObservationProtocol,
    DischargeStudyOrganizerProtocol,
)
from ccdakit.protocols.encounter import EncounterProtocol
from ccdakit.protocols.family_history import (
    FamilyHistoryObservationProtocol,
    FamilyMemberHistoryProtocol,
    FamilyMemberSubjectProtocol,
)
from ccdakit.protocols.functional_status import (
    FunctionalStatusObservationProtocol,
    FunctionalStatusOrganizerProtocol,
)
from ccdakit.protocols.goal import GoalProtocol
from ccdakit.protocols.health_concern import (
    HealthConcernObservationProtocol,
    HealthConcernProtocol,
)
from ccdakit.protocols.health_status_evaluation import (
    OutcomeObservationProtocol,
    ProgressTowardGoalProtocol,
)
from ccdakit.protocols.hospital_course import HospitalCourseProtocol
from ccdakit.protocols.immunization import ImmunizationProtocol
from ccdakit.protocols.instruction import InstructionProtocol
from ccdakit.protocols.intervention import (
    InterventionActivityProtocol,
    InterventionProtocol,
    PlannedInterventionProtocol,
)
from ccdakit.protocols.medical_equipment import MedicalEquipmentProtocol
from ccdakit.protocols.medication import MedicationProtocol
from ccdakit.protocols.medication_administered import MedicationAdministeredProtocol
from ccdakit.protocols.mental_status import (
    MentalStatusObservationProtocol,
    MentalStatusOrganizerProtocol,
)
from ccdakit.protocols.nutrition import (
    NutritionAssessmentProtocol,
    NutritionalStatusProtocol,
)
from ccdakit.protocols.patient import AddressProtocol, PatientProtocol, TelecomProtocol
from ccdakit.protocols.payer import PayerProtocol
from ccdakit.protocols.physical_exam import (
    PhysicalExamSectionProtocol,
    WoundObservationProtocol,
)
from ccdakit.protocols.plan_of_treatment import (
    PlannedActivityProtocol,
    PlannedEncounterProtocol,
    PlannedImmunizationProtocol,
    PlannedMedicationProtocol,
    PlannedObservationProtocol,
    PlannedProcedureProtocol,
    PlannedSupplyProtocol,
)
from ccdakit.protocols.postoperative_diagnosis import (
    PostoperativeDiagnosisProtocol,
)
from ccdakit.protocols.preoperative_diagnosis import PreoperativeDiagnosisProtocol
from ccdakit.protocols.problem import PersistentIDProtocol, ProblemProtocol
from ccdakit.protocols.procedure import ProcedureProtocol
from ccdakit.protocols.reason_for_visit import ReasonForVisitProtocol
from ccdakit.protocols.result import ResultObservationProtocol, ResultOrganizerProtocol
from ccdakit.protocols.social_history import SmokingStatusProtocol
from ccdakit.protocols.vital_signs import VitalSignProtocol, VitalSignsOrganizerProtocol


__all__ = [
    # Admission diagnosis protocols
    "AdmissionDiagnosisProtocol",
    # Advance directive protocols
    "AdvanceDirectiveProtocol",
    # Allergy protocols
    "AllergyProtocol",
    # Anesthesia protocols
    "AnesthesiaProtocol",
    # Assessment and plan protocols
    "AssessmentAndPlanItemProtocol",
    "PlannedActProtocol",
    # Author protocols
    "AuthorProtocol",
    "OrganizationProtocol",
    # Chief complaint protocols
    "ChiefComplaintProtocol",
    # Complication protocols
    "ComplicationProtocol",
    # Discharge diagnosis protocols
    "DischargeDiagnosisProtocol",
    # Discharge instruction protocols
    "DischargeInstructionProtocol",
    # Discharge studies protocols
    "DischargeStudyObservationProtocol",
    "DischargeStudyOrganizerProtocol",
    # Encounter protocols
    "EncounterProtocol",
    # Family history protocols
    "FamilyHistoryObservationProtocol",
    "FamilyMemberHistoryProtocol",
    "FamilyMemberSubjectProtocol",
    # Functional status protocols
    "FunctionalStatusObservationProtocol",
    "FunctionalStatusOrganizerProtocol",
    # Goal protocols
    "GoalProtocol",
    # Health concern protocols
    "HealthConcernObservationProtocol",
    "HealthConcernProtocol",
    # Health status evaluation protocols
    "OutcomeObservationProtocol",
    "ProgressTowardGoalProtocol",
    # Hospital course protocols
    "HospitalCourseProtocol",
    # Immunization protocols
    "ImmunizationProtocol",
    # Instruction protocols
    "InstructionProtocol",
    # Intervention protocols
    "InterventionActivityProtocol",
    "InterventionProtocol",
    "PlannedInterventionProtocol",
    # Medical equipment protocols
    "MedicalEquipmentProtocol",
    # Medication protocols
    "MedicationProtocol",
    "MedicationAdministeredProtocol",
    # Mental status protocols
    "MentalStatusObservationProtocol",
    "MentalStatusOrganizerProtocol",
    # Nutrition protocols
    "NutritionAssessmentProtocol",
    "NutritionalStatusProtocol",
    # Patient protocols
    "AddressProtocol",
    "PatientProtocol",
    "TelecomProtocol",
    # Payer protocols
    "PayerProtocol",
    # Persistent ID protocol
    "PersistentIDProtocol",
    # Physical exam protocols
    "PhysicalExamSectionProtocol",
    "WoundObservationProtocol",
    # Plan of treatment protocols
    "PlannedActivityProtocol",
    "PlannedEncounterProtocol",
    "PlannedImmunizationProtocol",
    "PlannedMedicationProtocol",
    "PlannedObservationProtocol",
    "PlannedProcedureProtocol",
    "PlannedSupplyProtocol",
    # Postoperative diagnosis protocols
    "PostoperativeDiagnosisProtocol",
    # Preoperative diagnosis protocols
    "PreoperativeDiagnosisProtocol",
    # Problem protocols
    "ProblemProtocol",
    # Procedure protocols
    "ProcedureProtocol",
    # Reason for visit protocols
    "ReasonForVisitProtocol",
    # Result protocols
    "ResultObservationProtocol",
    "ResultOrganizerProtocol",
    # Social history protocols
    "SmokingStatusProtocol",
    # Vital signs protocols
    "VitalSignProtocol",
    "VitalSignsOrganizerProtocol",
]
