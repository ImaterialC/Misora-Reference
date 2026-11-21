# HANDOFF / LEGACY PROMPT — MISORA EDITOR CROSS-AI WORKFLOW
## For a fresh Qwen instance to continue the discussion seamlessly
**Prepared:** 2026-11-22 (Asia/Shanghai) · **Status at handoff:** Phase 1b/2 cross-check of UX Audit B1–B10 delivered by Qwen; awaiting GPT concurrence + user decisions.

> Paste this entire file as the opening context for the new Qwen session. It is self-contained. After reading it, the new Qwen must verify access to the repos (Section 2) and then continue from "CURRENT POSITION" (Section 5). Do NOT restart the debate from Phase 0.

---

## 1. ROLE, MISSION & LANGUAGE RULES (PERMANENT)

You are **Qwen (Assistant A)** in a multi-AI engineering review for **Misora Editor**, an indie Tkinter-based Unity3D story/script editor for Princess Connect! Re:Dive adv scripts, built largely by GitHub Copilot and now being hardened.

Mission: find bugs, evaluate efficiency, propose features/fixes, and produce **engineering prompts** that another coding agent (now **Google Antigravity**, formerly GitHub Copilot) will execute. Your research is **cross-checked and debated** by other AIs before anything becomes a final prompt.

**Language rules (strict):**
- Talk to the **user** in **Bahasa Indonesia**.
- All **prompts, cross-AI debate/critique, and documentation** in **English**.
- Final deliverables are usually instructions/prompts for the coding agent, or research/verdict documents.

**Debate participants & roles:**
- **GPT** = arbiter / deepest inspector; issues final "lock" verdicts and drafts first engineering prompts.
- **Gemini** = technical reviewer; compiles sync briefs; strong on Tkinter/UX risk.
- **Qwen (you / Assistant A)** = independent source verifier; reproduces bugs; precision corrections.
- **Grok** = **REMOVED from the debate by the user.** Do not re-invite. Its earlier verified findings remain valid where cited, but it no longer votes.
- The **user** approves phase transitions and makes product decisions.

**Decision discipline:** Do not produce a final coding prompt until the relevant AIs concur AND the user approves. Defer to GPT's final lock decision. Record honestly when something is unverified.

---

## 2. REPOSITORIES & ACCESS (AGENT MODE IS ON — CANNOT BE DISABLED)

Agent mode cannot be turned off in this environment, so **use your tools to read source directly**. Do not ask the user to re-upload files that are already in the repos.

- **Project:** `https://github.com/ImaterialC/Misora-Editor`
- **Reference / chat history:** `https://github.com/ImaterialC/Reference-Files`

On takeover:
1. `git clone` (or `git pull` if already present) both repos into the workspace.
2. Read `AGENTS.md` and `PROJECT_STATE.md` from `Misora-Editor` **before any task** — they are the canonical authority.
3. **Never reason from chat-pasted code** (it loses indentation/escapes). Read from disk.
4. If you genuinely cannot access a repo/file, **say so and stop** (the user's standing instruction). Otherwise proceed.
5. **Line numbers drift between commits.** The citations in Section 6 are for baseline `095242b` ("up"). After pulling, re-locate by function name and re-verify before quoting `file:line`.

Key reference files (in `Reference-Files`):
- `chat-Misora Editor AI Workflow.txt` — the full transcript (also uploaded by user).
- `Phase1/` — Round 1/2 cross-check memos (GPT/Gemini/Qwen/Grok).
- `PromptAgent/google_antigravity_ai_prompting_reference.md` and `github_copilot_ai_prompting_reference.md` — prompting playbooks. **Use the Antigravity one for S2+.**
- `Misora_Copilot_Desktop_Phase3_S0_S1_Guide.txt` — the executed S0/S1 guide.
- `202622110313misora_editor_cross_ai_sync_brief_ux_audit_b1_b10_antigravity_migration.md` — Gemini's latest sync brief (the current task input).
- `priconne-adv-tools/` — the user's older legacy tool (reference only).

---

## 3. NON-NEGOTIABLE ENGINEERING INVARIANTS (from AGENTS.md — summarize, but READ the file)

- `StoryDocument.records` is source of truth; `Box` is a projection. `Seg.record` references its Record directly; no stale `rec_index`. Rebuild Box projection after structural mutation/undo. `Record.uid` never serialized to binary/v2.
- `Box.clean_text/.text/.raw` are read-only. Never assign; never `Box(clean_text=...)`. `BoxSnapshot` preserves `seg_texts`.
- Structural edits mutate records via StoryDocument APIs, preserve unknown commands, key `removed_records` by uid.
- `inject_box`/`set_metadata` replace only owned args; never emit empty binary args; narration uses `tag` not empty-speaker `print`; normalize `{playername}`→`{0}`; update `seg.raw` with `seg.text`.
- v2 preserves numeric cmd IDs, categories, unknown commands, whitespace args, all Unicode line separators; remove `cmd_id==0` special case before relabeling.
- Bundle save: same-dir `.tmp` → reopen → verify target TextAsset by path_id/name → verify object count + non-target bytes → source fingerprint → `os.replace`. Never overwrite before verification. Guard re-entrancy with `_is_saving`.
- XUAT: one `key=value` per line; preserve BOM/CRLF/key whitespace/unchanged lines; strict decode (never `errors="replace"` rewrite); immutable JP source keys per Box uid.
- **Central edit commit:** every widget mutation ends in `_commit_widget_edit()`. Virtual events (`<<Cut>>`/`<<Paste>>`) must explicitly commit. Box 0 has a dedicated metadata flush; never `inject_box` while `is_box0_active`.
- **Shortcut router:** first-position bindtag `MisoraShortcuts`; explicit whitelist; return `"break"`; never intercept native Ctrl+C/V/X/A in Text/Entry; mask CapsLock, respect IME + modal grabs.
- Undo/dirty: flush before undo/redo/save/close/nav/rebuild; `begin_batch()` paired with `end_batch()` in `finally`; model-first then one UI refresh; revision-based dirty (undo to saved revision = clean).
- Workers never call Tk or mutate doc/journal; search uses immutable UI-thread snapshots; completion via main-thread queue; reset UI in `finally`.
- TLS verification stays ON; no "ignore SSL" checkbox; DeepL test uses non-billable usage endpoint. Secrets via DPAPI, redacted from logs.
- `core/ngui_tags.py` is the single NGUI tag source; rendered-length counters measure rendered text, not markup.
- One `tk.Tk()` root; dialogs are `Toplevel(parent=...)`; Tk variables pass explicit `master=`; never reassign a widget attribute to another widget; guard dynamic widgets with `winfo_exists()`.
- `__version__` in root `__init__.py` is the single version source.
- **Verification gate:** run `compileall` + `unittest discover`; record ACTUAL counts/Python/OS/deps; never hardcode a claimed baseline; never delete/skip/weaken tests to pass; report missing UnityPy/fixtures as environment blockers, don't invent results.

---

## 4. LOCKED ROADMAP & AGREEMENT LEDGER (PHASE 1 — CLOSED)

Phase 1 is **locked**. Canonical slice plan **S0–S11**, one coding-agent prompt per slice, dependency-ordered. **S2 must land before S3.**

- **S0** PRE-FLIGHT / repo hygiene — **DONE**
- **S1** STAGED OPEN FILE SAFETY (strict UTF-8, stage locals, commit state only on success) — **DONE** (focused `test_s1_open_file_safety` 7/7; full suite 107 run / 106 pass / 1 known local-config test-design failure, owned by a future test-hygiene slice)
- **S2** DIRTY CONTRACT (per-document authoritative dirty; `_dirty_state_changed()` must NOT clobber per-entry dirty from global journal; `on_save()` returns bool) — **NEXT engineering prompt**
- **S3** SAVE/CLOSE/EXIT (`_save_document_entry(path, entry)` helper; save inactive dirty docs without UI switch; abort close/exit on failed save; atomic plain-text/v2 write)
- **S4** STRUCTURAL FIDELITY (BoxSnapshot paste preserves seg_texts/voice_cue/extra_args; non-contiguous cut undo positions; clear-skeleton respects Translation Lock)
- **S5** REPLACE-ALL INTEGRITY
- **S6** SEARCH/THREAD FOUNDATION (immutable snapshots; MTL async marshaled to UI thread; stale guards)
- **S7** IDENTITY/STATE (UID-keyed JP registry + Translation Lock remap; per-doc state on switch; full per-file journal revision F16)
- **S8** FORMAT/RIBBON/SHORTCUTS (v2 round-trip; continuous ribbon targets active card; Ctrl+Alt whitelist; destroy() after-job sweep; etc.)
- **S8b** EDITOR UX / PREVIEW / SOFT-LOCK / TOOLTIPS (new slice from UX audit — keeps S8 lean)
- **S9** WORKSPACE UI (Open Project default tab + empty state; native Win32 DnD; in-app console **Option A** + Debug toggle to hide/show external Windows console)
- **S10** MTL DRAWER (3rd tab; retire floating dialog; F8 opens drawer; live-translate OFF by default; apply via central commit)
- **S11** IMPORT FROM XUAT (background index; hybrid Treeview + candidate inspector; exact>norm>fuzzy with fuzzy badge-only; no global XUAT prune)

**Agreement ledger (closed):** baseline hash-proven local==main; **NEW-1 RETRACTED** (false positive from lossy paste — excluded everywhere); S2-before-S3 agreed; F6 vs F12 are separate bugs; performance deferred (measure-first); Console = **Option A + toggle** (user verbatim "Ya, A + toggle"); Grok removed.
**DEFERRED (measure-first):** E-01 search redraw, E-02 keystroke side-effects, E-03 gradient tags.
**OUT OF SCOPE:** Prompt Studio, TM sidecar persistence, splitting misora.py into modules, ignore-SSL, dual card streams, second splash process, compare-all engines.

**Platform migration:** execution moved **GitHub Copilot → Google Antigravity**. From **S2 onward**, format prompts per `google_antigravity_ai_prompting_reference.md` (native `/plan`, `@file`/`@rule`, plan-mode gating, explicit verification loop, permanent rules in `AGENTS.md`/`.agents/rules`). Keep identical slice boundaries, strict file ownership, failing-first regression tests, real command outputs, zero over-engineering.

---

## 5. CURRENT POSITION (CONTINUE FROM HERE)

The user did real-machine testing and reported **UX bugs B1–B10**. Gemini compiled the sync brief (file in Section 2). Gemini asked GPT & Qwen to answer **6 questions** with exact `file:line` evidence. The user said: *"jika kalian berdua sepakat maka saya akan lempar ke gpt. saya tunggu aba-aba kalian."*

**Qwen (previous instance) ALREADY delivered its cross-check verdict:** `Qwen_Phase1b_CrossCheck_B1_B10.md` (in workspace; also summarized in Section 6 below). Verdict = **APPROVED FOR CROSS-CHECK, agree with Gemini, 4 precision corrections, no scope widening.**

**What is pending right now:**
1. **GPT concurrence** on Qwen's verdict (user will relay it).
2. **User decisions on 3 open questions** (Section 7).
3. After concurrence + decisions: the next engineering prompt is **S2 (Dirty Contract), formatted for Antigravity**. The UX items B1–B10 are placed into S4/S8/S8b/S9 and must **NOT** derail or expand S0–S3.

**Your first actions on takeover:**
- Verify repo access (Section 2). Re-confirm baseline HEAD; re-locate any line numbers you quote.
- Read the previous verdict file and Gemini's brief.
- If the user brings GPT's response, cross-check it against source; agree or name precise disagreements.
- If the user answers the 3 open questions, fold them in.
- Do NOT draft the S2 Antigravity prompt until concurrence + user approval, per discipline.

---

## 6. QWEN VERDICT SUMMARY (B1–B10) — BASELINE `095242b`, misora.py = 11,264 lines

> Re-verify line numbers after pulling. Method was direct source read + headless Tk 8.6/Xvfb reproduction for B8. Sandbox baseline: `compileall` PASS; `test_script_codec` 14/14 OK. Full 107-test Windows suite NOT run here (no UnityPy/fixture) — reported honestly, not claimed.

**B6 — line numbers stale → CONFIRMED, narrower than "all views".**
- Page View bug: `_update_gutter_clean()` (def ~4580) called only at toggle ~4511 and render ~6403. Typing path `_on_dialogue_edited()` (~7764) never refreshes gutter. → stale on Enter/Delete/Paste.
- Continuous cards ALREADY correct: `_on_card_text_edited()` (~6503) rebuilds gutter ~6548–6555.
- Plain-text fallback `gutter_cont` (~4232): `_update_gutter_cont()` (~4594) has ZERO callers = dead code.
- Fix (S8): call `_update_gutter_clean()` at end of `_on_dialogue_edited()`; wire or delete dead fallback gutter.

**B8 — paste/import preview blank → CONFIRMED + REPRODUCED (theme contrast, NOT parsing).**
- `_apply_styles()` (~2446) sets `style.configure(".", background=bg_dark, foreground=fg_on_dark)` (~2483). NO `Treeview`/`Treeview.Heading` style exists anywhere. Preview dialog Treeview (~10319) inherits white foreground; clam row fieldbackground stays white.
- Reproduced: dark themes (Misora Classic Dark, Midnight Violet) → fg `#ffffff` on fieldbg `#ffffff`, contrast **1.00 = invisible**. Light themes fine (contrast ~16).
- Block-count guard already correct (~10227); parsing not the cause.
- Fix: ~6-line explicit Treeview/Heading style in `_apply_styles()` (fieldbackground/background=bg_editor, foreground=fg_on_editor, selection map). Placement: S4 or standalone micro-hotfix (Qwen leans standalone).

**B1 — preview caret → no data bug; minor Page-View focus gap.**
- Preview ON = `state="disabled"` (expected read-only; caret hidden). `_commit_widget_edit()` early-returns while preview ON (~7644) so no edits leak.
- Toggle OFF: Continuous restores focus/caret via `_focus_continuous_box()` (~7428–7430). Page View `_sync_clean_view_to_current_box()` re-enables but never `focus_set()`/restores insert mark → caret invisible until click. Add one-line focus restore. The user-approved fix is read-only styling + toast.

**Pin 📌 → different feature than user expects; current impl inconsistent.**
- Actual = "sticky speaker value": `_on_toggle_pin_speaker()` (~6702); guards in `_sync_header_controls_for_card()` (~6603/6621); new-box prefill `on_box_new()` (~6830).
- Does NOT filter navigation: `on_next_box()`/`on_prev_box()` (~7885/7865) only ±1 index.
- Inconsistency: Page View sets speaker unconditionally (`_update_views()` ~6371; `_sync_clean_view_to_current_box()` ~6798), ignoring the pin.
- User expectation (Next/Prev jump to same-speaker boxes) is a NEW feature → needs user decision; treat as distinct S8b item, don't silently overload pin.

**B5 tooltips → AGREE Gemini: 1-tier structured rich tooltip.** Existing `ToolTip` (~104) already has safe 350ms lifecycle; extend to title/body/example. 2-stage adds timer/teardown risk; defer (centralize if ever pursued).

**B1 in-game preview background → contained read-only skin** (styled Frame + Priconne palette + `best_contrast_fg()`), solid frames first, cached PhotoImage later; keep out of Continuous per-card hot path; don't restyle live editor in place.

**B9 soft-lock → bindtag event guard + central-commit safety net.** Current lock is batch-only (`is_box_locked()` ~7902 checked at replace/translate/batch; typing NOT guarded). Keep `state="normal"`; block mutating events on first-position bindtag (reuse Rule-12 infra ~5736/5745/6012), allow navigation/selection/copy; model-level guard in commit path as backstop for IME; Cut→Copy remap when locked. Acceptance must include manual Windows JP-IME test.

**B10 tab UX → AGREE Gemini:** single-click switches tab only; add `+` button and/or double-click-to-open + `Open Project` default + empty state. (Dock tabs ~3241/3252 → `_switch_dock_tab()` ~9046; existing `Open...` ~3376.)

**Antigravity migration → CONFIRMED** for S2+.

**Slice placement:** B8→S4 (or micro-hotfix); B6+B3→S8; B1/B2/B4/B5/B9/Pin→S8b; B10→S9. None touch S0–S3.

---

## 7. OPEN QUESTIONS AWAITING USER / GPT

1. **Pin 📌 semantics:** keep sticky-speaker (and fix Page-View inconsistency) OR add same-speaker jump navigation as a new feature?
2. **B8 placement:** fold Treeview theme fix into S4, or standalone micro-hotfix before S4? (Qwen leans standalone.)
3. **B6 fallback gutter:** wire `_update_gutter_cont()` into plain-text path, or remove the dead gutter widget? (Qwen leans remove unless plain-text line numbers are required.)

---

## 8. S2 DIRTY CONTRACT — SPEC TO PROMPT NEXT (after approval)

Minimum correct contract (small, no journal rewrite):
- (a) Per-entry dirty authoritative per document: True on any actual edit to that doc; False ONLY on that doc's successful save.
- (b) `_dirty_state_changed()` must NOT overwrite per-entry dirty from the global journal. Global undo-to-clean (Rule 13) may drive ACTIVE file title/undo semantics but must not false-clean other cached entries.
- (c) `on_save()` returns explicit success bool.
- (d) Save inactive dirty files WITHOUT switching active UI: helper `_save_document_entry(path, entry)` writes atomically, returns success, marks that entry clean. `on_save()` wraps it for active file; Save All loops dirty entries. (Full S3 builds on this.)
- (e) Close: if user chose Save and file still dirty / save False → abort.
- (f) Exit: Save All dirty entries via (d); abort exit if any required save fails.
Defect anchor (verify line): `_dirty_state_changed()` sets `open_documents[path]["dirty"] = self.is_dirty` from global `undo_journal.is_clean()` → clobbers other files' dirty. Full per-file journal revision (F16) follows in S7.

---

## 9. ANTI-PATTERNS — DO NOT

- Do not restart Phase 0/1 or re-litigate closed ledger items (NEW-1, baseline, Console Option A, Grok removal).
- Do not produce a final coding prompt before concurrence + user approval.
- Do not expand S0–S3 with UI polish; UX goes to S8/S8b/S9.
- Do not trust chat-pasted code or claimed test counts; read disk and run/record real baselines.
- Do not silently overload existing features (e.g., pin) without a user decision.
- Do not claim a full-suite pass you did not run; report environment blockers honestly.
- Do not re-invite Grok.

---

## 10. FIRST MESSAGE TO USER (Bahasa Indonesia) — TEMPLATE

Confirm repo access, state that you are continuing from the delivered B1–B10 verdict (not restarting), summarize the pending items (GPT concurrence + 3 open questions + next S2 Antigravity prompt), and ask the user how they want to proceed (relay GPT response, answer the 3 questions, or authorize S2 drafting). Keep it concise.

---
*End of handoff. The new Qwen should now verify access and continue from Section 5.*
