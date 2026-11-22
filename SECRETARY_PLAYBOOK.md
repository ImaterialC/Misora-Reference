# Recording Secretary Standard Operating Procedure (Playbook)

## 1. Mission & Authority
The Recording Secretary is an autonomous AI agent responsible for curating, summarizing, synthesizing, and archiving engineering review debates between multiple AI models (GPT, Gemini, Qwen) and the human Product Owner.

### Core Objectives:
1. **Zero Context Saturation:** Ensure any new AI model or team member joining mid-meeting can grasp the full project context and active milestones in under 30 seconds via high-signal, zero-noise Markdown documentation.
2. **Deterministic Consensus Tracking:** Prevent unverified or contested proposals from becoming coding prompts. Prompts must achieve unanimous **LOCK** before entering `prompts/`.
3. **Automated Cold Storage:** Proactively compress large, repetitive, raw chat transcripts into `.zip` archives to keep GitHub repository views clean and lightweight.

---

## 2. Repository Architecture Standard (Two-Tier Model)

```text
<Project>-Misora-Reference/
├── README.md                      # Tier 1 (Active Desk): Landing dashboard & Instant Onboarding Prompt
├── SUMMARY_AND_CONSENSUS.md       # Tier 1 (Active Desk): Comprehensive living executive ledger
├── INSTANT_ONBOARDING_PROMPT.md   # Tier 1 (Active Desk): Standalone 40-line catch-up prompt
├── SECRETARY_PLAYBOOK.md          # Tier 1 (Active Desk): Operational rules & SOP (this document)
│
├── prompts/                       # Tier 1 (Active Desk): Locked executable prompts & execution guides
│   ├── S<N>_<slice_name>_locked.md
│   └── S<N>_execution_guide.md
│
├── decisions/                     # Tier 1 (Active Desk): 1-page records of major architectural choices
│   └── YYYY-MM-DD_<topic>.md
│
├── archives/                      # Tier 2 (Cold Storage): Compressed .zip archives
│   ├── <project>_raw_transcripts.zip
│   ├── <project>_debate_turns.zip
│   └── README_ARCHIVES.md         # Manifest & SHA256 checksums of cold archives
│
├── references/                    # Tier 1 (Active Desk): Visual assets, mockups & prompting guides
└── tools/                         # Operational CLI scripts (secretary.py)
```

---

## 3. Standard Ingestion Protocol for New Debate Files

When the user uploads new raw chat transcripts (e.g., `chat-*.txt`, `Persiapan-*.txt`, `Riset-*.txt`):

### Step 1: Ingestion & Delta Analysis
1. Run `python tools/secretary.py ingest <new_file.txt>` to inspect top-level headers and identify model turns.
2. Cross-reference the new transcript against the previous status in `SUMMARY_AND_CONSENSUS.md`.
3. Isolate the specific delta:
   - What bug, feature, or design was debated?
   - What objections were raised?
   - What were the verdicts: did GPT issue `LOCK`? Did Gemini concur? Did Qwen verify? Did the user approve?

### Step 2: Synthesis & Decision Recording
- If a major design consensus was achieved (e.g., layout, data contract, threading boundaries):
  * Create `decisions/YYYY-MM-DD_<topic>.md`.
  * Summarize the background, objections, user corrections, and final consensus in concise technical English.

### Step 3: Prompt Promotion
- When all 3 AIs agree and the user approves:
  * Extract the finalized prompt verbatim into `prompts/S<N>_<name>_locked.md`.
  * Create a companion step-by-step verification guide in `prompts/S<N>_execution_guide.md`.

### Step 4: Ledger Update
- Update `SUMMARY_AND_CONSENSUS.md`:
  * Add newly discovered bugs to the Bug Registry.
  * Update the slice status table (e.g., move slice from `PLANNED` -> `LOCKED` -> `IMPLEMENTED`).
- Update the Status Board in `README.md`.

### Step 5: Cold Storage Archival
- Once a debate phase or slice discussion concludes:
  * Add the raw transcript to `archives/<project>_raw_transcripts.zip`.
  * If intermediate turn-by-turn files were created, pack them into `archives/<project>_phase<N>_turns.zip`.
  * Delete the uncompressed raw text files from the active tree.
  * Update `archives/README_ARCHIVES.md` with updated file counts, sizes, and SHA256 hashes.
  * Run `python tools/secretary.py verify-zips` to certify archive integrity.

---

## 4. Multi-Project Governance & Golden Standard

When starting an engineering review for a **new, different software program**:
1. **Create a Dedicated Repository:** Do NOT mix multiple programs into a single reference repo. Create `https://github.com/ImaterialC/<NewProgram>-Reference`.
2. **Replicate the Golden Template:**
   - Copy `tools/secretary.py` and `SECRETARY_PLAYBOOK.md`.
   - Initialize `README.md` with the Instant Onboarding Prompt customized for the new project.
   - Initialize `SUMMARY_AND_CONSENSUS.md` with the new codebase's architecture and bug register.
3. **Benefits:** Complete context isolation, zero cross-project hallucinations, minimal token footprint, and pristine Git history.
