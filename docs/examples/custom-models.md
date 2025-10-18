# Custom Data Models

Using your existing data models with ccdakit.

## With SQLAlchemy

```python
from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    sex = Column(String)

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    name = Column(String)
    code = Column(String)
    code_system = Column(String)
    status = Column(String)
    onset_date = Column(Date)

# Use with ccdakit
from ccdakit import ClinicalDocument, ProblemsSection, CDAVersion

# Query your database
patient = session.query(Patient).first()
problems = session.query(Problem).filter_by(patient_id=patient.id).all()

# Generate C-CDA
doc = ClinicalDocument(
    patient=patient,
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)
```

## With Pydantic

```python
from pydantic import BaseModel
from datetime import date
from typing import Optional

class Patient(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
    middle_name: Optional[str] = None
    ssn: Optional[str] = None

class Problem(BaseModel):
    name: str
    code: str
    code_system: str
    status: str
    onset_date: Optional[date] = None

# Use with ccdakit
patient = Patient(
    first_name="John",
    last_name="Doe",
    date_of_birth=date(1970, 1, 1),
    sex="M"
)

problems = [
    Problem(
        name="Diabetes",
        code="73211009",
        code_system="SNOMED",
        status="active",
        onset_date=date(2020, 1, 1)
    )
]

doc = ClinicalDocument(
    patient=patient,
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)
```

## With Dataclasses

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Patient:
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
    middle_name: Optional[str] = None

@dataclass
class Problem:
    name: str
    code: str
    code_system: str
    status: str
    onset_date: Optional[date] = None

# Works exactly the same
patient = Patient("John", "Doe", date(1970, 1, 1), "M")
```

## Adapter Pattern

If your models have different property names:

```python
class PatientAdapter:
    def __init__(self, db_patient):
        self._patient = db_patient

    @property
    def first_name(self):
        return self._patient.given_name

    @property
    def last_name(self):
        return self._patient.family_name

    @property
    def date_of_birth(self):
        return self._patient.birth_date

    @property
    def sex(self):
        return self._patient.gender

# Use adapter
db_patient = get_patient_from_db()
adapted_patient = PatientAdapter(db_patient)

doc = ClinicalDocument(
    patient=adapted_patient,
    sections=[...],
)
```

## Dictionary-Based

```python
from ccdakit.utils.converters import DictToCDAConverter

# Your data as dictionaries
patient_dict = {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1970-01-01",
    "sex": "M"
}

problems_dict = [{
    "name": "Diabetes",
    "code": "73211009",
    "code_system": "SNOMED",
    "status": "active"
}]

# Convert and generate
converter = DictToCDAConverter()
doc = converter.convert(
    patient=patient_dict,
    problems=problems_dict
)

xml = doc.to_string()
```

## Next Steps

- [Protocols Reference](../guides/protocols.md)
- [Builder API](builder-api.md)
- [API Reference](../api/protocols.md)
