# MISORA EDITOR — FINAL LOCKED S2 PROMPT (GOOGLE ANTIGRAVITY)

> **Status:** UNANIMOUS LOCK by GPT, Qwen, and Gemini on 2026-11-22.
> **Execution Target:** Google Antigravity on D:\Misora-Editor (Windows, Python 3.12).
> **Next Action:** Commit S0+S1 in Misora-Editor, then paste this prompt into Antigravity with /plan.

`plaintext
/plan Implement S2: Minimum Per-Document Dirty Contract and Explicit `on_save() -> bool` Return Value in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_s1_open_file_safety.py @tests/test_phase2_required.py @tests/

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate (STRICT):
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`), produce a clear **Implementation Plan artifact**, and WAIT for the user to approve (`Proceed`) before editing any file.
   - After approval (`Proceed`), execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. Workspace & Commit Hygiene Check:
   - Report actual local Git branch, `HEAD` commit hash, and `git status --short`.
   - S0 + S1 should be committed locally before S2 edits begin so `git diff` stays clean and reversible. If uncommitted S0/S1 edits or any unexpected local modifications exist, STOP and report them clearly in the Implementation Plan before proposing edits.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive checkout, `git commit`, or `git push`.
3. Allowed File Ownership (after approval):
   - `misora.py` (scoped strictly to per-document dirty tracking, no-op `<KeyRelease>` guards, flag-only `_mark_document_dirty()`, pure-UI `_dirty_state_changed()`, per-document saved-state checkpoint for Undo/Redo, cache-hit title/dock parity, and `on_save() -> bool`)
   - Focused new test file `tests/test_s2_dirty_contract.py`
   - `PROJECT_STATE.md` (measured S2 verification update + S8b-1..4 roadmap split ledger + confirmed-latent S7/F20 note for `_commit_widget_edit()` speaker `inject_box(..., None)`)
   - DO NOT modify `core/undo_journal.py`, `core/story_ast.py`, `core/bundle_io.py`, or any other `core/` module.
4. No new external dependencies. Follow all `AGENTS.md` architectural invariants (especially Rule 13 anti-UNDO-STORM and Rule 15 main-thread Tk safety). Do NOT use `/swarm`, `/teamwork`, or `/boost`.
5. Never remove, skip, weaken, or silently mock existing tests (including `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking`). Note: `test_phase3_performance_config.py::test_05_clean_committed_config_has_no_machine_paths` is a known pre-existing failure on this machine due to untracked local `misora_config.json`; re-measure honestly and do NOT modify or weaken it.
6. Stop strictly after S2. Do NOT implement S3 (`_save_document_entry`, `close_file()` abort, `_on_app_exit()` Save-All loop, raw plain-text save `F-GPT-04`, shared `write_atomic_utf8`), S5 (`BulkFileDelta` direct-to-disk checkpointing / multi-file Replace-All), S6 (Batch/MTL threading redesign), or S7 (full per-file `MasterUndoJournal` revision rewrite `F16` or speaker central-commit `F20`).

==================================================
PART 1 — PREFLIGHT REPORT (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live `misora.py` and `tests/` directly from disk and report:
- Current Git branch, `HEAD` commit hash, `git status --short`, and active Python 3.12 interpreter path/version (`py -3.12` preferred).
- Exact current implementations (by function name and live lines) of:
  1. `_dirty_state_changed()` and `_refresh_opened_files_list()`.
  2. `txt_dialogue` `<KeyRelease>` -> `_commit_widget_edit()` -> `_on_dialogue_edited()`, and `entry_speaker` `<KeyRelease>` -> `_on_speaker_edited()`.
  3. All mutation paths that currently rely on `_dirty_state_changed()` or set `self.is_dirty` directly, specifically auditing: `on_box_new()`, `on_box_cut()`, `on_box_paste()`, `on_paste_cross_box()` / script import apply, continuous speaker commit, continuous plain-text commit, `on_clear_dialogue_skeleton()`, `on_replace_next()`, current-file branch of `on_replace_all()`, BOTH MTL apply paths (`on_translate_current_box()`'s inner `update_ui()` AND `TranslatorAssistantDialog._on_apply()`), `BatchTranslateDialog.worker()` + `finish()`, and Undo/Redo (`on_undo()`, `on_redo()`, `_apply_delta()`).
  4. `open_file()` cache-hit sequence (specifically where window title is updated relative to restoring `entry["dirty"]`) and the exact key in `open_documents[path]` that stores plain-text content.
  5. `on_save()` end-to-end (every pre-`try` operation such as `_get_backup_dir()`, `_on_box0_metadata_edited()`, `_sync_continuous_box_from_widget()`, `inject_box()`, every primary bundle/v2/plain-text branch, optional XUAT sync block and where `_modified_boxes` is cleared, error branches, and current callers including shortcut wrappers, `close_file()`, and `_on_app_exit()`).
  6. Quote the EXACT assertions of `tests/test_phase2_required.py::test_34_undo_to_saved_revision_clears_dirty` (including its synthetic `current_file_path = tmp_txt` setup relative to `open_documents`) and `test_39_revision_dirty_tracking`, surfacing any compatibility nuance BEFORE editing.

==================================================
PART 2 — ROOT PROBLEMS & REQUIRED S2 IMPLEMENTATION
==================================================

### A. Single Source of Truth Per-Document Dirty Contract & Flag-Only Helper
- Make `open_documents[path]["dirty"]` the **single authoritative unsaved flag per document** (and mirror `self.is_dirty` strictly from the active document's authoritative flag when present, or `False` when no document is open).
- Introduce a dedicated **FLAG-ONLY** helper `_mark_document_dirty(file_path)`:
  * Mutates flags ONLY: sets `self.open_documents[file_path]["dirty"] = True` if `file_path in self.open_documents`, and sets `self.is_dirty = True` if `file_path == self.current_file_path`.
  * Performs **ZERO Tk calls** and **ZERO dock/title rebuilds** (strictly prevents Rule 13 UNDO-STORM during batch/undo loops and Rule 15 worker-thread Tk violations).
- Call `_mark_document_dirty(target_path)` explicitly after EVERY actual mutation across all audited mutation sites, and invoke `_dirty_state_changed()` **exactly ONCE** per user operation (for batch/undo/redo paths, invoke `_dirty_state_changed()` ONCE AFTER the entire batch/delta loop completes):
  * Dialogue & Box 0 edits, speaker edits, `on_box_new()`, `on_box_cut()`, `on_box_paste()`, `on_paste_cross_box()` / script import apply, continuous speaker & plain-text commits, `on_clear_dialogue_skeleton()`, `on_replace_next()`, current-file branch of `on_replace_all()` (multi-file Replace-All remains S5), BOTH MTL apply paths (`on_translate_current_box()`'s inner `update_ui()` AND `TranslatorAssistantDialog._on_apply()`), and Undo/Redo delta application.
  * **`BatchTranslateDialog` Rule 15 Constraint:** `worker()` may ONLY update plain Python dict/flag state via flag-only `_mark_document_dirty(target_path)` (ZERO Tk calls from the worker); ALL title/dock/undo-control synchronization MUST occur on the main thread inside the existing `finish()` `after_idle` callback. Do NOT redesign S6 threading in S2; note any remaining concurrency caveat in the plan.
- Set a document's dirty flag to `False` ONLY when:
  1. That specific document is freshly loaded from disk (`open_file()` fresh load or successful `reload_from_disk=True`), OR
  2. That specific document's own primary persistence in `on_save()` genuinely succeeds, OR
  3. An Undo/Redo operation restores THAT specific document's actual in-memory state back to its own saved-state checkpoint (see Section C below).
- **NEVER** derive or overwrite `open_documents[path]["dirty"]` or `self.is_dirty` from global `self.undo_journal.is_clean(...)`.
- Refactor `_dirty_state_changed()` to perform **pure UI synchronization only** (window title `*`, Opened Files dock list, undo/redo button state):
  * When `self.current_file_path in self.open_documents`, mirror `self.is_dirty = bool(self.open_documents[self.current_file_path]["dirty"])`.
  * When `self.current_file_path` is NOT `None` and has NO entry in `self.open_documents` (e.g., `test_34`'s synthetic `tmp_txt` path), **PRESERVE** the current `self.is_dirty` value (do NOT reset it to `False`) and refresh title/dock/controls from it.
- Update `_refresh_opened_files_list()` to read the single authoritative `info["dirty"]` entry flag (remove the dual `info.get("dirty") or (is_active and self.is_dirty)` expression), and fix `open_file()` cache-hit switching so the window title is refreshed **AFTER** restoring `entry["dirty"]`, guaranteeing title `*` and dock `*` never disagree.

### B. Guard Non-Mutating `<KeyRelease>` Handlers (Prevent False-Dirty)
- Update `_on_dialogue_edited()` so it compares actual old vs. new text BEFORE mutating state; if nothing changed, return cleanly without setting `self.is_dirty`, `open_documents[path]["dirty"]`, or `_modified_boxes`, and without calling `_dirty_state_changed()`.
- Update `_on_speaker_edited()` so it compares actual old vs. new speaker (and any associated committed state) BEFORE marking dirty; a no-op `<KeyRelease>` (e.g., arrow key, Shift, Ctrl) MUST leave a clean document completely clean and leave `_modified_boxes` untouched.
- **Confirmed-Latent Boundary (`Q5(b)`):** Do NOT modify `_commit_widget_edit()`'s currently unreachable speaker branch (`inject_box(..., None)`) in S2; record it explicitly in `PROJECT_STATE.md` as a confirmed-latent P0 defect owned by **S7/F20** (when speaker edits are routed through central commit), and do NOT exercise that latent branch in S2 tests.

### C. Deterministic Per-Document Saved-State Checkpoint for Undo/Redo (No `core/undo_journal.py` Edits)
- Preserve `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking` without weakening either test and without modifying `core/undo_journal.py`.
- Implement a deterministic per-document saved-state checkpoint map inside `MisoraApp` (e.g., `self._saved_state_checkpoints: dict[str, str]`):
  * **Exact Fingerprint Definition (NOT boxes-only, so structural/Box-0/extra-arg edits never false-clean):**
    - Story documents (`doc is not None`): digest (e.g., SHA-256) of `doc.to_v2_text()` (serializes all records including unknown commands, categories, extra args, Box 0 metadata, and removed records; excludes runtime `uid`).
    - Plain-text documents (`doc is None`): digest (or string) of the document's plain-text content (using the verified `open_documents[path]` key for cached docs, or `self._plain_text_content` for the active plain-text doc).
  * **When Recorded:** ONLY on fresh disk load, successful `reload_from_disk=True`, and successful primary save in `on_save()` — NEVER on keystrokes. Record keyed by `path` even if `path` is an uncached synthetic `current_file_path` (preserves `test_34`).
  * **When Evaluated (Exact Ordering in `on_undo()` / `on_redo()`):**
    1. Run the delta loop (`_apply_delta()` calls flag-only `_mark_document_dirty()`).
    2. Collect the **SET of distinct `file_path` values** touched across `op.deltas` (plus `self.current_file_path` if affected).
    3. **AFTER the delta loop and BEFORE the single `_dirty_state_changed()` call**, for each affected path that has a recorded checkpoint (and is either in `self.open_documents` OR equals `self.current_file_path`): recompute its live fingerprint and set that document's dirty flag to `False` if it matches its saved checkpoint, else `True` (updating `open_documents[p]["dirty"]` when cached and `self.is_dirty` when `p == self.current_file_path`).
    4. Call `_dirty_state_changed()` **ONCE** at the end.
  * **Explicit Boundary:** `BulkFileDelta` direct-to-disk paths (`fp.write_text` inside `_apply_delta()`) are explicitly OUT of S2 checkpoint scope (owned by S5); note this caveat in the Implementation Plan.

### D. Complete Explicit `on_save() -> bool` Contract
- Ensure EVERY exit path of `on_save()` returns an explicit Python `bool` (`True` or `False`, NEVER `None`).
- Wrap the ENTIRE `on_save()` workflow — including pre-save widget/model synchronization (`_on_box0_metadata_edited()`, `_sync_continuous_box_from_widget()`, `inject_box()`), `_get_backup_dir()`, backup creation, serialization, and primary disk persistence — inside an outer error boundary so ANY unexpected failure returns `False`.
- Do NOT invent a Save-As flow (current `on_save()` has none).
- Return `False` on:
  * No active document (`self.current_file_path is None`),
  * Any pre-save flush/validation/backup/serialization/write/repack failure or exception (preserve the in-memory document and keep both `open_documents[path]["dirty"]` [when cached] and `self.is_dirty` as `True`).
- Return `True` ONLY after the active document itself has been persisted to disk without error:
  * Immediately upon primary persistence success: if `path in self.open_documents`, set `self.open_documents[path]["dirty"] = False`; ALWAYS set `self.is_dirty = False`; update `self._saved_state_checkpoints[path]`; call `self.undo_journal.mark_saved(...)`; and call `_dirty_state_changed()` once.
  * **Deterministic Secondary XUAT Sync Failure Contract:** If primary document persistence already succeeded and optional XUAT synchronization fails afterward:
    - Primary file stays persisted; `open_documents[path]["dirty"]` (if cached) and `self.is_dirty` stay `False`; checkpoint remains updated;
    - **`self._modified_boxes` is RETAINED (NOT cleared)** so the next save can retry XUAT sync;
    - Report the secondary XUAT error clearly via `logger` and `lbl_status`;
    - Return **`True`** (primary save succeeded).
    - Clear `self._modified_boxes` only when XUAT sync succeeds (or is not applicable/skipped cleanly).
- Preserve Tkinter shortcut/event wrapper compatibility (direct `app.on_save()` returns strict `bool`, while Tk event wrappers continue returning `"break"` where required).
- Do NOT wire `close_file()` or `_on_app_exit()` to abort on `False` in S2 (those remain S3; document this boundary clearly).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create `tests/test_s2_dirty_contract.py` using existing `unittest` conventions (preserving/restoring `misora.CONFIG_PATH` in `setUp`/`tearDown` per `tests/test_s1_open_file_safety.py`, suppressing modal `messagebox` calls during automated failure tests, and keeping `var_preview_compiled` **OFF** in every save test so S3's `F-GPT-04` plain-text preview save defect is never pulled into S2).

Follow clean TDD order (no git commands needed): write tests first, run against unpatched code and record outputs, implement S2, re-run and confirm PASS.

Per-test expectation (do NOT weaken tests that already pass):
- **Defect / New-Behavior Probes (MUST FAIL before S2, PASS after S2):** Tests 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
- **Regression Guards (MUST PASS both before AND after S2):** Test 11 (plus existing `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking`).
- **Guard Authoring Constraint:** Guard Test 11 MUST assert ONLY against pre-S2 contracts/attributes and MUST NEVER dereference any new S2 attribute (such as `_saved_state_checkpoints` or `_mark_document_dirty`). If a Guard fails pre-S2 due to an unmasked bug, re-label it as a Probe rather than weakening it.

Required test cases:
1. [Probe — P0 Cross-File False-Clean Clobber]:
   - Open valid Document A, edit via real `txt_dialogue` commit -> A is dirty (`open_documents[A]["dirty"] is True`).
   - Open/switch to valid Document B, edit B, save B (`on_save()` -> `True`; global journal `mark_saved()` sets `is_clean == True`).
   - Switch back to Document A (cache hit). Assert A is dirty and window title has `*`.
   - Trigger BOTH a real no-op `<KeyRelease>` in `txt_dialogue` AND a direct `_dirty_state_changed()` call on A.
   - Assert `open_documents[A]["dirty"] is True`, `self.is_dirty is True`, and title/dock retain `*`.
2. [Probe — No-Op `<KeyRelease>` False-Dirty Prevention (Dialogue & Speaker)]:
   - Open Document A and edit A (dirty).
   - Open clean Document B (no edits on B).
   - Exercise the REAL Page View `<KeyRelease>` -> `_commit_widget_edit()` -> `_on_dialogue_edited()` path on clean B without changing text, AND exercise a real no-op speaker `<KeyRelease>` -> `_on_speaker_edited()` on clean B without changing speaker.
   - Assert `open_documents[B]["dirty"] is False`, `self.is_dirty is False`, `_modified_boxes` is unchanged, dock/title show no `*` for B, and `open_documents[A]["dirty"] is True`.
3. [Probe — `on_save()` Strict `True` Return & Scoped Clean]:
   - With dirty inactive Document A open, edit active Document B and call `res = app.on_save()` (cover story/text path and bundle path if fixture/UnityPy available; `var_preview_compiled` OFF).
   - Assert `res is True` (strict `bool`), `open_documents[B]["dirty"] is False`, `self.is_dirty is False`, and `open_documents[A]["dirty"] is True`.
4. [Probe — `on_save()` Strict `False` on Primary Non-Bundle Write Failure]:
   - Edit active non-bundle document (`dirty == True`), force the disk write target to raise `OSError`.
   - Call `res = app.on_save()`; assert `res is False`, `self.is_dirty is True`, and `open_documents[path]["dirty"] is True`.
5. [Probe — `on_save()` Strict `False` on Bundle Save Failure]:
   - With an active dirty bundle document, patch `misora.save_bundle_story` (module namespace — NOT `core.bundle_io.save_bundle_story`) to raise (suppressing `messagebox`).
   - Call `res = app.on_save()`; assert `res is False`, `self.is_dirty is True`, and `open_documents[path]["dirty"] is True`.
6. [Probe — `on_save()` Strict `False` on Pre-Save Flush Failure & No Active Document]:
   - (a) With an active dirty document, force a pre-save sync/preparation helper (e.g., `_on_box0_metadata_edited` / `_sync_continuous_box_from_widget` / `_get_backup_dir` / `inject_box`) to raise; assert `app.on_save() is False` and dirty remains `True`.
   - (b) With `current_file_path is None`, assert `app.on_save() is False` with no uncaught exception.
7. [Probe — `on_save()` Secondary XUAT Sync Failure Keeps Primary Save `True` & Retains `_modified_boxes`]:
   - With an active dirty document (with non-empty `_modified_boxes`) where primary disk persistence succeeds, force the optional XUAT synchronization step to fail/raise.
   - Assert primary file was persisted, `open_documents[path]["dirty"] is False`, `self.is_dirty is False`, `len(app._modified_boxes) > 0` (retained for retry), secondary error is reported via logger/`lbl_status`, and `app.on_save() is True`.
8. [Probe — Cache-Hit Title/Dock Parity]:
   - Edit Document A (dirty), switch to clean Document B, switch back to Document A via cache-hit `open_file(A)`.
   - Assert window title immediately includes `*` AND `_refresh_opened_files_list()` agrees with `open_documents[A]["dirty"] is True` (and inverse when switching to clean B).
9. [Probe — Representative Mutation Paths & Both MTL Apply Paths Mark Per-Doc Entry + Single UI Sync]:
   - Verify representative mutation paths mark `open_documents[path]["dirty"] is True` and update title/dock cleanly: structural (`on_box_new()`, `on_box_cut()`/`on_box_paste()`, `on_clear_dialogue_skeleton()`), current-file replace (`on_replace_next()`), script import/apply, AND **both** MTL apply paths (`on_translate_current_box()`'s inner `update_ui()` and `TranslatorAssistantDialog._on_apply()`, driven with stubbed engine/`translate_async` — ZERO live network calls). Do NOT exercise the deferred latent `_commit_widget_edit(entry_speaker)` branch.
10. [Probe — Per-Document Undo-to-Saved-State Checkpoint Isolation & Anti-UNDO-STORM]:
    - Open Document A and edit A (A is dirty).
    - Open Document B, perform a multi-delta edit on B (B is dirty), then Undo B back to B's saved state.
    - Assert Document B returns to clean (`open_documents[B]["dirty"] is False`, `self.is_dirty is False`), Document A remains dirty (`open_documents[A]["dirty"] is True`), and `_refresh_opened_files_list()` is NOT called per-delta inside the undo loop (called at most once for the undo operation).
11. [Guard — Single-Document Lifecycle & Fresh/Reload Isolation (Pre-S2 Attributes Only)]:
    - Single document: fresh load starts clean -> edit becomes dirty (`*` in title & dock) -> `on_save()` clears dirty -> second edit becomes dirty again.
    - With dirty Document A open, fresh load / `reload_from_disk=True` of B leaves B clean and `open_documents[A]["dirty"] is True`.
    - Verify `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking` pass untouched.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN S2)
==================================================
- `_save_document_entry(path, entry)` inactive-doc save helper (S3)
- `close_file()` abort on failed save or `_on_app_exit()` Save-All-dirty loop (S3)
- Plain-text save from raw model `F-GPT-04` or shared `write_atomic_utf8` `N-E` (S3)
- Structural snapshot/cut/clear-skeleton integrity fixes beyond dirty marking (S4)
- Multi-file Replace-All & `BulkFileDelta` direct-to-disk checkpointing (S5)
- Search/MTL/Batch threading redesign (S6)
- Full per-file `MasterUndoJournal` revision architecture in `core/undo_journal.py` (`F16` full), per-doc lock/selection switch state (`F17`), or `_commit_widget_edit()` speaker `inject_box(..., None)` hardening (`F20`) (S7)
- S8 / S8b-1..4 / S9–S11 features

==================================================
PART 4 — DELIVERABLES
==================================================
1. **Now (during `/plan` — ZERO file edits):**
   Produce an **Implementation Plan artifact** containing:
   - Preflight verification results (branch, `HEAD`, `git status --short`, Python 3.12 path/version, exact verified `misora.py` dirty/mutation/save/`open_file` call sites, plain-text cache key, Batch Translate Rule 15 note, and exact quoted assertions of `test_34` & `test_39`).
   - Flag-only `_mark_document_dirty(path)` + pure-UI `_dirty_state_changed()` + no-op `<KeyRelease>` guards + deterministic `to_v2_text()` / plain-text per-document checkpoint design (confirming zero edits to `core/undo_journal.py`, multi-file undo set evaluation, and `test_34` uncached path handling).
   - Exact `on_save() -> bool` outer error boundary, secondary XUAT failure `_modified_boxes` retention, and shortcut wrapper `"break"` compatibility check.
   - Planned `tests/test_s2_dirty_contract.py` cases (Probes 1–10 vs. Guard 11).
   STOP and wait for user approval (`Proceed`).

2. **After user clicks `Proceed`:**
   - Write `tests/test_s2_dirty_contract.py` -> run pre-fix (record Probes 1–10 failing, Guard 11 passing) -> implement S2 -> run:
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_s2_dirty_contract -v`
     * `py -3.12 -m unittest tests.test_s1_open_file_safety -v`
     * `py -3.12 -m unittest tests.test_phase2_required -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** with exact commands, real outputs (honestly reporting `test_05` status without weakening it), `git status --short`, concise diff summary, `PROJECT_STATE.md` update (including S8b-1..4 split and confirmed-latent S7/F20 note), and explicit handoff note that S3 is now unblocked (`close_file`/`_on_app_exit` consumption of `on_save() -> bool` remains S3).
```

Silakan kirim Blok 1 + Blok 2 secara identik ke GPT dan Qwen. Begitu keduanya membalas LOCK, pastikan S0+S1 sudah kamu commit lokal di D:\Misora-Editor, lalu langsung tempel Blok 2 ke Google Antigravity untuk memulai /plan S2!

You:
Saya akan ulangi temuan saya.

Jika semuanya sudah masuk abaikan. Dan saya akan pakai block sebelumnya

setelah saya tanya dengan gpt mengenai fitur preview(icon mata):

saya paham sekarang dan saya menemukan banyak bug disini.

B1.Men togle preview mode menghilangkan cursor, saat cursor hilang sama sekali tidak bisa mengetik tapi bisa sorot, tapi tidak bisa edit atau delete saat sorot.

B2. (Bukan bug sih) Karena preview itu satu grup dengan view makanseharusnya satu grup dalam ribbon menurutku ada di atas bareng dengan toggle view lain yaitu select dan continues view. Itu artinya perubahan desain agar 2 fungsi terlihat seragam yaitu membubuhkan icon pada select box dan continous view saya butuh saran dan masukan akan hal ini.

B3. Pada continous view semua pembubuhan atribut ngui tidak berfungsi

B4. (Bukan bug) Kata kata "GAME VIEW (xxxxx)" menjadi salah makna dan redundant arti. Mungkin ini di namai begitu sebagai counterpart terhadap windows bawah yang adalah raw script view. Tapi ini menjadi salah makna dengan adanya 2 tombol continuous dan preview saya minta saran untuk namai ulang ketika ganti ganti mode

B5. (Bukan bug) Mengenai tool tips hampir semua tombol dan fungsi belum ada tool tipsnya saya ingin ini berfungsi seperti level jika disorot sebentar maka akan muncul nama fungsi aslinya (bukan singkatan), aga lama akan muncul deskripsi, dan aga lama akan muncul contoh, beberapa yg tidak bisa menampilkan contoh akan diberi deskripsi tambahan bagai menjelaskan ke pemula.

B6. Bugs, view show line number tidak update ketika saya tekan enter atau delete enter atau paste yg mengandung line break. Ini terjadi di semua jenis view

Mengenai

Misora csif script detected in clipboard

Saya minta penjelasan dan ekspektasi desain nya.

Saya punya saran

Saat saya paste dan terdeteksi

[Insert as new box]

Tapi dimana? Kasih penjelasan misal nya setelah nomer box yg di sorot.

Pilihan kedua saya mau diganti menjadi

[Replace curent box (box number)]

Jika deteksi paste lebih dari satu box maka kata kata kedua berubah

[Replace current box dan seterusnya (box number-boxnumber)]

Paste import script preview terjadi jika box lebih dsri satu

Paste yg mengandung header box 0 akan mengalami perbedaan perlakuan karena jelas user ber ekspektasi bahwa itu bukan insert melainkan replace maka langsung ke paste inport preview.

B8. Saya mencoba paste script dan paste import preview tidak menampilkan apa apa.

Mengenai gembok.

Di continous view icon gembok mungkin tidak diletakan disana, yaitu disebelah kanan select box(jika diaktifkan) sebelum dot dan nomer box.

Ketika dipencet fungsinya adalah toggle lock. Toggle select box akan hilang (perhatikan jangan sampai tidak alignment meski 1 box kehilangan toggle button)

Karena saya minta toggle yg artinya seluruh box sibubuhi icon gembok jadi gembok teebuka tidak mencolok dan warnanya transparant icon gembok sekarang saya suka.

B9. Perubahan fungsi gembok.

Saat dibgembok cursor typing masih ada tapi tidak bisa diketik, tiap ada masukan dan penghapusan akan muncul notifikasi, untuk dibuka dulu gemboknya baru bisa edit.

Tombol cut dan fungsi cut menjadi sama dengan copy tanpa hapus informasi.

Saya mau penjelasan tentang icon 📌 disebelah speaker. Apa ekspektasi desain ini?

Saya sebagai user memiliki ezpektasi mempengaruhi tombol next/prev button jadi akan loncat ke speaker yang sama. Setiap kali jump berikan notifikasi. Pada tool tips sorot berikan deskripsi jelas.

Itu ekspektasi saya. Mungkin maksud anda berbeda saat mendesain.

B10 (bukan bug) ini terjadi setiap kali saya buka misora, sebelum tombol besar dan deskripsi bahwa ridak ada opened file. Saya selalu mengira opened file adalah Open file, dan kesal karena tidak membuka jendela untuk membuka file. Jadi buat tab nya memiliki fungsi ganda sebagai (open file) juga. Meskipun saya tahu ini kebodohan user.

Tolong berikan pendapatmu mengenai temuan dan ide saya

Gemini:
Semuanya sudah masuk 100% dan tercatat resmi. Kamu bisa langsung abaikan pengulangan ini dan pakai Blok 1 + Blok 2 (S2) dari pesan sebelumnya untuk dikirim ke GPT dan Qwen.

Berikut cek cepat bahwa tidak ada satu pun temuanmu yang terlewat:

| Temuan | Solusi Terkunci | Jadwal Slice |
| --- | --- | --- |
| B1 (Preview kursor) | Read-only, toast, pulihkan caret/scroll | S8b-1 (LOCKED) |
| B2 (Ribbon VIEW) | Grup VIEW seragam + ikon | S8b-2 |
| B3 (NGUI Continuous) | Target kartu aktif (F-GPT-13) | S8 |
| B4 (Nama mode) | 4 nama mode + RAW SCRIPT (v2) | S8b-2 |
| B5 (Tooltips) | Rich Tooltip 1 tingkat (3 ukuran) | S8b-2 |
| B6 (Line number) | Update Enter/Delete/Paste + hapus mati | S8b-2 |
| B7 (CSIF Paste) | Target eksplisit + Box 0 ke Preview | S8b-4 |
| B8 (Preview kosong) | Fix kontras Treeview gelap | S8b-4 |
| B9 (Gembok) | Per kartu sejajar, soft-lock, Cut=Copy | S8b-3 |
| Pin 📌 | Lompat speaker + isi box baru + toast | S8b-3 |
| B10 (Tab Open) | Default Open Project + tombol/tab buka | S9 |

Silakan langsung lanjut pakai Blok 1 + Blok 2 (S2) sebelumnya untuk mendapatkan LOCK dari GPT dan Qwen!

You:
QWEN (ASSISTANT A) — BINARY VERDICT ON FINAL S2 DRAFT

Verdict: NOT LOCK. One concrete blocker (B1) + one required preflight addition (B2).

Everything else in Block 2 is accepted: Q1 flag-only helper + single UI sync, Q2 fingerprint/

multi-file set/ordering, Q3 uncached-path guards, Q4 complete mutation audit incl. both MTL

paths and the Batch worker Rule-15 constraint, Q5(b) deferral of the latent speaker branch,

Q6 XUAT secondary-failure determinism, and all test-authoring notes.

B1 (BLOCKER) — THE test_34 BRIDGE ONLY FIXES EVALUATION, NOT RECORDING

The bridge says: include self.current_file_path in checkpoint recording (on_save()) and in

Undo/Redo evaluation even when uncached. But Section C records a checkpoint at exactly three

triggers: fresh disk load, successful reload_from_disk=True, and successful primary save in

on_save(). Evaluation step 3 then only acts on paths that ALREADY HAVE a recorded checkpoint.

test_34 assigns a synthetic current_file_path = tmp_txt directly. If that test establishes its

saved baseline by calling undo_journal.mark_saved() (or by manipulating journal revisions)

WITHOUT going through on_save() or open_file(), then NO checkpoint is ever recorded for

tmp_txt. Including it in the evaluation set changes nothing: step 3 skips it for lack of a

checkpoint, dirty is never cleared, and test_34 fails. The agent is then boxed in by Part 0

(never weaken test_34) with no authorized fallback, which is precisely the situation that

produces improvised logic or a quietly weakened assertion.

I cannot resolve which case test_34 is from the snapshot in context; the test source is not

in my knowledge base. That is exactly why this must be settled in the prompt, not assumed.

REQUIRED AMENDMENT (two sentences, no scope change):

1. Preflight must CLASSIFY test_34's baseline mechanism explicitly: does it reach

on_save() / open_file(), or does it establish the saved revision directly on the journal?

Quote the setup lines, not just the assertions.

2. Add an authorized branch:

• If test_34 reaches on_save() or open_file(), the current bridge is sufficient; record the

checkpoint at that same call site for the uncached active path (already specified).

• If test_34 establishes the baseline WITHOUT on_save()/open_file(), S2 must record the

active-path checkpoint at the corresponding misora.py baseline call site (the same place

the app calls undo_journal.mark_saved), still with ZERO edits to core/undo_journal.py.

• If neither is possible without weakening the test, the plan must STOP and ask the user

before editing. Never improvise, never weaken test_34/test_39.

Also state the general rule for completeness: an affected path with NO recorded checkpoint

keeps the dirty flag set by _mark_document_dirty (True). No lazy "first observation becomes

the baseline" shortcut — that would silently false-clean real documents.

B2 (REQUIRED PREFLIGHT ADDITION) — VERIFY THE FINGERPRINT SERIALIZER

Section C hardcodes doc.to_v2_text() as the fingerprint source, but Part 1 only requires

verifying the plain-text cache key. Add to preflight: confirm the exact serializer name and

signature on the live StoryDocument, and confirm it is (a) deterministic across calls,

(b) free of runtime uid, (c) inclusive of non-projected records (unknown commands, categories,

extra args, Box 0 metadata) and reflective of removed_records, and (d) side-effect free.

If the live name differs, report it in the plan and use the verified name — do not improvise

a boxes-only digest, which would false-clean structural and metadata edits.

ACCEPTED WITHOUT OBJECTION (verified against source)

• Cache-hit title defect and the restore-then-refresh ordering fix.
• _refresh_opened_files_list() dual-source removal.
• on_save() strict bool on every path incl. the bundle failure path that currently does not

return, and the outer boundary covering pre-save flush/backup/serialize/persist.

• Secondary XUAT failure: primary clean, return True, _modified_boxes retained, error reported.
• Q5(b): the latent inject_box(..., None) speaker branch stays untouched and unexercised,

logged as confirmed-latent P0 for S7/F20. Correct call for scope discipline.

• Probe/Guard split, Test 1's dual trigger (no-op KeyRelease AND direct _dirty_state_changed),

Test 5 patching misora.save_bundle_story, Test 9 stubbed MTL with no network, Test 10

anti-UNDO-STORM assertion, Test 11 forbidden from dereferencing new S2 attributes.

VERDICT

NOT LOCK. Fold B1 and B2 and I reply LOCK immediately — no further rounds from me.

S8b-1 remains PARKED and untouched. No files edited, no tests run, no prompt executed this turn.

Gemini:
Kedua tambahan dari Qwen (B1 dan B2) sangat tajam, masuk akal, dan tidak memperluas scope S2 sedikit pun—langsung saya terima dan lipat ke dalam teks final prompt S2:

• **B1 (Jalur recording untuk test_34):** Kalau test_34 ternyata menyetel saved baseline lewat metode lain (atau langsung di undo_journal.mark_saved() tanpa melewati on_save()/open_file()), checkpoint untuk tmp_txt tidak akan pernah terekam dan test_34 akan gagal. Dengan mewajibkan preflight mengutip baris setup test_34, memberi cabang sah yang jelas (termasuk perintah STOP di /plan untuk melapor ke user jika test_34 memanipulasi jurnal secara langsung tanpa melewati misora.py), serta menegaskan aturan bahwa path tanpa checkpoint tetap dirty = True, Antigravity tidak akan terjebak mengarang solusi atau melemahkan test_34.
• **B2 (Verifikasi serializer fingerprint di preflight):** Memastikan Antigravity mengecek langsung nama, signature, determinisme, dan bebas efek samping dari StoryDocument.to_v2_text() (dan tidak pernah membuat digest berbasis boxes saja yang melewatkan metadata/record struktural).

Kirim Blok 1 + Blok 2 di bawah secara identik ke Qwen (untuk LOCK langsung) dan GPT (untuk tinjauan final & LOCK).

Blok 1 — Pesan Final Lock untuk Qwen & GPT (Bahasa Inggris)

```plaintext
# MISORA EDITOR — `S2` FINAL REVISION WITH B1 & B2 FOLDED (GEMINI → QWEN & GPT)

Status:
- **S8b-1 (PARKED):** Officially LOCKED across GPT, Qwen, and Gemini. Untouched.
- **S2 (NEXT EXECUTABLE):** Gemini accepts BOTH Qwen amendments (`B1` and `B2`) verbatim without objection and folds them into Block 2 below.

Amendments Folded Into Block 2:
1. [B1 — `test_34` Baseline Recording Classification & Authorized Fallback]
   - Part 1 Preflight now explicitly quotes BOTH the setup lines (classifying whether `test_34` reaches `on_save()`/`open_file()`, another `misora.py` `mark_saved()` site, or manipulates `undo_journal` directly) AND the exact assertions of `test_34` and `test_39`.
   - Part 2 Section C now specifies the exact 3-branch rule (record at `open_file`/`on_save`, OR at the corresponding `misora.py` `mark_saved` call site with zero `core/undo_journal.py` edits, OR **STOP in `/plan`** and ask the user before editing if neither is possible — never improvise, never weaken `test_34`/`test_39`).
   - Added explicit general invariant: an affected path with NO recorded checkpoint keeps `dirty = True` set by `_mark_document_dirty()`; never use a lazy "first observation becomes baseline" shortcut.
2. [B2 — Preflight Verification of `StoryDocument` Fingerprint Serializer]
   - Added Part 1 Preflight item verifying the live serializer name & signature on `StoryDocument` (expected `to_v2_text()`), confirming (a) deterministic across calls, (b) free of runtime `uid`, (c) inclusive of non-projected records (unknown commands, categories, extra args, Box 0 metadata) and reflective of `removed_records`, and (d) side-effect free. Never improvise a boxes-only digest.

Request to Qwen and GPT:
Please reply **`LOCK`** on Block 2 below so all three AIs hold the exact same executable **S2** Antigravity prompt.
```

Blok 2 — Final Unified Prompt S2 (Google Antigravity — Siap LOCK Final)

```plaintext
/plan Implement S2: Minimum Per-Document Dirty Contract and Explicit `on_save() -> bool` Return Value in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @misora.py @tests/test_s1_open_file_safety.py @tests/test_phase2_required.py @tests/

==================================================
PART 0 — EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate (STRICT):
   - Do NOT modify any source or test files during this `/plan` phase.
   - Inspect the live local workspace (`D:\Misora-Editor`), produce a clear **Implementation Plan artifact**, and WAIT for the user to approve (`Proceed`) before editing any file.
   - After approval (`Proceed`), execute in strict failing-first TDD order and produce a **Walkthrough artifact** with real verification outputs.
2. Workspace & Commit Hygiene Check:
   - Report actual local Git branch, `HEAD` commit hash, and `git status --short`.
   - S0 + S1 should be committed locally before S2 edits begin so `git diff` stays clean and reversible. If uncommitted S0/S1 edits or any unexpected local modifications exist, STOP and report them clearly in the Implementation Plan before proposing edits.
   - NEVER run `git reset`, `git clean`, `git stash`, destructive checkout, `git commit`, or `git push`.
3. Allowed File Ownership (after approval):
   - `misora.py` (scoped strictly to per-document dirty tracking, no-op `<KeyRelease>` guards, flag-only `_mark_document_dirty()`, pure-UI `_dirty_state_changed()`, per-document saved-state checkpoint for Undo/Redo, cache-hit title/dock parity, and `on_save() -> bool`)
   - Focused new test file `tests/test_s2_dirty_contract.py`
   - `PROJECT_STATE.md` (measured S2 verification update + S8b-1..4 roadmap split ledger + confirmed-latent S7/F20 note for `_commit_widget_edit()` speaker `inject_box(..., None)`)
   - DO NOT modify `core/undo_journal.py`, `core/story_ast.py`, `core/bundle_io.py`, or any other `core/` module.
4. No new external dependencies. Follow all `AGENTS.md` architectural invariants (especially Rule 13 anti-UNDO-STORM and Rule 15 main-thread Tk safety). Do NOT use `/swarm`, `/teamwork`, or `/boost`.
5. Never remove, skip, weaken, or silently mock existing tests (including `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking`). Note: `test_phase3_performance_config.py::test_05_clean_committed_config_has_no_machine_paths` is a known pre-existing failure on this machine due to untracked local `misora_config.json`; re-measure honestly and do NOT modify or weaken it.
6. Stop strictly after S2. Do NOT implement S3 (`_save_document_entry`, `close_file()` abort, `_on_app_exit()` Save-All loop, raw plain-text save `F-GPT-04`, shared `write_atomic_utf8`), S5 (`BulkFileDelta` direct-to-disk checkpointing / multi-file Replace-All), S6 (Batch/MTL threading redesign), or S7 (full per-file `MasterUndoJournal` revision rewrite `F16` or speaker central-commit `F20`).

==================================================
PART 1 — PREFLIGHT REPORT (INCLUDE IN IMPLEMENTATION PLAN)
==================================================
Inspect live `misora.py`, `core/story_ast.py` (read-only), and `tests/` directly from disk and report:
- Current Git branch, `HEAD` commit hash, `git status --short`, and active Python 3.12 interpreter path/version (`py -3.12` preferred).
- Exact current implementations (by function name and live lines) of:
  1. `_dirty_state_changed()` and `_refresh_opened_files_list()`.
  2. `txt_dialogue` `<KeyRelease>` -> `_commit_widget_edit()` -> `_on_dialogue_edited()`, and `entry_speaker` `<KeyRelease>` -> `_on_speaker_edited()`.
  3. All mutation paths that currently rely on `_dirty_state_changed()` or set `self.is_dirty` directly, specifically auditing: `on_box_new()`, `on_box_cut()`, `on_box_paste()`, `on_paste_cross_box()` / script import apply, continuous speaker commit, continuous plain-text commit, `on_clear_dialogue_skeleton()`, `on_replace_next()`, current-file branch of `on_replace_all()`, BOTH MTL apply paths (`on_translate_current_box()`'s inner `update_ui()` AND `TranslatorAssistantDialog._on_apply()`), `BatchTranslateDialog.worker()` + `finish()`, and Undo/Redo (`on_undo()`, `on_redo()`, `_apply_delta()`).
  4. `open_file()` cache-hit sequence (specifically where window title is updated relative to restoring `entry["dirty"]`) and the exact key in `open_documents[path]` that stores plain-text content.
  5. `on_save()` end-to-end (every pre-`try` operation such as `_get_backup_dir()`, `_on_box0_metadata_edited()`, `_sync_continuous_box_from_widget()`, `inject_box()`, every primary bundle/v2/plain-text branch, optional XUAT sync block and where `_modified_boxes` is cleared, error branches, and current callers including shortcut wrappers, `close_file()`, and `_on_app_exit()`).
  6. Quote BOTH the setup lines AND the exact assertions of `tests/test_phase2_required.py::test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking`. Explicitly CLASSIFY `test_34`'s saved-baseline mechanism: does it reach `on_save()` / `open_file()`, another `misora.py` `undo_journal.mark_saved()` call site, or does it manipulate `undo_journal` directly without calling `misora.py`? Surface any incompatibility BEFORE editing.
  7. Verify the exact live serializer method name and signature on `StoryDocument` (expected `to_v2_text()`), confirming that it is: (a) deterministic across repeated calls, (b) free of runtime `uid`, (c) inclusive of non-projected records (unknown commands, categories, extra args, Box 0 metadata) and reflective of `removed_records`, and (d) side-effect free. If the live name differs, report it in the plan and use the verified name — NEVER improvise a boxes-only digest.

==================================================
PART 2 — ROOT PROBLEMS & REQUIRED S2 IMPLEMENTATION
==================================================

### A. Single Source of Truth Per-Document Dirty Contract & Flag-Only Helper
- Make `open_documents[path]["dirty"]` the **single authoritative unsaved flag per document** (and mirror `self.is_dirty` strictly from the active document's authoritative flag when present, or `False` when no document is open).
- Introduce a dedicated **FLAG-ONLY** helper `_mark_document_dirty(file_path)`:
  * Mutates flags ONLY: sets `self.open_documents[file_path]["dirty"] = True` if `file_path in self.open_documents`, and sets `self.is_dirty = True` if `file_path == self.current_file_path`.
  * Performs **ZERO Tk calls** and **ZERO dock/title rebuilds** (strictly prevents Rule 13 UNDO-STORM during batch/undo loops and Rule 15 worker-thread Tk violations).
- Call `_mark_document_dirty(target_path)` explicitly after EVERY actual mutation across all audited mutation sites, and invoke `_dirty_state_changed()` **exactly ONCE** per user operation (for batch/undo/redo paths, invoke `_dirty_state_changed()` ONCE AFTER the entire batch/delta loop completes):
  * Dialogue & Box 0 edits, speaker edits, `on_box_new()`, `on_box_cut()`, `on_box_paste()`, `on_paste_cross_box()` / script import apply, continuous speaker & plain-text commits, `on_clear_dialogue_skeleton()`, `on_replace_next()`, current-file branch of `on_replace_all()` (multi-file Replace-All remains S5), BOTH MTL apply paths (`on_translate_current_box()`'s inner `update_ui()` AND `TranslatorAssistantDialog._on_apply()`), and Undo/Redo delta application.
  * **`BatchTranslateDialog` Rule 15 Constraint:** `worker()` may ONLY update plain Python dict/flag state via flag-only `_mark_document_dirty(target_path)` (ZERO Tk calls from the worker); ALL title/dock/undo-control synchronization MUST occur on the main thread inside the existing `finish()` `after_idle` callback. Do NOT redesign S6 threading in S2; note any remaining concurrency caveat in the plan.
- Set a document's dirty flag to `False` ONLY when:
  1. That specific document is freshly loaded from disk (`open_file()` fresh load or successful `reload_from_disk=True`), OR
  2. That specific document's own primary persistence in `on_save()` genuinely succeeds, OR
  3. An Undo/Redo operation restores THAT specific document's actual in-memory state back to its own saved-state checkpoint (see Section C below).
- **NEVER** derive or overwrite `open_documents[path]["dirty"]` or `self.is_dirty` from global `self.undo_journal.is_clean(...)`.
- Refactor `_dirty_state_changed()` to perform **pure UI synchronization only** (window title `*`, Opened Files dock list, undo/redo button state):
  * When `self.current_file_path in self.open_documents`, mirror `self.is_dirty = bool(self.open_documents[self.current_file_path]["dirty"])`.
  * When `self.current_file_path` is NOT `None` and has NO entry in `self.open_documents` (e.g., `test_34`'s synthetic `tmp_txt` path), **PRESERVE** the current `self.is_dirty` value (do NOT reset it to `False`) and refresh title/dock/controls from it.
- Update `_refresh_opened_files_list()` to read the single authoritative `info["dirty"]` entry flag (remove the dual `info.get("dirty") or (is_active and self.is_dirty)` expression), and fix `open_file()` cache-hit switching so the window title is refreshed **AFTER** restoring `entry["dirty"]`, guaranteeing title `*` and dock `*` never disagree.

### B. Guard Non-Mutating `<KeyRelease>` Handlers (Prevent False-Dirty)
- Update `_on_dialogue_edited()` so it compares actual old vs. new text BEFORE mutating state; if nothing changed, return cleanly without setting `self.is_dirty`, `open_documents[path]["dirty"]`, or `_modified_boxes`, and without calling `_dirty_state_changed()`.
- Update `_on_speaker_edited()` so it compares actual old vs. new speaker (and any associated committed state) BEFORE marking dirty; a no-op `<KeyRelease>` (e.g., arrow key, Shift, Ctrl) MUST leave a clean document completely clean and leave `_modified_boxes` untouched.
- **Confirmed-Latent Boundary (`Q5(b)`):** Do NOT modify `_commit_widget_edit()`'s currently unreachable speaker branch (`inject_box(..., None)`) in S2; record it explicitly in `PROJECT_STATE.md` as a confirmed-latent P0 defect owned by **S7/F20** (when speaker edits are routed through central commit), and do NOT exercise that latent branch in S2 tests.

### C. Deterministic Per-Document Saved-State Checkpoint for Undo/Redo (No `core/undo_journal.py` Edits)
- Preserve `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking` without weakening either test and without modifying `core/undo_journal.py`.
- Implement a deterministic per-document saved-state checkpoint map inside `MisoraApp` (e.g., `self._saved_state_checkpoints: dict[str, str]`):
  * **Exact Fingerprint Definition (NOT boxes-only, so structural/Box-0/extra-arg edits never false-clean):**
    - Story documents (`doc is not None`): digest (e.g., SHA-256) of the preflight-verified full `StoryDocument` serializer (expected `doc.to_v2_text()`, verified deterministic, `uid`-free, side-effect free, and inclusive of non-projected records and `removed_records`). NEVER improvise a boxes-only digest.
    - Plain-text documents (`doc is None`): digest (or string) of the document's plain-text content (using the verified `open_documents[path]` key for cached docs, or `self._plain_text_content` for the active plain-text doc).
  * **When Recorded & Authorized `test_34` Baseline Branching:**
    - Standard triggers (NEVER per keystroke): fresh disk load (`open_file()`), successful `reload_from_disk=True`, and successful primary save in `on_save()`, recording keyed by `path` even if `path` is an uncached active path.
    - Authorized branches based on Preflight classification of `test_34`:
      1. If `test_34` establishes its saved baseline via `on_save()` or `open_file()`, recording at those call sites for the uncached active path is sufficient.
      2. If `test_34` establishes its baseline WITHOUT `on_save()`/`open_file()` via another `misora.py` baseline call site (where `misora.py` calls `undo_journal.mark_saved()`), record the active-path checkpoint at that corresponding `misora.py` call site (still ZERO edits to `core/undo_journal.py`).
      3. If `test_34` manipulates `undo_journal` directly without calling `misora.py`, or if neither branch preserves `test_34` without weakening its assertions, **STOP in `/plan`**, report the exact setup discrepancy, and wait for user direction before editing. Never improvise, never weaken `test_34`/`test_39`.
  * **When Evaluated (Exact Ordering in `on_undo()` / `on_redo()`):**
    1. Run the delta loop (`_apply_delta()` calls flag-only `_mark_document_dirty()`).
    2. Collect the **SET of distinct `file_path` values** touched across `op.deltas` (plus `self.current_file_path` if affected).
    3. **AFTER the delta loop and BEFORE the single `_dirty_state_changed()` call**, for each affected path that is either in `self.open_documents` OR equals `self.current_file_path`:
       - If the path has a recorded checkpoint: recompute its live fingerprint and set that document's dirty flag to `False` if it matches its saved checkpoint, else `True` (updating `open_documents[p]["dirty"]` when cached and `self.is_dirty` when `p == self.current_file_path`).
       - **General Rule (No Lazy Baseline):** An affected path with **NO recorded checkpoint** MUST keep the dirty flag set by `_mark_document_dirty()` (`True`). NEVER use a lazy "first observation becomes the baseline" shortcut — that would silently false-clean real documents.
    4. Call `_dirty_state_changed()` **ONCE** at the end.
  * **Explicit Boundary:** `BulkFileDelta` direct-to-disk paths (`fp.write_text` inside `_apply_delta()`) are explicitly OUT of S2 checkpoint scope (owned by S5); note this caveat in the Implementation Plan.

### D. Complete Explicit `on_save() -> bool` Contract
- Ensure EVERY exit path of `on_save()` returns an explicit Python `bool` (`True` or `False`, NEVER `None`).
- Wrap the ENTIRE `on_save()` workflow — including pre-save widget/model synchronization (`_on_box0_metadata_edited()`, `_sync_continuous_box_from_widget()`, `inject_box()`), `_get_backup_dir()`, backup creation, serialization, and primary disk persistence — inside an outer error boundary so ANY unexpected failure returns `False`.
- Do NOT invent a Save-As flow (current `on_save()` has none).
- Return `False` on:
  * No active document (`self.current_file_path is None`),
  * Any pre-save flush/validation/backup/serialization/write/repack failure or exception (preserve the in-memory document and keep both `open_documents[path]["dirty"]` [when cached] and `self.is_dirty` as `True`).
- Return `True` ONLY after the active document itself has been persisted to disk without error:
  * Immediately upon primary persistence success: if `path in self.open_documents`, set `self.open_documents[path]["dirty"] = False`; ALWAYS set `self.is_dirty = False`; update `self._saved_state_checkpoints[path]`; call `self.undo_journal.mark_saved(...)`; and call `_dirty_state_changed()` once.
  * **Deterministic Secondary XUAT Sync Failure Contract:** If primary document persistence already succeeded and optional XUAT synchronization fails afterward:
    - Primary file stays persisted; `open_documents[path]["dirty"]` (if cached) and `self.is_dirty` stay `False`; checkpoint remains updated;
    - **`self._modified_boxes` is RETAINED (NOT cleared)** so the next save can retry XUAT sync;
    - Report the secondary XUAT error clearly via `logger` and `lbl_status`;
    - Return **`True`** (primary save succeeded).
    - Clear `self._modified_boxes` only when XUAT sync succeeds (or is not applicable/skipped cleanly).
- Preserve Tkinter shortcut/event wrapper compatibility (direct `app.on_save()` returns strict `bool`, while Tk event wrappers continue returning `"break"` where required).
- Do NOT wire `close_file()` or `_on_app_exit()` to abort on `False` in S2 (those remain S3; document this boundary clearly).

==================================================
PART 3 — FAILING-FIRST REGRESSION TESTS (AFTER APPROVAL)
==================================================
Create `tests/test_s2_dirty_contract.py` using existing `unittest` conventions (preserving/restoring `misora.CONFIG_PATH` in `setUp`/`tearDown` per `tests/test_s1_open_file_safety.py`, suppressing modal `messagebox` calls during automated failure tests, and keeping `var_preview_compiled` **OFF** in every save test so S3's `F-GPT-04` plain-text preview save defect is never pulled into S2).

Follow clean TDD order (no git commands needed): write tests first, run against unpatched code and record outputs, implement S2, re-run and confirm PASS.

Per-test expectation (do NOT weaken tests that already pass):
- **Defect / New-Behavior Probes (MUST FAIL before S2, PASS after S2):** Tests 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
- **Regression Guards (MUST PASS both before AND after S2):** Test 11 (plus existing `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking`).
- **Guard Authoring Constraint:** Guard Test 11 MUST assert ONLY against pre-S2 contracts/attributes and MUST NEVER dereference any new S2 attribute (such as `_saved_state_checkpoints` or `_mark_document_dirty`). If a Guard fails pre-S2 due to an unmasked bug, re-label it as a Probe rather than weakening it.

Required test cases:
1. [Probe — P0 Cross-File False-Clean Clobber]:
   - Open valid Document A, edit via real `txt_dialogue` commit -> A is dirty (`open_documents[A]["dirty"] is True`).
   - Open/switch to valid Document B, edit B, save B (`on_save()` -> `True`; global journal `mark_saved()` sets `is_clean == True`).
   - Switch back to Document A (cache hit). Assert A is dirty and window title has `*`.
   - Trigger BOTH a real no-op `<KeyRelease>` in `txt_dialogue` AND a direct `_dirty_state_changed()` call on A.
   - Assert `open_documents[A]["dirty"] is True`, `self.is_dirty is True`, and title/dock retain `*`.
2. [Probe — No-Op `<KeyRelease>` False-Dirty Prevention (Dialogue & Speaker)]:
   - Open Document A and edit A (dirty).
   - Open clean Document B (no edits on B).
   - Exercise the REAL Page View `<KeyRelease>` -> `_commit_widget_edit()` -> `_on_dialogue_edited()` path on clean B without changing text, AND exercise a real no-op speaker `<KeyRelease>` -> `_on_speaker_edited()` on clean B without changing speaker.
   - Assert `open_documents[B]["dirty"] is False`, `self.is_dirty is False`, `_modified_boxes` is unchanged, dock/title show no `*` for B, and `open_documents[A]["dirty"] is True`.
3. [Probe — `on_save()` Strict `True` Return & Scoped Clean]:
   - With dirty inactive Document A open, edit active Document B and call `res = app.on_save()` (cover story/text path and bundle path if fixture/UnityPy available; `var_preview_compiled` OFF).
   - Assert `res is True` (strict `bool`), `open_documents[B]["dirty"] is False`, `self.is_dirty is False`, and `open_documents[A]["dirty"] is True`.
4. [Probe — `on_save()` Strict `False` on Primary Non-Bundle Write Failure]:
   - Edit active non-bundle document (`dirty == True`), force the disk write target to raise `OSError`.
   - Call `res = app.on_save()`; assert `res is False`, `self.is_dirty is True`, and `open_documents[path]["dirty"] is True`.
5. [Probe — `on_save()` Strict `False` on Bundle Save Failure]:
   - With an active dirty bundle document, patch `misora.save_bundle_story` (module namespace — NOT `core.bundle_io.save_bundle_story`) to raise (suppressing `messagebox`).
   - Call `res = app.on_save()`; assert `res is False`, `self.is_dirty is True`, and `open_documents[path]["dirty"] is True`.
6. [Probe — `on_save()` Strict `False` on Pre-Save Flush Failure & No Active Document]:
   - (a) With an active dirty document, force a pre-save sync/preparation helper (e.g., `_on_box0_metadata_edited` / `_sync_continuous_box_from_widget` / `_get_backup_dir` / `inject_box`) to raise; assert `app.on_save() is False` and dirty remains `True`.
   - (b) With `current_file_path is None`, assert `app.on_save() is False` with no uncaught exception.
7. [Probe — `on_save()` Secondary XUAT Sync Failure Keeps Primary Save `True` & Retains `_modified_boxes`]:
   - With an active dirty document (with non-empty `_modified_boxes`) where primary disk persistence succeeds, force the optional XUAT synchronization step to fail/raise.
   - Assert primary file was persisted, `open_documents[path]["dirty"] is False`, `self.is_dirty is False`, `len(app._modified_boxes) > 0` (retained for retry), secondary error is reported via logger/`lbl_status`, and `app.on_save() is True`.
8. [Probe — Cache-Hit Title/Dock Parity]:
   - Edit Document A (dirty), switch to clean Document B, switch back to Document A via cache-hit `open_file(A)`.
   - Assert window title immediately includes `*` AND `_refresh_opened_files_list()` agrees with `open_documents[A]["dirty"] is True` (and inverse when switching to clean B).
9. [Probe — Representative Mutation Paths & Both MTL Apply Paths Mark Per-Doc Entry + Single UI Sync]:
   - Verify representative mutation paths mark `open_documents[path]["dirty"] is True` and update title/dock cleanly: structural (`on_box_new()`, `on_box_cut()`/`on_box_paste()`, `on_clear_dialogue_skeleton()`), current-file replace (`on_replace_next()`), script import/apply, AND **both** MTL apply paths (`on_translate_current_box()`'s inner `update_ui()` and `TranslatorAssistantDialog._on_apply()`, driven with stubbed engine/`translate_async` — ZERO live network calls). Do NOT exercise the deferred latent `_commit_widget_edit(entry_speaker)` branch.
10. [Probe — Per-Document Undo-to-Saved-State Checkpoint Isolation & Anti-UNDO-STORM]:
    - Open Document A and edit A (A is dirty).
    - Open Document B, perform a multi-delta edit on B (B is dirty), then Undo B back to B's saved state.
    - Assert Document B returns to clean (`open_documents[B]["dirty"] is False`, `self.is_dirty is False`), Document A remains dirty (`open_documents[A]["dirty"] is True`), and `_refresh_opened_files_list()` is NOT called per-delta inside the undo loop (called at most once for the undo operation).
11. [Guard — Single-Document Lifecycle & Fresh/Reload Isolation (Pre-S2 Attributes Only)]:
    - Single document: fresh load starts clean -> edit becomes dirty (`*` in title & dock) -> `on_save()` clears dirty -> second edit becomes dirty again.
    - With dirty Document A open, fresh load / `reload_from_disk=True` of B leaves B clean and `open_documents[A]["dirty"] is True`.
    - Verify `test_34_undo_to_saved_revision_clears_dirty` and `test_39_revision_dirty_tracking` pass untouched.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT IN S2)
==================================================
- `_save_document_entry(path, entry)` inactive-doc save helper (S3)
- `close_file()` abort on failed save or `_on_app_exit()` Save-All-dirty loop (S3)
- Plain-text save from raw model `F-GPT-04` or shared `write_atomic_utf8` `N-E` (S3)
- Structural snapshot/cut/clear-skeleton integrity fixes beyond dirty marking (S4)
- Multi-file Replace-All & `BulkFileDelta` direct-to-disk checkpointing (S5)
- Search/MTL/Batch threading redesign (S6)
- Full per-file `MasterUndoJournal` revision architecture in `core/undo_journal.py` (`F16` full), per-doc lock/selection switch state (`F17`), or `_commit_widget_edit()` speaker `inject_box(..., None)` hardening (`F20`) (S7)
- S8 / S8b-1..4 / S9–S11 features

==================================================
PART 4 — DELIVERABLES
==================================================
1. **Now (during `/plan` — ZERO file edits):**
   Produce an **Implementation Plan artifact** containing:
   - Preflight verification results (branch, `HEAD`, `git status --short`, Python 3.12 path/version, exact verified `misora.py` dirty/mutation/save/`open_file` call sites, plain-text cache key, Batch Translate Rule 15 note, verified `StoryDocument` serializer properties, and exact quoted setup + assertions & baseline classification of `test_34` & `test_39`).
   - Flag-only `_mark_document_dirty(path)` + pure-UI `_dirty_state_changed()` + no-op `<KeyRelease>` guards + deterministic full-serializer / plain-text per-document checkpoint design (confirming zero edits to `core/undo_journal.py`, multi-file undo set evaluation, no-lazy-baseline rule, and `test_34` authorized branch).
   - Exact `on_save() -> bool` outer error boundary, secondary XUAT failure `_modified_boxes` retention, and shortcut wrapper `"break"` compatibility check.
   - Planned `tests/test_s2_dirty_contract.py` cases (Probes 1–10 vs. Guard 11).
   STOP and wait for user approval (`Proceed`).

2. **After user clicks `Proceed`:**
   - Write `tests/test_s2_dirty_contract.py` -> run pre-fix (record Probes 1–10 failing, Guard 11 passing) -> implement S2 -> run:
     * `py -3.12 -m compileall -q misora.py core assets tests`
     * `py -3.12 -m unittest tests.test_s2_dirty_contract -v`
     * `py -3.12 -m unittest tests.test_s1_open_file_safety -v`
     * `py -3.12 -m unittest tests.test_phase2_required -v`
     * `py -3.12 -m unittest discover -s tests -v`
   - Deliver a **Walkthrough artifact** with exact commands, real outputs (honestly reporting `test_05` status without weakening it), `git status --short`, concise diff summary, `PROJECT_STATE.md` update (including S8b-1..4 split and confirmed-latent S7/F20 note), and explicit handoff note that S3 is now unblocked (`close_file`/`_on_app_exit` consumption of `on_save() -> bool` remains S3).
```

Begitu Qwen dan GPT membalas LOCK pada Blok 2 di atas, pastikan perubahan S0 + S1 di lokal D:\Misora-Editor sudah kamu commit, lalu langsung jalankan Blok 2 di Google Antigravity!

You:
QWEN (ASSISTANT A) — FINAL VERDICT ON S2 (B1 + B2 FOLDED)

VERDICT: LOCK.

B1 — VERIFIED CORRECTLY FOLDED (both halves, not just evaluation)

• Part 1 item 6 now requires quoting BOTH setup lines AND assertions of test_34/test_39, and

explicitly CLASSIFIES the saved-baseline mechanism into the three cases I named:

on_save()/open_file(), another misora.py undo_journal.mark_saved() site, or direct journal

manipulation without touching misora.py. This is exactly the missing half of the earlier

bridge. Correct.

• Part 2 Section C now carries the authorized 3-branch rule, including branch 2 (record at the

corresponding misora.py mark_saved call site with ZERO core/undo_journal.py edits) and

branch 3 (STOP in /plan, report the exact setup discrepancy, await user direction — never

improvise, never weaken test_34/test_39). Correct and sufficient.

• The general invariant is present and correctly worded: an affected path with NO recorded

checkpoint KEEPS dirty=True from _mark_document_dirty(); no lazy "first observation becomes

baseline" shortcut. This closes the false-clean hole. Correct.

• Evaluation step 3 was restructured so the checkpoint-present and checkpoint-absent cases are

both explicit inside the same loop, still AFTER the delta loop and BEFORE the single

_dirty_state_changed() call. Ordering preserved. Correct.

B2 — VERIFIED CORRECTLY FOLDED

• Part 1 item 7 verifies the live StoryDocument serializer name/signature and all four

properties: deterministic, uid-free, inclusive of non-projected records (unknown commands,

categories, extra args, Box 0 metadata) and reflective of removed_records, side-effect free.

Report-and-use-verified-name if it differs; never a boxes-only digest. Correct.

• Section C no longer hardcodes to_v2_text() as an assumption; it defers to the

preflight-verified serializer. Correct.

• Good addition I did not ask for but endorse: Part 1 now inspects core/story_ast.py

READ-ONLY, which is what B2 verification requires while Part 0 still forbids modifying any

core/ module. No conflict — ownership governs modification, not inspection.

PREVIOUSLY ACCEPTED, UNCHANGED IN THE VISIBLE PORTION

Q1 flag-only _mark_document_dirty + exactly one _dirty_state_changed per operation (Rule 13);

Q2 fingerprint/multi-file affected-set/ordering; Q3 uncached-path guards in on_save() and

_dirty_state_changed(); Q4 complete mutation audit incl. on_replace_next, current-file

on_replace_all, BOTH MTL apply paths, and the BatchTranslateDialog worker flag-only / finish()

after_idle Rule-15 constraint; Q5(b) deferral of the latent inject_box(..., None) speaker

branch to S7/F20 with no S2 test exercising it; Q6 XUAT secondary-failure determinism.

Format conforms to the agreed Antigravity conventions: /plan zero-edit gate, @file mentions,

no /swarm//teamwork//boost, Proceed gate, Walkthrough with real outputs.

NON-TECHNICAL CONDITION — RELAY TRUNCATION

The pasted prompt ends mid-sentence in Part 2 Section D at

"
- **
`
