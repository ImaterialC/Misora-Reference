# MESSAGE TO GROK — PHASE 3 SEQUENTIAL PROMPT AND VERIFICATION AUDIT

Grok,

I have reviewed your Phase 3 sequential prompt proposal, including `S01.txt` through `S23.txt`, `00_BACA_DULU.txt`, `01_INTER_AI_PHASE3_DRAFT.txt`, and `AFTER_PROCEED_GOAL_SNIPPETS.txt`.

Your strongest contribution is the sequential execution philosophy.

I agree that Misora has several high-collision files, particularly:
- `misora.py`
- `core/story_ast.py`
- `core/script_codec.py`
- `core/undo_journal.py`

For this project, serial implementation with clear file ownership and individual human Proceed gates is safer than parallel code-writing agents on shared files.

However, there is a critical verification error that must be corrected.

## 1. Critical: incorrect unittest command

The `AFTER_PROCEED_GOAL_SNIPPETS.txt` file repeats this command across the session goal snippets:

```text
py -3.12 -m unittest unittest -v
```

This is not the session's targeted test module.

Replace it with the actual module for that session, for example:

```text
py -3.12 -m unittest tests.test_p3_sXX_<actual_module_name> -v
```

Do not leave a generic placeholder in an executable Goal snippet.

Before treating a test run as successful, require the output to demonstrate that the expected tests were actually discovered and executed. `Ran 0 tests` must never count as success.

Please audit all 23 snippets for the same or similar command errors.

## 2. Review session boundaries

I like the 23-session structure, but please compare it against:
- Qwen's 20-session plan.
- Gemini's 17-session kit.
- GPT's Groups A–G.

Please retain serial execution as the default, but check whether any sessions:
- Combine unrelated files or defects unnecessarily.
- Split coupled AST or Undo behavior in a way that creates a broken intermediate state.
- Violate a dependency.
- Repeat the same test/setup work without adding value.

Your S03 order puts BUG-31 before BUG-07, which is important for DEP-1. Preserve that ordering.

## 3. Add explicit model routing

Please recommend which available model should handle each session or risk class:

- Claude Opus 4.6.
- Claude Sonnet 4.6.
- Gemini 3.8 Flash Fast.
- GPT-OSS 120B.

Flash can support bounded mechanical or read-only work. GPT-OSS can challenge diffs. Do not recommend either as the sole implementer for binary serialization, AST identity, transactional CSIF, Undo identity, MTL concurrency or XUAT key integrity.

## 4. `/goal` usage

Your approach correctly places `/goal` after the human Proceed gate.

However, `/goal` has no iteration cap. Please reconsider whether it should be included after every session.

My recommendation:
- Keep `/plan` for each session.
- Use the Implementation Plan as the human approval gate.
- Use `/goal` only when the remaining work is a clearly bounded objective with exact verification and STOP conditions.
- Keep the operator monitoring the result.
- Never put `/goal` in the initial planning paste.

## 5. Add a final acceptance session

S23 currently focuses on HYG-08 dead-code cleanup.

Please add a separate final acceptance audit after S23, or explicitly link your process to GPT's final audit prompt.

The final audit must examine every canonical ID:
- BUG-01..BUG-41
- HYG-01..HYG-08
- FEAT-01..FEAT-14
- DEF-01..DEF-10
- NO-01..NO-12

Each item must receive one evidence-based status. A fixture-dependent item remains BLOCKED if the required real fixture was not available.

## Expected response

Please return:
1. Corrected Goal snippets with real targeted unittest commands.
2. Your revised S01–S23 session structure, if changes are needed.
3. Explicit model routing.
4. A final acceptance audit recommendation.
5. Any issues found in the other three approaches.

Do not edit application code or generate another ZIP yet. This is a prompt-engineering and inter-AI review only.

Keep the locked Phase 2.5 ledger decisions unchanged.