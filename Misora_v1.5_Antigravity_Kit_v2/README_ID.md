# Misora: Story Editor — Paket Prompt Google Antigravity v2 (`v1.4.1` -> `v1.5.0`)

Paket ini berisi seluruh rencana, spesifikasi teknis terverifikasi, template konfigurasi `.agents/`, dan **8 prompt sesi terisolasi** untuk dijalankan secara berurutan di **Google Antigravity** pada workspace lokal `D:\Misora-Editor`.

> **STATUS PAKET:** Revisi `v2` (hasil tindak lanjut review independen GPT). **Belum diotorisasi untuk eksekusi S01** sebelum review lintas-AI berikutnya menyatakan persetujuan eksplisit. Jangan mengubah kode sumber `Misora-Editor` sebelum otorisasi tersebut.

---

## 1. Struktur Isi ZIP

```text
Misora_v1.5_Antigravity_Kit_v2/
├── README_ID.md                                        # Panduan operator ini (Bahasa Indonesia)
├── MASTER_PLAN_AND_LEDGER.md                           # Ledger induk, rekonsiliasi baseline & peta 100% ID
├── AFTER_PROCEED_GOAL_SNIPPETS.md                      # Cuplikan /goal opsional (HANYA setelah klik Proceed)
├── MANIFEST.sha256                                     # Checksum SHA-256 semua berkas paket
├── setup_antigravity/
│   └── .agents/
│       ├── rules/misora-safety.md                      # Aturan permanen always_on (sudah diamendemen)
│       └── skills/misora-verify/SKILL.md               # Skill verifikasi otomatis Python 3.12 Windows
└── prompts/
    ├── S01_v1.4.1_stability_memory_version_rebrand.md  # Remediation P1 (BUG-01..06 + BONUS-01..03) + U00 + U04
    ├── S02_v1.4.2_fonts_ruler_gutter_char_counter.md   # Font Global/JP/Custom + Ruler konstan + Gutter + U06
    ├── S03_v1.4.3_all_script_techA_preview_paste.md    # All Script Teknik A + Fix 3rd Window + Preview + Lossless Paste Box
    ├── S04_v1.4.4_ribbon_header_drawer_mtl_controls.md # Layout Ribbon/Header + Drawer Lifecycle + MTL UX + Checkbox
    ├── S05_v1.4.5_speaker_jump_console_about_gif.md    # Speaker Jump/Autocomplete + Win32 Console + About Streaming GIF
    ├── S06_v1.4.6_tools_menu_auto_word_wrap.md         # Menu Tools + Auto Word Wrap (opt-in Import & manual)
    ├── S07_v1.4.7_xuat_cleanup_archive_safety.md       # Engine Transaksional XUAT Cleanup, Mandatory Archive & Debug > Safety
    └── S08_v1.5.0_release_gate_stress_qa.md            # Release Gate Jujur, Stress Test Memori (tracemalloc/weakref) & QA
```

---

## 2. Pengaturan Google Antigravity yang Direkomendasikan

- **Surface:** Antigravity App / IDE Extension (mode **Local** di `D:\Misora-Editor`).
- **Command Utama:** Setiap prompt sesi dimulai dengan `/plan` di baris pertama (**Planning-First Gate**). Antigravity wajib membaca file lokal dari disk, menyusun **Implementation Plan artifact**, lalu **BERHENTI** menunggu `Proceed` sebelum mengedit file apa pun.
- **Model & Effort yang Disarankan per Sesi:**
  - **S01, S03, S07, S08 (Risiko Tinggi — Concurrency/Memori/Lossless AST/Transaksi File/Gate):** *Claude Opus 4.6* atau *Gemini 4 Neon (High)*.
  - **S02, S04, S05, S06 (Menengah — Font/Win32/UI/Word-Wrap):** *Claude Sonnet 4.6* atau *Gemini 4 Carbon (High)*.
- **Command yang Sengaja Tidak Dipakai:** Tidak menggunakan `/teamwork` makro agar setiap sesi memiliki review manusia dan batas file eksklusif pada `misora.py`.

---

## 3. Prosedur Setup & Preflight Aman (WAJIB Sebelum S01)

> **PERINGATAN KESELAMATAN WORKSPACE:** Workspace yang bersih memang disarankan, tetapi **JANGAN PERNAH** menghapus, menimpa, me-`reset`, men-`clean`, atau men-`stash` pekerjaan lokal atau file tak terlacak (`untracked`) yang sah demi membuat `git status` terlihat bersih.

Lakukan 6 langkah berikut di `D:\Misora-Editor` sebelum memulai S01:

1. **Catat branch aktif dan commit `HEAD` lokal:**
   ```powershell
   git branch --show-current
   git rev-parse HEAD
   ```
2. **Catat seluruh status workspace awal (`git status --short`):**
   ```powershell
   git status --short
   ```
3. **Tinjau seluruh perubahan lokal & file untracked yang sudah ada** (mis. `misora_config.json`, fixture `.unity3d`, perubahan S24 lokal, atau catatan kerja).
4. **Pertahankan seluruh data lokal yang sah** — dilarang keras menjalankan `git reset`, `git clean`, `git stash`, destructive `git checkout`/`git restore`, atau menimpa `misora_config.json`.
5. **Gabungkan (*merge*) template `.agents/` dengan hati-hati:**
   - Periksa isi folder `D:\Misora-Editor\.agents\` yang sudah ada terlebih dahulu.
   - Gabungkan secara manual/selektif `setup_antigravity/.agents/rules/misora-safety.md` dan `setup_antigravity/.agents/skills/misora-verify/SKILL.md` tanpa menghapus rule/skill/hook/MCP lokal lain. Jika memakai CLI `agy`, jalankan `/skills reload`.
6. **Bandingkan perubahan akhir sesi terhadap status workspace awal** (pastikan sesi hanya menambahkan/mengubah berkas di dalam *Allowed Files* sambil tetap menjaga seluruh berkas lokal pra-sesi tetap utuh).

---

## 4. Preflight Aset Lokal (Wajib Dicek Sebelum Sesi Terkait)

Jangan mengasumsikan file aset pasti tersedia hanya karena disebut dalam prompt — pastikan keberadaannya di disk sebelum menempel prompt sesi terkait:
- **Sebelum S03:** Verifikasi keberadaan 2 gambar referensi Preview:
  - `bandicam 2026-11-22 02-28-14-200.jpg` (referensi Dialogue Preview)
  - `bandicam 2026-11-22 02-28-27-995.jpg` (referensi All Script Preview)
  Tempel keduanya lewat `Ctrl+V` bersamaan dengan `prompts/S03_v1.4.3_all_script_techA_preview_paste.md`.
- **Sebelum S04:** Verifikasi keberadaan 2 gambar referensi layout:
  - `current.png` dan `Espected.png`
  Tempel keduanya lewat `Ctrl+V` bersamaan dengan `prompts/S04_v1.4.4_ribbon_header_drawer_mtl_controls.md` (ingat: aturan tertulis `U09`/`U10`/`U12`/`U13`/`U14`/`4.2` mengalahkan distorsi mockup).
- **Sebelum S05:** Verifikasi langsung di disk apakah `D:\Misora-Editor\assets\Service.gif` benar-benar ada dan terbaca oleh Pillow. Jika tidak ada, catat dalam Plan S05 dan pastikan dialog Support Me tetap tampil rapi dengan fallback tanpa crash.

---

## 5. Cara Menjalankan Sesi (`S01` -> `S08`)

1. Buka **chat baru** (`/new` atau `/clear`) untuk **setiap sesi**.
2. Buka `prompts/S0X_...md`, salin utuh (`Ctrl+A` -> `Ctrl+C`), lalu tempel ke Antigravity (sertakan gambar via `Ctrl+V` untuk S03 dan S04).
3. Tinjau **Implementation Plan artifact** terlebih dahulu; pastikan preflight baseline, simbol target, dan rencana tes akurat sebelum menekan **Proceed**.
4. Jika agen berhenti sebelum seluruh verifikasi selesai setelah `Proceed`, kirimkan maksimal **1** cuplikan yang sesuai dari `AFTER_PROCEED_GOAL_SNIPPETS.md`.
5. Setelah **Walkthrough** selesai dengan bukti output nyata (`compileall`, targeted `unittest`, `unittest discover`, diff terhadap `git status` awal), tinjau `git diff` lalu lakukan **commit Git manual** oleh Project Lead sebelum membuka chat sesi berikutnya.
