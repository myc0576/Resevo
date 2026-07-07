# 20260627 SC-NMT full-frame rectangular scatter masking gate

```yaml
id: 20260627_sc_nmt_fullframe_scattermasking_gate
date: 2026-06-27
project_id: sc-nmt
status: validated
changed_route_or_assumption: true
```

## Decision

For the 20260624 Mie sequences, the user-confirmed red-box region in the full-frame P-018 pseudocolor image is treated as a fixed invalid-observation scatter region across all listed groups before Phase 1.7 temporal quality control.

The processed sequence is stored as derived `uint16` TIFF files under:

```text
G:\data\experiments\2026\20260624mie_scattermasking
```

The original TIFF root remains read-only:

```text
G:\data\experiments\2026\20260624mie
```

## Rationale

- The bottom red-box band was human-identified as unwanted scatter or reflection in the full composite frame.
- The user explicitly requested the same location be removed for all groups.
- The target for downstream work should be a derived TIFF sequence rather than a modified raw-data root.
- Prior split-view annotation artifacts are now intermediate process material and were moved into the SC-NMT project `outputs\runs` area.

## Constraints

- Do not copy raw experimental TIFFs into knowledge or harness.
- Do not claim the fill is physical zero signal.
- Do not claim downstream reconstruction improvement until Phase 1.7 and later checks validate it.
- P-014 has 240 frames in this root; the other processed groups have 120 frames.

## Verification

- `1440` derived TIFF files were written.
- Output shape and dtype were sampled as `1024x1024 uint16`.
- P-018 frame 61 sampled check: red-box outside pixels remained identical; red-box 99.5 percentile dropped from `34160` to `1224`.
- Existing code checks passed: `19 passed` for manual mask/inpaint/scatter-mask tests; `compileall` passed.

