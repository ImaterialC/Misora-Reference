# MISORA-EDITOR — PHASE 3 UNIFIED ANTIGRAVITY KIT v2 (REVISION FOR ROUND 3 AUDIT)

Compiler / Scribe: Gemini (accepted sole-compiler role after Qwen & Grok conceded authorship to corrector roles)
Correctors / Auditors: Qwen (byte/ID/probe audit), Grok (byte/ID/probe/guard audit), GPT (acceptance session & command routing audit)
Locked Input Ledger: `Phase_2.5_Canonical_Ledger_LOCKED.md` (SHA-256 `73d79e00770ead5964ebf3cab3095cf1e45f1447576865b73838dd127eaf35cd`, git blob `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`)
Initial Starting Baseline (S01 only): `683724edaf2afac89d2695a80e30a471a0da9195` (Misora-Editor `main`, v1.4.0)

======================================================================
1. ALL PEER CORRECTIONS APPLIED IN v2 (ZERO DEFENSIVENESS CHECKLIST)
======================================================================
1. **Removed unverified `guard_git.py` & `hooks.json` (Qwen R1 #1, Grok R1 #5 & R2 #3, GPT R1 Critical):** Do NOT ship a fail-open hook with unverified stdin schema or broken `checkout --\b` regex. Rely on `.agents/rules/misora-safety.md` (`trigger: always_on`) + explicit `/agy-customizations` bootstrap in `OPERATOR_GUIDE.md`.
2. **Line 1 Column 1 = `/plan` on EVERY prompt (`S01..S24`) (Grok R2, Gemini self-audit):** Removed all HTML wrapper comments above `/plan` so full-file `Ctrl+A` paste always triggers `/plan` cleanly.
3. **Topic-safe `AGENTS.md` edits in `S01` (Grok R1 #1 & R2):** Preserves `## 19. NGUI single source` heading and lines 110–112 intact (amends only length-counter bullet line 113); adds exact overflow rule **50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)** under `UI safety` (never shorthand `"50x3"`); amends `CSIF rules` (§20) future-format wording; updates `Scope discipline` (§24); updates ONLY `Ctrl+H` in §29 while keeping Ribbon Cut & Paste Box blockers intact.
4. **Clean 24-session split (`S01..S23` + `S24` Final Acceptance & Release) (Qwen + Grok R2 + GPT):**
   - `S01` strictly docs-only (`HYG-01` + `CHANGELOG.md` init); `S02` immediately isolates `tests/` `backups/` (`HYG-02` + `HYG-05` + `HYG-06` reading `__version__` without bumping).
   - `S05` puts **`BUG-31` (`DEP-1` Treeview theme) strictly FIRST** before `BUG-07` (`ScriptPastePreviewDialog`) (GPT R1 High Priority, Grok R2).
   - Split XUAT (`S10`: `BUG-25`, `BUG-26`) from MTL threading (`S11`: `BUG-14`, `BUG-27`) (Grok R1 #3).
   - Split Lifecycle/DPAPI (`S12`: `BUG-32..36`) from Ribbon/Shortcuts/Tooltips (`S13`: `BUG-28`, `BUG-29`, `HYG-03`, `HYG-07`) (Grok R2 #2).
   - Split Search (`S08`) from Replace-All/Backups (`S09`), Rulers (`S17`) from Preview (`S18`), and MTL Dialogue (`S20`) from MTL All Script (`S21`).
   - Standalone final grep-proven dead-code session `S23` (`HYG-08`) AFTER all features settle (Grok R1 #2 & R2 #2).
   - Added dedicated **`S24` Final Acceptance Audit & Single `v1.4.1` Release Stamp** (GPT `08_FINAL_ACCEPTANCE_AUDIT` + Project Lead Changelog/Version contract).
5. **Honest Probes vs Guards & Fixture Rules (Qwen R1 #2-#4, Grok R2 #4, GPT R1):**
   - Moved `cmd_id 35/32` survival and existing `cmd_id 10/12` behavior strictly into **Regression Guards** in `S03` (NOT Defect Probes!).
   - `BUG-09` uses a deterministic **synthetic** multi-object UnityPy probe; real production compatibility stays explicitly `BLOCKED` if no real `.unity3d` fixture exists locally.
   - Zero hardcoded test counts (`20 tests`, etc.); always assert observed discovery count with `Ran 0 tests` = FAIL.
   - Added symbol-binding anti-line-rot rule + `ALREADY PASSING / NOT REPRODUCED` STOP rule to every prompt.
   - Clarified `683724e` is the S01 baseline only; `S02..S24` expect the accepted tree from prior sessions.
6. **Dropped parallel-editing `/swarm` on `S12` (GPT R1, Grok R2):** `/swarm` is strictly **READ-ONLY cross-model audit** (optional after Track 1 `S13` and Track 2 `S23`), using `GPT-OSS 120B` / `Gemini 3.8 Flash` as read-only auditors and `Claude Sonnet 4.6` as lead verifier.
7. **Fixed `/misora-verify` Skill & `.agents/` Merge Safety (GPT R1, Grok R2):** Skill takes the exact test module argument (zero placeholder execution, `Ran 0 tests` = FAIL); `OPERATOR_GUIDE.md` requires inspecting & merging `.agents/` rather than blind overwrite.
8. **Project Lead Changelog & Single `v1.4.1` Bump Contract (Lead + Grok R2):** Every session `S01..S23` appends `### SXX` under `## [Unreleased] (Target: v1.4.1)` in `CHANGELOG.md`; `__version__` stays `'1.4.0'` until `S24` bumps it ONCE to `'1.4.1'`.
9. **Honest Flash Routing (Grok R1 #4 & R2):** `S14` (`FEAT-04`) and `S15` are planned by **Claude Sonnet 4.6**; `Gemini 3.8 Flash` may execute ONLY after an approved line-anchored plan.

======================================================================
2. UNIFIED 24-SESSION ROADMAP (100% COVERAGE: 63 / 63 ACTIVE IDs + S24 AUDIT)
======================================================================
| Session | Track / Group | Canonical Ledger IDs | Recommended Model | Target Test Module |
| :--- | :--- | :--- | :--- | :--- |
| **S01** | Track 1 · Group A (DEP-10) | HYG-01 (1) | Gemini 3.8 Flash (Plan + Execute) — SAFE (0 Python code edits) | `(docs-only; full discover)` |
| **S02** | Track 1 · Group A | HYG-02, HYG-05, HYG-06 (3) | Gemini 3.8 Flash (Plan + Execute) — SAFE (mechanical, cleanly bounded) | `tests.test_p3_s02_hygiene` |
| **S03** | Track 1 · Group B1 (DEP-5 part 1) | BUG-01, BUG-03, BUG-04, BUG-09 (4) | Claude Opus 4.6 (HIGH RISK — binary & v2 codec; optional `/boost` after `Proceed`) | `tests.test_p3_s03_binary_v2` |
| **S04** | Track 1 · Group B2 (DEP-5 part 2) | BUG-02, BUG-05, BUG-06, BUG-17, HYG-04 (5) | Claude Opus 4.6 (HIGH RISK — AST structural mutations & undo; optional `/boost` after `Proceed`) | `tests.test_p3_s04_ast_mutations` |
| **S05** | Track 1 · Group B3 (DEP-1 STRICTLY FIRST) | BUG-31, BUG-07, BUG-08 (3) | Claude Sonnet 4.6 | `tests.test_p3_s05_treeview_csif` |
| **S06** | Track 1 · Group C1 (DEP-2, DEP-4) | BUG-11, BUG-12, BUG-18, BUG-19 (4) | Claude Sonnet 4.6 | `tests.test_p3_s06_doc_state_save` |
| **S07** | Track 1 · Group C2 (post-DEP-4) | BUG-10, BUG-13, BUG-15, BUG-16, BUG-37 (5) | Claude Sonnet 4.6 | `tests.test_p3_s07_undo_locks_raw` |
| **S08** | Track 1 · Group D1 (DEP-7 part 1) | BUG-21, BUG-22, BUG-23, BUG-30 (4) | Claude Sonnet 4.6 | `tests.test_p3_s08_search_roots_focus` |
| **S09** | Track 1 · Group D2 | BUG-24, BUG-20 (2) | Claude Opus 4.6 (HIGH RISK — multi-file bundle Replace-All & BulkFileDelta undo; optional `/boost` after `Proceed`) | `tests.test_p3_s09_replace_all_backups` |
| **S10** | Track 1 · Group E (DEP-7 part 2 — Split from MTL per Grok R1) | BUG-25, BUG-26 (2) | Claude Sonnet 4.6 | `tests.test_p3_s10_xuat_integrity` |
| **S11** | Track 1 · Group F1 (DEP-6 — Split from XUAT per Grok R1) | BUG-14, BUG-27 (2) | Claude Opus 4.6 (HIGH RISK — threading & queue races; optional `/boost` after `Proceed`) | `tests.test_p3_s11_mtl_threading` |
| **S12** | Track 1 · Group F2 (DEP-9 part 1 — Split from Ribbon per Grok R2) | BUG-32, BUG-33, BUG-34, BUG-35, BUG-36 (5) | Claude Sonnet 4.6 (sequential `/plan` — NO parallel-editing `/swarm`!) | `tests.test_p3_s12_lifecycle_security` |
| **S13** | Track 1 · Group F3 (DEP-3 — Completes ALL Track 1 P0/P1 Bugs!) | BUG-28, BUG-29, HYG-03, HYG-07 (4) | Claude Sonnet 4.6 | `tests.test_p3_s13_ribbon_shortcuts` |
| **S14** | Track 2 · Group G1 (post-DEP-3) | BUG-38, BUG-39, FEAT-01, FEAT-02, FEAT-03, FEAT-04 (6) | Claude Sonnet 4.6 (Plan — REQUIRED; Flash may execute ONLY after approved line-anchored Plan per Grok R1/R2) | `tests.test_p3_s14_toolbar_search_ui` |
| **S15** | Track 2 · Group G2 (post-DEP-4, DEP-9) | BUG-41, FEAT-05, FEAT-06, FEAT-07 (4) | Claude Sonnet 4.6 (Plan — REQUIRED; Flash may execute ONLY after approved line-anchored Plan) | `tests.test_p3_s15_selection_drawer_open` |
| **S16** | Track 2 · Group G3 (post-DEP-4, DEP-9) | FEAT-08 (1) | Claude Sonnet 4.6 | `tests.test_p3_s16_misora_workspace` |
| **S17** | Track 2 · Group G4a (DEP-8 — Split from Preview per Grok/Gemini R2) | BUG-40, FEAT-09 (2) | Claude Sonnet 4.6 | `tests.test_p3_s17_pixel_rulers` |
| **S18** | Track 2 · Group G4b (post-DEP-2, DEP-8) | FEAT-10 (1) | Claude Sonnet 4.6 | `tests.test_p3_s18_game_preview` |
| **S19** | Track 2 · Group G5 (post-DEP-5) | FEAT-11 (1) | Claude Opus 4.6 / Claude Sonnet 4.6 | `tests.test_p3_s19_raw_commands_edit` |
| **S20** | Track 2 · Group G6a (post-DEP-6 — Split from All Script per Grok R1) | FEAT-12 (1) | Claude Sonnet 4.6 | `tests.test_p3_s20_mtl_drawer_dialogue` |
| **S21** | Track 2 · Group G6b (post-S20) | FEAT-13 (1) | Claude Sonnet 4.6 | `tests.test_p3_s21_mtl_drawer_all_script` |
| **S22** | Track 2 · Group G7 (post-DEP-2, DEP-7) | FEAT-14 (1) | Claude Opus 4.6 (HIGH complexity flagship workflow; optional `/boost` after `Proceed`) | `tests.test_p3_s22_import_xuat` |
| **S23** | Track 2 · Final Hygiene (`HYG-08` — Standalone per Grok R1/R2) | HYG-08 (1) | Claude Sonnet 4.6 (Plan) — Flash OK post-Proceed | `tests.test_p3_s23_dead_code_cleanup` |
| **S24** | Release Gate (GPT `08_FINAL_ACCEPTANCE_AUDIT` + Lead `v1.4.1` Changelog Contract) | Audit ALL 63 + v1.4.1 | Claude Opus 4.6 (Lead Auditor) + optional Read-Only `/swarm` with GPT-OSS 120B adversarial reviewer | `tests.test_p3_s24_release_version` |

### Complete 1:1 Traceability Map (63 / 63 Active IDs — Zero Duplicates, Zero Omissions)
| Ledger ID | Session |
| :--- | :--- |
| HYG-01 | **S01** |
| HYG-02 | **S02** |
| HYG-03 | **S13** |
| HYG-04 | **S04** |
| HYG-05 | **S02** |
| HYG-06 | **S02** |
| HYG-07 | **S13** |
| HYG-08 | **S23** |
| BUG-01 | **S03** |
| BUG-02 | **S04** |
| BUG-03 | **S03** |
| BUG-04 | **S03** |
| BUG-05 | **S04** |
| BUG-06 | **S04** |
| BUG-07 | **S05** |
| BUG-08 | **S05** |
| BUG-09 | **S03** |
| BUG-10 | **S07** |
| BUG-11 | **S06** |
| BUG-12 | **S06** |
| BUG-13 | **S07** |
| BUG-14 | **S11** |
| BUG-15 | **S07** |
| BUG-16 | **S07** |
| BUG-17 | **S04** |
| BUG-18 | **S06** |
| BUG-19 | **S06** |
| BUG-20 | **S09** |
| BUG-21 | **S08** |
| BUG-22 | **S08** |
| BUG-23 | **S08** |
| BUG-24 | **S09** |
| BUG-25 | **S10** |
| BUG-26 | **S10** |
| BUG-27 | **S11** |
| BUG-28 | **S13** |
| BUG-29 | **S13** |
| BUG-30 | **S08** |
| BUG-31 | **S05** |
| BUG-32 | **S12** |
| BUG-33 | **S12** |
| BUG-34 | **S12** |
| BUG-35 | **S12** |
| BUG-36 | **S12** |
| BUG-37 | **S07** |
| BUG-38 | **S14** |
| BUG-39 | **S14** |
| BUG-40 | **S17** |
| BUG-41 | **S15** |
| FEAT-01 | **S14** |
| FEAT-02 | **S14** |
| FEAT-03 | **S14** |
| FEAT-04 | **S14** |
| FEAT-05 | **S15** |
| FEAT-06 | **S15** |
| FEAT-07 | **S15** |
| FEAT-08 | **S16** |
| FEAT-09 | **S17** |
| FEAT-10 | **S18** |
| FEAT-11 | **S19** |
| FEAT-12 | **S20** |
| FEAT-13 | **S21** |
| FEAT-14 | **S22** |

Excluded by Phase 2.5 Lock (Out of Scope in ALL sessions, audited in `S24`): `DEF-01..DEF-10` (10), `NO-01..NO-12` (12).

======================================================================
3. ROUND 3 AUDIT CHECKLIST FOR CORRECTORS (QWEN, GROK, GPT)
======================================================================
Please audit `Phase_3_Antigravity_Kit_v2.zip` and respond with `PHASE 3 STATUS: APPROVED & IDENTICAL` (or exact diffs if any defect remains):
- **Qwen & Grok:** Byte-level check (`MANIFEST.sha256`, `^\\*@@` / `^\\+@@` in `S05`, `\b64:` in `S03`), 63/63 ID coverage, Line-1 `/plan`, `AGENTS.md` §19/20/21/24/29 safety in `S01`, Probe vs Guard honesty (`35/32` in Guards), zero `guard_git.py` hook claims, and `CHANGELOG.md` + single `v1.4.1` bump contract.
- **GPT:** `S24` Final Acceptance Audit completeness, `DEP-1` (`BUG-31` strictly before `BUG-07` in `S05`), read-only `/swarm` cross-model verifier separation, `.agents/` merge procedure, `/misora-verify` argument rule, and non-`683724e` progression clarity for `S02..S24`.

PHASE 3 STATUS: OPEN — READY FOR ROUND 3 FINAL AUDIT (UNIFIED v2 KIT BY GEMINI)
