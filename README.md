# s100calc

AISI S100 cold-formed steel member design checks, implemented in Python using the
[efficalc](https://github.com/youandvern/efficalc) calculation-as-documentation framework.

Currently covers axial compression and tension for hat section truss members per both
AISI S100-2016 and S100-2024, using section properties from ICC-ES evaluation reports.

## Installation

```bash
pip install -e ".[dev]"
```

## Running the tests

Tests use a captured oracle of known-good results from the reference Excel workbook.

```bash
pytest
```

## Structure

```
s100calc/
    esr/          — ESR section property registry and ABC/Protocol definitions
    calc/         — AISI S100 calculation functions (efficalc-based)
tests/
    conftest.py   — loads test vectors from the oracle CSV
```

## Reference documents

- AISI S100-2016: North American Specification for the Design of Cold-Formed Steel Structural Members
- AISI S100-2024: North American Specification for the Design of Cold-Formed Steel Structural Members
- ICC-ES ESR-2093: CSTRUSS Hat Section Members
