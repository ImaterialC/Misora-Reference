# Misora-Reference — Lean Multi-AI Council Kit (Token-Minimal Edition)

Repositori kerja hemat-token untuk rapat Multi-AI (`Misora-Editor` yang sudah besar + kompatibel dengan AI Web gratis seperti DeepSeek).

## Prinsip Hemat Token (Strategi Baru)
1. **English-only untuk semua prompt & hasil AI:** Tidak ada lagi ringkasan 2 bahasa (ID + EN) yang memboroskan ~30–40% token output & *context window*.
2. **Prompt super-ringkas:** Seluruh basa-basi & format hiasan dihapus; hanya menyisakan pagar anti-halusinasi, anti-terpotong, sitasi baris asli, dan pelacakan `U-xx`.
3. **Dua Jalur Audit Phase 1 (sesuai kapasitas AI):**
   - **Jalur A (`P1_Full.md`):** Untuk AI ber-konteks besar + bisa *fetch* GitHub Raw (Gemini, GPT, Qwen, Grok).
   - **Jalur B (`P1_Scoped_Upload.md`):** Untuk AI Web gratis / batas upload ketat (DeepSeek, Claude Free, dll.) — dipecah per **Batch domain** (maks 3–4 file / $\le$150 KB per chat baru).
4. **Folder `tools/` dan `references/` selalu kosong** di awal siklus — isi hanya dengan referensi siklus aktif (termasuk `references/misora_parts/` dari `split_code_for_ai.bat`).

## Struktur Folder
```text
Misora-Reference/
├── README.md
├── USER_WISHLIST.md         # Daftar bug & fitur Project Lead (U-01..U-N)
├── scan_meeting.bat         # Buat MANIFEST_AUTO.md + _BUNDLE aman (<=1500L / 65KB) + salin URL
├── templates/
│   ├── P0_Check.md          # Phase 0: Cek akses & anti-terpotong
│   ├── P1_Full.md           # Phase 1: Riset mandiri (AI full-fetch)
│   ├── P1_Scoped_Upload.md  # Phase 1: Riset per-batch (DeepSeek / AI upload gratis)
│   ├── P2_CrossCheck.md     # Phase 2: Rapat silang & kritik (maks 2-3 ronde)
│   ├── P3_Ledger.md         # Phase 3: Kunci Canonical Ledger (1 Notulen + Auditor)
│   ├── P4_Drafts.md         # Phase 4: Peta sesi + 2 Exemplar (bukan full ZIP)
│   ├── P5_KitAudit.md       # Phase 5: 1 Penyusun Tunggal + Korektor Spesialis
│   ├── P6_Execution.md      # Phase 6: Review Plan & Walkthrough Antigravity
│   └── P_LateJoin.md        # AI masuk di tengah phase (cek singkat + langsung loncat)
├── tools/                   # (Kosong)
├── references/              # (Kosong — taruh misora_parts/ di sini saat siklus aktif)
└── Phase_0_Baseline/ .. Phase_6_Execution/
```

## Pembagian Batch Ideal untuk DeepSeek / AI Upload Gratis (`P1_Scoped_Upload.md`)
Buka **chat baru** per batch (unggah maks 3–4 file, total $\le$150 KB):
- **Batch A (AST/Codec):** `AGENTS.md` + `core/story_ast.py` + `core/script_codec.py` + `core/bundle_io.py`
- **Batch B (Search/XUAT/Undo):** `AGENTS.md` + `core/search_engine.py` + `core/xunity_sync.py` + `core/undo_journal.py` + `core/text_encoding.py`
- **Batch C (MTL/Sec/Log):** `AGENTS.md` + `core/mtl_engine.py` + `core/security.py` + `core/logger.py` + `core/ngui_tags.py`
- **Batch D1..Dn (`misora.py`):** `AGENTS.md` + `00_INDEX_misora.md` + maks 2 file `misora_partXX.py` yang relevan dengan `USER_WISHLIST.md`.
- Simpan hasilnya sebagai `P1_DS_BatchA.md`, `P1_DS_BatchB.md`, dst. di `Phase_1_Research/` lalu jalankan `scan_meeting.bat`.
