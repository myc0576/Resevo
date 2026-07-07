# SC-NMT Mie-Pk-CS-TV-T Paper Sprint manuscript-first route

```yaml
id: 20260706_sc_nmt_paper_sprint_template_manuscript_route
project_id: sc-nmt
date: 2026-07-06
status: pending validation
allowed_status:
  - validated
  - hypothesis
  - pending validation
changed_route_or_assumption: true
```

## Decision

SC-NMT `plan20260627.md` is upgraded from a long-horizon phase harness into a template-literature-driven, Paper Sprint, manuscript-first plan for the first Mie-Pk-CS-TV-T method paper. The primary template paper is Klinner & Willert 2022, Experiments in Fluids. The sprint fixes a six-main-figure manuscript structure, at least four supplement figures, a figure pool, figure contracts, source data manifest, claim boundary, originality review, reviewer checklist, and manuscript v0 outputs.

## Context

The user wants the first method paper to move toward a concrete draft without waiting for the entire Phase 0-8 research harness to finish. Existing old P-011 / Mie-Pk-TV-S results may still help as pilot cases, preliminary validation, or figure-pool candidates, but must not be represented as new narrowed-field data. Scientific claim boundaries remain conservative: all 3D outputs are relative equivalent Mie scattering intensity only.

## Alternatives Considered

- Keep the plan as a long-term Phase 0-8 harness only; rejected because it delays manuscript synthesis and figure selection.
- Let old P-011 / Mie-Pk-TV-S results directly drive the main paper; rejected because they are pilot/historical evidence, not new data.
- Expand the manuscript to all existing figure ideas; rejected because the sprint needs a fixed six-main-figure structure and a separate figure pool.

## Evidence

- Updated plan: `G:\projects\SC-NMT\plan20260627.md`.
- Sprint artifact names recorded: `manuscript_mie_pk_cs_tv_t_v0.md`, `manuscript_mie_pk_cs_tv_t_v0.docx`, `paper_figures_mie_pk_cs_tv_t_v0.pptx`, `figure_pool_index.yaml`, `originality_review.md`.
- This decision is route-level only; no manuscript, figure, calibration, reconstruction, or originality evidence was generated in this turn.

## Impact

- Research goal: Mie-Pk-CS-TV-T becomes the first method-paper main line.
- Project route: Paper Sprint can produce v0 manuscript and figures before the long Phase 0-8 evidence chain is fully complete.
- Assumptions: old P-011 / Mie-Pk-TV-S can contribute only as pilot case, supplement candidate, diagnostic draft, or discard candidate until human selection.
- System design: future agents must maintain figure contracts, source data, originality gate, claim boundary, and reviewer checklist before promoting sprint outputs.

## Follow-up

- Generate `originality_review.md` and `claim_boundary.md` first.
- Build `figure_pool_index.yaml` before PPT creation.
- Write figure legends and claim-to-figure matrix before prose sections.
- Keep manuscript body under `G:\docs\小论文\mie_pk_cs_tv_t_v0\` and evidence under `G:\projects\SC-NMT\outputs20260628\paper_sprints\mie_pk_cs_tv_t_v0\`.
