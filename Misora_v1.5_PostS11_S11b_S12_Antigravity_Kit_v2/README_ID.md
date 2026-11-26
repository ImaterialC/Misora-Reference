# Misora: Story Editor — Paket Prompt Antigravity Post-S11 (`S11b`–`S12`, Kit v2)

Paket ini berisi 5 prompt eksekusi lengkap **`S11b` (`v1.4.11`)** s.d. **`S12` (`<final_pre_s12>` → kondisional `v1.5.0`)** yang telah menyatukan **seluruh koreksi akhir dari Qwen (`qwen.txt`) dan ChatGPT (`gbt.txt`)**, tanpa mengubah kode sumber produksi apa pun.

## Isi Paket
- `prompts/S11b_v1.4.11_XUAT_Scanner_Save_Preview.txt` — **SIAP REVIEW FINAL PERTAMA:** `Q-01` (strict `Translation\en\Text` + `src\BepInEx` + `_norm_stripped_map` + 5 negative tests), `Q-02` (5-stage profiling + STOP Gate A + Forbidden-Core STOP + `Ctrl+S` Save Project), `Q-04` (investigasi jujur, `1.3 = NOT TESTED`), `Q-18` (Ruby Preview + STOP Gate B), `Q-23` (Preview tanpa blok merah + defensive guard + migrasi S03/S18).
- `prompts/S11c_v1.4.12_Unified_Quick_Edit.txt` — `Q-22` eksklusif (*Quick Edit* 1-kotak gabungan via `box.clean_text` & `inject_box(idx, None, new_tx)`, 8 invariant, S09b Lock Parity Row 1, *parity test* AST+biner, migrasi S10 & S08).
- `prompts/S11d_v1.4.13_Import_UX_Productivity.txt` — `Q-06`–`Q-12` (Import MouseWheel, *tri-state* Select All per grup, Synopsis multi-line termasuk saat Box 0 `summary` kosong, sub-header Archiving, `Select All Box`, MTL Globe *clipboard + official site*, *window title* `Title (Subtitle)`).
- `prompts/S11e_v1.4.14_UI_Polish_Icons_Menu_Tooltips.txt` — `Q-03`, `Q-05`, `Q-13`–`Q-17` (*word-wrap* per kelas widget, *Splash* tampil sampai seluruh UI + *restore* selesai + tes *slowed startup*, branding `PriconneRe:TL` & `Cornelia`, `Support the Creator` EN + ~600px GIF, peta ikon terkoreksi, 2 `/plan` sub-gate untuk Main Menu & Tooltip 3 lapis).
- `prompts/S12_v1.5.0_Final_Audit_Release_Gate.txt` — Audit *read-only* 4 pilar, Pre-S12 baseline run, 3 *hygiene fixes* (Option B penuh + 5-titik `test_probe_8`), 8 syarat promosi, dan **2-Gate terpisah** (`Proceed` implementasi vs persetujuan promosi `v1.5.0`).
- `CHANGE_SUMMARY_FOR_REVIEWERS.md` — Ringkasan persis semua koreksi Qwen + GPT.
- `ROADMAP_RECONCILED_v5.md` — Roadmap terkunci v5 yang sudah disinkronkan.
- `SHA256SUMS.txt` — Manifest hash SHA-256 & ukuran byte seluruh berkas.

## Alur Eksekusi Aman (Berurutan Per Sesi)
1. **Review Cepat S11b Dulu:** Kirimkan **`prompts/S11b_v1.4.11_XUAT_Scanner_Save_Preview.txt`** (+ `CHANGE_SUMMARY_FOR_REVIEWERS.md`) ke ChatGPT & Qwen untuk konfirmasi cepat E-1 & audit baris-per-baris.
2. **Jalankan 1 Chat Baru per Sesi di Antigravity:**
   `S11b` → `/plan` → tinjau → `Proceed` → QA & commit lokal → re-verifikasi singkat `S11c` → ... → `S11e` → `S12` (Gate 1 implementasi → Gate 2 promosi `v1.5.0`).
3. **Penyesuaian Versi Otomatis:** Bila STOP Gate A (`Q-02`) atau STOP Gate B (`Q-18`) memunculkan sesi pecahan baru, cukup naikkan nomor versi sesi-sesi berikutnya secara berurutan; `S12` otomatis mengikuti versi akhir aktual di `__init__.py`.
4. **Rilis `v1.5.0` tetap ON HOLD** sampai seluruh Track A, QA manual Windows (atau *waiver* tertulis yang sah), dan Gate 2 S12 disetujui Project Lead.
