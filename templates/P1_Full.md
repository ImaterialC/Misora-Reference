PHASE 1 — INDEPENDENT AUDIT (NO ANTIGRAVITY PROMPTS YET)

Repo: `[REPO_URL]` @ `[40_CHAR_SHA]` (`[VERSION]`)
Refs/Wishlist: `[URLS_FROM_scan_meeting.bat]`
ID Prefix: `[AI-B01..]` bugs, `[AI-F01..]` features, `[AI-E01..]` hygiene, `[AI-Q01..]` questions.

Rules:
- Cite `file -> symbol (ORIG lines X-Y)` strictly from read code (use original line numbers if reading split parts).
- Tag every claim `[CONFIRMED]` or `[NEEDS-VERIFY]`. Never invent unread files.
- Trace 100% of `U-01..U-N` (`ACCEPT|REFINE|DEFER|REJECT`) and obey `AGENTS.md`.
- Prioritize: data loss, encoding/atomicity, locks, async/threading races, state desync, brittle tests, `DEP` edges.

Output (Markdown, concise):
1. Baseline & docs/code drift.
2. Bugs (`[AI-Bxx]`): Sev (`P0/P1/P2`), Tag, Location, Mechanism, Minimal Fix + Test.
3. Wishlist (`U-xx` -> `[AI-Fxx]`): Decision, Touchpoints, Deps, Guardrails.
4. Hygiene/Ref Traps (`[AI-Exx]`) + Dependency order (`DEP`).
5. Open Questions (`[AI-Qxx]`) with safe default.
End: `PHASE 1: COMPLETE`
