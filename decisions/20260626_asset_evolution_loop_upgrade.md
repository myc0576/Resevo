# Decision: Asset Evolution Loop Upgrade

## Date

2026-06-26

## Project

researchloop

## Decision

Upgrade ResearchLoop from closeout governance into a paper-driven output lifecycle with an Asset Evolution Loop. Every research project should bind to output objects, claims, figures, release artifacts and dissemination materials; every reusable pattern should begin as a candidate asset and earn reusable status only after review or reuse evidence.

## Rationale

The existing harness had strong closeout, registry and evaluation mechanics, but it did not yet model the full path from paper idea to reusable assets. The legacy `G:\知识库\_harness` contained useful first-generation case-bank assets and validation contracts, but it also carried obsolete paths and wrappers. Migrating only the useful ideas as candidate assets preserves the lessons without keeping an ambiguous harness root alive.

## Consequences

- `registry/output_objects.yaml` becomes the first stop for paper, release, PPT and dissemination work.
- `registry/asset_evolution.yaml` tracks candidate/reviewed/reusable/deprecated/replaced assets.
- `registry/workflow_improvement_backlog.yaml` records workflow pain points from retros, failed runs, reviews and validators.
- `workflows/paper_lifecycle/` now defines paper lifecycle states, gates and validation rules.
- Legacy case-bank entries are seed candidates, not reusable assets.
- `G:\知识库\_harness` is removed after migration and should not be recreated.

## Alternatives Considered

- Mirror the old `_harness` directory into the new harness. Rejected because it would preserve obsolete roots, wrappers and duplicate structure.
- Promote old active case-bank entries directly to reusable. Rejected because old active status does not satisfy the new reuse gate.
- Keep the old directory as a permanent read-only reference. Rejected because it continued path ambiguity after its useful content was inventoried.

## Verification

- `python -m py_compile scripts\validate_research_project.py scripts\validate_asset_evolution.py scripts\registry_tool.py scripts\evaluator.py scripts\kb_index.py`
- `python scripts\validate_research_project.py --project-root examples\paper_lifecycle_minimal --json`
- `python scripts\validate_asset_evolution.py --registry registry\asset_evolution.yaml --json`
- `python scripts\registry_tool.py validate`
- `python scripts\evaluator.py evaluate --target all --json`
- `python scripts\closeout_check.py`

## Status

implemented
