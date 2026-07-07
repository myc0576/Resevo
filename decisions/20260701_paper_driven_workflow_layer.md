# Paper-Driven Workflow Layer For Optical Tomography Papers

```yaml
id: 20260701_paper_driven_workflow_layer
project_id: researchloop
date: 2026-07-01
status: validated
changed_route_or_assumption: true
```

## Decision

Add a thin paper-driven workflow layer for 3D LIF/MIE, spray optical tomography, and limited-angle 3D reconstruction tasks.

## Context

ResearchLoop already had a paper lifecycle and asset evolution loop. The new layer makes five operational surfaces explicit: paper loop, literature intake, figure intake, experiment closeout, and reviewer gate. This avoids mixing raw PDFs, visual inspiration, claim evidence, and paper-readiness decisions into one loose closeout step.

## Alternatives Considered

| Alternative | Why Rejected Or Deferred |
|---|---|
| Fold everything into `workflows/paper_lifecycle/README.md` | Too dense; the user asked for named workflow files. |
| Create a new heavy validator for every paper field | Deferred to keep this change small and reviewable. |
| Copy literature PDFs into knowledge for easier retrieval | Rejected because reusable knowledge should store cards, summaries, evidence use, and citation locations, not PDF originals. |

## Evidence

- Files: `workflows/paper_driven/*.md`, `templates/paper_contract.md`, `registry/papers.yaml`, `registry/literature.yaml`, `registry/figures.yaml`.
- Commands: `python scripts\registry_tool.py validate`, `python scripts\evaluator.py evaluate --target all --json`, and `python scripts\closeout_check.py`.
- Verification status: run after implementation.

## Consequences

- Paper contracts become the front door for paper-bound research tasks.
- Literature intake records source use without copying PDF originals into reusable knowledge.
- Visual references live under `visual_refs/` and require figure cards.
- Each research task closeout must explicitly decide whether to create reusable knowledge, reusable prompts, research assets, or decision records.
- Strong claims pass through reviewer-gate boundary checks before being written as paper claims.

## Follow-up

- Add a dedicated paper-contract validator if multiple real paper projects start using this layer.
- Replace the Mie-Pk-TV-S example placeholders with path-bound project evidence when the user starts the actual paper pack.
