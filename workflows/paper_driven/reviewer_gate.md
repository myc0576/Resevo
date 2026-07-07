# Reviewer Gate Workflow

Use this gate before upgrading claims, submitting a paper draft, writing a response letter, or converting experimental output into reusable knowledge.

## Required Checks

1. Claim wording
   - Does each claim match the evidence strength?
   - Are relative and absolute quantities separated?
   - Are reconstruction and optical-diagnostic assumptions separated?
2. Evidence linkage
   - Is each claim linked to an evidence table row?
   - Is each paper figure linked to data, code, and reproduction command?
   - Are missing experiments visible rather than hidden in prose?
3. Baselines and uncertainty
   - Is there a baseline comparison where a reviewer would expect one?
   - Are residuals, error metrics, or plausibility checks recorded?
   - Are failure cases and finite-angle limitations shown?
4. Figure integrity
   - Does every figure serve a claim?
   - Are colorbars, units, axes, scale bars, and captions complete where needed?
   - Are style references separated from scientific evidence?
5. Boundary language
   - Are unsupported novelty, universality, and absolute-quantity claims removed?
   - Are limitations near the claims they constrain?

## Mie-Pk-TV-S Boundary Checks

Do not claim:

- absolute droplet concentration without calibration evidence;
- full-view tomography performance from limited-angle evidence alone;
- universal spray morphology recovery from one setup;
- algorithm superiority without matched baselines;
- denoising or regularization benefits without residual, robustness, or phantom checks.

Allowed conservative phrasing examples:

- "relative equivalent Mie scattering intensity";
- "limited-angle reconstruction under the tested view geometry";
- "candidate evidence pending additional phantom and baseline validation";
- "reprojection-consistent within the reported residual range".
