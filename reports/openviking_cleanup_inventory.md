# OpenViking Cleanup Inventory

## Status

- created_at: 2026-06-23
- action: inventory only
- deletion: none

## Decision

ResearchLoop 第一版检索入口采用 SQLite FTS5：

```text
G:\BaiduSyncdisk\ResearchLoop\state\kb_index\research_kb.sqlite
```

OpenViking 不再作为 `G:\knowledge` 的 canonical 检索描述。旧 OpenViking 相关内容只作为 legacy/optional reference，不删除、不移动。

## Current Known References

- `G:\AGENTS.md` 旧描述曾把 `G:\knowledge` 称为 OpenViking 知识库。
- Codex historical memory 中仍存在 OpenViking / `_harness` 相关旧描述，执行当前工作区任务时应以 `G:\BaiduSyncdisk\ResearchLoop\AGENTS.md` 和 `harness.yaml` 为准。

## Cleanup Policy

- 不创建 `G:\knowledge\_harness`。
- 不删除 `G:\知识库\_harness` 或历史 OpenViking 资料。
- 后续如需真实清理，先新增逐项清理清单和回滚策略。
