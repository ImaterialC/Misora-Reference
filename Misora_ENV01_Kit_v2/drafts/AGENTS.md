# Misora — Agent Rules (Layer 0)

## 1. Authority and evidence
- Read `PROJECT_STATE.md` and `docs/ai/CONTEXT_ROUTER.md`; working-tree source, not chat/index/archive, is proof.
- Evidence: `REPORTED`, `SOURCE-OBSERVED`, `CONFIRMED`, `NEEDS-REPRO`, `PROPOSAL`, `DEFERRED`. Lifecycle is separate: `ACTIVE`, `SUPERSEDED`, `DEFERRED`, `RETRACTED`, `HISTORICAL-REFERENCE`. Repetition is not confirmation.
- `/plan` is read-only. Edit only after independent review and explicit Project Lead `Proceed`. Stop on material uncertainty.

## 2. Scope and change safety
- Follow the reviewed allowlist; protect pre-existing, untracked, ignored, config, backup, fixture, and user data. Never `reset --hard`, `clean`, blanket-checkout, or discard unrelated changes.
- ENV-01 READ-ONLY paths: `__init__.py`, `misora.py`, `core/**`, `assets/**`, `tests/**`, `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, `README.md`.
- ENV-01 authorizes no source, test, dependency, version, release, commit, tag, or push changes. `__init__.py` is the version source.
- Before replacing root docs, archive raw bytes and verify SHA-256 + byte equality. Never decorate/normalize archives. Report paths, checks, limits, rollback; never claim unrun tests passed.

## 3. Tkinter and document model
- One `tk.Tk()` root (`MisoraApp`); dialogs/splash use `Toplevel(parent=...)`. Tk variables use `master=`; guard widgets with `winfo_exists()`.
- `StoryDocument.records` is authoritative; `Box` is a projection; `Seg.record` points to its `Record`. Runtime UIDs are not serialized. Rebuild projections after edits/undo/redo.
- New/Cut/Paste/Move/Clone use document APIs and preserve unknown commands/identity. `Box.clean_text`, `.text`, `.raw` are read-only; `BoxSnapshot` preserves `seg_texts`. Do not break `Box.__deepcopy__` before handler migration.
- Helpers precede callers; surface callback errors.

## 4. Serialization and persistence
- Preserve command IDs/categories, unknown args, whitespace-only args, Unicode separators, and binary arity. Narration uses `tag`; normalize `{playername}` to `{0}` where required.
- Keep DEF-01's empty-arg sentinel as exactly one ASCII space (`" "`). Do not strip/replace without a new decision and live-client evidence.
- Save bundles via same-directory temp; reopen/verify target TextAsset, object count, non-target bytes, and source fingerprint before `os.replace`. Guard re-entry.
- XUAT is one `key=value` per line. Decode strictly; preserve BOM, line endings, key whitespace, and unchanged lines; escape newlines. Keep immutable Japanese keys by box identity; preview conflicts.

## 5. Editing, undo, clipboard, CSIF
- All widget mutations use the central commit path; virtual `<<Cut>>`/`<<Paste>>` explicitly commit. Flush before undo/redo/save/close/navigation/rebuild; pair batches in `finally`; mutate model first, refresh once; dirty state is revision-based.
- Copy Box emits CSIF (`@@Speaker`, `@@_`, `@@!meta`). Paste Box INSERTS after the active box; Paste Script REPLACES forward. Plain Ctrl+V with CSIF headers must ask: text / across boxes / insert boxes / cancel. Headers never enter dialogue text or binary args.
- Sparse `@@#N|Speaker` is 1-based for filtered/non-contiguous output; reject mixed, duplicate, missing, or out-of-range addresses. Strip only outer Markdown fences. Use the clipboard retry helper; stale internal data must not shadow newer system content.

## 6. Workers and document lifecycle
- Workers never call Tk or mutate documents/undo. Capture UI-thread snapshots; marshal results/errors to UI; reset state in `finally`.
- Persist per-document view/selection/lock/JP state. Closing prunes undo; undo never reopens closed files. Dirty close/exit prompts Save/Discard/Cancel; failed save aborts. Reload/Revert reads disk.

## 7. Security, UI, and runtime
- Keep TLS verification enabled; no SSL bypass. Keep API keys out of config/logs; redact secrets. Preserve parse-failed config before defaults.
- `core/ngui_tags.py` is the NGUI tag source; gradients emit `[RRGGBB-RRGGBB]`. Length metrics measure rendered text, not markup.
- Shortcuts are whitelist-only; respect Text/Entry Ctrl+C/V/X/A, Shift, Caps Lock, AltGr, IME, and modal grabs. Advertised accelerators must work. Icon-only controls need tooltips, text fallback, and theme contrast.
- One process; no second splash process. Lazy-load dependencies; do not mutate DPI awareness at runtime. Logger writes use a background queue.
- Native overflow: 50 digit-widths or 3+ hard linebreaks (4+ lines); editor font is an estimate. Preserve Box 0 invariants.

## 8. Current release authority and delivery
- Product `1.4.15`; `v1.5.0` campaign `CANCELLED` / `NOT RELEASED`; promotion `NOT AUTHORIZED`. Old S12 audit `PAUSED / SUPERSEDED`.
- Future S15 proposal is `CANCELLED`; completed historical S15 stays historical. Future work needs a new Project Lead-approved charter.
- v1.4.0 Ribbon Cut/Paste Box reports need current manual revalidation; they are not confirmed current defects.
- Report changed paths, checks, limits, and rollback; never expand scope to force a gate pass.
