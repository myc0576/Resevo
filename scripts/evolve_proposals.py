from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from _harness_common import (
    REGISTRY_FILES,
    REPORTS_DIR,
    STATE_DIR,
    append_ledger,
    clamp_confidence,
    confidence_for_status,
    contains_bad_encoding,
    now_iso,
    read_yaml,
    registry_item_id,
    restore_snapshot,
    snapshot_files,
    today,
    write_json,
    write_yaml,
)

sys.path.insert(0, str(Path(__file__).absolute().parent))

import project_bridge  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def registry_entries(name: str) -> list[dict[str, Any]]:
    data = read_yaml(REGISTRY_FILES[name])
    items = data.get(name, [])
    return items if isinstance(items, list) else []


def proposal(kind: str, title: str, severity: str, target: str, recommendation: str, auto_safe: bool = False) -> dict[str, Any]:
    return {
        "id": f"{today()}_{kind}_{abs(hash((kind, title, target))) % 100000:05d}",
        "kind": kind,
        "title": title,
        "severity": severity,
        "target": target,
        "recommendation": recommendation,
        "auto_safe": auto_safe,
        "status": "open",
        "created_at": now_iso(),
    }


def scan_metadata_gaps() -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    required = ["confidence", "confidence_reason", "reference_count", "last_used_at", "last_reviewed_at", "quality_level", "superseded_by"]
    for name, path in REGISTRY_FILES.items():
        if name == "feedback":
            continue
        for index, item in enumerate(registry_entries(name)):
            missing = [field for field in required if field not in item]
            item_id = registry_item_id(item, index)
            if missing:
                proposals.append(
                    proposal(
                        "metadata",
                        f"{name}:{item_id} 缺少 v2 元数据字段",
                        "low",
                        f"{name}:{item_id}",
                        "补齐 confidence/reference/quality/review 元数据，不改变科学 status。",
                        auto_safe=True,
                    )
                )
            if contains_bad_encoding(item) and item.get("encoding_status") != "needs_review":
                proposals.append(
                    proposal(
                        "encoding",
                        f"{name}:{item_id} 存在未标记编码问题",
                        "high",
                        f"{name}:{item_id}",
                        "标记 encoding_status=needs_review，后续人工决定是否语义修复。",
                        auto_safe=True,
                    )
                )
    return proposals


def scan_quality_failures(evaluation: dict[str, Any]) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for item in evaluation.get("items", []):
        if item.get("hard_failures"):
            proposals.append(
                proposal(
                    "quality",
                    f"{item['registry']}:{item['id']} 有硬失败",
                    "high",
                    f"{item['registry']}:{item['id']}",
                    "人工修复硬失败；若是 validated_without_evidence，需要补证据或降级为 pending validation。",
                    auto_safe=False,
                )
            )
        elif item.get("quality_level") == "needs_attention":
            proposals.append(
                proposal(
                    "quality",
                    f"{item['registry']}:{item['id']} 质量低于 bronze",
                    "medium",
                    f"{item['registry']}:{item['id']}",
                    "补齐内容字段、验证依据或复现入口。",
                    auto_safe=False,
                )
            )
    return proposals


def scan_project_health(project_health: dict[str, Any]) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for row in project_health.get("projects", []):
        project_id = row.get("project_id") or row.get("name")
        if not row.get("registered"):
            proposals.append(
                proposal(
                    "project",
                    f"{row['name']} 未注册",
                    "medium",
                    str(row["path"]),
                    "注册项目信息后再桥接 closeout；未知项目不自动注册。",
                    auto_safe=False,
                )
            )
        elif not row.get("bridge", {}).get("has_bridge"):
            proposals.append(
                proposal(
                    "project_bridge",
                    f"{project_id} 缺少 closeout 桥接",
                    "high",
                    str(row["path"]),
                    "向项目级 AGENTS.md/CLAUDE.md 追加 canonical harness closeout 文本。",
                    auto_safe=True,
                )
            )
        if not row.get("assets", {}).get("complete", True):
            proposals.append(
                proposal(
                    "asset",
                    f"{project_id} research_assets 不完整",
                    "high",
                    str(row["path"]),
                    "补齐 00_asset_manifest.md 和 reproduction_entry.md。",
                    auto_safe=False,
                )
            )
    return proposals


def scan() -> dict[str, Any]:
    evaluation = load_json(STATE_DIR / "evaluation.json")
    project_health = load_json(STATE_DIR / "project_health.json")
    proposals = []
    proposals.extend(scan_metadata_gaps())
    proposals.extend(scan_quality_failures(evaluation))
    proposals.extend(scan_project_health(project_health))
    result = {
        "ok": True,
        "created_at": now_iso(),
        "proposal_count": len(proposals),
        "auto_safe_count": sum(1 for item in proposals if item["auto_safe"]),
        "proposals": proposals,
    }
    proposal_path = STATE_DIR / "proposals" / f"{today()}_evolution_proposals.json"
    write_json(proposal_path, result)
    report_path = REPORTS_DIR / "proposals" / f"{today()}_evolution_proposals.md"
    report_path.write_text(markdown_report(result), encoding="utf-8")
    append_ledger(
        "evolution_proposal_scan",
        {
            "proposal_count": result["proposal_count"],
            "auto_safe_count": result["auto_safe_count"],
            "proposal_path": str(proposal_path),
            "report": str(report_path),
        },
    )
    result["proposal_path"] = str(proposal_path)
    result["report"] = str(report_path)
    return result


def feedback_adjustment(target_id: str, feedback: list[dict[str, Any]]) -> float:
    delta = 0.0
    for item in feedback:
        if item.get("target_id") != target_id:
            continue
        feedback_type = item.get("feedback_type")
        if feedback_type == "useful":
            delta += 0.05
        elif feedback_type in {"wrong", "outdated"}:
            delta -= 0.20
        elif feedback_type == "needs_review":
            delta -= 0.05
    return delta


def update_registry_metadata(evaluation: dict[str, Any]) -> dict[str, Any]:
    eval_by_key = {(item["registry"], item["id"]): item for item in evaluation.get("items", [])}
    feedback = registry_entries("feedback")
    changed: list[str] = []
    for name, path in REGISTRY_FILES.items():
        if name == "feedback":
            continue
        data = read_yaml(path)
        items = data.get(name, [])
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            item_id = registry_item_id(item, index)
            eval_item = eval_by_key.get((name, item_id), {})
            reference_count = int(eval_item.get("reference_count") or item.get("reference_count") or 0)
            status = str(item.get("status") or "")
            confidence = confidence_for_status(status) + min(reference_count, 5) * 0.03 + feedback_adjustment(item_id, feedback)
            updates = {
                "confidence": clamp_confidence(confidence),
                "confidence_reason": item.get("confidence_reason") or f"default_from_status:{status or 'unknown'};refs:{reference_count}",
                "reference_count": reference_count,
                "last_used_at": item.get("last_used_at") or (now_iso() if reference_count else ""),
                "last_reviewed_at": now_iso(),
                "quality_level": eval_item.get("quality_level") or item.get("quality_level") or "unrated",
                "superseded_by": item.get("superseded_by") or "",
                "encoding_status": "needs_review" if contains_bad_encoding(item) else item.get("encoding_status", "ok"),
            }
            for field, value in updates.items():
                if item.get(field) != value:
                    item[field] = value
                    changed.append(f"{name}:{item_id}:{field}")
        write_yaml(path, data)
    return {"changed": changed, "changed_count": len(changed)}


def apply_safe_fixes() -> dict[str, Any]:
    run_id = f"{today()}_apply_safe_{abs(hash(now_iso())) % 100000:05d}"
    snapshot = snapshot_files(REGISTRY_FILES.values(), run_id, "evolve_proposals_apply_safe")
    evaluation = load_json(STATE_DIR / "evaluation.json")
    metadata_result = update_registry_metadata(evaluation)
    bridge_result = project_bridge.apply_registered()
    ledger = append_ledger(
        "evolution_apply_safe_fixes",
        {
            "run_id": run_id,
            "metadata_result": metadata_result,
            "bridge_result": bridge_result,
            "snapshot": snapshot,
            "rollback_manifest": snapshot["rollback_manifest"],
        },
    )
    return {
        "run_id": run_id,
        "metadata_result": metadata_result,
        "bridge_result": bridge_result,
        "snapshot": snapshot,
        "ledger_path": ledger["ledger_path"],
    }


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        f"# Evolution Proposals {today()}",
        "",
        f"- proposal_count: `{result['proposal_count']}`",
        f"- auto_safe_count: `{result['auto_safe_count']}`",
        "",
        "## Proposals",
        "",
    ]
    if not result["proposals"]:
        lines.append("- none")
    for item in result["proposals"]:
        lines.append(f"- [{item['severity']}] {item['kind']} | {item['target']} | auto_safe={item['auto_safe']} | {item['recommendation']}")
    lines.append("")
    return "\n".join(lines)


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate and optionally apply safe research harness evolution proposals")
    sub = parser.add_subparsers(dest="command", required=True)
    scan_parser = sub.add_parser("scan")
    scan_parser.add_argument("--apply-safe", action="store_true")
    rollback_parser = sub.add_parser("rollback")
    rollback_parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    if args.command == "scan":
        result = scan()
        if args.apply_safe:
            result["apply_safe"] = apply_safe_fixes()
        print_json(result)
        return 0
    if args.command == "rollback":
        print_json(restore_snapshot(args.manifest))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
