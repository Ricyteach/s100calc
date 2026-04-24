"""Concrete ESRSectionDataBase implementation for ICC-ES ESR-2093.

This module is the canonical worked example of the ESR extensibility
pattern. It lives in `tests/` rather than in the installed package
because s100calc ships mechanics only; ESR property data is supplied
by the user. See docs/adding_an_esr.md for the walkthrough.

Pattern:
  1. Subclass `ESRSectionDataBase`, adding ESR-specific audit-only fields
     as dataclass fields with defaults.
  2. Provide a `from_csv_row()` classmethod that maps CSV column names
     to dataclass attribute names, handling unit-suffix stripping and
     any AISI-vs-ESR symbol remaps (e.g. ESR-2093's `Yo` -> AISI `xo`).
  3. Load the CSV, build rows, register with `REGISTRY` at module
     import time.

Registration occurs at import; users of this ESR trigger it by simply
importing the module.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from s100calc.esr.abc import ESRSectionDataBase, read_csv_rows
from s100calc.esr.registry import REGISTRY


ESR_ID = "esr_2093"
CSV_PATH = Path(__file__).parent / "esr_2093.csv"


@dataclass
class ESRData2093(ESRSectionDataBase):
    """ESR-2093 row: required AISI fields (inherited) plus audit fields.

    The audit-only fields below are carried for test verification and
    potential future use (bending checks). The s100calc library itself
    consumes only the inherited required fields.

    The ESR-2093 Yo -> AISI xo remap is performed in `from_csv_row`.
    """

    # Identification / metadata
    Key: str = ""
    TradeName: str = ""
    Gauge: str = ""

    # Geometry
    t_in: float = 0.0
    Web_in: float = 0.0
    Flange_in: float = 0.0

    # Polar radius of gyration tabulated by ESR (audit-only; the library
    # computes ro from first principles per AISI in each calc function).
    ro_tab: float = 0.0

    # Bending properties (y-y axis: symmetric; x-x axis: +/- separately
    # tabulated because top vs bottom flange compression gives different
    # effective section properties).
    Iye: float = 0.0
    Sye: float = 0.0
    phiMnyo: float = 0.0          # kip-in
    posIxe: float = 0.0
    posSxe: float = 0.0
    posPhiMnxo: float = 0.0       # kip-in
    negIxe: float = 0.0
    negSxe: float = 0.0
    negPhiMnxo: float = 0.0       # kip-in
    negPhiMnd: float = 0.0        # kip-in (distortional, neg bending)

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "ESRData2093":
        """Map one ESR-2093 CSV row to a populated instance.

        Column -> attribute mapping:
          - Unit suffixes stripped (Ag_in2 -> Ag, Fy_ksi -> Fy, ...)
          - yo_in -> xo (AISI uses xo; ESR-2093 tabulates as Yo)
          - ro_in -> ro_tab (audit-only; library computes ro from
            first principles, so the tabulated value is parked on a
            differently-named attribute to avoid accidental consumption
            by calc functions).
        """
        def f(k: str) -> float:
            return float(row[k])

        return cls(
            # Required (inherited) AISI fields
            designation=row["MemberDesig"],
            Fy=f("Fy_ksi"),
            Fu=f("Fu_ksi"),
            Ag=f("Ag_in2"),
            Ix=f("Ix_in4"),
            rx=f("rx_in"),
            Iy=f("Iy_in4"),
            ry=f("ry_in"),
            xo=f("yo_in"),              # AISI notation remap
            J=f("J_in4"),
            Cw=f("Cw_in6"),
            Ae=f("Ae_in2"),
            phiPno=f("phiPno_lb"),
            phiPnd=f("phiPnd_lb"),
            phiTn=f("phiTn_lb"),
            # ESR-2093-specific audit fields
            Key=row["Key"],
            TradeName=row["TradeName"],
            Gauge=str(row["Gauge"]),
            t_in=f("t_in"),
            Web_in=f("Web_in"),
            Flange_in=f("Flange_in"),
            ro_tab=f("ro_in"),
            Iye=f("Iye_in4"),
            Sye=f("Sye_in3"),
            phiMnyo=f("phiMnyo_inkip"),
            posIxe=f("posIxe_in4"),
            posSxe=f("posSxe_in3"),
            posPhiMnxo=f("posPhiMnxo_inkip"),
            negIxe=f("negIxe_in4"),
            negSxe=f("negSxe_in3"),
            negPhiMnxo=f("negPhiMnxo_inkip"),
            negPhiMnd=f("negPhiMnd_inkip"),
        )


def _load_and_register() -> None:
    raw = read_csv_rows(CSV_PATH)
    rows = [ESRData2093.from_csv_row(r) for r in raw]
    REGISTRY.register(ESR_ID, rows)


# Side-effect: registration on import. Idempotent because register() allows
# overwrite for importlib.reload scenarios.
_load_and_register()
