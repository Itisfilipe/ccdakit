# C-CDA Builder - Open Source Architecture

**Project Name:** `ccda-builder`
**Version:** 1.0
**Date:** 2025-10-17
**License:** MIT (proposed)
**Status:** Design Phase

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Vision and Goals](#vision-and-goals)
3. [Architecture Overview](#architecture-overview)
4. [Design Principles](#design-principles)
5. [Core Components](#core-components)
6. [Version Management](#version-management)
7. [Extensibility](#extensibility)
8. [Implementation Details](#implementation-details)
9. [Testing Strategy](#testing-strategy)
10. [Roadmap](#roadmap)
11. [Community & Governance](#community--governance)
12. [Technical Decisions](#technical-decisions)

---

## Executive Summary

**ccda-builder** is a Python library for programmatic generation of HL7 C-CDA (Consolidated Clinical Document Architecture) documents. It provides a type-safe, composable, and version-aware builder pattern for creating ONC-compliant clinical documents.

### Why Another C-CDA Library?

Existing solutions have limitations:
- **Template-based** (Jinja2, XSLT): Hard to validate, verbose context management
- **String manipulation**: Error-prone, no type safety
- **Vendor-specific**: Locked to particular EHR systems
- **No version management**: Can't easily support multiple C-CDA versions

### Our Approach

- **lxml-based builders**: Programmatic XML construction with validation
- **Protocol-oriented**: No inheritance required, duck typing with type hints
- **Version-aware**: Built-in support for R2.0, R2.1
- **XSD validation**: Catch errors at build time, not runtime
- **Composable**: Reusable builders for common elements
- **Extensible**: Plugin system for custom sections and entries
- **Type-safe**: Full type hints, IDE autocomplete

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-version** | Support C-CDA R2.0, R2.1 in same codebase |
| **Build-time validation** | XSD/Schematron validation during generation |
| **Adapter pattern** | Easy integration with any EHR/data source |
| **Narrative generation** | Auto-generate human-readable sections |
| **Persistent IDs** | Built-in support for document versioning |
| **Plugin system** | Extend with custom sections/entries |
| **Pure Python** | No external dependencies except lxml |

---

## Vision and Goals

### Vision

**To be the de-facto Python library for C-CDA document generation, trusted by healthcare organizations worldwide for its robustness, compliance, and developer experience.**

### Primary Goals

1. **Standards Compliance**
   - Support HL7 C-CDA versions R2.0 and R2.1
   - Pass ONC certification validators
   - Maintain backward compatibility across supported versions

2. **Developer Experience**
   - Intuitive API that mirrors CDA structure
   - Comprehensive documentation with examples
   - Type hints for IDE support
   - Clear error messages

3. **Production Ready**
   - Battle-tested validation
   - Performance optimized for bulk generation
   - Memory efficient for large documents
   - Thread-safe for concurrent generation

4. **Community Driven**
   - Open source (MIT license)
   - Clear contribution guidelines
   - Active maintenance and support
   - Example adapters for common EHR systems

### Non-Goals

- **Parsing C-CDA documents**: Read-only, focus is on generation
- **FHIR conversion**: Separate concern, could be plugin
- **EHR system**: Not a complete EMR, just document builder
- **GUI/Web interface**: Library-first, UIs can be built on top

### Success Metrics

- 1000+ GitHub stars in first year
- Adopted by 10+ healthcare organizations
- 90%+ test coverage maintained
- <24hr response time on issues
- Monthly releases with version updates

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Application                          │
│              (EHR, HIE, Health App, etc.)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Custom Adapter (User Implements)           │    │
│  │  Converts app-specific data to ccda-builder         │    │
│  │  protocols (PatientProtocol, ProblemProtocol, etc.) │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             │ Uses
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    ccda-builder (Library)                    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Protocols   │  │   Builders   │  │  Validators  │     │
│  │ (interfaces) │  │  (lxml)      │  │  (XSD)       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Registry   │  │    Config    │  │    Utils     │     │
│  │ (versions)   │  │  (settings)  │  │  (IDs, etc)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ Outputs
                             ▼
                    ┌────────────────┐
                    │  C-CDA XML     │
                    │  (validated)   │
                    └────────────────┘
```

### Data Flow

```
User Data → Adapter → Protocols → Builders → XML → Validation → Output
   (DB)     (user)   (library)   (library)   (lxml)  (XSD)     (string)
```

### Layer Responsibilities

1. **User Application Layer**:
   - Fetch data from data source (database, API, files, etc.)
   - Implement adapter to convert to library protocols
   - Configure library for organization-specific settings
   - Handle output (save to file, S3, send via API, etc.)

2. **Library Core Layer**:
   - Define protocol interfaces for data contracts
   - Build XML using lxml and version-specific templates
   - Validate against XSD/Schematron schemas
   - Manage versions, registries, and configurations
   - Provide utilities (ID generation, code lookups, etc.)

3. **Output Layer**:
   - Validated C-CDA XML documents
   - Human-readable (pretty-printed) or compact
   - Ready for transmission via Direct, FHIR, etc.

---

## Design Principles

### 1. Protocol-Oriented Design

**Concept**: Define interfaces using Python Protocols (PEP 544) instead of inheritance.

**Benefits**:
- No forced inheritance hierarchy
- Structural typing (duck typing with type checking)
- Easy to adapt existing data models
- Testable with simple mocks

**Example**:

```python
from typing import Protocol
from datetime import date

class PatientProtocol(Protocol):
    """Protocol for patient data. Any object with these properties works."""

    @property
    def first_name(self) -> str: ...

    @property
    def last_name(self) -> str: ...

    @property
    def date_of_birth(self) -> date: ...

    @property
    def sex(self) -> str: ...

# Usage - any object with these properties works:
class MyPatient:
    def __init__(self, data):
        self._data = data

    @property
    def first_name(self) -> str:
        return self._data['fname']

    @property
    def last_name(self) -> str:
        return self._data['lname']

    @property
    def date_of_birth(self) -> date:
        return self._data['dob']

    @property
    def sex(self) -> str:
        return self._data['gender']

# No inheritance needed! MyPatient automatically satisfies PatientProtocol
```

### 2. Builder Pattern

**Concept**: Each CDA element is a builder class that knows how to construct itself.

**Benefits**:
- Composability: Builders return Elements that can be combined
- Testability: Unit test each builder independently
- Reusability: Common builders used across sections
- Type safety: IDE autocomplete and static type checking

**Example**:

```python
class ProblemObservation(CDAElement):
    """Builds a C-CDA Problem Observation entry."""

    def __init__(self, problem: ProblemProtocol):
        self.problem = problem

    def build(self) -> etree.Element:
        act = etree.Element('act', classCode='ACT', moodCode='EVN')

        # Compose with other builders
        act.append(Code('CONC', 'ActClass').to_element())
        act.append(EffectiveTime(low=self.problem.onset_date).to_element())

        return act
```

### 3. Version as First-Class Citizen

**Concept**: Every builder knows which C-CDA versions it supports.

**Benefits**:
- Easy to add new versions
- Backward compatibility maintained automatically
- Version-specific validation
- Clear documentation of version differences

**Example**:

```python
class ProblemsSection(CDAElement):
    TEMPLATES = {
        CDAVersion.R1_1: [
            TemplateConfig(root='2.16.840.1.113883.10.20.22.2.5'),
        ],
        CDAVersion.R2_1: [
            TemplateConfig(root='2.16.840.1.113883.10.20.22.2.5'),
            TemplateConfig(root='2.16.840.1.113883.10.20.22.2.5.1',
                         extension='2015-08-01'),
        ],
    }
```

### 4. Validation by Default

**Concept**: Documents are validated at build time, not after generation.

**Benefits**:
- Catch errors early
- Faster feedback loop
- Know exactly which builder failed
- Prevent invalid documents from being created

**Example**:

```python
def to_element(self) -> etree.Element:
    element = self.build()  # Subclass implements

    if self.schema:
        self.schema.assertValid(element)  # Validate immediately

    return element
```

### 5. Composition Over Inheritance

**Concept**: Prefer composition of small, reusable builders over large class hierarchies.

**Benefits**:
- Easier to understand
- More flexible (mix and match)
- Less coupling
- Better testability

**Example**:

```python
# Instead of inheritance:
class ProblemObservation(BaseObservation):
    pass

# Use composition:
class ProblemObservation(CDAElement):
    def build(self):
        obs = etree.Element('observation')

        # Compose with reusable builders
        obs.append(Code(...).to_element())
        obs.append(EffectiveTime(...).to_element())
        obs.append(StatusCode(...).to_element())

        return obs
```

### 6. Explicit Over Implicit

**Concept**: Make version dependencies, requirements, and defaults explicit.

**Benefits**:
- No surprises
- Easy to debug
- Clear documentation
- Reduced magic

**Example**:

```python
# Explicit version requirement
@requires_version(CDAVersion.R2_1)
class AuthorParticipation(CDAElement):
    """Author participation (required in R2.1, optional in R2.0)."""
    pass

# Explicit nullFlavor handling
def build_code(code: Optional[str], system: str):
    if code is None:
        return Code(nullFlavor='UNK', system=system)
    return Code(code, system)
```

---

## Core Components

### 1. Protocols (Data Contracts)

**Location**: `ccda_builder/protocols/`

**Purpose**: Define interfaces that user data must satisfy. No implementation, just contracts.

#### Patient Protocol

```python
# ccda_builder/protocols/patient.py
from typing import Protocol, Optional, List
from datetime import date

class AddressProtocol(Protocol):
    """Address data contract."""

    @property
    def street_lines(self) -> List[str]:
        """Street address lines (1-4 lines)."""
        ...

    @property
    def city(self) -> str:
        """City name."""
        ...

    @property
    def state(self) -> str:
        """State/province code (e.g., 'CA', 'NY')."""
        ...

    @property
    def postal_code(self) -> str:
        """ZIP/postal code."""
        ...

    @property
    def country(self) -> str:
        """Country code (ISO 3166-1 alpha-2, e.g., 'US')."""
        ...


class TelecomProtocol(Protocol):
    """Contact information protocol."""

    @property
    def type(self) -> str:
        """Type: 'phone', 'email', 'fax', 'url'."""
        ...

    @property
    def value(self) -> str:
        """The actual phone number, email, etc."""
        ...

    @property
    def use(self) -> Optional[str]:
        """Use code: 'HP' (home), 'WP' (work), 'MC' (mobile)."""
        ...


class PatientProtocol(Protocol):
    """Patient data contract."""

    @property
    def first_name(self) -> str:
        """Legal first name."""
        ...

    @property
    def last_name(self) -> str:
        """Legal last name."""
        ...

    @property
    def middle_name(self) -> Optional[str]:
        """Middle name or initial."""
        ...

    @property
    def date_of_birth(self) -> date:
        """Date of birth."""
        ...

    @property
    def sex(self) -> str:
        """Administrative sex: 'M', 'F', or 'UN'."""
        ...

    @property
    def race(self) -> Optional[str]:
        """Race code (CDC Race and Ethnicity)."""
        ...

    @property
    def ethnicity(self) -> Optional[str]:
        """Ethnicity code (CDC Race and Ethnicity)."""
        ...

    @property
    def language(self) -> Optional[str]:
        """Preferred language (ISO 639-2)."""
        ...

    @property
    def ssn(self) -> Optional[str]:
        """Social Security Number (US) or national ID."""
        ...

    @property
    def addresses(self) -> List[AddressProtocol]:
        """List of addresses (home, work, etc.)."""
        ...

    @property
    def telecoms(self) -> List[TelecomProtocol]:
        """List of contact methods (phone, email, etc.)."""
        ...

    @property
    def marital_status(self) -> Optional[str]:
        """Marital status code (HL7 MaritalStatus)."""
        ...
```

#### Problem Protocol

```python
# ccda_builder/protocols/problem.py
from typing import Protocol, Optional
from datetime import date

class PersistentIDProtocol(Protocol):
    """Persistent identifier protocol."""

    @property
    def root(self) -> str:
        """OID or UUID identifying the assigning authority."""
        ...

    @property
    def extension(self) -> str:
        """Unique identifier within the root's namespace."""
        ...


class ProblemProtocol(Protocol):
    """Problem/diagnosis data contract."""

    @property
    def name(self) -> str:
        """Human-readable problem name."""
        ...

    @property
    def code(self) -> str:
        """SNOMED CT or ICD-10 code."""
        ...

    @property
    def code_system(self) -> str:
        """Code system: 'SNOMED' or 'ICD-10'."""
        ...

    @property
    def onset_date(self) -> Optional[date]:
        """Date problem was identified/started."""
        ...

    @property
    def resolved_date(self) -> Optional[date]:
        """Date problem was resolved (None if ongoing)."""
        ...

    @property
    def status(self) -> str:
        """Status: 'active', 'inactive', 'resolved'."""
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """Persistent ID across document versions."""
        ...
```

#### Medication Protocol

```python
# ccda_builder/protocols/medication.py
from typing import Protocol, Optional, List
from datetime import date, datetime

class DosageProtocol(Protocol):
    """Dosage information protocol."""

    @property
    def value(self) -> float:
        """Dose quantity."""
        ...

    @property
    def unit(self) -> str:
        """Unit of measure (UCUM)."""
        ...


class FrequencyProtocol(Protocol):
    """Medication frequency protocol."""

    @property
    def institution_specified(self) -> bool:
        """True if frequency is institutional (e.g., 'BID', 'TID')."""
        ...

    @property
    def period_value(self) -> Optional[float]:
        """Period value (e.g., 8 for 'every 8 hours')."""
        ...

    @property
    def period_unit(self) -> Optional[str]:
        """Period unit: 'h' (hours), 'd' (days), etc."""
        ...


class MedicationProtocol(Protocol):
    """Medication data contract."""

    @property
    def name(self) -> str:
        """Medication name."""
        ...

    @property
    def rxnorm_code(self) -> str:
        """RxNorm code."""
        ...

    @property
    def status(self) -> str:
        """Status: 'active', 'completed', 'discontinued'."""
        ...

    @property
    def start_date(self) -> date:
        """Start date."""
        ...

    @property
    def end_date(self) -> Optional[date]:
        """End date (None if ongoing)."""
        ...

    @property
    def dosage(self) -> Optional[DosageProtocol]:
        """Dosage information."""
        ...

    @property
    def frequency(self) -> Optional[FrequencyProtocol]:
        """Frequency information."""
        ...

    @property
    def route(self) -> Optional[str]:
        """Route of administration code (SNOMED)."""
        ...

    @property
    def indication(self) -> Optional[str]:
        """Reason for medication."""
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """Persistent ID across document versions."""
        ...
```

#### Other Protocols

```python
# ccda_builder/protocols/allergy.py
class AllergyProtocol(Protocol):
    """Allergy/intolerance data contract."""

    @property
    def allergen_name(self) -> str: ...

    @property
    def allergen_code(self) -> str: ...

    @property
    def allergen_code_system(self) -> str: ...

    @property
    def reaction(self) -> Optional[str]: ...

    @property
    def severity(self) -> Optional[str]: ...

    @property
    def status(self) -> str: ...

    @property
    def onset_date(self) -> Optional[date]: ...


# ccda_builder/protocols/result.py
class LabResultProtocol(Protocol):
    """Lab result data contract."""

    @property
    def test_name(self) -> str: ...

    @property
    def loinc_code(self) -> str: ...

    @property
    def value(self) -> str: ...

    @property
    def unit(self) -> Optional[str]: ...

    @property
    def reference_range(self) -> Optional[str]: ...

    @property
    def interpretation(self) -> Optional[str]: ...

    @property
    def status(self) -> str: ...

    @property
    def effective_time(self) -> datetime: ...


# ccda_builder/protocols/vital.py
class VitalSignProtocol(Protocol):
    """Vital sign data contract."""

    @property
    def vital_type(self) -> str: ...

    @property
    def loinc_code(self) -> str: ...

    @property
    def value(self) -> float: ...

    @property
    def unit(self) -> str: ...

    @property
    def effective_time(self) -> datetime: ...


# ccda_builder/protocols/immunization.py
class ImmunizationProtocol(Protocol):
    """Immunization data contract."""

    @property
    def vaccine_name(self) -> str: ...

    @property
    def cvx_code(self) -> str: ...

    @property
    def administration_date(self) -> date: ...

    @property
    def status(self) -> str: ...

    @property
    def dose_number(self) -> Optional[int]: ...

    @property
    def route(self) -> Optional[str]: ...

    @property
    def site(self) -> Optional[str]: ...
```

### 2. Builders (XML Generation)

**Location**: `ccda_builder/builders/`

**Purpose**: Convert protocol objects to XML elements using lxml.

#### Base Classes

```python
# ccda_builder/builders/base.py
from abc import ABC, abstractmethod
from lxml import etree
from typing import List
from enum import Enum

class CDAVersion(Enum):
    """Supported C-CDA versions."""
    R2_0 = "2.0"
    R2_1 = "2.1"
    R3_0 = "3.0"


class TemplateConfig:
    """Template identifier configuration."""

    def __init__(self, root: str, extension: str = None, description: str = None):
        self.root = root
        self.extension = extension
        self.description = description

    def to_element(self) -> etree.Element:
        """Convert to templateId XML element."""
        elem = etree.Element('templateId', root=self.root)
        if self.extension:
            elem.set('extension', self.extension)
        return elem


class CDAElement(ABC):
    """Base class for all CDA elements."""

    # Subclasses override with version-specific templates
    TEMPLATES = {}

    def __init__(self, version: CDAVersion = CDAVersion.R2_1, schema=None):
        self.version = version
        self.schema = schema

    @abstractmethod
    def build(self) -> etree.Element:
        """Build and return the XML element. Implemented by subclasses."""
        pass

    def to_element(self) -> etree.Element:
        """Build with optional validation."""
        element = self.build()

        if self.schema:
            self.schema.assertValid(element)

        return element

    def to_string(self, pretty: bool = True, encoding: str = 'unicode') -> str:
        """Convert to XML string."""
        return etree.tostring(
            self.to_element(),
            pretty_print=pretty,
            encoding=encoding
        )

    def get_templates(self) -> List[TemplateConfig]:
        """Get templateIds for current version."""
        if self.version not in self.TEMPLATES:
            raise ValueError(
                f"Version {self.version.value} not supported for {self.__class__.__name__}"
            )
        return self.TEMPLATES[self.version]

    def add_template_ids(self, parent: etree.Element):
        """Add all templateIds for current version to parent element."""
        for template in self.get_templates():
            parent.append(template.to_element())
```

#### Common Builders

```python
# ccda_builder/builders/common.py
from lxml import etree
from datetime import datetime, date
from typing import Optional

class Code(CDAElement):
    """Reusable code element builder."""

    # Standard code system OIDs
    SYSTEM_OIDS = {
        'LOINC': '2.16.840.1.113883.6.1',
        'SNOMED': '2.16.840.1.113883.6.96',
        'RxNorm': '2.16.840.1.113883.6.88',
        'ICD-10': '2.16.840.1.113883.6.90',
        'CPT': '2.16.840.1.113883.6.12',
        'CVX': '2.16.840.1.113883.12.292',
        'UCUM': '2.16.840.1.113883.6.8',
    }

    def __init__(
        self,
        code: Optional[str] = None,
        system: Optional[str] = None,
        display_name: Optional[str] = None,
        null_flavor: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.code = code
        self.system = system
        self.display_name = display_name
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        elem = etree.Element('code')

        if self.null_flavor:
            elem.set('nullFlavor', self.null_flavor)
        else:
            if not self.code or not self.system:
                raise ValueError("code and system required when null_flavor not provided")

            elem.set('code', self.code)

            # Handle system OID lookup
            if self.system in self.SYSTEM_OIDS:
                elem.set('codeSystem', self.SYSTEM_OIDS[self.system])
                elem.set('codeSystemName', self.system)
            else:
                elem.set('codeSystem', self.system)

            if self.display_name:
                elem.set('displayName', self.display_name)

        return elem


class EffectiveTime(CDAElement):
    """Reusable effectiveTime element with support for points and intervals."""

    def __init__(
        self,
        value: Optional[datetime] = None,
        low: Optional[datetime] = None,
        high: Optional[datetime] = None,
        null_flavor: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.value = value
        self.low = low
        self.high = high
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        elem = etree.Element('effectiveTime')

        if self.null_flavor:
            elem.set('nullFlavor', self.null_flavor)
        elif self.value:
            # Point in time
            elem.set('value', self._format_datetime(self.value))
        else:
            # Interval
            if self.low:
                low = etree.SubElement(elem, 'low')
                low.set('value', self._format_datetime(self.low))

            if self.high:
                high = etree.SubElement(elem, 'high')
                high.set('value', self._format_datetime(self.high))
            elif self.low and not self.high:
                # Ongoing - use nullFlavor for high
                high = etree.SubElement(elem, 'high')
                high.set('nullFlavor', 'UNK')

        return elem

    @staticmethod
    def _format_datetime(dt: datetime) -> str:
        """Format datetime to CDA format: YYYYMMDDHHMMSSμμμμ+ZZZZ."""
        if isinstance(dt, date) and not isinstance(dt, datetime):
            # Date only
            return dt.strftime('%Y%m%d')
        # Full datetime with precision
        return dt.strftime('%Y%m%d%H%M%S')


class Identifier(CDAElement):
    """Reusable ID element builder."""

    def __init__(
        self,
        root: str,
        extension: Optional[str] = None,
        null_flavor: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.root = root
        self.extension = extension
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        elem = etree.Element('id')

        if self.null_flavor:
            elem.set('nullFlavor', self.null_flavor)
        else:
            elem.set('root', self.root)
            if self.extension:
                elem.set('extension', self.extension)

        return elem


class StatusCode(CDAElement):
    """Reusable statusCode element builder."""

    def __init__(self, code: str, **kwargs):
        super().__init__(**kwargs)
        self.code = code

    def build(self) -> etree.Element:
        elem = etree.Element('statusCode')
        elem.set('code', self.code)
        return elem
```

#### Entry Builders

```python
# ccda_builder/builders/entries/problem.py
from ccda_builder.builders.base import CDAElement, TemplateConfig, CDAVersion
from ccda_builder.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccda_builder.protocols import ProblemProtocol
from lxml import etree

class ProblemObservation(CDAElement):
    """C-CDA Problem Observation entry (Problem Concern Act)."""

    TEMPLATES = {
        CDAVersion.R1_1: [
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.4.4',
                description='Problem Observation (V1)'
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.4.4',
                extension='2014-06-09',
                description='Problem Observation (V2)'
            ),
        ],
        CDAVersion.R2_1: [
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.4.4',
                description='Problem Observation (V1)'
            ),
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.4.4',
                extension='2015-08-01',
                description='Problem Observation (V3)'
            ),
        ],
    }

    def __init__(self, problem: ProblemProtocol, **kwargs):
        super().__init__(**kwargs)
        self.problem = problem

    def build(self) -> etree.Element:
        # Build Problem Concern Act wrapper
        act = etree.Element('act', classCode='ACT', moodCode='EVN')

        # Add templateIds
        self.add_template_ids(act)

        # Persistent ID
        if self.problem.persistent_id:
            act.append(Identifier(
                root=self.problem.persistent_id.root,
                extension=self.problem.persistent_id.extension
            ).to_element())
        else:
            # Use nullFlavor if no ID
            act.append(Identifier(
                root='',
                null_flavor='NI'
            ).to_element())

        # Code for Problem Concern Act
        act.append(Code(
            code='CONC',
            system='2.16.840.1.113883.5.6',  # ActClass
            display_name='Concern'
        ).to_element())

        # Status code
        status = 'active' if not self.problem.resolved_date else 'completed'
        act.append(StatusCode(status).to_element())

        # Effective time (interval)
        act.append(EffectiveTime(
            low=self.problem.onset_date,
            high=self.problem.resolved_date
        ).to_element())

        # Entry relationship to actual observation
        entry_rel = etree.SubElement(act, 'entryRelationship', typeCode='SUBJ')
        entry_rel.append(self._build_observation())

        return act

    def _build_observation(self) -> etree.Element:
        """Build the nested Problem Observation element."""
        obs = etree.Element('observation', classCode='OBS', moodCode='EVN')

        # Observation templateIds
        obs_template = etree.SubElement(obs, 'templateId')
        obs_template.set('root', '2.16.840.1.113883.10.20.22.4.4')

        # ID
        if self.problem.persistent_id:
            obs.append(Identifier(
                root=self.problem.persistent_id.root,
                extension=self.problem.persistent_id.extension + '_obs'
            ).to_element())

        # Code (problem type)
        obs.append(Code(
            code='55607006',
            system='SNOMED',
            display_name='Problem'
        ).to_element())

        # Status
        obs.append(StatusCode('completed').to_element())

        # Effective time (onset)
        if self.problem.onset_date:
            obs.append(EffectiveTime(low=self.problem.onset_date).to_element())

        # Value (the actual problem code)
        value = etree.SubElement(obs, 'value')
        value.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'CD')
        value.set('code', self.problem.code)

        if self.problem.code_system in Code.SYSTEM_OIDS:
            value.set('codeSystem', Code.SYSTEM_OIDS[self.problem.code_system])
            value.set('codeSystemName', self.problem.code_system)
        else:
            value.set('codeSystem', self.problem.code_system)

        value.set('displayName', self.problem.name)

        return obs
```

#### Section Builders

```python
# ccda_builder/builders/sections/problems.py
from ccda_builder.builders.base import CDAElement, TemplateConfig, CDAVersion
from ccda_builder.builders.common import Code
from ccda_builder.builders.entries.problem import ProblemObservation
from ccda_builder.protocols import ProblemProtocol
from lxml import etree
from typing import List

class ProblemsSection(CDAElement):
    """C-CDA Problems Section."""

    TEMPLATES = {
        CDAVersion.R1_1: [
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.2.5',
                description='Problem Section'
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.2.5',
                description='Problem Section'
            ),
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.2.5',
                extension='2014-06-09',
                description='Problem Section (V2)'
            ),
        ],
        CDAVersion.R2_1: [
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.2.5',
                description='Problem Section'
            ),
            TemplateConfig(
                root='2.16.840.1.113883.10.20.22.2.5.1',
                extension='2015-08-01',
                description='Problem Section (entries required) (V3)'
            ),
        ],
    }

    LOINC_CODE = '11450-4'
    LOINC_DISPLAY = 'Problem List'

    def __init__(self, problems: List[ProblemProtocol], **kwargs):
        super().__init__(**kwargs)
        self.problems = problems

    def build(self) -> etree.Element:
        section = etree.Element('section')

        # Template IDs
        self.add_template_ids(section)

        # Section code
        section.append(Code(
            self.LOINC_CODE,
            'LOINC',
            display_name=self.LOINC_DISPLAY
        ).to_element())

        # Title
        title = etree.SubElement(section, 'title')
        title.text = 'Problems'

        # Narrative text (human-readable)
        section.append(self._build_narrative())

        # Entries (machine-readable)
        for problem in self.problems:
            entry = etree.SubElement(section, 'entry', typeCode='DRIV')
            entry.append(ProblemObservation(
                problem,
                version=self.version
            ).to_element())

        return section

    def _build_narrative(self) -> etree.Element:
        """Build human-readable narrative table."""
        text = etree.Element('text')

        if not self.problems:
            para = etree.SubElement(text, 'paragraph')
            para.text = 'No known problems.'
            return text

        table = etree.SubElement(text, 'table', border='1', width='100%')

        # Table header
        thead = etree.SubElement(table, 'thead')
        tr = etree.SubElement(thead, 'tr')
        for header in ['Problem', 'Code', 'Status', 'Onset Date', 'Resolved Date']:
            th = etree.SubElement(tr, 'th')
            th.text = header

        # Table body
        tbody = etree.SubElement(table, 'tbody')
        for problem in self.problems:
            tr = etree.SubElement(tbody, 'tr')

            # Problem name
            td = etree.SubElement(tr, 'td')
            td.text = problem.name

            # Code
            td = etree.SubElement(tr, 'td')
            td.text = f"{problem.code} ({problem.code_system})"

            # Status
            td = etree.SubElement(tr, 'td')
            td.text = problem.status

            # Onset date
            td = etree.SubElement(tr, 'td')
            if problem.onset_date:
                td.text = problem.onset_date.strftime('%Y-%m-%d')
            else:
                td.text = 'Unknown'

            # Resolved date
            td = etree.SubElement(tr, 'td')
            if problem.resolved_date:
                td.text = problem.resolved_date.strftime('%Y-%m-%d')
            elif problem.status == 'active':
                td.text = 'Ongoing'
            else:
                td.text = '-'

        return text
```

#### Document Builder

```python
# ccda_builder/builders/document.py
from ccda_builder.builders.base import CDAElement, CDAVersion
from ccda_builder.protocols import PatientProtocol
from lxml import etree
from typing import List
import uuid

class ClinicalDocument(CDAElement):
    """Top-level C-CDA Clinical Document."""

    NAMESPACES = {
        None: 'urn:hl7-org:v3',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'sdtc': 'urn:hl7-org:sdtc'
    }

    def __init__(
        self,
        patient: PatientProtocol,
        sections: List[CDAElement],
        document_id: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.patient = patient
        self.sections = sections
        self.document_id = document_id or str(uuid.uuid4())

    def build(self) -> etree.Element:
        # Create root with namespaces
        root = etree.Element(
            'ClinicalDocument',
            nsmap=self.NAMESPACES
        )

        # TODO: Build header components
        # - realmCode
        # - typeId
        # - templateId
        # - id
        # - code
        # - title
        # - effectiveTime
        # - confidentialityCode
        # - languageCode
        # - recordTarget (patient)
        # - author
        # - custodian
        # - documentationOf

        # Component
        component = etree.SubElement(root, 'component')
        structured_body = etree.SubElement(component, 'structuredBody')

        # Add all sections
        for section_builder in self.sections:
            component_section = etree.SubElement(structured_body, 'component')
            component_section.append(section_builder.to_element())

        return root
```

### 3. Configuration System

```python
# ccda_builder/core/config.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Callable
from enum import Enum

@dataclass
class OrganizationInfo:
    """Organization/custodian information."""
    name: str
    npi: Optional[str] = None
    tin: Optional[str] = None  # Tax ID Number
    oid_root: Optional[str] = None  # Organization's OID namespace
    address: Optional[Dict] = None
    phone: Optional[str] = None


@dataclass
class CDAConfig:
    """Global configuration for C-CDA generation."""

    # Organization (custodian)
    organization: OrganizationInfo

    # Version
    version: CDAVersion = CDAVersion.R2_1

    # Validation
    validate_on_build: bool = True
    xsd_schema_path: Optional[str] = None
    schematron_path: Optional[str] = None

    # Code system preferences
    prefer_snomed_over_icd10: bool = True

    # Persistent ID strategy
    id_generator: Optional[Callable] = None

    # Narrative options
    include_narrative: bool = True
    narrative_style: str = 'table'  # 'table', 'list', or 'paragraph'

    # Document metadata
    document_id_root: Optional[str] = None
    confidentiality_code: str = 'N'  # Normal

    # Custom extensions
    custom_namespaces: Dict[str, str] = field(default_factory=dict)
    custom_template_ids: Dict[str, list] = field(default_factory=dict)


# Global config instance
_config: Optional[CDAConfig] = None

def configure(config: CDAConfig):
    """Set global configuration."""
    global _config
    _config = config

def get_config() -> CDAConfig:
    """Get current configuration."""
    if _config is None:
        raise RuntimeError(
            "ccda-builder not configured. Call configure() before generating documents."
        )
    return _config

def reset_config():
    """Reset configuration (useful for testing)."""
    global _config
    _config = None
```

### 4. Validators

```python
# ccda_builder/validators/xsd.py
from lxml import etree
from typing import List

class XSDValidator:
    """XSD schema validator."""

    def __init__(self, schema_path: str):
        """
        Initialize validator with XSD schema.

        Args:
            schema_path: Path to CDA.xsd file
        """
        with open(schema_path, 'rb') as f:
            schema_doc = etree.parse(f)
            self.schema = etree.XMLSchema(schema_doc)

    def validate(self, element: etree.Element) -> bool:
        """
        Validate element against schema.

        Args:
            element: XML element to validate

        Returns:
            True if valid, False otherwise
        """
        return self.schema.validate(element)

    def assert_valid(self, element: etree.Element):
        """
        Assert element is valid, raise exception if not.

        Args:
            element: XML element to validate

        Raises:
            etree.DocumentInvalid: If validation fails
        """
        self.schema.assertValid(element)

    def get_errors(self, element: etree.Element) -> List[str]:
        """
        Get validation errors.

        Args:
            element: XML element to validate

        Returns:
            List of error messages
        """
        self.schema.validate(element)
        return [str(error) for error in self.schema.error_log]


# ccda_builder/validators/schematron.py
class SchematronValidator:
    """Schematron validator for C-CDA business rules."""

    def __init__(self, schematron_path: str):
        """
        Initialize validator with Schematron rules.

        Args:
            schematron_path: Path to schematron file
        """
        # TODO: Implement Schematron validation
        # This requires ISO Schematron processing
        pass

    def validate(self, element: etree.Element) -> bool:
        """Validate against Schematron rules."""
        raise NotImplementedError("Schematron validation not yet implemented")
```

### 5. Utilities

```python
# ccda_builder/utils/ids.py
import uuid
from typing import Dict

def generate_uuid_id(entity_type: str, entity_id: str) -> Dict[str, str]:
    """
    Generate a persistent ID using UUID v5 (namespace + name).

    Args:
        entity_type: Type of entity (e.g., 'problem', 'medication')
        entity_id: Unique identifier for the entity

    Returns:
        Dict with 'root' and 'extension' keys
    """
    namespace = uuid.NAMESPACE_OID
    name = f"{entity_type}:{entity_id}"
    generated_uuid = str(uuid.uuid5(namespace, name))

    return {
        'root': generated_uuid,
        'extension': '1'
    }


def generate_oid_id(oid_root: str, entity_id: str) -> Dict[str, str]:
    """
    Generate a persistent ID using organization's OID.

    Args:
        oid_root: Organization's OID namespace
        entity_id: Unique identifier for the entity

    Returns:
        Dict with 'root' and 'extension' keys
    """
    return {
        'root': oid_root,
        'extension': str(entity_id)
    }


# ccda_builder/utils/codes.py
from typing import Optional

# Standard code system OIDs
CODE_SYSTEMS = {
    'LOINC': '2.16.840.1.113883.6.1',
    'SNOMED': '2.16.840.1.113883.6.96',
    'RxNorm': '2.16.840.1.113883.6.88',
    'ICD-10': '2.16.840.1.113883.6.90',
    'CPT': '2.16.840.1.113883.6.12',
    'CVX': '2.16.840.1.113883.12.292',
    'UCUM': '2.16.840.1.113883.6.8',
}

def get_oid(system_name: str) -> Optional[str]:
    """Get OID for a code system name."""
    return CODE_SYSTEMS.get(system_name)

def is_valid_oid(oid: str) -> bool:
    """Check if string is a valid OID format."""
    parts = oid.split('.')
    return all(part.isdigit() for part in parts)
```

---

## Version Management

(Content similar to previous document, adapted for open-source context)

### Version Strategy

Each builder declares supported versions in `TEMPLATES` dict. When generating a document, pass the desired version:

```python
from ccda_builder import ClinicalDocument, ProblemsSection, CDAVersion

# Generate R2.1 document
doc = ClinicalDocument(
    patient=patient,
    sections=[ProblemsSection(problems, version=CDAVersion.R2_1)],
    version=CDAVersion.R2_1
)

# Generate R2.0 document
doc = ClinicalDocument(
    patient=patient,
    sections=[ProblemsSection(problems, version=CDAVersion.R2_0)],
    version=CDAVersion.R2_0
)
```

### Adding New Versions

If additional C-CDA versions need to be supported in the future:

1. Add to enum
2. Add templates to each builder
3. Override methods if structure changed
4. Add version-specific tests
5. Update documentation

---

## Extensibility

### Plugin System

Users can register custom sections and entries:

```python
# ccda_builder/core/registry.py
class PluginRegistry:
    """Registry for custom sections and entries."""

    _sections = {}
    _entries = {}

    @classmethod
    def register_section(cls, name: str, builder_class):
        """Register a custom section."""
        cls._sections[name] = builder_class

    @classmethod
    def register_entry(cls, name: str, builder_class):
        """Register a custom entry."""
        cls._entries[name] = builder_class

    @classmethod
    def get_section(cls, name: str):
        """Get registered section."""
        return cls._sections.get(name)


# User code
from ccda_builder.core.registry import PluginRegistry
from ccda_builder.builders.base import CDAElement

class CustomSection(CDAElement):
    """My organization's custom section."""

    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(root='2.16.840.1.MYORG.1.2.3'),
        ],
    }

    def build(self):
        # Custom logic
        pass

# Register
PluginRegistry.register_section('my_custom', CustomSection)
```

---

## Implementation Details

### Project Structure

```
ccda-builder/
├── pyproject.toml
├── README.md
├── LICENSE (MIT)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── .github/
│   ├── workflows/
│   │   ├── tests.yml
│   │   ├── publish.yml
│   │   └── docs.yml
│   └── ISSUE_TEMPLATE/
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   ├── api/
│   ├── examples/
│   └── contributing.md
├── ccda_builder/
│   ├── __init__.py
│   ├── py.typed  # PEP 561 marker
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── version.py
│   │   ├── registry.py
│   │   └── config.py
│   ├── protocols/
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   ├── problem.py
│   │   ├── medication.py
│   │   ├── allergy.py
│   │   ├── result.py
│   │   ├── vital.py
│   │   └── immunization.py
│   ├── builders/
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── entries/
│   │   │   ├── __init__.py
│   │   │   ├── problem.py
│   │   │   ├── medication.py
│   │   │   ├── allergy.py
│   │   │   ├── result.py
│   │   │   ├── vital.py
│   │   │   └── immunization.py
│   │   ├── sections/
│   │   │   ├── __init__.py
│   │   │   ├── problems.py
│   │   │   ├── medications.py
│   │   │   ├── allergies.py
│   │   │   ├── results.py
│   │   │   ├── vitals.py
│   │   │   └── immunizations.py
│   │   └── document.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── xsd.py
│   │   └── schematron.py
│   └── utils/
│       ├── __init__.py
│       ├── ids.py
│       └── codes.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_protocols/
│   ├── test_builders/
│   ├── test_validators/
│   └── test_integration/
├── examples/
│   ├── basic_usage.py
│   ├── custom_adapter.py
│   ├── bulk_generation.py
│   └── django_integration.py
└── schemas/
    ├── CDA.xsd
    ├── SDTC/
    └── README.md
```

### Package Configuration

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ccda-builder"
version = "0.1.0"
description = "Python library for generating HL7 C-CDA clinical documents"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["c-cda", "ccda", "hl7", "healthcare", "clinical-document", "ehr"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Medical Science Apps.",
]
dependencies = [
    "lxml>=4.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.0.250",
    "pyright>=1.1.0",
]
docs = [
    "mkdocs>=1.4.0",
    "mkdocs-material>=9.0.0",
]
validation = [
    "lxml[validation]",
]

[project.urls]
Homepage = "https://github.com/Itisfilipe/ccdakit"
Documentation = "https://Itisfilipe.github.io/ccdakit"
Repository = "https://github.com/Itisfilipe/ccdakit"
Issues = "https://github.com/Itisfilipe/ccdakit/issues"
Changelog = "https://github.com/Itisfilipe/ccdakit/blob/main/CHANGELOG.md"

[tool.setuptools]
packages = ["ccdakit"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=ccda_builder --cov-report=html --cov-report=term"

[tool.ruff]
line-length = 100
target-version = "py38"
```

### Public API

```python
# ccda_builder/__init__.py
"""
ccda-builder: Python library for generating HL7 C-CDA clinical documents.

Usage:
    from ccda_builder import (
        configure,
        CDAConfig,
        OrganizationInfo,
        CDAVersion,
        ClinicalDocument,
        ProblemsSection,
    )

    # Configure
    config = CDAConfig(
        organization=OrganizationInfo(name="My Clinic", npi="1234567890"),
        version=CDAVersion.R2_1,
    )
    configure(config)

    # Generate document
    doc = ClinicalDocument(
        patient=my_patient,
        sections=[ProblemsSection(problems)],
    )

    xml = doc.to_string()
"""

__version__ = "0.1.0"

from ccda_builder.core.config import (
    CDAConfig,
    OrganizationInfo,
    configure,
    get_config,
    reset_config,
)
from ccda_builder.core.version import CDAVersion
from ccda_builder.builders.document import ClinicalDocument
from ccda_builder.builders.sections import (
    ProblemsSection,
    MedicationsSection,
    AllergiesSection,
    ResultsSection,
    VitalsSection,
    ImmunizationsSection,
)
from ccda_builder.protocols import (
    PatientProtocol,
    ProblemProtocol,
    MedicationProtocol,
    AllergyProtocol,
    LabResultProtocol,
    VitalSignProtocol,
    ImmunizationProtocol,
    PersistentIDProtocol,
)

__all__ = [
    "__version__",
    # Config
    "CDAConfig",
    "OrganizationInfo",
    "configure",
    "get_config",
    "reset_config",
    # Version
    "CDAVersion",
    # Document
    "ClinicalDocument",
    # Sections
    "ProblemsSection",
    "MedicationsSection",
    "AllergiesSection",
    "ResultsSection",
    "VitalsSection",
    "ImmunizationsSection",
    # Protocols
    "PatientProtocol",
    "ProblemProtocol",
    "MedicationProtocol",
    "AllergyProtocol",
    "LabResultProtocol",
    "VitalSignProtocol",
    "ImmunizationProtocol",
    "PersistentIDProtocol",
]
```

### Basic Usage Example

```python
# examples/basic_usage.py
"""Basic example of generating a C-CDA document."""

from ccda_builder import (
    configure,
    CDAConfig,
    OrganizationInfo,
    CDAVersion,
    ClinicalDocument,
    ProblemsSection,
)
from datetime import date

# Step 1: Configure the library
config = CDAConfig(
    organization=OrganizationInfo(
        name="Example Medical Center",
        npi="1234567890",
        oid_root="2.16.840.1.113883.3.EXAMPLE",
    ),
    version=CDAVersion.R2_1,
    validate_on_build=True,
)
configure(config)


# Step 2: Create data objects that satisfy protocols
class MyPatient:
    """Simple patient implementation."""

    @property
    def first_name(self):
        return "John"

    @property
    def last_name(self):
        return "Doe"

    @property
    def middle_name(self):
        return "Q"

    @property
    def date_of_birth(self):
        return date(1970, 1, 1)

    @property
    def sex(self):
        return "M"

    # ... other properties ...


class MyProblem:
    """Simple problem implementation."""

    @property
    def name(self):
        return "Type 2 Diabetes Mellitus"

    @property
    def code(self):
        return "44054006"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def onset_date(self):
        return date(2020, 6, 15)

    @property
    def resolved_date(self):
        return None  # Ongoing

    @property
    def status(self):
        return "active"

    @property
    def persistent_id(self):
        return None  # Will auto-generate


# Step 3: Generate document
patient = MyPatient()
problems = [MyProblem()]

sections = [
    ProblemsSection(problems),
]

doc = ClinicalDocument(
    patient=patient,
    sections=sections,
)

# Step 4: Output XML
xml = doc.to_string(pretty=True)
print(xml)

# Or save to file
with open('ccda_document.xml', 'w') as f:
    f.write(xml)
```

---

## Testing Strategy

### Test Pyramid

1. **Unit Tests** (70%): Test individual builders
2. **Integration Tests** (20%): Test full document generation
3. **Validation Tests** (10%): Test XSD/Schematron compliance

### Unit Test Example

```python
# tests/test_builders/test_problem.py
import pytest
from datetime import date
from unittest.mock import Mock
from ccda_builder.builders.entries.problem import ProblemObservation
from ccda_builder.protocols import ProblemProtocol
from lxml import etree


def test_problem_observation_with_resolved_date():
    """Test problem observation with resolved date."""
    problem = Mock(spec=ProblemProtocol)
    problem.name = "Diabetes Mellitus Type 2"
    problem.code = "E11.9"
    problem.code_system = "ICD-10"
    problem.onset_date = date(2020, 1, 1)
    problem.resolved_date = date(2023, 1, 1)
    problem.status = "resolved"
    problem.persistent_id = None

    obs = ProblemObservation(problem)
    xml = obs.to_string()

    # Parse and validate structure
    tree = etree.fromstring(xml)

    # Check effective time has both low and high
    low = tree.find('.//effectiveTime/low')
    high = tree.find('.//effectiveTime/high')

    assert low is not None
    assert low.get('value') == '20200101'
    assert high is not None
    assert high.get('value') == '20230101'

    # Check problem code in value element
    value = tree.find('.//value')
    assert value.get('code') == 'E11.9'


def test_problem_observation_ongoing():
    """Test ongoing problem (no resolved date)."""
    problem = Mock(spec=ProblemProtocol)
    problem.name = "Hypertension"
    problem.code = "38341003"
    problem.code_system = "SNOMED"
    problem.onset_date = date(2020, 1, 1)
    problem.resolved_date = None
    problem.status = "active"
    problem.persistent_id = None

    obs = ProblemObservation(problem)
    tree = etree.fromstring(obs.to_string())

    # High should have nullFlavor for ongoing
    high = tree.find('.//effectiveTime/high')
    assert high is not None
    assert high.get('nullFlavor') == 'UNK'


@pytest.mark.parametrize('version', [
    CDAVersion.R2_0,
    CDAVersion.R2_1,
])
def test_problem_observation_all_versions(version):
    """Test problem observation generates valid XML for all versions."""
    problem = Mock(spec=ProblemProtocol)
    problem.name = "Test Problem"
    problem.code = "12345"
    problem.code_system = "SNOMED"
    problem.onset_date = date(2020, 1, 1)
    problem.resolved_date = None
    problem.status = "active"
    problem.persistent_id = None

    obs = ProblemObservation(problem, version=version)
    xml = obs.to_string()

    # Should generate valid XML
    tree = etree.fromstring(xml)
    assert tree.tag == 'act'

    # Should have version-specific templateIds
    template_ids = tree.findall('.//templateId')
    expected_count = len(ProblemObservation.TEMPLATES[version])
    assert len(template_ids) >= expected_count
```

### Coverage Goals

- Overall: 90%+
- Core builders: 95%+
- Protocols: 100% (just interfaces)
- Utilities: 90%+

---

## Roadmap

### Phase 1: MVP (Months 1-3)

**Goal**: Generate basic C-CDA R2.1 documents

- ✅ Core architecture
- ✅ Protocol system
- ✅ Builder pattern
- [ ] Problems section (complete)
- [ ] Medications section (complete)
- [ ] Allergies section (complete)
- [ ] XSD validation
- [ ] Documentation
- [ ] Unit tests (90%+)
- [ ] PyPI release (0.1.0)

### Phase 2: Full Sections (Months 4-6)

**Goal**: Support all ONC-required sections

- [ ] Results/Labs section
- [ ] Vital Signs section
- [ ] Immunizations section
- [ ] Procedures section
- [ ] Encounters section
- [ ] Plan of Care section
- [ ] Social History section
- [ ] Integration tests
- [ ] Example adapters

### Phase 3: Multi-Version ✅ COMPLETE

**Goal**: Support R2.0, R2.1

- [x] R2.0 support
- [x] R2.1 support
- [x] Version-specific tests
- [ ] Migration guides
- [ ] Version comparison tools

### Phase 4: Advanced Features (Months 10-12)

**Goal**: Production-ready features

- [ ] Schematron validation
- [ ] Performance optimization
- [ ] Bulk generation
- [ ] Plugin system
- [ ] Custom sections
- [ ] CLI tool
- [ ] PyPI release (1.0.0)

### Phase 5: Community Growth (Year 2)

**Goal**: Build ecosystem

- [ ] Additional examples
- [ ] EHR integrations (Django, Flask, FastAPI)
- [ ] FHIR conversion plugin
- [ ] VS Code extension
- [ ] Conference talks
- [ ] 1000+ stars

---

## Community & Governance

### Open Source

**License**: MIT

**Code of Conduct**: Contributor Covenant

**Contribution Process**:
1. Open issue for discussion
2. Fork repo
3. Create feature branch
4. Write tests
5. Submit PR
6. Code review
7. Merge

### Maintainers

**Core Team** (initially):
- You (Founder)
- TBD (Co-maintainer)

**Decision Making**:
- Lazy consensus for minor changes
- Voting for major changes
- BDFL (you) has final say initially

### Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Q&A, ideas
- **Discord/Slack**: Real-time chat (future)
- **Email**: Security issues only

---

## Technical Decisions

### Why lxml over ElementTree?

- XSD validation support
- Better performance (C library)
- More features (XPath, XSLT)
- Industry standard

### Why Protocols over ABC?

- No forced inheritance
- Easier for users to adapt existing models
- Duck typing with type checking
- More flexible

### Why Not Templates?

- Hard to validate
- Performance overhead
- Verbose context management
- Difficult to compose

### Why Version Registry?

- Easy to add new versions
- Clear version support
- Backward compatibility
- Single source of truth

### Performance Targets

- Single document: < 100ms
- 1000 documents: < 2 minutes
- Memory: < 2MB per document
- Thread-safe for concurrency

---

## Next Steps

1. [ ] Review architecture with potential users
2. [ ] Set up GitHub repo
3. [ ] Implement core infrastructure
4. [ ] Build Problems section (MVP)
5. [ ] Write basic documentation
6. [ ] Create first alpha release
7. [ ] Get feedback from early adopters
8. [ ] Iterate based on feedback

---

## Appendices

### A. Glossary

(Same as before)

### B. Reference Documents

- [HL7 C-CDA R2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- [ONC Certification Criteria](https://www.healthit.gov/topic/certification-ehrs/2015-edition-test-method)
- [C-CDA Validator](https://site.healthit.gov/sandbox-ccda/ccda-validator)
- [lxml Documentation](https://lxml.de/)
- [Python Protocols (PEP 544)](https://peps.python.org/pep-0544/)

### C. Code System References

(Same as before)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-17
**Status**: Design Phase
**License**: MIT
