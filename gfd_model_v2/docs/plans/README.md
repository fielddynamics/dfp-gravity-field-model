# GFD Planning Documents

Design specifications and implementation plans for GFD Model V2 expansions.

## Current Plans

| Document | Status | Scope |
|----------|--------|-------|
| [Advanced Timing Analysis Plan](advanced_timing_analysis_plan.md) | Planning | 7 new test modules across `timing_analysis/` (core) and `timing_analysis_advanced/` |
| [Report Generation Plan](report_generation_plan.md) | Planning | `report_generator.py` — Pre-Flight Check + Advanced Timing reports |

## Conventions

Plans follow a consistent format:
- **Executive summary** — what and why
- **Module specifications** — test-by-test detail with inspiration sources
- **Implementation priority** — phased rollout
- **Dependency map** — what builds on what
- **Console registration** — how it plugs into `dfp_console.py`
