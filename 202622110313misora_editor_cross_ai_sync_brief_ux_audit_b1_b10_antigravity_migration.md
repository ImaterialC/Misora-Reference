# MISORA EDITOR — CROSS-AI SYNC BRIEF (UX AUDIT B1–B10, DESIGN DECISIONS & ANTIGRAVITY MIGRATION)

**From:** Gemini (Compiled from User Testing, Decisions & Technical Review)  
**To:** GPT & Qwen (Assistant A)  
**Purpose:** Sync all newly discovered UI/UX bugs, finalized user preferences, honest technical critiques, and the execution platform shift to **Google Antigravity** without derailing the locked `S0–S11` data-integrity roadmap.

---

## 1. EXECUTION PLATFORM UPDATE — MIGRATION TO GOOGLE ANTIGRAVITY

- The user has begun executing and **migrated from GitHub Copilot to Google Antigravity**.
- **Prompting Implication (Phase 2 onward):**
  - Keep all locked engineering discipline unchanged: narrow single-slice scope, strict file ownership, failing-first regression tests, real command outputs, zero over-engineering, and `AGENTS.md` invariants.
  - Starting with the next slice prompt (e.g., `S2`), adapt surface/mode instructions to **Google Antigravity** conventions (aligned with the repository's `google_antigravity_ai_prompting_reference.md`) rather than Copilot-specific slash commands/surfaces.

---

## 2. NEW BUGS & UX FINDINGS FROM REAL USER TESTING (B1–B10)

> **Verification Note:** Items marked `[NEEDS-CODE-VERIFY]` have not been inspected at exact line level by Gemini and must be verified against the authoritative local `misora.py` / `core/script_codec.py` before any Phase 2 prompt includes them.

### A. Preview Mode (Eye Icon), Ribbon Grouping & Header Naming (B1–B4)

1. **B1 — Preview Mode Behavior & Visual Redesign (`CONFIRMED DESIGN + [NEEDS-CODE-VERIFY]`)**
   - **Observed Issue:** Toggling Preview hides the typing cursor; text can be highlighted/copied, but cannot be edited or deleted (expected Tkinter `state="disabled"` behavior, currently lacking clear visual feedback).
   - **Verify:** Confirm whether toggling Preview **OFF** always cleanly restores the caret and normal editability in both Single and Continuous views.
   - **User-Approved Design:**
     - Keep Preview strictly **Read-Only** (protects raw NGUI markup).
     - Change the Preview layout/background to resemble the **in-game Princess Connect! Re:Dive dialogue box aesthetic** (lightweight Tkinter styling: frame/border/background palette matching in-game look — avoid heavy canvas/image redraw overhead or breaking readability).
     - When any text edit/delete attempt is detected while Preview is active, trigger a non-modal notification (toast with cooldown): *"You are in Preview mode (read-only)."*

2. **B2 — Unified View Group on Top Ribbon (`DESIGN`)**
   - Move Preview (`👁`) into the same top ribbon group as **Single/Continuous View** and **Select Box**, with uniform monochrome/theme-adaptive icons separated cleanly from NGUI formatting buttons.
   - Dim/disable NGUI formatting buttons while Preview is ON so users immediately see editing tools are inactive.

3. **B3 — Continuous View NGUI Formatting Dead (`ALREADY CONFIRMED`)**
   - Confirmed duplicate of `F-GPT-13` / `NEW-2` (`_insert_text_wrapper` targets hidden `txt_continuous` instead of the active card editor). Remains scheduled in **S8**.

4. **B4 — Replace Misleading `"GAME VIEW (xxxxx)"` Header (`DESIGN`)**
   - Dynamic header reflecting actual active mode:
     - Single + Edit: `DIALOGUE EDITOR (Box #N)`
     - Single + Preview: `GAME PREVIEW — Read-Only (Box #N)`
     - Continuous + Edit: `CONTINUOUS EDITOR (N Boxes)`
     - Continuous + Preview: `GAME PREVIEW — Continuous • Read-Only`
     - Lower pane: `RAW SCRIPT (v2)`

---

### B. Tooltips & Line Numbers (B5–B6)

5. **B5 — Structured Tooltips (`USER DECISION + OPEN CRITIQUE ON 2-STAGE`)**
   - Nearly all buttons/controls currently lack helpful tooltips.
   - **User-Accepted Baseline (1-Tier Rich Tooltip):**
     - Single clean popup with clear typographic hierarchy:
       1. **Large Bold Title:** Full real function name + shortcut (no cryptic abbreviations).
       2. **Smaller Body:** Concise 1-line description.
       3. **Smallest Italicized Footer:** Concrete usage example or beginner-friendly explanation.
   - **Open Critique Requested by User (1-Tier vs. 2-Tier):**
     - The user noted that a **2-stage timed tooltip** (short hover = title; longer hover = description + example) might be nice, **but explicitly welcomes objections and technical critiques if it is risky or harmful**.
     - **Gemini's Position:** Strongly recommend **1-tier structured tooltip** (single ~350–400 ms delay). Why: (a) faster to scan without forcing users to hold the mouse still twice; (b) avoids extra stateful `after()` timers that risk Tcl teardown leaks (`F23`) or flicker during rapid cursor sweeps. If 2-stage is ever considered, it MUST be centralized in a single `TooltipManager` that cancels all pending jobs on `<Leave>`, `<ButtonPress>`, `<Destroy>`, and `MisoraApp.destroy()`.

6. **B6 — `Show Line Number` Does Not Update on Newline / Delete / Multiline Paste (`NEW BUG [NEEDS-CODE-VERIFY]`)**
   - **Symptom:** Pressing `Enter`, deleting a line break, or pasting text containing line breaks does NOT update line numbers across **all views**.
   - **Likely Root Cause to Verify:** Line-number gutter redraw is either missing bindings for `<Return>`, `<BackSpace>`, `<Delete>`, `<<Paste>>`, `<<Cut>>`, `<<Modified>>`, or reads line counts before Tkinter finishes mutating the `Text` widget (missing `after_idle` redraw).

---

### C. CSIF Clipboard Detection, Paste Dialog & Blank Preview Bug (B8)

7. **CSIF Paste Dialog & Routing Rules (`USER SPEC`)**
   - Make clipboard CSIF paste choices explicit and position-aware:
     - Option 1: `Insert as New Box (after Box #N)`
     - Option 2 (single box): `Replace Current Box (Box #N)`
     - Option 2 (multiple boxes): `Replace Current Box Onward (Box #N–#M)` *(note overflow/append behavior clearly if clipboard has more boxes than remain in the story)*.
   - Multi-box CSIF paste (`> 1` box) opens **Paste Import Script Preview**.
   - Clipboard containing a **Box 0 header** bypasses Insert entirely and opens **Paste Import Script Preview** directly in **Replace** mode.

8. **B8 — Paste Script / Paste Import Preview Displays Nothing (`NEW HIGH-PRIORITY BUG [NEEDS-CODE-VERIFY]`)**
   - **Symptom:** User pasted a script and the Paste Import Preview window rendered empty/blank.
   - **Action Needed:** Inspect `ScriptPastePreviewDialog` in `misora.py` and `core/script_codec.py` parsing/normalization to identify why valid/semi-valid pasted scripts yield an empty preview or blank widget.

---

### D. Translation Lock Visuals & Soft-Lock Behavior (B9)

9. **B9 — Lock Icon Placement, Alignment & Soft-Lock UX (`USER SPEC + TECHNICAL GUARDRAILS`)**
   - **Continuous View Placement:** Place the lock icon to the right of the Select Box toggle (when enabled), immediately before the dot and box number.
   - **Alignment Invariant:** Hiding the Select Box toggle on a box MUST NOT shift the lock icon or box number horizontally (use fixed-width grid column or placeholder spacer instead of collapsing layout via `pack_forget()`).
   - **Visual Style:** Show lock icon on every box — keep current liked lock glyph, using a subtle/low-contrast muted tone when unlocked and a crisp prominent state when locked.
   - **Soft-Lock Behavior:**
     - Keep cursor visible and allow text selection/copying (do NOT use hard `state="disabled"`).
     - Block all mutations (typing, `BackSpace`/`Delete`, `<<Paste>>`, drag-drop text, **and Japanese IME composition commits**) and display a cooldown toast: *"Box is locked — unlock it first to edit."*
     - `Cut` button and `Ctrl+X` on a locked box act as **Copy** without deleting text (with a brief toast confirmation).

---

### E. Speaker Pin Icon (`📌`) & Left Tab Confusion (B10)

10. **Speaker Pin Icon (`📌`) (`[NEEDS-CODE-VERIFY] + USER EXPECTATION`)**
    - **Action Needed:** Verify the current code behavior of the `📌` button beside the speaker field in `misora.py` and explain the original design intent vs. actual implementation.
    - **User Expectation:** Toggling `📌` pins the current speaker so `Next` / `Prev` buttons jump strictly to the next/previous box spoken by that **same speaker**, displaying a jump notification (e.g., `Pinned: <Speaker> — Box #24 (3/12)` or boundary notice) and a clear hover tooltip.

11. **B10 — `Opened Files` Tab Mistaken for `Open File` Button (`UX SIGNIFIER FIX`)**
    - **Problem:** Users routinely click the `Opened Files` tab expecting a file picker dialog to open.
    - **User Idea:** Dual-function tab that also opens the file picker.
    - **Gemini Critique for Debate:** Triggering a modal OS file dialog on a **single tab click** can disrupt users who simply switch to the tab to drag-and-drop files or inspect the list. Recommend pairing **S9's default `Open Project` tab + big `Open Files...` Empty State** with either:
      - a dedicated compact **`+`** icon button directly in the tab header strip, and/or
      - **double-click on the tab** to trigger the file picker (single-click switches tab cleanly).

---

## 3. PROPOSED SLICE INTEGRATION (PROTECTING S0–S7 DATA SAFETY)

Do **not** expand `S0–S3` data-safety slices with UI polish. Proposed placement:

| Item | Type | Proposed Slice |
| :--- | :--- | :--- |
| **B8 (`PASTE-PREVIEW-EMPTY`)** + CSIF Paste UX | New Bug + UX | Verify now; fix **B8** in **S4** (Structural/Paste) or **S4b**; CSIF dialog labels in **S4/S8b** |
| **B3 (`F-GPT-13` Continuous Ribbon)** | Confirmed Bug | **S8** (already scheduled) |
| **B6 (`LINE-NUMBER-STALE-ON-NEWLINE`)** | New Bug | **S8** (after source verification) |
| **B1, B2, B4, B5, B9, Pin `📌`** | UX & Editor Polish | Dedicated **S8b — Editor UX, Preview, Soft-Lock & Tooltips** (keeps S8 lean) |
| **B10 (`Opened Files` / `Open Project` tab)** | Sidebar UX | **S9** (Left Sidebar Workspace, already scheduled) |

---

## 4. QUESTIONS FOR GPT & QWEN (PHASE 1b/2 CROSS-CHECK)

Please answer with exact `file:line` evidence from the authoritative `misora.py` / `core/` tree:

1. **Source Verification (4 items):**
   - **B6:** Where are line numbers rendered/updated, and why do Enter/Delete/Paste miss updates?
   - **B8:** What causes `ScriptPastePreviewDialog` to render empty on pasted scripts?
   - **B1:** When Preview is toggled OFF, is there a real caret-restoration bug or only `state="disabled"` read-only confusion?
   - **Pin `📌`:** What does the `📌` icon next to Speaker currently do in `misora.py`?
2. **B5 Critique (1-Tier vs. 2-Tier Tooltips):** Do you agree with Gemini's pushback favoring a **1-tier structured Rich Tooltip** (Title / Short Description / Small Italic Example) over a 2-stage timed tooltip, or is a centralized 2-stage `TooltipManager` safe and worthwhile?
3. **B1 In-Game Preview Background:** What is the cleanest, lowest-risk way in Tkinter to style the Preview box background/frame like Priconne's in-game dialogue box without breaking dark/light themes or Continuous View performance?
4. **B9 Soft-Lock Implementation:** What is the cleanest Tkinter mechanism to keep the caret visible and selection/copy active while reliably blocking typing, `<<Paste>>`, `Delete`/`BackSpace`, and **Japanese IME commits** (and remapping `Cut` -> `Copy`)?
5. **B10 Tab UX:** Do you agree with Gemini's refinement (`+` button / double-click tab + `Open Project` default) over single-click modal file picker?
6. **Antigravity Migration:** Confirm we will format subsequent Phase 2 prompts (`S2+`) for **Google Antigravity** using `google_antigravity_ai_prompting_reference.md` while keeping the exact same slice boundaries and verification discipline.