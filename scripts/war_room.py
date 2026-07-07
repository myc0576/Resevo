from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _harness_common import REPORTS_DIR, STATE_DIR, append_ledger, today, write_json


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def latest_proposals() -> dict[str, Any]:
    proposal_dir = STATE_DIR / "proposals"
    if not proposal_dir.exists():
        return {}
    files = sorted(proposal_dir.glob("*_evolution_proposals.json"))
    if not files:
        return {}
    return load_json(files[-1])


def build_report() -> dict[str, Any]:
    evaluation = load_json(STATE_DIR / "evaluation.json")
    closeout = load_json(STATE_DIR / "closeout_health.json")
    project_health = load_json(STATE_DIR / "project_health.json")
    proposals = latest_proposals()
    hard_failures = evaluation.get("hard_failure_count", 0)
    closeout_errors = len(closeout.get("health", {}).get("errors", []))
    encoding_issues = len(closeout.get("health", {}).get("encoding_issues", []))
    forbidden = [
        row
        for row in closeout.get("health", {}).get("forbidden_paths", [])
        if row.get("exists") and str(row.get("path", "")).lower().endswith("knowledge\\_harness")
    ]
    verdict = "BLOCKED_FOR_REVIEW" if hard_failures or closeout_errors or forbidden else "READY"
    opinions = {
        "knowledge_auditor": {
            "summary": f"质量评估平均分 {evaluation.get('average_score', 0)}，硬失败 {hard_failures}，编码问题 {encoding_issues}。",
            "actions": ["优先处理 validated_without_evidence、bad_encoding、missing_path。"] if hard_failures or encoding_issues else ["继续保持知识卡证据边界。"],
        },
        "closeout_inspector": {
            "summary": f"项目体检 ok={project_health.get('ok')}，项目数 {project_health.get('project_count', 0)}。",
            "actions": [
                f"{row.get('project_id') or row.get('name')}: {', '.join(row.get('recommended_actions', []))}"
                for row in project_health.get("projects", [])
                if row.get("recommended_actions") != ["none"]
            ]
            or ["所有已扫描项目 closeout 桥接与素材清单处于可接受状态。"],
        },
        "structure_optimizer": {
            "summary": f"当前 evolution proposal 数 {proposals.get('proposal_count', 0)}，auto-safe {proposals.get('auto_safe_count', 0)}。",
            "actions": ["只允许小修自动应用；科学结论、验证状态和未知项目注册继续人工确认。"],
        },
    }
    result = {
        "verdict": verdict,
        "ok": verdict == "READY",
        "inputs": {
            "evaluation": str(STATE_DIR / "evaluation.json"),
            "closeout_health": str(STATE_DIR / "closeout_health.json"),
            "project_health": str(STATE_DIR / "project_health.json"),
        },
        "opinions": opinions,
    }
    write_json(STATE_DIR / "war_room.json", result)
    report_path = REPORTS_DIR / "war_room" / f"{today()}_war_room.md"
    report_path.write_text(markdown_report(result), encoding="utf-8")
    append_ledger("war_room_report", {"verdict": verdict, "report": str(report_path)})
    result["report"] = str(report_path)
    return result


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        f"# ResearchLoop War Room {today()}",
        "",
        f"- verdict: `{result['verdict']}`",
        "",
    ]
    labels = {
        "knowledge_auditor": "知识审计官",
        "closeout_inspector": "Closeout 督查官",
        "structure_optimizer": "结构优化官",
    }
    for key, opinion in result["opinions"].items():
        lines.extend([f"## {labels[key]}", "", opinion["summary"], ""])
        for action in opinion["actions"]:
            lines.append(f"- {action}")
        lines.append("")
    return "\n".join(lines)


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a lightweight research harness war-room report")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    if args.report:
        result = build_report()
        print_json(result)
        return 0 if result["ok"] else 1
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
