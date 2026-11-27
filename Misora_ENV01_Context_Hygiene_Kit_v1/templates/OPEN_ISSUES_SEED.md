# Misora: Story Editor — Open Issues & Post-S11e Triage Ledger

> **Status:** Active Backlog (Post-`S11e` `v1.4.15` | `S12` Paused | `v1.5.0` ON HOLD)
> **Rule:** Never mix product bugs, test debt, missing fixtures, pending manual QA, and deferred enhancements into one flat list.

---

## A. Confirmed Active Product Bugs (Pre-v1.5.0 Triage Priority)

| ID | Legacy Ref | Severity | Status | Description & Closure Criteria |
|---|---|---|---|---|
| **T-01** | `BUG-UI-EMPTY-STATE-01` | P1 | `OPEN` | Purple `Open Files` empty-state button + drag-and-drop caption remains visible below `txt_dialogue` when bundles (`1381002.unity3d`, `1380003.unity3d`) are open, obscuring the bottom border and `clean_scroll_x`. Repro must cover: open 2 docs, close 1, close all, switch Dialogue/All Script, and `_deferred_restore()`. |
| **T-02** | `u-08` | P2 | `OPEN` | Tooltip next to the `Next` button still displays stale `"50x3"` limit instead of `"54d x 3"`. |
| **T-03** | `u-05` | P1/P2 | `OPEN` | Using `Pin` in `All Script` view causes box selection to turn into multi-select: every speaker jump adds boxes to selection. |
| **T-04** | `u-02` | P2 | `OPEN` | Red overflow marker is not yet applied to line 4+ (`>3L`) in addition to horizontal `>54d` overflow. |

---

## B. Naming, Path Configuration & Lightweight UX Candidates

| ID | Legacy Ref | Type | Status | Description |
|---|---|---|---|---|
| **T-05** | `u-01` | Config / Naming | `TRIAGE` | Remove hardcoded framework examples (frameworks vary, e.g., BepInEx, Daring Tact for Android compatibility; XUnity.AutoTranslator is a plugin, not a framework). Rename `Project Folder` -> `Game Folder` (auto-detecting preset subfolders when present). Expose 3 individually editable paths: (1) `Game Folder`, (2) `RedirectedResources` folder, (3) `XUnity.AutoTranslator Text Folder` (multi-language/multi-framework safe). Avoid unofficial abbreviation `"XUAT"` where UI space permits; audit UI naming across dialogs/menus. |
| **T-06** | `u-03a` | UX | `TRIAGE` | Separate remembered default Save directories for **Save Project (`.misora`)** vs **Save / Patch Bundle (`Ctrl+Shift+S`)**. |
| **T-07** | `u-07` | Tooltip UX | `PROPOSAL` | Extend lazy 350ms tooltips to informative non-button UI labels & remaining surfaces: voice cue audio filename code, `X seg` typing-pause count, `Opened Files` drawer tab & `Open...` button, `Box x/max` indicator, `Customize` & `NGUI Glossary` tabs, `Search Results` panel, and any remaining controls inside `Import from XUAT`. |

---

## C. UI Ribbon Redesign & Selection Proposals (Require Design Sign-Off Before Code)

| ID | Legacy Ref | Type | Status | Description |
|---|---|---|---|---|
| **T-08** | `u-11` | UI Redesign | `PROPOSAL` | Relocate `x/54d · 4/3L Box y/Z` so `Prev`/`Next` buttons stay horizontally stationary across boxes. Project Lead proposed a 4-row ribbon (Row 1 Info: `[select check] [lock] [0/42] [Title] [Subtitle] [char/line] [selected] [Select All] [Select None]`, Row 2 View Nav, Row 3 MTL/AI/Edit, Row 4 NGUI), View-menu toggles for header info items (View-type label default OFF; `Title -> Subtitle` coupled toggle where disabling Title disables Subtitle, while Title-only is allowed), and removing the ribbon `Select Box` toggle since box checkboxes remain visible (hideable via View menu). Evaluate compact height impact on 768p/125%-DPI screens before coding. |
| **T-09** | `u-12` | Toolbar UI | `PROPOSAL` | Add explicit `Insert Box`, `Replace Box`, and tri-state `Select All Box` buttons (cycling `Select All` / `Some selected` / `Select None` matching `Import from XUAT`). |
| **T-10** | `u-06` | All Script UI | `PROPOSAL` | Apply card-level visual highlight to Selected Boxes (beyond checkbox state) alongside active-box highlight in `All Script` view without degrading virtualized card pool latency. |

---

## D. Revalidation Items, Test Hygiene Debt, Fixture Blockers & Manual QA Pending

### D.1 Legacy Items Requiring Manual Revalidation
- **`AGENTS.md §29` — Ribbon Cut after navigation:** Confirm current status on Windows `v1.4.15` before S12.
- **`AGENTS.md §29` — Paste Box Insert/Replace:** Confirm current status on Windows `v1.4.15` before S12.
- **`Q-04.1.2` / `Q-04.1.3`:** Needs Project Lead repro confirmation if still applicable.

### D.2 Non-Fixture Automated Test Hygiene Debt (3 FAILs — Scheduled for S12)
1. `tests/test_v15_s01_stability_remediation.py::test_probe_8` — hardcoded `'1.4.1'` expectation (`'1.4.15' != '1.4.1'`).
2. `tests/test_phase3_performance_config.py::test_05` — local `misora_config.json` isolation hygiene.
3. `tests/test_s9c_workspace_safety.py::test_04` — default config template contract hygiene.

### D.3 Environment / Fixture Blocker & Intermittent Watch-Item
- **Missing Proprietary Fixture (`storydata_1001005.unity3d`):** Causes `3 FAIL + 2 ERROR` in `test_s8b2_memory_guards` and `35` `@skipUnless` skips across the test suite. Requires real fixture or written Project Lead waiver at S12 Gate 2.
- **`Tcl_AsyncDelete` Cross-Test GC Race (`Watch-Item`):** Intermittent CPython/Tk teardown abort during monolithic single-process discovery (aborted in S11c/S11d; completed cleanly in S11e at 475/475). Audit under S12 Pillar C.

### D.4 Manual Windows QA Items (`MANUAL-PENDING`)
- **S11c:** Manual `Ctrl+Z` Undo verification after `Import from XUAT` following a Quick Edit change.
- **S11d `Q-08`:** Manual post-import Synopsis Undo/Redo verification.
- **S11d `Q-11`:** Manual MTL Globe check on `DeepL` card and when `Box 0` is active.

---

## E. Deferred Features & Core Limitations (Track B / Post-v1.5.0)

| ID | Legacy Ref | Category | Description |
|---|---|---|---|
| **T-11** | `u-03b` | Feature Proposal | Read-only **Original Data** panel beside `Raw Commands` (including original speaker/actor names) acting as permanent translation reference / "Master Undo" even after bundle save/commit (pairs naturally with `T-13` archive storage). |
| **T-12** | `U-04` / `S11b2` | Performance (Track B) | Move `Ctrl+Shift+S` XUnity.AutoTranslator scan/write (`~2.899s` on 1,814 files, accepted via Option A waiver) to a background worker thread (`AGENTS.md §15`-safe) for 0 ms UI responsiveness. |
| **T-13** | `u-10` | Safety / Backup Proposal | Optional `XUnity.AutoTranslator`-format text backup generated on `Ctrl+Shift+S` (matching Import backup format with distinct source naming: datamine vs plugin-generated) so backups are human-auditable and selectively re-importable without re-datamining. |
| **T-14** | `u-09` & `u-13` | CI/CD Infrastructure | Tag-triggered (`v*`) GitHub Actions release pipeline automatically building `.zip` + `.exe` artifacts per version release for fast rollback. |
| **DEF-01** | `Grok-B07` / `QW-B19` | Core Limitation | `core/story_ast.py:to_binary()` encodes empty args as `" "` sentinel (preserves binary arity; causes trailing spaces on cleared multi-segment boxes after binary reload; stable on re-serialization). Accepted via S11c Option A. |
| **DEF-02..10** | Phase 2.5 Ledger | Deferred Architecture | Binary ID verification (`35`/`32` vs `9`/`61`), Multi-TextAsset selector, Box 0 in-game measurement, Dataminer rewrite, measure-first perf items, and **`DEF-10` modular decomposition of 1 MB `misora.py`** (post-`v1.5.0`). |
| **Track B Big** | Roadmap v5 | Future Features | `Q-18` true ruby above-text renderer, `BIG-01` MTL overhaul, `BIG-02` MeCab furigana, `BIG-03` glossary/dictionary system.
