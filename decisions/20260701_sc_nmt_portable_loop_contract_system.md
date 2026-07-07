# SC-NMT Portable Loop Contract System

## Decision

SC-NMT loop governance uses a portable project-local contract system as the source of truth. Markdown contracts, JSON/JSONL runtime files, stdlib Python validators, and pytest coverage live inside `G:\projects\SC-NMT`; Codex, OMX, or other agent runtimes are only invocation layers.

## Rationale

The loop system must survive context loss, runtime changes, and partial agent restarts. Binding the contract to a single orchestration runtime would make the scientific workflow fragile. The project therefore keeps restart state on disk and requires every loop run to be understandable from:

- `G:\projects\SC-NMT\docs\loop\contract.md`
- `G:\projects\SC-NMT\STATE.md`
- `G:\projects\SC-NMT\loop-run-log.md`

## Boundaries

- The loop may validate infrastructure and current artifact pointers.
- The loop may produce `pass|warning|block` reports and scorecards.
- The loop must not write scientific approval.
- `current_gate: pass`, `approved=true`, `paper_ready=true`, `source_status=calibrated`, and `final_evidence=true` require explicit human-gate artifacts.
- `outputs20260628` remains the active output root; old `outputs\` remains historical.

## Evidence

- `G:\projects\SC-NMT\tests\test_loop_contract_system.py`
- `G:\projects\SC-NMT\scripts\sc_nmt_loop.py`
- `G:\projects\SC-NMT\outputs20260628\loop\phase2_20260701_loop1\verifier_report.md`
- `G:\projects\SC-NMT\outputs20260628\loop\phase2_20260701_loop1\scorecard.json`
- `G:\projects\SC-NMT\research_assets\20260701_sc_nmt_loop_system_optimization\00_asset_manifest.md`

## Verification

2026-07-01 verification:

- `$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'; python -m pytest tests\test_loop_contract_system.py tests\test_phase2_3_reacquired_checkerboard_calibration.py -q`: 8 passed.
- `python -m compileall -q sc_nmt scripts tests`: passed.
- `python scripts\sc_nmt_loop.py validate --state STATE.md --contract docs\loop\contract.md --output outputs20260628\loop\phase2_20260701_loop1\verifier_report.md`: pass.
- `python scripts\sc_nmt_loop.py phase-verifier --phase phase2_3 --run-id phase2_20260701_loop1 --dry-run`: pass against `STATE.md` latest artifacts.

## Rejected Alternatives

- Put loop state only in chat/context: rejected because context compaction and session loss would break restartability.
- Bind loop execution to OMX runtime state: rejected because SC-NMT needs portable project-local contracts.
- Let scorecards auto-open gates: rejected because subjective scoring is diagnostic, not human approval.
