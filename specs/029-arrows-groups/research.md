# Research: Arrows of Groups category implementation (`cat.arrows_groups`)

Decisions of this feature, and the survey record of its versions. The shared decisions are those of [001 research](../001-category-implementations/research.md).

## Decisions

**R1. Named group maps come from the groups implementation.** The v1 kernel handler lowers `mor.groups.sign`, `mor.groups.identity`, `mor.groups.trivial`, `identity`, `zero` and `compose` itself (`gap_groups.py:134-176` at `8b181d7`). The lowering of the named group maps is the lowering table of `backends/groups.py` (LV1, one lowering table).

## Survey record

LV7 fixes the content, and 001 research, "Survey record", fixes the row format. The survey tasks T001 (V2) add the rows of their version before its implementation tasks. The record starts from the engine survey sections that the plan names.

| Part (generated interface) | Engine and routine | Container command | Version or revision | Decision | Reasons | Gap searches |
| --- | --- | --- | --- | --- | --- | --- |
