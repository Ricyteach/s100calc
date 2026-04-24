"""Consumption-side type contract for ESR section property rows.

`ESRSectionData` is the runtime-checkable Protocol that every row returned
by `ESRRegistry.lookup()` must satisfy. Calc functions in s100calc
(compression_s100_16, compression_s100_24, tension) annotate their section
parameter against this Protocol, so mypy flags missing fields at the call
site regardless of whether the concrete row inherits from `ESRSectionDataBase`
or is a standalone dataclass.

Attribute names follow AISI S100 notation, without unit suffixes. This is the
library-facing vocabulary. The CSV column names and their unit suffixes
(e.g. `Ag_in2`, `yo_in`) are an implementation detail of each concrete ESR
subclass's `from_csv_row()` factory, not visible here.

Note on `xo`: AISI S100 uses `xo` for the shear-center offset. ESR-2093
tabulates the same quantity as `Yo` (ESR coordinate convention). The
Protocol normalizes to the AISI symbol; concrete ESR subclasses handle the
remap in their CSV factory.
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class ESRSectionData(Protocol):
    """Required fields on every ESR row consumed by s100calc calc functions.

    Unit conventions:
      - Lengths: in, in², in⁴, in⁶
      - Stresses (Fy, Fu): ksi
      - Capacities (phi-values): lb
    """

    # Identification
    designation: str
    Fy: float
    Fu: float

    # Gross-section properties
    Ag: float
    Ix: float
    rx: float
    Iy: float
    ry: float
    xo: float
    J: float
    Cw: float

    # Effective-section property (used in compression)
    Ae: float

    # ESR-tabulated LRFD capacities (phi applied)
    phiPno: float
    phiPnd: float
    phiTn: float
