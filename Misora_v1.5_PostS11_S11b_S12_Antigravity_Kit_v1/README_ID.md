# Misora: Story Editor — Paket Prompt Lengkap Post-S11 (`S11b`–`S12`, v1.0)

Paket ini berisi **5 prompt eksekusi Google Antigravity lengkap** untuk seluruh jalur pra-`v1.5.0` (`S11b`, `S11c`, `S11d`, `S11e`, dan `S12` versi rekonsiliasi) yang sudah membawa seluruh invariant terkunci (`S01`–`S11`, `S09b` Lock Matrix, `Q-01`–`Q-18`, `Q-22`–`Q-23`, Option B config, dan 8 syarat gerbang rilis `S12`).

## Isi Paket
1. `prompts/S11b_v1.4.11_XUAT_Scanner_Save_Ruby_Preview.txt` — `Q-01`, `Q-02` (+ STOP gate Save Hang & cek bentrok `Ctrl+Shift+S` vs `Save As`), `Q-04` (`1.1`, `1.2`; `1.3 = NOT TESTED`), `Q-18` (+ STOP gate Ruby Preview), `Q-23`.
2. `prompts/S11c_v1.4.12_Quick_Edit_Unified_Single_Box.txt` — `Q-22` eksklusif (`box.clean_text`, `inject_box(idx, None, new_tx)`, parity test vs Manual Dialogue, migrasi S08 & S10).
3. `prompts/S11d_v1.4.13_Import_UX_SelectAll_MTLGlobe_TitleBar.txt` — `Q-06` s.d. `Q-12`.
4. `prompts/S11e_v1.4.14_WordWrap_Splash_Branding_Icons_Menu_Tooltips.txt` — `Q-03`, `Q-05`, `Q-13` s.d. `Q-17` (+ 2 sub-gate `/plan` untuk inventaris Menu Utama dan definisi Tooltip 3 Lapis).
5. `prompts/S12_v1.5.0_Audit_Hygiene_Release_Gate.txt` — Audit *read-only* produksi, 3 perbaikan tes hygiene (S01 `test_probe_8` + Option B config), tabel disposisi 8 *failure/error* individual + 35 *skip*, dan 8 syarat promosi `v1.5.0`.
6. `ROADMAP_RECONCILED_v5.md` — Ringkasan kontrak v5 & Track B pasca-`v1.5.0`.
7. `SHA256SUMS.txt` — Manifest integritas SHA-256 seluruh berkas dalam paket ini.

## Aturan Eksekusi Aman di Google Antigravity
1. **Opsional Review Cepat GPT:** Anda bisa mengunggah file ZIP ini (atau `prompts/S11b_...txt` saja terlebih dulu) ke ChatGPT jika ingin verifikasi lintas-AI sebelum memulai `/plan`.
2. **1 Chat Baru per Sesi (Berurutan):** Jalankan `S11b` -> QA manual Windows -> commit lokal -> `S11c` -> QA -> commit -> `S11d` -> QA -> commit -> `S11e` -> QA -> commit -> `S12`.
3. **Wajib Tunggu `/plan`:** Tempel seluruh isi file `.txt` (dimulai dari `/plan`), baca *Implementation Plan* (terutama hasil *profiling* `Q-02`, cek konflik `Ctrl+Shift+S`, cek `Q-18` di `S11b`, serta inventaris Menu & Tooltip 3 Lapis di `S11e`), baru klik **`Proceed`**.
4. **Rekomendasi Model:**
   - `S11b` & `S11c`: Model reasoning tinggi (*Gemini 4 Neon High* / *Claude Sonnet/Opus High* / *Orchestrator*) karena menyentuh profiling Save, scanner XUAT, dan AST/Undo parity.
   - `S11d` & `S11e`: *Gemini 4 Carbon/Neon High* atau *Claude Sonnet*.
   - `S12`: Model reasoning tinggi untuk audit *read-only* mendalam dan evaluasi 8 syarat gerbang rilis.
5. **Jika STOP Gate Terpicu di `S11b`:** Bila hasil `/plan` memisahkan *async save* atau *Ruby renderer* ke sesi tambahan, nomor versi sesi berikutnya tinggal dinaikkan berurutan — seluruh prompt `S11c`–`S12` sudah ditulis agar mengikuti versi aktual di `__init__.py`.
