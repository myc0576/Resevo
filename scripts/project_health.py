from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from _harness_common import (
    PROJECTS_ROOT,
    REGISTRY_FILES,
    REPORTS_DIR,
    STATE_DIR,
    append_ledger,
    path_exists,
    read_jsonl,
    read_yaml,
    today,
    write_json,
)


BRIDGE_NEEDLE = "G:\\projects\\ResearchLoop"


def load_registry(name: str) -> list[dict[str, Any]]:
    data = read_yaml(REGISTRY_FILES[name])
    items = data.get(name, [])
    return items if isinstance(items, list) else []


def bridge_status(project_path: Path) -> dict[str, Any]:
    docs = [project_path / "AGENTS.md", project_path / "CLAUDE.md"]
    inspected: list[str] = []
    for path in docs:
        if path.exists():
            inspected.append(str(path))
            text = path.read_text(encoding="utf-8", errors="replace")
            if BRIDGE_NEEDLE in text and "G:\\knowledge\\_harness" in text:
                return {"has_bridge": True, "bridge_file": str(path), "inspected": inspected}
            if BRIDGE_NEEDLE in text:
                return {"has_bridge": True, "bridge_file": str(path), "inspected": inspected}
    return {"has_bridge": False, "bridge_file": "", "inspected": inspected}


def candidate_project_paths() -> list[Path]:
    markers = {"AGENTS.md", "CLAUDE.md", "README.md", "pyproject.toml", "package.json", ".git"}
    rows: list[Path] = []
    if not PROJECTS_ROOT.exists():
        return rows
    harness_dir_names = {"ResearchLoop", "research-harness"}
    for path in sorted(PROJECTS_ROOT.iterdir()):
        if not path.is_dir() or path.name.startswith(".") or path.name in harness_dir_names:
            continue
        if any((path / marker).exists() for marker in markers):
            rows.append(path)
    return rows


def project_last_closeout(project_id: str, project_path: Path) -> str:
    latest = ""
    ledger_path = STATE_DIR / "evolution_ledger.jsonl"
    for entry in read_jsonl(ledger_path):
        payload_text = json.dumps(entry, ensure_ascii=False)
        if project_id and project_id in payload_text or str(project_path) in payload_text:
            latest = max(latest, str(entry.get("created_at") or ""))
    asset_root = project_path / "research_assets"
    if asset_root.exists():
        for path in asset_root.rglob("00_asset_manifest.md"):
            try:
                latest = max(latest, datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"))
            except OSError:
                continue
    return latest


def asset_health(project_id: str, project_path: Path, assets: list[dict[str, Any]]) -> dict[str, Any]:
    project_assets = [item for item in assets if item.get("project_id") == project_id or str(item.get("asset_dir", "")).startswith(str(project_path))]
    missing_manifest = [item.get("id") for item in project_assets if not path_exists(item.get("manifest"))]
    missing_reproduction = [item.get("id") for item in project_assets if not path_exists(item.get("reproduction_entry"))]
    return {
        "registered_asset_count": len(project_assets),
        "missing_manifest": missing_manifest,
        "missing_reproduction": missing_reproduction,
        "complete": not missing_manifest and not missing_reproduction,
    }


def contribution_counts(project_id: str, knowledge: list[dict[str, Any]], prompts: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "knowledge_contributions": sum(1 for item in knowledge if item.get("source_project") == project_id),
        "prompt_contributions": sum(1 for item in prompts if item.get("source_project") == project_id or project_id in str(item.get("task", ""))),
        "pending_validation": sum(1 for item in knowledge if item.get("source_project") == project_id and item.get("status") == "pending validation"),
    }


def quality_for_project(project_id: str) -> dict[str, Any]:
    evaluation_path = STATE_DIR / "evaluation.json"
    if not evaluation_path.exists():
        return {"quality_score": 0.0, "quality_items": 0}
    data = json.loads(evaluation_path.read_text(encoding="utf-8"))
    rows = [item for item in data.get("items", []) if project_id in json.dumps(item, ensure_ascii=False)]
    scores = [int(item.get("score") or 0) for item in rows]
    return {"quality_score": round(sum(scores) / len(scores), 2) if scores else 0.0, "quality_items": len(scores)}


def recommended_actions(row: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if not row["registered"]:
        actions.append("register_project")
    if not row["bridge"]["has_bridge"]:
        actions.append("bridge_closeout_protocol")
    if not row["assets"]["complete"]:
        actions.append("repair_research_asset_manifest_or_reproduction_entry")
    if row["pending_validation"] > 0:
        actions.append("review_pending_validation_knowledge")
    if not row["last_closeout_date"]:
        actions.append("run_first_project_closeout")
    return actions or ["none"]


def report() -> dict[str, Any]:
    projects = load_registry("projects")
    knowledge = load_registry("knowledge")
    prompts = load_registry("prompts")
    assets = load_registry("research_assets")
    registered_by_path = {str(item.get("path")): item for item in projects}
    rows: list[dict[str, Any]] = []
    for path in candidate_project_paths():
        registry_item = registered_by_path.get(str(path), {})
        project_id = str(registry_item.get("project_id") or "")
        bridge = bridge_status(path)
        contrib = contribution_counts(project_id, knowledge, prompts) if project_id else {"knowledge_contributions": 0, "prompt_contributions": 0, "pending_validation": 0}
        asset = asset_health(project_id, path, assets) if project_id else {"registered_asset_count": 0, "missing_manifest": [], "missing_reproduction": [], "complete": True}
        row = {
            "project_id": project_id,
            "name": registry_item.get("name") or path.name,
            "path": str(path),
            "registered": bool(registry_item),
            "bridge": bridge,
            "last_closeout_date": project_last_closeout(project_id, path),
            "assets": asset,
            **contrib,
            **quality_for_project(project_id),
        }
        row["recommended_actions"] = recommended_actions(row)
        rows.append(row)
    registered_only = [
        item
        for item in projects
        if str(item.get("path", "")).startswith("G:\\projects") and str(item.get("path")) not in {row["path"] for row in rows}
    ]
    for item in registered_only:
        path = Path(str(item.get("path")))
        row = {
            "project_id": item.get("project_id"),
            "name": item.get("name"),
            "path": str(path),
            "registered": True,
            "bridge": bridge_status(path) if path.exists() else {"has_bridge": False, "bridge_file": "", "inspected": []},
            "last_closeout_date": project_last_closeout(str(item.get("project_id")), path) if path.exists() else "",
            "assets": asset_health(str(item.get("project_id")), path, assets) if path.exists() else {"registered_asset_count": 0, "missing_manifest": [], "missing_reproduction": [], "complete": True},
            **contribution_counts(str(item.get("project_id")), knowledge, prompts),
            **quality_for_project(str(item.get("project_id"))),
        }
        row["recommended_actions"] = recommended_actions(row)
        rows.append(row)
    hard_blockers = [
        row["project_id"] or row["name"]
        for row in rows
        if not row["registered"] or not row["assets"]["complete"]
    ]
    result = {
        "ok": not hard_blockers,
        "hard_blockers": hard_blockers,
        "project_count": len(rows),
        "projects": rows,
    }
    write_json(STATE_DIR / "project_health.json", result)
    report_path = REPORTS_DIR / "project_health" / f"{today()}_project_health.md"
    report_path.write_text(markdown_report(result), encoding="utf-8")
    append_ledger(
        "project_health_report",
        {
            "ok": result["ok"],
            "project_count": result["project_count"],
            "report": str(report_path),
            "unhealthy_projects": [row["project_id"] or row["name"] for row in rows if row["recommended_actions"] != ["none"]],
        },
    )
    result["report"] = str(report_path)
    return result


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        f"# Project Health {today()}",
        "",
        f"- ok: `{result['ok']}`",
        f"- project_count: `{result['project_count']}`",
        f"- hard_blockers: `{len(result.get('hard_blockers', []))}`",
        "",
        "## Projects",
        "",
    ]
    for row in result["projects"]:
        actions = ", ".join(row["recommended_actions"])
        lines.append(
            f"- {row['project_id'] or '(unregistered)'} | {row['name']} | bridge={row['bridge']['has_bridge']} "
            f"| assets={row['assets']['registered_asset_count']} | knowledge={row['knowledge_contributions']} "
            f"| pending={row['pending_validation']} | quality={row['quality_score']} | actions={actions}"
        )
    lines.append("")
    return "\n".join(lines)


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate project-level ResearchLoop health report")
    sub = parser.add_subparsers(dest="command", required=True)
    report_parser = sub.add_parser("report")
    report_parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.command == "report":
        result = report()
        print_json(result)
        return 0 if result["ok"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
