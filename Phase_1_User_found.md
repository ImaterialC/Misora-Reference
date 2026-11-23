bug yang sekarang saya temukan antara lain:
B1. text box find dan replace tidak sejajar.
B2. 4 button find in files, cancel, replace, replace all tidak sejajar.
B4. tombol [-] pada ribon group ngui dihapus karena tidak berguna dan redundant dengan fungsi tombol warna yang sudah sepaket dengan [-]
B5 tombol icon player{0} diganti menjadi cuma icon player .
B6 toggle continous view diganti menjadi toggle all script (melihat seluruh box dialog berurutan dari atas kebawah)
B7. toggle untuk select box, all script (continous view) belum memiliki icon
B8 memindahkan tombol preview bareng dengan tombol continous view dan select box dan menjadikan nya 1 grup
B9. permintaan untuk membuat tombol mtl menjadi drawer tidak dilakukan.
B10. float windows paste import script preview tidak terlihat apa apa.
B11. select box cuma muncul saat continous view aktif.
B12. icon gembok berada di sebelah kanan check box select box
B13. tombol player keluar dari group ngui
B14. tambahkan di main menu view>toggle ribbon ngui> tombol2 ngui di hilangkan,
temuan ini terjadi karena dalam tampilan kecil saat snap, banyak tombol dan fungsi di sebelah kiri hilang/tertutup, sedangkan untuk view lemabr kerja text dan box sudah berlebih
B15. rubah windows search result dan opened files menjadi drawer yang bisa di buka
B16. default untuk pertama kali dibuka atau saat opened files kosong adalah tombol besar ditengah "open files" dan di bawah ada deskripsi, drag and drop unity3d story data  disini atau save lembar kerja .misora.
B17. save project, kemampuan untuk menyimpan sesi pekerjaan dan dilanjutkan nanti dalam bentuk file .misora
B18 saat membuka save project padahal ada project lain akan ada prompt untuk menyimpan project lama, atau ditimpa, berikan warning jika ditimpa maka pekerjaan lama akan hilang, buat windows untuk memetakan perbedaan project yang akan ditimpa.

File .misora hanya menyimpan daftar referensi file yang terbuka, file & box aktif, mode tampilan, status gembok per box.uid, dan pengaturan scope—bukan isi biner editan yang belum disimpan (editan tetap disimpan ke file .unity3d/.txt asli lewat prompt Save / Discard / Cancel standar agar tidak tercipta dua versi file yang saling bentrok). Jendela diff (B18) cukup berupa tabel ringkas: file yang ada di sesi lama vs sesi baru + penanda file mana yang masih dirty.

B19 tab opened files jika dipencet 2 kali fungsinya sama dengan open file
B20 tombol open files tidak bisa memilih lebih dari 1 file.
B21. ketika select current files text box directori dihapus
B22. perhitungan characters tidak tepat, perhatikan juga bahwa karakter latin dan jepang beda ukuran, usulan saya adalah dihapus, karena sudah ada vertical rules dan horisontal rules,
B23 berikan warna merah pada rules horisontal 60 dan seterusnya
B24 berikan warna merah pada line 4 dan seterusnya pada vertikal
B25 highlight ketika ada  horisontal 60 ditembus. perhatikan bahwa ukuran font jepang dan latin berbeda.
B26 angka pada rules menyesatkan B23 dan B26 menyebut angka 60 yang sejatinya adalah 50 jika berdasarkan  jumlah karakter. mungkin ini diakibatkan bedanya font pada box kerja dan rules perhatikan refrensi gambat ini
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-23%2012-02-06-049.jpg
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-23%2012-02-21-785.jpg

B27 toggle preview membuat tampilan box identik dengan game mengacu pada gambar di bawah dan juga asset game dibawah ini
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-22%2002-28-14-200.jpg
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/AtlasAdv%20[48D3C5B6AD].png
B28 toggle preview pada continous mode membuat tampilan box identik dengan game mengacu pada gambar di bawah
https://github.com/ImaterialC/Misora-Reference/blob/main/references/assets/bandicam%202026-11-22%2002-28-27-995.jpg
pakai gambar primitif kode Tkinter (tanpa memasukkan file gambar AtlasAdv Cygames ke repo MIT), serta apakah batas kapasitas hanya untuk Dialogue (50×3) dulu atau sekalian Box 0 Summary (berapa digit × baris pada screenshot Summary)?

B29 toggle select box juga berfungsi pada tampilan Game view (clean dialogue)
di header atas (jadi kamu bisa lompat-lompat box lalu centang mana yang mau di-copy/cut)
B30 ubah nama yang membingungkan Game view (XXX) Nama ini dibuat sebagai lawan dari raw view di window bawah.
B31 kemampuan untuk bisa meng edit raw view, tapi saat meng edit akan ada warning box sebelum di commit di tampilan ketika menekan yes, akan di parser sebagai edited files dan tampilan refresh sesuai yang di edit di raw, tapi jika parser gagal misalnya karena yang di edit bukan string text maka akan revert atau batal.


B32 windows mtl di rombak total, windows mtl di pindah di drawer kanan, disana berbagai macam pilihan mtl disusun dari atas kebawah dari berbagai MTL yang ada.
box dari translate bisa di edit, tombol refresh dengan icon refresh di tiap box agar bisa di translate ulang, tombol apply dengan icon panah ke kanan untuk menerapkan terjemahan. terdapat refresh semuanya
Di drawer kanan, pengguna mencentang mesin mana saja yang ingin ditampilkan berurutan dari atas ke bawah (mencegah token user hangus)Tiap kartu mesin bisa diedit, punya tombol ↻ (Refresh) & → (Apply, hormati gembok). Tombol Refresh All hanya menyegarkan mesin yang dicentang + minta konfirmasi jika ada mesin berbayar + memakai cache sesi.

B33 untuk tampilan alls script tampilan mtl drawer berubah bukan menampilkan berbagai mtl tiap box melainkan menampilkan terjemahan tiap box pada mtl yang di pilih di atas.
B34 kemampuan untuk import from xuat. problematikanya adalah ada beberapa terjemahan ganda, dan ada yang belum diterjemahkan, oleh karena itu akan muncul floating windows untuk memilah milah terjemahan apa saja yang akan di terapkan, tampilannya mirip dengan all script view.

Disklaimer, semua penamaan dan konsep visual masih tentatif dan boleh diusulkan ulang, kalian bebas membantah usulan saya dan merevisi ulang atas usulan saya.
