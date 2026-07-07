# Mie-Pk-TV-S Limited-Angle 3D Reconstruction Paper Contract

```yaml
id: paper_mie_pk_tv_s_limited_angle_3d_reconstruction_example
title: Mie-Pk-TV-S limited-angle 3D reconstruction
source_project: sc-nmt
status: pending validation
target_journal: Experiments in Fluids or related optical diagnostics venue, human selection required
manuscript_root: G:\docs\小论文\paper_mie_pk_tv_s_limited_angle_3d_reconstruction_example
output_write_policy: paper_body_figures_and_submission_files_go_to_manuscript_root
core_claim: Mie-Pk-TV-S is a candidate workflow for relative 3D Mie scattering reconstruction under limited-angle views.
updated_at: 2026-07-01
```

## Core Claim

Mie-Pk-TV-S can be framed as a candidate limited-angle reconstruction workflow for relative equivalent Mie scattering intensity, provided the paper binds simulation or phantom checks, reprojection residuals, baseline comparisons, and finite-angle limitations before making performance claims.

## Target Journal

- Primary target: human-selected optical diagnostics or spray measurement journal.
- Backup target: reconstruction-methods or applied optics venue.
- Fit rationale: the paper should combine a measurement problem, finite-view reconstruction method, and evidence-driven validation story.
- Known style/format constraints: Figure 1-6 must carry the story without overstating absolute concentration or full-view equivalence.

## Write Targets

- Paper正文、图件、投稿文件默认写入：`G:\docs\小论文\paper_mie_pk_tv_s_limited_angle_3d_reconstruction_example`
- `ResearchLoop` 只保存本示例的 contract/card/registry/decision scaffold。
- 真实 SC-NMT 原始数据、大中间结果和可复现实验输出继续留在项目或数据目录，不进入 harness。

## Figure 1-6

| Figure | Working Title | Claim Role | Evidence Needed | Current Status |
|---|---|---|---|---|
| Figure 1 | View geometry and missing-angle map | Establish finite-view setup and boundary | Optical layout, view count, angle coverage | draft |
| Figure 2 | Mie-Pk-TV-S pipeline | Explain data-to-volume workflow | Inputs, priors, support mask, solver settings | draft |
| Figure 3 | Phantom or simulation validation | Test known ground truth behavior | Synthetic volume, noise/angle sweep, error metrics | missing |
| Figure 4 | Real spray reconstructed volume | Show scoped application | Real sequence, slices, isosurfaces, physical plausibility | missing |
| Figure 5 | Reprojection and baseline comparison | Support reconstruction credibility | Residuals, ART/SART or declared baseline | missing |
| Figure 6 | Uncertainty and failure cases | Prevent overclaiming | Sensitivity, failure examples, limitations | missing |

## Existing Evidence

| Evidence ID | Source Path | Claim/Figure | What It Supports | Verification |
|---|---|---|---|---|
| E0 | project evidence to be bound later | C1/F1-F6 | Historical project context only | pending validation |

## Missing Evidence

| Gap ID | Missing Evidence | Blocks Claim/Figure | Next Action |
|---|---|---|---|
| G1 | Phantom or simulation ground truth | C1/F3 | Create controlled validation pack |
| G2 | Reprojection residual audit | C1/F5 | Add command and residual report |
| G3 | Baseline comparison | C1/F5 | Select and run matched baseline |
| G4 | Finite-view sensitivity | C1/F6 | Sweep view count/angle/noise |

## Cannot Overclaim

- Absolute droplet concentration.
- Full-view tomography equivalence.
- Universal spray morphology recovery.
- Algorithm superiority without matched baselines.
- Paper-ready status before human review.

## Reviewer Risks

- Limited-angle ambiguity may explain apparent structure.
- TV regularization may sharpen artifacts.
- Mie scattering intensity is relative unless calibration supports stronger wording.
- Real spray validation without ground truth needs reprojection and plausibility checks.

## Closeout Links

- papers registry: `registry/papers.yaml`
- literature registry: `registry/literature.yaml`
- figures registry: `registry/figures.yaml`
- prompts registry: `registry/prompts.yaml`
- decisions registry: `registry/decisions.yaml`
