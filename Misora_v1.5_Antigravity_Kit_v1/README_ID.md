# Misora: Story Editor — Paket Prompt Google Antigravity (`v1.4.1` -> `v1.5.0`)

Paket ini berisi seluruh rencana, spesifikasi teknis terverifikasi, aturan proyek (`.agents/`), dan **8 prompt sesi terisolasi** untuk dijalankan secara berurutan di **Google Antigravity** pada workspace lokal `D:\Misora-Editor`.

---

## 1. Struktur Isi ZIP

```text
Misora_v1.5_Antigravity_Kit_v1/
├── README_ID.md                                       # Panduan ini (Bahasa Indonesia)
├── MASTER_PLAN_AND_LEDGER.md                          # Ledger induk & peta 100% ID (untuk cross-check AI lain)
├── AFTER_PROCEED_GOAL_SNIPPETS.md                     # Cuplikan /goal opsional (HANYA setelah klik Proceed)
├── MANIFEST.sha256                                    # Checksum SHA-256 semua berkas paket
├── setup_antigravity/
│   └── .agents/
│       ├── rules/misora-safety.md                     # Aturan permanen yang sudah diamendemen (A.b.c, XUAT, dll.)
│       └── skills/misora-verify/SKILL.md              # Skill verifikasi otomatis Python 3.12 Windows
└── prompts/
    ├── S01_v1.4.1_stability_memory_version_rebrand.md # Remediation P1 (GPT BUG-01..06 + BONUS-01..03) + U00 + U04
    ├── S02_v1.4.2_fonts_ruler_gutter_char_counter.md  # Font Global/JP/Custom + Ruler konstan + Line Number + U06
    ├── S03_v1.4.3_all_script_techA_preview_paste.md   # All Script Teknik A + Fix 3rd Window + Preview Priconne + Paste Box
    ├── S04_v1.4.4_ribbon_header_drawer_mtl_controls.md# Layout Ribbon/Header + Left Drawer + MTL UX + Checkbox/Radio
    ├── S05_v1.4.5_speaker_jump_console_about_gif.md   # Speaker Jump/Autocomplete + Win32 Console + About Support Me
    ├── S06_v1.4.6_tools_menu_auto_word_wrap.md        # Menu Tools + Auto Word Wrap (opt-in Import & manual)
    ├── S07_v1.4.7_xuat_cleanup_archive_safety.md      # Engine Transaksional XUAT Cleanup, Archive, & Debug > Safety
    └── S08_v1.5.0_release_gate_stress_qa.md           # Audit Final, Stress Test Memori, QA Windows, Promosi v1.5.0
```

---

## 2. Pengaturan Google Antigravity yang Direkomendasikan

- **Surface:** Antigravity App / IDE Extension (mode **Local** di `D:\Misora-Editor`).
- **Command Utama:** Setiap file prompt dimulai dengan `/plan` di baris pertama (**Planning-First Gate**). Antigravity wajib membaca kode lokal, membuat **Implementation Plan artifact**, lalu **BERHENTI** menunggu Anda mengklik **Proceed** sebelum mengubah satu baris pun.
- **Model & Effort yang Disarankan per Sesi:**
  - **S01, S03, S07 (Risiko Tinggi — Concurrency/Memori/Render/Transaksi File):** *Gemini 4 Neon (High)* atau *Claude Opus 4.6* / *Orchestrator*.
  - **S02, S04, S05, S06 (Menengah — Font/Win32/UI/Word-Wrap):** *Gemini 4 Carbon (High)* atau *Claude Sonnet 4.6*.
  - **S08 (Release Gate & Audit):** *Gemini 4 Neon (High)* atau *Claude Opus 4.6*.
- **Command yang Sengaja Tidak Dipakai:** Tidak menggunakan `/teamwork` makro agar setiap sesi punya gerbang review manusia + commit Git yang bersih.

---

## 3. Cara Menjalankan (Langkah demi Langkah)

1. **Sinkronisasi Git & Setup `.agents/` (Sekali di Awal):**
   - Pastikan `git status` di `D:\Misora-Editor` bersih dan tersinkron dengan GitHub sebelum memulai S01.
   - **Periksa dulu** isi `D:\Misora-Editor\.agents\` yang sudah ada. Gabungkan (*merge*) secara aman `setup_antigravity/.agents/rules/misora-safety.md` dan `setup_antigravity/.agents/skills/misora-verify/SKILL.md` (jangan menimpa file lokal lain secara membabi buta). Jika memakai CLI `agy`, jalankan `/skills reload`.
2. **Eksekusi Berurutan (`S01` -> `S08`):**
   - Buka **chat baru** (`/new` atau `/clear`) untuk **setiap sesi**.
   - Buka file `prompts/S0X_...md`, tekan `Ctrl+A` -> `Ctrl+C`, tempel utuh ke Antigravity.
   - **Lampiran Gambar Visual (Wajib di S03 & S04):**
     - Pada **S03**, tempel juga lewat `Ctrl+V` dua screenshot game: `bandicam 2026-11-22 02-28-14-200.jpg` (Dialogue Preview) dan `bandicam 2026-11-22 02-28-27-995.jpg` (All Script Preview).
     - Pada **S04**, tempel juga lewat `Ctrl+V` gambar `current.png` dan `Espected.png` (dengan aturan teks `U09`/`U10`/`U13`/`U14`/`4.2` sebagai penentu akhir).
3. **Review Plan -> Klik `Proceed` -> Review Walkthrough:**
   - Periksa **Implementation Plan** (atau tempel ke panel AI untuk review cepat `SAFE TO PROCEED`), berikan komentar inline jika perlu, lalu klik **Proceed**.
   - Jika agen berhenti terlalu cepat setelah `Proceed`, kirimkan 1 cuplikan yang sesuai dari `AFTER_PROCEED_GOAL_SNIPPETS.md` pada chat yang sama.
   - Setelah **Walkthrough** keluar dengan hasil tes hijau, tinjau `git diff`, lakukan uji cepat manual di Windows, lalu **commit manual di Git** sebelum membuka chat baru untuk sesi berikutnya.
4. **Hukum Berhenti (`STOP`):**
   - Jika sebuah *failing-first Probe* ternyata sudah `PASS` sebelum patch, agen harus berhenti dan melapor — jangan pernah memaksa bug palsu atau melemahkan tes.
   - Jangan lanjut ke sesi berikutnya sebelum sesi berjalan hijau dan di-commit.
