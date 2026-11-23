Saya menyarankan pendekatan **Phase 3 berbasis milestone, dengan Teamwork sebagai pengelola utama dan pengujian independen sebagai gerbang setiap milestone**.

Saya sudah membuat ZIP berisi perintah Antigravity, bukan hanya satu prompt panjang. Paket ini dirancang agar Antigravity memahami bahwa Phase 2.5 sudah selesai dan terkunci, sedangkan Phase 3 adalah tahap implementasi.

**Misora Phase 3 — Antigravity Prompt Pack**

Siap digunakan

# **31 KB**

15 file, seluruh dokumen teks menggunakan UTF-8. Arsip sudah diperiksa integritas ZIP dan validitas encoding-nya.

Download ZIP — Prompt Pack Phase 3

Download prompt utama saja — siap ditempel

## **1. Pendapat saya tentang pendekatan implementasi**

Ledger Gemini yang terkunci memuat 41 BUG, 8 HYG, dan 14 FEAT. Ini bukan pekerjaan yang aman apabila diberikan sebagai satu instruksi sederhana seperti:

> Fix all bugs and implement all features.

Instruksi semacam itu membuka terlalu banyak ruang interpretasi. AI bisa memperbaiki satu masalah tetapi merusak invariant pada bagian lain, mengubah format binary, atau mulai membuat fitur baru sebelum bug dependensinya selesai.

Saya memilih tujuh kelompok pekerjaan:

1. **A — Baseline & Repository Hygiene**

   Audit repository, dokumentasi, jumlah test, dan kondisi awal. HYG-01 menjadi pekerjaan pertama.
2. **B — AST, Binary & Codec**

   BUG-01 sampai BUG-09. Fokus pada keamanan binary parser, v2, command ID, voice cue, multi-segment, dan CSIF.
3. **C — Document State & Undo**

   BUG-10 sampai BUG-20. Fokus pada dirty state, Translation Lock, tab switching, transaksi edit, Undo/Redo dan backup.
4. **D — Search & Replace**

   BUG-21 sampai BUG-24. Fokus pada search matcher, error reporting, project roots, cache dan multi-file Replace.
5. **E — XUAT Integrity**

   BUG-25 sampai BUG-26. Menjaga identitas sumber Jepang dan penulisan dictionary secara atomik.
6. **F — MTL & Application Lifecycle**

   BUG-27 sampai BUG-37. Fokus pada thread safety, stale-result guard, logger, security, dan lifecycle.
7. **G — UI & Accepted Features**

   BUG-38 sampai BUG-41, FEAT-01 sampai FEAT-14 serta hygiene terkait. Dikerjakan setelah dependensi stabilisasi terpenuhi.

Ini mengikuti dependency order yang sudah disepakati di ledger. Terutama, fitur Preview, Import XUAT, MTL Drawer dan Raw Commands tidak boleh mendahului persyaratan integritas yang menjadi dependensinya.

## **2. Mengapa saya memilih&#x20;**`/teamwork`

Rekomendasi utama

Saya memilih `/teamwork` sebagai orchestrator utama Phase 3, bukan `/goal` atau `/swarm`.

Menurut dokumentasi resmi, Teamwork memang ditujukan untuk proyek besar dengan banyak milestone. Ada Explorer untuk riset read-only, Worker untuk implementasi, serta Critic, Challenger, Auditor dan Success Auditor untuk pemeriksaan independen. Teamwork juga menggunakan direktori proyek terisolasi dan file ownership antar-worker.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://antigravity.google\&sz=32)

Google Antigravity Docs



Ada satu hal penting yang harus Anda ketahui:

**Teamwork tidak otomatis bekerja langsung di&#x20;**`D:\Misora-Editor`**.** Dokumentasi menyebutkan adanya dedicated project directory, secara default `~/teamwork_projects/{PROJECT_NAME}`.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://antigravity.google\&sz=32)

Google Antigravity Docs



Justru saya memanfaatkan hal tersebut sebagai pengaman.

Prompt utama memerintahkan Antigravity untuk:

1. Memeriksa repository lokal dan HEAD.
2. Menginspeksi staged, unstaged, untracked dan ignored files.
3. Mengidentifikasi fixture lokal yang mungkin penting.
4. Menjelaskan bagaimana snapshot repository akan dibuat.
5. Berhenti dan meminta persetujuan jika kondisi working tree tidak aman untuk disalin.

Dengan demikian, Teamwork tidak langsung mengacak repository utama. Pekerjaan dilakukan dalam ruang terisolasi, lalu hasil akhirnya disiapkan sebagai diff/patch untuk ditinjau dan diintegrasikan.

**Jangan langsung menyetujui prompt artifact Teamwork** jika ia mengusulkan reset, clean, menghapus file lokal, melewati test, atau mengubah hard guardrail ledger.

## **3. Bagaimana saya memanfaatkan command Antigravity**

Saya tidak memaksakan semua command untuk menjalankan pekerjaan yang sama. Saya memilih command berdasarkan jenis tugasnya.

| Command               | Penggunaan dalam Phase 3                                                                             |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| `/teamwork`           | Orchestrator seluruh milestone A–G.                                                                  |
| `/plan`               | Membuat rencana satu milestone dengan review sebelum editing.                                        |
| `/boost`              | Memecahkan bug sulit seperti AST conversion, sparse CSIF, race condition MTL dan batch cancellation. |
| `/swarm`              | Audit paralel untuk pekerjaan yang benar-benar tidak berbenturan.                                    |
| `/run-workflow`       | Inventaris terstruktur, pemetaan bug ke source/test, dan audit read-only berulang.                   |
| `/goal`               | Satu target final audit dengan Done criteria yang jelas. Bukan seluruh Phase 3.                      |
| `/compact`            | Menyimpan checkpoint setelah setiap milestone.                                                       |
| `/btw`                | Pertanyaan sampingan agar tidak mengotori konteks implementasi.                                      |
| `/learn`              | Menyimpan koreksi berulang sebagai Rule atau Skill setelah disetujui.                                |
| `/agy-customizations` | Memuat panduan customization sebelum mengatur Rules/Skills/hooks.                                    |
| `/antigravity-guide`  | Meminta Antigravity memeriksa dokumentasi resmi.                                                     |

Saya sengaja tidak menggunakan `/browser` untuk pengujian UI utama karena Misora adalah aplikasi desktop Tkinter. Browser subagent bukan pengganti pengujian langsung di Windows. `/automation`, `/generative_ui` dan `/mcp-app-development` juga tidak relevan untuk implementasi ini.

Perbedaan fungsi command tersebut sesuai panduan Antigravity: `/boost` untuk masalah sulit, `/swarm` untuk pekerjaan luas yang dapat dipisahkan, dan `/teamwork` untuk proyek multi-milestone.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://antigravity.google\&sz=32)

Google Antigravity Docs+2



## **4. Apakah prompt ini aman digunakan model murah?**

Pendapat saya: **prompt-nya dibuat cukup ketat untuk mengurangi salah tafsir, tetapi tidak cukup untuk menjamin model murah selalu benar.**

Saya memisahkan tugas berdasarkan risiko:

**Gemini 3.8 Flash Fast**

Aman untuk tugas terbatas

Gunakan untuk inventaris read-only, pencarian referensi, mapping BUG ke file/test, dokumentasi dan audit sederhana.

Jangan jadikan penentu tunggal untuk binary parser, AST identity, transactional CSIF, Undo identity, MTL concurrency, DPAPI dan XUAT source key.

**GPT-OSS 120B**

Reviewer tambahan

Saya akan memakainya untuk mengkritik diff, mencari edge case, dan mempertanyakan apakah test sudah cukup.

Jangan menjadikan opini GPT-OSS sebagai bukti bahwa perubahan benar.

**Claude Sonnet 4.6**

Implementasi terarah

Cocok sebagai implementer untuk satu milestone atau satu kelompok file dengan batas ownership yang jelas.

**Claude Opus 4.6**

Prioritas reasoning

Saya sarankan untuk orchestrator, keputusan arsitektur, audit perubahan berisiko tinggi, dan kasus yang berhubungan dengan integritas data.

Nama model di atas mengikuti daftar yang Anda sampaikan. Saya tidak memasukkan model ID dari contoh lama seperti Gemini 4 Carbon atau Claude Opus 5.5 ke prompt, karena tidak sesuai dengan daftar model yang tersedia di akun Anda. Jika Antigravity tidak dapat melakukan model routing per-worker, prompt meminta AI menyatakan keterbatasan tersebut, bukan berpura-pura sudah mengaturnya.

**Apakah Flash Fast bisa digunakan untuk Phase 3?** Bisa, tetapi jangan untuk memimpin seluruh implementasi. Model murah dapat membantu banyak pekerjaan read-only; untuk bagian yang mengubah representasi binary atau struktur dokumen, biaya kegagalan jauh lebih besar daripada penghematan token.

## **5. Cara menggunakan ZIP**

**Langkah 1 — Ekstrak**

Ekstrak ZIP ke folder referensi di luar repository. Jangan menimpa `AGENTS.md` yang ada.

**Langkah 2 — Buka repository**

Buka `D:\Misora-Editor` di Antigravity App.

**Langkah 3 — Pilih prompt utama**

Buka:

`prompts/00_PHASE3_TEAMWORK_START.md`

Salin seluruh isi prompt dan tempel ke command composer. Prompt dimulai dengan:

```
/teamwork
```

**Langkah 4 — Periksa scoping artifact**

Teamwork akan melewati tahap scoping dan membuat prompt artifact yang harus Anda review sebelum menyetujui eksekusi. Dokumentasi resmi juga menjelaskan bahwa `/plan` menghasilkan Implementation Plan yang dapat diberi komentar dan harus ditinjau sebelum Proceed.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://antigravity.google\&sz=32)

Google Antigravity Docs+1



Pastikan artifact:

- Mengikuti ledger terkunci.
- Tidak membuka kembali keputusan Project Lead.
- Membuat milestone A–G dengan dependency yang benar.
- Tidak menghapus atau mengubah data lokal.
- Tidak langsung mengerjakan semua fitur.

**Langkah 5 — Pantau milestone**

Setelah setiap kelompok selesai, tinjau test output dan diff. Kemudian gunakan `/compact` untuk menyimpan checkpoint sebelum melanjutkan.

Jika `/teamwork` tidak tersedia di menu command, ZIP juga memiliki prompt alternatif `00B_FALLBACK_WITHOUT_TEAMWORK.md` yang menggunakan `/plan` dan milestone terpisah.

## **6. Isi paket**

| File                                        | Fungsi                           |
| ------------------------------------------- | -------------------------------- |
| `00_PHASE3_TEAMWORK_START.md`               | Instruksi utama Teamwork         |
| `00B_FALLBACK_WITHOUT_TEAMWORK.md`          | Jalur alternatif                 |
| `01_GROUP_A...` sampai `07_GROUP_G...`      | Perintah masing-masing milestone |
| `08_FINAL_ACCEPTANCE_AUDIT.md`              | Audit akhir Phase 3              |
| `09_COMMAND_ROUTING.md`                     | Panduan penggunaan command       |
| `.agents/rules/misora-phase3-guardrails.md` | Optional persistent project rule |
| `README_ID.md`                              | Panduan penggunaan Indonesia     |

Rule di dalam ZIP bersifat opsional. Jangan langsung memasangnya dengan menimpa Rules atau AGENTS yang sudah ada. Dokumentasi Antigravity membedakan Rules untuk invariant/constraint dari Skills untuk workflow berulang.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://antigravity.google\&sz=32)

Google Antigravity Docs



## **7. Pendapat akhir saya**

Ada tiga lapisan pengaman yang sengaja saya masukkan ke pendekatan ini:

1. **Specification safety:** locked ledger menjadi kontrak utama. Tidak ada keputusan lama yang ditafsirkan ulang oleh model.
2. **Workspace safety:** tidak mengubah source asli secara membabi buta, tidak menghapus perubahan lokal, dan tidak melakukan commit/push tanpa izin.
3. **Verification safety:** setiap bug harus punya test dan bukti hasil; item yang memerlukan fixture produksi tetap `BLOCKED`, bukan dipaksakan menjadi `PASS`.

Saya tidak akan menyebut prompt ini kebal halusinasi. Tidak ada prompt yang bisa menjamin itu. Tetapi dengan mekanisme berhenti ketika bukti tidak tersedia, pemisahan milestone, serta pemeriksaan oleh model lain dan test nyata, risikonya jauh lebih terkendali.

**Saran saya:** mulai dengan model Claude Opus 4.6 untuk Teamwork scoping. Setelah prompt artifact disetujui, gunakan Sonnet untuk implementasi milestone kecil, Flash untuk eksplorasi read-only, dan GPT-OSS 120B untuk review adversarial. Jangan biarkan model murah menjadi satu-satunya penjaga integritas binary Misora.