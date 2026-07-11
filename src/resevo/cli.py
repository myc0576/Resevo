from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


SCRIPT_COMMANDS = {
    "closeout-check": ("scripts", "closeout_check.py"),
    "daily-cycle": ("scripts", "daily_cycle.py"),
    "evaluate": ("scripts", "evaluator.py"),
    "evolve-proposals": ("scripts", "evolve_proposals.py"),
    "kb-index": ("scripts", "kb_index.py"),
    "project-bridge": ("scripts", "project_bridge.py"),
    "project-health": ("scripts", "project_health.py"),
    "registry": ("scripts", "registry_tool.py"),
    "run-capture": ("scripts", "run_capture.py"),
    "self-evolution": ("scripts", "self_evolution_loop.py"),
    "validate-asset-evolution": ("scripts", "validate_asset_evolution.py"),
    "validate-project": ("scripts", "validate_research_project.py"),
    "visual-to-editable": ("scripts", "visual_to_editable_router.py"),
    "war-room": ("scripts", "war_room.py"),
}


def package_public_root() -> Path:
    env_root = (
        os.environ.get("RESEVO_ENGINE_ROOT")
        or os.environ.get("RESEARCHLOOP_ENGINE_ROOT")
        or os.environ.get("RESEARCHLOOP_PUBLIC_ROOT")
    )
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def run_python_file(public_root: Path, instance_root: Path, parts: tuple[str, str], argv: list[str]) -> int:
    target = public_root / parts[0] / parts[1]
    if not target.exists():
        raise SystemExit(f"Resevo command implementation not found: {target}")
    env = os.environ.copy()
    env["RESEVO_ENGINE_ROOT"] = str(public_root)
    env["RESEVO_ROOT"] = str(instance_root)
    env["RESEARCHLOOP_ENGINE_ROOT"] = str(public_root)
    env["RESEARCHLOOP_ROOT"] = str(instance_root)
    env.setdefault("PYTHONPATH", "")
    script_path = str(public_root / "scripts")
    env["PYTHONPATH"] = script_path + (os.pathsep + env["PYTHONPATH"] if env["PYTHONPATH"] else "")
    completed = subprocess.run([sys.executable, str(target), *argv], cwd=str(instance_root), env=env)
    return int(completed.returncode)


def normalize_mcp_args(argv: list[str]) -> list[str]:
    if argv and argv[0] == "self-test":
        return ["--self-test", *argv[1:]]
    if argv and argv[0] == "serve":
        return argv[1:]
    return argv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resevo",
        description="Resevo local-first research workflow external brain.",
    )
    parser.add_argument(
        "--root",
        default=os.environ.get("RESEARCHLOOP_ROOT"),
        help="Resevo instance/workspace root. Defaults to the public checkout root.",
    )
    parser.add_argument(
        "--engine-root",
        default=os.environ.get("RESEARCHLOOP_ENGINE_ROOT") or os.environ.get("RESEARCHLOOP_PUBLIC_ROOT"),
        help="Public Resevo engine checkout. Usually inferred from the editable install.",
    )
    parser.add_argument("command", choices=sorted([*SCRIPT_COMMANDS, "mcp"]))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    public_root = Path(ns.engine_root).expanduser().resolve() if ns.engine_root else package_public_root()
    instance_root = Path(ns.root).expanduser().resolve() if ns.root else public_root

    if ns.command == "mcp":
        return run_python_file(public_root, instance_root, ("mcp", "resevo_mcp.py"), normalize_mcp_args(ns.args))
    return run_python_file(public_root, instance_root, SCRIPT_COMMANDS[ns.command], ns.args)


if __name__ == "__main__":
    raise SystemExit(main())
