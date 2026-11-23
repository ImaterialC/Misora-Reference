# Panduan Lengkap Pengguna (Bahasa Indonesia)

Panduan ini menjelaskan cara menggunakan **Kyouka Asset Explorer** dari awal untuk mencari teks *Princess Connect! Re:Dive*, mengekstrak seluruh folder kategori, mengunduh aset dari CDN Jepang, hingga mengunggah proyek ke GitHub.

---

## Langkah 1: Persiapan Folder Kerja

1. Pastikan **Python 3.10 – 3.14** sudah terpasang di komputer Anda.
2. Taruh file **`master.db`** terbaru (misalnya unduhan dari `https://roboninon.win/db/download`) ke dalam folder `Kyouka-Asset-Explorer/`:
   ```text
   Kyouka-Asset-Explorer/
   ├── Kyouka-Asset-Explorer.bat
   ├── Kyouka-Asset-Explorer.py
   ├── master.db
   └── modules/
   ```
3. *(Opsional, khusus untuk ekstrak/repack file `.unity3d` Main Story & Subtitle)* Jalankan perintah berikut sekali saja di Command Prompt/PowerShell:
   ```bash
   pip install -r requirements.txt
   ```
4. Klik dua kali **`Kyouka-Asset-Explorer.bat`** untuk membuka menu utama.

---

## Langkah 2: Mencari Teks yang Terlihat di Game (`master.db`)

Jika Anda melihat sebuah kalimat atau nama di layar game (misalnya nama monster, deskripsi skill, celotehan Guildhouse, atau pesan sistem) dan tidak tahu letaknya:

1. Pilih **Menu 1 (`Global Full-Text Search`)**.
2. Ketik persis kata yang muncul di game (contoh: `コボルト`, `Lizardman`, atau potongan kalimat Jepang).
3. Program akan memindai **seluruh tabel dan seluruh kolom teks** di `master.db` lalu menampilkan nama tabel beserta **Category Folder**-nya.
4. Langsung pilih aksi dari hasil pencarian:
   - Ketik **`v 1`** untuk melihat isi detail kecocokan pada tabel nomor 1.
   - Ketik **`e 1`** untuk mengekspor **hanya tabel nomor 1**.
   - Ketik **`f 1`** untuk mengekspor **seluruh folder kategori yang berkaitan** sekaligus (contoh: begitu menemukan 1 monster di `enemy_parameter`, ketik `f 1` untuk mengekspor semua tabel monster ke `exports/07_monsters_and_enemies/`).

---

## Langkah 3: Cara Menerjemahkan Hasil Ekspor

Buka folder `exports/`. Setiap tabel menghasilkan dua format:

- **`.csv`** (UTF-8 BOM): Bisa langsung dibuka di Microsoft Excel atau Google Sheets tanpa huruf Jepang rusak. Di sebelah setiap kolom teks sudah tersedia kolom kosong `*_translation`.
- **`.translation.json`**: Format terstruktur dengan `key` unik (`nama_tabel:primary_key:kolom`) dan field `"translation": ""`. Sangat cocok untuk kolaborasi tim (Crowdin/Weblate) maupun suntik ulang otomatis.

### Menyuntikkan Kembali Terjemahan ke `master.db`
Setelah mengisi kolom `"translation"` pada file `.translation.json` di folder `exports/`, jalankan **Menu 5 (`Re-Inject Translations`)**. Program akan membuat salinan baru di **`output/master_patched.db`** tanpa pernah merusak `master.db` asli Anda.

---

## Langkah 4: Memahami Kode Developer & Mengunduh Story dari CDN Jepang

> **Penting:** Naskah dialog **Main Story, Event Story, Bond Story, dan Guild Story** TIDAK tersimpan di `master.db`, melainkan di file `.unity3d` pada server CDN Jepang.

1. **Menerjemahkan Kode Nama Aset Developer:**
   Pilih **Menu 6 (`Developer Codename Glossary & Asset/ID Decoder`)** untuk melihat arti istilah seperti `hatsune` (Event Bulanan), `shiori` (Side Story), `room` (Guildhouse), atau memasukkan nama file/ID agar otomatis diterjemahkan artinya.
2. **Mengunduh Story dari CDN Jepang:**
   - Taruh file manifest CSV server Jepang ke dalam folder `manifests/` (lihat `manifests/README.md`).
   - Pilih **Menu 7 (`JP CDN Asset Bridge`)** -> pilih pencarian berdasarkan `master.db` atau langsung ke manifest.
   - Program akan mengunduh file dari `prd-priconne-redive.akamaized.net`, memverifikasi MD5, mengecek duplikat BepInEx (jika dijalankan dengan `--bepinex`), lalu otomatis mengekstraknya ke folder `text/`.
3. **Ekstrak & Repack `.unity3d` Lokal:**
   - Taruh file `.unity3d` di folder `input/`, lalu gunakan **Menu 8** untuk ekstrak ke `text/` dan **Menu 9** untuk *repack* terverifikasi ke `output/`.

---

## Langkah 5: Mengunggah ke GitHub dengan Aman

File **`.gitignore`** di paket ini sudah dikonfigurasi agar **`master.db`, file `.unity3d`, serta folder kerja (`exports/`, `input/`, `text/`, `output/`) TIDAK ikut terunggah ke GitHub** (menghindari file raksasa & masalah hak cipta).

Jalankan perintah berikut di folder `Kyouka-Asset-Explorer`:

```bash
git init
git add .
git commit -m "Initial commit: Kyouka Asset Explorer"
git branch -M main
git remote add origin https://github.com/USERNAME-ANDA/Kyouka-Asset-Explorer.git
git push -u origin main
```
