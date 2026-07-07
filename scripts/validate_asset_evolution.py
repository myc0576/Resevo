from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).absolute().parents[1]

ASSET_TYPES = {
    "figure_style",
    "plotting_script",
    "narrative_pattern",
    "caption_pattern",
    "prompt",
    "template",
    "validation_rule",
    "dataset_recipe",
    "release_recipe",
    "dissemination_recipe",
    "workflow_rule",
}
STATUSES = {"candidate", "reviewed", "reusable", "deprecated", "replaced"}
EXPECTED_FIELDS = {
    "asset_id",
    "asset_type",
    "title",
    "source_project",
    "source_output_objects",
    "source_claims",
    "source_figures",
    "current_version",
    "status",
    "quality_score",
    "reuse_count",
    "known_issues",
    "applicable_contexts",
    "non_applicable_contexts",
    "reproduction_entry",
    "linked_files",
    "successor_asset_id",
    "next_upgrade_action",
    "updated_at",
}
NONEMPTY_FIELDS = {
    "asset_id",
    "asset_type",
    "title",
    "source_project",
    "source_output_objects",
    "current_version",
    "status",
    "quality_score",
    "reuse_count",
    "applicable_contexts",
    "non_applicable_contexts",
    "reproduction_entry",
    "linked_files",
    "next_upgrade_action",
    "updated_at",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def resolve_path(raw: Any) -> Path:
    path = Path(str(raw))
    if path.is_absolute():
        return path
    return ROOT / path


def as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    return value if isinstance(value, list) else [value]


def nonempty(value: Any) -> bool:
    return value not in (None, "", [])


def output_object_ids(path: Path) -> set[str]:
    data = load_yaml(path)
    return {str(item.get("output_id")) for item in data.get("output_objects", []) or [] if item.get("output_id")}


def validate(registry: Path, output_objects: Path) -> dict[str, Any]:
    data = load_yaml(registry)
    items = data.get("asset_evolution", [])
    known_outputs = output_object_ids(output_objects)
    errors: list[str] = []
    warnings: list[str] = []
    ids: set[str] = set()

    if not isinstance(items, list):
        return {"ok": False, "registry": str(registry), "errors": ["asset_evolution_not_list"], "warnings": warnings}

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"item_not_object:{index}")
            continue
        asset_id = str(item.get("asset_id") or f"item_{index}")
        if asset_id in ids:
            errors.append(f"duplicate_asset_id:{asset_id}")
        ids.add(asset_id)

        missing_keys = sorted(EXPECTED_FIELDS - item.keys())
        if missing_keys:
            errors.append(f"{asset_id}:missing_keys:{missing_keys}")
        for field in sorted(NONEMPTY_FIELDS):
            if not nonempty(item.get(field)):
                errors.append(f"{asset_id}:missing_required_field:{field}")

        if item.get("asset_type") not in ASSET_TYPES:
            errors.append(f"{asset_id}:invalid_asset_type:{item.get('asset_type')}")
        if item.get("status") not in STATUSES:
            errors.append(f"{asset_id}:invalid_status:{item.get('status')}")

        try:
            score = float(item.get("quality_score"))
            if score < 0 or score > 5:
                errors.append(f"{asset_id}:quality_score_out_of_range:{score}")
        except (TypeError, ValueError):
            errors.append(f"{asset_id}:quality_score_not_number:{item.get('quality_score')}")

        for linked in as_list(item.get("linked_files")):
            if not resolve_path(linked).exists():
                errors.append(f"{asset_id}:missing_linked_file:{linked}")
        if item.get("reproduction_entry") and not resolve_path(item["reproduction_entry"]).exists():
            errors.append(f"{asset_id}:missing_reproduction_entry:{item['reproduction_entry']}")
        if item.get("asset_card") and not resolve_path(item["asset_card"]).exists():
            errors.append(f"{asset_id}:missing_asset_card:{item['asset_card']}")

        for output_id in as_list(item.get("source_output_objects")):
            if str(output_id) not in known_outputs:
                errors.append(f"{asset_id}:unknown_source_output_object:{output_id}")

        if item.get("status") == "reusable":
            if not item.get("asset_card"):
                errors.append(f"{asset_id}:reusable_missing_asset_card")
            if not item.get("reproduction_entry"):
                errors.append(f"{asset_id}:reusable_missing_reproduction_entry")
            if not item.get("applicable_contexts"):
                errors.append(f"{asset_id}:reusable_missing_applicable_contexts")
            if not item.get("source_output_objects"):
                errors.append(f"{asset_id}:reusable_missing_real_source")

        if item.get("status") in {"deprecated", "replaced"} and not (item.get("successor_asset_id") or item.get("known_issues")):
            errors.append(f"{asset_id}:{item.get('status')}_missing_reason_or_successor")

        if item.get("status") == "candidate" and item.get("reuse_count", 0):
            warnings.append(f"{asset_id}:candidate_has_reuse_count")

    return {
        "ok": not errors,
        "registry": str(registry),
        "output_objects": str(output_objects),
        "asset_count": len(items),
        "errors": errors,
        "warnings": warnings,
    }


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate asset evolution registry")
    parser.add_argument("--registry", default=str(ROOT / "registry" / "asset_evolution.yaml"))
    parser.add_argument("--output-objects", default=str(ROOT / "registry" / "output_objects.yaml"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(resolve_path(args.registry), resolve_path(args.output_objects))
    if args.json:
        print_json(result)
    else:
        print("asset evolution validation passed" if result["ok"] else "asset evolution validation failed")
        for error in result["errors"]:
            print(error)
        for warning in result["warnings"]:
            print(f"warning: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
