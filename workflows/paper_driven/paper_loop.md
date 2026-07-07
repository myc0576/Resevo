# Paper Loop Workflow

This layer is a paper-driven operating loop for 3D LIF/MIE, spray optical tomography, and limited-angle 3D reconstruction work. It complements `workflows/paper_lifecycle/` by making paper contracts, literature cards, visual references, reviewer gates, and task closeout explicit.

## Loop

1. Start with `templates/paper_contract.md`.
   - Define the core claim.
   - Select the target journal or venue class.
   - Set the paper write root to `G:\docs\小论文\<paper_id>`.
   - Draft Figure 1-6 before treating experiments as complete.
   - List existing evidence, missing evidence, and boundaries that must not be overstated.
2. Run `literature_intake.md`.
   - Keep PDF originals outside `G:\knowledge\reusable_knowledge`.
   - Save only cards, summaries, evidence uses, and citation locations.
3. Run `figure_intake.md`.
   - Save useful paper figures, visual styles, and example layouts under `visual_refs/`.
   - Every saved visual reference must have a matching figure card.
4. Execute experiment and reconstruction work.
   - Keep raw data and large intermediate outputs in the project tree.
   - Bind evidence to claims through `templates/evidence_table.md`.
5. Run `experiment_closeout.md` at the end of every research task.
   - Decide whether the task produced reusable knowledge, reusable prompts, research assets, or decision records.
6. Run `reviewer_gate.md` before writing strong paper language.
   - Claims may advance only when evidence level, baselines, residuals, and limitations match the wording.

## Hard Write Rule

- Small-paper正文、图件、投稿文件默认写入 `G:\docs\小论文\<paper_id>`。
- ResearchLoop only stores templates, workflows, indexes, registry cards, and decision records for paper work.
- Do not place manuscript drafts, final figures, cover letters, response letters, journal submission files, or paper build outputs inside `G:\BaiduSyncdisk\ResearchLoop`.
- Visual references may live under `visual_refs/` only as indexed references with figure cards; they are not the paper figure output directory.

## Status Vocabulary

- `draft`: structure exists but evidence is not bound.
- `pending validation`: evidence is planned or partially observed.
- `hypothesis`: plausible but not yet demonstrated.
- `supported`: evidence exists for the scoped claim.
- `blocked`: a missing data, method, or review dependency prevents progress.

Do not use `approved`, `pass`, or `paper_ready` as automatic machine outputs. Those remain human-controlled decisions.

## Mie-Pk-TV-S Example Route

For a limited-angle 3D reconstruction paper:

1. Create a paper contract with the conservative claim: Mie-Pk-TV-S is a candidate workflow for reconstructing relative 3D Mie scattering intensity under limited-angle views, pending simulation, reprojection, and baseline evidence.
2. Intake target literature on limited-angle tomography, spray diagnostics, Mie/LIF calibration, TV regularization, and validation metrics as literature cards.
3. Draft Figure 1-6:
   - Figure 1: optical layout, view geometry, and limited-angle missing cone.
   - Figure 2: reconstruction pipeline from calibrated images to support mask, priors, and volume.
   - Figure 3: simulation or phantom validation with known ground truth.
   - Figure 4: real spray reconstruction with orthogonal slices and isosurfaces.
   - Figure 5: reprojection residuals and baseline comparison against ART/SART or related methods.
   - Figure 6: uncertainty, failure cases, and angle/count sensitivity.
4. Close each experiment with an evidence table row that links claim, data, command, figure, metric, and limitation.
5. At reviewer gate, forbid unsupported claims about absolute concentration, full-view equivalence, universal denoising, or morphology accuracy beyond the measured resolution and angular coverage.
