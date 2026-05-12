#!/usr/bin/env python3
"""Read-only database/storage inventory for OpenClaw -> Hermes migration.

The script reports file metadata and schema-level information only. It does not
print row contents, messages, documents, secrets or connection strings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DB_SUFFIXES = {
    ".db", ".sqlite", ".sqlite3", ".duckdb", ".mdb", ".realm",
}
DATA_SUFFIXES = {
    ".jsonl", ".json", ".csv", ".tsv", ".parquet", ".feather", ".arrow",
    ".pkl", ".pickle", ".ndjson",
}
VECTOR_DIR_HINTS = {
    "chroma", "chromadb", "faiss", "lancedb", "qdrant", "milvus", "weaviate",
    "vectors", "vectorstore", "embeddings", "sqlite-vec",
}
SECRET_NAME_HINTS = {
    "secret", "token", "auth", "credential", "cookie", "password", "key",
}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}


def sha256_prefix(path: Path, max_bytes: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        remaining = max_bytes
        while remaining > 0:
            chunk = f.read(min(65536, remaining))
            if not chunk:
                break
            h.update(chunk)
            remaining -= len(chunk)
    return h.hexdigest()


def is_sqlite(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            return f.read(16) == b"SQLite format 3\x00"
    except OSError:
        return False


def sqlite_schema(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"quick_check": None, "tables": [], "errors": []}
    try:
        uri = f"file:{path.resolve()}?mode=ro"
        con = sqlite3.connect(uri, uri=True, timeout=2)
        try:
            cur = con.execute("PRAGMA quick_check")
            result["quick_check"] = cur.fetchone()[0]
            rows = con.execute(
                "SELECT name, type FROM sqlite_master "
                "WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' "
                "ORDER BY type, name"
            ).fetchall()
            tables = []
            for name, typ in rows:
                entry = {"name": name, "type": typ}
                if typ == "table":
                    try:
                        cnt = con.execute(f'SELECT COUNT(*) FROM "{name.replace(chr(34), chr(34)*2)}"').fetchone()[0]
                        entry["row_count"] = cnt
                    except Exception as e:  # noqa: BLE001
                        entry["row_count_error"] = type(e).__name__
                tables.append(entry)
            result["tables"] = tables
        finally:
            con.close()
    except Exception as e:  # noqa: BLE001
        result["errors"].append(f"{type(e).__name__}: {e}")
    return result


def count_lines(path: Path, max_lines: int = 10_000_000) -> int | str:
    try:
        total = 0
        with path.open("rb") as f:
            for total, _ in enumerate(f, 1):
                if total >= max_lines:
                    return f">={max_lines}"
        return total
    except Exception as e:  # noqa: BLE001
        return f"error:{type(e).__name__}"


def classify_action(path: Path, kind: str, secret_risk: bool) -> str:
    lower = str(path).lower()
    if secret_risk:
        return "quarantine_or_manual_review"
    if kind == "sqlite" and any(x in lower for x in ["session", "history", "conversation"]):
        return "archive_plus_summarize_not_direct_import"
    if kind == "sqlite" and any(x in lower for x in ["memory", "vector", "embedding"]):
        return "rebuild_index_in_hermes_not_blind_copy"
    if kind == "vector_directory":
        return "rebuild_from_source_documents_if_available"
    if kind in {"jsonl", "json", "csv", "parquet", "flat_data"}:
        return "classify_private_then_import_or_archive"
    if kind == "sqlite":
        return "manual_mapping_before_import"
    return "manual_review"


def inventory_file(path: Path, source: Path) -> dict[str, Any]:
    rel = str(path.relative_to(source))
    suffix = path.suffix.lower()
    lower_parts = [part.lower() for part in path.parts]
    secret_risk = any(h in part for h in SECRET_NAME_HINTS for part in lower_parts)
    stat = path.stat()
    kind = "flat_data"
    extra: dict[str, Any] = {}

    if is_sqlite(path):
        kind = "sqlite"
        extra["sqlite"] = sqlite_schema(path)
    elif suffix in {".jsonl", ".ndjson"}:
        kind = "jsonl"
        extra["line_count"] = count_lines(path)
    elif suffix == ".json":
        kind = "json"
    elif suffix in {".csv", ".tsv"}:
        kind = "csv"
        extra["line_count"] = count_lines(path)
    elif suffix == ".parquet":
        kind = "parquet"
    elif suffix == ".duckdb":
        kind = "duckdb"

    return {
        "path": rel,
        "kind": kind,
        "size_bytes": stat.st_size,
        "sha256_first_1mb": sha256_prefix(path),
        "secret_name_risk": secret_risk,
        "recommended_action": classify_action(path, kind, secret_risk),
        **extra,
    }


def walk(source: Path, max_files: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for dirpath, dirnames, filenames in os.walk(source):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        current = Path(dirpath)
        low_name = current.name.lower()
        if any(h == low_name or h in low_name for h in VECTOR_DIR_HINTS):
            out.append({
                "path": str(current.relative_to(source)),
                "kind": "vector_directory",
                "size_bytes": None,
                "secret_name_risk": any(h in str(current).lower() for h in SECRET_NAME_HINTS),
                "recommended_action": "rebuild_from_source_documents_if_available",
            })
        for name in filenames:
            p = current / name
            suffix = p.suffix.lower()
            if suffix in DB_SUFFIXES or suffix in DATA_SUFFIXES or is_sqlite(p):
                try:
                    out.append(inventory_file(p, source))
                except Exception as e:  # noqa: BLE001
                    out.append({
                        "path": str(p.relative_to(source)),
                        "kind": "unknown_error",
                        "error": f"{type(e).__name__}: {e}",
                        "recommended_action": "manual_review",
                    })
                if len(out) >= max_files:
                    return out
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="~/.openclaw", help="OpenClaw/source root to scan read-only")
    ap.add_argument("--out", default="database-inventory.json", help="Output JSON path")
    ap.add_argument("--max-files", type=int, default=5000)
    args = ap.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"source not found: {source}")
    items = walk(source, args.max_files)
    report = {
        "source": str(source),
        "mode": "read_only_schema_and_metadata_no_row_contents",
        "count": len(items),
        "items": items,
    }
    out = Path(args.out).expanduser()
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(out), "count": len(items)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
