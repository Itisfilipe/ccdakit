"""Protocol for immunization data.

This module defines the protocol (interface) for immunization objects.
Any object that implements ImmunizationProtocol can be passed to the
ImmunizationActivity builder.
"""

from datetime import date, datetime
from typing import Optional, Protocol


class ImmunizationProtocol(Protocol):
    """Protocol for immunization data.

    Defines the interface that immunization objects must implement to be
    used with the ImmunizationActivity builder.

    Attributes:
        vaccine_name: Name of the vaccine (e.g., "Influenza vaccine")
        cvx_code: CVX code for the vaccine (CDC vaccine code system)
        administration_date: Date the vaccine was administered
        status: Status of the immunization (e.g., "completed", "refused")
        lot_number: Optional vaccine lot number
        manufacturer: Optional vaccine manufacturer name
        route: Optional route of administration (e.g., "Intramuscular", "Oral")
        site: Optional body site where vaccine was administered
        dose_quantity: Optional dose quantity and unit (e.g., "0.5 mL")
    """

    vaccine_name: str
    cvx_code: str
    administration_date: date | datetime
    status: str
    lot_number: Optional[str]
    manufacturer: Optional[str]
    route: Optional[str]
    site: Optional[str]
    dose_quantity: Optional[str]
