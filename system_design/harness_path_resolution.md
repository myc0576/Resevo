# Harness Path Resolution

## Problem

The word `harness` became ambiguous because older memory and previous work mentioned `_harness` under knowledge directories, while the current English research harness lives at `G:\BaiduSyncdisk\ResearchLoop`.

This caused a failure mode: when the user asked another project to “沉淀到 harness,” the project could interpret that as `G:\knowledge\_harness` instead of the current canonical harness.

## Canonical Rule

Inside the `G:\` workspace, `harness` always resolves to:

```text
G:\BaiduSyncdisk\ResearchLoop
```

The following phrases also resolve to `G:\BaiduSyncdisk\ResearchLoop`:

- 沉淀到 harness
- 写入 harness
- 更新 harness
- harness closeout
- research harness

## Non-Targets

Do not write to:

```text
G:\knowledge\_harness
```

This is a deprecated or ambiguous path and should not be created as a compatibility target.

Do not write to:

```text
G:\知识库\_harness
```

This path has been migrated and removed. Its useful case-bank material is represented by `reports\legacy_cleanup\20260626_zhishiku_harness_inventory.md` and `registry\asset_evolution.yaml` candidate assets. Do not recreate it.

## Write Targets

- Harness rules, skills, templates, reports, registries, and decisions: `G:\BaiduSyncdisk\ResearchLoop`
- Reusable knowledge cards: `G:\knowledge\reusable_knowledge`
- Reusable prompt cards: `G:\knowledge\reusable_prompts`
- Project-local assets and reproduction entries: `<project>\research_assets\YYYYMMDD_task_name`

## Required Behavior

If an older memory, project note, or user wording conflicts with this rule, prefer this rule and record the conflict as a decision or closeout note when it affects the task outcome.
