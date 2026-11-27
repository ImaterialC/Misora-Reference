# Ringkasan Indonesia — Misora ENV-01

## Keputusan yang sedang berlaku

Menurut laporan Project Lead, S11e `v1.4.15` sudah di-commit lokal dan belum di-push. SHA terakhir yang tersedia dari transcript adalah `ead65077a2a6cf3a664543cfb50f855268a29e2a`. Status working tree setelah commit belum ditampilkan, jadi tetap periksa `git status --short`.

Tiga AI dilaporkan sepakat menunda S12, membatalkan/menangguhkan rencana rilis `v1.5.0` dan rencana S15 yang dimaksud dalam keputusan baru, lalu memprioritaskan ENV-01. Saya setuju dengan arah tersebut.

Catatan: Project State lama memiliki catatan historis milestone bernama S15 yang sudah selesai. Jangan menghapus atau mengganti catatan lama itu sebelum Project Lead memperjelas apakah “S15” yang dibatalkan adalah rencana baru yang berbeda.

## Mengapa ENV-01 penting

Masalah yang Anda sebut nyata secara engineering: agent membaca file yang terlalu besar sebelum tahu tugasnya. Akibatnya sejarah, status lama, aturan permanen, keputusan yang sudah diganti, dan backlog tercampur. Ini meningkatkan risiko agent mengambil keputusan dari konteks yang tidak lagi berlaku.

Snapshot publik yang saya baca menunjukkan:
- `AGENTS.md`: sekitar 10.7 KB.
- `PROJECT_STATE.md`: sekitar 223.6 KB dan 1.631 baris.
- `misora.py`: sekitar 1.03 MB.

Angka publik ini bukan pengukuran pasti working tree lokal yang belum di-push.

## Pendapat saya tentang T-01..T-14

Daftar Gemini/Project Lead berguna, tetapi bukan 14 bug. Isinya campuran:
- Bug yang perlu direproduksi: T-01, T-03, T-04; T-02 kemungkinan koreksi kecil.
- UX/config change: T-05, T-06, T-07.
- UI redesign dan interaction proposal: T-08, T-09, T-10.
- Fitur/infrastruktur besar: T-11, T-12, T-13, T-14.

Urutan yang saya sarankan: T-01 dahulu, kemudian T-03 dan T-04, setelah itu T-02. T-05/T-06 perlu design spec. T-07 jangan menjadi tooltip di semua tempat tanpa inventaris. T-08 sampai T-10 butuh mockup dan kontrak interaction. T-11 sampai T-14 sebaiknya menjadi track terpisah.

### Catatan paling penting per temuan

- **T-01:** prioritas pertama. Jangan menebak root cause. Periksa pack manager (`winfo_manager`) dan mapped state (`winfo_ismapped`) ketika 0, 1, dan 2 dokumen terbuka.
- **T-02:** cari string tooltip aktual. Ganti hanya teks yang masih memakai 50x3, cocokkan dengan kontrak 54d × 3.
- **T-03:** pisahkan active card, current box, selection set, dan selection anchor. Pin/jump seharusnya tidak memilih semua card secara tidak sengaja.
- **T-04:** pastikan satu sumber kebenaran overflow. Aturan proyek menyebut 54 digit-width atau 4+ baris; jangan menghitung soft-wrap seolah-olah newline eksplisit tanpa keputusan desain.
- **T-05:** desain model path yang mendukung berbagai framework/plugin dan input manual; jangan mengunci ke BepInEx. Pisahkan Game Folder, RedirectedResources, dan text dictionary folder.
- **T-06:** direktori terakhir Save Project dan Save/Patch Bundle sebaiknya diingat terpisah.
- **T-07:** tooltip selektif saja. Semua elemen tidak perlu tooltip.
- **T-08:** redesign ribbon besar; mockup/responsive layout lebih dahulu.
- **T-09:** audit overlap dengan S11e karena chooser BoxInsert/BoxReplace dan trio seleksi sudah dilaporkan ada. Jangan membuat kontrol duplikat.
- **T-10:** definisikan Ctrl/Shift range selection dan anchor; ukur dampak pada virtualized card pool.
- **T-11:** istilah “Master Undo permanen” kurang tepat. Lebih baik “Original Source Snapshot” yang immutable, terpisah dari Undo Journal dan punya persistence/recovery design.
- **T-12:** async XUAT dapat memperbaiki respons UI, tetapi butuh immutable snapshot, freshness check, atomic writes, cancellation dan partial failure handling. Jangan menjanjikan 0 ms.
- **T-13:** desain backup perlu manifest, fingerprint sumber, encoding/newline, collision-safe naming, retention, preview dan restore test.
- **T-14:** CI artifact/exe ditunda sampai strategi distribusi, dependency packaging, signing/checksum dan rollback jelas.

## Apa yang harus Anda lakukan

1. **Jangan mulai S12.** Release `v1.5.0` tetap HOLD dan tidak ada version promotion.
2. Jalankan preflight lokal: branch, HEAD, `git status --short`, log terakhir, ukuran file aktual.
3. Setujui scope ENV-01 hanya dokumentasi dan tool pembuat symbol index. Jangan sentuh product source/tests/assets/config/backups pada tahap ini.
4. Arsipkan versi penuh `AGENTS.md` dan `PROJECT_STATE.md` sebelum mengganti root files. Jangan menghapus sejarah.
5. Buat migration matrix untuk setiap ID, keputusan, invariant dan test: lokasi lama → lokasi baru → status ACTIVE/SUPERSEDED/DEFERRED/RETRACTED.
6. Audit T-01..T-14 sebagai triage terpisah. Minta reproduksi dan source/test evidence sebelum memberi status CONFIRMED.
7. Uji environment baru dengan Gemini, ChatGPT, Qwen dan Antigravity menggunakan task read-only yang sama. Bandingkan akurasi, bukan hanya jumlah token.

## Target hasil ENV-01

- `AGENTS.md`: sekitar 3–5 KB, aturan permanen saja.
- `PROJECT_STATE.md`: sekitar 8–15 KB, kondisi terkini saja.
- `CONTEXT_ROUTER.md`: mengarahkan agent ke referensi sesuai domain.
- `DECISION_REGISTER.md`: keputusan aktif, bukan transcript.
- `OPEN_ISSUES.md`: bug yang masih terbuka dan bukti/statusnya.
- `docs/history/`: semua sejarah tetap ada tetapi tidak dimuat otomatis.
- Symbol index untuk `misora.py`: class/method, line span, caller dan test terkait; dihasilkan dari source pada HEAD tertentu.

## Pendapat akhir

Saya mendukung fokus ENV-01 sebelum triage besar dan sebelum release gate. Ini bukan sekadar merapikan Markdown. Ini membangun sistem kerja AI yang mencegah konteks lama mengambil alih keputusan baru.

Jangan minta AI meringkas 250 KB lalu mengganti file lama. Audit dan klasifikasikan seluruh isi lebih dulu, arsipkan sumber asli, validasi setiap invariant dengan source/test, kemudian bangun dashboard kecil. Kecepatan hanya berguna kalau akurasinya tetap terjaga.
