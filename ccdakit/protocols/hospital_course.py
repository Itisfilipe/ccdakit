"""Hospital Course protocol for C-CDA documents.

This module defines the protocol for Hospital Course Section data.
The section describes the sequence of events from admission to discharge
in a hospital facility.

Template ID: 1.3.6.1.4.1.19376.1.5.3.1.3.5
LOINC Code: 8648-8 (Hospital Course)
"""

from typing import Protocol


class HospitalCourseProtocol(Protocol):
    """
    Data contract for Hospital Course Section.

    The Hospital Course Section describes the sequence of events from admission
    to discharge in a hospital facility. This is primarily a narrative section
    that documents the patient's hospital stay, including:
    - Admission events and initial assessment
    - Daily progress and significant events during hospitalization
    - Treatments, procedures, and interventions performed
    - Response to treatment and clinical course
    - Complications or significant findings
    - Preparation for discharge

    This section is typically used in Discharge Summary documents.
    Template ID: 1.3.6.1.4.1.19376.1.5.3.1.3.5

    Example:
        The patient was admitted through the Emergency Department on 03/15/2024
        with acute exacerbation of COPD. Initial treatment included supplemental
        oxygen, nebulizer treatments, and IV corticosteroids. By hospital day 2,
        the patient showed improvement with decreased work of breathing. Antibiotics
        were added for suspected respiratory infection. The patient continued to
        improve and was transitioned to oral medications on day 3. Discharge
        planning was initiated with patient education on inhaler technique and
        smoking cessation resources.
    """

    @property
    def course_text(self) -> str:
        """
        The hospital course narrative text.

        This is the comprehensive narrative describing the patient's hospital
        stay from admission to discharge. The text should provide a chronological
        account of significant events, treatments, and the patient's clinical
        progress.

        The narrative may include:
        - Admission circumstances and initial condition
        - Daily hospital course and significant events
        - Procedures and interventions performed
        - Laboratory and imaging results with clinical significance
        - Consultations obtained
        - Complications or changes in condition
        - Response to treatment
        - Discharge preparation activities

        Returns:
            Hospital course narrative text

        Example:
            "The patient was admitted on 03/15/2024 with acute exacerbation
            of COPD. Initial vital signs showed respiratory distress with
            oxygen saturation of 88% on room air. Treatment was initiated
            with supplemental oxygen via nasal cannula, nebulizer treatments
            with albuterol and ipratropium, and IV methylprednisolone.
            Chest X-ray showed hyperinflation without acute infiltrate.
            By hospital day 2, the patient demonstrated clinical improvement
            with decreased work of breathing and improved oxygen saturation..."
        """
        ...


__all__ = ["HospitalCourseProtocol"]
