# Decision Record: S8b Narrowed Game-Style Dialogue Box Preview Design

**Date:** 2026-11-22  
**Participants:** GPT (Arbiter), Gemini (Technical Reviewer), Qwen (Source Verifier), User (Product Owner)  
**Status:** **UNANIMOUS LOCK & PARKED**  
**Prompt File:** `prompts/S8b-1_narrowed_dialogue_box.md`

---

## 1. Context & Purpose
Translators working in Misora Editor need immediate visual feedback to determine whether localized dialogue fits within in-game Princess Connect! Re:Dive text boxes or overflows.

An earlier AI hallucination produced a standalone web mockup in HTML/JS, which the user firmly rejected: *all preview features must remain native Python/Tkinter widgets inside the desktop editor.*

---

## 2. Critical User Clarification on Word-Wrapping Mechanics
During review, AI models initially assumed that dialogue boxes perform automatic word-wrapping. The user issued an authoritative correction:
1. **Summary Box (Box 0):** Uses automatic word-wrapping.
2. **Story Dialogue Box:** **Does NOT use automatic word-wrapping** (particularly in non-NGUI assets). While the game engine's NGUI plugin can auto-shrink fonts as a fallback, translators must never rely on font shrinking for formatting.
3. **Safe Text Dimension Calibration:** Fixed at `50 characters width × 3 lines height` (`Font.measure("1234567890" * 5)` wide × 3 lines high).
4. **Widget Configuration:** The preview `tk.Text` widget MUST use `wrap="none"` to detect true horizontal spill, combined with dual-axis overflow indicators (vertical line indicator if lines > 3, horizontal spill indicator if line width > safe boundary).

---

## 3. Visual & Safety Specification
- **Palette & Frame:** Lightweight cream panel (`#F9F5EA` / `#FFFDF6`) with double gold border (`#C9A25F` / `#E8CF96`) and dark ink text verified via `best_contrast_fg()`.
- **Next Indicator:** Static pink downward triangle (`▼`) drawn via anti-aliased `Canvas.create_text(..., text="▼")` (zero external bitmap dependencies).
- **Read-Only Protection:**
  * Mode Preview is strictly read-only to safeguard raw NGUI markup.
  * Text selection and `Ctrl+C` remain fully operational.
  * Typing or deleting triggers a non-modal cooldown toast via `time.monotonic()`: *"You are in Preview mode (read-only)."*
  * Disabling Preview cleanly restores focus and caret to the active Single-Box Editor.

---

## 4. Architectural Splitting (S8b-1 to S8b-4)
To maintain narrow, verifiable prompt sizes, the S8b initiative is partitioned into 4 distinct slices:
- **`S8b-1`:** Narrowed Game-Style Dialogue Box Preview (Preview layout, frame, wordwrap, toast). **Status: LOCKED & PARKED.**
- **`S8b-2`:** Ribbon cleanup, monochrome styling, Speaker Pin toggle (`📌`) behavior.
- **`S8b-3`:** Rich 1-tier structured tooltips.
- **`S8b-4`:** Translation soft-lock UX.

---

## 5. Consensus Verdict & Parked Condition
GPT, Qwen, and Gemini unanimously issued **LOCK** on the `S8b-1` Antigravity prompt specification.

**Parked Condition:** Because `S8b-1` is purely a presentation-layer feature, it is **PARKED** and strictly forbidden from early execution before core data-integrity slices S2 through S7 are implemented and verified.
