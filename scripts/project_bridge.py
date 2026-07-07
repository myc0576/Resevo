from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _harness_common import PROJECTS_ROOT, append_ledger, read_yaml, slugify_project_id, write_json, write_yaml


BRIDGE_MARKER_START = "<!-- RESEARCH_HARNESS_PROJECT_CLOSEOUT:START -->"
BRIDGE_MARKER_END = "<!-- RESEARCH_HARNESS_PROJECT_CLOSEOUT:END -->"
BRIDGE_TEXT = f"""
{BRIDGE_MARKER_START}
## Workspace Closeout

本项目所有有价值任务完成后，必须参照 ResearchLoop 的 `G:\\projects\\ResearchLoop\\AGENTS.md` 执行 task closeout。
路径解析硬规则：`harness` 的唯一写入目标是 `G:\\projects\\ResearchLoop`。不要写入或创建 `G:\\knowledge\\_harness`；`G:\\知识库\\_harness` 只能只读参考。
当用户说“自进化 / 沉淀 / 更新 / 写回 / 复用 / 调用 harness / 查历史 / closeout / loop”时，先运行 `G:\\projects\\ResearchLoop\\scripts\\self_evolution_loop.py recall`，需要写回时先生成 self-evolution intake，再运行 `self_evolution_loop.py run --apply-candidates`。
自动写回只能使用 `candidate` 或 `pending validation`，不得自动晋升为 `validated`、`reusable`、`approved`、`pass` 或 `paper_ready`。
可复用知识写入 `G:\\knowledge\\reusable_knowledge`，可复用 prompt 写入 `G:\\knowledge\\reusable_prompts`，项目素材写入本项目 `research_assets\\YYYYMMDD_task_name`。
小论文正文、图件和投稿文件默认写入 `G:\\docs\\小论文\\<paper_id>`；ResearchLoop 只保存模板、流程、索引和决策记录。
无可沉淀内容时，最终回复说明：`closeout checked: no reusable assets`。
{BRIDGE_MARKER_END}
""".strip()

MARKERS = {"AGENTS.md", "CLAUDE.md", "README.md", "pyproject.toml", "package.json", ".git"}
DOCS = ("AGENTS.md", "CLAUDE.md", "README.md")


def load_projects() -> dict[str, Any]:
    path = Path("G:/BaiduSyncdisk/ResearchLoop/registry/projects.yaml")
    data = read_yaml(path)
    data.setdefault("version", 1)
    data.setdefault("projects", [])
    return data


def save_projects(data: dict[str, Any]) -> None:
    write_yaml(Path("G:/BaiduSyncdisk/ResearchLoop/registry/projects.yaml"), data)


def candidate_projects() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not PROJECTS_ROOT.exists():
        return rows
    for path in sorted(PROJECTS_ROOT.iterdir()):
        if not path.is_dir() or path.name.startswith(".") or path.name == "__pycache__":
            continue
        marker_names = sorted(marker for marker in MARKERS if (path / marker).exists())
        if marker_names:
            rows.append({"name": path.name, "path": str(path), "markers": marker_names})
    return rows


def doc_files(project_path: Path) -> list[Path]:
    return [project_path / name for name in DOCS if (project_path / name).exists()]


def has_bridge(project_path: Path) -> bool:
    for path in doc_files(project_path):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "G:\\projects\\ResearchLoop" in text or BRIDGE_MARKER_START in text:
            return True
    return False


def select_bridge_file(project_path: Path) -> Path:
    if (project_path / "AGENTS.md").exists():
        return project_path / "AGENTS.md"
    if (project_path / "CLAUDE.md").exists():
        return project_path / "CLAUDE.md"
    return project_path / "AGENTS.md"


def scan() -> dict[str, Any]:
    registry = load_projects()
    registered_paths = {str(item.get("path")) for item in registry.get("projects", [])}
    registered_ids = {str(item.get("project_id")): item for item in registry.get("projects", [])}
    rows: list[dict[str, Any]] = []
    for candidate in candidate_projects():
        path = Path(candidate["path"])
        project_id = ""
        for item_id, item in registered_ids.items():
            if str(item.get("path")) == str(path):
                project_id = item_id
                break
        rows.append(
            {
                **candidate,
                "project_id": project_id,
                "registered": str(path) in registered_paths,
                "has_bridge": has_bridge(path),
                "bridge_target": str(select_bridge_file(path)),
            }
        )
    result = {
        "candidate_count": len(rows),
        "unregistered": [row for row in rows if not row["registered"]],
        "missing_bridge": [row for row in rows if not row["has_bridge"]],
        "projects": rows,
    }
    write_json(Path("G:/BaiduSyncdisk/ResearchLoop/state/project_bridge_scan.json"), result)
    return result


def find_project(identifier: str) -> Path:
    registry = load_projects()
    for item in registry.get("projects", []):
        if identifier in {str(item.get("project_id")), str(item.get("name")), Path(str(item.get("path", ""))).name}:
            return Path(str(item["path"]))
    direct = PROJECTS_ROOT / identifier
    if direct.exists():
        return direct
    raise SystemExit(f"project not found: {identifier}")


def ensure_registered(project_path: Path, project_id: str | None = None, role: str | None = None) -> str:
    data = load_projects()
    for item in data.get("projects", []):
        if str(item.get("path")) == str(project_path):
            return str(item.get("project_id"))
    resolved_id = project_id or slugify_project_id(project_path.name)
    existing = {str(item.get("project_id")) for item in data.get("projects", [])}
    base = resolved_id
    counter = 2
    while resolved_id in existing:
        resolved_id = f"{base}-{counter}"
        counter += 1
    data["projects"].append(
        {
            "project_id": resolved_id,
            "name": project_path.name,
            "path": str(project_path),
            "role": role or "active workspace project",
            "closeout_required": True,
            "notes": "由 project_bridge.py 自动注册；任务结束后执行 ResearchLoop workspace closeout。",
        }
    )
    save_projects(data)
    return resolved_id


def apply_bridge(project_path: Path, register: bool = True, project_id: str | None = None, role: str | None = None) -> dict[str, Any]:
    project_path.mkdir(parents=True, exist_ok=True)
    resolved_project_id = ensure_registered(project_path, project_id=project_id, role=role) if register else ""
    target = select_bridge_file(project_path)
    if target.exists():
        text = target.read_text(encoding="utf-8", errors="replace")
        if BRIDGE_MARKER_START in text or "G:\\projects\\ResearchLoop" in text:
            return {"project": str(project_path), "project_id": resolved_project_id, "target": str(target), "changed": False, "reason": "already_bridged"}
        target.write_text(text.rstrip() + "\n\n" + BRIDGE_TEXT + "\n", encoding="utf-8")
    else:
        target.write_text("# AGENTS.md\n\n" + BRIDGE_TEXT + "\n", encoding="utf-8")
    return {"project": str(project_path), "project_id": resolved_project_id, "target": str(target), "changed": True}


def apply_registered() -> dict[str, Any]:
    data = load_projects()
    results: list[dict[str, Any]] = []
    for item in data.get("projects", []):
        path = Path(str(item.get("path", "")))
        if str(path) in {"G:\\", "G:/"} or path.name == "ResearchLoop" or not str(path).startswith("G:\\projects"):
            continue
        if path.exists():
            results.append(apply_bridge(path, register=False))
    append_ledger("project_bridge_apply_registered", {"results": results})
    return {"changed_count": sum(1 for row in results if row.get("changed")), "results": results}


def print_json(data: dict[str, Any]) -> None:
    import json

    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Bridge projects to ResearchLoop closeout")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("scan")
    apply_parser = sub.add_parser("apply")
    group = apply_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--registered", action="store_true")
    group.add_argument("--project")
    apply_parser.add_argument("--project-id")
    apply_parser.add_argument("--role")
    args = parser.parse_args()
    if args.command == "scan":
        print_json(scan())
        return 0
    if args.command == "apply":
        if args.registered:
            print_json(apply_registered())
        else:
            result = apply_bridge(find_project(args.project), register=True, project_id=args.project_id, role=args.role)
            append_ledger("project_bridge_apply_project", result)
            print_json(result)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
