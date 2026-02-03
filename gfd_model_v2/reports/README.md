# GFD Flight Reports

This directory contains automatically generated validation reports.

## Report Types

| Prefix | Name | Purpose |
|--------|------|---------|
| `GFD-PFC-*` | Pre-Flight Check | GO/NO-GO for all ENGINE subsystems |
| `GFD-ATR-*` | Advanced Timing Report | Science findings from advanced timing analysis |

## Naming Convention

```
GFD-{TYPE}-{YYYYMMDD}-{HHMMSS}.md
```

## How to Generate

From the DFP Console:
- `[6] Generate Flight Reports` — generates both reports
- `[2] Run All Validation Tests` — also auto-generates reports

From Python:
```python
from report_generator import generate_flight_reports
result = generate_flight_reports()
```

## Cross-References

Every Advanced Timing Report references its Pre-Flight Check by document ID,
creating an audit trail. You can always find which pre-flight check a given
advanced analysis was based on.

## Note

Reports are `.gitignore`-able — they are generated artifacts, not source.
Add `reports/GFD-*.md` to `.gitignore` if you don't want to track them.
