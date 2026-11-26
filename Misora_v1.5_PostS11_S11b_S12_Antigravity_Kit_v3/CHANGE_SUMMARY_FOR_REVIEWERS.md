# Change Summary — Post-S11 S11b–S12 Antigravity Kit v3 (All Remaining Qwen + GPT Corrections Applied)

Responding To:
- Qwen Final Audit (`C-1` `assets/splash.py` canonical path in S11e + S12; `C-2` `assets/icon.py` load-time resizing in S11e without overwriting source PNGs in `assets/icons/`)
- GPT Independent Review — Post-S11 Kit v2: Remaining Corrections (`#1` exact `entry_count` semantics, `#2` operational `files_scanned` definition, `#3` `assets/splash.py` & `assets.splash._VERSION` throughout S11e & S12)

Execution Boundary: Prompt/documentation revision ONLY. Zero production source files modified; zero `/plan` sessions started; `v1.5.0` remains ON HOLD. `S11c` and `S11d` are preserved verbatim from Kit v2.

## Exact Corrections Applied in Kit v3

1. **S11b `Q-01` — Exact `entry_count` & `add_entry()` Semantics (GPT #1):**
   - Preserves existing `_exact_map`, `_value_map`, and `entries` insertion behavior (explicitly forbids silently dropping entries from `_exact_map`, `_value_map`, or `entries`).
   - Increments canonical `entry_count` ONLY when `normalize_xuat_key(raw_key, strip_ngui=True) != ""`, keeping `entries_read` and canonical `entry_count` strictly synchronized (`entries_read == entry_count == unique_keys + duplicate_entries`).
   - Requires auditing ALL callers of `len(idx)` and `bool(idx)` in `/plan` before changing `entry_count` semantics.
   - Confirms empty normalized keys never enter `_norm_stripped_map`, and adds explicit regression tests in `test_probe_1` for exact-tier lookup and value lookup including the empty-normalized-key edge case.

2. **S11b `Q-01` — Operational `files_scanned` Definition (GPT #2):**
   - Exposes persistent `files_scanned` on `XuatIndex` defined as unique, eligible, non-excluded `.txt` files actually attempted after deduplication.
   - Locks completed-scan identity: `files_scanned == len(files_indexed) + len(skipped_files)` (excluded rule files and duplicate paths do NOT count; attempted files that fail read/decode DO count in `files_scanned` and remain visible in `skipped_files`).
   - Adds explicit test requirements in `test_probe_1` covering successful reads, duplicate paths, excluded rule files, and simulated read/decode failures.

3. **S11e — Canonical `assets/splash.py` + `assets/icon.py` Load-Time Resizing (Qwen C-1, C-2 & GPT #3):**
   - Replaced every root `splash.py` reference (`@splash.py`, Allowed Files, Q-05/Q-13) with canonical `assets/splash.py`.
   - Added `assets/icon.py` to S11e Context Pointers, Allowed Files, and Q-15 for load-time Pillow LANCZOS DPI-aware resizing/caching, and explicitly barred overwriting original source PNGs in `assets/icons/` without explicit Project Lead approval.

4. **S12 — Canonical `assets/splash.py` & `assets.splash._VERSION` Throughout (Qwen C-1 & GPT #3):**
   - Replaced every bare `splash.py` reference in S12 Context Pointers, Read-Only Source lists (keeping `assets/*` read-only), Pillar A/B audit inventories, and dropped bare `splash.py` from `compileall` (`assets` already covers `assets/splash.py`).
   - Updated `test_probe_8` parity check to verify `assets.splash._VERSION` (noting existing test alias `import assets.splash as splash`).
