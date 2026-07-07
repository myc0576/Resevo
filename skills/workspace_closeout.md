# Skill: Workspace Closeout

## Purpose

This skill applies to every meaningful task performed under `G:\`. It prevents useful process knowledge, prompts, scripts, evidence, and research assets from remaining only in a chat transcript or a project output folder.

## Path Resolution

When the user says `harness`, `沉淀到 harness`, `写入 harness`, or `更新 harness`, resolve it to:

```text
G:\BaiduSyncdisk\ResearchLoop
```

Do not write to `G:\knowledge\_harness`. Do not recreate or write to `G:\知识库\_harness`; its useful contents were migrated into the canonical harness as a cleanup report and candidate assets.

## Trigger

Run before the final assistant response whenever the task touches `G:\` and any of the following are true:

- A reusable workflow, prompt, script, configuration, template, report, figure, CAD model, PPT, dataset manifest, or verification pattern was produced.
- A project route, assumption, design standard, or feedback loop changed.
- A failure exposed a reusable lesson or missing rule.
- The user explicitly asks for work to be preserved, remembered, archived, indexed, or沉淀.

If none of these apply, state in the final response: `closeout checked: no reusable assets`.

## Procedure

1. Identify the current project:
   - Prefer the nearest `G:\projects\<project_name>` ancestor.
   - If no project ancestor exists, use `g-workspace`.

2. Run goal alignment:
   - What goal did this task serve?
   - Did it change the route, assumption, design standard, or system design?

3. Review process:
   - Input, process, output.
   - Reusable code, config, prompt, workflow, report, or evidence.

4. Verify evidence:
   - Use paths, logs, metrics, images, reports, reproduction commands, or file-existence checks.
   - Mark unsupported conclusions as `hypothesis` or `pending validation`.

5. Capture assets:
   - Project-local outputs go to `<project>\research_assets\YYYYMMDD_task_name`.
   - Write `00_asset_manifest.md` and `reproduction_entry.md`.
   - Do not copy large raw data, binary CAD files, model files, or temporary files into `G:\knowledge`.

6. Capture reusable knowledge:
   - Write a knowledge card in `G:\knowledge\reusable_knowledge\<category>`.
   - Keep only conclusion, scope, steps, parameters, risks, evidence, and unverified boundaries.

7. Capture reusable prompts:
   - Write a prompt card in `G:\knowledge\reusable_prompts\<category>`.
   - Include task, input, output, prompt body, model, notes, and revision history.

8. Update registries:
   - `registry\projects.yaml`
   - `registry\knowledge.yaml`
   - `registry\prompts.yaml`
   - `registry\research_assets.yaml`
   - `registry\output_objects.yaml`
   - `registry\asset_evolution.yaml`
   - `registry\workflow_improvement_backlog.yaml`
   - `registry\decisions.yaml` when route or assumptions changed.

9. Validate:
   - Parse registry YAML.
   - Check referenced paths exist.
   - Run keyword retrieval for the new topic when practical.

## Non-Goals

- This is not a background daemon.
- This does not copy project outputs into knowledge.
- This does not promote unverified claims into validated scientific conclusions.
