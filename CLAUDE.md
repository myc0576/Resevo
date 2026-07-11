# CLAUDE.md

This file provides guidance to Claude Code when working on MycEvo in
`<MycEvo路径>`.

MycEvo is the project brand and the current canonical local entry is
`<MycEvo路径>`. The historical name `research-harness` should be
treated only as an old path or compatibility identifier, not as the recommended
working directory.

## 语言

默认使用中文简体回复。结论必须基于刚读取的文件、刚运行的命令或明确证据。

## Canonical Targets

- MycEvo local root: `<MycEvo路径>`
- Reusable knowledge: `<knowledge-root>\reusable_knowledge`
- Reusable prompts: `<knowledge-root>\reusable_prompts`
- Forbidden harness write roots: `<knowledge-root>\_harness`, `<legacy-knowledge-root>\_harness`

Do not treat legacy `_harness` paths as write targets.

## Self-Evolution Trigger

When the user says any broad harness trigger such as `自进化`, `沉淀`,
`更新`, `写回`, `复用`, `调用 harness`, `查历史`, `closeout`, `loop`,
`一键 loop`, or `retro`, use the self-evolution loop:

```powershell
mycevo recall --query "<task>" --project-root <cwd>
mycevo intake --project-root <cwd> --trigger "自进化" --out <intake.yaml>
mycevo self-evolution run --intake <intake.yaml> --apply-candidates --json
```

Claude Code should create or fill `templates\self_evolution_intake.yaml` from
the current task context before running writeback. The runner writes
`contract.yaml`, `state.json`, and `trace.jsonl` under `runs\YYYYMMDD\<run_id>`.

Automatic writeback is candidate-first only. Do not auto-promote to
`validated`, `reusable`, `approved`, `pass`, or `paper_ready`.

## Starter Workflow Onboarding

On the first interaction in a fresh MycEvo checkout, check whether the
optional Nature Skills starter workflow has already been handled:

```powershell
mycevo status
```

If the result has `needs_prompt: true`, ask one structured AskUserQuestion-style
question with these choices:

- download Nature Skills to `external\nature-skills`;
- skip for now, then run `mark --decision skipped`;
- do not ask again, then run `mark --decision dismissed`.

Only run the installer after explicit user consent:

```powershell
mycevo workspace add nature-skills <starter-workflow-path>
```

This is clone-and-reference only. Do not install dependencies, configure
credentials, or copy skills into `%USERPROFILE%\.codex\skills` by default. If an
existing local clone is dirty or the local path is not a git checkout, stop and
report the blocker.

## Visual-To-Editable

When a task asks to convert an image, screenshot, PDF page, chart, table,
scientific figure, flowchart, formula image, or UI screenshot into editable
assets, treat it as a Figure Loop / closeout extension. Do not treat
MycEvo as the converter.

Use the router first:

```powershell
python scripts\visual_to_editable_router.py classify --request <request.yaml> --json
python scripts\visual_to_editable_router.py validate-manifest --manifest <visual_reconstruction_manifest.yaml> --json
python scripts\visual_to_editable_router.py validate-case --case-dir <case_dir> --json
```

Actual reconstruction stays with Claude Code, Codex, Cursor, or an external
skill. MycEvo stores only templates, prompts, manifests, QA summaries,
reproduction notes, registry entries, and sanitized examples. Do not commit raw
screenshots, PDFs, private experiment figures, final paper figures, generated
PPTX files, large binaries, credentials, or tool traces.

## Verification

After edits, run the relevant focused tests plus the harness validation chain:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
python -m pytest
python scripts\visual_to_editable_router.py validate-case --case-dir examples\visual_to_editable_minimal --json
python scripts\registry_tool.py validate
python scripts\evaluator.py evaluate --target all --json
python scripts\kb_index.py rebuild
python scripts\closeout_check.py
```
