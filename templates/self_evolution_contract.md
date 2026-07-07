# Self-Evolution Contract

```yaml
schema: research_harness_self_evolution_contract.v1
run_id:
trigger:
project_root:
project_id:
intake:
status: pending validation
allowed_auto_status:
  - candidate
  - pending validation
forbidden_auto_status:
  - validated
  - reusable
  - approved
  - pass
  - paper_ready
```

## Done Means

- Recall was run before writing new reusable material.
- Intake was written to disk and copied into the run directory.
- `contract.yaml`, `state.json`, and `trace.jsonl` exist in the run directory.
- Automatic writeback used only `candidate` or `pending validation` status.
- Registries were snapshotted before writeback.
- Registry validation and closeout validation were run after writeback.

## Write Targets

- Knowledge: `G:\knowledge\reusable_knowledge\<category>`
- Prompts: `G:\knowledge\reusable_prompts\<category>`
- Project assets: current project `research_assets\<YYYYMMDD_task_name>`
- Decisions, workflow rules, templates, reports, registries:
  `G:\BaiduSyncdisk\ResearchLoop`

## Forbidden Targets

- `G:\knowledge\_harness`
- `G:\知识库\_harness`
- Raw experimental data copied into reusable knowledge
- Temporary or unreviewed generated files as knowledge cards

## Evidence

- source refs:
- evidence refs:
- verification commands:
- validation reports:

## Next Bottleneck

-
