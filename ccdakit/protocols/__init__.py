"""Protocol definitions for C-CDA data contracts."""

from ccdakit.protocols.admission_diagnosis import AdmissionDiagnosisProtocol
from ccdakit.protocols.allergy import AllergyProtocol
from ccdakit.protocols.anesthesia import AnesthesiaProtocol
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
from ccdakit.protocols.functional_status import (
    FunctionalStatusObservationProtocol,
    FunctionalStatusOrganizerProtocol,
)
from ccdakit.protocols.goal import GoalProtocol
from ccdakit.protocols.health_status_evaluation import (
    OutcomeObservationProtocol,
    ProgressTowardGoalProtocol,
)
from ccdakit.protocols.hospital_course import HospitalCourseProtocol
from ccdakit.protocols.instruction import InstructionProtocol
from ccdakit.protocols.medication import MedicationProtocol
from ccdakit.protocols.medication_administered import MedicationAdministeredProtocol
from ccdakit.protocols.patient import AddressProtocol, PatientProtocol, TelecomProtocol
from ccdakit.protocols.payer import PayerProtocol
from ccdakit.protocols.physical_exam import (
    PhysicalExamSectionProtocol,
    WoundObservationProtocol,
)
from ccdakit.protocols.postoperative_diagnosis import (
    PostoperativeDiagnosisProtocol,
)
from ccdakit.protocols.preoperative_diagnosis import PreoperativeDiagnosisProtocol
from ccdakit.protocols.problem import PersistentIDProtocol, ProblemProtocol
from ccdakit.protocols.procedure import ProcedureProtocol
from ccdakit.protocols.result import ResultObservationProtocol, ResultOrganizerProtocol
from ccdakit.protocols.social_history import SmokingStatusProtocol


__all__ = [
    # Patient protocols
    "AddressProtocol",
    "TelecomProtocol",
    "PatientProtocol",
    # Problem protocols
    "PersistentIDProtocol",
    "ProblemProtocol",
    # Author protocols
    "AuthorProtocol",
    "OrganizationProtocol",
    # Medication protocols
    "MedicationProtocol",
    "MedicationAdministeredProtocol",
    # Allergy protocols
    "AllergyProtocol",
    # Anesthesia protocols
    "AnesthesiaProtocol",
    # Chief complaint protocols
    "ChiefComplaintProtocol",
    # Complication protocols
    "ComplicationProtocol",
    # Encounter protocols
    "EncounterProtocol",
    # Procedure protocols
    "ProcedureProtocol",
    # Result protocols
    "ResultObservationProtocol",
    "ResultOrganizerProtocol",
    # Social history protocols
    "SmokingStatusProtocol",
    # Goal protocols
    "GoalProtocol",
    # Health status evaluation protocols
    "OutcomeObservationProtocol",
    "ProgressTowardGoalProtocol",
    # Functional status protocols
    "FunctionalStatusObservationProtocol",
    "FunctionalStatusOrganizerProtocol",
    # Discharge diagnosis protocols
    "DischargeDiagnosisProtocol",
    # Admission diagnosis protocols
    "AdmissionDiagnosisProtocol",
    # Discharge diagnosis protocols
    "DischargeDiagnosisProtocol",
    # Discharge instruction protocols
    "DischargeInstructionProtocol",
    # Discharge studies protocols
    "DischargeStudyObservationProtocol",
    "DischargeStudyOrganizerProtocol",
    # Hospital course protocols
    "HospitalCourseProtocol",
    # Instruction protocols
    "InstructionProtocol",
    # Payer protocols
    "PayerProtocol",
    # Physical exam protocols
    "PhysicalExamSectionProtocol",
    "WoundObservationProtocol",
    # Postoperative diagnosis protocols
    "PostoperativeDiagnosisProtocol",
    # Preoperative diagnosis protocols
    "PreoperativeDiagnosisProtocol",
]
