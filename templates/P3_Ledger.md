PHASE 3 — CANONICAL LEDGER LOCK

Baseline: `[40_CHAR_SHA]`
Role: Compiler=`[AI_NAME]` | Auditors=`[AI_NAMES]`
Inputs: `[PHASE_2_URLS]`

Compiler: output ONE zero-omission `Canonical_Ledger_LOCKED.md` containing:
1. Locked Lead Rulings & Hard Invariants.
2. Dependency Graph (`DEP-1..N`).
3. Tables: `BUG-01..N` (Sev, Aliases, Symbol, Fix+Test), `FEAT-01..N` (`U-xx`, Spec+Guardrails), `HYG-01..N`.
4. Lists: `DEF-01..N` (deferred), `NO-01..N` (rejected/retracted).
5. 100% Traceability Map: every `U-xx` and Phase 1/2 peer ID -> canonical ID (0 omitted).

Auditors: verify 100% ID coverage, zero contradictions with live code, zero dropped guardrails. Reply ONLY:
- `LEDGER: OPEN — MUST-FIX:` (numbered surgical diffs), OR
- `LEDGER: LOCKED & IDENTICAL`
