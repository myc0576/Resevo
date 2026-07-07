# Research Retro

## Output

- output_type: figure pack
- output_object: asset_evolution_minimal_output
- date: 2026-06-26
- project: ResearchLoop

## What Improved

- The v1 figure record links a claim, output object, style pack and reproduction entry.

## Still Weak

- It is a dry-run fixture, not a real journal style review.

## Failed Attempts

- v0 had no explicit asset boundary.

## Reusable Asset Candidates

| Candidate | Asset type | Source claim/figure/output | Why candidate | Required review |
|---|---|---|---|---|
| asset.figure_style.minimal_line_comparison.v1 | figure_style | C1/F1/asset_evolution_minimal_output | tests validator shape | one real reuse |

## Old Assets To Deprecate

- asset_id:
- reason:
- successor:

## Prompts To Upgrade

- prompt: retro-to-candidate asset extraction
- issue: candidate status must be default
- proposed_upgrade: require applicable and non-applicable contexts

## Validation Rules To Upgrade

- rule: asset_candidate_gate
- issue: reusable promotion needs asset_card and reproduction
- proposed_upgrade: validate via `validate_asset_evolution.py`

## Reusable Knowledge

- should_enter_reusable_knowledge: yes
- category: paper_writing
- evidence: this fixture and legacy migration report

## Reusable Prompts

- should_enter_reusable_prompts: yes
- category: paper_writing
- evidence: prompt card for retro-to-candidate extraction

## Workflow Improvement Action

- pain_point: asset evolution examples were absent.
- proposed_fix: add minimal fixture and backlog item.
- validation_method: asset validator and registry validator.
- backlog_issue_id: WIB-20260626-minimal-asset-retro
