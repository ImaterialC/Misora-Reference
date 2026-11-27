# ENV-01 Implementation Plan — Context Hygiene v2

**Status:** PLAN ONLY (Read-Only Preflight Complete — Awaiting Independent Review & Proceed)  
**Repository:** `ImaterialC/Misora-Editor` (`D:\Misora-Editor`)  
**Branch:** `main`  
**HEAD:** `ead65077a2a6cf3a664543cfb50f855268a29e2a`  
**Product Version:** `1.4.15` (Locked; v1.5.0 CANCELLED / NOT RELEASED / VERSION PROMOTION NOT AUTHORIZED)  

---

## 1. Phase A — Preflight Transcript & PASS/STOP Result

**Result:** **PASS** (All preflight gates satisfied; zero repository mutations performed.)

| Check | Command / Source | Observed Output | Status |
| :--- | :--- | :--- | :--- |
| Repo Root | `git rev-parse --show-toplevel` | `D:/Misora-Editor` | PASS |
| Exact HEAD | `git rev-parse HEAD` | `ead65077a2a6cf3a664543cfb50f855268a29e2a` | PASS |
| Branch | `git branch --show-current` | `main` | PASS |
| Working Tree | `git status --short --untracked-files=all` | *(empty — clean working tree)* | PASS |
| Latest Commit | `git log -1 --oneline --decorate` | `ead6507 (HEAD -> main, origin/main, origin/HEAD) S11e (v1.4.15): UI Polish, Branding, Verified Icons + 3-Icon Selection Trio, Splash Lifecycle, Menu Dedup & Tooltips (475 tests, 0 regressions)` | PASS |
| Product Version | `__init__.py` | `__version__ = "1.4.15"` | PASS |
| Test Discovery (Count-Only) | `py -3.12 -B -c "import unittest; suite=unittest.TestLoader().discover('tests'); n=suite.countTestCases(); print('countTestCases() =', n); raise SystemExit(0 if n == 475 else 1)"` | `countTestCases() = 475` (exit code 0, `-B` prevented bytecode writes) | PASS |

---

## 2. Exact Baseline Hashes, Byte Lengths, Line Counts & Collisions

| File | Byte Length | Line Count | SHA-256 |
| :--- | ---: | ---: | :--- |
| `AGENTS.md` | `10,748` | `163` | `40bc51b69270262f31651faec3ad9e48cb633d2c972e24f9a3ec7dc77de682aa` |
| `PROJECT_STATE.md` | `257,683` | `1,758` | `6823100d99b91bf266a9035c9d2c581c7a61657dbe0a5a5f99b17e9265b4d39d` |

### Target Collisions, Untracked & Ignored State
- `docs/` exists: `False` (no target collisions)
- `tools/` exists: `False` (no target collisions)
- Ignored local paths (`git status --ignored --short`): `.agents/`, `__pycache__/`, `assets/__pycache__/`, `backups/`, `core/__pycache__/`, `misora_config.json`, `tests/__pycache__/`. None of these are in scope; all remain untouched.
- Reference kit verified read-only at `D:\Reference\Misora-Reference\Misora_ENV01_Kit_v2` (`drafts/`, `scripts/generate_symbol_index.py`, `prompts/`, `README_ID.md`, `SHA256SUMS.txt`).

---

## 3. Phase B — Strict Path Ownership Matrix

### Allowed Candidate Paths (13 Total)

| Target Path | Action | Source / Origin | Preconditions | Validation | Rollback |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `docs/archive/AGENTS_v1.4_PRE_ENV01.md` | `BYTE-COPY` | `AGENTS.md` at `ead6507` | `docs/` does not exist | Raw byte equality + SHA-256 `40bc51b6...` | Delete file |
| `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md` | `BYTE-COPY` | `PROJECT_STATE.md` at `ead6507` | `docs/` does not exist | Raw byte equality + SHA-256 `6823100d...` | Delete file |
| `docs/archive/ARCHIVE_SHA256SUMS.txt` | `CREATE` | Computed hashes + manifest | Byte-copies verified | `sha256sum` / Python check matches | Delete file |
| `docs/archive/HISTORY_INDEX.md` | `CREATE` | `Kit_v2/drafts/HISTORY_INDEX_TEMPLATE.md` + extracted headings | Archive hashes verified | All `PROJECT_STATE.md` headings indexed | Delete file |
| `docs/archive/superseded-plans/README.md` | `CREATE` | `Kit_v2/drafts/SUPERSEDED_PLANS_README_TEMPLATE.md` | Archive hashes verified | Marks S12 & future S15 as superseded/cancelled | Delete file |
| `AGENTS.md` | `REPLACE` | `Kit_v2/drafts/AGENTS.md` (verified against 29 rules) | Verbatim archive verified | Size `<= 6144` bytes; all 29 rules mapped | Restore from `docs/archive/AGENTS_v1.4_PRE_ENV01.md` |
| `PROJECT_STATE.md` | `REPLACE` | `Kit_v2/drafts/PROJECT_STATE.md` (verified against S11e) | Verbatim archive verified | Size `<= 15360` bytes; exact `1.4.15` & `475` split | Restore from `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md` |
| `docs/ai/CONTEXT_ROUTER.md` | `CREATE` | `Kit_v2/drafts/CONTEXT_ROUTER.md` | None | Layer 0/1/2/3 routing; max 1–3 Layer 1 refs | Delete file |
| `docs/ai/ENV01_MIGRATION_MAP.md` | `CREATE` | `Kit_v2/drafts/ENV01_MIGRATION_MAP_TEMPLATE.md` + Section 5 tables | All 29 AGENTS + all PS headings mapped | 100% row coverage | Delete file |
| `docs/project/OPEN_ISSUES.md` | `CREATE` | `Kit_v2/drafts/OPEN_ISSUES.md` | None | Includes T-01..T-14, DEF-01..10, test debt, manual QA | Delete file |
| `docs/project/DECISIONS.md` | `CREATE` | `Kit_v2/drafts/DECISIONS.md` | None | Exact `1.4.15`, v1.5.0 CANCELLED, S12 PAUSED/SUPERSEDED, S15 historical retained | Delete file |
| `tools/generate_symbol_index.py` | `CREATE` | `Kit_v2/scripts/generate_symbol_index.py` | `tools/` does not exist | Python 3.12 stdlib only; strict UTF-8; `--check` | Delete file |
| `docs/architecture/MISORA_SYMBOL_INDEX.md` | `GENERATED` | `tools/generate_symbol_index.py` | Generator created | `--check` exits 0; exact HEAD + per-file SHA-256 | Delete file |

### Absolutely Read-Only / Forbidden Paths
- `__init__.py`, `misora.py`, `core/**`, `assets/**`, `tests/**`
- `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, `README.md`
- All other application, configuration, build, or runtime files.
- No dependencies added; no tests edited/run; no version bump; no git commit/push/reset/clean.

---

## 4. Phase C — Verbatim Archive Design (Before Root Replacement)

1. Read `AGENTS.md` and `PROJECT_STATE.md` as raw bytes from HEAD `ead65077a2a6cf3a664543cfb50f855268a29e2a`.
2. Write raw bytes verbatim to `docs/archive/AGENTS_v1.4_PRE_ENV01.md` and `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md` (no header/TOC, no line-ending normalization, no encoding change, no trailing newline added).
3. Verify `source_bytes == archive_bytes` and SHA-256 equality (`40bc51b69270262f31651faec3ad9e48cb633d2c972e24f9a3ec7dc77de682aa` and `6823100d99b91bf266a9035c9d2c581c7a61657dbe0a5a5f99b17e9265b4d39d`) **before** touching root `AGENTS.md` or `PROJECT_STATE.md`.
4. Record manifest in `docs/archive/ARCHIVE_SHA256SUMS.txt` and `docs/archive/HISTORY_INDEX.md`.
5. After root replacement, re-verify archive hashes against `ARCHIVE_SHA256SUMS.txt` (never against the rewritten root files).
6. **STOP Trigger:** Any byte/hash mismatch halts execution immediately before root replacement.

---

## 5. Phase D — Complete Retention / Migration Map

### A. `AGENTS.md` — All 29 Numbered Sections Mapped

| # | Old Section Title | Lines | Old Invariant / Meaning | Target Destination | Lifecycle | Retained / Condensed Rule & Validation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Source of truth | 3–8 | Read `PROJECT_STATE.md` & disk files; separate confirmed/conditional/invariants/retracted | `AGENTS.md` | `ACTIVE` | Condensed into Layer 0 Source & Evidence Discipline |
| 2 | Verification gate | 9–14 | `compileall` + `unittest discover`; record actual baseline; never fake/skip | `AGENTS.md` | `ACTIVE` | Condensed into Verification & Test Discipline |
| 3 | Tkinter architecture | 15–20 | Single `tk.Tk()`, explicit `master=`, no widget attr reassignment, `winfo_exists()` | `AGENTS.md` | `ACTIVE` | Retained in Tk Main-Thread & Widget Architecture |
| 4 | AST identity | 21–27 | `records` is truth, `Box` is projection, `Seg.record` direct ref, no serialized `uid` | `AGENTS.md` | `ACTIVE` | Retained in AST / Box / Structural Identity |
| 5 | Box model safety | 28–33 | `clean_text`/`text`/`raw` read-only; `BoxSnapshot` preserves `seg_texts` | `AGENTS.md` | `ACTIVE` | Retained in AST / Box / Structural Identity |
| 6 | Structural edits | 34–38 | Mutate `records`, preserve unknown commands, `removed_records` by `uid` | `AGENTS.md` | `ACTIVE` | Retained in AST / Box / Structural Identity |
| 7 | Argument integrity | 39–45 | Preserve extra args, no empty binary arg, narration=`tag`, `{playername}`->`{0}`, update `seg.raw` | `AGENTS.md` | `ACTIVE` | Retained in Binary & Argument Integrity |
| 8 | v2 text safety | 46–50 | Preserve numeric IDs, categories, unknown cmds, whitespace-only args, Unicode line seps | `AGENTS.md` | `ACTIVE` | Retained in Binary & Argument Integrity |
| 9 | Bundle save safety | 51–56 | `packer="original"`, `.tmp` -> reopen & verify -> `os.replace`, `_is_saving` | `AGENTS.md` | `ACTIVE` | Retained in Bundle Save & Disk Integrity |
| 10 | XUAT dictionary safety | 57–64 | `key=value` per line, escape newlines, strict decode, immutable JP keys | `AGENTS.md` | `ACTIVE` | Retained in XUAT Encoding & Dictionary Safety |
| 11 | Central edit commit | 65–69 | Single shared commit path; virtual events commit; Box 0 dedicated flush | `AGENTS.md` | `ACTIVE` | Retained in Edit Commit & Undo Lifecycle |
| 12 | Shortcut router | 70–76 | `MisoraShortcuts` bindtag, whitelist, don't intercept Ctrl+C/V/X/A, IME/AltGr safe | `AGENTS.md` | `ACTIVE` | Retained in Clipboard & Shortcut Router |
| 13 | Undo and dirty state | 77–83 | Flush before undo/save/nav; `begin_batch`/`end_batch` in `finally`; revision-based dirty | `AGENTS.md` | `ACTIVE` | Retained in Edit Commit & Undo Lifecycle |
| 14 | Clipboard | 84–87 | Retry on `TclError`, normalize CRLF/CR, don't shadow newer system clipboard | `AGENTS.md` | `ACTIVE` | Retained in Clipboard & Shortcut Router |
| 15 | Workers and search | 88–93 | Workers never call Tk; immutable snapshots; main-thread queue; `finally` reset | `AGENTS.md` | `ACTIVE` | Retained in Tk Main-Thread & Worker Architecture |
| 16 | Document lifecycle | 94–99 | Per-doc view state; prune undo on close; dirty prompt; `reload_from_disk=True` | `AGENTS.md` | `ACTIVE` | Retained in Edit Commit & Undo Lifecycle |
| 17 | Config and secrets | 100–103 | Recovery copy on parse fail; OS credential/DPAPI for API keys; redact logs | `AGENTS.md` | `ACTIVE` | Retained in Secrets & Network Safety |
| 18 | Network safety | 104–108 | TLS cert & hostname verification enabled; no ignore-SSL checkbox; DeepL usage check | `AGENTS.md` | `ACTIVE` | Retained in Secrets & Network Safety |
| 19 | NGUI single source | 109–114 | `core/ngui_tags.py` single source; hyphen gradients; TagMasker; pixel-calibrated length | `AGENTS.md` | `ACTIVE` | Retained in NGUI & CSIF Rules |
| 20 | CSIF rules | 115–121 | `@@Speaker`, `@@_`, `@@!meta`, 1-based sparse `@@#N\|Speaker`, outer fence strip | `AGENTS.md` | `ACTIVE` | Retained in NGUI & CSIF Rules |
| 21 | UI safety | 122–128 | `best_contrast_fg()`, tooltips, `__init__.py` `__version__` single source, overflow rule | `AGENTS.md` | `ACTIVE` | Retained in UI, Version & Overflow Policy |
| 22 | Startup | 129–133 | Single process; lazy-load UnityPy under lock; defer session restore | `AGENTS.md` | `ACTIVE` | Retained in Startup & Logging |
| 23 | Disk and logging | 134–138 | Windows long-path helper; background logger queue; no runtime DPI change | `AGENTS.md` | `ACTIVE` | Retained in Startup & Logging |
| 24 | Scope discipline | 139–142 | Gate MTL/Prompt Studio/LRU; no invented fixtures | `AGENTS.md`, `DECISIONS.md` | `SUPERSEDED` (old v1.5 Track 1 gate) / `ACTIVE` (no invented fixtures) | Scope gating updated in `DECISIONS.md`; honesty rule retained in `AGENTS.md` |
| 25 | Delivery | 143–145 | Report changed files, tests, output, limitations, rollback, update `PROJECT_STATE.md` | `AGENTS.md` | `ACTIVE` | Retained in Delivery & Rollback |
| 26 | Box clipboard contract | 146–152 | Copy Box=CSIF, Paste Box=insert, Paste Script=replace, Ctrl+V prompt on CSIF | `AGENTS.md` | `ACTIVE` | Retained in Clipboard & Shortcut Router |
| 27 | No broken intermediate state | 153–156 | Migrate callers in same phase; no broken `Box.__deepcopy__` before snapshot | `AGENTS.md` | `ACTIVE` | Retained in Scope & Safety |
| 28 | Helpers before callers, and visible failures | 157–160 | Define helpers before callers; `report_callback_exception` surfaces status-bar error | `AGENTS.md` | `ACTIVE` | Retained in Scope & Safety |
| 29 | Machine-confirmed release blockers | 161–163 | v1.4.0 manual blockers (Ctrl+H fixed; ribbon Cut & Paste Box reopened) | `OPEN_ISSUES.md`, `HISTORY_INDEX.md` | `HISTORICAL-REFERENCE` / `ACTIVE` (manual QA) | Moved out of `AGENTS.md` to `OPEN_ISSUES.md` (manual QA) & archive |

### B. `PROJECT_STATE.md` — Exhaustive Heading Migration Matrix

Every Markdown heading (levels 1–6) from `PROJECT_STATE.md` (`1,758` lines) is accounted for below:

| Line | Lvl | Heading Text | Anchor / Slug | Canonical IDs | Target Destination | Lifecycle |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | H1 | `Misora: Story Editor — Canonical Project State` | `#misora-story-editor-canonical-project-state` | `v1.4.15`, `S11e` | `PROJECT_STATE.md`, `HISTORY_INDEX.md` | `ACTIVE` |
| 16 | H2 | `1. How to use this document` | `#1-how-to-use-this-document` | — | `CONTEXT_ROUTER.md`, `HISTORY_INDEX.md` | `SUPERSEDED` |
| 31 | H2 | `2. Measured Verification Baseline` | `#2-measured-verification-baseline` | `475`, `432 pass`, `35 skip`, `6 fail`, `2 error` | `PROJECT_STATE.md`, `OPEN_ISSUES.md` | `ACTIVE` |
| 159 | H3 | `Current Test Environment Blockers` | `#current-test-environment-blockers` | `storydata_1001005.unity3d` | `OPEN_ISSUES.md` | `ACTIVE` |
| 162 | H3 | `Reference Audit Provenance & Document Exclusions` | `#reference-audit-provenance-document-exclusions` | — | `HISTORY_INDEX.md` | `HISTORICAL-REFERENCE` |
| 171 | H3 | `Track 1 Automated Stabilization Gate: COMPLETE (S01..S13)` | `#track-1-automated-stabilization-gate-complete-s01s13` | `S01..S13` | `HISTORY_INDEX.md` | `HISTORICAL-REFERENCE` |
| 176 | H3 | `v1.5 S11e (v1.4.15) — UI Polish, Branding & Usability (Q-03, Q-05, Q-13..Q-17) (2026-11-28)` | `#v15-s11e-v1415-ui-polish-branding-usability-q-03-q-05-q-13q-17-2026-11-28` | `S11e`, `v1.4.15`, `Q-03`, `Q-05`, `Q-13..Q-17` | `PROJECT_STATE.md`, `HISTORY_INDEX.md` | `ACTIVE` (baseline) / `HISTORICAL-REFERENCE` (log) |
| 194–1023 | H3–H4 | Historical Session Logs (`S11d`, `S11c`, `S11b2`, `S11b`, `S11`, `S10`, `S09b`, `S09`, `S08`, `S07`, `S06`, `S05`, `S04`, `S03`, `S02`, `S01`, `S20`..`S12`, `S0/S1`) | *(individual slugs in `HISTORY_INDEX.md`)* | `S01..S20`, `v1.4.1..v1.4.14`, `Q-01..Q-23` | `HISTORY_INDEX.md`, `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md` | `HISTORICAL-REFERENCE` |
| 1030–1385 | H3–H4 | `S2`..`S9c`, `Phase 5`..`Phase 2` New Deliverables & Runtime Fixes | *(individual slugs in `HISTORY_INDEX.md`)* | `S2..S9c`, `Phase 2..5` | `HISTORY_INDEX.md`, `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md` | `HISTORICAL-REFERENCE` |
| 1396 | H3 | `Manual Windows Tests Still Required (Rule 29 — cannot be automated headlessly)` | `#manual-windows-tests-still-required-rule-29-cannot-be-automated-headlessly` | `MANUAL-PENDING` | `OPEN_ISSUES.md` | `ACTIVE` |
| 1402 | H3 | `Baseline Before This Session (for comparison)` | `#baseline-before-this-session-for-comparison` | — | `HISTORY_INDEX.md` | `HISTORICAL-REFERENCE` |
| 1410 | H2 | `3. Historical Baseline B1–B20 (Preserved)` | `#3-historical-baseline-b1b20-preserved` | `B1..B20` | `HISTORY_INDEX.md` | `HISTORICAL-REFERENCE` |
| 1437 | H2 | `4. Canonical Defect Ledger` | `#4-canonical-defect-ledger` | `BUG-*`, `FEAT-*`, `HYG-*`, `DEF-01..10` | `OPEN_ISSUES.md`, `HISTORY_INDEX.md` | `HISTORICAL-REFERENCE` / `ACTIVE` |
| 1439 | H3 | `P0 — Data Integrity & Release Blockers (Phase 1 & Phase 2)` | `#p0-data-integrity-release-blockers-phase-1-phase-2` | `P0` | `HISTORY_INDEX.md`, `OPEN_ISSUES.md` | `HISTORICAL-REFERENCE` |
| 1462 | H3 | `P0 (new, from manual testing 2026-11-20)` | `#p0-new-from-manual-testing-2026-11-20` | `P0` | `HISTORY_INDEX.md`, `OPEN_ISSUES.md` | `HISTORICAL-REFERENCE` |
| 1474 | H3 | `P1 — Functional, UI, & Security Issues (Phases 2, 3, 5)` | `#p1-functional-ui-security-issues-phases-2-3-5` | `P1` | `HISTORY_INDEX.md`, `OPEN_ISSUES.md` | `HISTORICAL-REFERENCE` |
| 1532 | H3 | `P2 — Performance, QoL, & Measured Risks (Phases 3, 4, 5)` | `#p2-performance-qol-measured-risks-phases-3-4-5` | `P2` | `HISTORY_INDEX.md`, `OPEN_ISSUES.md` | `HISTORICAL-REFERENCE` |
| 1549 | H2 | `5. Retracted Claims` | `#5-retracted-claims` | `RETRACTED` | `OPEN_ISSUES.md`, `HISTORY_INDEX.md` | `RETRACTED` |
| 1571 | H2 | `6. Design Invariants for Future Capabilities` | `#6-design-invariants-for-future-capabilities` | `DEF-01..DEF-10`, `NO-03` | `DECISIONS.md`, `OPEN_ISSUES.md` | `ACTIVE` |
| 1594 | H2 | `7. Five-Phase Execution Roadmap` | `#7-five-phase-execution-roadmap` | `Phase 1..6` | `HISTORY_INDEX.md`, `DECISIONS.md` | `SUPERSEDED` |
| 1596–1660 | H3 | `Phase 1`..`Phase 6 — Safety & Multi-Document Architecture Roadmap (S-Series)` | *(individual slugs in `HISTORY_INDEX.md`)* | `Phase 1..6` | `HISTORY_INDEX.md` | `SUPERSEDED` |
| 1737 | H2 | `8. Fixture & Platform Observations` | `#8-fixture-platform-observations` | `storydata_1001005.unity3d` | `OPEN_ISSUES.md`, `HISTORY_INDEX.md` | `ACTIVE` / `HISTORICAL-REFERENCE` |
| 1754 | H2 | `9. GitHub Documentation Audit (2026-11-21)` | `#9-github-documentation-audit-2026-11-21` | — | `HISTORY_INDEX.md` | `HISTORICAL-REFERENCE` |

---

## 6. Phase E — Target File Drafts & Generator Plan

- **Root `AGENTS.md`** (`<= 6144` bytes): Use `Kit_v2/drafts/AGENTS.md` as base, ensuring all 29 active rules are concisely represented without exceeding 6 KiB.
- **Root `PROJECT_STATE.md`** (`<= 15360` bytes): Use `Kit_v2/drafts/PROJECT_STATE.md` as base, stating:
  - Version `1.4.15`, HEAD `ead65077a2a6cf3a664543cfb50f855268a29e2a` (S11e).
  - `v1.5.0` release campaign **CANCELLED / NOT RELEASED / PROMOTION NOT AUTHORIZED**.
  - Old S12 release audit **PAUSED / SUPERSEDED**.
  - Future S15 work proposal **CANCELLED** (historical completed S15 retained).
  - Test baseline: `475 total = 432 pass + 35 skip + 6 fail + 2 error` (not 475 pass).
- **`docs/project/OPEN_ISSUES.md`**: Include `T-01..T-14` (`T-01..T-04` as `REPORTED / NEEDS-REPRO`), `DEF-01..DEF-10`, 3 non-fixture failures, fixture-related failures/errors + 35 skips, `Tcl_AsyncDelete` watch item, and `MANUAL-PENDING`.
- **`docs/project/DECISIONS.md`**: Reconcile old v1 seed with current ruling (`1.4.15`, v1.5.0 CANCELLED, S12 PAUSED/SUPERSEDED, future S15 CANCELLED, historical S15 retained, no "post-v1.5.0" schedule).
- **`docs/ai/CONTEXT_ROUTER.md`**: Layer 0 (`AGENTS.md` + `PROJECT_STATE.md`), Layer 1 (`CONTEXT_ROUTER.md` + 1–3 relevant docs), Layer 2 (source slices/tests), Layer 3 (archive/history opt-in).
- **`tools/generate_symbol_index.py` & `docs/architecture/MISORA_SYMBOL_INDEX.md`**:
  - Copy/adapt from `Kit_v2/scripts/generate_symbol_index.py` (Python 3.12 stdlib only: `ast`, `pathlib`, `hashlib`, `subprocess`, `argparse`, `sys`).
  - Strict UTF-8 (no `errors="replace"`), exact `git rev-parse HEAD` + per-file SHA-256, deterministic output (no timestamps), `--check` flag (exits nonzero on mismatch).
  - Default indexed files: `misora.py`, `__init__.py`, `core/*.py`, `assets/*.py`.
  - Commands after Proceed:
    - `py -3.12 -B tools/generate_symbol_index.py`
    - `py -3.12 -B tools/generate_symbol_index.py --check`

---

## 7. 11 Objective Acceptance Gates

1. **Preflight:** Exact HEAD `ead65077a2a6cf3a664543cfb50f855268a29e2a`, `main`, clean tree, `__version__ == "1.4.15"`.
2. **Strict ownership:** Changed paths only from the 13-path allowlist; forbidden paths untouched.
3. **Verbatim archive:** Raw byte copy; hash/equality verified before root edits; captured manifest verified after.
4. **Migration proof:** All 29 `AGENTS.md` sections and every `PROJECT_STATE.md` heading/slug/ID mapped.
5. **Layer 0 size:** `AGENTS.md <= 6144` bytes; `PROJECT_STATE.md <= 15360` bytes.
6. **Ledger:** `T-01..T-14`, `DEF-01..10`, test debt, fixture, manual QA/revalidation; evidence and lifecycle separated.
7. **Decisions:** Exact `1.4.15` / v1.5.0 CANCELLED / S12 PAUSED-SUPERSEDED / future S15 CANCELLED / historical S15 retained.
8. **Router:** Layer 0/1/2/3 and max 1–3 Layer 1 refs.
9. **AST index:** Strict UTF-8, HEAD + per-file hashes, deterministic generation, `--check` exits 0, no deps/source writes.
10. **Product/test boundary:** Forbidden paths unchanged; production diff empty; `countTestCases() == 475` (count only).
11. **Four-AI validation:** Identical 7-question read-only test for Gemini, GPT-6, Qwen, Antigravity; factual alignment and honest unknowns; no commit/push.

---

## 8. Risks, STOP Triggers & File-by-File Rollback Plan

- **STOP Triggers:** Any HEAD/branch/status mismatch, version mismatch, test count != 475, target collision, archive byte/hash mismatch, missing migration row, scope outside allowlist, or any production/test/config change.
- **Rollback Plan (Zero Product Impact):**
  1. Restore `AGENTS.md` from `docs/archive/AGENTS_v1.4_PRE_ENV01.md` (raw byte copy) and verify SHA-256 `40bc51b6...`.
  2. Restore `PROJECT_STATE.md` from `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md` (raw byte copy) and verify SHA-256 `6823100d...`.
  3. Delete created `docs/` and `tools/` directories.
  4. Verify `git status --short --untracked-files=all` is clean.
