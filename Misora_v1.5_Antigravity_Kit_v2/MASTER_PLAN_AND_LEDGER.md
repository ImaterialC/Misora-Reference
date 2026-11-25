# Misora: Story Editor — Master Change Specification & Session Plan v2 (`v1.4.1` -> `v1.5.0`)

- **Repository:** `ImaterialC/Misora-Editor` (`D:\Misora-Editor`)
- **Reference Kit Repository:** `ImaterialC/Misora-Reference`
- **Target Release:** `v1.5.0` (incremented per completed session via `U00`: `1.4.1`..`1.4.7` -> `1.5.0`, gated on honest Release Gate criteria)
- **Kit Status:** **REVISION v2 — SUBMITTED FOR INDEPENDENT REVIEW (NOT IMPLEMENTATION-AUTHORIZED YET)**

---

## 1. Baseline & Source-State Reconciliation (Explicitly Distinguished)

Two different read-only snapshots of `Misora-Editor` were observed during pre-kit audits. Neither remote snapshot is assumed authoritative over the live local disk; **S01 Preflight MUST verify and pin the exact local starting commit before any code edit**:

1. **Public GitHub `ImaterialC/Misora-Editor` (`main`) Snapshot (inspected by GPT):**
   - `PROJECT_STATE.md`: S23 complete, S24 listed as next session.
   - `__init__.py`: `__version__ = "1.4.0"`.
   - `CHANGELOG.md`: `## [Unreleased] (Target: v1.4.1)` up through S23.
   - Recorded test baseline: `344` tests (`304` passed, `35` skipped, `3` failures, `2` errors linked to unavailable proprietary fixture `storydata_1001005.unity3d`).
2. **Google Drive Synced `Misora-Editor` + `Misora-Reference` Snapshot (inspected by Gemini):**
   - `PROJECT_STATE.md` & `CHANGELOG.md`: include S24 Final Acceptance Audit & Release Gate Hold (`__version__ = "1.4.0"`, `344` tests: `304` pass, `35` skip, `3` fail, `2` error due to missing `storydata_1001005.unity3d`).
   - `misora.py`: 796,849 bytes / 17,315 lines; split reference SHA `ec4d9bfc8ec60885` in `Misora-Reference/references/misora_parts/`.
3. **Authoritative Local Workspace `D:\Misora-Editor` (Pinned Live in S01 Preflight):**
   - S01 Preflight MUST record and distinguish:
     1. Public GitHub remote branch & commit (`git rev-parse origin/main` if available),
     2. Local `D:\Misora-Editor` branch & `HEAD` commit (`git branch --show-current`, `git rev-parse HEAD`),
     3. Pre-existing local uncommitted changes & untracked files (`git status --short`),
     4. Whether S24 has actually been completed and/or committed locally (verified on disk in `CHANGELOG.md`, `PROJECT_STATE.md`, and `tests/test_phase4_import_export_preview.py`),
     5. The exact reproducible starting commit/snapshot from which S01 begins.
   - **NEVER overwrite or discard local work merely to synchronize with GitHub.**

---

## 2. Preserved Phase 2.5 Hard Invariants (NEVER REOPEN)

1. Preserve binary `cmd_id == 35` (narration) and `cmd_id == 32` (subtitle) unchanged across every path (`DEF-02`).
2. Clearing a speaker adjacent to narration MUST keep boxes separate — never implicitly merge (`QW-B01`).
3. Multi-segment editing stays non-blocking with segment-aware Undo (`old_seg_texts`/`new_seg_texts`) and **full lossless `BoxSnapshot` preservation** (`speaker`, `voice_cue`, `kind`, `seg_texts`, `raw_breaks`, `extra_args`).
4. `.misora` v1 stores file references, view/scope state, and composite stable locks `(box_ordinal, sha256(original_jp_text))` ONLY — never drafts, binary blobs, or runtime `Record.uid`.
5. Native overflow rule: **50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)**, `wrap="none"` visible bleed in Preview, no auto-shrink, ZERO copyrighted `AtlasAdv` sprites, Box 0 Summary unmeasured (`DEF-04`).
6. `All Script` mode inside the right-side **MTL Drawer** stays strictly 2 `tk.Text` widgets + 5 static status tags (`NO-03`).
7. Worker threads NEVER call Tkinter APIs (including `after_idle`); communicate strictly via `queue.Queue` (`Rule 15`) with per-job `threading.Event` cancellation AND bounded workers PLUS finite pending-work backpressure.
8. Translation Lock is enforced at the model/application layer across all mutation paths, not only UI button state.
9. Dependencies remain strictly `stdlib + UnityPy + Pillow`. No destructive git commands (`reset/clean/stash/commit/push`). Never overwrite untracked `misora_config.json`, print secrets/DPAPI blobs, pollute repo `backups/` during unit tests, or commit proprietary commercial fonts.

---

## 3. Explicit Contract Amendments (Approved by Project Lead)

| Amendment | Previous Rule / Test | New Approved Contract | Target Session |
| :--- | :--- | :--- | :---: |
| **AMD-01 (`U00`)** | `misora-safety.md` §7 & `test_p3_s02_hygiene.py::test_guard_1_root_version_untouched` pinned `"1.4.0"` across all sessions. | Adopt `A.b.c` policy: `A`=major total/product pivot, `b`=official milestone release after all planned sessions and release gates pass, `c`=incremented `+1` per completed session (`1.4.1`..`1.4.7` -> `1.5.0`). Root `__init__.py` remains the sole version source; other modules derive from it (no hardcoded duplicates). Update S02 guard test to verify dynamic parity with `__init__.__version__`. | **S01** |
| **AMD-02 (`U06`)** | `test_p3_s17_pixel_rulers.py` asserted character counter removal. | Restore pixel-calibrated character/overflow indicator (NO literal `(max)` text), turning red on `>50d` or `>=4` lines, with `50 x 3` tooltip. Amend S17 test accordingly. | **S02** |
| **AMD-03 (`U08`/`U-7`)** | S13–S15 continuous view tests assumed multi-widget `_card_widgets` per box. | Refactor main editor `All Script` view to **Technique A**: 1 read-only `tk.Text` with cached clean-room Pillow inline headers (`image_create()`), clickable Select/Lock tags, single-click sync + double-click/Enter jump to Dialogue View. Keep `self.txt_continuous` as plain-text fallback. | **S03** |
| **AMD-04 (`U-5`)** | Preview used raw `Canvas.create_rectangle` primitives. | Permit cached clean-room Pillow rounded-frame `PhotoImage` assets generated locally (still strictly ZERO copyrighted `AtlasAdv` sprites). | **S03** |
| **AMD-05 (`4.1`)** | `BoxEditDelta` only tracked `speaker`/`text`/`seg_texts` (insufficient for lossless `BoxSnapshot` Replace). | Add `BoxSnapshotReplaceDelta` in `core/undo_journal.py` + `StoryDocument.replace_box()` in `core/story_ast.py` so Replace mode preserves all 6 `BoxSnapshot` fields (`speaker`, `voice_cue`, `kind`, `seg_texts`, `raw_breaks`, `extra_args`) losslessly across Replace, Undo, and Redo. | **S03** |
| **AMD-06 (`U01`)** | `NO-09` prohibited `Import from XUAT` from modifying XUAT `.txt` files. | Silent/global XUAT pruning remains FORBIDDEN. Opt-in, SHA-256-verified, previewed, per-file transactional post-import XUAT cleanup + **mandatory archival backup** (requiring explicit separate irreversible confirmation to opt out) + 2-stage empty-file deletion confirmation + manual `Tools -> Clean / Archive XUAT...` are APPROVED. | **S07** |

---

## 4. Complete 1:1 Coverage Matrix (All Confirmed Bugs + Wishlist Items)

| ID | Category | Summary | Confirmed Root Cause / Agreed Spec (v2 Hardened) | Session | Version |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `BUG-01` | Stability (P1) | Search worker keeps running after Cancel / Exit | Per-job `threading.Event`; bounded `search_queue` with cancellation-aware `put(timeout=0.05)` loop; cancel checks in `os.walk`, dir/file loops, file scan, queue submit, and `destroy()`. | S01 | `1.4.1` |
| `BUG-02` | Stability (P1) | `Translate All` spawns 1 thread per Box | Bounded worker pool (`max_workers=3`) **PLUS** finite pending-work limit / producer backpressure (bounded `Semaphore`/queue; never blocks Tk UI); per-batch cancel `Event` on close/engine-switch/shutdown; cooperative cancel guarantees documented; respects `rate_limit_delay` & timeouts. | S01 | `1.4.1` |
| `BUG-03` | Memory Leak (P1) | `_mtl_all_*` state never pruned on close | Prune `_mtl_all_req_seqs/results/statuses/errors`, `_mtl_all_selected_uid`, `_mtl_all_last_ctx`, `_mtl_all_block_ranges`, `_mtl_drawer_active_context` on close/reload; prevent late worker completions from repopulating pruned state. | S01 | `1.4.1` |
| `BUG-04` | Memory Leak (P1) | `load_bundle_story()` leaks `env` on error | Dispose `env` on every failure path when ownership has NOT been transferred to the caller; never dispose an owned live env. | S01 | `1.4.1` |
| `BUG-05` | Stability (P2) | `MisoraLogger.close()` can orphan writer thread | Idempotent `close()`, concurrent-producer safe after shutdown starts, `_stop_event` + timed `get(timeout=0.1)` so full queue never drops stop signal, never clear `_writer_thread` while still alive. | S01 | `1.4.1` |
| `BUG-06` | Reliability (P1) | `_is_saving` global guard stuck `True` on `mkdir` error | Move `mkdir` and `tmp_path` init inside `try/finally` so `_is_saving` always resets. | S01 | `1.4.1` |
| `BONUS-01` | Memory Leak (P1) | `sync_manager.jp_source_cache` & `_latest_applied_mtl_seq` never pruned | Safe per-UID `unregister_jp_keys(uids)` (NOT global clear) + prune `_latest_applied_mtl_seq` & per-UID sequences on close/reload. | S01 | `1.4.1` |
| `BONUS-02` | Perf/RAM (P1) | `ssl.create_default_context()` called per box in MTL | Cache one shared thread-safe SSL context in `core/mtl_engine.py`. | S01 | `1.4.1` |
| `BONUS-03` | Lifecycle (P2) | Idle polling + double reload in `BulkFileDelta` | Poll `_mtl_queue` & `search_queue` only while active; remove redundant `open_file(reload_from_disk=True)` in `_apply_delta(BulkFileDelta)` ONLY while demonstrably refreshing all model/cache/UI state. | S01 | `1.4.1` |
| `U00` | Governance | `A.b.c` versioning & changelog contract | Single source in `__init__.py` (compiled via `compileall`); increment `c` per session (`1.4.1`..`1.4.7`), promote to `1.5.0` ONLY when release gate passes; blocked/reverted sessions never bump release. | S01 | `1.4.1` |
| `U04` | Branding | Rename user-facing product to `Misora: Story Editor` | Update titles, splash, About, README, docs; keep internal namespaces/config/extensions untouched; document Unit/Monster Editor direction only. | S01 | `1.4.1` |
| `U15` | Bug / Perf | Char measurement mismatch & O(L^2) measure loop | Fix `self.prefs[...]` lookup in `_get_dialogue_measure_font` & `_apply_gutter_overflow_tag`; full-line fast-path + O(log L) binary search. | S02 | `1.4.2` |
| `U16`–`U18` | Typography | Global/JP 2 presets + Custom Fonts (`assets/fonts/`) | `Global — Nunito Bold` & `Japanese — nintendoP_Humming-E_002pr` presets + separate Custom Fonts area with Win32 `AddFontResourceExW(..., FR_PRIVATE, 0)` / cleanup + `.gitignore` proprietary JP font. | S02 | `1.4.2` |
| `U19`–`U20` | Ruler / Gutter | Constant `Nunito Bold` ruler + overlap fix + gutter sync | Constant `50d` ruler anchored to `Nunito Bold`; fix `'50d'`/`'>50d'` overlap; sync `gutter_clean` font/linespace/padding to active dialogue font. | S02 | `1.4.2` |
| `U06` | Metrics UI | Restore pixel-calibrated char/overflow indicator | No literal `(max)`; turns red on `>50d` or `>=4` lines; `50 x 3` tooltip; updates on every central commit/navigation/undo. | S02 | `1.4.2` |
| `U08` / `U-7` | Perf / Arch | All Script Technique A + fix leaked 3rd window | Fix `_update_empty_state_visibility()` guard; 1 read-only `tk.Text` + cached clean-room Pillow inline headers (`image_create()`); clickable Select/Lock; double-click/Enter -> Dialogue View. | S03 | `1.4.3` |
| `U-5` | Visual UX | Precision Priconne-like Dialogue & All Script Preview | Clean-room Pillow rounded frames matching Bandicam references (narration has NO nameplate, `wrap="none"` visible bleed, ZERO `AtlasAdv`). | S03 | `1.4.3` |
| `4.1` | Data Integrity | Native Paste Box (`Ctrl+Alt+V`) Lossless Insert vs Replace | 3-way dialog (`Insert` / `Replace` / `Cancel`); lossless `BoxSnapshotReplaceDelta` preserving all 6 `BoxSnapshot` fields across Replace/Undo/Redo; staged atomic validation; Lock-safe. | S03 | `1.4.3` |
| `U09`–`U14`, `U22`, `4.2` | Layout | 3-row header/ribbon layout (`NGUI Ribbon` default OFF) | Row 1: flat Lock + Dialogue + VIEW group + icon-only MTL/AI + compact Prev/Next + overflow/counter; Row 2: Speaker + Edit Group (`[Box Actions] | [Player] | [Undo][Redo]`); Row 3: NGUI Ribbon default OFF. | S04 | `1.4.4` |
| `U03`, `U-1`, `U-2`, `U-6`, `U21` | Drawers / UX | Left Drawer minimize + lifecycle, Search dblclick, MTL controls, Checkbox clarity | 0 px Left Drawer minimize/reopen without unnecessary view rebuilds; repeated toggle/resize/minimize tests; Search tab dblclick -> Find; `Enabled Engines` -> `Translator` menu; left `←` Apply arrows + `refresh.png`; WCAG checkbox/radio clarity. | S04 | `1.4.4` |
| `U-3` / `U-4` | Speaker UX | Cyclic Jump (`▼`) + Google-style Autocomplete + FocusOut & Lock safety | `▼` cyclic jump + toast; `entry_speaker` popup autocomplete; deferred FocusOut ignores focus moving into popup; Lock-enforced commit; distinct Jump vs Rename toasts. | S05 | `1.4.5` |
| `U02` | Console | Win32 Console Show/Hide (`4.3` Option B) | Query `IsWindowVisible(hwnd)` BEFORE `ShowWindow(SW_HIDE/SW_SHOW)`; safe under `python.exe` and `pythonw.exe`; `Debug` menu + `F12`. | S05 | `1.4.5` |
| `U05` | About UX | About `"Support Me"` with sequential streaming GIF & links | Local preflight for `assets/Service.gif`; sequential frame decoding reusing a single `PhotoImage` (no retaining every decompressed frame); stop timer & close PIL handle on close; exact Indonesian caption; Ko-fi/Patreon/PayPal (`https://paypal.me/CorneliaCrimson`, `SHOW_PAYPAL_BUTTON = True`). | S05 | `1.4.5` |
| `U07` / `4.5` | Tools / Import | Top-level `Tools` menu + NGUI/Grapheme-aware `Auto Word Wrap` | Reflow preserving NGUI tags, placeholders, EN/JP, multi-seg, intentional whitespace, malformed tags, Unicode grapheme boundaries, existing breaks, Locks, immutable JP keys, 1 Undo batch; opt-in on Import + manual `Tools -> Auto Word Wrap...`. | S06 | `1.4.6` |
| `U01` | XUAT Workflow | Transactional XUAT Cleanup, Mandatory Archive, & `Debug > Safety` | Pure-core `core/xuat_cleanup.py` with injected backup-path callback; mandatory archive (separate irreversible confirmation to opt out); per-file archive preserves original bytes, combined archive uses canonical UTF-8/LF + source encoding/BOM/EOL metadata; SHA-256 stale-file abort; per-file transaction with archive-first order + granular report; `.xuat.old` outside `Text/` + `.txt` warning; 2-step empty-file delete; `Tools -> Clean / Archive XUAT...`. | S07 | `1.4.7` |
| `GATE` | Release Gate | Honest Release Gate, Deep Memory Stress (`weakref`/`tracemalloc`), & `v1.5.0` | Separate acceptance/stress tests from failing-first probes; `weakref`+`gc.collect()`+`tracemalloc` plateau + thread/queue checks; reproducible benchmark context; missing proprietary fixture stays `BLOCKED` (no artificial green / no forced bump to `1.5.0`); stop if source defect found outside Allowed Files. | S08 | `1.5.0` |

**Coverage Check:** 100% of items mapped (0 dropped, 0 duplicated).
