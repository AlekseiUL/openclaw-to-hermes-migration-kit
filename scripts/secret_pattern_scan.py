#!/usr/bin/env python3
"""Pattern-based secret scanner for generated migration artifacts.
Prints paths/lines/pattern names, never full matched values.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

PATTERNS = {
    "openai_api_key": re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "telegram_bot_token": re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{25,}\b"),
    "generic_secret_assignment": re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*=\s*['\"]?[^\s'\"]{16,}"),
}
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}


def iter_files(path: Path):
    if path.is_file():
        yield path
        return
    for p in path.rglob('*'):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            yield p


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
            for name, rx in PATTERNS.items():
                if rx.search(line):
                    findings.append({"file": str(f), "line": ln, "pattern": name, "preview": line[:80].replace(rx.search(line).group(0), "[REDACTED_MATCH]") if rx.search(line) else line[:80]})
    if args.json:
        print(json.dumps({"findings": findings, "count": len(findings)}, ensure_ascii=False, indent=2))
    else:
        for x in findings:
            print(f"{x['file']}:{x['line']} {x['pattern']} {x['preview']}")
        print(f"findings={len(findings)}")
    return 1 if findings else 0

if __name__ == '__main__':
    raise SystemExit(main())
