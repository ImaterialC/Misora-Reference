# COUNCIL KICKOFF PROMPT — MISORA DATAMINE TEXT + MV SUBTITLE

You are joining a new, clean engineering debate for the Misora Editor Datamine plugin.

## Your assignment
Perform **Phase 0 source audit and independent design review only**. Do not edit code, create an implementation prompt, or claim consensus.

Read:
1. `AGENTS.md`
2. `README.md`
3. `docs/LEGACY_TOOLCHAIN_AUDIT_2026-11-23.md`
4. `active_debates/datamine_text_mv/00_KICKOFF_BRIEF.md`
5. `active_debates/datamine_text_mv/01_SOURCE_MAP.md`
6. Candidate source files listed in the source map
7. Current `Misora-Editor/AGENTS.md`, `PROJECT_STATE.md`, `core/story_ast.py`, `core/bundle_io.py`, and relevant tests

## Important boundaries
- First release target is text datamine and MV/movie subtitle records only.
- Keep master.db read-only.
- Distinguish DB text, Unity TextAsset, ADV story text, subtitle MonoBehaviour records, and `.usm` video files.
- Do not assume a `.usm` contains the subtitle text.
- Do not assume the recordList schema is complete based on the old codec. Verify it against actual typetree fixtures.
- The legacy subtitle repack path has no read-back verification in the inspected version. Treat it as unverified.
- Do not rename old source files in place or delete archives.
- Do not invent Misora Editor APIs. Inspect the target code.

## Independent review output
Use `02_REVIEW_TEMPLATE.md` and save your completed copy as `REVIEW_<MODEL>_PHASE0.md`.

Must answer:
1. Which legacy source modules are the best starting point and why?
2. Which source copies are identical to curated V2/V3 and which are different variants?
3. What is the exact data path for master.db text, ADV story `.txt`, and MV subtitle JSON?
4. How can movie manifest entries be linked to the subtitle-bearing Unity bundle? What evidence is missing?
5. What real fixture(s) are needed before D3 is safe?
6. What should the plugin headless API look like?
7. Which parts should remain out of scope?
8. What tests are required before integration into Tkinter?

For every technical claim, provide file path and code symbol/line evidence. Label each statement `CONFIRMED`, `UNVERIFIED`, or `CONTRADICTED`.

End with a recommendation: `PROCEED`, `PROCEED WITH CONDITIONS`, or `BLOCK`.

**Do not use unanimity as a substitute for evidence. Do not write an Antigravity implementation prompt until the Product Owner approves the design.**
