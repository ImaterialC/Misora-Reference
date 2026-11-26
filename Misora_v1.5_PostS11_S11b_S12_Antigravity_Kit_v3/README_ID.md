# Misora: Story Editor — Paket Prompt Antigravity Post-S11 (`S11b`–`S12`, Kit v3)

Paket ini berisi 5 prompt eksekusi lengkap **`S11b` (`v1.4.11`)** s.d. **`S12` (`<final_pre_s12>` → kondisional `v1.5.0`)** yang telah menyertakan **seluruh koreksi terakhir dari Qwen (`C-1`, `C-2`) dan ChatGPT (`#1`, `#2`, `#3`)** atas Kit v2, tanpa mengubah kode sumber produksi apa pun.

## Isi Paket
- `prompts/S11b_v1.4.11_XUAT_Scanner_Save_Preview.txt` — **SIAP REVIEW FINAL:** Mengunci semantik `entry_count`/`entries_read` (tanpa menghapus entri dari `_exact_map`/`_value_map`/`entries`, audit caller `len(idx)`/`bool(idx)`), definisi operasional `files_scanned == len(files_indexed) + len(skipped_files)` (termasuk uji *simulated read failure*), resolver ketat `Translation\en\Text`, `Q-02` profiling + STOP Gate A + `Ctrl+S` Save Project, `Q-04` jujur, `Q-18` STOP Gate B, dan `Q-23` Preview tanpa blok merah.
- `prompts/S11c_v1.4.12_Unified_Quick_Edit.txt` — Utuh dari v2 (`Q-22` eksklusif).
- `prompts/S11d_v1.4.13_Import_UX_Productivity.txt` — Utuh dari v2 (`Q-06`–`Q-12`, termasuk impor Synopsis saat Box 0 `summary` kosong).
- `prompts/S11e_v1.4.14_UI_Polish_Icons_Menu_Tooltips.txt` — Diperbaiki ke path kanonik `assets/splash.py` + penambahan `assets/icon.py` (*load-time resizing* tanpa menimpa PNG sumber di `assets/icons/`).
- `prompts/S12_v1.5.0_Final_Audit_Release_Gate.txt` — Diperbaiki ke path kanonik `assets/splash.py`, `assets.splash._VERSION`, `compileall` bersih tanpa argumen `splash.py` kosong, Pre-S12 baseline run, dan 2-Gate terpisah.
- `CHANGE_SUMMARY_FOR_REVIEWERS.md` — Ringkasan persis koreksi Kit v3 (Qwen C-1/C-2 & GPT #1/#2/#3).
- `ROADMAP_RECONCILED_v5.md` — Roadmap terkunci v5 tersinkronisasi.
- `SHA256SUMS.txt` — Manifest hash SHA-256 & ukuran byte seluruh berkas.

## Batas Eksekusi
- **Belum ada izin `/plan` atau implementasi kode sumber** sebelum S11b mendapat konfirmasi review final.
- **`v1.5.0` tetap ON HOLD** sampai Track A, Manual Windows QA (atau *waiver* tertulis), dan Gate 2 S12 disetujui Project Lead.
