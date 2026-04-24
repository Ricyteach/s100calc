"""s100calc.esr — ESR (ICC-ES Evaluation Service Report) infrastructure.

Ships mechanics only. No ESR property data is bundled with the library;
concrete ESR implementations live in user/test code and register
themselves with the module-level `REGISTRY` at import time.

Public symbols:
  ESRSectionData      (Protocol) — consumption-side type contract
  ESRSectionDataBase  (dataclass) — creation-side base class
  read_csv_rows       — CSV loader helper for ESR implementations
  ESRRegistry         — registry class (instantiate for isolation)
  REGISTRY            — module-level singleton
"""
from s100calc.esr.abc import ESRSectionDataBase, read_csv_rows
from s100calc.esr.protocol import ESRSectionData
from s100calc.esr.registry import ESRRegistry, REGISTRY

__all__ = [
    "ESRSectionData",
    "ESRSectionDataBase",
    "read_csv_rows",
    "ESRRegistry",
    "REGISTRY",
]
