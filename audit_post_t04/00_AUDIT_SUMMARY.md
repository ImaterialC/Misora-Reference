# Misora POST-T-04 — Consolidated Audit Summary

**Audit baseline:** `8affb7c53b6af6047ace423c7e4d830a978eb644` on `main`  
**Version:** `1.4.15` (root `__init__.py` authoritative)  
**Scan date:** 2026-11-28/29  
**Python:** 3.12.10 (MSC v.1943 64-bit)  
**OS:** Windows NT 10.0.26100.0  
**Symbol Index:** `CHECK PASS`  
**Test count:** 516 discovered (473 PASS, 35 SKIP, 6 FAIL, 2 ERROR — unchanged baseline debt)  
**Zero-edit gate:** PASS (git status empty, pre_pyc_count = post_pyc_count = 125, no .ruff_cache)

---

## Step 1 — Preflight & Baseline

| Gate | Result |
|---|---|
| Branch | `main` |
| HEAD | `8affb7c53b6af6047ace423c7e4d830a978eb644` |
| Git status | Empty (clean) |
| Version | `1.4.15` |
| Symbol index | `CHECK PASS` |
| Test count | 516 |
| Pre-.pyc count | 125 |

All preflight gates **PASS**.

---

## Step 2 — AST Static Analysis (`01_ast_static_report.md`)

**Scope:** 33 production files + 103 total .py files + 3 .bat launchers

| Check | Count | Label |
|---|---:|---|
| Duplicate Functions / Methods | 2 | `SOURCE-OBSERVED` — **FALSE POSITIVE**: both are `@property` / `@X.setter` pairs (`dialogue_font_family` at L3138/3143, `dialogue_font_size` at L3150/3155) |
| Unreachable Statements | 0 | — |
| Mutable Default Arguments | 0 | — |
| Zero-Caller Dead-Code Candidates | 501 | `UNVERIFIED-DEAD` — **~465 are test methods** (unittest discovery invokes by name, not token reference); ~36 are production candidates requiring manual verification |
| Potential Dead Standalone Scripts | 0 | — |
| Remaining `winfo_ismapped()` | 5 | `SOURCE-OBSERVED + NEEDS-REPRO` — 1 in select-box UI (L10778), 2 in ruler (L13756/L13770), 1 in ruler-cont (L13770), 1 in comparison frame (L23597); T-01-class visibility risk |
| Broad `except` Blocks | 233 | `SOURCE-OBSERVED` — includes defensive Tk lifecycle, teardown, and I/O error handling; majority are in non-critical UI/toast/theme paths |
| `after()` / Tk Variables / Workers | 96 | `SOURCE-OBSERVED` — 41 `after_cancel` sites, 86+ Tk Variable creations, 13 thread creation sites; Tcl_AsyncDelete risk surface |

**Actionable findings:**
- **5 `winfo_ismapped()` calls** remain in production code (potential T-01-class visibility bugs)
- **233 broad `except` blocks** — triage recommended for critical-path functions (save/export/undo)
- **96 after/Variable/thread sites** — mapped for Tcl_AsyncDelete teardown audit

---

## Step 3 — External Linters

| Linter | Status |
|---|---|
| ruff | NOT INSTALLED (skipped) |
| vulture | NOT INSTALLED (skipped) |

---

## Step 4 — Priority Watch & Wave-0/1 Source Audit (`04_priority_watch_audit.md`)

### Wave 0 — Tcl_AsyncDelete Test Teardown

| Item | Evidence | Lifecycle |
|---|---|---|
| `Variable.__del__` RuntimeError in monolithic test `discover` | `SOURCE-OBSERVED + NEEDS-REPRO` | `ACTIVE` (watch) |

**Root cause:** 80+ Tk Variables per `MisoraApp()` instance, GC cleanup after `destroy()` races with Tk interpreter shutdown. Test-infrastructure issue, not proven app crash. Split runs pass cleanly.

### Wave 1 — F-GPT-03 (Exit/Close Safety)

| Item | Evidence | Lifecycle |
|---|---|---|
| `_on_app_exit` multi-dirty-doc behavior | `SOURCE-OBSERVED` | `ACTIVE` |
| `close_file` / `close_all_files` abort-on-cancel | `SOURCE-OBSERVED` | `ACTIVE` |

**Assessment:** Correctly implements AGENTS.md §6 — per-document Save/Discard/Cancel with abort on Cancel or save failure.

### Wave 1 — F-GPT-07 (XUAT-JP-KEY-DRIFT) & Bundle Integrity

| Item | Evidence | Lifecycle |
|---|---|---|
| `register_jp_key` immutability guard | `SOURCE-OBSERVED` | `ACTIVE` |
| `save_bundle_story` 7-gate verification pipeline | `SOURCE-OBSERVED` | `ACTIVE` |
| JP key drift on box clone/insert edge cases | `UNVERIFIED + NEEDS-REPRO` | `ACTIVE` |

**Assessment:** Core immutability contract is sound. Bundle save pipeline is robustly defensive. Edge-case drift during clone/insert with shared UIDs requires targeted manual trace.

### Wave 1/2 — T-12 (XUAT Sync Threading)

| Item | Evidence | Lifecycle |
|---|---|---|
| `batch_sync` runs synchronously on UI thread | `SOURCE-OBSERVED + DEFERRED` | `DEFERRED` |

**Assessment:** ~2.899s synchronous I/O accepted under S11b2 Option A waiver. **NOT a new P1 bug.** Async worker IO explicitly deferred.

### Wave 2 — T-03 (All Script Stale Purple Highlight)

| Item | Evidence | Lifecycle |
|---|---|---|
| `_set_as_active_card` only tracks `old_idx → new_idx` | `SOURCE-OBSERVED` | `ACTIVE` |
| `_apply_as_card_visual_state` highlight/unhighlight | `SOURCE-OBSERVED` | `ACTIVE` |

**Assessment:** `CONFIRMED` per OPEN_ISSUES.md with 4 reproduction screenshots. Likely root cause: `_set_as_active_card` unhighlights only the single previous active card, missing intermediate cards during rapid multi-step navigation. Full root-cause verification requires keyboard shortcut dispatch path trace.

---

## Step 5 — Post-Scan Integrity Gate

| Gate | Result |
|---|---|
| Git status (post-scan) | Empty (clean) — **PASS** |
| .ruff_cache | Not present — **PASS** |
| Post-.pyc count | 125 = pre_pyc_count — **PASS** |

**ZERO-EDIT GATE: ALL CHECKS PASS**

---

## Verification Boundary

**Inspected:**
- Full AST scan of 33 production files and 103 total .py files
- Targeted deep source audit of `misora.py` (24,004 lines — ~15 method clusters)
- `core/bundle_io.py` (325 lines — full `save_bundle_story` pipeline)
- `core/xunity_sync.py` (612 lines — `XUnitySyncManager`, `batch_sync`)
- `tests/test_s8b2_memory_guards.py` and `tests/test_s8b3_encoding_detection.py` teardown patterns

**NOT inspected:**
- `_bind_as_pool_card` full implementation
- Keyboard shortcut dispatch path for Prev/Next in All Script view
- Full `open_file` method body (only JP key section)
- `_save_document_entry` implementation
- XUAT cleanup module (`core/xuat_cleanup.py`)
- Dynamic dispatch (`command=`, `.bind(`, `.after(`, `.protocol(`) for dead-code verification
- Any file inside `docs/archive/`

---

## Audit File Manifest

| File | SHA-256 |
|---|---|
| `00_baseline.txt` | `55D6D1D974655C473960993C67C306C5E2C68160C251C6D1C264288BF88F6792` |
| `01_ast_static_report.md` | `3EF701EE7D2B9B38E30FD4A15C54A8AE895CA4BB105FA45B2C8317347300DF34` |
| `02_ruff_report.txt` | `22DC8AEB493D8BAF44D98D74DB2B07378D57B74928BB6E7F8674A011599C160A` |
| `03_vulture_report.txt` | `942A5EAFAC72F51EEEEE3F07DCBDA5F2049CA3117ADBF723D748ECCD01DA24FB` |
| `04_priority_watch_audit.md` | `4221E21559951EF0AE313F7E380AE88D7D975039823C84524D320BC5ECA71EE2` |
| `scan_static_ast.py` | `8E4DFFD4AAAB5C1C91DF0A9524CB88EE943C752BF2CC2692E3CC4BD2FB61F5F5` |

---

**STOP — AUDIT REPORTS READY FOR MULTI-AI TRIAGE**
