# Medical Equipment Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.23`
**Version:** 2014-06-09 (R2.1 | R2.0)
**Badge:** Extended Section

## Overview

The **Medical Equipment Section (V2)** defines a patient's implanted and external health and medical devices and equipment. This section lists any pertinent durable medical equipment (DME) used to help maintain the patient's health status.

Medical equipment documented in this section includes:
- **Implanted Devices:** Pacemakers, defibrillators, joint replacements, stents, cochlear implants
- **External Equipment:** Wheelchairs, walkers, canes, crutches, oxygen equipment
- **Home Medical Devices:** CPAP machines, nebulizers, glucose monitors, insulin pumps
- **Prosthetics and Orthotics:** Artificial limbs, braces, orthotic shoes
- **Assistive Devices:** Hearing aids, eyeglasses, communication devices

This information is critical for patient safety, care coordination, and understanding functional status.

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.23`
- **Extension:** `2014-06-09`
- **LOINC Code:** `46264-8` (Medical Equipment)

### Conformance Requirements
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1098-7944)
- **SHALL** contain exactly one [1..1] `code` with code="46264-8" from LOINC (CONF:1098-15381)
- **SHALL** contain exactly one [1..1] `title` (CONF:1098-7946)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1098-7947)
- **MAY** contain zero or more [0..*] `entry` with Medical Equipment Organizer (CONF:1098-7948)
- **MAY** contain zero or more [0..*] `entry` with Non-Medicinal Supply Activity (CONF:1098-31125)

### Cardinality
- **Section:** Optional
- **Entries:** Optional (0..*)
- **Equipment per Entry:** One Non-Medicinal Supply Activity or one Organizer

## Protocol Requirements

The section uses the `MedicalEquipmentProtocol` from `ccdakit.protocols.medical_equipment`:

### Required Properties
```python
@property
def name(self) -> str:
    """Equipment/supply name (e.g., 'Wheelchair', 'Insulin Pump')"""

@property
def status(self) -> str:
    """Status: 'completed', 'active', 'aborted', 'cancelled'"""
```

### Optional Properties
```python
@property
def code(self) -> Optional[str]:
    """Equipment/supply code (from SNOMED CT, HCPCS, or CPT)"""

@property
def code_system(self) -> Optional[str]:
    """Code system: 'SNOMED CT', 'HCPCS', 'CPT'"""

@property
def date_supplied(self) -> Optional[date | datetime]:
    """Date/time when equipment was supplied"""

@property
def date_end(self) -> Optional[date | datetime]:
    """Date/time when equipment usage ended or is expected to end"""

@property
def quantity(self) -> Optional[int]:
    """Quantity of equipment/supplies provided"""

@property
def manufacturer(self) -> Optional[str]:
    """Manufacturer name of the equipment"""

@property
def model_number(self) -> Optional[str]:
    """Model number/identifier of the equipment"""

@property
def serial_number(self) -> Optional[str]:
    """Serial number/UDI of the specific equipment instance"""

@property
def instructions(self) -> Optional[str]:
    """Patient instructions for using the equipment"""
```

## Code Example

### Basic Usage

```python
from datetime import date, datetime
from ccdakit import MedicalEquipmentSection, CDAVersion

# Define medical equipment
equipment_list = [
    {
        "name": "Wheelchair",
        "code": "58938008",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 1, 15),
        "manufacturer": "Mobility Plus",
        "model_number": "WC-2024",
    },
    {
        "name": "Home Oxygen Concentrator",
        "code": "426294006",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 2, 1),
        "manufacturer": "Respironics",
        "model_number": "EverFlo",
        "serial_number": "RF12345678",
        "instructions": "Use continuously at 2 L/min",
    },
    {
        "name": "Blood Glucose Monitor",
        "code": "43252007",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2023, 11, 10),
        "manufacturer": "OneTouch",
        "model_number": "Ultra 2",
        "quantity": 1,
    }
]

# Create section
section = MedicalEquipmentSection(
    equipment_list=equipment_list,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Empty Section (No Equipment)

```python
# Create section with no equipment
section = MedicalEquipmentSection(
    equipment_list=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No medical equipment recorded"
```

### Implanted Devices

```python
equipment_list = [
    {
        "name": "Cardiac Pacemaker",
        "code": "14106009",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": datetime(2022, 8, 15, 10, 30),
        "manufacturer": "Medtronic",
        "model_number": "Azure XT DR",
        "serial_number": "MP123456789",
    },
    {
        "name": "Left Total Hip Prosthesis",
        "code": "304120007",
        "code_system": "SNOMED",
        "status": "completed",
        "date_supplied": datetime(2020, 3, 22, 14, 0),
        "manufacturer": "Zimmer Biomet",
        "model_number": "Taperloc Complete",
    },
    {
        "name": "Coronary Artery Stent",
        "code": "397578001",
        "code_system": "SNOMED",
        "status": "completed",
        "date_supplied": datetime(2023, 5, 10, 11, 45),
        "manufacturer": "Abbott",
        "model_number": "Xience Skypoint",
    }
]

section = MedicalEquipmentSection(equipment_list=equipment_list)
```

### Durable Medical Equipment (DME)

```python
dme_list = [
    {
        "name": "Walker",
        "code": "466289007",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 1, 20),
        "quantity": 1,
    },
    {
        "name": "Hospital Bed",
        "code": "229772003",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 2, 15),
        "manufacturer": "Hill-Rom",
    },
    {
        "name": "Bedside Commode",
        "code": "360008001",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 2, 15),
        "quantity": 1,
    }
]

section = MedicalEquipmentSection(equipment_list=dme_list)
```

### Diabetes Equipment

```python
diabetes_equipment = [
    {
        "name": "Insulin Pump",
        "code": "63653004",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": datetime(2023, 9, 1, 0, 0),
        "manufacturer": "Medtronic",
        "model_number": "MiniMed 770G",
        "serial_number": "MM7701234567",
        "instructions": "Check infusion site every 3 days. "
                       "Monitor for occlusion alarms.",
    },
    {
        "name": "Continuous Glucose Monitor",
        "code": "467453001",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2023, 9, 1),
        "manufacturer": "Dexcom",
        "model_number": "G6",
        "instructions": "Replace sensor every 10 days",
    },
    {
        "name": "Blood Glucose Test Strips",
        "code": "701000122105",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 3, 1),
        "quantity": 100,
    }
]

section = MedicalEquipmentSection(equipment_list=diabetes_equipment)
```

### Equipment with End Date

```python
equipment_list = [
    {
        "name": "Post-surgical Knee Brace",
        "code": "42152006",
        "code_system": "SNOMED",
        "status": "completed",
        "date_supplied": date(2023, 10, 15),
        "date_end": date(2024, 1, 15),  # Discontinued after healing
        "manufacturer": "DonJoy",
    },
    {
        "name": "Wound VAC System",
        "code": "469824008",
        "code_system": "SNOMED",
        "status": "completed",
        "date_supplied": datetime(2024, 1, 5, 9, 0),
        "date_end": datetime(2024, 2, 20, 14, 30),
        "manufacturer": "KCI",
        "model_number": "V.A.C. Ulta",
    }
]

section = MedicalEquipmentSection(equipment_list=equipment_list)
```

### Using Organizer (Grouped Equipment)

```python
# Group related equipment together
equipment_list = [
    {
        "name": "CPAP Machine",
        "code": "706172005",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 1, 1),
        "manufacturer": "ResMed",
        "model_number": "AirSense 10",
    },
    {
        "name": "CPAP Mask",
        "code": "467138007",
        "code_system": "SNOMED",
        "status": "active",
        "date_supplied": date(2024, 1, 1),
        "manufacturer": "ResMed",
    }
]

section = MedicalEquipmentSection(
    equipment_list=equipment_list,
    use_organizer=True,
    organizer_start_date=date(2024, 1, 1),
)
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class MedicalDevice:
    """Custom medical equipment implementation."""
    name: str
    status: str
    code: Optional[str] = None
    code_system: Optional[str] = None
    date_supplied: Optional[date | datetime] = None
    date_end: Optional[date | datetime] = None
    quantity: Optional[int] = None
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    instructions: Optional[str] = None

# Create equipment
equipment_list = [
    MedicalDevice(
        name="Nebulizer",
        code="34234003",
        code_system="SNOMED",
        status="active",
        date_supplied=date(2024, 2, 10),
        manufacturer="Pari",
        model_number="LC Plus",
        instructions="Use with albuterol as needed for wheezing",
    )
]

section = MedicalEquipmentSection(equipment_list=equipment_list)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Medical Equipment Section (V2)](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.23.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.23.html`

## Best Practices

### 1. Status Management
```python
# Active: Currently in use
{"status": "active"}

# Completed: Previously used, now discontinued
{"status": "completed", "date_end": date(2024, 2, 15)}

# Aborted: Equipment not successfully delivered
{"status": "aborted"}

# Cancelled: Order cancelled before delivery
{"status": "cancelled"}
```

### 2. Implanted Devices
```python
# Always include manufacturer and model for implanted devices
{
    "name": "Cardiac Pacemaker",
    "manufacturer": "Medtronic",
    "model_number": "Azure XT DR",
    "serial_number": "MP123456789",  # Critical for recalls
}
```

### 3. Unique Device Identification (UDI)
```python
# Use UDI format for serial numbers when available
{
    "serial_number": "(01)00643169001763(11)141231(17)150707(10)A213B1(21)1234"
}
```

### 4. Equipment Categories
```python
equipment_categories = {
    "Implanted": ["Pacemaker", "Defibrillator", "Joint Replacement", "Stent"],
    "Respiratory": ["Oxygen", "CPAP", "BiPAP", "Nebulizer", "Ventilator"],
    "Mobility": ["Wheelchair", "Walker", "Cane", "Crutches", "Scooter"],
    "Diabetes": ["Insulin Pump", "CGM", "Glucose Monitor", "Test Strips"],
    "Home Medical": ["Hospital Bed", "Hoyer Lift", "Suction Machine"],
    "Prosthetics": ["Artificial Limb", "Eye Prosthesis"],
    "Orthotics": ["Brace", "Orthotic Shoes", "Splint"],
    "Assistive": ["Hearing Aid", "Glasses", "Communication Device"],
}
```

### 5. Date Precision
```python
# Use datetime for precise implantation times
{
    "date_supplied": datetime(2024, 3, 15, 14, 30),  # Surgery time
}

# Use date for general equipment
{
    "date_supplied": date(2024, 3, 15),
}
```

### 6. Manufacturer Information
```python
# Include for tracking, recalls, and troubleshooting
{
    "manufacturer": "Medtronic",
    "model_number": "MiniMed 770G",
    "serial_number": "MM7701234567",
}
```

### 7. Patient Instructions
```python
# Include usage instructions
{
    "name": "CPAP Machine",
    "instructions": "Use nightly with pressure setting 12 cmH2O. "
                   "Clean mask daily. Replace filter monthly.",
}
```

### 8. Narrative Generation
The section automatically generates an HTML table with:
- Equipment name with unique ID reference
- Code and code system
- Date supplied
- Date end (if applicable)
- Quantity
- Status
- Manufacturer
- Model and serial number

### 9. Code Systems
```python
# SNOMED CT for clinical devices
{"code_system": "SNOMED"}

# HCPCS for DME billing codes
{"code_system": "HCPCS"}

# CPT for procedure-related equipment
{"code_system": "CPT"}
```

### 10. Safety Critical Equipment
```python
# Flag critical implanted devices
critical_equipment = [
    {
        "name": "Implantable Cardioverter Defibrillator (ICD)",
        "code": "360129009",
        "code_system": "SNOMED",
        "status": "active",
        "manufacturer": "Boston Scientific",
        "model_number": "INOGEN X4",
        "serial_number": "ICD1234567",
        # Critical for MRI safety, emergency care
    }
]
```

## Common Equipment Codes (SNOMED CT)

### Implanted Devices
- `14106009` - Cardiac pacemaker
- `360129009` - Implantable cardioverter-defibrillator
- `304120007` - Total hip prosthesis
- `304121006` - Total knee prosthesis
- `397578001` - Coronary artery stent
- `257327003` - Cochlear implant

### Respiratory Equipment
- `426294006` - Oxygen concentrator
- `706172005` - CPAP machine
- `706174006` - BiPAP machine
- `34234003` - Nebulizer
- `706223000` - Home ventilator

### Mobility Aids
- `58938008` - Wheelchair
- `466289007` - Walker
- `63653004` - Cane
- `183135000` - Crutches
- `469512007` - Motorized wheelchair

### Diabetes Equipment
- `63653004` - Insulin pump
- `467453001` - Continuous glucose monitor
- `43252007` - Blood glucose monitor

### Home Medical Equipment
- `229772003` - Hospital bed
- `360008001` - Bedside commode
- `469824008` - Wound VAC system
- `257265003` - Suction machine

## Common Pitfalls

1. **Missing Critical Info:** Always include manufacturer/model for implanted devices
2. **No Serial Numbers:** UDI/serial numbers critical for recalls and MRI safety
3. **Vague Descriptions:** Use specific equipment names, not "device" or "machine"
4. **Missing End Dates:** Document when equipment discontinued
5. **No Instructions:** Include patient-specific usage instructions
6. **Wrong Status:** Update status when equipment discontinued or replaced
7. **Missing Dates:** Always include when equipment was supplied
8. **Incomplete DME:** Document all assistive devices patient uses
9. **No Quantity:** Specify quantity for consumable supplies
10. **Missing Code System:** Always specify which code system used

## Safety Considerations

### MRI Safety
Document equipment that affects MRI compatibility:
- Pacemakers and ICDs
- Cochlear implants
- Metallic implants
- Programmable shunts

### Recalls and Alerts
Maintain accurate equipment information for:
- FDA recalls
- Safety alerts
- Software updates
- Battery replacements

### Home Safety
Document equipment requiring:
- Electrical power (backup plans)
- Regular maintenance
- Professional servicing
- Oxygen safety precautions

## Integration with Other Sections

### Procedures Section
Link equipment to implantation procedures

### Problem List
Document conditions requiring equipment

### Functional Status
Equipment affects functional assessments

### Plan of Treatment
Include equipment orders and follow-up
