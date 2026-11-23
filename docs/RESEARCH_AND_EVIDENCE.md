# Research and Evidence Standard

## Evidence hierarchy

Prefer evidence in this order, while recording context:
1. Reproducible behavior in the current application or reference tool.
2. Current source code and tests in the relevant repository.
3. Runtime logs, stack traces, structured dumps, and test outputs.
4. Current official documentation for the exact library, format, or platform version.
5. Maintainer documentation, release notes, and upstream source.
6. Carefully qualified community references or reverse-engineering notes.
7. Inference or hypothesis, clearly labeled as such.

A source file existing does not prove that its code path is used by the application. A comment does not prove runtime behavior. A test passing does not prove cases the test does not cover.

## Every technical claim must be traceable

Where possible, record:
- Repository and branch/commit SHA.
- Exact file path.
- Class, function, method, or data structure.
- Line range or small relevant excerpt.
- Reproduction steps and input conditions.
- Expected and actual result.
- Test command and raw result.
- Platform/runtime/library version.
- Confidence and remaining unknowns.

If exact line numbers are unavailable, use the exact symbol name and file path, and say why line-level evidence is unavailable.

## Finding categories

- `BUG` — implemented behavior is incorrect.
- `REGRESSION` — previously working behavior is now broken.
- `MISSING_CORE_FEATURE` — required core capability is not implemented.
- `FEATURE_PROPOSAL` — new capability or enhancement requested.
- `RISK` — credible technical, data, security, compatibility, or maintenance risk.
- `CONSTRAINT` — proven limitation or external requirement.
- `OPEN_QUESTION` — not enough evidence to determine the answer.

## Confidence

- `HIGH` — directly observed or reproducibly verified with strong primary evidence.
- `MEDIUM` — supported by code or documentation but not fully reproduced.
- `LOW` — plausible interpretation or incomplete evidence.
- `UNVERIFIED` — not yet supported enough to assess.

Do not use confidence as a substitute for status. A user-reported issue can be important while still not reproduced.

## Bug report shape

Every bug block should contain:
- ID and concise title.
- Category, severity, status, confidence.
- Affected repository and exact source location.
- Preconditions and reproduction steps.
- Expected result.
- Actual result.
- Evidence.
- User impact.
- Suspected cause (clearly separated from proven facts).
- Proposed fix direction (optional and non-binding in Phases 1–2).
- Regression tests needed.
- Unresolved questions.

## Feature report shape

Every feature block should contain:
- ID and title.
- User problem and intended outcome.
- Scope and explicit non-goals.
- Current behavior and evidence that the capability is missing or inadequate.
- Dependencies and affected application layers.
- Data format/API assumptions, all clearly labeled.
- Acceptance criteria.
- Risks and open questions.

## Prohibited practices

- Inventing file names, functions, line numbers, test runs, or application behavior.
- Treating a guess as a confirmed bug.
- Treating a feature preference as an engineering constraint.
- Using another AI's claim as the only evidence.
- Claiming that a binary/archive/image was inspected when only its filename was visible.
- Claiming that a feature is absent without checking the current implementation and relevant history where available.
