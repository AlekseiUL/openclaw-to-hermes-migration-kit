#!/usr/bin/env python3
"""Scan for active pointers to old roots.
Allows legacy/provenance paths by default, reports severity.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

FORBIDDEN = [
    "<old-external-wiki-root>",
    "<old-external-references-root>",
    "<old-external-project-root>",
    "~/.openclaw",
    "~/.openclaw",
]
ALLOW_HINTS = ["legacy-openclaw", "quarantine", "migration", "provenance", "forbidden", "do not use", "source-only", "boundary", "read-only", "metadata-only", "schema only", "example", "examples", "template", "research", "source root", "default `~/.openclaw`", "--source ~/.openclaw", "openclaw_hermes_audit.py", "database_inventory.py", "где найден", "где был найден", "source_file"]
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}


def iter_files(path: Path):
    if path.is_file():
        yield path
    else:
        for p in path.rglob('*'):
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            if p.is_file():
                yield p


def classify(file: Path, line: str) -> str:
    blob = (str(file) + ' ' + line).lower()
    if any(h in blob for h in ALLOW_HINTS):
        return 'allowed-provenance-or-guard'
    if any(k in blob for k in ['source ', 'bash ', 'python ', '.env', 'config.yaml', 'soul.md', 'skill.md', 'cron', 'gateway', 'token']):
        return 'active-risk'
    return 'needs-review'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', required=True)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    root = Path(args.path).expanduser()
    findings = []
    for f in iter_files(root):
        try:
            text = f.read_text(errors='replace')
        except Exception:
            continue
        for ln, line in enumerate(text.splitlines(), 1):
            if any(s in line for s in FORBIDDEN):
                findings.append({"file": str(f), "line": ln, "severity": classify(f, line), "text": line.strip()[:240]})
    data = {"findings": findings, "count": len(findings), "active_risk_count": sum(x['severity']=='active-risk' for x in findings)}
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for x in findings:
            print(f"{x['severity']} {x['file']}:{x['line']} {x['text']}")
        print(f"findings={data['count']} active_risk={data['active_risk_count']}")
    return 1 if data['active_risk_count'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
