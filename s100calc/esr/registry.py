"""Runtime registry mapping ESR IDs to their section-property collections.

`ESRRegistry` holds a lookup table per registered ESR, keyed internally by
(designation, Fy) which matches the workbook's two-column lookup exactly.
Registration performs a runtime structural check against
`ESRSectionData` so an ESR implementation missing required fields fails
loudly at registration, not silently via `AttributeError` inside a calc
function.

The module-level `REGISTRY` singleton is the object calc functions import
and query. Applications needing isolation (e.g. tests that want a fresh
registry) can instantiate their own `ESRRegistry()`.
"""
from __future__ import annotations

from typing import Iterable

from s100calc.esr.protocol import ESRSectionData


# Field names the registry verifies at registration time. Kept in sync
# with ESRSectionData; duplicated here deliberately so the error message
# produced by `_missing_fields` is explicit (Protocol introspection via
# typing internals is fragile across Python versions).
_REQUIRED_FIELDS: tuple[str, ...] = (
    "designation", "Fy", "Fu",
    "Ag", "Ix", "rx", "Iy", "ry", "xo", "J", "Cw",
    "Ae",
    "phiPno", "phiPnd", "phiTn",
)


class ESRRegistry:
    """Central registry for ESR section tables.

    Typical usage:
        from s100calc.esr.registry import REGISTRY
        row = REGISTRY.lookup("esr_2093", "51H39-048", 50.0)
        # row satisfies ESRSectionData Protocol
    """

    def __init__(self) -> None:
        self._tables: dict[str, list[ESRSectionData]] = {}

    def register(self, esr_id: str, rows: Iterable[ESRSectionData]) -> None:
        """Register a table of section rows under the given ESR ID.

        Each row is checked against the `ESRSectionData` Protocol. Rows
        missing required fields raise `TypeError` with the field list.

        Re-registering an already-registered `esr_id` overwrites the
        previous table (supports `importlib.reload` during development).
        """
        rows_list = list(rows)
        for i, row in enumerate(rows_list):
            if not isinstance(row, ESRSectionData):
                missing = _missing_fields(row)
                raise TypeError(
                    f"Row {i} in ESR {esr_id!r} does not satisfy "
                    f"ESRSectionData Protocol; missing fields: {missing}"
                )
        self._tables[esr_id] = rows_list

    def is_registered(self, esr_id: str) -> bool:
        """True if an ESR has been registered under this ID."""
        return esr_id in self._tables

    def lookup(
        self, esr_id: str, designation: str, Fy: float
    ) -> ESRSectionData:
        """Return the row matching (designation, Fy) for a registered ESR.

        Raises `KeyError` if the ESR is not registered or no row matches.
        """
        if esr_id not in self._tables:
            known = sorted(self._tables)
            raise KeyError(
                f"ESR {esr_id!r} is not registered. Known: {known}"
            )
        for row in self._tables[esr_id]:
            if row.designation == designation and row.Fy == Fy:
                return row
        raise KeyError(
            f"No row in {esr_id!r} for designation={designation!r}, Fy={Fy}"
        )

    def designations(self, esr_id: str) -> list[str]:
        """Return sorted unique designations for a registered ESR."""
        if esr_id not in self._tables:
            raise KeyError(f"ESR {esr_id!r} is not registered")
        return sorted({row.designation for row in self._tables[esr_id]})

    def registered_ids(self) -> list[str]:
        """Return sorted list of all registered ESR IDs."""
        return sorted(self._tables)


def _missing_fields(obj: object) -> list[str]:
    """Return the ESRSectionData fields that `obj` lacks."""
    return [f for f in _REQUIRED_FIELDS if not hasattr(obj, f)]


# Module-level singleton. Concrete ESR `implementation.py` modules register
# themselves against this on import.
REGISTRY = ESRRegistry()
