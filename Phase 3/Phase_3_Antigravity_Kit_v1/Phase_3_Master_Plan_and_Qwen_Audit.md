# MISORA-EDITOR — PHASE 3 ANTIGRAVITY PROMPT ENGINEERING & SESSION SLICING (ROUND 1)

Author / Scribe: Gemini (Notulen)
Peer Evaluator: Qwen (sole active evaluator; GPT/Claude/Grok parked)
Locked Input Ledger: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`)
Pinned Baseline Commit: `683724edaf2afac89d2695a80e30a471a0da9195` (Misora-Editor `main`, v1.4.0)
Antigravity Reference Applied: `google_antigravity_ai_prompting_reference.md`, `ANTIGRAVITY_GUIDE.md`, `templates/ANTIGRAVITY_PROMPT_TEMPLATE.md`

======================================================================
1. ANTIGRAVITY ORCHESTRATION & MODEL-ROUTING STRATEGY
======================================================================
Project Lead's Antigravity Account Models:
- **Claude Opus 4.6** (Frontier deep reasoning)
- **Claude Sonnet 4.6** (Balanced frontier coding)
- **Gemini 3.8 Flash** (Fast / low-quota tier)
- **GPT-OSS 120B** (Low-cost open-weight model)

### A. Why Persistent Customizations Come First ("Don't Prompt It Twice — File It!")
Per `google_antigravity_ai_prompting_reference.md` §5, we separate permanent invariants from per-session prompts via 3 lightweight files in `setup_antigravity/` (copy into `D:\Misora-Editor\.agents\`):
1. `.agents/rules/misora-safety.md` — Valid snake_case YAML frontmatter (`trigger: always_on`, flat directory, <24 KB). Permanently locks non-negotiable guardrails (no destructive git, no test weakening, `cmd_id` 35/32 lock, no `.misora` drafts, no `AtlasAdv`, main-thread Tk only).
2. `.agents/skills/misora-verify/SKILL.md` — Invocable via **`/misora-verify`** for uniform Windows `py -3.12` verification + `backups/` cleanliness audit.
3. `.agents/hooks.json` + `.agents/hooks/guard_git.py` — Mechanical `PreToolUse` safety net on `run_command` that hard-blocks destructive git commands even if a cheaper model hallucinates a git reset/commit.

### B. Honest Model-Safety Verdict (Can Cheap Models Run These Prompts Safely?)
Strict failing-first TDD probes + explicit `@file` pointers + `PreToolUse` hooks dramatically reduce ambiguity, **but `misora.py` is 12,144 lines (~543 KB)** with subtle AST/Tkinter state coupling. Honest tier routing:
- **Tier 1 — SAFE for `Gemini 3.8 Flash` (Save Quota):** `S01` (docs/test isolation), `S09` (isolated `core/security.py`, `core/logger.py`, `assets/splash.py` — ideal `/swarm` with Flash workers + Sonnet 4.6 `@verifier`), `S11` (geometric Search/Toolbar layout + naming), `S12` (Select Box UI, left drawer, empty state, multi-open).
- **Tier 2 — HYBRID (`Claude Sonnet 4.6` for `/plan`, optional `Gemini 3.8 Flash` for execution):** `S10` (once the Implementation Plan specifies exact edit sites).
- **Tier 3 — REQUIRE `Claude Sonnet 4.6`:** `S04` (atomic CSIF + regex parity), `S05` (per-doc state + save integrity), `S06` (undo/lock atomicity), `S08` (immutable XUAT keys + main-thread MTL queue), `S13` (`.misora` v1 workspace), `S14` (pixel rulers + `wrap="none"` Preview), `S15` (editable `Raw Commands`), `S16` (2-widget MTL Drawer), `S17` (`Import from XUAT` + `core/xuat_index.py`).
- **Tier 4 — REQUIRE `Claude Opus 4.6` (+ `/boost` on Pro plan):** `S02` (binary parser + lossless v2 + cmd map/breakers + 35/32 guardrail), `S03` (AST kind-conversion separation + structural voice/breaker ownership + multi-seg undo), `S07` (search snapshots + bounded roots + multi-file bundle Replace-All & `BulkFileDelta` undo).
- **Role for `GPT-OSS 120B`:** Safe ONLY for `S01` docs reconciliation, small isolated fixes (`BUG-36` splash sort, `HYG-05` `Any` import, `HYG-06` DeepL UA), or as a **cheap cross-model `@verifier` / read-only diff auditor** inside `/swarm` — NOT recommended as sole editor of 12k-line `misora.py`.

### C. Native Antigravity Commands Utilized (Zero Deprecated Traps)
- `/plan` — Mandatory Planning-First Gate on EVERY session (`S01..S17`).
- `/boost` — Recommended after `Proceed` on high-risk sessions `S02`, `S03`, `S07` (and optionally `S17`).
- `/goal` — Optional after `Proceed` on `S01` (`tests/*.py` backup isolation sweep across 23 test files).
- `/swarm` — Optional on `S09` (exclusive ownership across `core/security.py`, `core/logger.py`, `assets/splash.py`, `misora.py` + cross-model `@verifier`). NEVER use `/swarm` with two workers editing `misora.py` simultaneously.
- `/misora-verify` — Custom skill invoked at end of every session.
- `/compact <focus>` — Leading token only whenever a session grows long.
- `/btw <question>` & `/learn` — For read-only side questions and distilling repeated corrections.
- Strictly avoids deprecated `/planning`, `/fast`, `--permission-mode`, nested rule directories, and camelCase YAML triggers.

======================================================================
2. 17-SESSION ROADMAP & 100% LEDGER COVERAGE TABLE (63 / 63 ITEMS)
======================================================================
| Session | Group / Gate | Canonical Ledger IDs Covered (Count) | Antigravity Command | Recommended Model | Target Test Suite |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S01** | Group A (DEP-10) | HYG-01, HYG-02 (2) | `/plan (then /goal after Proceed)` | Gemini 3.8 Flash (Plan + Execute) — SAFE for cheap model (zero production code edits) | `tests/test_p3_s01_hygiene_backup_isolation.py` |
| **S02** | Group B1 (DEP-5 part 1) | BUG-01, BUG-03, BUG-04, BUG-09 (4) | `/plan (review Plan Artifact) -> /boost (after Proceed)` | Claude Opus 4.6 (HIGH risk: binary format & v2 codec — DO NOT use Flash or GPT-OSS 120B) | `tests/test_p3_s02_ast_codec.py` |
| **S03** | Group B2 (DEP-5 part 2) | BUG-02, BUG-05, BUG-06, BUG-17, HYG-04 (5) | `/plan (review Plan Artifact) -> /boost (after Proceed)` | Claude Opus 4.6 (HIGH risk: AST structural mutations & undo integrity — DO NOT use Flash or GPT-OSS 120B) | `tests/test_p3_s03_ast_mutations.py` |
| **S04** | Group B3 (DEP-1) | BUG-07, BUG-08, BUG-31 (3) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 | `tests/test_p3_s04_csif_atomic.py` |
| **S05** | Group C1 (DEP-2, DEP-4) | BUG-11, BUG-12, BUG-18, BUG-19, BUG-20 (5) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 (Core document lifecycle & save safety) | `tests/test_p3_s05_doc_lifecycle_save.py` |
| **S06** | Group C2 (post-DEP-4) | BUG-10, BUG-13, BUG-15, BUG-16, BUG-37 (5) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 | `tests/test_p3_s06_undo_locks_raw.py` |
| **S07** | Group D (DEP-7 part 1) | BUG-21, BUG-22, BUG-23, BUG-24, HYG-05 (5) | `/plan (review Plan Artifact) -> /boost (after Proceed)` | Claude Opus 4.6 (HIGH risk: search threading, project root security, multi-file bundle Replace-All & BulkFileDelta undo) | `tests/test_p3_s07_search_replace.py` |
| **S08** | Group E + F1 (DEP-6, DEP-7) | BUG-14, BUG-25, BUG-26, BUG-27, HYG-06 (5) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 (Thread safety & XUAT sync integrity) | `tests/test_p3_s08_xuat_mtl_threading.py` |
| **S09** | Group F2 (DEP-9 part 1) | BUG-32, BUG-33, BUG-34, BUG-35, BUG-36 (5) | `/plan (or /swarm with exclusive file workers + cross-model @verifier)` | Gemini 3.8 Flash (workers on isolated files) + Claude Sonnet 4.6 (@verifier) — SAFE for cheap workers! | `tests/test_p3_s09_lifecycle_security.py` |
| **S10** | Final Stabilization Gate (DEP-3 — Completes ALL P0/P1 Bugs!) | BUG-28, BUG-29, BUG-30, HYG-03, HYG-07, HYG-08 (6) | `/plan (Claude Sonnet 4.6) -> Proceed (Sonnet 4.6 or Gemini 3.8 Flash)` | Claude Sonnet 4.6 (Plan) — optional Gemini 3.8 Flash for execution after reviewing Plan Artifact | `tests/test_p3_s10_editor_shortcuts_ribbon.py` |
| **S11** | Group G1 (UX Toolbar & Naming — post-DEP-3) | BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04 (6) | `/plan -> Proceed` | Gemini 3.8 Flash (SAFE! Unambiguous geometric & naming acceptance criteria) | `tests/test_p3_s11_toolbar_search_ui.py` |
| **S12** | Group G2 (post-DEP-4, DEP-9) | BUG-41, FEAT-05, FEAT-06, FEAT-07 (4) | `/plan -> Proceed` | Gemini 3.8 Flash (or Claude Sonnet 4.6 for Plan -> Flash for Execute) | `tests/test_p3_s12_selection_drawer_open.py` |
| **S13** | Group G3 (post-DEP-4, DEP-9) | FEAT-08 (1) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 | `tests/test_p3_s13_misora_workspace.py` |
| **S14** | Group G4 (post-DEP-2, DEP-8) | BUG-40, FEAT-09, FEAT-10 (3) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 (Tkinter font metrics, Canvas ruler & hybrid Preview rendering) | `tests/test_p3_s14_rulers_preview.py` |
| **S15** | Group G5 (post-DEP-5) | FEAT-11 (1) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 | `tests/test_p3_s15_raw_commands_edit.py` |
| **S16** | Group G6 (post-DEP-6) | FEAT-12, FEAT-13 (2) | `/plan (review Plan Artifact) -> Proceed` | Claude Sonnet 4.6 | `tests/test_p3_s16_mtl_drawer.py` |
| **S17** | Group G7 (Final Cycle Deliverable — post-DEP-2, DEP-7) | FEAT-14 (1) | `/plan (review Plan Artifact) -> /boost (or Sonnet 4.6 Proceed)` | Claude Sonnet 4.6 (or Opus 4.6 for Plan/Verify — flagship translator workflow feature) | `tests/test_p3_s17_import_xuat.py` |

### Dependency Order Verification (`DEP-1`..`DEP-10` — 100% Satisfied)
- **DEP-10:** `HYG-01` lands first in `S01` (zero production code edits).
- **DEP-5:** `BUG-01..BUG-06` complete in `S02..S03`, strictly before `FEAT-11` (`S15`).
- **DEP-1:** `BUG-31` (`Treeview` dark-theme contrast) completes in `S04`, before all later UI sessions.
- **DEP-2:** `BUG-11` (plain-text Preview save) completes in `S05`, strictly before `FEAT-10` (`S14`) and `FEAT-14` (`S17`).
- **DEP-4:** `BUG-12` (per-doc state & stable locks) completes in `S05`, strictly before `BUG-15`/`BUG-16` (`S06`), `BUG-24` (`S07`), `FEAT-05` (`S12`), and `FEAT-08` (`S13`).
- **DEP-7:** `BUG-23` (bounded project roots, `S07`) and `BUG-25` (immutable JP keys, `S08`) complete strictly before `FEAT-14` (`S17`).
- **DEP-6:** `BUG-14` & `BUG-27` (`S08`) + `HYG-01` (`S01`) complete strictly before `FEAT-12`/`FEAT-13` (`S16`).
- **DEP-3:** `BUG-28` & `HYG-03` (`S10`) complete strictly before `FEAT-02`/`FEAT-04` (`S11`).
- **DEP-9:** `BUG-35` (`S09`) and `FEAT-07` (`S12`) complete strictly before `FEAT-08` (`S13`).
- **DEP-8:** Shared pixel-measure helper ships together with `BUG-40`/`FEAT-09`/`FEAT-10` in `S14` (and is reused by `FEAT-14` in `S17`).
- **Track 1 Stabilization Gate:** ALL 37 core bugs (`BUG-01..BUG-37`) and ALL 8 hygiene items (`HYG-01..HYG-08`) complete in `S01..S10` BEFORE Track 2 UX/Feature slices (`S11..S17`) begin.

### Complete 1:1 Traceability Map (Every Active Phase 2.5 ID -> Exactly 1 Session)
| Ledger ID | Session |
| :--- | :--- |
| HYG-01 | **S01** |
| HYG-02 | **S01** |
| HYG-03 | **S10** |
| HYG-04 | **S03** |
| HYG-05 | **S07** |
| HYG-06 | **S08** |
| HYG-07 | **S10** |
| HYG-08 | **S10** |
| BUG-01 | **S02** |
| BUG-02 | **S03** |
| BUG-03 | **S02** |
| BUG-04 | **S02** |
| BUG-05 | **S03** |
| BUG-06 | **S03** |
| BUG-07 | **S04** |
| BUG-08 | **S04** |
| BUG-09 | **S02** |
| BUG-10 | **S06** |
| BUG-11 | **S05** |
| BUG-12 | **S05** |
| BUG-13 | **S06** |
| BUG-14 | **S08** |
| BUG-15 | **S06** |
| BUG-16 | **S06** |
| BUG-17 | **S03** |
| BUG-18 | **S05** |
| BUG-19 | **S05** |
| BUG-20 | **S05** |
| BUG-21 | **S07** |
| BUG-22 | **S07** |
| BUG-23 | **S07** |
| BUG-24 | **S07** |
| BUG-25 | **S08** |
| BUG-26 | **S08** |
| BUG-27 | **S08** |
| BUG-28 | **S10** |
| BUG-29 | **S10** |
| BUG-30 | **S10** |
| BUG-31 | **S04** |
| BUG-32 | **S09** |
| BUG-33 | **S09** |
| BUG-34 | **S09** |
| BUG-35 | **S09** |
| BUG-36 | **S09** |
| BUG-37 | **S06** |
| BUG-38 | **S11** |
| BUG-39 | **S11** |
| BUG-40 | **S14** |
| BUG-41 | **S12** |
| FEAT-01 | **S11** |
| FEAT-02 | **S11** |
| FEAT-03 | **S11** |
| FEAT-04 | **S11** |
| FEAT-05 | **S12** |
| FEAT-06 | **S12** |
| FEAT-07 | **S12** |
| FEAT-08 | **S13** |
| FEAT-09 | **S14** |
| FEAT-10 | **S14** |
| FEAT-11 | **S15** |
| FEAT-12 | **S16** |
| FEAT-13 | **S16** |
| FEAT-14 | **S17** |

Total Mapped: **63 / 63** (`BUG`: 41, `FEAT`: 14, `HYG`: 8). Duplicates: **0**. Omissions: **0**.
Excluded by Lock: `DEF-01..DEF-10` (10 deferred), `NO-01..NO-12` (12 rejected/non-goals).

======================================================================
3. PEER AUDIT REQUEST FOR QWEN (PHASE 3 ROUND 1)
======================================================================
Qwen (sole active evaluator), please audit this Phase 3 package (`Phase_3_Master_Plan_and_Qwen_Audit.md`, `setup_antigravity/*`, and `prompts/S01..S17`) against `Phase_2.5_Canonical_Ledger_LOCKED.md`, `ANTIGRAVITY_GUIDE.md`, and `google_antigravity_ai_prompting_reference.md`:
1. Confirm **100% coverage** of all 63 active IDs (`BUG-01..41`, `FEAT-01..14`, `HYG-01..08`) with zero dropped acceptance criteria or guardrails.
2. Check for any hidden **dependency inversions**, **file-ownership conflicts**, or **Regression Guards that accidentally reference post-patch attributes**.
3. Check `.agents/rules/misora-safety.md`, `.agents/skills/misora-verify/SKILL.md`, and `.agents/hooks.json` for strict compliance with `google_antigravity_ai_prompting_reference.md` (valid frontmatter, no deprecated commands, Windows `py -3.12` safety).
4. Review the **Model-Routing Matrix** (`Gemini 3.8 Flash` vs `Claude Sonnet 4.6` vs `Claude Opus 4.6` vs `GPT-OSS 120B`) and flag any session where a cheaper model is too risky or where a split can be tightened further.

Respond with `PHASE 3 STATUS: APPROVED & IDENTICAL` or `PHASE 3 STATUS: OPEN — DEBATING PLAN/PROMPTS` with exact diffs.

PHASE 3 STATUS: OPEN — DEBATING PLAN/PROMPTS (GEMINI ROUND 1 DRAFT READY FOR QWEN AUDIT)
