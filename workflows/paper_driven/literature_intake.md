# Literature Intake Workflow

Use this workflow whenever a paper, review, dataset article, thesis, or methods note influences a claim, figure, baseline, or reviewer response.

## Rules

- Do not copy literature PDF originals into `G:\knowledge\reusable_knowledge`.
- Keep PDF originals in the user's source library, project-local reading folder, or citation manager.
- Write one `templates/literature_card.md` per source that is actually used.
- Record evidence use, citation location, claim linkage, and uncertainty.
- Preserve contradictions and limitations instead of turning every source into support.

## Intake Steps

1. Identify the source.
   - Citation key.
   - Full citation.
   - Local PDF/source location, if allowed to reference.
   - DOI, URL, or library handle.
2. Extract the paper-level role.
   - Target-paper exemplar.
   - Method baseline.
   - Validation metric source.
   - Figure-style reference.
   - Claim boundary or limitation source.
3. Create a literature card.
   - Summary in your own words.
   - Evidence use in the current paper.
   - Exact citation locations such as `Introduction paragraph 2`, `Methods baseline`, or `Reviewer response`.
4. Register the card in `registry/literature.yaml`.
5. If a figure is saved from the source, also run `figure_intake.md`.

## Domain Lens

For 3D LIF/MIE and limited-angle spray tomography, literature cards should separate:

- optical-diagnostic evidence from reconstruction-algorithm evidence;
- relative intensity claims from absolute concentration claims;
- simulated or phantom validation from real spray validation;
- full-view tomography assumptions from finite-view or limited-angle assumptions.
