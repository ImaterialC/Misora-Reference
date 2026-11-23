# Panduan Paket Perbaikan Misora Reference

Paket ini berisi pengganti beberapa dokumen dan file aturan repository `Misora-Reference`. Isinya menata ulang workflow rapat AI, roster model, peran sekretaris, dan perlindungan file lokal.

## Cara memakai paket

1. Buat salinan cadangan repository `Misora-Reference` atau buat branch baru terlebih dahulu. Anda dapat menyalin isi `INSTALL_REPAIR_PACK_PROMPT.md` ke Antigravity setelah paket diekstrak.
2. Ekstrak isi ZIP ini ke folder root `Misora-Reference` (folder yang berisi `README.md`, `tools/`, dan `extractor_prototype/`).
3. Izinkan file dengan nama sama ditimpa. Folder `templates/` dan file `AGENTS.md`, `.gitignore` adalah tambahan baru.
4. Jangan masukkan `master.db` ke ZIP maupun Git. Paket ini tidak berisi database.
5. Setelah file ditimpa, buka repository dengan Antigravity dan minta agent memeriksa `git status`, memastikan file yang berubah hanya sesuai daftar, dan memeriksa file `.pyc` yang sudah terlanjur tracked. `.gitignore` tidak otomatis menghapus file yang sudah pernah masuk Git.
6. Untuk `.pyc` yang sudah tracked, jangan jalankan `git clean`. Minta agent memeriksa file spesifik `tests/__pycache__/test_extractor_prototype.cpython-312.pyc`, lalu usulkan penghapusan hanya dari Git index (misalnya `git rm --cached -- <path>`) setelah memastikan file itu memang masih tracked. Review diff sebelum commit.

## File yang diganti

- `README.md`
- `INSTANT_ONBOARDING_PROMPT.md`
- `SECRETARY_PLAYBOOK.md`
- `plan_multi_ai_workflow_and_db_strategy.md`
- `plan_multi_ai_roster_and_workflow_strategy.md`

## File baru

- `INSTALL_REPAIR_PACK_PROMPT.md` — instruksi siap-tempel untuk Antigravity agar menerapkan paket secara aman tanpa mengubah kode aplikasi.

- `AGENTS.md` — aturan permanen untuk AI agent di repository referensi.
- `.gitignore` — mengabaikan database lokal, cache Python, temporary files, log, dan asset Unity.
- `templates/DEBATE_BRIEF_TEMPLATE.md` — template memulai rapat.
- `templates/AI_REVIEW_TEMPLATE.md` — template hasil review independen.
- `templates/DECISION_RECORD_TEMPLATE.md` — template keputusan dan dissent.
- `templates/IMPLEMENTATION_BRIEF_TEMPLATE.md` — template prompt implementasi yang dibatasi.

## Apa yang sengaja tidak saya ubah

- `tools/secretary.py`: script yang ada tetap dipertahankan. Dokumen baru menjelaskan command yang benar-benar tersedia, bukan mengklaim command baru sudah dibuat.
- `master.db`: tidak diunduh, tidak disalin, dan tidak dihapus.
- `Misora-Editor`: tidak ada source code aplikasi yang diubah.
- Riwayat debat dan arsip: tidak dihapus atau ditulis ulang.

## Rekomendasi setelah pemasangan

Mulai dengan membaca `SECRETARY_PLAYBOOK.md` dan `plan_multi_ai_workflow_and_db_strategy.md`. Untuk rapat berikutnya, salin template di `templates/`. Jangan meminta semua AI menyetujui satu jawaban; minta bukti, catat perbedaan pendapat, dan biarkan pemilik proyek mengambil keputusan.

## Catatan audit

Audit repository dan riset produk dilakukan pada 23 November 2026. Katalog model, paket gratis, dan command Antigravity dapat berubah; dokumen roster mencantumkan sumber resmi dan tanggal snapshot. Lakukan pengecekan ulang sebelum membuat keputusan berdasarkan model atau kuota.
