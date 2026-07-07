# Decision: Canonical Harness Path Resolution

## Date

2026-06-23

## Project

g-workspace

## Decision

In the `G:\` workspace, the word `harness` resolves to `G:\BaiduSyncdisk\ResearchLoop` for all write operations.

## Rationale

Older memory and previous knowledge workflows referenced `_harness` under knowledge directories. This made the phrase “沉淀到 harness” ambiguous in other projects. The current long-term English harness is intentionally located under `G:\BaiduSyncdisk\ResearchLoop` so Codex, Git, and scripts can use stable English directory names.

## Explicit Non-Targets

- `G:\knowledge\_harness` is deprecated/ambiguous and must not be used as a write target.
- `G:\知识库\_harness` is read-only legacy reference only.

## Consequences

- Root `G:\AGENTS.md` now states the path-resolution rule.
- `G:\BaiduSyncdisk\ResearchLoop\AGENTS.md` now contains a canonical harness path section.
- `harness.yaml` now records canonical, legacy, deprecated, and forbidden write roots.
- Future closeout should write harness registries/decisions/reports to `G:\BaiduSyncdisk\ResearchLoop`, knowledge cards to `G:\knowledge\reusable_knowledge`, and prompt cards to `G:\knowledge\reusable_prompts`.

## Status

validated
