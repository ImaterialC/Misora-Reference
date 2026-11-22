# Cold Storage Archives Manifest

This directory contains compressed .zip archives of raw chat exports, repetitive turn-by-turn debate transcripts, and historical drafts.

> **Why are these archived in .zip format?**
> To prevent AI context window saturation and repository bloat. When an AI or human developer browses this repository, they should only ingest the clean, high-signal active documentation (README.md, SUMMARY_AND_CONSENSUS.md, decisions/, prompts/). These archives preserve complete historical data for forensic auditing without cluttering the active workspace.

## Archive Inventory

### misora_raw_transcripts_final.zip
- **Description:** Full historical raw chat transcripts from all 3 AI reviewers (GPT, Gemini, Qwen) and quarantined HTML mockups.
- **File Size:** 616.0 KB (630,760 bytes)
- **SHA256:** 7b40e26c6e210c716242849c6811af303c4dadc7dc1baaf0ee457c129d599f1b
- **Files Contained (6):**
  * Persiapan_Analisis_Program_Gemini_Final.txt
  * Riset_Bug_Misora_GPT_Phase0_1.txt
  * Riset_Bug_Misora_GPT_Phase1b_2.txt
  * chat_Misora_Editor_Handoff_Qwen_Final.txt
  * deprecated_hallucinations/202622110312Qwen_html_20261122_seb6a19hg.html
  * deprecated_hallucinations/202622110315Qwen_html_20261122_qmplgmx8s.html

### misora_phase1_debate_turns.zip
- **Description:** 28 turn-by-turn research dossiers, cross-checks, and convergence files from 2026-11-21 Phase 1 debate.
- **File Size:** 147.2 KB (150,691 bytes)
- **SHA256:** a031076875c1ca5dc988b22c01cd16ab13d90a6a2b4faee486c589f587058580
- **Files Contained (28):**
  * round1_phase0_dossiers/gemini_phase0_dossier.txt
  * round1_phase0_dossiers/gpt_phase0_dossier.txt
  * round1_phase0_dossiers/grok_phase0_dossier.txt
  * round1_phase0_dossiers/qwen_phase0_dossier.txt
  * round2_crosscheck/MISORA_PHASE1_CROSSCHECK_ROUND2.md
  * round2_crosscheck/gemini_round2_critique.txt
  * round2_crosscheck/grok_round2_critique.txt
  * round2_crosscheck/qwen_round2_critique.txt
  * round3_convergence/gemini_code_review1.txt
  * round3_convergence/gemini_code_review2.txt
  * round3_convergence/gemini_code_review3.txt
  * round3_convergence/gemini_round3_review.txt
  * round3_convergence/gemini_round4_review.txt
  * round3_convergence/gpt_round3_convergence.txt
  * round3_convergence/grok_round3_review.txt
  * ... and 13 more files

### misora_phase2_debate_turns.zip
- **Description:** Intermediate turn-by-turn catch-up relays and handoff files from 2026-11-21/2026-11-22 Phase 2 debate.
- **File Size:** 39.7 KB (40,616 bytes)
- **SHA256:** c9a14cac97ab20c2353617f75e02b88185cb02eca58b5a43a7e51934673b5bd1
- **Files Contained (6):**
  * 2026-11-21_phase2_s0_s1/Misora_Copilot_Desktop_Phase3_S0_S1_Guide.txt
  * 2026-11-22_phase2_s8b_s2/round1_ux_audit_and_migration/HANDOFF_PROMPT_Qwen_Misora_2026-11-22.md
  * 2026-11-22_phase2_s8b_s2/round1_ux_audit_and_migration/gemini_master_catchup_s1_relay_s8b_sync.txt
  * 2026-11-22_phase2_s8b_s2/round1_ux_audit_and_migration/gemini_sync_brief_ux_audit_b1_b10_antigravity.md
  * 2026-11-22_phase2_s8b_s2/round1_ux_audit_and_migration/qwen_response_to_master_catchup.txt
  * 2026-11-22_phase2_s8b_s2/round1_ux_audit_and_migration/qwen_verdict_b4_b5_preview_skin.md

