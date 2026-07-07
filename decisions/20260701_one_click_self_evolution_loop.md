# Decision: One-click self-evolution loop becomes the harness writeback surface

```yaml
id: 20260701_one_click_self_evolution_loop
project_id: researchloop
date: 2026-07-01
status: validated
changed_route_or_assumption: true
```

## Decision

ResearchLoop now treats self-evolution as a first-class loop. When a G
drive task uses trigger words such as `自进化`, `沉淀`, `更新`, `写回`,
`复用`, `调用 harness`, `查历史`, `closeout`, or `loop`, the Agent first
runs recall, then writes an intake file, then uses
`scripts/self_evolution_loop.py` for candidate-first writeback, trace capture,
restart state, registry update, and validation.

## Context

The prior system had strong closeout validators and registries, but the
operating surface still depended on the Agent remembering to convert a task
into knowledge, prompts, research assets, decisions, and backlog entries. The
new loop makes that conversion explicit and restartable through three run-local
files: `contract.yaml`, `state.json`, and `trace.jsonl`.

## Alternatives Considered

- Keep manual closeout only: rejected because valuable task evidence can remain
  in chat rather than becoming searchable assets.
- Build a large multi-agent scheduler first: rejected because the current
  harness already has scripts for registry validation, evaluation, indexing,
  run capture, and closeout checks.
- Let the runner read chat transcripts directly: rejected because the Agent
  can produce a cleaner, auditable intake contract from the active context.

## Evidence

- `G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py`
- `G:\BaiduSyncdisk\ResearchLoop\workflows\self_evolution_loop\README.md`
- `G:\BaiduSyncdisk\ResearchLoop\templates\self_evolution_intake.yaml`
- `G:\BaiduSyncdisk\ResearchLoop\templates\self_evolution_contract.md`
- `G:\BaiduSyncdisk\ResearchLoop\tests\test_self_evolution_loop.py`

## Impact

- 对 research goal 的影响：把跨项目经验沉淀变成可重复、可检索、可验证的默认闭环。
- 对 project route 的影响：G 盘任务的 `自进化`、`沉淀`、`更新` 等关键词会触发 recall 和 intake，而不是只靠最终回复口头总结。
- 对 assumption 的影响：自动写回只能生成 `candidate` 或 `pending validation`，不能自动晋升最终状态。
- 对 system design 的影响：新增一键 self-evolution runner、模板、workflow 文档、Claude/Codex 触发桥接和 restart trace。

## Verification

- `python -m py_compile scripts\self_evolution_loop.py tests\test_self_evolution_loop.py`
- `$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'; python -m pytest tests\test_self_evolution_loop.py -q`
- Follow-up full harness validators are required after registry update.

## Follow-up

- Watch the first real G drive self-evolution runs for over-capture and tune
  trigger terms or intake fields if noisy candidates appear.
