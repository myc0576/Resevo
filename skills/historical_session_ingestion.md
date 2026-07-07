# Historical Session Ingestion

## Purpose

将历史 Codex 会话沉淀为 ResearchLoop 可追踪资产，而不是普通聊天摘要。

该 skill 适用于 SC-NMT 或其他 G 盘科研项目的历史会话复盘。输出应进入 canonical harness：`G:\BaiduSyncdisk\ResearchLoop`，以及长期知识入口：`G:\knowledge\reusable_knowledge` 和 `G:\knowledge\reusable_prompts`。

## Procedure

1. 读取 `harness.yaml` 和 `AGENTS.md`。
2. 扫描 `C:\Users\Administrator\.codex\sessions\**\rollout-*.jsonl`。
3. 用 `session_meta.cwd`、路径、关键词和用户目标识别目标项目会话。
4. 生成 machine-readable inventory 和 human-readable inventory。
5. 按主题聚类。
6. 提取 reusable knowledge。
7. 提取 reusable prompts。
8. 将原始素材清单写入项目内 `research_assets`。
9. 生成或更新 decision records。
10. 更新 registry，并运行 validator、index rebuild 和 closeout_check。

## Quality Gates

- 不复制原始实验大数据到 knowledge。
- 不复制完整 JSONL 到 knowledge。
- 未验证科学结论必须标记为 `hypothesis` 或 `pending validation`。
- 只把可复用流程、参数、边界、风险和验证依据写入知识卡。
- 所有 registry 和 markdown 使用 UTF-8。

## Outputs

- `session_inventory.json`
- `session_inventory.md`
- `theme_summary.md`
- `00_asset_manifest.md`
- `reproduction_entry.md`
- reusable knowledge cards
- reusable prompt cards
- registry updates
- closeout health report
