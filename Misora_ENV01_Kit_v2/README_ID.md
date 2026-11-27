# Misora — ENV-01 Context Hygiene Kit v2

**Status paket: siap untuk review/upload; belum dijalankan pada working tree Misora.**

Kit ini menyatukan alur `/plan` Kit v1 dengan Context Router, klasifikasi bukti, pemetaan retensi menyeluruh, dan validasi empat-AI. Kit v2 menjadi satu-satunya kit eksekusi kanonis. Dua paket lama tetap disimpan sebagai provenance; jangan memuat keduanya bersamaan sebagai instruksi aktif.

## Baseline yang dikunci

| Item | Nilai |
|---|---|
| Repository | `ImaterialC/Misora-Editor` |
| Branch | `main` (wajib diverifikasi lokal) |
| S11e HEAD | `ead65077a2a6cf3a664543cfb50f855268a29e2a` |
| Current product version | `1.4.15` |
| v1.5.0 release campaign | `CANCELLED`; belum dirilis; promosi versi tidak diotorisasi |
| Old S12 release audit | `PAUSED / SUPERSEDED`; plan lama jangan dijalankan |
| Future S15 work proposal | `CANCELLED`; milestone S15 historis yang telah selesai tetap dipertahankan |
| ENV-01 scope | Dokumentasi + generator indeks AST baca-saja; tanpa perubahan produk/tes |

**Konflik sumber yang harus direkonsiliasi:** `PROJECT_STATE.md` pada baseline S11e masih menulis `v1.5.0 ON HOLD`. Keputusan Project Lead yang lebih baru adalah `CANCELLED`. Simpan teks lama dalam arsip byte-identical; tampilkan keputusan terkini pada dashboard dan ledger keputusan.

## Isi paket

```text
Misora_ENV01_Kit_v2/
├── README_ID.md
├── SHA256SUMS.txt
├── prompts/
│   ├── 01_ENV01_v2_Antigravity_PLAN_Prompt.txt
│   ├── 02_Reviewer_Handoff_Template.txt
│   ├── 03_ENV01_v2_Proceed_Template.txt
│   └── 04_Four_AI_Validation_Test.txt
├── drafts/
│   ├── AGENTS.md
│   ├── PROJECT_STATE.md
│   ├── CONTEXT_ROUTER.md
│   ├── OPEN_ISSUES.md
│   ├── DECISIONS.md
│   ├── HISTORY_INDEX_TEMPLATE.md
│   ├── ENV01_MIGRATION_MAP_TEMPLATE.md
│   └── SUPERSEDED_PLANS_README_TEMPLATE.md
└── scripts/
    └── generate_symbol_index.py
```

Semua file di `drafts/` adalah rancangan target, bukan file yang boleh disalin tanpa review. `ENV01_MIGRATION_MAP.md` final harus dihasilkan dari file lokal pada HEAD yang dikunci karena line number, heading, dan slug wajib berasal dari bytes lokal.

## Apa yang dilakukan terhadap setiap file

| File paket | Tindakan di repo Misora-Editor | Catatan penting |
|---|---|---|
| `drafts/AGENTS.md` | Setelah plan disetujui, jadikan kandidat pengganti root `AGENTS.md`. | Ringkas aturan permanen; pertahankan semua 29 topik melalui migration map. Maksimum 6.144 bytes. |
| `drafts/PROJECT_STATE.md` | Jadikan kandidat pengganti root `PROJECT_STATE.md`. | Dashboard aktif, bukan arsip. Wajib mencerminkan pembatalan v1.5.0 dan status S15 secara tepat. Maksimum 15.360 bytes. |
| `drafts/CONTEXT_ROUTER.md` | Salin ke `docs/ai/CONTEXT_ROUTER.md`. | Instruksi routing; default hanya Layer 0, lalu 1–3 dokumen relevan. |
| `drafts/ENV01_MIGRATION_MAP_TEMPLATE.md` | Gunakan sebagai kerangka untuk menghasilkan `docs/ai/ENV01_MIGRATION_MAP.md`. | Bukan migration map final; Antigravity harus mengisi tiap 29 bagian AGENTS dan setiap heading H1–H6 PROJECT_STATE berdasarkan file lokal arsip. |
| `drafts/OPEN_ISSUES.md` | Salin/review sebagai `docs/project/OPEN_ISSUES.md`. | Ledger T-01..T-14, DEF-01..DEF-10, test debt, fixture blocker, watch-item, dan MANUAL-PENDING. Tidak mengotorisasi implementasi. |
| `drafts/DECISIONS.md` | Salin/review sebagai `docs/project/DECISIONS.md`. | Otoritas keputusan aktif; DEC-01A membatalkan status ON HOLD lama. |
| `drafts/HISTORY_INDEX_TEMPLATE.md` | Gunakan untuk membuat `docs/archive/HISTORY_INDEX.md`. | Index terpisah; jangan menambahkan apa pun ke dua arsip byte-identical. |
| `drafts/SUPERSEDED_PLANS_README_TEMPLATE.md` | Salin ke `docs/archive/superseded-plans/README.md`. | Tandai plan S12 lama sebagai superseded; simpan file plan asli tanpa menjalankannya. |
| `scripts/generate_symbol_index.py` | Salin ke `tools/generate_symbol_index.py`. | Jalankan hanya setelah Proceed; membuat `docs/architecture/MISORA_SYMBOL_INDEX.md` dengan `Indexed Source Revision` (pathspec Python-only) dan penolakan file `.py` untracked/ignored. `--check` hanya membandingkan bytes dan tidak menulis. |
| `prompts/01_...PLAN_Prompt.txt` | Tempel ke Antigravity dalam sesi baru. | Perencanaan read-only. Hasil akhir harus STOP sebelum edit. |
| `prompts/02_...Reviewer_Handoff_Template.txt` | Kirim bersama plan yang sama ke Gemini, GPT-6, dan Qwen. | Review independen; bukan otorisasi edit. |
| `prompts/03_...Proceed_Template.txt` | Isi dan kirim hanya setelah Project Lead memberi Proceed eksplisit dan reviewer tidak menemukan blocker. | Mengotorisasi allowlist sempit saja; tidak mengizinkan commit/push. |
| `prompts/04_Four_AI_Validation_Test.txt` | Jalankan identik pada Gemini, GPT-6, Qwen, Antigravity setelah migrasi. | Berikan hanya Layer 0 + Router; jangan berikan seluruh arsip/backlog. |
| `SHA256SUMS.txt` | Gunakan untuk memverifikasi transfer paket v2. | Ini checksum file paket, bukan checksum arsip lama dalam repo. Manifest arsip dibuat terpisah saat migrasi. |

### Perlakuan terhadap file lama di Misora-Editor

Sebelum mengganti root docs, salin raw bytes `AGENTS.md` ke `docs/archive/AGENTS_v1.4_PRE_ENV01.md` dan `PROJECT_STATE.md` ke `docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md`. Verifikasi SHA-256 dan byte equality sebelum mengubah sumber. Jangan menambahkan judul, TOC, metadata, newline, atau melakukan konversi encoding. Catat hash/byte count/HEAD dalam `docs/archive/ARCHIVE_SHA256SUMS.txt` dan `HISTORY_INDEX.md` yang terpisah. Setelah itu baru ganti root docs dengan draft yang sudah direview.

Di `Misora-Reference`, jangan hapus atau timpa `Misora_ENV01_Context_Hygiene_Kit_v1/`, `Misora_ENV01_Context_Reset_Pack/`, atau plan S12 lama. Pertahankan sebagai provenance dan beri penanda bahwa v2 adalah kit eksekusi kanonis; v1/Reset Pack/S12 lama bukan instruksi aktif. Jangan meminta AI membaca beberapa kit lama dan baru sekaligus.

## Urutan penggunaan

### 0. Upload paket dan verifikasi

Unggah folder ini ke `ImaterialC/Misora-Reference/main` sebagai `Misora_ENV01_Context_Hygiene_Kit_v2/`. Jangan menimpa/menghapus `Misora_ENV01_Context_Hygiene_Kit_v1/` atau `Misora_ENV01_Context_Reset_Pack/`. Verifikasi seluruh file dan checksum `SHA256SUMS.txt`. Tandai v2 sebagai **canonical execution kit**; dua paket sebelumnya hanya provenance.

### 1. Preflight lokal — read-only

Di PowerShell pada `D:\Misora-Editor`:

```powershell
git rev-parse --show-toplevel
git rev-parse HEAD
git branch --show-current
git status --short --untracked-files=all
py -3.12 -c "import pathlib; print(pathlib.Path('__init__.py').read_text(encoding='utf-8'))"
```

HEAD harus persis `ead65077a2a6cf3a664543cfb50f855268a29e2a`, branch `main`, working tree bersih, dan `__version__` `1.4.15`. Bila berbeda, STOP. Jangan `reset`, `clean`, `checkout`, `stash`, menghapus file, atau mencoba pemulihan otomatis.

### 2. Antigravity `/plan` — tanpa edit

Mulai chat Antigravity baru pada repo yang benar dan tempel seluruh `prompts/01_ENV01_v2_Antigravity_PLAN_Prompt.txt`. Antigravity harus membaca repo secara read-only dan mengembalikan `ENV-01_Implementation_Plan.md` dalam jawaban/artefak di luar working tree. Pada tahap ini tidak boleh membuat atau mengubah file repo. Akhiri dengan `STOP — WAITING FOR INDEPENDENT REVIEW`.

### 3. Review independen

Kirim plan yang sama kepada Gemini, GPT-6, dan Qwen dengan `prompts/02_Reviewer_Handoff_Template.txt`. Setiap reviewer menilai sendiri scope, preflight, arsip byte-identical, pemetaan 29 bagian AGENTS, seluruh heading PROJECT_STATE, ledger, generator indeks, acceptance gates, dan rollback. Reviewer tidak boleh menjadikan kesimpulan AI lain sebagai bukti.

### 4. Proceed — setelah otorisasi Project Lead

Isi `prompts/03_ENV01_v2_Proceed_Template.txt` dengan HEAD aktual, hasil preflight, referensi plan, dan verdict reviewer. Kirim perintah Proceed hanya setelah semua review bersih dan Project Lead memberi izin eksplisit. Proceed mengotorisasi hanya allowlist ENV-01 — bukan source code, tests, release, commit, atau push.

### 5. Verifikasi hasil

Jalankan 11 acceptance gates dalam Proceed Template. Jika satu gagal, STOP dan laporkan. `countTestCases() == 475` adalah pemeriksaan jumlah discovery, **bukan 475 PASS**. ENV-01 tidak membutuhkan full test run karena source dan tests tidak berubah.

### 6. Uji empat-AI

Jalankan prompt identik dari `prompts/04_Four_AI_Validation_Test.txt` kepada Gemini, GPT-6, Qwen, dan Antigravity. Masing-masing hanya menerima `AGENTS.md`, `PROJECT_STATE.md`, dan `docs/ai/CONTEXT_ROUTER.md`. Jangan lampirkan arsip atau seluruh backlog. Bandingkan konsistensi fakta, status, scope, routing, dan pengakuan unknown.

## Target struktur di Misora-Editor

```text
AGENTS.md                                  # Layer 0; target 3–5 KiB, hard cap 6 KiB
PROJECT_STATE.md                           # Layer 0; target 8–10 KiB, hard cap 15 KiB
docs/ai/CONTEXT_ROUTER.md
docs/ai/ENV01_MIGRATION_MAP.md
docs/project/OPEN_ISSUES.md
docs/project/DECISIONS.md
docs/architecture/MISORA_SYMBOL_INDEX.md
docs/archive/AGENTS_v1.4_PRE_ENV01.md       # bytes identik
docs/archive/PROJECT_STATE_v1.4_PRE_ENV01.md # bytes identik
docs/archive/ARCHIVE_SHA256SUMS.txt
docs/archive/HISTORY_INDEX.md
docs/archive/superseded-plans/README.md
tools/generate_symbol_index.py
```

Jangan membuat enam dokumen arsitektur domain kosong. Buat dokumen domain hanya setelah audit domain menyatakan perlu.

## Pengamanan

- `__init__.py`, `misora.py`, `core/`, `assets/`, `tests/`, `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/`, dan `README.md` **READ-ONLY 100%**.
- Jangan ubah versi; `__version__` tetap `1.4.15`.
- Jangan jalankan old S12 plan atau buat release gate aktif untuk v1.5.0 yang dibatalkan.
- Jangan hapus milestone S15 historis. Pembatalan hanya berlaku untuk proposal S15 mendatang.
- Risiko perubahan production code: **nol karena scope**. Risiko migrasi dokumentasi: **terkendali tetapi tidak nol**.
- Arsip dibuat dari raw bytes pada HEAD lokal sebelum root file diganti. Jangan menambahkan header, TOC, newline, atau normalisasi encoding.
- Symbol index adalah alat navigasi, bukan bukti dead code atau runtime call graph lengkap.
- Kit ini belum mengubah repo, menjalankan tes pada mesin pengguna, atau mengunggah dirinya ke GitHub.

## Referensi

- [S11e commit](https://github.com/ImaterialC/Misora-Editor/commit/ead65077a2a6cf3a664543cfb50f855268a29e2a)
- [Current AGENTS.md](https://github.com/ImaterialC/Misora-Editor/blob/main/AGENTS.md)
- [Current PROJECT_STATE.md](https://github.com/ImaterialC/Misora-Editor/blob/main/PROJECT_STATE.md)
- [Kit v1 — provenance](https://github.com/ImaterialC/Misora-Reference/tree/main/Misora_ENV01_Context_Hygiene_Kit_v1)
- [Context Reset Pack — provenance](https://github.com/ImaterialC/Misora-Reference/tree/main/Misora_ENV01_Context_Reset_Pack)
