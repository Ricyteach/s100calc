"""Creation-side type contract for ESR section property rows.

`ESRSectionDataBase` is a dataclass that new ESR implementations should
inherit from. Inheritance gives IDE/mypy feedback at class-definition
time when required fields are missing, complementing the runtime
structural check the registry performs against `ESRSectionData` at
registration time.

Design note: we use a `@dataclass` rather than `abc.ABC`+`@abstractmethod`
properties because dataclass inheritance achieves the same "missing fields
flagged at subclass definition" goal with vastly less boilerplate for 15
required fields. The "ABC" name is kept to signal intent.

`read_csv_rows()` lives here rather than in a standalone module because
CSV parsing is part of the creation-side contract: a typical ESR
implementation instantiates its rows from a committed CSV file shipped
alongside its subclass definition.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ESRSectionDataBase:
    """Base for concrete ESR section-property dataclasses.

    Subclasses inherit all 15 required fields and may add ESR-specific
    audit fields (e.g. `ro_tab`, bending properties) as additional
    dataclass fields with defaults.

    See `ESRSectionData` in `protocol.py` for field semantics and units.
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

    # Effective-section property
    Ae: float

    # ESR-tabulated LRFD capacities
    phiPno: float
    phiPnd: float
    phiTn: float

    @staticmethod
    def astm_a1003_fu(Fy: float) -> float:
        """Return Fu per ASTM A1003 for cold-formed steel framing members.

        Useful for concrete ESR implementations whose tables do not tabulate
        Fu explicitly. Typical call site is the subclass's `from_csv_row`
        factory when the CSV lacks an `Fu_ksi` column.

        Mapping:
          Fy = 50 ksi -> Fu = 65 ksi
          Fy = 70 ksi -> Fu = 80 ksi

        Raises ValueError for other Fy values; add cases here if a future
        ESR registers sections at a different grade.
        """
        match Fy:
            case 50.0:
                return 65.0
            case 70.0:
                return 80.0
            case _:
                raise ValueError(
                    f"ASTM A1003 Fu default not defined for Fy={Fy} ksi. "
                    "Override Fu explicitly in your ESR subclass."
                )


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Load a CSV file as a list of dicts (str keys -> str values).

    Type coercion is intentionally deferred to the concrete ESR subclass's
    factory (typically `from_csv_row`), so unit parsing and remaps
    (e.g. `yo_in` -> `xo`) stay co-located with the ESR-specific logic.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"ESR CSV not found: {p}")
    with p.open(newline="") as f:
        return list(csv.DictReader(f))
