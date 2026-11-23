# MISORA-EDITOR - PHASE 3 PROMPT ENGINEERING PROPOSAL (ROUND 1 - QWEN)

Reviewer: Qwen (sole evaluator) + Gemini (Notulen). Baseline pinned: 683724e (v1.4.0).
Source: Phase_2.5_Canonical_Ledger_LOCKED.md (FE-1..FE-3 stamped, verified).

## 1. SESSION COVERAGE TABLE (100% exactly-once, verified programmatically: 63/63)
S01 HYG-01                                  | docs/ledger reconcile          | Flash-eligible (explicit list) / Sonnet
S02 BUG-01,03,04                            | binary+v2 integrity, cmd map   | Opus 4.6
S03 BUG-02,05,06                            | projection identity, ownership | Opus 4.6
S04 BUG-07,08,09                            | CSIF transactional + escape    | Sonnet 4.6
S05 BUG-11,12,13                            | save/state/commit integrity    | Opus 4.6
S06 BUG-10,15,16,17                         | lock enforcement + undo        | Sonnet 4.6
S07 BUG-21,22,23,30                         | search matcher/report/roots    | Sonnet 4.6
S08 BUG-24,20                               | replace-all cache/locks/backup | Opus 4.6
S09 BUG-25,26                               | XUAT uid keys + atomic write   | Sonnet 4.6
S10 BUG-27,14                               | MTL queue marshal + cancel     | Opus 4.6
S11 BUG-18,19,34,35,36 + HYG-04,05,06       | mechanical safety batch        | Flash-eligible / Sonnet
S12 BUG-29,32,33 + HYG-02,07,08             | shortcuts/logger/DPAPI/hygiene | Sonnet 4.6
S13 BUG-28,31,37,38,39 + FEAT-04            | UI foundations + ribbon        | Sonnet 4.6
S14 FEAT-01,02,03 + HYG-03                  | scope/player/view/tooltips     | Flash-eligible / Sonnet
S15 FEAT-05,06,07 + BUG-41                  | select-box/drawer/multi-open   | Sonnet 4.6
S16 FEAT-09,10 + BUG-40                     | pixel ruler + preview          | Sonnet/Opus
S17 FEAT-08                                 | .misora workspace              | Sonnet 4.6
S18 FEAT-11                                 | editable Raw Commands          | Opus 4.6
S19 FEAT-12,13                              | MTL drawer                     | Sonnet/Opus
S20 FEAT-14                                 | XUAT importer                  | Opus 4.6

## 2. DEPENDENCY CHECK
DEP-10 HYG-01 first (S01). DEP-5 BUG-01..06 (S02/S03) before FEAT-11 (S18). DEP-2 BUG-11 (S05)
before FEAT-10 (S16)/FEAT-14 (S20). DEP-4 BUG-12 (S05) before lock fixes (S06)/FEAT-05 (S15)/FEAT-08
(S17). DEP-6 BUG-14+27 (S10)+HYG-01 sec24 before FEAT-12/13 (S19). DEP-7 BUG-25 (S09)+BUG-23 (S07)
before FEAT-14 (S20). DEP-9 BUG-35 (S11)+FEAT-07 (S15) before FEAT-08 (S17). DEP-8 shared measure
helper built in S16. DEP-3 BUG-28 (S13)+HYG-03 (S14) with FEAT-02/04.
DEP-1 NOTE for panel: BUG-31 (Treeview theme) placed S13. S19/S20 use tk.Text/paired boxes (not new
Treeview), so DEP-1's real gate (new Treeview features) is satisfied. S04 touches the EXISTING
ScriptPastePreviewDialog logic (headless-testable), not a new Treeview build. If panel reads DEP-1
strictly (theme before ANY dialog work), move BUG-31 earlier - flag for debate.

## 3. COMMAND UTILIZATION (map every useful native command)
/plan        -> EVERY session (mandatory Planning-First gate; human Proceed).
/model /effort -> per-session tiering above (Opus hard, Sonnet medium, Flash mechanical).
/goal        -> optional wrapper for autonomous hygiene sweeps (S11/S12) WITH strict command-verifiable
                Done checklist (no iteration cap; must avoid fake-success).
/compact     -> between milestones / when context grows (leading token only).
/btw         -> side questions without polluting main context.
/learn       -> persist a rule after any repeated mistake.
@file        -> explicit context pointers in every prompt (no chat-summary reliance).
/boost       -> OPTIONAL for hard slices (S03/S05/S08/S10) IF Pro plan enables; fallback /plan.
/swarm       -> OPTIONAL cross-model verification: worker Sonnet 4.6, @verifier Opus 4.6 or GPT-OSS 120B
                (read-only). Quota-heavy; NOT default. Exclusive file ownership if used.
CLI /diff /artifact -> review; /rewind /fork -> recovery; /context /usage -> token budget.
NOT USED (honest): /grill-me (spec locked; would reopen settled items), /browser (Tkinter desktop, not
web), /teamwork /run-workflow /automation /generative_ui /mcp-app-development (over-engineering).

## 4. PROMPT DESIGN PRINCIPLES (anti-misinterpretation / cheap-model safety)
- Closed-world: exact file+line anchors, exact acceptance tests, forbidden-actions list, STOP conditions.
- Failing-first Defect Probes (FAIL before, PASS after) + Regression Guards (PASS before+after, pre-patch
  contracts only). Full existing suite must stay green.
- Strict file ownership (Allowed vs DO NOT modify) + Out-of-Scope per session.
- No new deps, no test weakening, no destructive git, no secrets, preserve untracked config.
- ASCII-only prompt text + SHA-256 per file (anti character-corruption).
- Small diff surface so weak models stay focused; /plan human gate is the final safety net.
- HONEST tiering: Flash only on designated mechanical slices; GPT-OSS 120B verifier-only.

## 5. DELIVERABLES THIS ROUND
Full prompts for S01 and S02 (pattern exemplars) attached as ASCII blocks + SHA-256. Remaining 18
session prompts to be generated after panel approves slicing/order/test-strategy (Phase 3 gate).

PHASE 3 STATUS: OPEN - DEBATING PLAN/PROMPTS