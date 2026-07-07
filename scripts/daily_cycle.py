from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from _harness_common import ROOT, REPORTS_DIR, append_ledger, make_run_dir, now_iso, today, write_json, write_yaml


def run_step(name: str, argv: list[str], artifacts: Path) -> dict[str, Any]:
    completed = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
    (artifacts / f"{name}.stdout.txt").write_text(completed.stdout or "", encoding="utf-8")
    (artifacts / f"{name}.stderr.txt").write_text(completed.stderr or "", encoding="utf-8")
    return {
        "name": name,
        "argv": argv,
        "returncode": completed.returncode,
        "stdout_artifact": str(artifacts / f"{name}.stdout.txt"),
        "stderr_artifact": str(artifacts / f"{name}.stderr.txt"),
    }


def cycle(apply_safe: bool = False) -> dict[str, Any]:
    run_id, run_dir = make_run_dir("daily-cycle")
    artifacts = run_dir / "artifacts"
    py = sys.executable
    steps: list[tuple[str, list[str]]] = [
        ("registry_validate", [py, "scripts/registry_tool.py", "validate"]),
        ("evaluate", [py, "scripts/evaluator.py", "evaluate", "--target", "all", "--json"]),
        ("project_health", [py, "scripts/project_health.py", "report", "--json"]),
        ("proposal", [py, "scripts/evolve_proposals.py", "scan"] + (["--apply-safe"] if apply_safe else [])),
        ("kb_index_rebuild", [py, "scripts/kb_index.py", "rebuild"]),
        ("closeout_check", [py, "scripts/closeout_check.py"]),
        ("war_room", [py, "scripts/war_room.py", "--report"]),
    ]
    results = [run_step(name, argv, artifacts) for name, argv in steps]
    ok = all(step["returncode"] == 0 for step in results)
    result = {
        "schema": "research_harness_daily_cycle.v1",
        "run_id": run_id,
        "created_at": now_iso(),
        "ok": ok,
        "apply_safe": apply_safe,
        "steps": results,
    }
    write_json(artifacts / "daily_cycle.json", result)
    write_yaml(
        run_dir / "manifest.yaml",
        {
            "schema": "research_harness_daily_cycle_manifest.v1",
            "run_id": run_id,
            "created_at": result["created_at"],
            "apply_safe": apply_safe,
            "steps": [{"name": name, "argv": argv} for name, argv in steps],
            "outputs": [
                str(REPORTS_DIR / "daily" / f"{today()}_daily_cycle.md"),
                str(artifacts / "daily_cycle.json"),
            ],
        },
    )
    report_path = REPORTS_DIR / "daily" / f"{today()}_daily_cycle.md"
    report_path.write_text(markdown_report(result), encoding="utf-8")
    (run_dir / "closeout_report.md").write_text(markdown_report(result), encoding="utf-8")
    ledger = append_ledger(
        "daily_cycle",
        {
            "run_id": run_id,
            "ok": ok,
            "apply_safe": apply_safe,
            "report": str(report_path),
            "run_dir": str(run_dir),
            "failed_steps": [step["name"] for step in results if step["returncode"] != 0],
        },
    )
    result["report"] = str(report_path)
    result["run_dir"] = str(run_dir)
    result["ledger_path"] = ledger["ledger_path"]
    return result


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        f"# Daily Cycle {today()}",
        "",
        f"- run_id: `{result['run_id']}`",
        f"- ok: `{result['ok']}`",
        f"- apply_safe: `{result['apply_safe']}`",
        "",
        "## Steps",
        "",
    ]
    for step in result["steps"]:
        lines.append(f"- {step['name']}: returncode={step['returncode']}")
    lines.append("")
    return "\n".join(lines)


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the research harness daily quality cycle")
    parser.add_argument("--apply-safe", action="store_true")
    args = parser.parse_args()
    result = cycle(apply_safe=args.apply_safe)
    print_json(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
