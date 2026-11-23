/plan Implement Session S02: Binary & v2 Serialization Integrity (BUG-01, BUG-03, BUG-04) in Misora Editor.

CONTEXT POINTERS (READ DIRECTLY FROM DISK BEFORE PLANNING):
@AGENTS.md @PROJECT_STATE.md @core/story_ast.py @misora.py @tests/test_misora_core.py @tests/test_script_codec.py

==================================================
PART 0 - EXECUTION MODE, GATE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate (STRICT): Do NOT modify any file during /plan. Inspect live disk, produce an
   Implementation Plan artifact, WAIT for Proceed. After Proceed, work in failing-first TDD order and
   produce a Walkthrough artifact with real outputs.
2. Workspace & Git Hygiene: Report branch, HEAD hash, git status --short, Python 3.12 path/version.
   Expected pinned baseline 683724edaf2afac89d2695a80e30a471a0da9195 (v1.4.0). If HEAD differs or
   unexpected uncommitted changes conflict, STOP and report. NEVER run git reset/clean/stash,
   destructive checkout, commit, or push.
3. Allowed File Ownership (after approval):
   - core/story_ast.py (scoped to serialization + command map + breaker classification ONLY).
   - misora.py (ONLY the _update_raw_view Box 0 highlight condition near line 6825).
   - tests/test_s02_serialization_integrity.py (NEW).
   - PROJECT_STATE.md (measured verification update only).
   DO NOT modify: core/script_codec.py, core/bundle_io.py, core/undo_journal.py, any other misora.py
   region, assets/, other test files, config files.
4. No new external dependencies. Follow AGENTS.md invariants (byte-exact binary codec, main-thread
   Tk safety, undo integrity, atomic writes).
5. Never remove/skip/weaken/mock existing tests. No live network calls in tests.
6. Stop strictly after S02. Do NOT implement BUG-02/05/06 (projection identity / structural ownership /
   multi-segment) - those belong to S03.

==================================================
PART 1 - PREFLIGHT VERIFICATION (INCLUDE IN PLAN)
==================================================
Report exact current line ranges in core/story_ast.py for: from_binary (~670-697), to_binary
(~699-729, cmd_id==0 special case ~710-712, empty-arg space sentinel ~725), escape_arg (~124-138),
unescape_arg (~141-169), Record.render_v2 (~185-197), from_v2_text (~735-788, blank-line break ~771,
category check ~773), _CMD_MAP (~40-57), _INV_CMD_MAP (~58), DEFAULT_BREAKERS (~33),
_rebuild_boxes (~295-334). In misora.py report _update_raw_view Box 0 highlight (~6823-6828).
If any anchor drifted from the pinned baseline, STOP and surface the discrepancy before editing.

==================================================
PART 2 - REQUIRED IMPLEMENTATION (BUG-01, BUG-03, BUG-04)
==================================================
A. BUG-01 strict binary parse: in from_binary, validate record header, 4-byte arg length, arg payload
   bounds, and the length-0 terminator. On truncated/trailing/overrun bytes RAISE ValueError (or the
   module's existing error type) instead of silently breaking. Refuse to produce a partial document.
   Do NOT add command-specific arity checks (some arities are unknown per PROJECT_STATE 8.4).
B. BUG-03 v2 losslessness + cmd0:
   - escape_arg: escape trailing/whitespace-only spaces as \s (ASCII space) and \S (U+3000); prefix a
     backslash when the escaped arg equals a DEFAULT_CATEGORIES name; emit \b64:<base64> for args
     containing surrogate-escaped non-UTF-8 bytes. unescape_arg must reverse ALL of these exactly.
   - to_binary: REMOVE the legacy cmd_id==0 remapping branch (~710-712). Numeric cmd_id is authoritative.
   - render_v2: remove the dead "if self.cmd_name in _CMD_MAP" conditional; ALWAYS emit name#id header
     (unconditional) so v2 is lossless. Do not emit bare names.
   - misora.py _update_raw_view: Box 0 cmd_id==0 highlight must test r.args[0] (not r.args[1]), matching
     get_metadata. Change only that condition.
C. BUG-04 command map + breakers (GUARD 35/32):
   - Separate Raw Commands display labels from the inverse id map so display cleanup never changes a
     numeric id. Make plain-name v2 header resolution unambiguous (a name mapping to multiple ids must
     require #id; do not silently pick last-wins).
   - Classify structural breakers by verified numeric cmd_id: 0=title, 1=outline, 4=type, 10=goto,
     36=situation. NEVER treat cmd_id==12 with a vo_ argument as a breaker. Preserve cmd_id==6 dialogue
     projection. Do NOT change the speaker/kind merge grouping logic in _rebuild_boxes (that is S03).
   - HARD GUARDRAIL: NEVER alter binary cmd_id 35 (narration) or 32 (subtitle) on any path.

==================================================
PART 3 - FAILING-FIRST TESTS (tests/test_s02_serialization_integrity.py)
==================================================
Use unittest; preserve/restore misora.CONFIG_PATH in setUp/tearDown; suppress modal messagebox; no network.
Defect Probes (MUST FAIL before patch, PASS after):
 1. from_binary on a truncated final record raises (no partial doc).
 2. binary->v2->binary round-trip preserves a whitespace-only arg " " exactly.
 3. binary->v2->binary round-trip preserves an arg equal to "Sound" and an arg equal to "Other".
 4. binary->v2->binary round-trip preserves an invalid-UTF-8 arg via \b64: (surrogateescape).
 5. a cmd_id==0 record with a non-fade name keeps cmd_id 0 through to_binary.
 6. records with cmd_id 35 and 32 keep those ids through binary and v2 round-trips.
 7. a mid-script title(0)/outline(1) record splits boxes (breaker by id).
Regression Guards (MUST PASS before AND after; reference only pre-existing contracts):
 1. existing well-formed binary round-trips byte-exact (to_binary(from_binary(b)) == b).
 2. existing v2 files with name#id headers parse unchanged.
 3. the full pre-existing test suite stays green.

==================================================
OUT OF SCOPE (DO NOT IMPLEMENT)
==================================================
- BUG-02/05/06 (S03), BUG-07/08/09 (S04), all other ledger items, all features.
- Do not change empty-arg space sentinel behavior (DEF-01, test-only).

==================================================
PART 4 - VERIFICATION COMMANDS & DELIVERABLES
==================================================
1. Now (/plan, ZERO edits): Implementation Plan artifact, WAIT for Proceed.
2. After Proceed: write tests -> run pre-fix (record Probes failing, Guards passing) -> implement -> run:
   - py -3.12 -m compileall -q misora.py core assets tests
   - py -3.12 -m unittest tests.test_s02_serialization_integrity -v
   - py -3.12 -m unittest discover -s tests -v
   - Walkthrough with exact commands, real outputs, git status --short, concise diff summary, handoff to S03.