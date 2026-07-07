from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).absolute().parents[1]


def resolve_path(raw: str | Path, base: Path) -> Path:
    path = Path(str(raw))
    if path.is_absolute():
        return path
    return base / path


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def nonempty(value: Any) -> bool:
    return value not in (None, "", [])


def validate_markdown_terms(project_root: Path, rules: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    for check in rules.get("markdown_checks", []) or []:
        path = resolve_path(check["path"], project_root)
        if not path.exists():
            errors.append(f"missing_markdown:{check['id']}:{path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for term in check.get("required_terms", []) or []:
            if str(term).lower() not in text:
                warnings.append(f"markdown_missing_term:{check['id']}:{term}")


def validate_yaml_lists(project_root: Path, rules: dict[str, Any], errors: list[str]) -> None:
    for check in rules.get("yaml_checks", []) or []:
        path = resolve_path(check["path"], project_root)
        if not path.exists():
            errors.append(f"missing_yaml:{check['id']}:{path}")
            continue
        data = load_yaml(path)
        items = data.get(check["list_key"], [])
        if not isinstance(items, list) or not items:
            errors.append(f"yaml_list_empty:{check['id']}:{path}:{check['list_key']}")
            continue
        allowed_status = set(check.get("status_values", []) or [])
        status_field = check.get("status_field")
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"yaml_item_not_object:{check['id']}:{index}")
                continue
            for field in check.get("required_fields", []) or []:
                if not nonempty(item.get(field)):
                    errors.append(f"yaml_item_missing_field:{check['id']}:{index}:{field}")
            if status_field and allowed_status and item.get(status_field) not in allowed_status:
                errors.append(f"yaml_item_invalid_status:{check['id']}:{index}:{item.get(status_field)}")


def validate(project_root: Path, rules_path: Path) -> dict[str, Any]:
    project_root = project_root.absolute()
    rules = load_yaml(rules_path)
    errors: list[str] = []
    warnings: list[str] = []
    checked: list[str] = []

    for item in rules.get("required_paths", []) or []:
        path = resolve_path(item["path"], project_root)
        checked.append(str(path))
        if not path.exists():
            errors.append(f"missing_required_path:{item['id']}:{path}")

    for item in rules.get("reproduction_entry", {}).get("required_any", []) or []:
        candidates = [resolve_path(candidate, project_root) for candidate in item.get("paths", []) or []]
        checked.extend(str(path) for path in candidates)
        if not any(path.exists() for path in candidates):
            errors.append(f"missing_reproduction_entry:{item['id']}:{[str(path) for path in candidates]}")

    validate_yaml_lists(project_root, rules, errors)
    validate_markdown_terms(project_root, rules, errors, warnings)

    return {
        "ok": not errors,
        "project_root": str(project_root),
        "rules": str(rules_path),
        "checked_count": len(checked),
        "errors": errors,
        "warnings": warnings,
    }


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a paper-driven research project skeleton")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--rules", default=str(ROOT / "workflows" / "paper_lifecycle" / "validation_rules.yaml"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(Path(args.project_root), Path(args.rules))
    if args.json:
        print_json(result)
    else:
        print("research project validation passed" if result["ok"] else "research project validation failed")
        for error in result["errors"]:
            print(error)
        for warning in result["warnings"]:
            print(f"warning: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
