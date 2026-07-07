# Decision: Require Workspace Closeout For G Drive Work

## Date

2026-06-23

## Project

g-workspace

## Decision

All meaningful work performed under `G:\` must run workspace closeout before the final assistant response. This includes SC-NMT, CAD modeling, PPT work, paper writing, scripts, project architecture, experiment workflows, and other project outputs.

## Rationale

Session `019ef32c-2559-7a43-848f-f4a87ff12856` produced reusable SolidWorks/API modeling outputs and verification reports, but the closeout stopped at a final recommendation instead of a required writeback. The missing rule was not a storage problem; it was a trigger-scope problem.

## Consequences

- Root `G:\AGENTS.md` now points all workspace tasks to the research harness closeout rule.
- Harness rules now cover all `G:\` work, not only SC-NMT or explicitly labeled research projects.
- A new `workspace_closeout` skill defines the concrete procedure.
- A no-op closeout statement is required when no reusable asset exists.

## Status

validated
