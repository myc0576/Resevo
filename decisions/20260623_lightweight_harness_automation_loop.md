# Decision: 建立轻量 ResearchLoop 自动化闭环

date: 2026-06-23
project_id: g-workspace
status: validated
changed_route_or_assumption: true

## Decision

将 `G:\BaiduSyncdisk\ResearchLoop` 从纯 Markdown 协议型 harness 升级为轻量自动化闭环 harness。

第一阶段采用 Python CLI、YAML registry validator、SQLite FTS5、本地 runs 记录和 evolution ledger；不复制 QuantKB 的复杂自动进化系统，不引入第三方依赖，不移动旧项目，不删除旧文件。

## Rationale

用户报告中指出当前最大问题是 closeout 开环、知识不可检索、registry 手工维护、项目桥接不稳定，以及 `G:\knowledge\_harness` 与 canonical harness path 混淆。

轻量 CLI 能先解决“可发现、可验证、可检索、可追踪”的底层问题，同时保持科研资产边界清楚：知识和 prompt 写入 `G:\knowledge`，harness 规则、registry、runs、reports 写入 `G:\BaiduSyncdisk\ResearchLoop`，原始 research assets 留在项目内。

## Rejected

- 直接复制 QuantKB 全套自动化系统：复杂度过高，第一阶段会遮蔽路径治理和 registry 质量问题。
- 立即引入 FastMCP / 向量检索：会增加依赖和维护面；第一阶段 SQLite FTS5 足够支撑关键词检索。
- 自动 apply 自我进化 proposal：风险过高，先保留 proposal-only。

## Verification

- registry validator 可解析并检查所有 registry。
- kb index 可 rebuild 和 search。
- project bridge 可扫描并桥接第一批项目。
- closeout check 可生成 health report、state JSON、runs 和 evolution ledger。
