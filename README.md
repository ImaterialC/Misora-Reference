# Misora-Reference — Multi-AI Engineering Council Workspace (Clean Cycle Template)

Repositori ini berfungsi sebagai **ruang rapat & indeks artefak** untuk siklus diskusi Multi-AI (Gemini, GPT, Claude, Qwen, Grok) sebelum eksekusi di Google Antigravity.

> **Prinsip Kebersihan:**
> - Rencana implementasi & *changelog* resmi milik kode berada di repositori proyek (`Misora-Editor`).
> - Folder `tools/` dan `references/` sengaja dikosongkan setiap siklus baru — isi **hanya** dengan referensi yang relevan untuk debat siklus saat ini.
> - **Jangan gunakan spasi** pada nama folder/file agar Raw URL GitHub tetap bersih (tanpa `%20`).

---

## Struktur Folder Standar

```text
Misora-Reference/
├── README.md                 # Panduan ini
├── USER_WISHLIST.md          # Daftar bug, keluhan, dan fitur keinginan Project Lead (U-01..U-N)
├── scan_meeting.bat          # Scanner otomatis: buat MANIFEST_AUTO.md + _BUNDLE aman + salin URL ke Clipboard
├── templates/                # Prompt standar Phase 0 s.d. Phase 6 + Late-Join (AI masuk di tengah rapat)
├── tools/                    # (Kosong) Isi dengan skrip/alat referensi khusus siklus ini saja
├── references/               # (Kosong) Isi dengan gambar/contoh data/log khusus siklus ini saja
├── Phase_0_Baseline/         # Bukti akses & baseline SHA dari semua AI
├── Phase_1_Research/         # Dossier riset mandiri (P1_Gemini.md, P1_GPT.md, P1_Qwen.md, P1_Grok.md)
├── Phase_2_CrossCheck/       # Rapat silang & kritik temuan (P2R1_..., P2R2_...)
├── Phase_3_Ledger/           # Canonical Ledger terkunci (100% cakupan ID + grafik dependensi)
├── Phase_4_Drafts/           # Draft arsitektur perintah (Aturan 2-Exemplar: peta sesi + 2 contoh prompt)
├── Phase_5_KitAudit/         # 1 Paket ZIP final dari Sole Compiler + audit byte/hash korektor
└── Phase_6_Execution/        # Catatan feedback/temuan penting selama eksekusi Antigravity (opsional)
```

## Konvensi Penamaan File (Anti-Tertukar)
- Phase 1: `P1_Gemini.md`, `P1_GPT.md`, `P1_Claude.md`, `P1_Qwen.md`, `P1_Grok.md`
- Phase 2: `P2R1_GPT.md`, `P2R2_Qwen2Gemini.md`
- Phase 3: `Phase_3_Canonical_Ledger_LOCKED.md`
- Phase 5: `Phase_5_Antigravity_Kit_v1.zip`, `P5R1_QwenAudit.md`

## Alur Cepat Menggunakan `scan_meeting.bat`
1. Simpan laporan AI ke folder phase yang sesuai (mis. `Phase_1_Research/`).
2. Klik 2x `scan_meeting.bat` (atau *drag-and-drop* folder phase ke atas `scan_meeting.bat`).
3. Pilih buat bundle anti-terpotong (`_BUNDLE_*.md`, default maks **1500 baris / 65 KB** per bagian).
4. `git add . && git commit -m "Phase X update" && git push`.
5. Daftar Raw URL + SHA-256 sudah otomatis ada di Clipboard Windows — tinggal **`Ctrl+V`** ke semua AI!
