# Small Paper Manuscript Write Root

```yaml
id: 20260701_small_paper_docs_write_root
project_id: researchloop
date: 2026-07-01
status: validated
changed_route_or_assumption: true
```

## Decision

Any small-paper正文、图件、投稿文件 default to `G:\docs\小论文\<paper_id>`.

ResearchLoop only stores templates, workflows, indexes, registry cards, and decision records for paper work.

## Rationale

Paper workflows need a clean separation between governance assets and actual manuscript/submission files. The harness should make paper work traceable, but it should not become the storage location for manuscript drafts, final figures, cover letters, response letters, submission packages, or journal files.

## Alternatives Considered

| Alternative | Why Rejected Or Deferred |
|---|---|
| Store paper正文 and figures under `ResearchLoop/examples` | Examples are scaffolds and validators, not live manuscript directories; the path text is local-directory compatibility, not the public brand. |
| Store paper files in each project repo | Project repos may hold evidence and code, but paper submission files need a stable docs root. |
| Store paper files in reusable knowledge | Rejected because manuscript/submission files are not reusable knowledge cards. |

## Verification

- Files: `harness.yaml`, `README.md`, `templates/paper_contract.md`, `workflows/paper_driven/*.md`, `registry/papers.yaml`.
- Commands: `python scripts\registry_tool.py validate`, `python scripts\evaluator.py evaluate --target all --json`, `python scripts\closeout_check.py`.

## Consequences

- Paper contracts must name `manuscript_root`.
- Paper registry entries must record `manuscript_root` and `output_write_policy`.
- Final paper figures are not stored in `visual_refs/`; that folder remains an indexed visual-reference area.
- ResearchLoop remains a governance and indexing layer, not a manuscript workspace.

## Follow-up

- If a paper project becomes active, create `G:\docs\小论文\<paper_id>` there before drafting正文 or submission files.
