# Auto Assignment Approval Script

Script ini mengotomatiskan proses persetujuan (approval) penugasan di **Fasih SM BPS**. Script akan login menggunakan akun SSO kamu, memproses link penugasan dari file CSV, dan menyetujuinya satu per satu.

## Fitur

- 🔐 **Login Aman**: Meminta username dan password SSO kamu saat dijalankan (tidak ada password yang disimpan di kode).
- ⏳ **Smart Waits**: Otomatis menunggu tombol dan elemen muncul sebelum diklik, jadi aman kalau koneksi agak lambat.
- 🔁 **Auto-Retry**: Kalau ada yang gagal, bakal diingat dan dicoba lagi otomatis di akhir proses.
- 🚀 **Error Handling**: Kalau ada error di satu baris, script tetap jalan ke baris berikutnya.

## Prasyarat

1.  **Python 3.x** terinstall.
2.  **Google Chrome** terinstall.
3.  Install library Python yang dibutuhkan:

    ```bash
    pip install selenium webdriver-manager
    ```

## Cara Pakai

1.  **Siapkan `input.txt`**:
    - Buka halaman Fasih yang berisi tabel penugasan.
    - Copy seluruh **HTML table content** dari tabel yang sudah di-approve oleh PML.
    - Paste ke dalam file bernama `input.txt` di folder yang sama dengan script ini.
    - Pastikan file `input.txt` KOSONGKAN isinya sebelum di-paste data baru agar bersih.

2.  **Jalankan Konversi**:
    - Script butuh `output.csv` yang dihasilkan dari `input.txt`.
    - Pastikan kamu menjalankan `html_to_csv.py` terlebih dahulu (jika ada) atau pastikan `output.csv` sudah tersedia dari hasil ektrak `input.txt`.
    *(Catatan: Script `approve_script.py` membaca `output.csv`)*

3.  **Jalankan Script Approval**:
    ```bash
    python approve_script.py
    ```

4.  **Login**:
    - Masukkan Username dan Password SSO saat diminta di terminal.
    - Browser akan terbuka dan mulai memproses approval.

5.  Santai sejenak sambil script bekerja! ☕

---

**Made with ❤️ by Albert Assidiq**
