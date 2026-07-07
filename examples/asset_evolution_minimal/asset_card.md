# Reusable Asset Card

## Asset Name

- name: Minimal line comparison figure style candidate
- asset_id: asset.figure_style.minimal_line_comparison.v1
- asset_type: figure_style

## Problem Solved

- problem: show how a figure style candidate records v0/v1 quality iteration.
- why_reusable: it is a tiny fixture for testing the asset evolution validator.

## Applicable Contexts

- dry-run examples
- small workflow demonstrations

## Non Applicable Contexts

- final journal figures
- scientific claims requiring real data

## Source Project / Source Outputs

- source_project: ResearchLoop
- source_output_objects: asset_evolution_minimal_output
- source_claims: C1
- source_figures: F1

## Minimal Reproduction

```powershell
python scripts\validate_asset_evolution.py --registry registry\asset_evolution.yaml --json
```

## Dependency Files

- `examples/asset_evolution_minimal/05_figure_registry.yaml`
- `examples/asset_evolution_minimal/reproduction_entry.md`

## How To Use

- Copy the card structure.
- Replace the fixture paths with real figure scripts and review evidence.
- Keep status as `candidate` until reuse is validated.

## Quality Score

- score: 3.0
- evidence: validator dry-run only
- reviewer: ResearchLoop

## Known Issues

- no target journal comparison
- no real plotting script

## Next Upgrade Direction

- reuse in one real figure pack
- record before/after image paths and reviewer feedback

## Version History

| Version | Date | Change | Evidence |
|---|---|---|---|
| v1 | 2026-06-26 | seed candidate | `registry/asset_evolution.yaml` |

## Replacement Relationship

- replaces:
- replaced_by:
- deprecation_reason:

## Closeout Decision Record

- decision_id: 20260626_asset_evolution_loop_upgrade
- decision_path: G:\BaiduSyncdisk\ResearchLoop\decisions\20260626_asset_evolution_loop_upgrade.md
- status: planned during implementation
