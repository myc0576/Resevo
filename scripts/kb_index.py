from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from _harness_common import (
    ROOT,
    REUSABLE_KNOWLEDGE_ROOT,
    REUSABLE_PROMPTS_ROOT,
    STATE_DIR,
    append_ledger,
    first_heading,
    read_yaml,
    write_json,
)


INDEX_PATH = STATE_DIR / "kb_index" / "research_kb.sqlite"
INDEX_ROOTS = [
    REUSABLE_KNOWLEDGE_ROOT,
    REUSABLE_PROMPTS_ROOT,
    ROOT / "system_design",
    ROOT / "skills",
    ROOT / "workflows",
    ROOT / "templates",
    ROOT / "registry",
    ROOT / "examples",
    ROOT / "decisions",
    ROOT / "reports",
]


def connect() -> sqlite3.Connection:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(INDEX_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS docs ("
        "id INTEGER PRIMARY KEY, path TEXT UNIQUE NOT NULL, title TEXT NOT NULL, kind TEXT NOT NULL, "
        "mtime REAL NOT NULL, content TEXT NOT NULL)"
    )
    conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(path, title, content)")
    return conn


def classify(path: Path) -> str:
    parts = {part.lower() for part in path.parts}
    if "reusable_knowledge" in parts:
        return "knowledge"
    if "reusable_prompts" in parts:
        return "prompt"
    if "decisions" in parts:
        return "decision"
    if "workflows" in parts:
        return "workflow"
    if "templates" in parts:
        return "template"
    if "registry" in parts:
        return "registry"
    if "examples" in parts:
        return "example"
    if "reports" in parts:
        return "report"
    if "skills" in parts:
        return "skill"
    if "system_design" in parts:
        return "system_design"
    return "document"


def iter_documents() -> list[Path]:
    files: list[Path] = []
    for root in INDEX_ROOTS:
        if not root.exists():
            continue
        files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".txt"})
    return sorted(set(files))


def rebuild() -> dict[str, Any]:
    conn = connect()
    conn.execute("DELETE FROM docs")
    conn.execute("DELETE FROM docs_fts")
    count = 0
    for path in iter_documents():
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        title = first_heading(path)
        kind = classify(path)
        mtime = path.stat().st_mtime
        cur = conn.execute(
            "INSERT INTO docs(path, title, kind, mtime, content) VALUES (?, ?, ?, ?, ?)",
            (str(path), title, kind, mtime, content),
        )
        rowid = cur.lastrowid
        conn.execute(
            "INSERT INTO docs_fts(rowid, path, title, content) VALUES (?, ?, ?, ?)",
            (rowid, str(path), title, content),
        )
        count += 1
    conn.commit()
    conn.close()
    result = {"ok": True, "index": str(INDEX_PATH), "document_count": count}
    write_json(STATE_DIR / "kb_index" / "last_rebuild.json", result)
    append_ledger("kb_index_rebuild", result)
    return result


def fts_query(raw: str) -> str:
    tokens = [token.replace('"', "") for token in raw.split() if token.strip()]
    if not tokens:
        return raw
    return " OR ".join(f'"{token}"' for token in tokens)


def search(query: str, limit: int) -> dict[str, Any]:
    conn = connect()
    rows: list[tuple[str, str, str, float, str]] = []
    try:
        rows = conn.execute(
            "SELECT d.path, d.title, d.kind, bm25(docs_fts) AS score, "
            "snippet(docs_fts, 2, '[', ']', ' ... ', 18) "
            "FROM docs_fts JOIN docs d ON docs_fts.rowid = d.id "
            "WHERE docs_fts MATCH ? ORDER BY score LIMIT ?",
            (fts_query(query), limit),
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []
    if not rows:
        like = f"%{query}%"
        rows = conn.execute(
            "SELECT path, title, kind, 0.0 AS score, substr(content, 1, 260) FROM docs "
            "WHERE content LIKE ? OR title LIKE ? OR path LIKE ? LIMIT ?",
            (like, like, like, limit),
        ).fetchall()
    if not rows:
        terms = [term for term in query.split() if term]
        for term in terms:
            like = f"%{term}%"
            rows.extend(
                conn.execute(
                    "SELECT path, title, kind, 0.0 AS score, substr(content, 1, 260) FROM docs "
                    "WHERE content LIKE ? OR title LIKE ? OR path LIKE ? LIMIT ?",
                    (like, like, like, limit),
                ).fetchall()
            )
            if len(rows) >= limit:
                rows = rows[:limit]
                break
    conn.close()
    results = [
        {"path": path, "title": title, "kind": kind, "score": score, "snippet": snippet}
        for path, title, kind, score, snippet in rows[:limit]
    ]
    return {"query": query, "limit": limit, "result_count": len(results), "results": results}


def stale(days: int) -> dict[str, Any]:
    cutoff = datetime.now().date() - timedelta(days=days)
    stale_items: list[dict[str, Any]] = []
    for reg_name, list_name in [("knowledge.yaml", "knowledge"), ("prompts.yaml", "prompts")]:
        data = read_yaml(ROOT / "registry" / reg_name)
        for item in data.get(list_name, []) or []:
            status = item.get("status")
            if status not in {"pending validation", "hypothesis"}:
                continue
            raw_date = str(item.get("updated_at") or item.get("created_at") or "")
            try:
                item_date = datetime.fromisoformat(raw_date[:10]).date()
            except ValueError:
                item_date = cutoff
            if item_date <= cutoff:
                stale_items.append(
                    {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "status": status,
                        "updated_at": raw_date,
                        "path": item.get("path"),
                    }
                )
    return {"days": days, "cutoff": cutoff.isoformat(), "count": len(stale_items), "items": stale_items}


def print_json(data: dict[str, Any]) -> None:
    import json

    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Research harness SQLite FTS5 index")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("rebuild")
    search_parser = sub.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    stale_parser = sub.add_parser("stale")
    stale_parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    if args.command == "rebuild":
        print_json(rebuild())
        return 0
    if args.command == "search":
        print_json(search(args.query, args.limit))
        return 0
    if args.command == "stale":
        print_json(stale(args.days))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
