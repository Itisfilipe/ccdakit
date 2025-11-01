"""Simple data models for converting test data dictionaries to protocol-compliant objects."""

from __future__ import annotations

from datetime import datetime
from typing import Any


class DictWrapper:
    """Base class to wrap dictionaries as objects with attribute access."""

    def __init__(self, data: dict[str, Any]):
        self._data = data

    def __getattr__(self, name: str) -> Any:
        """Allow attribute-style access to dictionary keys."""
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        return self._data.get(name)


class Address(DictWrapper):
    """Address wrapper for test data dictionaries."""

    @property
    def street_lines(self) -> list[str]:
        # Try 'street_lines' first (from test data generator)
        street_lines = self._data.get("street_lines", [])
        if street_lines:
            return street_lines
        # Fall back to 'street' field (for backwards compatibility)
        street = self._data.get("street", "")
        return [street] if street else []

    @property
    def city(self) -> str:
        return self._data.get("city", "")

    @property
    def state(self) -> str:
        return self._data.get("state", "")

    @property
    def postal_code(self) -> str:
        return self._data.get("zip", "")

    @property
    def country(self) -> str:
        return "US"


class Telecom(DictWrapper):
    """Telecom wrapper for test data dictionaries."""

    @property
    def type(self) -> str:
        return "phone"

    @property
    def value(self) -> str:
        return self._data.get("phone", "")

    @property
    def use(self) -> str:
        return "home"


class Patient(DictWrapper):
    """Patient wrapper for test data dictionaries."""

    @property
    def first_name(self) -> str:
        return self._data.get("first_name", "")

    @property
    def middle_name(self) -> str | None:
        return self._data.get("middle_name")

    @property
    def last_name(self) -> str:
        return self._data.get("last_name", "")

    @property
    def date_of_birth(self) -> Any:
        return self._data.get("date_of_birth")

    @property
    def sex(self) -> str:
        return self._data.get("sex", "")

    @property
    def race(self) -> str | None:
        return self._data.get("race")

    @property
    def ethnicity(self) -> str | None:
        return self._data.get("ethnicity")

    @property
    def language(self) -> str:
        return self._data.get("language", "eng")

    @property
    def ssn(self) -> str | None:
        return self._data.get("ssn")

    @property
    def marital_status(self) -> str | None:
        return self._data.get("marital_status")

    @property
    def addresses(self) -> list[Address]:
        addrs = self._data.get("addresses", [])
        return [Address(addr) for addr in addrs]

    @property
    def telecoms(self) -> list[Telecom]:
        telecoms = self._data.get("telecoms", [])
        return [Telecom(t) for t in telecoms]


class Organization(DictWrapper):
    """Organization wrapper for test data dictionaries."""

    @property
    def name(self) -> str:
        return self._data.get("name", "Unknown Organization")

    @property
    def npi(self) -> str | None:
        return self._data.get("npi")

    @property
    def tin(self) -> str | None:
        return self._data.get("tin")

    @property
    def oid_root(self) -> str | None:
        return self._data.get("oid_root")

    @property
    def addresses(self) -> list[Address]:
        addr_dict = self._data.get("address", {})
        return [Address(addr_dict)] if addr_dict else []

    @property
    def telecoms(self) -> list[Telecom]:
        telecom = self._data.get("telecom", "")
        if telecom:
            return [Telecom({"phone": telecom})]
        return []


class Author(DictWrapper):
    """Author wrapper for test data dictionaries."""

    @property
    def first_name(self) -> str:
        return self._data.get("first_name", "")

    @property
    def middle_name(self) -> str | None:
        return self._data.get("middle_name")

    @property
    def last_name(self) -> str:
        return self._data.get("last_name", "")

    @property
    def npi(self) -> str | None:
        return self._data.get("npi")

    @property
    def time(self) -> datetime:
        return self._data.get("time", datetime.now())

    @property
    def addresses(self) -> list[Address]:
        # Return default work address to satisfy C-CDA requirement
        addr_dict = self._data.get("address")
        if addr_dict:
            return [Address(addr_dict)]
        # Default work address
        return [
            Address(
                {
                    "street": "123 Healthcare Drive",
                    "city": "Medical City",
                    "state": "CA",
                    "zip": "94000",
                }
            )
        ]

    @property
    def telecoms(self) -> list[Telecom]:
        # Return default work phone to satisfy C-CDA requirement
        telecom = self._data.get("telecom")
        if telecom:
            return [Telecom({"phone": telecom})]
        # Default work phone
        return [Telecom({"phone": "tel:+1-555-123-4567"})]

    @property
    def organization(self) -> Organization | None:
        return None


# Protocol wrappers that passthrough dictionaries with attribute access
class Problem(DictWrapper):
    """Problem wrapper."""

    pass


class Medication(DictWrapper):
    """Medication wrapper."""

    pass


class Allergy(DictWrapper):
    """Allergy wrapper."""

    pass


class Immunization(DictWrapper):
    """Immunization wrapper."""

    pass


class VitalSign(DictWrapper):
    """Vital sign wrapper."""

    pass


class VitalSignsOrganizer(DictWrapper):
    """Vital signs organizer wrapper."""

    @property
    def vital_signs(self) -> list:
        """Return list of vital sign observations."""
        vital_signs_data = self._data.get("vital_signs", [])
        return [VitalSign(vs) for vs in vital_signs_data]
