# QWEN — INDEPENDENT REVIEW: T-04 IMPLEMENTATION PLAN (REV 1) + HYDROGEN REVISION REQUEST

**Artifacts reviewed (READ-ONLY, GitHub API blobs at pinned SHAs):**
- `ImaterialC/Misora-Reference` @ `d470d411129c…` — `T-04_Implementation_Plan.md` (25,490 B, 471 lines, SHA-256 `172b0e6c…`)
- `ImaterialC/Misora-Editor` @ **`b50c75e7555779cbff0b6821933e11b5f7ef9bf9`** (confirmed live HEAD; matches Hydrogen's rollback pin ✅)

**Boundary:** static line/symbol/arithmetic verification only. I did **not** run Tk, the suite, `git apply`, or discovery on a Windows worktree. The discovery baseline below is established from the committed dashboard + a static test-method chain; the executor must still confirm it live.

---

## 0. T-08a Closure — Verified

Commit chain confirmed: `67459913` (fix `misora.py +78/−3` + new `tests/test_t08a_tooltip_clamping.py`, **exactly 8 test methods**) → `0d831699` (symbol-index regen, index only) → `b50c75e7` (docs closeout, `OPEN_ISSUES.md` + `PROJECT_STATE.md` only). Ledger records **8/8 TDD + M-1..M-6 Windows QA PASS**, lifecycle `HISTORICAL-REFERENCE`, baseline **502**. My prior binding note **E-1 was honored**: the main-window startup off-screen observation is preserved as an OPEN sub-item (`NEEDS-REPRO`), not silently closed. (Your note said M-1..M-5; the committed ledger records M-1..M-6 — the ledger is authoritative.) `misora.py` @ HEAD = **23,987 logical lines**, LF-normalized blob 1,079,059 B → working-tree CRLF 1,103,045 B / 23,986 terminators. ✅

---

## 1. HEADLINE BLOCKER — The Baseline Is 502, Not 504 (Hydrogen's request propagates the error)

The plan Rev 1 asserts baseline **504 (461 PASS)** in §1 preflight, §7.3, and §8 rollback. **This is wrong.** Verified chain:

| Stage | Δ | Total |
|---|---|---|
| S11e | — | 475 |
| T-01 | +11 | 486 |
| T-02 | +8 | 494 |
| T-08a | **+8** (file has exactly 8 methods; regen/docs commits added 0 tests) | **502** |

Committed `PROJECT_STATE.md` @ `b50c75e7` states verbatim: **`502 = 459 PASS + 35 SKIP + 6 FAIL + 2 ERROR`**.

**Hydrogen's items 3, 4, and 6 inherit the plan's wrong 504 and lock it in:**
- Item 3: "`504 + 12 = 516`", "`516 = 473 PASS + …`" → **must be `502 + 12 = 514`**, **`514 = 471 PASS + 35 SKIP + 6 FAIL + 2 ERROR`**.
- Item 4: discovery "`== 504`" → **must be `== 502`**.
- Item 6: rollback "`504` test count" → **must be `502`**.

If Rev 2 locks 504/516/473, the executor's preflight gate `countTestCases() == 504` will **HARD STOP** on the real machine (which reports 502). This alone is a HOLD.

## 2. SECOND BLOCKER — Hydrogen's Item 3 Is Incomplete: P1 Also Passes Pre-Patch

Live `_apply_overflow_highlights` (`misora.py:1117–1131`), verified verbatim:
```python
for ln, info in enumerate(line_metrics, start=1):
    if info["overflow_raw_start"] is not None:      # width-overflow tail FIRST
        widget.tag_add("line_overflow", f"{ln}.{start_char}", f"{ln}.end")
    elif info["line_no"] >= 4:                       # line 4+ full-line
        widget.tag_add("line_overflow", f"{ln}.0", f"{ln}.end")
```
`_compute_line_overflow_metrics` emits an entry for **every** line with `line_no == ln`. Therefore:

- **P1** `test_probe_1_line4_no_width_overflow_full_line_tag` (plan line 302: "4-line text, line 4 **within 54d**") → `overflow_raw_start is None` → `elif line_no >= 4` → full-line tag **already applied pre-patch**. **P1 PASSES pre-patch** despite being labeled "FAIL (Defect A)". It is a regression guard, not a failing probe.
- **P4** `test_probe_4_line3_no_overflow_tag` → passes pre-patch (Hydrogen correctly catches this one).

So the plan's "P1–P4 fail, `failures=4`" is wrong by **two**. Hydrogen item 3 moves P4→G8 and inserts a genuine Defect-A probe as new P4, **but leaves P1 unchanged**. Result: P1(pass) + P2(fail) + P3(fail) + newP4(fail) = **3 failures**, contradicting Hydrogen's own locked `failures=4`.

**Required correction:** Rev 2 must make **all four** probes genuinely fail pre-patch — e.g., redesign P1 to "line 4 **with** width overflow → full-line tag" (true Defect A), move the old P1 "line-4-no-width-overflow" case into a guard, and keep new P4 as a second Defect-A variant (line 5+, or overflow-at-char-0). Then 4 Probes (2 Defect A + 2 Defect B) + 8 Guards = 12, `failures=4`, `0 errors` holds.

## 3. Item-by-Item Adjudication of Hydrogen's 8 Items

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Defect A patch logic | **CORRECT & critical** | Plan §5.1 (lines 165–176) puts `if line_no >= 4:` first with inner `if overflow_raw_start is None:` → line 4+ **with** width overflow gets **no tag** (worse than live tail-only). Drop the inner guard: `if line_no >= 4:` → always `f"{ln}.0"..f"{ln}.end"`. `line_no == ln` verified, so either form is equivalent. |
| 2 | P3 determinism | **CORRECT** | Force `pixel_width = safe_w + 1` so `round(max_px/digit_w) == 54` independent of DPI/font; also assert `>= 55` → `"55/54d"` (no `">55/54d"`). The `total_digits <= max_d` guard in §5.2 supports this. Apply the same mocking to P2. |
| 3 | P4 trap + 12-test arithmetic | **PARTIALLY CORRECT — needs §2 fix above + §1 baseline fix** | P4→G8 right; but P1 also passes pre-patch; and 504/516/473 → **502/514/471**. |
| 4 | Callers / discovery / zero-`.pyc` | **Callers already satisfied; discovery number WRONG** | Plan §2.5 already lists all 3 callers correctly: `misora.py:1558` (`on_key_release`), `:1703` (`flush_pending_updates`), `:5754` (`_refresh_dialogue_metrics`) — verified, exactly 3 call sites. Discovery must be **502**. BOM-safe in-memory `compile()` + `pre_pyc_count == post_pyc_count`, no `compileall`: sound. |
| 5 | Exact diff / line count / EOL / `apply --check` | **CORRECT — and currently absent** | Plan §5 has **no unified diff** (no `@@` hunks), only code snippets + a claimed `+38/−8`, net +30, 23,987→24,017. That numstat is **unverifiable as-is** and **will change** once Defect A is corrected. Rev 2 must emit a hunk-level diff (T-08a precedent), recompute numstat/line-count/CRLF, and pre-validate `git apply --check`. Pre-edit 23,987 / 23,986 CRLF confirmed ✅. |
| 6 | 4-file matrix / pinned rollback / N-4 | **Structure correct; rollback count WRONG** | Matrix + pin `b50c75e7…` (no `HEAD`, no `reset --hard`) + N-4 note already present and correct. Rollback verification count must be **502**, not 504. `PROJECT_STATE.md` ≤ 15,360 B ✅ (currently 5,414 B). |
| 7 | Harness isolation | **ALREADY SATISFIED** | Plan §7.1 already specifies CONFIG_PATH→`tempfile.mkdtemp()`, `misora.messagebox` mocked, `MisoraApp(restore_session=False, show_splash=False)`, zero `.unity3d`, zero `skipTest()`, `tearDown` `app.destroy()` + `shutil.rmtree`. Rev 2 retains it. |
| 8 | M-6 ▼▶ badge fact | **CORRECT — M-6 step 4 is factually wrong** | `▼▶` badges belong to **`ImportFromXUATDialog`** (class @9620; badges @10371/10531/10598/10641). All Script card headers (`_render_script_card` @1322, header @1353–1369) show only `#{box_no} {speaker}` + Lock checkbox — **no ▼▶**. The `▼ Expand All`/`▶ Collapse All` @18433/18437 are toolbar buttons. Correct/remove M-6 step 4. |

## 4. Additional Independent Observation (scope clarity — non-blocking)

The **All Script full-card overflow path is separate and untouched** by this plan: `misora.py:1434–1466` uses a hardcoded `cw > 54` + `east_asian_width` counter and tail-only `tag_add` (@1464), with **no line-4+ full-line logic**. T-04's `_apply_overflow_highlights` fix affects only the Dialogue `txt_dialogue`. Rev 2 should **explicitly state All Script card overflow rendering is OUT OF SCOPE** (and M-6 must not imply T-04 changes it). If All Script line-4+ highlighting is desired, that is a separate task. This reinforces item 8.

## 5. Blockers Summary

1. **B-1 (baseline):** 504/461/516/473 → **502/459/514/471** everywhere (plan §1/§7.3/§8; Hydrogen items 3/4/6).
2. **B-2 (failing-first):** P1 passes pre-patch; Hydrogen item 3 must also redesign P1 so exactly 4 probes fail pre-patch (`failures=4`, `0 errors`).
3. **B-3 (exact diff):** produce a real hunk-level unified diff and recompute numstat/line-count after the Defect A correction; pre-validate `git apply --check`.
4. **B-4 (M-6 fact):** correct the All Script ▼▶ claim (item 8).

Non-blocking: scope-clarity note (§4); item 7 already satisfied; item 4 caller list already present.

---

## 6. RULING

The T-04 plan Rev 1 is **not** ready, and Hydrogen's revision request — while sound in direction and correct on items 1, 2, 5, 8 — **carries two errors of its own** (the 504 baseline and the incomplete P4-only fix) that would still produce a broken Rev 2 if executed verbatim. The planner should address Hydrogen's 8 items **as corrected by B-1…B-4 above**, then re-submit for final clearance.

**`HOLD`** — T-04 Rev 1 not cleared; Rev 2 required with the mandatory corrections.

Read-only compliance: no files in either repository were created, modified, or deleted by me; no commands were run against `D:\Misora-Editor` or `D:\Reference`. Authority unchanged — only Project Lead (Cornelia) grants `Proceed`/commit/push; version stays `1.4.15`.

`STOP — WAITING FOR FINAL CLEARANCE`