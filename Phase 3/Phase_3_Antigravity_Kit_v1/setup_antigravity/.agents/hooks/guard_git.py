#!/usr/bin/env python3
"""Antigravity PreToolUse safety hook: blocks destructive git commands on run_command."""
import json
import re
import sys

BLOCKED_PATTERNS = [
    r"\bgit\s+reset\b",
    r"\bgit\s+clean\b",
    r"\bgit\s+stash\b",
    r"\bgit\s+push\b",
    r"\bgit\s+commit\b",
    r"\bgit\s+checkout\s+--\b",
    r"\bgit\s+restore\b",
]

def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return

    tool_input = payload.get("tool_input") or payload.get("input") or {}
    cmd = str(tool_input.get("command") or tool_input.get("CommandLine") or "")

    for pat in BLOCKED_PATTERNS:
        if re.search(pat, cmd, re.IGNORECASE):
            print(json.dumps({
                "decision": "deny",
                "reason": f"Blocked by Misora safety hook: destructive or user-controlled git command matched `{pat}`. The Project Lead runs git commits/resets manually."
            }))
            return

    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
