"""Example of creating a Hospital Course Section."""

from lxml import etree

from ccdakit.builders.sections.hospital_course import HospitalCourseSection
from ccdakit.core.base import CDAVersion


def main():
    """Create and display a Hospital Course Section example."""

    # Example 1: Simple hospital course
    print("Example 1: Simple Hospital Course")
    print("=" * 80)

    simple_course = (
        "The patient was admitted for observation following a syncopal episode. "
        "Telemetry monitoring showed no arrhythmias. Orthostatic vital signs were negative. "
        "Echocardiogram was normal. The patient remained stable and was discharged home "
        "on hospital day 2 with cardiology follow-up."
    )
    section1 = HospitalCourseSection(
        narrative_text=simple_course,
        title="Hospital Course",
        version=CDAVersion.R2_1,
    )

    elem1 = section1.to_element()
    xml_string1 = etree.tostring(
        elem1, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string1)

    # Example 2: Detailed medical hospital course with multiple paragraphs
    print("\n" + "=" * 80)
    print("Example 2: Detailed Medical Hospital Course")
    print("=" * 80)

    medical_course = (
        "The patient is a 72-year-old male with history of diabetes mellitus type 2, "
        "hypertension, and hyperlipidemia who presented to the Emergency Department on "
        "04/01/2024 with altered mental status and fever to 103.2°F. Initial workup "
        "revealed white blood cell count of 18,000, urinalysis with pyuria and bacteriuria, "
        "and chest X-ray without infiltrate. The patient was admitted with diagnosis of "
        "urosepsis and acute encephalopathy. Empiric antibiotic therapy was initiated with "
        "ceftriaxone and IV fluids were administered. Blood and urine cultures were obtained.\n\n"
        "Over the first 48 hours, the patient showed gradual improvement in mental status "
        "and defervescence of fever. Blood cultures returned positive for E. coli sensitive "
        "to ceftriaxone, and antibiotic therapy was continued. By hospital day 3, the patient "
        "was alert and oriented to person, place, and time with return to baseline cognitive "
        "function. Vital signs remained stable without fever. Repeat urinalysis showed "
        "improvement in pyuria.\n\n"
        "The patient continued to improve clinically and was transitioned to oral ciprofloxacin "
        "on hospital day 5. Home medications were resumed with adjustments to diabetic regimen "
        "due to hyperglycemia during acute illness. Endocrinology consultation recommended "
        "uptitration of long-acting insulin. The patient was discharged home on hospital day 6 "
        "in stable condition with 10-day course of oral antibiotics, modified insulin regimen, "
        "and follow-up appointments scheduled with primary care physician and endocrinology."
    )
    section2 = HospitalCourseSection(
        narrative_text=medical_course,
        title="Hospital Course - Medical Service",
        version=CDAVersion.R2_1,
    )

    elem2 = section2.to_element()
    xml_string2 = etree.tostring(
        elem2, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string2)

    # Example 3: Surgical hospital course
    print("\n" + "=" * 80)
    print("Example 3: Surgical Hospital Course")
    print("=" * 80)

    surgical_course = (
        "The patient, a 58-year-old female, was admitted on 03/20/2024 for elective "
        "laparoscopic cholecystectomy for symptomatic cholelithiasis. The patient had "
        "been experiencing recurrent episodes of right upper quadrant pain over the past "
        "3 months. Preoperative workup included ultrasound confirming multiple gallstones "
        "and normal liver function tests. The patient was taken to the operating room on "
        "the day of admission where she underwent uncomplicated laparoscopic cholecystectomy. "
        "Operative time was 75 minutes with minimal blood loss. The patient tolerated the "
        "procedure well and was transferred to the post-anesthesia care unit in stable condition.\n\n"
        "Postoperatively, the patient was managed with IV fluids and pain control with "
        "hydromorphone PCA. She was started on clear liquids on postoperative day 1 and "
        "advanced to regular diet as tolerated. Pain was well-controlled with transition to "
        "oral pain medications. The surgical incisions appeared clean, dry, and intact without "
        "signs of infection. The patient ambulated independently without difficulty.\n\n"
        "On postoperative day 2, the patient met all discharge criteria including adequate "
        "pain control on oral medications, tolerance of regular diet, and independent ambulation. "
        "Discharge instructions were reviewed including wound care, activity restrictions, and "
        "warning signs. The patient was discharged home in stable condition with prescription "
        "for oral pain medication and scheduled follow-up with the surgeon in 2 weeks."
    )
    section3 = HospitalCourseSection(
        narrative_text=surgical_course,
        version=CDAVersion.R2_1,
    )

    elem3 = section3.to_element()
    xml_string3 = etree.tostring(
        elem3, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string3)

    # Example 4: Cardiac care hospital course
    print("\n" + "=" * 80)
    print("Example 4: Cardiac Care Hospital Course")
    print("=" * 80)

    cardiac_course = (
        "The patient, a 65-year-old male with history of coronary artery disease and "
        "hypertension, was admitted to the hospital on 03/15/2024 via the Emergency "
        "Department with chief complaint of chest pain. Initial EKG showed ST-segment "
        "elevations in leads V2-V4 consistent with anterior STEMI. The patient was "
        "taken emergently to the cardiac catheterization laboratory where he underwent "
        "successful percutaneous coronary intervention with drug-eluting stent placement "
        "to the proximal left anterior descending artery. Door-to-balloon time was 45 minutes.\n\n"
        "Post-procedure, the patient was transferred to the Cardiac Care Unit for "
        "monitoring. He was started on dual antiplatelet therapy, high-intensity statin, "
        "ACE inhibitor, and beta-blocker. Serial cardiac enzymes showed peak troponin of "
        "25.6 ng/mL at 12 hours post-admission. Transthoracic echocardiogram on hospital "
        "day 2 revealed anterior wall hypokinesis with ejection fraction estimated at 45%. "
        "The patient remained hemodynamically stable without recurrent chest pain or "
        "arrhythmias.\n\n"
        "By hospital day 3, the patient was transferred to the telemetry floor and began "
        "cardiac rehabilitation with physical therapy. He ambulated in the hallways without "
        "difficulty and demonstrated proper understanding of medication regimen. Cardiology "
        "consultation recommended continuing current medical therapy with outpatient follow-up "
        "in 1 week. Discharge planning was completed with arrangements for cardiac rehabilitation "
        "program enrollment and smoking cessation counseling. The patient was discharged home "
        "in stable condition on hospital day 4 with prescriptions and follow-up appointments "
        "scheduled with both primary care physician and cardiologist."
    )
    section4 = HospitalCourseSection(
        narrative_text=cardiac_course,
        title="Hospital Course - Cardiac Care",
        version=CDAVersion.R2_1,
    )

    elem4 = section4.to_element()
    xml_string4 = etree.tostring(
        elem4, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string4)

    # Example 5: C-CDA R2.0 version
    print("\n" + "=" * 80)
    print("Example 5: Hospital Course (C-CDA R2.0)")
    print("=" * 80)

    r20_course = (
        "The patient was admitted with community-acquired pneumonia. Treatment included "
        "IV antibiotics and supplemental oxygen. Clinical improvement noted by day 3. "
        "Transitioned to oral antibiotics and discharged home on day 5."
    )
    section5 = HospitalCourseSection(
        narrative_text=r20_course,
        version=CDAVersion.R2_0,
    )

    elem5 = section5.to_element()
    xml_string5 = etree.tostring(
        elem5, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string5)

    # Show validation info
    print("\n" + "=" * 80)
    print("Section Summary:")
    print("=" * 80)
    print("  - Template ID: 1.3.6.1.4.1.19376.1.5.3.1.3.5 (IHE)")
    print("  - LOINC Code: 8648-8 (Hospital Course)")
    print("  - Section Type: Narrative-only (no structured entries)")
    print("  - Versions: Supports both C-CDA R2.1 and R2.0")
    print("\nConformance Requirements:")
    print("  - CONF:81-7852: SHALL contain exactly one [1..1] templateId")
    print("  - CONF:81-10459: templateId/@root='1.3.6.1.4.1.19376.1.5.3.1.3.5'")
    print("  - CONF:81-15487: SHALL contain exactly one [1..1] code")
    print("  - CONF:81-15488: code/@code='8648-8' (Hospital Course)")
    print("  - CONF:81-26480: code/@codeSystem='2.16.840.1.113883.6.1' (LOINC)")
    print("  - CONF:81-7854: SHALL contain exactly one [1..1] title")
    print("  - CONF:81-7855: SHALL contain exactly one [1..1] text")
    print("\nUsage Notes:")
    print("  - This section describes the sequence of events from admission to discharge")
    print("  - Provides a chronological account of the patient's hospital stay")
    print("  - Typically included in Discharge Summary documents")
    print("  - Documents significant events, treatments, procedures, and response to therapy")
    print("  - Narrative can be split into multiple paragraphs using double line breaks (\\n\\n)")
    print("  - Single line breaks are preserved within paragraphs")

    # Display example use cases
    print("\n" + "=" * 80)
    print("Common Use Cases:")
    print("=" * 80)
    use_cases = [
        "Post-surgical recovery course",
        "Medical admission for acute illness",
        "ICU stay with critical care management",
        "Cardiac care unit admission for MI",
        "Obstetric admission for delivery",
        "Psychiatric hospitalization course",
        "Trauma admission and stabilization",
        "Oncology admission for chemotherapy",
        "Rehabilitation admission progress",
        "Pediatric admission for acute condition",
    ]

    for i, use_case in enumerate(use_cases, 1):
        print(f"  {i}. {use_case}")

    # Example 6: Using HospitalCourseProtocol object
    print("\n" + "=" * 80)
    print("Example 6: Using Protocol Object")
    print("=" * 80)

    # Create a simple class that implements the protocol
    class HospitalCourseData:
        def __init__(self, text):
            self._text = text

        @property
        def course_text(self):
            return self._text

    course_data = HospitalCourseData(
        "The patient was admitted to the ICU with severe sepsis secondary to pneumonia. "
        "Initial management included mechanical ventilation, broad-spectrum antibiotics, "
        "and vasopressor support with norepinephrine.\n\n"
        "By hospital day 4, the patient showed improvement with successful liberation "
        "from mechanical ventilation. Vasopressor support was weaned off and the patient "
        "was transferred to the medical floor.\n\n"
        "The patient completed a 7-day course of antibiotics and was discharged home in "
        "stable condition on hospital day 8."
    )

    section6 = HospitalCourseSection(
        hospital_course=course_data,
        title="Hospital Course - ICU Stay",
        version=CDAVersion.R2_1,
    )

    elem6 = section6.to_element()
    xml_string6 = etree.tostring(
        elem6, pretty_print=True, encoding="unicode", xml_declaration=False
    )
    print(xml_string6)

    print("\n" + "=" * 80)
    print("Protocol Usage:")
    print("=" * 80)
    print("  - Any object with a 'course_text' property can be used")
    print("  - No inheritance required - uses duck typing")
    print("  - Alternatively, pass narrative_text directly as a string")
    print("  - narrative_text parameter takes precedence over protocol object")


if __name__ == "__main__":
    main()
