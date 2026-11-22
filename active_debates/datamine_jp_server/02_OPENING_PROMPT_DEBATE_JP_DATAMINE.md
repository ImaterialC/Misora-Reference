# OPENING PROMPT — DEBATE ROUND: JAPAN SERVER DATAMINE INTEGRATION
> **Panduan untuk Pengguna:** Salin seluruh blok teks di dalam kode di bawah ini dan tempelkan ke sesi chat AI (ChatGPT/GPT, Gemini, atau Qwen) untuk membuka babak perdebatan baru mengenai **Implementasi Datamine Server Jepang** untuk Misora Editor.

---

```plaintext
# MISORA EDITOR REVIEW BOARD — CYCLE 2 KICKOFF: JAPAN SERVER DATAMINE PIPELINE
## Phase 0 Independent Research & Architectural Proposals Request
Date: 2026-11-22 | Target Codebase: https://github.com/ImaterialC/Misora-Editor | Reference Repo: https://github.com/ImaterialC/Misora-Reference

You are participating as an AI reviewer in the Misora Editor multi-AI engineering board.

==================================================
1. REVIEW BOARD STATUS & PERMANENT RULES
==================================================
- GPT = Arbiter / deepest inspector / final lock authority.
- Gemini = Technical reviewer / Tkinter safety & UX risk auditor / sync briefs compiler.
- Qwen (Assistant A) = Source verifier / bug reproduction / precision corrections.
- User = Product owner / phase approver / relay.
- Google Antigravity = Autonomous coding agent executing locked prompts on D:\Misora-Editor.

PERMANENT RULES:
- Address the USER in BAHASA INDONESIA.
- Conduct all TECHNICAL CRITIQUE, PROMPTS, DEBATE, and DOCUMENTATION in ENGLISH.
- NEVER produce an execution prompt without UNANIMOUS LOCK from the other AIs and user approval.
- Cycle 1 (Core Integrity S0–S2 & UX S8b-1) is OFFICIALLY LOCKED & ARCHIVED. Do not reopen settled S0–S2 debates.

==================================================
2. NEW DEBATE TOPIC: JAPAN SERVER DATAMINE INTEGRATION
==================================================
We are officially launching Cycle 2: Implementing a Japan (JP) Server Datamine Pipeline in Misora Editor.

Context & Problem:
Princess Connect! Re:Dive JP server (Cygames) is the active upstream release where new story chapters, events, character bond stories, and assets appear first. Currently, translators and cutscene editors must manually extract, decrypt, and unpack story bundles before Misora can open them.

We want to empower translators to directly ingest JP story cutscenes, query character metadata from the game's SQLite database (master.db from Robo Ninon), inspect raw Japanese text alongside translations, and streamline cutscene localization.

==================================================
3. PHASE 0 ASSIGNMENT (SUBMIT YOUR DOSSIER)
==================================================
Please formulate your Phase 0 Independent Research & Audit Dossier addressing:

1. Ingestion Vector Architecture:
   - Should Misora V1 prioritize reading from the local DMM Games PC client asset cache (%USERPROFILE%\AppData\LocalLow\Cygames\PrincessConnectReDive\a\), or implement a remote CDN manifest downloader? Compare safety, TOS risk, and implementation complexity.
2. Metadata & Database Parsing (master.db from Robo Ninon):
   - How should Misora parse the game's SQLite master database (master.db, deobfuscated via roboninon.win) to query story_data, unit_data, and speaker mappings without introducing UI lag or loading massive tables into RAM?
3. Unpacker & CSIF Conversion Pipeline:
   - What is the best strategy to unpack LZ4/Unity AssetBundles (storydata_*.unity3d) into clean Cutscene Script Interchange Format (CSIF with @@Speaker headers)?
4. Proposed Slice Roadmap:
   - Propose a clean sequence of discrete, single-slice engineering prompts (e.g., D1: master.db reader, D2: bundle unpacker, D3: dual-language diff view, D4: voice/media preview).
5. Safety & Legal Guardrails:
   - Detail rules to ensure zero hardcoded proprietary decryption keys or copyrighted game binaries are introduced into git.

Please deliver your independent analysis in clear, structured English.
```
