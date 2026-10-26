#!/usr/bin/env python3
"""Generate a proposed Hermes profile/workspace skeleton.
Default is dry-run; --apply writes only non-secret scaffold files.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--agent', required=True)
    ap.add_argument('--profile', required=True)
    ap.add_argument('--workspace-root', default='<target-workspace>/agents')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true')
    mode.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    for value in [args.agent, args.profile]:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', value):
            ap.error('agent and profile must be simple names, not paths')
    home = Path(args.workspace_root).expanduser() / args.agent
    profile = Path.home() / '.hermes' / 'profiles' / args.profile
    files = {
        str(home/'RoleBrief.md'): f"# {args.agent} role brief\n\nTODO: migrated role summary.\n",
        str(home/'migration'/'profile-mapping.yaml'): f"source_agent: {args.agent}\ntarget_profile: {args.profile}\nmode: dry-run\n",
        str(home/'reports'/'migration-plan.md'): f"# Migration plan for {args.agent}\n\nStatus: draft. No secrets copied.\n",
        str(home/'sessions'/'legacy-openclaw'/'README.md'): "# Legacy OpenClaw sessions\n\nArchive only. Do not index raw private sessions by default.\n",
    }
    plan = {"agent": args.agent, "profile": args.profile, "workspace": str(home), "profile_path": str(profile), "files": list(files)}
    if args.apply:
        for path, content in files.items():
            p = Path(path)
            if p.is_symlink() or any(parent.is_symlink() for parent in p.parents):
                ap.error('symlink destination refused')
            p.parent.mkdir(parents=True, exist_ok=True)
            try:
                with p.open('x', encoding='utf-8') as output:
                    output.write(content)
            except FileExistsError:
                pass
        plan['applied'] = True
    else:
        plan['applied'] = False
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
