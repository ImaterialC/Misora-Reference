# Misora: Story Editor — Master Change Specification & Session Plan (`v1.4.1` -> `v1.5.0`)

- **Repository:** `ImaterialC/Misora-Editor` (`D:\Misora-Editor`)
- **Starting Baseline:** `__version__ = "1.4.0"` (post-S24 hold; `misora.py` = 17,315 lines; 344 tests across 45 modules)
- **Target Release:** `v1.5.0` (incremented per session via `U00`: `1.4.1`..`1.4.7` -> `1.5.0`)
- **Purpose:** Canonical traceability ledger for Google Antigravity and peer AI cross-checking (GPT, Claude, Qwen, Grok, Gemini).

---

## 1. Preserved Phase 2.5 Hard Invariants (NEVER REOPEN)

1. Preserve binary `cmd_id == 35` (narration) and `cmd_id == 32` (subtitle) unchanged across every path (`DEF-02`).
2. Clearing a speaker adjacent to narration MUST keep boxes separate — never implicitly merge (`QW-B01`).
3. Multi-segment editing stays non-blocking with segment-aware Undo (`old_seg_texts`/`new_seg_texts`) and full `BoxSnapshot` preservation.
4. `.misora` v1 stores file references, view/scope state, and composite stable locks `(box_ordinal, sha256(original_jp_text))` ONLY — never drafts, binary blobs, or runtime `Record.uid`.
5. Native overflow rule: **50 digit-widths without a linebreak OR 3 or more linebreaks (4 or more lines)**, `wrap="none"` visible bleed in Preview, no auto-shrink, no copyrighted `AtlasAdv` sprites, Box 0 Summary unmeasured (`DEF-04`).
6. `All Script` mode in the right-side **MTL Drawer** stays strictly 2 `tk.Text` widgets + 5 static status tags (`NO-03`).
7. Worker threads NEVER call Tkinter APIs (including `after_idle`); communicate strictly via `queue.Queue` (`Rule 15`).
8. Translation Lock is enforced at the model/application layer, not just UI button state.
9. Dependencies remain strictly `stdlib + UnityPy + Pillow`. No destructive git commands (`reset/clean/stash/commit/push`). Never overwrite local untracked `misora_config.json`, print secrets/DPAPI blobs, or pollute repo `backups/` during unit tests.

---

## 2. Explicit Contract Amendments (Approved by Project Lead)

| Amendment | Previous Rule / Test | New Approved Contract | Target Session |
| :--- | :--- | :--- | :---: |
| **AMD-01 (`U00`)** | `misora-safety.md` §7 & `test_p3_s02_hygiene.py::test_guard_1_root_version_untouched` pinned `__version__ = "1.4.0"` across all sessions. | Adopt `A.b.c` policy: `A`=major total/product change, `b`=official milestone release after all sessions pass, `c`=incremented `+1` per completed session (`1.4.1`..`1.4.7` -> `1.5.0`). Root `__init__.py` remains the single version source. Update S02 guard test to assert cross-module parity with `__init__.__version__` rather than hardcoded `"1.4.0"`. | **S01** |
| **AMD-02 (`U06`)** | `test_p3_s17_pixel_rulers.py` asserted character counter removal. | Restore pixel-calibrated character/overflow indicator (NO literal `(max)` text), turning red on `>50d` or `>=4` lines, with `50 x 3` tooltip. Amend S17 test accordingly. | **S02** |
| **AMD-03 (`U08`/`U-7`)** | S13–S15 continuous view tests assumed multi-widget `_card_widgets` per box. | Refactor main editor `All Script` view to **Technique A**: 1 read-only `tk.Text` with cached clean-room Pillow inline headers (`image_create()`), clickable Select/Lock tags, single-click sync + double-click/Enter jump to Dialogue View. Keep `self.txt_continuous` as fallback widget. | **S03** |
| **AMD-04 (`U-5`)** | Preview used raw `Canvas.create_rectangle` primitives. | Permit cached clean-room Pillow rounded-frame `PhotoImage` assets generated locally (still strictly ZERO copyrighted `AtlasAdv` sprites). | **S03** |
| **AMD-05 (`U01`)** | `NO-09` prohibited `Import from XUAT` from touching XUAT `.txt` files. | Silent/global XUAT pruning remains FORBIDDEN. Opt-in, previewed, transactional post-import XUAT cleanup + mandatory archival backup + 2-stage empty-file deletion confirmation + manual `Tools -> Clean / Archive XUAT...` are APPROVED. | **S07** |

---

## 3. Complete 1:1 Coverage Matrix (All Confirmed Bugs + Wishlist Items)

| ID | Category | Summary | Confirmed Root Cause / Agreed Spec | Session | Version |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `BUG-01` | Stability (P1) | Search worker keeps running after Cancel / Exit | Shared boolean `search_cancel_flag` overwritten by new search; `os.walk` unchecked; `destroy()` sends no cancel. Fix with per-job `threading.Event` + bounded queue. | S01 | `1.4.1` |
| `BUG-02` | Stability (P1) | `Translate All` spawns 1 thread per Box | `translate_async()` creates unbounded `threading.Thread` in box loop and ignores `rate_limit_delay`. Fix with bounded `ThreadPoolExecutor` + cancel `Event`. | S01 | `1.4.1` |
| `BUG-03` | Memory Leak (P1) | `_mtl_all_*` dicts never pruned on close | `_mtl_all_req_seqs/results/statuses/errors` grow unbounded across opened/closed docs. Prune per document in `close_file`, `_close_all_documents_without_prompt`, `reload`. | S01 | `1.4.1` |
| `BUG-04` | Memory Leak (P1) | `load_bundle_story()` leaks `env` on error | Missing `try/except` `dispose_unity_env(env)` when TextAsset missing or `from_binary` fails. | S01 | `1.4.1` |
| `BUG-05` | Stability (P2) | `MisoraLogger.close()` can orphan writer thread | `put_nowait(None)` swallows `queue.Full`; clears `_writer_thread` after timeout. Add `_stop_event` + timed `get(timeout=0.1)` + flush. | S01 | `1.4.1` |
| `BUG-06` | Reliability (P1) | `_is_saving` global guard stuck `True` on `mkdir` error | `out_path.parent.mkdir()` runs before `try/finally`. Move `mkdir` & `tmp_path` init inside `try:`. | S01 | `1.4.1` |
| `BONUS-01` | Memory Leak (P1) | `sync_manager.jp_source_cache` & `_latest_applied_mtl_seq` never pruned | Monotonic `b_uid` entries accumulate across closed/reloaded docs. Prune by document UIDs on close/reload. | S01 | `1.4.1` |
| `BONUS-02` | Perf/RAM (P1) | `ssl.create_default_context()` called per box in MTL | Loads Windows OS root cert store per thread. Cache one shared SSL context in `core/mtl_engine.py`. | S01 | `1.4.1` |
| `BONUS-03` | Lifecycle (P2) | Idle 50ms/100ms polling + double bundle reload on `BulkFileDelta` | Poll `_mtl_queue` & `search_queue` only while active; avoid redundant `open_file(reload_from_disk=True)` after cache refresh in `_apply_delta`. | S01 | `1.4.1` |
| `U00` | Governance | `A.b.c` versioning & changelog contract | Single source in `__init__.py`; increment `c` per session (`1.4.1`..`1.4.7`), promote to `1.5.0` at release gate; blocked/reverted sessions never bump release. | S01 | `1.4.1` |
| `U04` | Branding | Rename user-facing product to `Misora: Story Editor` | Update titles, splash, About, README, docs; keep internal namespaces/config/extensions untouched; document Unit/Monster Editor direction only. | S01 | `1.4.1` |
| `U15` | Bug / Perf | Char measurement mismatch & O(L^2) measure loop | `_get_dialogue_measure_font` read missing `self.dialogue_font_family` instead of `self.prefs[...]`. Fix prefs lookup + fast full-line check & binary search. | S02 | `1.4.2` |
| `U16` | Typography | Global/JP dialogue font labels & tooltips | Label `Global — Nunito Bold` & `Japanese — nintendoP_Humming-E_002pr` with explanatory tooltip. | S02 | `1.4.2` |
| `U17` | Typography | Restrict built-in dialogue font list to 2 presets | Keep only Global & Japanese built-in options + safe migration for legacy `misora_config.json` fonts. | S02 | `1.4.2` |
| `U18` | Typography | User-managed custom fonts folder (`assets/fonts/`) | Separate Custom Fonts area + Win32 `AddFontResourceExW(..., FR_PRIVATE, 0)` / cleanup + `Refresh Fonts` + `.gitignore` proprietary JP font. | S02 | `1.4.2` |
| `U19` | UI / Ruler | Constant `Nunito Bold` horizontal ruler + fix `50d` overlap | Ruler `50d` boundary fixed to `Nunito Bold` regardless of dialogue font; fix `'50d'` / `'est. >50d'` label collision. | S02 | `1.4.2` |
| `U20` | UI / Gutter | Line numbers follow active dialogue font | Sync `gutter_clean` font, linespace, padding, and spacing in `_apply_theme_and_fonts_live()` and `_apply_gutter_overflow_tag()`. | S02 | `1.4.2` |
| `U06` | UI / Metrics | Restore pixel-calibrated char/overflow indicator | No literal `(max)`; turns red on `>50d` or `>=4` lines; `50 x 3` tooltip; updates on every central commit/navigation/undo. | S02 | `1.4.2` |
| `U08` | Performance | Fix All Script lag + leaked 3rd window above Raw View | Fix `_update_empty_state_visibility()` guard (`not var_continuous_view.get()`); eliminate redundant rebuilds & double `_update_raw_view()`; profile before/after. | S03 | `1.4.3` |
| `U-7` | Architecture | All Script Technique A (1 read-only `tk.Text` + inline headers) | Replace 100+ card widgets with 1 `tk.Text` + cached Pillow inline headers (`image_create()`), clickable Select/Lock, double-click/Enter -> Dialogue View. | S03 | `1.4.3` |
| `U-5` | Visual UX | Precision Priconne-like Dialogue & All Script Preview | Clean-room Pillow rounded frames matching reference Bandicam shots (Dialogue cream/gold capsule, narration has no nameplate, pink triangle; All Script white card + steel-blue speaker + dotted divider). | S03 | `1.4.3` |
| `4.1` | UX / Parity | Native Paste Box (`Ctrl+Alt+V`) Insert vs Replace chooser | Add 3-way dialog (`Insert after Box #N` / `Replace Box #N..#M` / `Cancel`), Lock-safe, 1 Undo batch. | S03 | `1.4.3` |
| `U09` | Layout | Move Undo & Redo out of NGUI Ribbon to right end of Edit Group | Right end of Edit Group (`[Box Actions] | [Player] | [Undo][Redo]`). | S04 | `1.4.4` |
| `U10` | Layout | Move Insert Player Name into Edit Group (just before Undo/Redo) | Precedence per Lead `4.2`: `[Box Actions] | [Player] | [Undo][Redo]`. | S04 | `1.4.4` |
| `U11` | Layout | Move VIEW group (`Select Box`, `All Script`, `Preview`) left of MTL/AI | Docked on Row 1 header left of MTL & AI Prompt icons. | S04 | `1.4.4` |
| `U12` | Layout | Move Edit Group up beside Speaker; NGUI Ribbon on Row 3 (default OFF) | Clean 2-row default workspace safe when both side drawers are open; NGUI Ribbon toggles cleanly on Row 3. | S04 | `1.4.4` |
| `U13` | Layout | Compact `Prev` and `Next` box buttons | Proportionally smaller without distorting icons/fonts. | S04 | `1.4.4` |
| `U14` | Layout | Icon-only `MTL` and `AI Prompt` buttons | Compact icon-only buttons with tooltips & accessible text fallback. | S04 | `1.4.4` |
| `U22` | Layout | Borderless lock icon placed before `"Dialogue"` label | Flat icon without frame box; tooltip & identical lock semantics. | S04 | `1.4.4` |
| `U03` | Drawer UX | Small button to fully minimize/close & reopen Left Drawer (`4.4`) | 0 px collapse + small discoverable reopen control + `View` menu toggle; preserves state & `winfo_exists()` guards. | S04 | `1.4.4` |
| `U-1` | Dock UX | Double-click `Search Results` tab opens Find bar | Bind `<Double-Button-1>` on `btn_tab_search` -> `on_show_find()`. | S04 | `1.4.4` |
| `U-2` | MTL UX | Move `Enabled Engines` from MTL Drawer to `Translator > Enabled Engines` | Init engine `BooleanVar`s before `_build_menu()` so menu & drawer stay synced. | S04 | `1.4.4` |
| `U-6` | MTL UX | Flip MTL Apply arrows to left & add `refresh.png` icon | Point Apply arrows left toward Editor; add `assets/icons/refresh.png` with Unicode fallback. | S04 | `1.4.4` |
| `U21` | Accessibility | High-clarity Checkbox & Radio states in Light & Dark themes | Distinct checked/unchecked/hover/focus/disabled visuals with `best_contrast_fg()`. | S04 | `1.4.4` |
| `U-3` | Speaker UX | Cyclic Jump to Speaker (`▼`) + Google-style autocomplete on `entry_speaker` | Dropdown jumps to speaker's first/next box with wrap-around; `entry_speaker` drops live-filtered popup on click/clear for renaming. | S05 | `1.4.5` |
| `U-4` | Speaker Safety | Notification clarity, no mid-keystroke commit, Translation Lock guard | Commit speaker rename only on `Enter`/select/`FocusOut`; enforce `is_box_locked()`; distinct toast messages for Jump vs Rename. | S05 | `1.4.5` |
| `U02` | Console | Windows Terminal Show/Hide toggle (`4.3` Option B) | `Debug > Show/Hide Windows Console` + `F12` via Win32 `GetConsoleWindow()` + `ShowWindow()`; safe under `pythonw.exe`. | S05 | `1.4.5` |
| `U05` | About UX | About `"Support Me"` dialog (`4.6`) | Lazy-loaded resized `assets/Service.gif` loop + cleanup on close, Indonesian caption, Ko-fi/Patreon/PayPal icons (`https://paypal.me/CorneliaCrimson`, `SHOW_PAYPAL_BUTTON = True`). | S05 | `1.4.5` |
| `U07` | Tools / Import | Top-level `Tools` menu + `Auto Word Wrap` (`4.5`) | Pixel-calibrated `50d x 3` reflow aware of NGUI tags, `{playername}`, EN/JP, multi-seg, Lock, 1 Undo batch; opt-in on Import + manual `Tools -> Auto Word Wrap...`. | S06 | `1.4.6` |
| `U01` | XUAT Workflow | Transactional Post-Import XUAT Cleanup, Archive, & `Debug > Safety` | Conservative 3-tier classification (applied / unique right-side / uncertain unchecked), duplicate & linebreak options, Combined & Per-File archives + traceability headers, `.xuat.old` default outside `Text/` + `.txt` warning, `Debug > Safety` backup toggle, 2-step empty file deletion, `Tools -> Clean / Archive XUAT...`. | S07 | `1.4.7` |
| `GATE` | Release Gate | Final Audit, Memory Stress Verification, & `v1.5.0` Promotion | Stress test cycles, full test suite, manual Windows QA checklist, promote `CHANGELOG.md` & `__version__ = "1.5.0"`. | S08 | `1.5.0` |

**Coverage Check:** 100% of items mapped (0 dropped, 0 duplicated).
