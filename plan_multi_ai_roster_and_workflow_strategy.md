# Multi-AI Roster and Model Evaluation Strategy

**Research snapshot:** 2026-11-23  
**Purpose:** Assign useful work to available tools without pretending that model personalities or rankings are permanent.

## Executive recommendation

Keep a small active council and a reserve list. Choose roles based on measured performance on Misora tasks, not a universal model ranking. Record the exact model label, product surface, plan, date, file/tool access, and observed result. Treat model capabilities and free-tier limits as time-sensitive.

## 1. Provisional roster for the current workflow

The roles below are starting hypotheses. `USER-OBSERVATION` means the owner has seen this behavior; it is not an independent benchmark result.

| Participant | Provisional role | Current reason to keep/use | Caveat / validation required |
|---|---|---|---|
| ChatGPT Free | Independent critic and research reviewer | Owner reports strong late-stage critical reviews. OpenAI's current Free FAQ lists web search, file uploads, data analysis, GPT-5.6 Luna, and Think on mobile with web rollout underway. | Use scarce deeper-thinking opportunities for high-risk decisions. Confirm Think/model availability in the account UI. Do not retain old `o1`/`o3-mini`/`GPT-4o` labels as the current roster. |
| Qwen4-Max | First-pass research and code reviewer | Owner reports high diligence. Alibaba announced Qwen4-Max on 2026-11-16 for coding, reasoning, vision, and long-running tasks. | New model; test it on the actual Misora code and fixtures. Vendor benchmarks are not a direct comparison with the user's other web models. A published context window is not proof of the web UI's actual upload or context limit. |
| Gemini / Antigravity | Technical reviewer and document compiler; local Orchestrator when available | Owner reports good synthesis/documentation. Antigravity provides model selection, Orchestrator, and agent workflows. | Separate model quality from the tools and context the Antigravity surface provides. Do not assume Gemini 4 Carbon is included in Google AI Pro: the current Antigravity table lists Carbon for Ultra/Enterprise, while Neon and Argon have Pro eligibility subject to plan/trial conditions. |
| Claude Free | New independent architecture reviewer to test | Claude is worth testing for architecture and code review. Anthropic announced Sonnet 5.5 on 2026-09-28; its positioning is a vendor description, not a Misora result. | Confirm which model and features the free web account actually exposes. Standard Claude file upload docs list PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX, and images; ZIP is not listed. Claude Code/local shell is a different product surface. |
| DeepSeek Free | Specialist for isolated pasted snippets | May be useful for a second opinion on a specific algorithm or decoding function. | The quoted self-description is not enough to judge all DeepSeek products. DeepSeek API docs now list file/document input and search/fetch tools, but API capability does not prove those tools are present in the free web chat. Keep it out of repository-wide audits unless tested. |
| Kimi | Reserve / optional long-context reviewer | Owner has observed useful enough potential to try it in a meeting. | Mid-generation interruptions are a reliability failure for the meeting workflow. Do not use it as a required gate until it completes the same short test set consistently. |
| Grok | Parked | Owner encountered a hallucination and lost confidence. | Respect the decision not to use it. Do not generalize a single failure into a universal coding-quality verdict. Re-test only if it offers a clear benefit. |
| Meta AI | Parked | Not currently needed in the council. | Do not generalize limitations of one Meta AI interface to every Llama model or hosting surface. |
| GitHub Copilot Free | Secondary local coding assistant for bounded tasks | Current Free plan includes limited chat and agent use; GitHub documents agent mode for IDEs and the Copilot app/CLI. The Misora-Editor repository already has `AGENTS.md` and `docs/COPILOT_WORKFLOW.md`. | Free plan is limited and model selection is auto-only in the current plan table. Do not switch the primary workflow before a controlled trial. |
| Antigravity Pro | Primary local implementation agent | It works against the local checkout and can run the project's own commands/tests; the current account is already paid for. | Always inspect the generated plan/diff, approve commands deliberately, and verify test output. An agent's report is not a test result. |

## 2. Current product facts that should replace stale claims

### Antigravity model availability (snapshot 2026-11-23)

The official Antigravity model page currently lists Gemini 3.8 Flash, Gemini 4 Neon/Carbon/Argon/Hydrogen, Orchestrator, Claude Sonnet 5.5/Opus 5.5, and Claude Sonnet 4.6/Opus 4.6, subject to plan and eligibility conditions.

Important distinctions shown by the current page:

- Gemini 3.8 Flash is listed across Free, Pro, and Ultra.
- Gemini 4 Neon is listed for Google AI Pro under stated eligibility conditions and Ultra; Carbon is listed for Ultra and Enterprise, not Pro.
- Claude Sonnet 5.5 and Opus 5.5 are listed for paid Google AI Pro subscriptions (not trial) and Ultra/Enterprise.
- Claude Sonnet 4.6 and Opus 4.6 are listed for Free and Pro, with a scheduled removal date of 2026-11-30 on the page at the time of research.
- Orchestrator pairs a planner and executor. On Google AI Pro/Ultra, the current documentation describes planner choices and executor choices in Settings > Models > Orchestrator Settings. Check the live account selector before assuming a model is available.

Official source (accessed 2026-11-23): https://antigravity.google/docs/models

### GitHub Copilot Free (snapshot 2026-11-23)

GitHub's current plans page describes Free as having limited chat and agent usage and automatic model selection. The pricing page lists 2,000 monthly completions and entry-level model access. The plan is useful for bounded IDE/CLI agent tasks, but not a like-for-like replacement for a paid Antigravity plan with the model options and quota the owner currently uses.

Official sources:

- https://docs.github.com/en/copilot/get-started/plans
- https://github.com/features/copilot/plans
- https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/use-copilot-agents/use-agent-mode

### ChatGPT Free (snapshot 2026-11-23)

OpenAI's current Free FAQ lists GPT-5.6 Luna, web search, file uploads, data analysis, and Think on mobile with web rollout underway. It explicitly says the default model and available limits can change. Do not hardcode a universal query quota into this repository.

Official source: https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq

### Qwen4-Max (snapshot 2026-11-23)

Alibaba announced Qwen4-Max on 2026-11-16 and lists it for coding, reasoning, vision, and long-running work. The release announcement includes company-reported benchmark claims. Treat those as vendor-reported metrics, not a head-to-head Misora benchmark.

Official sources:

- https://www.alibabagroup.com/en-US/document-2060139246777270272
- https://docs.qwencloud.com/developer-guides/getting-started/latest-model

### Claude file handling (snapshot 2026-11-23)

Anthropic's file-upload help page (updated 2026-07-23) lists supported document and image types and states current chat upload limits of 500 MB per file and 20 files per chat. ZIP is not in the listed document formats. Do not state that Claude Web can unzip an uploaded ZIP unless that exact product surface has been tested. A local Claude Code shell is a different workflow.

Official source: https://support.claude.com/en/articles/8241126-upload-files-to-claude

### DeepSeek product-surface distinction

DeepSeek API documentation lists file upload/document parsing and search/fetch tools. Those are API capabilities and may require API access/billing; they do not establish that a particular free web chat session has the same tools.

Official source: https://api-docs.deepseek.com/api/create-file/

## 3. Misora-specific model bake-off

Run this small test set when adding or reconsidering a model. Give each model the same brief and the same repository snapshot. Do not share other models' answers until independent reviews are complete.

| Test | Input | What to measure |
|---|---|---|
| A. Repository navigation | Public repo links plus a request to inspect a named module and its tests | Correct paths, accurate summary, honest list of files actually inspected |
| B. Bug diagnosis | One known issue with a minimal reproduction or failing test | Root-cause accuracy, evidence, false positives, missing edge cases |
| C. Regression design | One confirmed bug and relevant source | Test quality, preservation of existing behavior, test actually fails before the fix |
| D. Architecture review | A bounded proposed change and relevant interfaces | Correct dependency boundaries, risks, simpler alternative, explicit unknowns |
| E. Output reliability | A multi-part report with a fixed response structure | Completes without truncation, follows structure, does not invent results |
| F. Coding agent only | One small isolated change on a disposable branch/worktree | Diff quality, tests, scope discipline, commands/permissions, recoverability |

Use a 1–5 score for each dimension: source/evidence accuracy, technical correctness, regression awareness, task completion, tool/file access, reliability, and time/usage cost. Add a short evidence note for every score. Do not collapse the results into one permanent “best model” label.

Record the exact date, model label, account tier, product surface, tools enabled, input files, repository SHA, result, interruptions, and actual test outcome. Retest after a material model or product update.

## 4. Recommended role assignment today

1. **Primary analyst:** Qwen4-Max or Gemini, selected by the task's actual file/tool access and the last Misora-specific test result.
2. **Independent reviewer:** ChatGPT Thinking for high-impact decisions, or Claude after its first bake-off. Keep the review independent before showing the first analyst's conclusion.
3. **Scribe:** Gemini when its documentation/synthesis result passes source checks. The scribe organizes findings; it does not decide facts.
4. **Specialist:** DeepSeek for a pasted, isolated function only, until its free web interface proves more capability.
5. **Implementer:** Antigravity Orchestrator/agent on the local checkout.
6. **Secondary implementer/reviewer:** Copilot Free for small, bounded tasks; do not give two coding agents simultaneous ownership of the same files.
7. **Owner/decision-maker:** The human user. AI unanimity is not required and cannot replace approval.

## 5. Operating rule

The roster is a living record, not a ranking. Keep an AI in the active council when it produces evidence-backed value on the same test set. Park it when access or reliability makes it unsuitable. Revisit the decision when the provider or model changes.
