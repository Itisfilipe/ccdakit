"""Section-level builders for C-CDA documents."""

from ccdakit.builders.sections.admission_diagnosis import AdmissionDiagnosisSection
from ccdakit.builders.sections.admission_medications import AdmissionMedicationsSection
from ccdakit.builders.sections.advance_directives import AdvanceDirectivesSection
from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.builders.sections.anesthesia import AnesthesiaSection
from ccdakit.builders.sections.assessment_and_plan import AssessmentAndPlanSection
from ccdakit.builders.sections.chief_complaint_reason_for_visit import (
    ChiefComplaintAndReasonForVisitSection,
)
from ccdakit.builders.sections.complications import ComplicationsSection
from ccdakit.builders.sections.discharge_diagnosis import DischargeDiagnosisSection
from ccdakit.builders.sections.discharge_medications import DischargeMedicationsSection
from ccdakit.builders.sections.discharge_studies import (
    HospitalDischargeStudiesSummarySection,
)
from ccdakit.builders.sections.encounters import EncountersSection
from ccdakit.builders.sections.family_history import FamilyHistorySection
from ccdakit.builders.sections.functional_status import FunctionalStatusSection
from ccdakit.builders.sections.goals import GoalsSection
from ccdakit.builders.sections.health_concerns import HealthConcernsSection
from ccdakit.builders.sections.health_status_evaluations import (
    HealthStatusEvaluationsAndOutcomesSection,
)
from ccdakit.builders.sections.hospital_course import HospitalCourseSection
from ccdakit.builders.sections.hospital_discharge_instructions import (
    HospitalDischargeInstructionsSection,
)
from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.builders.sections.instructions import InstructionsSection
from ccdakit.builders.sections.interventions import InterventionsSection
from ccdakit.builders.sections.medical_equipment import MedicalEquipmentSection
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.medications_administered import (
    MedicationsAdministeredSection,
)
from ccdakit.builders.sections.mental_status import MentalStatusSection
from ccdakit.builders.sections.nutrition import NutritionSection
from ccdakit.builders.sections.past_medical_history import PastMedicalHistorySection
from ccdakit.builders.sections.payers import PayersSection
from ccdakit.builders.sections.physical_exam import PhysicalExamSection
from ccdakit.builders.sections.plan_of_treatment import PlanOfTreatmentSection
from ccdakit.builders.sections.postoperative_diagnosis import (
    PostoperativeDiagnosisSection,
)
from ccdakit.builders.sections.preoperative_diagnosis import (
    PreoperativeDiagnosisSection,
)
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.builders.sections.procedures import ProceduresSection
from ccdakit.builders.sections.reason_for_visit import ReasonForVisitSection
from ccdakit.builders.sections.results import ResultsSection
from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.builders.sections.vital_signs import VitalSignsSection


__all__ = [
    "AdmissionDiagnosisSection",
    "AdmissionMedicationsSection",
    "AdvanceDirectivesSection",
    "AllergiesSection",
    "AnesthesiaSection",
    "AssessmentAndPlanSection",
    "ChiefComplaintAndReasonForVisitSection",
    "ComplicationsSection",
    "DischargeDiagnosisSection",
    "DischargeMedicationsSection",
    "EncountersSection",
    "FamilyHistorySection",
    "FunctionalStatusSection",
    "GoalsSection",
    "HealthConcernsSection",
    "HealthStatusEvaluationsAndOutcomesSection",
    "HospitalCourseSection",
    "HospitalDischargeInstructionsSection",
    "HospitalDischargeStudiesSummarySection",
    "ImmunizationsSection",
    "InstructionsSection",
    "InterventionsSection",
    "MedicalEquipmentSection",
    "MedicationsSection",
    "MedicationsAdministeredSection",
    "MentalStatusSection",
    "NutritionSection",
    "PastMedicalHistorySection",
    "PayersSection",
    "PhysicalExamSection",
    "PlanOfTreatmentSection",
    "PostoperativeDiagnosisSection",
    "PreoperativeDiagnosisSection",
    "ProblemsSection",
    "ProceduresSection",
    "ReasonForVisitSection",
    "ResultsSection",
    "SocialHistorySection",
    "VitalSignsSection",
]
