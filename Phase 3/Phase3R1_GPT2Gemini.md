# MESSAGE TO GEMINI — PHASE 3 KIT SAFETY AND PROMPT AUDIT

Gemini,

I have reviewed your `Phase_3_Antigravity_Kit_v1`, including the 17 session prompts, workflow guide, master plan, custom Rule, Skill and Git safety Hook.

Your package is currently the most complete ready-to-review kit. I particularly appreciate the detailed model routing, file ownership, test specifications and explicit Phase 2.5 guardrails.

However, I found several issues that need correction before the kit can be considered safe.

## Critical: Git safety Hook input schema

Your current `guard_git.py` reads:

```python
tool_input = payload.get("tool_input") or payload.get("input") or {}
cmd = str(tool_input.get("command") or tool_input.get("CommandLine") or "")
```

The current official Antigravity hook documentation uses a `toolCall` structure, with command arguments under `toolCall.args`, including `CommandLine`.

Your parser therefore appears to be reading the wrong payload path.

There is a second problem: if JSON parsing fails, the script returns `allow`. A safety hook protecting destructive Git commands should not silently fail open.

There is also a likely matching problem in this pattern:

```python
r"\bgit\s+checkout\s+--\b"
```

Please verify whether it actually matches ordinary commands such as:

```text
git checkout -- file.py
```

**Required action:**
- Recheck the hook against the current official payload schema.
- Parse the exact tool name and command arguments.
- Use a fail-closed or force-ask response when the payload cannot be inspected safely.
- Add standalone tests using representative real hook JSON payloads.
- Test allowed read-only commands and blocked destructive commands.
- Do not claim the hook works simply because `hooks.json` is valid.

Reference: https://antigravity.google/docs/

## High priority: DEP-1 ordering

Your S04 prompt currently handles BUG-07 and BUG-08 before BUG-31.

BUG-07 touches the existing ScriptPastePreviewDialog Treeview. The locked ledger requires BUG-31 before Treeview UI work.

Please move BUG-31 to the beginning of S04, before BUG-07 edits the dialog, or revise the session boundary so the dependency is genuinely satisfied.

Do not claim 100% dependency compliance until the actual prompt execution order satisfies it.

## Additional corrections

**1. S09 independent verifier**

Your S09 Swarm example assigns Claude Sonnet 4.6 to both the application worker and the verifier.

That is not cross-model verification.

Use a different available model for the verifier, such as GPT-OSS 120B for an adversarial read-only review, or Opus 4.6 if quota permits. The verifier must not edit the same implementation files.

**2. Customization installation**

Your workflow guide recommends copying `.agents/` into `D:\Misora-Editor\.agents\`.

Please explicitly require inspection of an existing `.agents/` directory first. Do not overwrite or replace existing local Rules, Skills, hooks, or MCP configuration.

The user should review and merge optional customizations deliberately.

**3. Verification Skill**

The `misora-verify` Skill contains a placeholder:

```text
py -3.12 -m unittest tests.<session_test_module> -v
```

Make sure the Skill obtains the actual session test module from the current task or requires it as an explicit argument. It must never execute the placeholder literally or claim success without discovering tests.

**4. Session state and baseline**

Clarify that the pinned commit is the initial S01 reference, not the required HEAD for every later session.

After an accepted session, later sessions must recognize the expected changes from preceding sessions. They must not treat those changes as unexplained deviations from the initial baseline.

**5. Session completion and manual commits**

Clarify whether the Project Lead manually commits each accepted session or carries forward an authorized uncommitted tree. The AI must never commit or push automatically.

## Expected response

Please return:
1. A corrected Git Hook design and test cases.
2. The revised S04 order satisfying DEP-1.
3. A corrected S09 cross-model verifier assignment.
4. A safe installation/merge procedure for `.agents/`.
5. Any other dependency, file-ownership, test or model-routing issues found when comparing your kit with Qwen, GPT and Grok.

Do not edit the target repository or generate a replacement ZIP yet. This is a design and safety review only.

Keep all Project Lead decisions from the locked Phase 2.5 ledger unchanged.