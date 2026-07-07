# Legacy `G:\知识库\_harness` Inventory And Migration Plan

## Scope

- legacy_path: `G:\知识库\_harness`
- canonical_harness: `G:\BaiduSyncdisk\ResearchLoop`
- inventory_date: 2026-06-26
- pre_delete_file_count: 120
- pre_delete_total_size: 165499 bytes
- pre_delete_total_size_kb: 161.62

## Evidence Read

- `G:\AGENTS.md`
- `G:\CLAUDE.md`
- `G:\.workspace.yaml`
- `G:\BaiduSyncdisk\ResearchLoop\AGENTS.md`
- `G:\BaiduSyncdisk\ResearchLoop\README.md`
- `G:\BaiduSyncdisk\ResearchLoop\harness.yaml`
- `G:\知识库\_harness\10-workflows\research-agent\*.md`
- `G:\知识库\_harness\40-memory\case-bank\**\*.yaml`
- `G:\知识库\_harness\40-memory\memory-deltas\pending\*.yaml`
- `G:\知识库\_harness\50-evals\contracts\*\*.yaml`
- `G:\知识库\_harness\50-evals\review-checklists\*.md`
- `G:\知识库\_harness\reports\2026-06-22_workspace_ingestion_report.md`

## Extension Summary

| Extension | Count |
|---|---:|
| `.md` | 68 |
| `.yaml` | 29 |
| `.json` | 6 |
| `.toml` | 6 |
| `.gitkeep` | 5 |
| `.py` | 4 |
| `.pyc` | 2 |

## Migration Decision

The old directory is not the current harness. Its durable value is the asset-review pattern, validation contract seeds, and domain case-bank entries. The directory structure, agent wrappers, pycache, and references to old `_harness` roots should not be mirrored into the canonical harness.

## Migrated Concepts

| Legacy source | New target |
|---|---|
| `task-lifecycle.md` | `workflows/paper_lifecycle/paper_state_machine.yaml` |
| `cross-project-reuse.md` | `registry/asset_evolution.yaml` reuse policy |
| `memory-update-workflow.md` | `asset_candidate_gate` and `research_retro.md` |
| `scientific-figure-quality.v1.yaml` | `workflows/paper_lifecycle/validation_rules.yaml` |
| `claim-boundary.v1.yaml` | `workflows/paper_lifecycle/validation_rules.yaml` |
| `literature-citation-quality.v1.yaml` | `workflows/paper_lifecycle/validation_rules.yaml` |
| `algorithm-validation-quality.v1.yaml` | `workflows/paper_lifecycle/validation_rules.yaml` |
| `ppt-quality.v1.yaml` | `workflows/paper_lifecycle/validation_rules.yaml` |
| `conversation_to_harness_memory.md` | `templates/research_project/research_retro.md` and reusable prompt closeout |

## Legacy Case-Bank Seed Assets

All legacy case-bank entries are migrated as `candidate` assets. No legacy `active` or `draft` status is carried forward as `reusable`.

| Legacy asset id | New asset type | Status |
|---|---|---|
| `case.figure.sc_nmt_mie_core_figure_workflow.v1` | `figure_style` | candidate |
| `case.figure.lif_mie_support_mask_relative_smd_visualization.v1` | `figure_style` | candidate |
| `case.figure.lif_mie_signal_branch_baseline_contract.v1` | `workflow_rule` | candidate |
| `case.literature.claims_evidence_matrix.v1` | `validation_rule` | candidate |
| `case.literature.chinese_academic_model_review.v1` | `prompt` | candidate |
| `case.literature.pdf_markdown_openviking_ingestion.v1` | `dataset_recipe` | candidate |
| `case.literature.desktop_ingestion_dedup_manifest.v1` | `dataset_recipe` | candidate |
| `case.experiment.agent_artifact_archiving_manifest.v1` | `workflow_rule` | candidate |
| `case.experiment.conservative_descatter_background_handling.v1` | `dataset_recipe` | candidate |
| `case.ppt.editable_text_and_figure_separation.v1` | `dissemination_recipe` | candidate |
| `case.reconstruction.art_sart_projection_alignment.v1` | `validation_rule` | candidate |
| `case.reconstruction.lif_mie_2d_to_3d_calibration_bridge.v1` | `workflow_rule` | candidate |
| `case.reconstruction.relative_equivalent_mie_claim_boundary.v1` | `validation_rule` | candidate |
| `case.reconstruction.spray_3d_review_skill_distillation.v1` | `narrative_pattern` | candidate |
| `case.reconstruction.wuyuxuan_flame_3d_inheritance.v1` | `workflow_rule` | candidate |

## Not Migrated

- old agent TOML wrappers
- old root README/AGENTS/CLAUDE skeleton
- `__pycache__`
- old validation script copies
- old acceptance checklist that assumes `G:\knowledge\_harness`
- generated traces as durable registry entries

## Delete Verification Plan

```powershell
$target = Resolve-Path -LiteralPath 'G:\知识库\_harness'
if ($target.Path -eq 'G:\知识库\_harness') {
  Remove-Item -LiteralPath 'G:\知识库\_harness' -Recurse -Force
}
Test-Path -LiteralPath 'G:\知识库\_harness'
Test-Path -LiteralPath 'G:\knowledge\_harness'
python scripts\closeout_check.py
```

## Post Delete Verification

- `G:\知识库\_harness`: `False`
- `G:\knowledge\_harness`: `False`
- closeout_check_after_delete: `ok=True`; run_id `20260626_173416_closeout-check_1f43ee3e`; report `G:\BaiduSyncdisk\ResearchLoop\reports\health\20260626_closeout_health.md`
