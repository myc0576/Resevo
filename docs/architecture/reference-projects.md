# Reference Projects and MycEvo Boundaries

This document records architectural borrowing boundaries. MycEvo does not copy
source code from these projects. It keeps a local-first, agent-agnostic scope:
an external agent performs research while MycEvo governs workflow memory,
evidence, provenance, validation, and candidate-first evolution.

## langchain-ai/openwiki

- **Borrowable capability:** A local CLI, filesystem-backed workspace, incremental
  update model, and agent-facing documentation surface. OpenWiki is useful as a
  reference for making a local knowledge surface easy to initialize and update.
- **MycEvo boundary:** OpenWiki manages what a codebase or project knows. MycEvo
  manages how a scientific task should be done next, including claim, evidence,
  artifact, decision, and validation gates. MycEvo does not become a generic
  code wiki or connector marketplace.
- **License and implementation risk:** The repository is MIT licensed. Its
  agent/API-key and code-wiki assumptions are product-specific; copying those
  integrations would add credentials, network, and scope coupling.
- **MycEvo implementation:** `mycevo init`, portable workspace paths, SQLite FTS
  retrieval, YAML registries, provenance records, and a thin stdio MCP layer.
- **Source:** <https://github.com/langchain-ai/openwiki>

## MemTensor/MemRL

- **Borrowable capability:** Explicit episodic memory records, retrieval stages,
  measurable reuse signals, and benchmark-oriented evaluation discipline.
- **MycEvo boundary:** MycEvo does not implement or claim reinforcement learning.
  Its utility metadata is deterministic and advisory; evidence status and human
  gates remain authoritative.
- **License and implementation risk:** The repository is MIT licensed. It is
  designed around general memory optimization and may expect model or embedding
  services; importing that runtime would violate MycEvo's local-first boundary.
- **MycEvo implementation:** `semantic_relevance`, `domain_fit`,
  `evidence_grade`, reuse counts, freshness, feedback, provenance, and
  `utility_score` are stored or derived in `mycevo.retrieval`.
- **Source:** <https://github.com/MemTensor/MemRL>

## aiming-lab/SimpleMem and EvolveMem

- **Borrowable capability:** The observe, evaluate, diagnose, propose, validate,
  and compare-with-champion lifecycle; explicit separation between memory
  capture and later evolution.
- **MycEvo boundary:** MycEvo evolves research workflows, not a universal memory
  service. It does not silently promote candidates and does not treat an LLM
  score as scientific validation.
- **License and implementation risk:** SimpleMem is MIT licensed. Its hybrid
  retrieval, multimodal memory, MCP/cloud options, and provider configuration
  are useful references but would introduce API keys, hosted state, and a larger
  runtime surface.
- **MycEvo implementation:** `mycevo.evolution.evaluate_guard` persists
  contract/state/trace/diff plus champion and candidate snapshots, requires a
  held-out pass and minimum improvement, and records rollback/next-bottleneck
  evidence. Human promotion remains separate.
- **Source:** <https://github.com/aiming-lab/SimpleMem>

## ai4s-research/open-science

- **Borrowable capability:** Local-first run artifacts, reproducibility records,
  model-agnostic provider boundaries, and an inspectable desktop workflow.
- **MycEvo boundary:** Open Science is an autonomous research application with
  an agent and integrations. MycEvo does not bundle an Agent, model, provider,
  or full scientific execution environment. Codex and Claude Code remain
  external callers.
- **License and implementation risk:** The repository is MIT licensed. Its beta
  desktop, provider, connector, and credential surfaces are broader than the
  small Python CLI/MCP engine and should not be vendored into MycEvo.
- **MycEvo implementation:** `run.json`, `trace.jsonl`,
  `artifact_manifest.json`, `decision_record.json`, environment summary,
  reproduction entry, and input/output hashes are emitted under workspace-local
  `.mycevo/runs/` without copying source artifacts.
- **Source:** <https://github.com/ai4s-research/open-science>

## nexu-io/open-design

- **Borrowable capability:** A product-shaped local CLI plus MCP installation
  workflow, agent adapters, `--print`/dry-run behavior, and official agent
  command delegation.
- **MycEvo boundary:** OpenDesign is a design workspace and skill system.
  MycEvo does not copy its templates, skills, UI, or agent-specific product
  behavior; it only adopts the safe adapter principle.
- **License and implementation risk:** The core repository is Apache-2.0, while
  bundled skills/templates can carry their own licenses. Adapter commands and
  configuration formats can change, so MycEvo must prefer official `mcp add`,
  `mcp get`, and `mcp remove` commands and print a snippet when uncertain.
- **MycEvo implementation:** `mycevo mcp install|status|uninstall codex|claude`
  is idempotent, supports dry-run/print, records only preflight metadata, and
  delegates to the installed agent CLI. The MCP server itself stays a thin
  adapter over the shared service layer.
- **Source:** <https://github.com/nexu-io/open-design>

## Differentiation Summary

| Project | Primary object | MycEvo difference |
|---|---|---|
| OpenWiki | What a project knows | How a research task should be done next |
| MemRL / SimpleMem / EvolveMem | General memory and retrieval optimization | Claim-evidence-artifact workflow evolution with gates |
| Open Science Desktop | Autonomous local research application | External-agent governance and memory layer only |
| OpenDesign | Design workspace plus agent integrations | Research provenance, validation, and candidate-first promotion |
| MycEvo | Evidence-governed research workflow harness | CLI + stdio MCP external brain for Codex/Claude Code |

