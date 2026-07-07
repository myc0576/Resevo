from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from _harness_common import ROOT, STATE_DIR, append_ledger, make_run_dir, now_iso, write_json, write_yaml


def latest_quality_result() -> dict[str, Any]:
    path = STATE_DIR / "evaluation.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "ok": data.get("ok"),
        "average_score": data.get("average_score"),
        "hard_failure_count": data.get("hard_failure_count"),
        "quality_counts": data.get("quality_counts"),
        "source": str(path),
    }


def capture(
    label: str,
    argv: list[str],
    timeout: int,
    project_id: str = "",
    decision_id: str = "",
    outcome: str = "partial",
    notes: str = "",
) -> dict[str, Any]:
    run_id, run_dir = make_run_dir(label)
    manifest = {
        "schema": "research_harness_run_manifest.v1",
        "run_id": run_id,
        "label": label,
        "created_at": now_iso(),
        "cwd": str(ROOT),
        "argv": argv,
        "timeout_seconds": timeout,
        "project_id": project_id,
        "decision_id": decision_id,
        "decision": {"id": decision_id, "notes": notes},
        "outcome": {"status": outcome, "notes": notes},
        "artifacts": [],
        "quality_result": latest_quality_result(),
    }
    write_yaml(run_dir / "manifest.yaml", manifest)
    started_at = now_iso()
    try:
        completed = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        result = {
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        result = {
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or f"command timed out after {timeout}s",
            "timed_out": True,
        }
    finished_at = now_iso()
    artifacts = run_dir / "artifacts"
    stdout_path = artifacts / "stdout.txt"
    stderr_path = artifacts / "stderr.txt"
    meta_path = artifacts / "command.meta.json"
    stdout_path.write_text(result["stdout"] or "", encoding="utf-8")
    stderr_path.write_text(result["stderr"] or "", encoding="utf-8")
    meta = {"started_at": started_at, "finished_at": finished_at, **{k: v for k, v in result.items() if k not in {"stdout", "stderr"}}}
    write_json(meta_path, meta)
    manifest["artifacts"] = [str(stdout_path), str(stderr_path), str(meta_path)]
    manifest["quality_result"] = latest_quality_result()
    write_yaml(run_dir / "manifest.yaml", manifest)
    report = [
        f"# Run Capture: {label}",
        "",
        f"- run_id: `{run_id}`",
        f"- project_id: `{project_id or 'none'}`",
        f"- decision_id: `{decision_id or 'none'}`",
        f"- outcome: `{outcome}`",
        f"- argv: `{argv}`",
        f"- returncode: `{result['returncode']}`",
        f"- timed_out: `{result['timed_out']}`",
        f"- notes: {notes or 'none'}",
        "",
        "## Artifacts",
        "",
        "- `artifacts/stdout.txt`",
        "- `artifacts/stderr.txt`",
        "- `artifacts/command.meta.json`",
        "",
    ]
    (run_dir / "closeout_report.md").write_text("\n".join(report), encoding="utf-8")
    ledger = append_ledger(
        "run_capture",
        {
            "run_id": run_id,
            "label": label,
            "project_id": project_id,
            "decision_id": decision_id,
            "outcome": outcome,
            "notes": notes,
            "argv": argv,
            "returncode": result["returncode"],
            "timed_out": result["timed_out"],
            "run_dir": str(run_dir),
            "quality_result": manifest["quality_result"],
        },
    )
    return {"run_id": run_id, "run_dir": str(run_dir), "ledger_path": ledger["ledger_path"], **meta}


def print_json(data: dict[str, Any]) -> None:
    import json

    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a ResearchLoop maintenance run")
    parser.add_argument("--label", default="harness-command")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--project-id", default="")
    parser.add_argument("--decision-id", default="")
    parser.add_argument("--outcome", choices=["success", "partial", "fail"], default="partial")
    parser.add_argument("--notes", default="")
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv
    if argv and argv[0] == "--":
        argv = argv[1:]
    if not argv:
        raise SystemExit("missing command after --")
    result = capture(
        args.label,
        argv,
        args.timeout,
        project_id=args.project_id,
        decision_id=args.decision_id,
        outcome=args.outcome,
        notes=args.notes,
    )
    print_json(result)
    return 0 if result.get("returncode") == 0 else int(result.get("returncode") or 1)


if __name__ == "__main__":
    raise SystemExit(main())
