# Workflow Rules

## Official phase structure

The process has five main phases. Phase 2.5 is a mandatory sub-gate within Phase 2.

| Phase | Name | Output | Must stop? |
|---|---|---|---|
| 0 | Access and integrity | Per-AI access report | Yes, await owner approval |
| 1 | Independent research | Independent technical report per AI | Yes, await owner |
| 2 | Cross-review | Canonical findings ledger and council messages | At Phase 2.5 gate |
| 2.5 | Exhaustive reconciliation | Completeness verdict | Yes, unless every active AI and owner accept |
| 3 | Implementation planning | Agreed sequence and bounded Antigravity prompts | Yes, await owner approval |
| 4 | Execution feedback | Verification of each Antigravity slice | Yes, await owner decision |

Phase 2.5 is called a sub-phase for tracking, but it is mandatory. It must not be skipped or silently merged into a casual summary.

## Owner-controlled gates

- The owner chooses the participating AIs and defines the active-AI set for each session.
- The owner confirms when Phase 0 is complete.
- The owner decides when Phase 1 reports are collected and Phase 2 begins.
- The owner provides other AI reports and private findings to start Phase 2.
- The owner confirms Phase 2.5 completeness.
- The owner approves the Phase 3 plan before execution.
- The owner sends approved prompts to Antigravity and returns the results in Phase 4.

An AI cannot declare the workflow advanced merely because it has completed its own output.

## Independence and information release

- Phase 0 is about access; no technical diagnosis.
- Phase 1 is performed independently. Other AI reports and owner private/manual findings must not be provided or used.
- Phase 2 is the first point at which the owner releases cross-model reports and owner findings.
- Phase 2.5 compares a fresh inventory from each active AI against the canonical ledger.
- Phase 3 uses the reconciled ledger only.
- Phase 4 evaluates actual implementation feedback against the approved plan.

## Language policy

- Conversation and explanations to the owner: Bahasa Indonesia.
- Technical reports and bug/feature finding blocks: English.
- Reusable AI-to-AI council messages: English.
- Antigravity prompts and test instructions: English.
- Repository documentation may be English for consistent cross-model use.

## Manual relay model

The AI services do not need to be connected to each other. The owner is the relay:
1. Copy the same phase prompt to each active AI.
2. Collect each AI's output.
3. Provide the required reports to each AI at Phase 2 onward.
4. Keep the same source snapshot and finding IDs across conversations.
5. Do not omit a dissenting report merely because it disagrees with the majority.

## Consensus and disagreement

- Consensus is not a vote on truth. Evidence determines technical confidence.
- Repeated unsupported statements do not become facts.
- Every active AI must explicitly review the Phase 2.5 inventory before the owner closes that gate.
- Remaining disagreements may be retained as DISPUTED or UNKNOWN when their treatment is explicit and accepted by the owner.
- Never claim unanimity if any active AI has not responded.
- Do not force every finding to become CONFIRMED.

## No premature implementation

No AI should write or modify application code during Phases 0–3. Phase 3 may create implementation prompts, but not execute them. Phase 4 begins when the owner runs an approved prompt in Antigravity.

## Scope change

If new evidence changes severity, dependencies, architecture, or feature scope:
- Record the new evidence and affected finding IDs.
- Explain why the existing decision is no longer valid.
- Ask the owner whether to reopen Phase 2 or Phase 3.
- Do not quietly expand scope.
