# Experiment Plan

## Output Object Link

- output_id: paper_lifecycle_minimal_output
- claim_ids: C1
- target_figures: F1

## Experiment Question

- question: Does the validator accept a complete minimal project?
- hypothesis: yes, if all required files and YAML fields exist.
- expected_failure_mode: missing reproduction entry or claim fields.

## Data Lineage

- raw_data: no real raw data.
- intermediate_data: `results/minimal_points.csv`.
- result_data: `results/figure_v1.txt`.
- data_that_must_not_be_copied: real experimental data.

## Method

- code_entrypoints: `scripts/validate_research_project.py`.
- config_files: `workflows/paper_lifecycle/validation_rules.yaml`.
- parameters_from_yaml: required paths and fields.
- baselines: v0 placeholder.
- controls: v1 complete record.
- statistics: not applicable.
- uncertainty: structure-only dry-run.

## Reproduction

- environment: local Python with PyYAML already used by harness.
- minimal_command: `python scripts\validate_research_project.py --project-root examples\paper_lifecycle_minimal --json`
- expected_outputs: JSON with `ok: true`.
- smoke_test: command exits 0.

## Gate Checklist

- raw/intermediate/results traceable: yes.
- claim link recorded: yes.
- figure link recorded: yes.
- risk: dry-run only.
- next_action: run validator.
