# Universal Copy-Paste Prompts for Web AIs

Copy and paste the exact prompt block below into **every participating web AI** (ChatGPT, Claude, Gemini, Qwen, Grok, etc.) at each phase. Because every prompt points to the same Markdown specifications in `Misora-Reference`, all AIs follow identical rules without prompt drift.

> **Tip:** If an AI cannot fetch GitHub URLs directly in Phase 0, it will tell you immediately — simply upload the `Misora-Editor` ZIP and `Misora-Reference` ZIP to that AI before continuing.

---

## PHASE 0 — Onboarding & Complete File Access Check

```text
Halo! Kamu bergabung dalam rapat teknis lintas-AI untuk pengembangan aplikasi **Misora-Editor** yang nantinya akan dieksekusi menggunakan **Google Antigravity**.

Sebelum berpikir, menganalisis, atau memberi saran apa pun, WAJIB baca seluruh aturan dan lakukan pemeriksaan akses file terlebih dahulu dari dua repositori GitHub berikut:

1. **Target Codebase (Source of Truth):**
   - Repo: https://github.com/ImaterialC/Misora-Editor
2. **Reference & Meeting Protocol Hub:**
   - Repo: https://github.com/ImaterialC/Misora-Reference
   - Master Protocol (Raw): https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/PROTOCOL.md
   - Phase 0 Rules (Raw): https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/phases/PHASE_0_ACCESS_CHECK.md
   - Antigravity Guide (Raw): https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/ANTIGRAVITY_GUIDE.md
   - Cek juga seluruh isi folder `tools/` dan `images/` di repo `Misora-Reference` (serta file lampiran jika ada).

TUGAS SAAT INI — **PHASE 0 SAJA**:
Ikuti instruksi di `phases/PHASE_0_ACCESS_CHECK.md` secara persis:
- JANGAN mulai meriset bug, memberi saran fitur, atau berdebat dulu.
- Laporkan secara jujur dalam **Bahasa Indonesia**:
  1. Identitas model kamu dan kemampuan akses GitHub/file kamu.
  2. Commit/versi terakhir `Misora-Editor` dan `Misora-Reference` yang terbaca.
  3. Daftar file/folder yang berhasil kamu akses di kedua repo (termasuk `misora.py`, `core/`, `assets/`, `tests/`, `AGENTS.md`, `PROJECT_STATE.md`, `tools/`, dan `images/`).
  4. Katakan secara tegas jika ada file yang TIDAK bisa diakses, rusak, atau terpotong (truncated).
  5. Akhiri dengan status: `STATUS PHASE 0: READY FOR PHASE 1` atau `STATUS PHASE 0: BLOCKED — BUTUH FILE TAMBAHAN`.
```

---

## PHASE 1 — Independent Research & Audit

```text
Semua akses file sudah terverifikasi. Sekarang kita masuk ke **PHASE 1 (Riset Mandiri)**.

Baca dan patuhi aturan lengkap di:
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/PROTOCOL.md
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/phases/PHASE_1_INDEPENDENT_RESEARCH.md

INSTRUKSI PHASE 1:
1. Lakukan riset mandiri secara mendalam terhadap https://github.com/ImaterialC/Misora-Editor (serta referensi di `tools/` dan `images/` pada `Misora-Reference` jika ada) untuk menemukan bug, risiko integritas data/threading, masalah efisiensi, dan ide fitur praktis yang relevan.
2. Kamu bekerja secara **independen** (tanpa terpengaruh AI lain maupun saya). Jangan tunda Phase 1 untuk hal-hal kecil; taruh pertanyaan ambigu di bagian akhir blok untuk dibahas di Phase 2. Hanya konfirmasi ke saya jika ada blocker krusial.
3. **Aturan Bahasa:**
   - Pengantar/ringkasan ke saya dalam **Bahasa Indonesia**.
   - Seluruh hasil riset & temuan dalam **Bahasa Inggris** di dalam **SATU blok teks (` ```text `)** sesuai template di `PHASE_1_INDEPENDENT_RESEARCH.md` agar bisa langsung saya copy/download ke AI lain.
   - Setiap klaim bug WAJIB menyertakan file, fungsi, baris, dan status `[CONFIRMED]` atau `[NEEDS-VERIFY]`.
4. JANGAN buat prompt Antigravity dulu. Akhiri blok dengan `PHASE 1 STATUS: COMPLETE`.
```

---

## PHASE 2 — Multi-AI Debate & Synthesis

```text
Phase 1 selesai. Sekarang kita masuk ke **PHASE 2 (Penggabungan, Cross-Check & Debat Lintas-AI)**.

Baca dan patuhi aturan lengkap di:
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/phases/PHASE_2_DEBATE_SYNTHESIS.md

Di bawah ini adalah gabungan hasil riset Phase 1 dari AI lain serta temuan bug manual / ide / batasan dari saya:

---
[TEMPELKAN HASIL PHASE 1 AI LAIN & TEMUAN MANUAL SAYA DI SINI]
---

INSTRUKSI PHASE 2:
1. Cross-check setiap klaim AI lain langsung terhadap kode sumber asli `Misora-Editor`. Jangan setuju hanya karena sopan — bantah dengan bukti file/baris jika ada halusinasi atau over-engineering, dan tarik klaim lamamu jika terbukti keliru.
2. Evaluasi dan gabungkan temuan manual / kebutuhan saya dengan jujur (beri tahu jika ada risiko teknis di Tkinter/UnityPy dan usulkan desain teraman).
3. **Aturan Bahasa:**
   - Penjelasan & pertanyaan untuk saya dalam **Bahasa Indonesia**.
   - Pesan debat/kritik untuk AI lain dalam **Bahasa Inggris** di dalam **SATU blok teks (` ```text `)** yang mudah di-download/copy sesuai template `PHASE_2_DEBATE_SYNTHESIS.md`.
4. JANGAN tulis prompt Antigravity dulu.
5. Akhiri blok dengan status tegas:
   - `PHASE 2 STATUS: OPEN — CONTINUING DEBATE` (jika masih ada sanggahan/pertanyaan)
   - atau `PHASE 2 STATUS: READY TO LOCK FOR PHASE 2.5` (jika kamu sudah sepakat penuh).
```

*(Untuk ronde lanjutan Phase 2, cukup ganti bagian tempelan dengan balasan terbaru dari AI lain dan jawaban user.)*

---

## PHASE 2.5 — Canonical Ledger Lock (Fast Anti-Hallucination Sync)

```text
Semua AI dan saya sudah sepakat di Phase 2! Sekarang kita masuk ke **PHASE 2.5 (Canonical Ledger Lock — Sinkronisasi Cepat & Audit Anti-Halusinasi)**.

Baca dan patuhi aturan lengkap di:
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/phases/PHASE_2_5_LEDGER_LOCK.md
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/templates/CANONICAL_LEDGER_TEMPLATE.md

[OPSIONAL — TEMPELKAN DRAFT LEDGER DARI AI PERTAMA JIKA RONDE KONFIRMASI]

INSTRUKSI PHASE 2.5:
1. Generate daftar seragam seluruh **Bug (`BUG-*`)**, **Fitur/UX (`FEAT-*`)**, **Hygiene (`HYG-*`)**, **Deferred (`DEF-*`)**, dan **Rejected/Non-Goals (`NO-*`)** yang telah disepakati selama rapat.
2. JANGAN tambah ide baru dan JANGAN buka debat lama.
3. Lakukan audit ketat:
   - Pastikan **TIDAK ADA SATU PUN** temuan bug, ide user, atau guardrail yang terlewat.
   - Pastikan **TIDAK ADA** halusinasi, klaim belum terverifikasi, atau bug yang sudah di-retract yang masih nyangkut.
4. Sampaikan catatan singkat ke saya dalam **Bahasa Indonesia**, dan keluarkan Canonical Ledger dalam **Bahasa Inggris** di **SATU blok teks (` ```text `)**.
5. Akhiri dengan status tegas: `PHASE 2.5 STATUS: LOCKED & IDENTICAL` atau `PHASE 2.5 STATUS: MISMATCH FOUND`.
```

---

## PHASE 3 — Antigravity Prompt Engineering & Session Slicing Debate

```text
Phase 2.5 selesai dan Canonical Ledger sudah **LOCKED & IDENTICAL** di semua AI!
Sekarang kita masuk ke **PHASE 3 (Penyusunan Prompt Google Antigravity, Urutan Eksekusi, Strategi Test & Pembagian Sesi)**.

Baca dan patuhi aturan lengkap di:
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/ANTIGRAVITY_GUIDE.md
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/phases/PHASE_3_PROMPT_ENGINEERING.md
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/templates/ANTIGRAVITY_PROMPT_TEMPLATE.md

[TEMPELKAN CANONICAL LEDGER FINAL PHASE 2.5 ATAU DRAFT PROMPT AI LAIN UNTUK DIKRITIK DI SINI]

INSTRUKSI PHASE 3:
1. Susun / debat:
   - Pembagian sesi Antigravity (kecil, aman, dependency-ordered) dan peta cakupan 100% ID dari Phase 2.5 (`BUG-*`, `FEAT-*`, `HYG-*`).
   - Strategi pengujian (failing-first Probes vs Regression Guards, isolasi test, perintah verifikasi `py -3.12`).
   - Draft prompt Antigravity yang mematuhi `/plan` gate, file ownership ketat, dan guardrails `ANTIGRAVITY_GUIDE.md` tanpa over-engineering.
2. Jika sedang membandingkan draft prompt antar-AI, bersikaplah jujur: kritik kelemahan tiap draft dan pilih/gabungkan menjadi SATU versi prompt terbaik yang identik.
3. **Aturan Bahasa:** Ringkasan ke saya dalam **Bahasa Indonesia**; blok debat & draft prompt Antigravity dalam **Bahasa Inggris** di dalam blok teks siap salin.
4. Akhiri blok dengan: `PHASE 3 STATUS: OPEN — DEBATING PLAN/PROMPTS` atau `PHASE 3 STATUS: APPROVED & IDENTICAL`.
```

---

## PHASE 4 — Official Antigravity Execution & Feedback Q&A (NO DEBATE)

```text
Phase 3 sudah sepakat dan prompt sudah saya jalankan di **Google Antigravity**.
Sekarang kita resmi berada di **PHASE 4 (Tanya Jawab & Evaluasi Feedback Antigravity — TANPA DEBAT)**.

Baca dan patuhi aturan di:
- https://raw.githubusercontent.com/ImaterialC/Misora-Reference/main/phases/PHASE_4_ANTIGRAVITY_QA.md

ATURAN KETAT PHASE 4:
- JANGAN memulai debat baru, JANGAN menambah fitur di luar prompt Phase 3.
- Fokus 100% menganalisis output Antigravity di bawah ini (Implementation Plan / Error Loop / Test Output / Walkthrough).
- Jawab saya dalam **Bahasa Indonesia** dengan verdict tegas (`APPROVE — KLIK PROCEED`, `REVISI PLAN DULU`, `FIX ERROR LOOP`, atau `SESSION COMPLETE`).
- Jika perlu instruksi perbaikan ke Antigravity, sertakan blok teks **Bahasa Inggris** yang singkat, bedah tepat sasaran, dan siap copy-paste ke Antigravity.

---
[TEMPELKAN FEEDBACK / ARTIFACT / ERROR LOG DARI ANTIGRAVITY DI SINI]
---
```
