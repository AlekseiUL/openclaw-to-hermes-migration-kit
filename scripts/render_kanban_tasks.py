#!/usr/bin/env python3
"""Render Hermes Kanban commands for a migration.

Default mode is safe for a subscriber with only one Hermes profile: all cards are
assigned to --profile. If a team exists, pass explicit worker profile names.
"""
from __future__ import annotations
import argparse
import shlex

TASKS = [
    ("researcher", "external research", "Read-only external/source research. No secrets. Output source ledger."),
    ("technical", "technical audit", "Read-only audit of source/target dependency classes, scripts, tools, cron, storage and gateway risks."),
    ("privacy", "privacy and approval gate", "Review secrets/private/client/finance/psychological data risks and approval gates."),
    ("implementation", "build migration artifacts", "Build/adapt scripts/templates after parent findings. Dry-run only unless approved."),
    ("final", "final synthesis", "Collect parent results, verify artifacts and report final status."),
]


def q(s: str) -> str:
    return shlex.quote(s)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True)
    ap.add_argument("--profile", required=True, help="Target Hermes profile; also default assignee for all cards")
    ap.add_argument("--board", default="migration")
    ap.add_argument("--dispatcher-profile", help="Profile that creates Kanban cards; default: --profile")
    ap.add_argument("--researcher-profile")
    ap.add_argument("--technical-profile")
    ap.add_argument("--privacy-profile")
    ap.add_argument("--implementation-profile")
    ap.add_argument("--final-profile")
    args = ap.parse_args()

    dispatcher = args.dispatcher_profile or args.profile
    assignees = {
        "researcher": args.researcher_profile or args.profile,
        "technical": args.technical_profile or args.profile,
        "privacy": args.privacy_profile or args.profile,
        "implementation": args.implementation_profile or args.profile,
        "final": args.final_profile or args.profile,
    }

    print(f"# Kanban commands for {args.agent} -> {args.profile}")
    print("# Safe default: all cards assigned to the target profile unless worker profiles were passed.")
    prev_ids: list[int] = []
    for i, (role, title, body) in enumerate(TASKS, 1):
        assignee = assignees[role]
        full_title = f"OpenClaw→Hermes {args.agent}: {title}"
        full_body = (
            f"Agent: {args.agent}\n"
            f"Target profile: {args.profile}\n"
            "Policy: read-only/dry-run unless explicit approval.\n"
            f"{body}"
        )
        parents = "".join(f" --parent <TASK_{j}_ID>" for j in prev_ids) if role in {"implementation", "final"} else ""
        print(
            f"hermes --profile {q(dispatcher)} kanban --board {q(args.board)} create "
            f"{q(full_title)} --assignee {q(assignee)} --workspace scratch --max-runtime 45m{parents} --body {q(full_body)}"
        )
        if role in {"researcher", "technical", "privacy"}:
            prev_ids.append(i)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
