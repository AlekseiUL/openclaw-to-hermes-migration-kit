#!/usr/bin/env python3
"""Read-only OpenClaw -> Hermes migration audit.

Does not print secret values. Produces JSON inventory.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path
from typing import Any

SECRET_NAME_RE = re.compile(r"(TOKEN|KEY|SECRET|PASSWORD|AUTH|COOKIE|SESSION)", re.I)
ROLE_NAMES = {"AGENTS.md", "SOUL.md", "IDENTITY.md", "MEMORY.md", "TOOLS.md", "RoleBrief.md", "README.md"}
STORAGE_SUFFIXES = {'.db', '.sqlite', '.sqlite3', '.duckdb', '.jsonl', '.ndjson', '.csv', '.tsv', '.parquet', '.feather'}
STORAGE_HINTS = {'memory', 'session', 'vector', 'embedding', 'chroma', 'faiss', 'lancedb', 'qdrant'}


def mask_value(v: str) -> dict[str, Any]:
    s = v.strip().strip('"').strip("'")
    if not s:
        return {"present": False, "length": 0, "value": ""}
    return {"present": True, "length": len(s), "value": "[REDACTED]"}


def read_env_keys(path: Path) -> list[dict[str, Any]]:
    out = []
    if not path.exists() or not path.is_file():
        return out
    for i, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or '=' not in stripped:
            continue
        k, v = stripped.split('=', 1)
        item = {"name": k.strip(), "line": i, "secret_like": bool(SECRET_NAME_RE.search(k))}
        item.update(mask_value(v))
        out.append(item)
    return out


def safe_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(errors="replace"))
    except Exception as e:
        return {"_error": str(e)}


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    n = 0
    for p in path.rglob('*'):
        try:
            if p.is_file():
                n += 1
        except OSError:
            pass
    return n


def list_names(path: Path, limit: int = 200) -> list[str]:
    if not path.exists() or not path.is_dir():
        return []
    names = []
    for p in sorted(path.iterdir(), key=lambda x: x.name.lower()):
        names.append(p.name + ('/' if p.is_dir() else ''))
        if len(names) >= limit:
            names.append(f"... truncated at {limit}")
            break
    return names


def agent_inventory(agent_dir: Path) -> dict[str, Any]:
    agent_id = agent_dir.name
    agent_home = agent_dir / 'agent'
    sessions = agent_dir / 'sessions'
    role_files = []
    memory_files = []
    tools_or_scripts = []
    skills = []
    storage_candidates = []
    provider_auth = []
    telegram_env_keys = []

    for base in [agent_home, agent_dir]:
        if not base.exists():
            continue
        for p in base.rglob('*'):
            try:
                if not p.is_file():
                    continue
            except OSError:
                continue
            rel = str(p.relative_to(agent_dir))
            if p.name in ROLE_NAMES:
                role_files.append(rel)
            if 'memory' in p.name.lower() or 'memory' in rel.lower():
                memory_files.append(rel)
            if p.suffix in {'.py', '.sh', '.js', '.ts'} or 'tools' in rel.lower():
                tools_or_scripts.append(rel)
            low_rel = rel.lower()
            if p.suffix.lower() in STORAGE_SUFFIXES or any(h in low_rel for h in STORAGE_HINTS):
                storage_candidates.append({"path": rel, "size_bytes": p.stat().st_size})
            if p.name in {'auth-state.json', 'auth-profiles.json'}:
                provider_auth.append(rel)
            if p.name == '.env':
                for item in read_env_keys(p):
                    if 'TELEGRAM' in item['name'].upper():
                        telegram_env_keys.append({"file": rel, **item})
        for sdir in [base/'skills', base/'skill', base/'shared'/'skills']:
            if sdir.exists() and sdir.is_dir():
                skills.extend([str(x.relative_to(agent_dir)) for x in sdir.iterdir() if x.is_dir() or x.is_file()])

    return {
        "agent_id": agent_id,
        "agent_dir": str(agent_dir),
        "agent_home_exists": agent_home.exists(),
        "role_files": sorted(set(role_files))[:200],
        "memory_files": sorted(set(memory_files))[:200],
        "sessions_dir_exists": sessions.exists(),
        "sessions_count": count_files(sessions),
        "skills": sorted(set(skills))[:200],
        "tools_or_scripts": sorted(set(tools_or_scripts))[:200],
        "storage_candidates": sorted(storage_candidates, key=lambda x: x['path'])[:300],
        "provider_auth_files_present": sorted(set(provider_auth)),
        "telegram_env_keys": telegram_env_keys,
        "top_level": list_names(agent_dir, 80),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default='~/.openclaw', help='OpenClaw root')
    ap.add_argument('--out', help='Write JSON output to file')
    ap.add_argument('--pretty', action='store_true', help='Pretty-print summary to stderr')
    args = ap.parse_args()

    src = Path(args.source).expanduser().resolve()
    agents_root = src / 'agents'
    inventory = {
        "source_root": str(src),
        "exists": src.exists(),
        "openclaw_json_exists": (src/'openclaw.json').exists(),
        "env_keys": read_env_keys(src/'.env'),
        "cron_files_present": [str(p.relative_to(src)) for p in [src/'cron'/'jobs.json', src/'cron.json', src/'jobs.json'] if p.exists()],
        "agents_root_exists": agents_root.exists(),
        "agents": [],
        "warnings": [],
    }
    if not src.exists():
        inventory["warnings"].append("source root not found")
    if agents_root.exists():
        for d in sorted([p for p in agents_root.iterdir() if p.is_dir()], key=lambda x: x.name.lower()):
            inventory["agents"].append(agent_inventory(d))
    txt = json.dumps(inventory, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).expanduser().write_text(txt, encoding='utf-8')
    else:
        print(txt)
    if args.pretty:
        print(f"source={src} agents={len(inventory['agents'])}", file=sys.stderr)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
