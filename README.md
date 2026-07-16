# Portofolio Jenny — Flask + TiDB + Cloudinary + Resend

Project ini dibuat mengikuti mockup `Untitled.zip`: tema floral krem/pink, logo **Jenny.**, hero dua kolom, bagian Tentang, kartu Keahlian, timeline Pengalaman, kartu Proyek, dan form Hubungi Saya.

## Fitur yang sudah tersedia

### Halaman publik
- Hero profil dinamis
- Tentang saya dan tautan resume
- Grid keahlian
- Timeline pengalaman bergantian kiri/kanan
- Grid proyek
- Form kontak
- Responsive untuk desktop, tablet, dan ponsel

### Dashboard admin
- Login dan logout
- Edit profil serta upload foto ke Cloudinary
- CRUD keahlian
- CRUD pengalaman serta upload gambar
- CRUD proyek serta upload gambar
- Daftar pesan kontak, status baca, dan hapus pesan

### Integrasi
- **TiDB Cloud** untuk seluruh data
- **Cloudinary** untuk media gambar
- **Resend** untuk notifikasi pesan kontak
- Pesan kontak tetap tersimpan di TiDB walaupun Resend belum dikonfigurasi atau gagal mengirim

---

# Langkah 1 — Persiapan Python

Disarankan menggunakan Python 3.11 atau lebih baru.

Buka terminal pada folder project:

```powershell
cd C:\lokasi\Portofolio_Jenny
```

Buat virtual environment:

```powershell
py -m venv venv
```

Aktifkan:

```powershell
venv\Scripts\activate
```

Install dependency:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# Langkah 2 — Membuat database TiDB Cloud

1. Masuk ke dashboard TiDB Cloud.
2. Buat cluster Starter/Essential bila belum ada.
3. Buka cluster, pilih **Connect**.
4. Pilih:
   - Connection Type: `Public`
   - Branch: `main`
   - Connect With: `General`
5. Generate atau salin password database.
6. Catat `host`, `port`, `user`, dan password.
7. Buka SQL Editor TiDB lalu jalankan:

```sql
CREATE DATABASE IF NOT EXISTS portfolio_jenny
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

8. Bila menu Connect menyediakan CA certificate, unduh dan simpan, misalnya:

```text
C:\sertifikat\isrgrootx1.pem
```

Jangan memindahkan atau menghapus file tersebut setelah path dimasukkan ke `.env`.

---

# Langkah 3 — Mengisi file `.env`

Buka `.env.example`, lalu salin isinya ke `.env`.

Isi koneksi TiDB:

```env
SECRET_KEY=isi-dengan-secret-random-yang-panjang

TIDB_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USER=xxxxxx.root
TIDB_PASSWORD=password_tidb_anda
TIDB_DATABASE=portfolio_jenny
TIDB_CA_PATH=C:/sertifikat/isrgrootx1.pem
```

Gunakan `/` pada path Windows agar tidak terjadi masalah escape character.

Buat secret key dengan perintah:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Isi akun admin awal:

```env
ADMIN_NAME=Jenny
ADMIN_EMAIL=email-admin-anda@gmail.com
ADMIN_PASSWORD=PasswordKuat123!
```

Password ini hanya dipakai ketika akun admin pertama kali dibuat oleh perintah `init-db`.

---

# Langkah 4 — Menyiapkan Cloudinary

1. Buat atau masuk ke akun Cloudinary.
2. Buka dashboard produk Cloudinary.
3. Salin:
   - Cloud name
   - API key
   - API secret
4. Isi `.env`:

```env
CLOUDINARY_CLOUD_NAME=cloud_name_anda
CLOUDINARY_API_KEY=api_key_anda
CLOUDINARY_API_SECRET=api_secret_anda
CLOUDINARY_FOLDER=portfolio-jenny
```

Gambar profil, gambar pengalaman, dan gambar proyek akan masuk ke subfolder:

```text
portfolio-jenny/profile
portfolio-jenny/experiences
portfolio-jenny/projects
```

API secret tidak boleh ditaruh di HTML, JavaScript frontend, screenshot, atau GitHub.

---

# Langkah 5 — Menyiapkan Resend

1. Buat akun Resend.
2. Buka menu API Keys dan buat API key.
3. Untuk penggunaan produksi, tambahkan dan verifikasi domain milik Anda.
4. Tentukan email penerima notifikasi.
5. Isi `.env`:

```env
RESEND_API_KEY=re_xxxxxxxxx
RESEND_FROM_EMAIL=Portfolio Jenny <portfolio@domain-terverifikasi.com>
CONTACT_RECEIVER_EMAIL=email-anda@gmail.com
```

Pada tahap pengujian tanpa domain, `onboarding@resend.dev` dapat digunakan sesuai batasan akun Resend. Form kontak tetap menyimpan pesan ke database walaupun pengiriman email belum aktif.

---

# Langkah 6 — Membuat tabel dan data awal

Pastikan virtual environment aktif dan `.env` sudah benar, lalu jalankan:

```powershell
flask --app app init-db
```

Perintah ini akan:
- Membuat tabel `admins`
- Membuat tabel `profiles`
- Membuat tabel `skills`
- Membuat tabel `experiences`
- Membuat tabel `projects`
- Membuat tabel `contact_messages`
- Membuat akun admin awal
- Menambahkan konten contoh agar tampilan langsung terisi

Perintah aman dijalankan kembali karena tidak menghapus data yang telah ada.

Untuk mengganti password admin setelah akun dibuat:

```powershell
flask --app app set-admin-password "PasswordBaruYangKuat123!"
```

---

# Langkah 7 — Menjalankan website

Jalankan:

```powershell
python app.py
```

Buka halaman publik:

```text
http://127.0.0.1:5000
```

Buka login admin:

```text
http://127.0.0.1:5000/admin/login
```

Login menggunakan `ADMIN_EMAIL` dan `ADMIN_PASSWORD` yang dipakai ketika menjalankan `init-db` pertama kali.

---

# Langkah 8 — Mengganti data agar sesuai identitas Jenny

Urutan yang disarankan:

1. Buka **Admin > Profil**.
2. Ganti sapaan, nama lengkap, judul, deskripsi, dan tentang saya.
3. Upload foto. Foto otomatis masuk ke Cloudinary.
4. Isi email, telepon, lokasi, resume, GitHub, LinkedIn, dan Instagram.
5. Buka **Keahlian**, ubah empat data contoh.
6. Buka **Pengalaman**, ubah timeline dan upload gambar.
7. Buka **Proyek**, ubah proyek contoh, teknologi, tautan, dan gambarnya.
8. Buka website publik melalui tombol **Preview Website**.

Ikon menggunakan Bootstrap Icons. Contoh nilai ikon:

```text
bi-code-slash
bi-brush
bi-database
bi-bar-chart
bi-box
bi-flower1
bi-leaf
bi-heart
```

---

# Alur data aplikasi

## Upload gambar

```text
Admin memilih gambar
→ Flask memvalidasi ekstensi dan ukuran
→ Cloudinary mengunggah gambar
→ secure_url dan public_id disimpan di TiDB
→ halaman publik membaca URL dari TiDB
```

## Form kontak

```text
Pengunjung mengisi form
→ Flask memvalidasi input
→ pesan disimpan di TiDB
→ Resend mengirim notifikasi ke pemilik portofolio
→ admin dapat membaca pesan di dashboard
```

---

# Struktur tabel

| Tabel | Fungsi |
|---|---|
| `admins` | Akun login admin |
| `profiles` | Hero, bio, kontak, dan sosial media |
| `skills` | Kartu keahlian |
| `experiences` | Timeline pengalaman |
| `projects` | Kartu proyek |
| `contact_messages` | Pesan dari pengunjung |

---

# Troubleshooting

## `Table ... doesn't exist`

Jalankan:

```powershell
flask --app app init-db
```

## `Access denied` atau `Missing user name prefix`

Salin ulang username persis dari menu **Connect** TiDB. Pada TiDB Starter, username sering memiliki prefix seperti:

```text
xxxxxx.root
```

## `Can't connect to MySQL server`

Periksa:
- Cluster masih aktif
- Public endpoint aktif
- Host dan port benar
- Password benar
- IP access list bila jenis cluster mewajibkannya
- Path CA certificate benar

## `SSL certificate verify failed`

Unduh CA certificate dari menu Connect TiDB dan isi `TIDB_CA_PATH` dengan path file yang benar.

## Upload Cloudinary gagal

Periksa ketiga credential Cloudinary, format gambar, dan ukuran file. Maksimum upload aplikasi adalah 5 MB.

## Email Resend tidak masuk

Periksa:
- API key benar
- Domain pengirim sudah diverifikasi
- `RESEND_FROM_EMAIL` memakai alamat pada domain tersebut
- `CONTACT_RECEIVER_EMAIL` benar
- Status email pada menu Admin > Pesan

## Ganti `.env` tetapi perubahan tidak terbaca

Hentikan server dengan `Ctrl + C`, lalu jalankan kembali:

```powershell
python app.py
```

---

# Keamanan sebelum upload GitHub

Pastikan `.gitignore` berisi `.env`. Jangan pernah mengunggah:
- Password TiDB
- Cloudinary API secret
- Resend API key
- Flask secret key
- File CA pribadi bila kebijakan cluster melarangnya
