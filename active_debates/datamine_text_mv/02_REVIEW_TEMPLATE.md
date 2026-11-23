# Independent Review — Datamine Text + MV Subtitle

**Reviewer/model:**  
**Date:**  
**Repository commit(s) inspected:**  
**Files actually opened:**  
**Tools available in this session:**  

## 1. Independent understanding
Restate the requested plugin in your own words. Do not assume the previous reviewer's conclusion.

## 2. Source inspection evidence
For each claim, cite exact file paths, functions/classes, and line ranges or code excerpts.

| Claim | Evidence | Status (`CONFIRMED` / `UNVERIFIED` / `CONTRADICTED`) |
|---|---|---|
|  |  |  |

## 3. Text data pipeline
Describe the proposed source, identity, extraction, export, import and validation path for:
- `master.db` text tables
- Unity TextAssets
- ADV story scripts

## 4. MV subtitle pipeline
Describe:
- How the subtitle-bearing bundle is found.
- How the relevant MonoBehaviour is selected unambiguously.
- Required record fields and optional/unknown fields.
- Whether record count can change.
- How start/end timing is preserved.
- How output is reopened and verified.
- How it maps to a movie `.usm`, if that relationship is proven.

## 5. Risks and failure modes
List at least five concrete failure cases and how to test each.

## 6. Minimal architecture
Propose a headless API before proposing UI. Name real existing Misora APIs only after checking the target repository source.

## 7. Test plan
Include synthetic fixtures, real fixtures, round-trip checks, malformed input, missing database, missing manifest, and GUI-thread safety.

## 8. Objections to your own proposal
What part of your proposal is weakest? What evidence could disprove it?

## 9. Recommendation
State `PROCEED`, `PROCEED WITH CONDITIONS`, or `BLOCK`. List any unresolved questions for the Product Owner.

**Rules:** do not claim a test passed unless you executed it; do not infer uninspected file contents; do not treat consensus as verification.
