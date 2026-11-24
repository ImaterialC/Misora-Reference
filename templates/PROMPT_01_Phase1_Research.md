# MULTI-AI ENGINEERING COUNCIL — PHASE 1 (INDEPENDENT RESEARCH DOSSIER)

Project: **[PROJECT_NAME]** | Pinned Baseline: `[40_CHAR_COMMIT_SHA]` (`[CURRENT_VERSION]`)
Cycle Goal: **[SHORT_GOAL_DESCRIPTION]**
Inputs: Target repo at pinned commit (or provided split parts `*_part01..N` with original line headers) + `USER_WISHLIST.md` + `AGENTS.md` + `PROJECT_STATE.md` + `CHANGELOG.md` + `tools/` & `references/` from Phase 0.

You are conducting **INDEPENDENT RESEARCH**. Do NOT assume what other AIs will find, do NOT write final Antigravity prompts yet, and do NOT invent runtime outputs you did not actually run.

## Mandatory Research Rules
1. **Bind Every Finding to Live Code:** Cite exact `file_path`, `symbol/function_name`, and **ORIGINAL** line range at `[40_CHAR_COMMIT_SHA]` (if reading split parts, always report the original file's line numbers from the part header!).
2. **Strict Epistemic Labels:** Tag every item `[CONFIRMED]`, `[NEEDS-VERIFY]`, or `[CONFLICT]` (docs/tests contradict live code).
3. **100% Wishlist Traceability:** Every single `U-01..U-N` item in `USER_WISHLIST.md` MUST be explicitly evaluated (`ACCEPT` / `REFINE` / `DEFER` / `REJECT`) with concrete code touchpoints and risks.
4. **Hunt Hidden Traps Early:** Look explicitly for data-loss/encoding/atomicity traps, threading/stale async callbacks, brittle existing tests (e.g., hardcoded version or UI assertions), and dependency ordering (`DEP-1..N`).

## Required Output Structure (Strict Markdown Dossier)
Use prefixed IDs with your AI tag (e.g., `[GPT-B01]` bugs, `[GPT-F01]` features, `[GPT-E01]` hygiene, `[GPT-Q01]` open questions):

### 1. Executive Baseline Audit
- Pinned SHA verified, docs-vs-code drift, and brittle existing tests that may break during this cycle.

### 2. Confirmed Bugs & Integrity Risks (`[AI-B01..]`)
- `Severity (P0/P1/P2)` | `Status` | `File:Symbol (Original Lines)` | `Exact Failure Mechanism` | `User Impact` | `Minimal Root-Cause Fix & Test Proof`.

### 3. Wishlist & Feature Analysis (`[AI-F01..]`)
- Map 100% of `U-01..U-N`: `Recommendation` | `Dependencies` | `Exact Touchpoints` | `Guardrails`.

### 4. Efficiency, Hygiene & Reference Traps (`[AI-E01..]`)
- Dead code (must require grep proof before deletion), test leaks, or pitfalls in `tools/` / `references/`.

### 5. Proposed Dependency Graph & Collision Files
- Hard edges (`DEP-1..N`) and high-collision monolithic files that MUST be edited serially.

### 6. Open Questions for the Project Lead (`[AI-Q01..]`)
- Only genuine product/design decisions that cannot be inferred from code, each with a recommended safe default.

End with: `PHASE 1 STATUS: COMPLETE — READY FOR PHASE 2 CROSS-EXAMINATION`
