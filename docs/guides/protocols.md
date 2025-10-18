# Protocols Reference

Complete reference for all protocols in ccdakit.

## What are Protocols?

Protocols define the interface your data models must satisfy. They use Python's structural subtyping - no inheritance required.

## Core Protocols

### PatientProtocol

```python
class PatientProtocol(Protocol):
    @property
    def first_name(self) -> str: ...

    @property
    def last_name(self) -> str: ...

    @property
    def date_of_birth(self) -> date: ...

    @property
    def sex(self) -> str: ...  # "M", "F", "UN"

    # Optional
    @property
    def middle_name(self) -> Optional[str]: ...

    @property
    def suffix(self) -> Optional[str]: ...

    @property
    def ssn(self) -> Optional[str]: ...

    @property
    def race(self) -> Optional[str]: ...

    @property
    def ethnicity(self) -> Optional[str]: ...
```

### AuthorProtocol

```python
class AuthorProtocol(Protocol):
    @property
    def first_name(self) -> str: ...

    @property
    def last_name(self) -> str: ...

    @property
    def npi(self) -> Optional[str]: ...
```

### OrganizationProtocol

```python
class OrganizationProtocol(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def npi(self) -> Optional[str]: ...
```

## Clinical Protocols

### ProblemProtocol

```python
class ProblemProtocol(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def code(self) -> str: ...

    @property
    def code_system(self) -> str: ...

    @property
    def status(self) -> str: ...

    @property
    def onset_date(self) -> Optional[date]: ...
```

### MedicationProtocol

```python
class MedicationProtocol(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def code(self) -> str: ...

    @property
    def status(self) -> str: ...

    @property
    def dosage(self) -> str: ...

    @property
    def route(self) -> str: ...

    @property
    def frequency(self) -> str: ...
```

### AllergyProtocol

```python
class AllergyProtocol(Protocol):
    @property
    def allergen(self) -> str: ...

    @property
    def code(self) -> str: ...

    @property
    def code_system(self) -> str: ...

    @property
    def type(self) -> str: ...

    @property
    def status(self) -> str: ...

    @property
    def reaction(self) -> Optional[str]: ...

    @property
    def severity(self) -> Optional[str]: ...
```

## Adapting Your Models

### Using Dataclasses

```python
from dataclasses import dataclass
from datetime import date

@dataclass
class Patient:
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
```

### Using SQLAlchemy

```python
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    sex = Column(String)
```

### Using Pydantic

```python
from pydantic import BaseModel
from datetime import date

class Patient(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
```

All work automatically with ccdakit!

## Next Steps

- [API Reference](../api/protocols.md)
- [Examples](../examples/custom-models.md)
