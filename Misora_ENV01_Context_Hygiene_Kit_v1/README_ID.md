# Misora: Story Editor — ENV-01 Context Hygiene & Doc-Layering Kit (v1)

Paket ini disiapkan untuk merampingkan lingkungan konteks AI (**`AGENTS.md`**, **`PROJECT_STATE.md`**, arsip sejarah, ledger isu terbuka, dan indeks simbol AST `misora.py`) **sebelum** melanjutkan perbaikan bug (`T-01`–`T-14`) maupun gerbang rilis **`S12` (`v1.5.0`)**.

- **Status S12 & v1.5.0:** S12 resmi **DITUNDA sementara**; `v1.5.0` tetap **STRICTLY ON HOLD**.
- **Risiko Kode Produksi:** **0%** — sesi `ENV-01` bersifat *doc-only* + skrip indeks AST baca-saja (`misora.py`, `core/*.py`, `assets/*`, `tests/*`, `__init__.py` **100% READ-ONLY**).
- **Target Dampak:** Paket baca wajib AI turun dari ~235–260 KB (~60k+ token) menjadi **<= 20 KB (~5k token)** tanpa menghapus satu baris sejarah pun.

---

## Isi Paket

| Berkas | Fungsi |
|---|---|
| `README_ID.md` | Panduan urutan eksekusi singkat ini. |
| `prompts/01_ENV01_Antigravity_PLAN_Prompt.txt` | Prompt `/plan` siap tempel ke chat baru Antigravity (`ENV-01`). |
| `prompts/02_Reviewer_Handoff_GPT6_Qwen.txt` | Pesan handoff siap kirim ke **GPT-6** dan **Qwen** setelah `/plan` selesai. |
| `prompts/03_ENV01_Proceed_Template.txt` | Template perintah `Proceed` siap tempel ke Antigravity setelah GPT-6 & Qwen memberi `CLEARED FOR PROCEED`. |
| `templates/OPEN_ISSUES_SEED.md` | Rekapitulasi master `T-01`–`T-14`, item revalidasi, utang tes, `MANUAL-PENDING`, dan `DEF-01`–`DEF-10` (siap salin ke catatan Anda & sebagai acuan `docs/project/OPEN_ISSUES.md`). |
| `templates/DECISIONS_SEED.md` | Daftar keputusan aktif/deferred/superseded sebagai acuan `docs/project/DECISIONS.md`. |
| `scripts/generate_symbol_index.py` | Skrip Python 3.12 murni (stdlib `ast`, tanpa dependency tambahan) untuk menghasilkan `docs/architecture/MISORA_SYMBOL_INDEX.md` secara otomatis dari `misora.py`, `core/*.py`, dan `assets/*.py`. |
| `SHA256SUMS.txt` | Checksum SHA-256 seluruh berkas di dalam paket ini. |

---

## Urutan Pemakaian (5 Langkah Cepat)

1. **Verifikasi Kondisi Bersih Pasca-Commit `S11e` (`v1.4.15`):**
   Jalankan di PowerShell/CMD `D:\Misora-Editor`:
   ```cmd
   git rev-parse HEAD
   git status --short
   git log -2 --oneline
   ```
   Catat nilai `HEAD` baru Anda (untuk ditempel ke pesan reviewer & `Proceed`).

2. **Jalankan `/plan` `ENV-01` di Chat Baru Antigravity:**
   Tempel seluruh isi `prompts/01_ENV01_Antigravity_PLAN_Prompt.txt` ke sesi baru Antigravity. Antigravity akan membaca kondisi disk secara *read-only*, menghasilkan `ENV-01_Implementation_Plan.md` (termasuk tabel pemetaan retensi 29 bagian `AGENTS.md`), lalu **STOP**.

3. **Review Independen (Gemini, GPT-6, Qwen):**
   Unggah `ENV-01_Implementation_Plan.md` ke `ImaterialC/Misora-Reference/main` dan kirim `prompts/02_Reviewer_Handoff_GPT6_Qwen.txt` ke GPT-6 dan Qwen (ganti `<PASTE_S11E_HEAD_HERE>` dengan hasil `git rev-parse HEAD` Anda).

4. **Eksekusi `Proceed` di Antigravity:**
   Setelah GPT-6 & Qwen menjawab `CLEARED FOR PROCEED`, tempel `prompts/03_ENV01_Proceed_Template.txt` ke Antigravity (isi `<PASTE_S11E_HEAD_HERE>`). Anda juga dapat menaruh `scripts/generate_symbol_index.py` sebagai acuan implementasi `tools/generate_symbol_index.py`.

5. **Verifikasi & Commit Lokal `ENV-01` (Tanpa Push):**
   Pastikan:
   - `AGENTS.md` <= 6 KB, `PROJECT_STATE.md` <= 15 KB.
   - 100% sejarah lama tersimpan utuh di `docs/archive/PROJECT_STATE_HISTORY_v1.4.md`.
   - `git diff -- __init__.py misora.py core assets tests misora.bat requirements.txt README.md` = **KOSONG** (0 perubahan kode produksi).
   - `countTestCases()` tetap eksak `475`.
   - Commit lokal `ENV-01`, lalu lanjut ke sesi triage & perbaikan bug (`T-01` dst.) dalam kondisi konteks AI yang kembali segar!
