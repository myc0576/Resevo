# ResearchLoop MCP

本目录提供本地 stdio MCP 服务，用于让 Agent 直接访问 `G:\BaiduSyncdisk\ResearchLoop` 的检索、健康状态和反馈记录。

## Tools

- `search_kb(query, limit)`：查询 SQLite FTS5 知识索引。
- `read_kb_doc(path)`：读取白名单内文档。
- `get_closeout_health()`：读取最新 closeout health。
- `get_project_health(project_id?)`：读取项目级体检。
- `list_proposals(status?)`：列出 evolution proposals。
- `record_feedback(target_id, feedback_type, note)`：唯一写接口，只写 `registry\feedback.yaml` 并追加 ledger。

Self-evolution 的写入入口不是 MCP，而是可审计 CLI：

```powershell
python G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py recall --query "<task>" --project-root <cwd> --json
python G:\BaiduSyncdisk\ResearchLoop\scripts\self_evolution_loop.py run --intake <intake.yaml> --apply-candidates --json
```

MCP 继续负责检索和健康状态读取；候选写回必须通过 CLI 留下 `contract.yaml`、`state.json` 和 `trace.jsonl`。

## Boundary

- 不依赖 OpenViking。
- 不需要网络。
- 不提供任意文件写入。
- 不写入 `G:\knowledge\_harness`。
- 不通过 MCP 自动提升 `candidate` / `pending validation` 为 `validated` 或 `reusable`。

## Self Test

```powershell
python G:\BaiduSyncdisk\ResearchLoop\mcp\research_harness_mcp.py --self-test
```
