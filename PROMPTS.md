# Copy-paste prompts for participating AIs

Use the same prompt for every participating AI. Replace no URLs unless the repository location changes. The detailed rules live in this repository; the prompt below only selects the phase.

**Canonical repository:** https://github.com/ImaterialC/Misora-Reference  
**Main application:** https://github.com/ImaterialC/Misora-Editor

## Phase 0 — access and integrity

```text
Read and follow the complete instructions in https://github.com/ImaterialC/Misora-Reference/blob/main/Phase0.md and the project rules it links to. Inspect the actual current Misora-Reference repository and verify which files you can genuinely open, read, and inspect. Perform Phase 0 only. Return the required access/integrity report in the specified format, communicate with me in Bahasa Indonesia, and STOP for my approval. Do not begin technical research.
```

## Phase 1 — independent research

```text
Read and follow https://github.com/ImaterialC/Misora-Reference/blob/main/Phase1.md and all required linked rules. Perform an independent technical review using primary evidence. Do not read or rely on reports from other AIs or my private findings. Return your complete technical report in English, explain it to me in Bahasa Indonesia, ask only essential blocking questions, and STOP. Do not cross-review or plan implementation yet.
```

## Phase 2 — cross-review

```text
Read and follow https://github.com/ImaterialC/Misora-Reference/blob/main/Phase2.md. I will provide the Phase 1 reports from the participating AIs and my own findings. Compare them against the actual evidence, identify duplicates and disagreements, maintain traceable finding IDs, and produce your own complete English council message for the other AIs. Do not force agreement or mark an unsupported claim as confirmed. Stop when the review packet is ready for the Phase 2.5 completeness gate.
```

## Phase 2.5 — exhaustive reconciliation gate

```text
Read and follow https://github.com/ImaterialC/Misora-Reference/blob/main/Phase2.5.md. Independently enumerate every bug, regression, missing core feature, proposed feature, owner-reported issue, risk, constraint, and unresolved question in the agreed review scope. Compare your inventory with the canonical ledger and the other AIs' inventories that I provide. Identify omissions, duplicates, unsupported claims, and hallucinations. Confirm explicitly whether the ledger is exhaustive. Do not begin implementation planning until this gate is passed.
```

## Phase 3 — implementation planning

```text
Read and follow https://github.com/ImaterialC/Misora-Reference/blob/main/Phase3.md. Use only the reconciled Phase 2/2.5 ledger. Agree on dependency-aware implementation order, bounded Antigravity execution sessions, acceptance criteria, tests, rollback points, and stop conditions. Produce implementation prompts in English. Do not edit code or claim to have implemented anything. Wait for my approval.
```

## Phase 4 — Antigravity execution feedback

```text
Read and follow https://github.com/ImaterialC/Misora-Reference/blob/main/Phase4.md. I will provide Antigravity's implementation report, changed-file list, diffs, and test results. Review only the execution feedback and the approved Phase 3 task. Do not restart the multi-AI debate or expand scope without evidence. Tell me in Bahasa Indonesia what passed, failed, remains unverified, and what exact follow-up prompt or manual check is needed.
```

## Operating note

- Phase 0 is a real access gate, not a project-research phase.
- Phase 1 reports must remain independent until the owner opens Phase 2.
- Phase 2.5 is mandatory and is a sub-gate of the Phase 2 review.
- Only the owner can authorize the next phase.
