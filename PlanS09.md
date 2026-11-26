# MISORA: STORY EDITOR — MASTER SPECIFICATION & POST-S08 REKAPITULASI (`U-01` s.d. `U-20`)

**Status Baseline:** `v1.4.7` (S08 Release Gate Hold — 8/8 *stress test* lulus, 413 tes ditemukan, 0 regresi; `storydata_1001005.unity3d` masih *fixture-BLOCKED*).

**Kebijakan Rilis:** Promosi ke **`v1.5.0` ditunda**. Seluruh item di dokumen ini diselesaikan bertahap melalui sesi **`S09`–`S11**`, dan **`v1.5.0`** ditetapkan sebagai **tahap akhir pembersihan bug, *dead code*, serta audit *memory leak*** menyeluruh.

---

## 1. Hasil Uji Manual Windows (`v1.4.7`) — Ringkasan Status

| # | Area Uji Manual | Status | Temuan Terkait |
| --- | --- | --- | --- |
| 1 | Ribbon Cut & Cut Box | **Ragu / Normal** | Fungsi tetap berjalan normal, tidak ditemukan masalah saat uji. |
| 2 | Native Paste Box (`Insert` / `Replace`) | **Confirmed + Issue** | Berfungsi, tetapi terasa berat saat *paste* di *All Script* (142 box) dan gagal mendeteksi jumlah box terpilih di mode *Dialogue* (`U-01`). |
| 3 | *All Script* & *Preview* | **Needs Redesign** | Dekorasi/background jendela oke, tetapi sorotan box aktif tidak terlihat (`U-04`), *All Script Preview* berantakan (`U-05`), Box 0 ikut terpotong (`U-17`), dan panah `▼` hilang di *Dialogue Preview* (`U-19`). |
| 4 | Font, Ruler, & Line Numbers | **OK + Recalibrate** | Berjalan baik, namun batas asli in-game terverifikasi **54 digit** (`U-07`) dan Box 0 harus kebal spidol merah (`U-18`). |
| 5 | DPI & Left/Right Drawer | **PASS** | Sejauh ini berjalan baik. |
| 6 | Speaker Jump & Autocomplete | **Bug Found** | Tombol pin `📌` tidak lompat ke aktor sama berikutnya (`U-02`); kotak autocomplete melayang di pojok kiri atas layar `(0, 0)` di luar jendela saat klik pertama (`U-06`).

 |
| 7 | Win32 Console Toggle (`F12`) | **DROP / REMOVE** | Di Windows 11 Terminal hanya meminimalkan, tidak menghilangkan konsol — **hapus total fitur ini (`RM-01`)**. |
| 8 | Auto Word Wrap | **PASS** | Berfungsi baik (perlu penyesuaian target lebar ke `54d` sesuai `U-07` & pengecualian Box 0 sesuai `U-18`). |
| 9 | Import XUAT & Archiving | **Critical Hang + UX** | *Hang* sebelum jendela cleanup muncul (`U-08`), alur checkbox arsip terbalik (`U-09`), penamaan (`U-10`), nama karakter masuk arsip meski tidak dicentang (`U-11`), butuh *unified loading bar* (`U-12`, `U-13`), dan struktur Import 1-baris tanpa Box 0 (`U-14`). |

---

## 2. Daftar Lengkap Spesifikasi (`U-01` – `U-20` & `RM-01`)

### A. Perbaikan Bug Inti, Kalibrasi `54d`, Preview, & Penghapusan Fitur

| ID | Kategori | Spesifikasi & Perilaku yang Diinginkan | Bukti / Catatan |
| --- | --- | --- | --- |
| **`U-01`** | Bug (P1) | **Native Paste (`Ctrl+Alt+V`) di mode *Dialogue*** wajib mendeteksi jumlah box terpilih (`_selected_boxes`) dengan benar saat memilih `Insert` vs `Replace`. | Saat ini gagal mendeteksi jumlah box terpilih di mode *Dialogue*. |
| **`U-02`** | Bug / UX (P1) | **Tombol Pin Speaker (`📌`)** harus berfungsi melompat ke dialog berikutnya/sebelumnya dari **aktor/speaker yang sama** (saat `📌` aktif dan user klik `Next` / `Prev`, atau saat mekanisme pin dipicu), disertai feedback posisi kemunculan. | Saat ini tombol pin tidak melompatkan kursor ke aktor sama berikutnya. |
| **`U-06`** | Bug (P1) | **Perbaiki posisi *popup* Speaker Autocomplete:** saat kolom Speaker diklik pertama kali sebelum mengetik apa pun, *popup* tidak boleh muncul di pojok kiri atas monitor `(0, 0)` di luar jendela Misora. | Terkonfirmasi visual di `image_b6e902.png` (kotak putih `ヒヨリ` melayang di atas Notepad++).

 |
| **`U-07`** | Kalibrasi (P1) | **Ubah batas maksimum horizontal dari `50d` menjadi `54d`:** hasil verifikasi in-game menunjukkan batas aman adalah **54 digit**, dan auto-resize baru aktif saat menyentuh **55** (~75–80%). Jadikan satu konstanta tunggal untuk Ruler (`54d | >54d`), indikator header (`N/54d · M/3L`), spidol merah editor, *Dialogue Preview*, dan *Auto Word Wrap*. | Batas vertikal tetap **3 baris** (baris ke-4+ overflow). |
| **`U-18`** | Bug / Rule (P1) | **Box 0 wajib 100% kebal terhadap spidol merah / peringatan overflow** (baik horizontal maupun vertikal, di *Dialogue*, *All Script*, indikator header, dan *Auto Word Wrap*), karena perhitungan panjang karakter Box 0 berbeda dari kotak dialog. | Mencegah *false positive* merah pada sinopsis/metadata Box 0. |
| **`U-19`** | Bug Visual (P2) | **Kembalikan panah bawah pink (`▼`) pada *Dialogue Preview*:** pastikan panah `▼` di pojok kanan bawah kapsul emas terlihat penuh dan tajam, tidak tertutup widget `txt_dialogue_preview` maupun memotong bingkai emas kanan. | Terkonfirmasi visual di `image_b84a7e.png` (ujung pink nyaris tak terlihat & bingkai kanan terpotong latar teks).

 |
| **`RM-01`** | Removal | **Hapus total opsi Windows Console Visibility** (`Debug > Show / Hide Windows Console`, variabel/state konsol terkait, dan pintasan `F12`) beserta kode/tes terkaitnya. | Di Windows Terminal hanya meminimalkan jendela, bukan menyembunyikan total. |

---

### B. *All Script* Redesign, Tab `Quick Edit`, & Performa

| ID | Kategori | Spesifikasi & Perilaku yang Diinginkan | Bukti / Catatan |
| --- | --- | --- | --- |
| **`U-03`** | Feature (P1) | **Tab `Quick Edit` di panel bawah (sebelah `Raw Commands`) khusus untuk mengedit dari mode *All Script*:** saat penerjemah memilih box di *All Script*, kotak edit sederhana ini otomatis menyorot/memuat isi box aktif dan mendukung ***live edit*** (perubahan langsung terlihat di *All Script* secara *in-place* tanpa *re-render* penuh). **Sifat kotak:** polos, sederhana, **tanpa ruler, tanpa perhitungan karakter, tanpa spidol merah, tanpa dekorasi/efek NGUI, dan tidak terpengaruh mode Preview** (karena ruler & visual sudah ada di jendela atas). | Menghilangkan kewajiban pindah ke mode *Dialogue* untuk mengedit teks, sambil menjaga *All Script* tetap *read-only* & anti-hang. (Nama tab bawah `Raw Commands` tetap dipertahankan di sebelahnya.)

 |
| **`U-04`** | UX (P1) | **Sorotan / Highlight Box Aktif di *All Script*:** ketika satu box diklik/dipilih, harus ada penanda visual yang kontras dan jelas (warna latar sorotan dan/atau marker aktif pada header box) sehingga langsung terlihat box mana yang sedang disorot. | Terkonfirmasi di `image_b6e902.png` (Box `#019` tampak identik dengan `#018` dan `#020`).

 |
| **`U-05`** | Redesign (P1) | **Hapus mode *All Script Preview* (tombol `Preview` hanya untuk mode *Dialogue*):** karena tampilan *All Script Preview* saat ini buruk dan *All Script* sendiri *read-only*, satukan menjadi **1 tampilan *All Script* tunggal yang bersih dan rapi**. | Terkonfirmasi di `image_b85165.jpg` (cap atas/bawah terputus dan garis titik-titik berantakan).

 |
| **`U-15`** | Perf Reference | **Optimasi performa *All Script* (termasuk saat Paste di 142+ box):** jendela *Import from XUAT* memiliki 2× jumlah kotak dengan konsep tampilan serupa tetapi terbuka jauh lebih cepat dan lebih disukai tampilannya; gunakan prinsip keringanan yang sama agar *All Script* tidak terasa berat (benchmark S08 sebelumnya `1436.37 ms` untuk 150 box).

 | Menghilangkan beban render ulang penuh & gambar Pillow *cap* berlebih per box. |
| **`U-17`** | UX (P2) | **Box 0 di *All Script* tampil biasa:** tampilkan sebagai blok metadata/sinopsis normal (bukan dipaksa masuk bentuk kartu dialog `54×3` yang memotong teks sinopsis). | Terlihat terpotong di tepi kanan pada `image_b85165.jpg`.

 |
| **`U-20`** | Redesign (P1) | **Tampilan kartu *All Script* mengacu `Expectasi2.jpg` + pilihan Opsi A:** (1) Header di atas kotak `[ ] 🔓 ◆ [BOX #NNN] Speaker [N segs]` **tanpa ikon suara** dan **tanpa garis `----------**`; (2) **Tidak ada spidol merah** di *All Script* (spidol merah khusus di *Dialogue Editor* saja); (3) **Tinggi tetap 3 baris** — baris ke-4+ tertutup di dalam kotak (penerjemah sorot & *scroll* tanpa *scrollbar* terlihat); (4) **Lebar `54d**` — teks `>54d` idealnya tembus ke kanan jika memungkinkan secara teknis, atau bila tidak memungkinkan maka terpotong/masuk ke dalam kotak dan menghilang seperti *textbox* UI konstan pada umumnya.

 | Wajib diverifikasi mekanisme widget Tkinter-nya (lihat Bagian 4 — Diskusi Teknis untuk AI). |

---

### C. `Import from XUAT`, `XUAT Translation Archiving`, & Unified Loading Bar

| ID | Kategori | Spesifikasi & Perilaku yang Diinginkan | Bukti / Catatan |
| --- | --- | --- | --- |
| **`U-08`** | Bug (P0) | **Atasi *Hang* saat membuka jendela Archiving pasca-Import:** memindahkan pemindaian kandidat arsip ke *background thread* dan mengganti daftar ratusan widget `tk.Checkbutton` berat dengan tampilan daftar ringan agar UI tidak pernah membeku. | Terjadi *hang* tepat sebelum jendela *Import Complete / Clean up* muncul. |
| **`U-09`** | UX / Safety (P1) | **Pindahkan kontrol *Archive* ke dalam jendela `Import from XUAT` (sebelum Apply):** tambahkan *checkbox* **`Archive the XUAT translation`** dengan **default TERCENTANG (`True`)**, dilengkapi peringatan jelas tentang risiko bila tidak dicentang. Jika dicentang → lanjut membuka *XUAT Translation Archiving* setelah Import; jika tidak dicentang → selesai langsung tanpa membuka jendela Archiving. | Membalik alur lama yang keliru (opsi skip baru muncul setelah masuk jendela archiving). |
| **`U-10`** | Naming (P2) | **Ganti judul/label** `"Import Complete — Clean up / Archive"` menjadi **`XUAT Translation Archiving`**. | Lebih jelas, konsisten, dan tidak membingungkan. |
| **`U-11`** | Bug (P1) | **Perbaiki kebocoran nama karakter ke daftar Archiving:** nama aktor/speaker tidak boleh diam-diam ikut masuk ke daftar pembersihan/pengarsipan XUAT (terutama saat tidak dipilih, dan secara desain kamus nama karakter bersifat global lintas cerita). | Sebelumnya nama tetap masuk daftar arsip meski `Include Name` tidak dicentang, sekaligus memperparah *hang*. |
| **`U-12`** | UX (P1) | **Tambahkan indikator *loading bar* saat proses pemindaian *XUAT Translation Archiving*** sehingga pengguna tahu program sedang memindai, bukan *hang*. | Operasi pemindaian indeks XUAT analog dengan *Search*. |
| **`U-13`** | UX / Arch (P1) | **Tambahkan *loading bar* pada `Reload XUAT Translations` dan satukan seluruh *loading bar* operasi pencarian/pemindaian menjadi 1 lokasi terpadu** (mis. satu *unified progress bar* di *status bar* bawah dengan label status tugas aktif: *Project Search*, *Reload XUAT*, *XUAT Archiving Scan*). | Menghindari duplikasi *progress bar* dan memberi sinyal kerja yang konsisten. |
| **`U-14`** | Redesign (P1) | **Struktur baru jendela `Import from XUAT`:** (1) **Hapus *checkbox* `Include Actor**`; (2) Tampilkan entri khusus berbentuk **kotak tetap 1 baris (`1 × 50`, *read-only* berpasangan kiri/kanan)** untuk setiap **Nama Aktor/Speaker unik**, **Title**, dan **Subtitle**; (3) **Tidak ada `Box 0**` di dalam daftar Import. | Mengubah impor nama/judul dari sakelar global buta menjadi peninjauan 1-baris per item yang transparan & bisa di-*skip* / pilih duplikatnya. |

---

### D. MTL Drawer

| ID | Kategori | Spesifikasi & Perilaku yang Diinginkan | Bukti / Catatan |
| --- | --- | --- | --- |
| **`U-16`** | UX (P2) | **Pindahkan tombol Apply (`←`) di kartu MTL Drawer ke sebelah kiri SEBELUM nama engine MTL** (contoh: `[←] Google Translate ... [↻]`), bukan di sisi kanan. | Lebih ergonomis karena *MTL Drawer* berada di sisi kanan editor (tombol `←` menempel langsung ke tepi kiri menuju kotak dialog). |

---

## 3. Invarian Keras yang Tetap Terkunci (Untuk Semua AI & Antigravity)

Seluruh perubahan `S09`–`S12` **WAJIB** menjaga aturan dasar berikut tanpa pengecualian:

* **Binary & AST Safety:** Pertahankan `cmd_id == 35` (narration) dan `cmd_id == 32` (subtitle) tidak berubah; jangan gabungkan kotak narasi bersebelahan saat menghapus speaker; pertahankan *multi-segment* & `BoxSnapshot` *lossless*.


* **Panel & Workspace Contracts:** Nama panel bawah tetap **`Raw Commands`** (tab `Quick Edit` berada di sebelahnya, tidak menghapus/mengganti nama `Raw Commands`); `.misora` v1 hanya menyimpan referensi + state + kunci gembok stabil (tanpa *draft* / *blob*).


* **Thread Safety & Atomicity:** Worker thread (Search, Reload XUAT, XUAT Archiving Scan, MTL) **dilarang keras** memanggil method Tkinter secara langsung — wajib via *queue* ke *main thread*; seluruh modifikasi file XUAT tetap transaksional dengan SHA-256 *stale guard* dan *archive-first*.


* **Translation Lock:** Wajib ditegakkan di lapisan model/aplikasi (termasuk di `Quick Edit`, `Paste Box`, `Auto Word Wrap`, dan `Import from XUAT`).


* **Aset & Lisensi:** Nol aset berhak cipta (`AtlasAdv`); *Dialogue Preview* tetap *clean-room* (Pillow / Tk primitives).



---

## 4. Poin Diskusi Teknis untuk Review AI Lain (Sebelum Mengunci Prompt `S09+`)

Agar diskusi lintas-AI (GPT / Claude / Qwen) langsung tajam tanpa mengulang keputusan yang sudah final, berikut **4 pertanyaan arsitektur sempit** untuk ditinjau bersama:

1. **Mekanisme Widget `U-20` (*All Script* 3-Baris Tertutup + Focus-Scroll vs Opsi A):**
* *Konflik mekanis Tkinter:* 1 `tk.Text` tunggal tidak bisa meng-clip baris ke-4+ dan memberi *focus-scroll* independen per box.
* *Pertanyaan untuk AI lain:* Mana yang paling optimal untuk 150–300 box di Windows/Tk 8.6 tanpa *hang* saat Paste:
* **(a) Virtualized Read-Only Card Pool** (~12–15 widget `tk.Text(height=3, wrap="none")` *read-only* yang didaur ulang saat *scroll*, mendukung clip baris ke-4+ + *focus-scroll* tanpa scrollbar + lebar tetap `54d` persis `U-15` *Import* & `Expectasi2.jpg`), atau
* **(b) Read-Only Fixed `tk.Text(height=3, wrap="none")` ringan per box** (pola persis `Import from XUAT`, tanpa binding edit/gutter/Pillow cap — perlu *benchmark* 150–300 box), atau
* **(c) Single `tk.Text` murni** dengan kompromi: tidak ada clip baris ke-4+ per box, hanya `wrap="none"` melewati 54d?




2. **Harmonisasi Lebar Kotak Import (`1×50` vs `54d`) pada `U-14` & `U-07`:**
* Kotak dialog kini memakai **`54d` (`U-07`)**, sementara pada `U-14` disebutkan kotak 1-baris untuk Actor/Title/Subtitle berukuran **`1×50`** (dan kotak dialog di jendela Import lama memakai `3×50`). Perlu disepakati apakah kotak dialog Import ikut naik ke `3×54` sementara kotak Actor/Title/Subtitle tetap `1×50`, atau semuanya seragam ke `54d`.




3. **Batas Arsip untuk Actor vs Title/Subtitle (`U-11` + `U-14`):**
* Konfirmasi aturan: **Title**, **Subtitle**, dan **Dialogue** yang berhasil diimpor masuk ke kandidat `XUAT Translation Archiving`; sedangkan **Actor/Speaker** (meski diimpor lewat kotak `1×50`) **dikecualikan secara default dari penghapusan/pengarsipan XUAT** karena merupakan kamus nama global lintas cerita.


4. **Dampak `U-03` (`Quick Edit`) terhadap Sinkronisasi *In-Place*:**
* Pastikan setiap ketikan di `Quick Edit` hanya memperbarui isi blok/kartu box aktif secara $O(1)$ (bukan memanggil `_render_continuous_view()` seluruh dokumen), dan tab `Quick Edit` otomatis aktif saat berpindah ke *All Script* sementara `Raw Commands` tetap mudah diklik di sebelahnya.



---

## 5. Peta Pembagian Sesi Usulan (`S09` → `S12 / v1.5.0`)

| Sesi | Target Versi | Cakupan Utama |
| --- | --- | --- |
| **S09** | `v1.4.8` | **Core Fixes, `54d` Calibration, Preview Fix, & Cleanup:** `U-01`, `U-02`, `U-06`, `U-07`, `U-18`, `U-19`, `U-16`, dan `RM-01` (hapus Windows Console toggle & `F12`). |
| **S10** | `v1.4.9` | **All Script Redesign, Perf Overhaul, & `Quick Edit`:** `U-03`, `U-04`, `U-05`, `U-15`, `U-17`, `U-20` (termasuk penghapusan *All Script Preview*, penghapusan ikon suara & `----------`, dan optimasi Paste 142+ box). |
| **S11** | `v1.4.10` | **Import from XUAT 1-Line Redesign, Archiving Anti-Hang, & Unified Loading Bar:** `U-08`, `U-09`, `U-10`, `U-11`, `U-12`, `U-13`, `U-14`. |
| **S12** | **`v1.5.0`** | **Final Deep Code Inspection, Dead-Code & Bloat Sweep, Memory-Leak Audit, & Release Gate:** Audit menyeluruh `misora.py`/`core/`/`assets/`, pembersihan sisa *dead code*, verifikasi *stress test* + QA manual Windows final → promosi resmi ke **`v1.5.0`**. |

---

Anda bisa langsung menyimpan atau menyalin blok spesifikasi di atas sebagai bahan dokumentasi dan diskusi ke AI lain. Apakah ada poin pada tabel `U-01`–`U-20` atau pembagian sesi `S09`–`S12` di atas yang masih perlu direvisi sebelum dibawa ke review AI lain?