# Misora Reference — Priconne JP Research and Extractor Prototypes

This repository is the research and reference workspace for [Misora Editor](https://github.com/ImaterialC/Misora-Editor). It contains source references, historical toolchains, exploratory prototypes, tests, and AI-assisted engineering records. It is **not** the production application repository.

## Start here

| File | Purpose |
|---|---|
| [INSTANT_ONBOARDING_PROMPT.md](INSTANT_ONBOARDING_PROMPT.md) | Compact handoff for a new reviewer joining mid-task |
| [SECRETARY_PLAYBOOK.md](SECRETARY_PLAYBOOK.md) | Evidence, debate, decision, and archive procedure |
| [plan_multi_ai_workflow_and_db_strategy.md](plan_multi_ai_workflow_and_db_strategy.md) | Multi-AI workflow, Antigravity feature selection, and database policy |
| [plan_multi_ai_roster_and_workflow_strategy.md](plan_multi_ai_roster_and_workflow_strategy.md) | Provisional roster and a repeatable model evaluation method |
| [AGENTS.md](AGENTS.md) | Operating rules for AI agents in this repository |
| [INSTALL_REPAIR_PACK_PROMPT.md](INSTALL_REPAIR_PACK_PROMPT.md) | Safe Antigravity instructions for applying this repair pack |
| [templates/](templates/) | Reusable brief, review, decision, and implementation templates |

## Related application

**Misora Editor:** https://github.com/ImaterialC/Misora-Editor

For editor implementation work, the application's current checkout is authoritative. Read its `AGENTS.md`, `PROJECT_STATE.md`, relevant source files, and tests. `Misora-Reference` does not replace that source of truth.

## Repository map

```text
Misora-Reference/
├── README.md
├── AGENTS.md
├── .gitignore
├── INSTANT_ONBOARDING_PROMPT.md
├── SECRETARY_PLAYBOOK.md
├── plan_multi_ai_workflow_and_db_strategy.md
├── plan_multi_ai_roster_and_workflow_strategy.md
├── active_debates/
│   └── extractor_plugin/
│       └── 01_KICKOFF_BRIEFING_EXTRACTOR_PLUGIN.md
├── archives/                         # Historical debate and reference archives
├── extractor_prototype/              # Experimental headless extraction code
│   ├── local_scanner.py              # Local DMM cache discovery
│   ├── story_codec.py                # ADV bytecode parsing / CSIF generation
│   ├── db_metadata.py                # Optional read-only SQLite metadata lookup
│   └── service.py                    # Prototype service facade
├── reference_toolchains/             # Historical/community reference code
│   ├── community_heritage/
│   ├── v2_modular_tools/
│   ├── v3_kyouka_suite/
│   └── archives/
├── references/                       # Visual assets and prompting/reference guides
├── templates/                        # New reusable workflow templates
├── tests/                             # Prototype tests
└── tools/
    └── secretary.py                  # Small local records/archive helper
```

This tree is a navigation summary, not a promise that every path exists in every branch or checkout. Verify the current Git tree before relying on it.

## Prototype status

`extractor_prototype/` is a reference prototype. It contains a local cache scanner, an ADV/story codec, and a SQLite metadata resolver. Do **not** describe it as integrated into Misora Editor unless the current editor source demonstrates that integration. Do not repeat historical benchmark or test-pass claims without running the relevant commands on the current checkout.

Suggested local test command:

```bash
python -m unittest tests.test_extractor_prototype -v
```

Record the actual Python version, environment, test count, failures, errors, and skips. A command listed here is not evidence that it has passed.

## `master.db` note

`master.db` is an optional local dependency for `extractor_prototype/db_metadata.py`. In the inspected `main` tree on 2026-11-23, no `.db` or `.sqlite` database file was tracked. The resolver searches a small set of local paths, opens SQLite in read-only mode, and has static fallback values. The code does not implement automatic upstream download or synchronization.

Keep the real database outside Git and outside this repository's archives. Do not assume a download URL, file size, update schedule, or redistribution permission without current evidence. The root `.gitignore` excludes local database files, Python caches, temporary files, logs, and Unity binary payloads. A `.gitignore` does not untrack files that are already committed.

## Secretary CLI

Run from the repository root:

```bash
python tools/secretary.py status
python tools/secretary.py verify-zips
python tools/secretary.py ingest path/to/transcript.md
```

These are the commands currently implemented by `tools/secretary.py`. The script reports basic repository status, checks ZIP integrity, and inspects transcript headers/possible `LOCK` keywords. It does not automatically synthesize debates, append opinions, make decisions, or generate prompts.

## AI collaboration principles

- Obtain independent first-pass reviews before sharing conclusions between reviewers.
- Require evidence for important technical claims; label uncertainty explicitly.
- Preserve disagreement. AI unanimity is not a correctness test.
- Let the human project owner approve decisions and implementation prompts.
- Use one bounded implementation brief with allowed files, acceptance criteria, test commands, data-preservation rules, and stop conditions.
- Record actual command output; never copy old test counts into a new verification report.

See [SECRETARY_PLAYBOOK.md](SECRETARY_PLAYBOOK.md) for the operating procedure.

## Current task status

The active task is defined by its current brief and decision records under `active_debates/`, not by a fixed phase label in this README. Inspect the most recent brief, repository SHA, and actual code before starting work.
