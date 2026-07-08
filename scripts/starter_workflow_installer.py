from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).absolute().parents[1]

WORKFLOWS: dict[str, dict[str, Any]] = {
    "nature-skills": {
        "registry_id": "yuan1z0825_nature_skills",
        "title": "Nature Skills",
        "upstream_url": "https://github.com/Yuan1z0825/nature-skills.git",
        "pinned_ref": "8990143c3835f899e5331286a6a3b3393a2926ef",
        "local_path": Path("external") / "nature-skills",
    }
}

SUPPRESS_PROMPT_DECISIONS = {"skipped", "dismissed"}
MARK_DECISIONS = {"skipped", "dismissed"}


@dataclass(frozen=True)
class GitCommandResult:
    args: list[str]
    cwd: str
    returncode: int
    stdout: str
    stderr: str


GitRunner = Callable[[list[str], Path | None], GitCommandResult]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def state_path() -> Path:
    return ROOT / "state" / "starter_workflows.json"


def workflow(workflow_id: str) -> dict[str, Any]:
    if workflow_id not in WORKFLOWS:
        raise ValueError(f"unknown_workflow:{workflow_id}")
    return WORKFLOWS[workflow_id]


def workflow_path(config: dict[str, Any]) -> Path:
    return ROOT / Path(config["local_path"])


def read_state() -> dict[str, Any]:
    path = state_path()
    if not path.exists():
        return {"version": 1, "starter_workflows": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "starter_workflows": {}, "warnings": ["state_json_invalid"]}
    if not isinstance(data, dict):
        return {"version": 1, "starter_workflows": {}, "warnings": ["state_not_object"]}
    data.setdefault("version", 1)
    data.setdefault("starter_workflows", {})
    return data


def write_state(data: dict[str, Any]) -> None:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_git(args: list[str], cwd: Path | None = None) -> GitCommandResult:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    return GitCommandResult(args=args, cwd=str(cwd or ""), returncode=completed.returncode, stdout=completed.stdout, stderr=completed.stderr)


def is_git_checkout(path: Path) -> bool:
    return path.exists() and (path / ".git").exists()


def current_ref(path: Path, runner: GitRunner = run_git) -> str:
    if not is_git_checkout(path):
        return ""
    result = runner(["rev-parse", "HEAD"], path)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def dirty_status(path: Path, runner: GitRunner = run_git) -> str:
    if not is_git_checkout(path):
        return ""
    result = runner(["status", "--short"], path)
    if result.returncode != 0:
        return "git_status_failed"
    return result.stdout.strip()


def command_record(args: list[str], cwd: Path | None = None) -> dict[str, str]:
    return {"command": "git " + " ".join(args), "cwd": str(cwd or "")}


def status(workflow_id: str, runner: GitRunner = run_git) -> dict[str, Any]:
    config = workflow(workflow_id)
    path = workflow_path(config)
    state = read_state()
    entry = dict(state.get("starter_workflows", {}).get(workflow_id, {}))
    decision = str(entry.get("decision") or "")
    blocked_reason = ""
    installed = False
    ref = ""

    if path.exists() and not is_git_checkout(path):
        blocked_reason = "local_path_exists_not_git"
    else:
        ref = current_ref(path, runner)
        installed = bool(ref)

    needs_prompt = not installed and not blocked_reason and decision not in SUPPRESS_PROMPT_DECISIONS
    return {
        "ok": not blocked_reason,
        "id": workflow_id,
        "registry_id": config["registry_id"],
        "title": config["title"],
        "upstream_url": config["upstream_url"],
        "pinned_ref": config["pinned_ref"],
        "local_path": str(path),
        "state_path": str(state_path()),
        "installed": installed,
        "current_ref": ref,
        "decision": decision,
        "needs_prompt": needs_prompt,
        "blocked_reason": blocked_reason,
    }


def mark(workflow_id: str, decision: str) -> dict[str, Any]:
    workflow(workflow_id)
    if decision not in MARK_DECISIONS:
        return {"ok": False, "id": workflow_id, "error": f"invalid_decision:{decision}"}
    state = read_state()
    workflows = state.setdefault("starter_workflows", {})
    workflows[workflow_id] = {
        "decision": decision,
        "decided_at": now_iso(),
        "local_path": str(workflow_path(workflow(workflow_id))),
        "pinned_ref": workflow(workflow_id)["pinned_ref"],
    }
    write_state(state)
    result = status(workflow_id)
    result["marked"] = decision
    return result


def run_step(args: list[str], cwd: Path | None, runner: GitRunner, executed: list[dict[str, str]]) -> GitCommandResult:
    executed.append(command_record(args, cwd))
    return runner(args, cwd)


def install(workflow_id: str, runner: GitRunner = run_git, dry_run: bool = False) -> dict[str, Any]:
    config = workflow(workflow_id)
    path = workflow_path(config)
    planned: list[dict[str, str]] = []
    executed: list[dict[str, str]] = []

    clone_args = ["clone", "--no-checkout", config["upstream_url"], str(path)]
    checkout_args = ["checkout", config["pinned_ref"]]

    if not path.exists():
        planned.extend([command_record(clone_args, ROOT), command_record(checkout_args, path)])
    elif not is_git_checkout(path):
        return {
            "ok": False,
            "id": workflow_id,
            "local_path": str(path),
            "blocked_reason": "local_path_exists_not_git",
        }
    else:
        dirty = dirty_status(path, runner)
        if dirty:
            return {
                "ok": False,
                "id": workflow_id,
                "local_path": str(path),
                "blocked_reason": "existing_clone_dirty",
                "dirty_status": dirty,
            }
        fetch_args = ["fetch", "origin"]
        planned.extend([command_record(fetch_args, path), command_record(checkout_args, path)])

    if dry_run:
        return {
            "ok": True,
            "id": workflow_id,
            "local_path": str(path),
            "pinned_ref": config["pinned_ref"],
            "dry_run": True,
            "planned_commands": planned,
        }

    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        clone = run_step(clone_args, ROOT, runner, executed)
        if clone.returncode != 0:
            return {
                "ok": False,
                "id": workflow_id,
                "local_path": str(path),
                "blocked_reason": "git_clone_failed",
                "stderr": clone.stderr,
                "executed_commands": executed,
            }
    else:
        fetch = run_step(["fetch", "origin"], path, runner, executed)
        if fetch.returncode != 0:
            return {
                "ok": False,
                "id": workflow_id,
                "local_path": str(path),
                "blocked_reason": "git_fetch_failed",
                "stderr": fetch.stderr,
                "executed_commands": executed,
            }

    checkout = run_step(checkout_args, path, runner, executed)
    if checkout.returncode != 0:
        return {
            "ok": False,
            "id": workflow_id,
            "local_path": str(path),
            "blocked_reason": "git_checkout_failed",
            "stderr": checkout.stderr,
            "executed_commands": executed,
        }

    state = read_state()
    state.setdefault("starter_workflows", {})[workflow_id] = {
        "decision": "installed",
        "installed_at": now_iso(),
        "local_path": str(path),
        "pinned_ref": config["pinned_ref"],
    }
    write_state(state)

    result = status(workflow_id, runner)
    result["installed_now"] = True
    result["executed_commands"] = executed
    return result


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"ok: {result.get('ok')}")
    for key in ("id", "local_path", "installed", "needs_prompt", "blocked_reason"):
        if key in result:
            print(f"{key}: {result[key]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install optional ResearchLoop starter workflows")
    sub = parser.add_subparsers(dest="command", required=True)

    status_parser = sub.add_parser("status")
    status_parser.add_argument("--id", required=True)
    status_parser.add_argument("--json", action="store_true")

    install_parser = sub.add_parser("install")
    install_parser.add_argument("--id", required=True)
    install_parser.add_argument("--json", action="store_true")
    install_parser.add_argument("--dry-run", action="store_true")

    mark_parser = sub.add_parser("mark")
    mark_parser.add_argument("--id", required=True)
    mark_parser.add_argument("--decision", required=True, choices=sorted(MARK_DECISIONS))
    mark_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()
    try:
        if args.command == "status":
            result = status(args.id)
            emit(result, args.json)
            return 0 if result.get("ok") else 1
        if args.command == "install":
            result = install(args.id, dry_run=args.dry_run)
            emit(result, args.json)
            return 0 if result.get("ok") else 1
        if args.command == "mark":
            result = mark(args.id, args.decision)
            emit(result, args.json)
            return 0 if result.get("ok") else 1
    except ValueError as exc:
        result = {"ok": False, "error": str(exc)}
        emit(result, getattr(args, "json", False))
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
