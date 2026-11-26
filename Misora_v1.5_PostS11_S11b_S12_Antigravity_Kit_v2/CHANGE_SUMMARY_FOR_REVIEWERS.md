# Change Summary — Post-S11 S11b–S12 Antigravity Kit v2 (All Qwen + ChatGPT Corrections Applied)

Responding To:
- `qwen.txt` (Independent Technical Audit — Blocker E-1 + Minor Notes N-1, Forbidden-Core STOP, S12 `FIXED` evidence rule)
- `gbt.txt` (GPT Independent Review — 6 Final Corrections across S11b, S11d, and S12)

Execution Boundary: Prompt kit revision ONLY. Zero source files modified; zero `/plan` sessions started; `v1.5.0` remains ON HOLD. Per-session authorization remains enforced: **`S11b` is submitted first for line-by-line review; `S11c`–`S12` will be re-verified sequentially at their respective turns.**

## All Corrections Applied in Kit v2

1. **S11b `Q-01` — Binding Erratum `E-1` & GPT #1 (Replaced ALL `by_norm_key` with `XuatIndex._norm_stripped_map`):**
   - Removed every fictional `by_norm_key` reference in `S11b`.
   - Locked `XuatIndex._norm_stripped_map` (`strip_ngui=True`) as the authoritative structure:
     * `unique_keys = len(idx._norm_stripped_map)`
     * `duplicate_keys = sum(1 for v in idx._norm_stripped_map.values() if len(v) > 1)`
     * `entries_read` increments ONLY when `normalize_xuat_key(raw_key, strip_ngui=True) != ""`
     * `duplicate_entries = entries_read - unique_keys`
     * Tested identity: `entries_read == unique_keys + duplicate_entries`.
   - Added explicit `/plan` parity guard on `add_entry()` so empty normalized keys are never counted in `entries_read` / inserted into `_norm_stripped_map` while exact-tier (`_exact_map`) and value-lookup (`_value_map`) parity is explicitly verified by regression tests.

2. **S11b `Q-01` — Strict `Translation\en\Text` Resolver Hardening (GPT #2 + Qwen N-1):**
   - Closed all 3 permissive paths in `resolve_xuat_text_roots()` (unvalidated direct `.txt`, arbitrary `Text` dir, non-English `p / "Text"` such as `Translation\ja\Text`).
   - Explicitly supported Project Lead's real `src\BepInEx` hierarchy under Game Root (`<GameRoot>\src\BepInEx\Translation\en\Text` AND `<GameRoot>\BepInEx\Translation\en\Text`) plus `BepInEx`, `Translation`, `Translation\en`, `Translation\en\Text`, and direct `.txt` ONLY inside `Translation\en\Text`.
   - Added mandatory negative tests for ALL 5 forbidden targets: `Translation\ja\Text`, arbitrary unrelated `Text`, standalone `.txt` outside `Translation\en\Text`, `Translation\en\Other`, and `Translation\en\RedirectedResources`.

3. **S11b `Q-02` — Explicit Forbidden-Core STOP Rule (Qwen minor note):**
   - Added explicit STOP rule inside STOP Gate A: if bounded Save Hang remediation requires editing forbidden files (`core/bundle_io.py`, `core/xunity_sync.py`, `core/story_ast.py`), STOP in `/plan` and request explicit scope expansion or spin-off session.

4. **S11b `Q-04` & `Q-18` — Non-Manufactured Failing-First Test Rule (GPT #3):**
   - Separated manual investigation (`Q-04.1.1`, `Q-04.1.2`, `Q-04.1.3 = NOT TESTED`) and STOP-gated `Q-18` from confirmed failing-first probes so Antigravity never manufactures failing tests for non-bugs or deferred renderer work.

5. **S11d `Q-08` — Synopsis Import Available When Existing Box 0 `summary` Is Empty (GPT #4):**
   - Explicitly required the Synopsis import row to be available whenever a valid XUAT Synopsis candidate exists, even if the current document's Box 0 `summary` is empty.

6. **S12 — Pre-S12 Fresh Baseline Run, 2-Gate Separate Approval & Evidence-Backed `FIXED` Rule (GPT #5, GPT #6 & Qwen minor note):**
   - Added mandatory `py -3.12 -m unittest discover -s tests -v` baseline run AFTER S11e and BEFORE modifying any of the 3 hygiene tests, compared against the post-fix discovery run while retaining the historical S11 8-item table.
   - Separated **Gate 1 (`Proceed — S12 Implementation`)** from **Gate 2 (`Separate Explicit Release Promotion Approval` -> `v1.5.0`)**.
   - Locked that marking the 3 hygiene tests as `FIXED` is valid ONLY after observed green post-fix re-run output in S12.
