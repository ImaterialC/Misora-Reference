# MISORA-EDITOR — PHASE 2.5 CANONICAL LEDGER LOCK (PEER AUDIT OF NOTULEN MASTER DRAFT)

Reviewer: Qwen
Baseline Commit: Misora-Editor main @ 683724edaf2afac89d2695a80e30a471a0da9195 (v1.4.0)
Audited Artifact: Phase_2.5_NotulenGemini.md (Misora-Reference @ c3b29d7, "Create Phase_2.5_NotulenGemini.md")
Audit Method: cross-check against (1) all Phase 1 dossiers, (2) Phase_2R1/R2/R3 transcript incl.
  Phase_2R3_GPT.md / Phase_2R3_Grok.md / Phase_2R3_Qwen.md, (3) Project Lead R2 rulings + R3 answers (a)/(b),
  (4) source lines personally verified by Qwen at HEAD 683724e in Phase 1 and Phase 2 R3.
Scope note: sandbox code-execution was unavailable this turn; line citations below reuse Qwen's earlier
  direct reads at the SAME pinned HEAD (unchanged), plus peer R3 confirmations. No new source was assumed.

OVERALL VERDICT: The Notulen is substantively FAITHFUL and COMPLETE. No invented defect, no invented
requirement, no dropped user item. All 34 U-B items mapped; all peer bugs deduplicated; Lead (a)/(b)
recorded correctly (Rulings 5/6, DEF-02). The mismatches below are transcription/citation/provenance
defects, NOT substantive hallucinations. They are correctable and MUST be fixed before LOCKED & IDENTICAL.

======================================================================
A. MUST-FIX BEFORE LOCK (real fidelity defects)
======================================================================

- [MF-1] BUG-08 (csif-backslash-parity) — regex literals and test cases corrupted by backslash loss.
  * Notulen text: "Serialize adds exactly one \ to any body line matching `^*@@`; parse removes exactly
    one \ from `^+@@`. Test exact round-trip for `@@x`, `\@@x`, `@@x`, `\@@x`, and ordinary `\text`."
  * Problem: `^*@@` and `^+@@` are INVALID regexes (bare quantifier with nothing to repeat). The test
    list collapses to duplicates (`@@x`,`\@@x`,`@@x`,`\@@x`) — the 3rd/4th cases lost their extra
    backslashes. This corruption is inherited from Phase_2R3_GPT.md §4.5 and Phase_2R3_Qwen.md §1A
    (markdown/copy pipeline ate the backslashes). GPT R3 §8 test 11 has the correct PROSE.
  * Required correction (restore intended semantics, per QW-B15 / GPT R3 §4.5 / Grok R3):
      - Serialize: add exactly one backslash to any body line matching  ^\\*@@  (zero-or-more leading
        backslashes immediately followed by @@).
      - Parse: remove exactly one backslash from any line matching  ^\\+@@  (one-or-more leading
        backslashes immediately followed by @@). Never strip all leading backslashes.
      - Round-trip test cases must be FOUR DISTINCT inputs:  "@@x", "\@@x", "\\@@x", "\\\@@x"
        (0,1,2,3 leading backslashes), plus an ordinary "\text" line that does NOT precede @@.
  * Why it matters: Antigravity implements from this ledger; an invalid regex / duplicate test list
    would produce a wrong or untestable fix. P0-for-prompt-fidelity (the underlying bug stays P2).

- [MF-2] Stale source provenance in Notulen header + HYG-01 (Reference repo was corrected AFTER the
  Notulen text was drafted).
  * Current repo state (verified via GitHub root tree @ c3b29d7): BOTH `Phase_1_Claude.md` (new) AND
    `Phase_1_Gemini.md` (updated, commit 8625794) now exist. `Phase_1_Gemini.md` now contains GEMINI's
    genuine Phase 1 dossier (Reviewer: Gemini; GEM-B01..B20, GEM-E01..E05, GEM-F01..F05, GEM-R01..R04;
    baseline 8e40994). Claude's dossier was moved to `Phase_1_Claude.md`. This RESOLVES Claude REC-01.
  * Notulen still says: header "Phase_1_Gemini.md (Claude's Phase 1 dossier)" + "Gemini Phase 1 chat
    dossier"; HYG-01 "Phase_1_Gemini.md holds Claude's Phase 1 dossier". Both are now STALE/WRONG.
  * Required correction: update the source-record list and HYG-01 provenance to:
      Phase_1_Gemini.md = Gemini's dossier; Phase_1_Claude.md = Claude's dossier. Drop the "chat dossier"
      fallback now that the authoritative file exists. Reconcile the Gemini coverage map (see MF-3).
  * Why it matters: Antigravity/peers reading "Phase_1_Gemini.md = Claude" will cite the wrong author.

- [MF-3] Gemini coverage map is incomplete vs the now-authoritative Phase_1_Gemini.md; "100%" claim
  is slightly overstated (substance IS present, explicit aliases are missing).
  * Notulen §6 Gemini line maps B01..B20, N01, E01..E05, F05, F06 only. It does NOT explicitly map
    GEM-F01, F02, F03, F04, R01, R02, R03, R04 (all present in the authoritative dossier).
  * Required correction — add explicit aliases (substance already in the ledger):
      GEM-F01 (fixed-box preview)            -> FEAT-10
      GEM-F02 (UX polish: view group/naming/tooltips/soft-lock align; hybrid-pin part) -> FEAT-03, FEAT-05, HYG-03 (+DEF-06 for pin)
      GEM-F03 (docked MTL drawer)            -> FEAT-12, FEAT-13
      GEM-F04 (Import from XUAT)             -> FEAT-14
      GEM-R01 (advscript 6 traps)            -> FEAT-14 guardrails
      GEM-R02 (priconne_tool command table + speaker-completion gate) -> BUG-04, DEF-02, FEAT-14
      GEM-R03 (NewDataMiner 4 gaps)          -> DEF-05
      GEM-R04 (asset_registry reuse + find_match 3-tuple caller bug) -> FEAT-14 / DEF-05 note
  * Also add QWEN R04 -> NO-02 (images are scoped visual references; no AtlasAdv bundling / no game
    emulation). The Notulen Qwen line omits R04 (substance already in NO-02).
  * Provenance note: GEM-F06 (Watermark/Hybrid Pin) is cited in R2 §1#9 / GPT R3 §5 / DEF-06 but is
    ABSENT from the uploaded Phase_1_Gemini.md (which ends at F05). Record GEM-F06's true origin
    (Gemini R1/chat) so the deferred item is traceable; do not silently renumber.

- [MF-4] BUG-19 (save-empty-zero-box-story) — third location cite does not match Grok R3's correction.
  * Notulen cites on_save "(8519, 8524, 8528)". Verified source: 8519 (preview) and 8524 (continuous)
    index boxes directly; the PAGE branch line 8528 is only `txt_dialogue.get(...)` (no indexing) — the
    crash occurs inside inject_box() called at 8529. Grok R3 explicitly corrected this ("the page branch
    crashes inside inject_box, not on line 8528 itself"); the Notulen did not absorb it.
  * Required correction: cite "(8519, 8524, and inject_box call at 8529)". Fix direction (guard all three
    branches when not self.current_doc.boxes) is already correct.

======================================================================
B. RECOMMENDED REFINEMENTS (accuracy / single-owner / guardrails)
======================================================================

- [RF-1] Single canonical severity: BUG-33 and BUG-34 are listed "P1/P2". Phase 2.5 wants one severity
  per ID. Recommend BUG-33 = P1 (silent plaintext credential persistence is a security fail-closed issue;
  the decrypt-warn half is P2 but ride along), BUG-34 = P2 (env leak on reload). Decide and record one.

- [RF-2] BUG-03 / BUG-04 share the inverse-map disambiguation fix. BUG-03 says "separate display names
  from unambiguous inverse ID resolution" and BUG-04 says "Separate Raw Commands display labels from
  binary/inverse ID map". Assign the _INV_CMD_MAP disambiguation to exactly ONE owner (suggest BUG-04)
  and have BUG-03 reference it, so Antigravity does not implement it twice. (cmd0 rewrite stays in BUG-03.)

- [RF-3] FEAT-14 "avoids all 6 advscript.py traps" enumerates: unescaped-= split, block-mode hijack,
  unconditional global conflict resolution, non-deterministic fuzzy set slice, speaker-blind completion,
  global pruning. But GEM-R01's actual 6th trap is "norm2() ignores NGUI tags and {playername}/{0}
  equivalence"; "speaker-blind completion" is GEM-R02 (priconne_tool miss_names), not advscript.
  Restore the norm2 NGUI/{playername} equivalence trap in FEAT-14's guardrail list and attribute
  speaker-blind completion to GEM-R02. (Both matter for indexer correctness.)

- [RF-4] Minor line-range precision pass (all at HEAD 683724e; mechanism correct, ranges slightly off):
    BUG-05 insert_box() starts ~527 (Notulen "553-644" clips its head; delete_boxes 589-612, move_box 614-644).
    BUG-07 _show_paste_preview_and_apply() ends 10766 (Notulen 10756); _populate_tree() 11172-11193 (Notulen 11175).
    BUG-15 on_box_cut() ends 7442 (Notulen 7444).
    BUG-16 on_clear_dialogue_skeleton() 10867-10904 (Notulen 10870-10905); _on_apply() 11839-11867 (Notulen 11840).
    BUG-27 MTLSettingsDialog._on_test_connection() 11395-11411 (Notulen 11410-11427 spans into _on_save).
    BUG-33 protect_secret() 28-61 / unprotect_secret() 64-99 (Notulen 28-62 / 65-100, off by 1).
  These do not change any fix; correct them so Antigravity's /plan line anchors are exact.

- [RF-5] HYG-08 "Remove verified dead code": require per-item unreferenced-proof before deletion.
  Qwen personally confirmed existence of _update_gutter_cont() (4939-4949) and
  BatchTranslateDialog._toggle_pin_top() (11952-11956) but did NOT line-verify each is unreferenced.
  Add guardrail: Antigravity must grep-confirm zero callers for each candidate before removing.
  Also GEM-E04's last bullet ("on_box_new() honors _is_speaker_pinned while Page View _update_views()
  ignores it") is not captured in HYG-08 — either add it or record it as deferred with the pin work.

- [RF-6] DEF-04 "~47 digits" Box 0 Summary figure is an UNMEASURED estimate (not in any verified
  transcript). Keep it explicitly deferred/gated on real in-game measurement; do not let it drive code.

======================================================================
C. CONFIRMED CORRECT (no change needed)
======================================================================
- Baseline pin 683724e; "1 commit ahead of 1924487, only .gitignore, source-identical" — matches
  GPT R3 §1.1 and Grok R3 GitHub compare (ahead_by=1). CONFIRMED.
- Lead (a) keep cmd_id 35/32 until real fixture (Ruling 5, DEF-02) and (b) speaker-clear keeps separate
  boxes (Ruling 6) — correctly recorded; matches GPT R3 §2 and Grok R3 §1. CONFIRMED.
- BUG-02/03/04/05/06/07/10/11/12/13/14/15/16/17/18/20/21/22/23/24/25/26/27/28/29/30/31/32/35/36/37/38/39/40/41
  mechanisms and core line cites match Qwen's direct Phase 1 / R3 verification. CONFIRMED.
- BUG-20 includes Grok-N03 normal-save backup collision (on_save 8494-8495, 8550-8551) — matches Grok R3 §2. CONFIRMED.
- NO-05 (Grok-B05 original retracted; GEM-B02 current-file lock correction), NO-06 (get_icon returns None;
  MisoraLogger not AppLogger), NO-08 (Phase_2R1_Claude.md 22,852 B, Grok retracted empty-file note) — all
  match the R3 transcript. CONFIRMED.
- FEAT-08 .misora references-only + composite lock key + unresolved-lock-notify; FEAT-13 2-widget tk.Text;
  FEAT-14 Import-menu separation + bounded Text source + pre-apply counts + single undo batch; FEAT-10
  wrap="none" bleed 50x3, no AtlasAdv; DEP-1..DEP-10 + Group A-G ordering — all match Lead R2 rulings and
  GPT R3 §6/§7. CONFIRMED.
- All 34 U-B items present in §6 user coverage. CONFIRMED.
- Notulen status "READY FOR PEER AUDIT (NOTULEN MASTER DRAFT)" is the correct pre-lock state; it does NOT
  falsely claim unanimity. Claude's final nod is still absent from the record (no Phase_2R3_Claude.md);
  GPT R3 §9 and Grok R3 gate both note Claude/Grok nods required. Grok has now nodded (R3); Claude pending.

======================================================================
ANTI-HALLUCINATION & OMISSION AUDIT (the two required questions)
======================================================================
- Hallucinations / Unverified Claims Found:
    NO invented defect and NO invented requirement. However, the following unverified/corrupted claims
    MUST be corrected: MF-1 (BUG-08 invalid regex + duplicate test cases), MF-2 (stale Phase_1_Gemini.md
    provenance), MF-4 (BUG-19 page-branch line), RF-3 (FEAT-14 trap list mis-attribution), RF-6 (DEF-04
    unmeasured ~47 figure). The Notulen's self-claim "Hallucinations Found: NONE" is therefore NOT yet
    accurate — it should read "NONE substantive; transcription/citation corrections MF-1..MF-4 pending."
- Omitted Phase 2 Items Found:
    No agreed bug/feature/user-item is substantively dropped. Bookkeeping omissions to close:
    MF-3 (Gemini F01-F04/R01-R04 and Qwen R04 aliases), RF-5 (GEM-E04 _is_speaker_pinned inconsistency).
    The "Omitted: NONE" claim should be qualified until MF-3/RF-5 are recorded.
- Ledger Parity With Peer AIs: MISMATCH — see exact diff in sections A and B.
    Parity will become IDENTICAL once MF-1..MF-4 are applied and RF-1..RF-6 are dispositioned.

======================================================================
PHASE 2.5 GATE DECLARATION
======================================================================
PHASE 2.5 STATUS: MISMATCH FOUND
Blocking Items: MF-1 (BUG-08 regex/test corruption), MF-2 (Phase_1_Gemini.md / Phase_1_Claude.md
  provenance), MF-3 (Gemini + Qwen coverage-map aliases), MF-4 (BUG-19 line cite).
Recommended (non-blocking but should be dispositioned): RF-1..RF-6.
Next step: Notulen (Gemini) applies MF-1..MF-4, dispositions RF-1..RF-6, re-issues the master draft;
Qwen will then re-audit and confirm PHASE 2.5 STATUS: LOCKED & IDENTICAL. Claude's final Phase 2 nod
should also be recorded (or the Project Lead explicitly closes Phase 2) before full panel lock.