# Misora: Story Editor — Paket Prompt Antigravity S09–S12 (v1.0)

Paket ini berisi 4 prompt eksekusi final **S09 (`v1.4.8`)** s.d. **S12 (`v1.4.10` -> kondisional `v1.5.0`)** yang telah menyertakan seluruh 7 koreksi teknis dari review terakhir GPT (`GPT2Gemini3.txt`).

## Isi Paket
- `prompts/S09_v1.4.8_Core_Fixes_54d.txt` — Perbaikan bug inti (`U-01`, `U-02`, `U-06`, `U-07`, `U-16`, `U-18`, `U-19`, `RM-01`).
- `prompts/S10_v1.4.9_All_Script_Virtualized_Quick_Edit.txt` — Virtualized Card Pool All Script (`U-04`, `U-05`, `U-15`, `U-17`, `U-20`) & `raw_breaks`-safe `Quick Edit` (`U-03`).
- `prompts/S11_v1.4.10_Async_XUAT_Archiving_Progress.txt` — Async `XUAT Translation Archiving` (`U-08`..`U-14`), pre-pass proteksi Actor, guard identitas dokumen, dan unified progress controller.
- `prompts/S12_v1.5.0_Audit_Release_Gate.txt` — Audit read-only bloat/dead-code/memory-leak, perbaikan 3 tes hygiene non-fixture, dan Release Gate jujur `v1.5.0`.
- `CHANGE_SUMMARY_FOR_GPT.md` — Ringkasan 7 koreksi untuk verifikasi cepat GPT.
- `SHA256SUMS.txt` — Daftar hash SHA-256 dan ukuran byte seluruh file dalam paket ini.

## Rekomendasi Model & Urutan Eksekusi di Google Antigravity
1. Jalankan **1 chat baru per sesi** (berurutan: `S09` -> commit lokal -> `S10` -> commit lokal -> `S11` -> commit lokal -> `S12`).
2. Salin isi file `.txt` (dimulai dari `/plan`) ke Google Antigravity, tunggu *Implementation Plan* keluar, tinjau Allowed Files & simbol, lalu baru klik **`Proceed`**.
3. Rekomendasi model:
   - **S09 (`v1.4.8`):** Model reasoning kuat untuk `/plan` (mis. *Gemini 4 Carbon/Neon High* atau *Orchestrator*).
   - **S10 (`v1.4.9`):** **Wajib model kuat** (*Gemini 4 Neon High* / *Orchestrator* / *Claude Opus/Sonnet High*) karena arsitektur virtualisasi + `raw_breaks` AST multi-segmen.
   - **S11 (`v1.4.10`):** **Wajib model kuat** (*Gemini 4 Neon High* / *Orchestrator*) karena *concurrency*, antrean terminal, dan transaksi XUAT.
   - **S12 (`v1.4.10` -> `v1.5.0?`):** Model reasoning tinggi untuk audit *read-only* mendalam dan evaluasi Release Gate.

## Pengingat Penting
- Jangan menempelkan teks dari chat yang terpotong — ekstrak ZIP ini dan salin langsung dari file `prompts/S09..S12*.txt`.
- Lakukan commit lokal Git per sesi (tanpa `git push` otomatis) setelah Walkthrough setiap sesi diverifikasi.
