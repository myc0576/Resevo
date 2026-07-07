# Decision: SC-NMT 历史会话采用分组资产化沉淀

date: 2026-06-23
project_id: sc-nmt
status: validated
changed_route_or_assumption: true

## Decision

SC-NMT 历史 Codex 会话采用 inventory、主题聚类和按类别知识卡沉淀的方式处理。

具体做法是：先建立 `session_inventory` 和 `theme_summary`，再分别生成 reusable knowledge、reusable prompts、project research_assets 和 decision records，最后更新 ResearchLoop registry。

## Rationale

一次性把 72 个 SC-NMT 相关历史会话压缩成普通摘要，会丢失可复用的过程资产、验证边界和触发条件。

分组资产化能够保留：

- 哪些会话服务于 calibration/projection、scatter/alignment、reconstruction、PPT、paper claim boundary 或 harness/memory。
- 哪些内容是可复用 workflow。
- 哪些内容只是 historical evidence，必须保留为 `pending validation`。
- 哪些素材应该留在项目 `research_assets`，而不是复制到 knowledge。

## Rejected

- 将所有 JSONL 全量复制进 knowledge：体积大、噪声高，且容易污染可复用知识。
- 将每个会话都写成单独知识卡：维护成本过高，检索质量差。
- 将历史对话里的科学判断直接提升为 validated：缺少 artifact、metric、figure 和 reproduction evidence。

## Closeout Effect

- research goal：服务于 SC-NMT 长期科研记忆、可复用工作流和论文证据治理。
- project route：从 prose summary 转为 registry-backed assetization。
- system design：新增 historical session ingestion skill、prompt card 和 research asset manifest。

## Verification

- 扫描 551 个 session 文件。
- 识别 72 个 SC-NMT 相关会话。
- 生成 `session_inventory.json`、`session_inventory.md` 和 `theme_summary.md`。
- 更新 knowledge、prompts、research_assets 和 decisions registry。
