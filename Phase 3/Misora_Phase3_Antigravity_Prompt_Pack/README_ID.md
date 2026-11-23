# MISORA-EDITOR — PHASE 3 ANTIGRAVITY PROMPT PACK

**Versi:** 1.0  
**Bahasa instruksi AI:** English  
**Panduan penggunaan:** Indonesia  
**Status proyek:** Phase 3 — implementation from the locked canonical ledger. Bukan Phase 2.5.

## 1. Sumber kebenaran dan baseline

Prompt pack ini dibuat berdasarkan:

- Canonical ledger: [Phase_2.5_Canonical_Ledger_LOCKED.md](https://raw.githubusercontent.com/ImaterialC/Misora-Reference/refs/heads/main/Phase_2.5_Canonical_Ledger_LOCKED.md)
- Ledger blob SHA yang dibaca: `e51291724d485eebbe18142f68ecdc4fdf4a7c1b`
- Reference repository HEAD saat paket disusun: `49be42ad6802c6fe200557e6753a3fbf27a11ef9`
- Target repository HEAD yang dipin di ledger dan masih menjadi `main` saat paket disusun: `683724edaf2afac89d2695a80e30a471a0da9195`
- Target: `https://github.com/ImaterialC/Misora-Editor`

**Penting:** Antigravity wajib memeriksa HEAD dan `git status` lokal sebelum bekerja. Jangan menganggap checkout lokal pasti identik dengan GitHub. Jangan reset, clean, checkout paksa, atau menghapus perubahan lokal demi menyesuaikan baseline.

Ledger terkunci adalah kontrak implementasi. Jangan membuka kembali keputusan Project Lead yang sudah dikunci. Bila kode, test, atau fixture membuktikan ledger memiliki kekeliruan faktual, jangan memperbaiki diam-diam: buat discrepancy report dengan bukti dan berhenti pada item terkait.

## 2. Rekomendasi utama

Gunakan **Antigravity App** pada workspace `D:\Misora-Editor` dan mulai dengan `/teamwork` menggunakan prompt di `prompts/00_PHASE3_TEAMWORK_START.md`.

Mengapa Teamwork:
- Phase 3 memiliki banyak milestone dan dependency lintas modul.
- Teamwork secara resmi dirancang untuk proyek repository-scale / multi-milestone.
- Teamwork menyediakan Explorer read-only, Worker, Critic, Challenger, Auditor, dan Success Auditor.
- Teamwork menggunakan project directory terisolasi (`~/teamwork_projects/{PROJECT_NAME}`), jadi sumber asli tidak semestinya langsung ditimpa selama pengerjaan awal.

**Perhatian terhadap workspace Teamwork:** Ia menggunakan folder proyek khusus, bukan otomatis workspace `D:\Misora-Editor`. Prompt utama memerintahkan Antigravity untuk memeriksa repository sumber, status working tree, dan cara membuat snapshot/copy yang aman. Jika working tree dirty atau ada file ignored lokal yang mungkin menjadi fixture, Antigravity harus melaporkan dulu dan tidak boleh menyalin/mengabaikan/menghapusnya secara diam-diam. Setelah pekerjaan, integrasi kembali ke repository utama dilakukan melalui review diff/patch yang eksplisit.

Jangan memakai satu `/goal` untuk mengerjakan seluruh Phase 3. `/goal` tidak memiliki iteration cap dan berisiko menjadi loop panjang. Gunakan milestone Teamwork dengan acceptance gate.

## 3. Pilihan model yang direkomendasikan

Gunakan nama model persis seperti yang tampil di picker akun Anda. Saya tidak mengasumsikan semua model dapat dipilih untuk semua role Teamwork.

| Tugas | Model yang disarankan dari opsi akun Anda | Catatan |
|---|---|---|
| Orchestrator / arsitektur / keputusan P0 | Claude Opus 4.6 | Gunakan untuk menyusun milestone, menilai ambiguity, dan kasus data-integrity sulit. |
| Implementasi per milestone | Claude Sonnet 4.6 | Cocok sebagai default implementer bila model routing per agent tersedia. Tetap wajib tes. |
| Inventaris read-only, grep, dokumentasi, test matrix | Gemini 3.8 Flash Fast | Aman untuk pekerjaan terstruktur dan read-only; jangan jadikan penentu final untuk binary/AST/concurrency. |
| Independent diff review / challenge | GPT-OSS 120B | Pakai sebagai reviewer adversarial yang berbeda dari implementer; bukan satu-satunya sign-off. |

Jika Teamwork tidak menyediakan pemilihan model per role, jangan mengarang kemampuan tersebut. Pakai model yang tersedia, catat keterbatasannya, dan tetap pertahankan Auditor/Challenger serta test nyata.

## 4. Cara menjalankan

1. Ekstrak ZIP ini di luar repository atau di folder referensi yang mudah ditemukan. Jangan menimpa `AGENTS.md` yang sudah ada.
2. Buka `D:\Misora-Editor` sebagai project/workspace di Antigravity App.
3. Pastikan perubahan lokal sudah di-commit atau setidaknya diketahui. Jangan melakukan reset atau clean untuk membuat working tree bersih.
4. Buka `prompts/00_PHASE3_TEAMWORK_START.md`, salin seluruh prompt, lalu tempel ke command composer Antigravity.
5. Gunakan `/teamwork` sesuai instruksi pada file itu. Pilih Claude Opus 4.6 untuk orchestrator bila tersedia.
6. Pada scoping phase Teamwork, pastikan ia menemukan ledger LOCKED yang tepat, mengecek repository lokal, serta mengusulkan milestone A–G. **Jangan approve** jika prompt artifact mengubah keputusan terkunci, menghapus data, menggabungkan milestone, atau melompati P0/P1 gates.
7. Approve Teamwork prompt artifact hanya setelah path copy/worktree dan preservation of local changes dijelaskan dengan benar.
8. Monitor tiap milestone. Jangan melanjutkan milestone dependent saat acceptance gate gagal atau bukti belum tersedia.
9. Setelah setiap milestone, gunakan `/compact` dengan checkpoint khusus milestone (contoh di `prompts/08_COMMAND_ROUTING.md`). Review diff dan hasil test sebelum approval.
10. Integrasikan patch ke `D:\Misora-Editor` hanya setelah diff ditinjau dan Anda menyetujui integrasi. Jangan push ke GitHub otomatis.

## 5. Urutan implementasi

| Urutan | Milestone | Cakupan |
|---|---|---|
| A | Baseline & repository hygiene | HYG-01, baseline/test inventory, canonical ledger traceability |
| B | AST, binary, v2, structural ownership, CSIF | BUG-01..BUG-09 + HYG-04 (BUG-09 fixture-gated) |
| C | Document state, locks, Undo/Redo, mutation transactions | BUG-10..BUG-20 + HYG-02 where relevant |
| D | Search, Replace, project-root correctness | BUG-21..BUG-24 + HYG-05 |
| E | XUAT identity and atomic synchronization | BUG-25..BUG-26 |
| F | MTL threading, lifecycle, security and stabilization | BUG-27..BUG-37 + HYG-06/HYG-07 |
| G | UI fixes and accepted feature slices | BUG-38..BUG-41, FEAT-01..FEAT-14, HYG-03/HYG-08 |

Group G is gated behind stabilization and the dependencies in the canonical ledger. A fixture-gated item may remain BLOCKED without blocking unrelated tasks, but it must never be marked PASS by assumption.

## 6. Strategi command — manfaatkan, bukan memaksakan

Tidak semua command relevan untuk semua pekerjaan. Memasukkan semua slash command ke satu prompt justru menambah ambiguity.

| Command | Dipakai untuk Misora Phase 3 |
|---|---|
| `/teamwork` | Pengelola utama proyek panjang dan milestone A–G. |
| `/plan` | Rencana terstruktur untuk milestone terpisah bila tidak memakai Teamwork atau saat perlu revisi plan. |
| `/boost` | Bug yang sulit/terikat erat: BUG-02, BUG-07, BUG-14, BUG-27, BUG-33. Pakai satu isu per sesi. |
| `/swarm` | Audit/test parallel yang benar-benar terpisah; jangan jalankan nested swarm jika Teamwork sedang membagi worker untuk pekerjaan yang sama. |
| `/run-workflow` | Inventaris berulang / structured read-only checks; simpan script workflow dan hasil JSON. Jangan biarkan banyak worker menulis file yang sama. |
| `/goal` | Hanya untuk satu milestone kecil dengan Done criteria dan stop conditions yang tegas. Bukan seluruh Phase 3. |
| `/compact` | Checkpoint setelah eksplorasi atau milestone. Harus di awal pesan. |
| `/btw` | Pertanyaan sampingan read-only yang tidak perlu masuk konteks utama. |
| `/learn` | Mengubah koreksi yang berulang menjadi Rule/Skill setelah Anda menyetujuinya. |
| `/agy-customizations` | Memuat dokumentasi customization sebelum membuat Rules, Skills, agents, hooks atau MCP config. |
| `/antigravity-guide` | Meminta Antigravity memeriksa dokumentasi resminya saat ada ketidakpastian UI/command. |
| `/browser` | Tidak dipakai untuk menguji UI Tkinter desktop. Gunakan run app/manual Windows GUI test. |
| `/schedule`, `/automation` | Tidak diperlukan untuk coding milestone; hanya dipakai bila Anda memang meminta pengingat/pekerjaan terjadwal. |
| `/generative_ui`, `/mcp-app-development` | Tidak relevan dengan implementasi editor ini; jangan dipaksakan. |
| CLI `/context`, `/agents`, `/tasks`, `/diff`, `/model`, `/effort`, `/permissions`, `/usage` | Monitoring bila Anda memakai `agy` CLI. |

Jangan gunakan CLI headless `agy -p` untuk keseluruhan Phase 3 karena pekerjaan ini membutuhkan review artifacts, approvals, dan pengawasan GUI/test.

## 7. Aman untuk model murah?

Instruksi ini dirancang untuk mengurangi salah tafsir dengan: ledger sebagai otoritas tunggal, path eksplisit, file ownership, no-edit preflight, milestone gates, test evidence, no silent fallback, no automatic commit/push, dan hard STOP conditions.

Namun, **prompt yang presisi tidak membuat model murah setara model reasoning kuat**. Gunakan Flash Fast untuk read-only inventory, test discovery, mapping ID, dan dokumentasi. Jangan serahkan keputusan atau implementasi inti binary parser, v2 codec, AST projection, sparse transaction, undo identity, MTL race, DPAPI, atau XUAT keying hanya kepada Flash/GPT-OSS tanpa review model kuat dan regression tests.

GPT-OSS 120B bisa menjadi reviewer tambahan, tetapi klaim “lulus” harus dibuktikan dengan command output dan independent test, bukan opini model.

## 8. Files

- `prompts/00_PHASE3_TEAMWORK_START.md` — prompt utama yang ditempel pertama kali jika `/teamwork` tersedia.
- `prompts/00B_FALLBACK_WITHOUT_TEAMWORK.md` — jalur alternatif `/plan` + milestone terpisah jika `/teamwork` tidak tersedia.
- `prompts/01_GROUP_A_BASELINE_HYGIENE.md` sampai `07_GROUP_G_UI_FEATURES.md` — prompt milestone jika Anda memilih menjalankan satu grup per sesi.
- `prompts/08_FINAL_ACCEPTANCE_AUDIT.md` — audit final sebelum integrasi.
- `prompts/09_COMMAND_ROUTING.md` — command & model playbook.
- `.agents/rules/misora-phase3-guardrails.md` — optional workspace rule; review dan salin dengan sadar, jangan otomatis menimpa rules yang ada.

Canonical ledger tidak diduplikasi di ZIP untuk menghindari salinan stale. Prompt selalu merujuk ke URL locked ledger dan SHA blob di atas.
