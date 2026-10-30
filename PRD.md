# PRODUCT REQUIREMENTS DOCUMENT (PRD) & SYSTEM DESIGN
## Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB
**Versi:** 2.2.0-FINAL  
**Tanggal:** 10 Oktober 2026  
**Status:** Disetujui 100% & Terkunci untuk Implementasi (*Final Approved Specification*)  
**Unit Operasional:** Pusat Pengendalian Operasi Penanggulangan Bencana (Pusdalops-PB) BNPB  
**Afiliasi:** Capstone Design Project S1 Sistem Informasi Telkom University Jakarta  

---

## 1. Ringkasan Eksekutif (*Executive Summary*)

Pusat Pengendalian Operasi Penanggulangan Bencana (Pusdalops-PB) BNPB beroperasi secara kontinu selama 24 jam sehari untuk memantau situasi kebencanaan di seluruh wilayah Republik Indonesia. Salah satu luaran (*output*) wajib harian adalah penyusunan **Laporan Harian Situasi Bencana (Lapsit / SitRep Bagian A)** yang dilaporkan kepada Kepala BNPB, Kementerian/Lembaga terkait, dan Presiden RI.

Sistem ini dirancang sebagai platform otomasi pemantauan kebencanaan berbasis intelijen teks yang mengintegrasikan:
1. **Windowing Siklus Operasional 24 Jam (07.00 – 07.00 WIB)** dengan fleksibilitas penautan siklus dan *countdown timer* menuju cut-off.
2. **Dual-Trigger Data Ingestion**: Penjadwalan berkala latar belakang (*Celery Beat*) dan tombol instan *on-demand* `[🔄 Tarik Data Sekarang / Sync Now]` di header.
3. **Penyaring Gempa Adaptif**: Lolos otomatis jika $M \ge 5.0$ & Depth $\le 20\text{ km}$, serta gempa darat dangkal merusak $M \ge 4.5$ dengan intensitas $\ge \text{III MMI}$.
4. **Deduplikasi 2 Lapis**: Lapis 1 ($\ge 0.80$ teks utuh) dan Lapis 2 ($\ge 0.60$ jika wilayah dan jenis bencana sama $< 24\text{ jam}$), dilengkapi fitur interaktif `[🔗 Gabung Berita Susulan (Merge)]`.
5. **Antrean Meja Piket & 4 Tab Status**: `Belum Terverifikasi (Pending)`, `Terverifikasi`, `Hoaks`, dan `Semua Data`, dilengkapi badge alarm visual `[🚨 ISU BANTUAN]`.
6. **Formulir Koreksi Metadata 5 Blok** serta formulir ad-hoc `[+ Tambah Kejadian Manual]`.
7. **Pusat Ekspor & Penguncian Status Siklus**: Tombol `[🔒 Lock Snapshot]` dan fitur darurat `[🔓 Emergency Unlock]` oleh akun Supervisor.
8. **Dual Output Satu-Klik Berstandar Tata Naskah Dinas**: Teks Ringkasan WhatsApp Pimpinan & Dokumen Microsoft Word (`.docx`) Bagian A resmi Pusdalops BNPB ($\le 5\text{ detik}$) dengan *null-safety* frasa baku dinas.

---

## 2. Arsitektur Siklus Operasional 24 Jam (*Windowing 07.00 – 07.00 WIB*)

Di Pusdalops BNPB, satu siklus pemantauan harian resmi **tidak mengikuti tanggal kalender umum (00.00 – 23.59)**, melainkan dihitung mulai **pukul 07.00 WIB hari ini hingga pukul 07.00 WIB hari berikutnya**.

```
        Siklus: SIKLUS-20261009 (24 Jam Operasional)
┌─────────────────────────────────────────────────────────────┐
│ 07:00:00 WIB (H)                 │ 06:59:59 WIB (H+1)       │
├─────────────────┬────────────────┼──────────────────────────┤
│ Shift 1 (Pagi)  │ Shift 2 (Sore) │ Shift 3 (Malam/Subuh)    │
│ 07.00-15.00 WIB │ 15.00-23.00 WIB│ 23.00-07.00 WIB          │
└─────────────────┴────────────────┴──────────────────────────┘
▲                                                             ▲
Cut-Off Mulai                                        Cut-Off Tutup / Freeze
```

### 2.1. Aturan Penomoran & Fleksibilitas Siklus
* **Logika Kode Siklus**:
  $$\text{Kode Siklus} = \text{SIKLUS-YYYYMMDD}$$
  *Tanggal yang dicantumkan pada kode siklus adalah tanggal hari mulainya pukul 07.00 WIB.*
* **Contoh Kasus Normal**:
  * Berita masuk **9 Oktober 2026 pukul 14.00 WIB** $\rightarrow$ Terikat pada `SIKLUS-20261009`.
  * Berita masuk **10 Oktober 2026 pukul 02.30 WIB (subuh)** $\rightarrow$ **Tetap terikat pada `SIKLUS-20261009`**.
  * Berita masuk **10 Oktober 2026 pukul 07.00:01 WIB** $\rightarrow$ Otomatis berpindah dan terikat pada `SIKLUS-20261010`.
* **Penyempurnaan Penanganan Kejadian di Batas Cut-Off**:
  * Jika sebuah bencana terjadi pukul **06.45 WIB** (siklus kemarin), namun beritanya baru terbit atau dilaporkan pukul **07.15 WIB** (siklus baru), operator pada formulir *Edit Metadata* memiliki dropdown **Tautkan ke Siklus** untuk memindahkannya ke siklus riil (`SIKLUS-20261009`).
  * Dasbor menampilkan widget **Hitung Mundur Cut-Off** (contoh: *"06j 18m 42s menuju 07.00 WIB"*).

---

## 3. Alur Kerja Hulu ke Hilir (*End-to-End Workflow Pipeline*)

```
[Portal Berita & RSS Publik] + [API BMKG]
                  │
                  ▼ (1. Ingestion Berkala Celery Beat ATAU Tombol [🔄 Sync Now])
     [Penyaring Kata Kunci & Aturan Gempa Adaptif]
     ├── Bencana Umum: Banjir, Longsor, Karhutla, Cuaca Ekstrem
     └── Khusus Gempa: 
         - Lolos Otomatis: M >= 5.0 & Kedalaman <= 20 km
         - Gempa Darat Dangkal: M >= 4.5 & Guncangan dirasakan >= III MMI
                  │
                  ▼ (2. Deduplikasi 2 Lapis & Toponym Extraction)
     ├── Lapis 1: Cosine Similarity >= 0.80 teks utuh
     ├── Lapis 2: Cosine Similarity >= 0.60 jika Kab/Kota + Bencana sama (< 24 jam)
     ├── Portal paling kredibel = Rujukan Utama (Lead Article)
     └── Pencocokan Master Wilayah Kemendagri (Provinsi -> Kab/Kota -> Kecamatan)
                  │
                  ▼ (3. Masuk Antrean Meja Piket)
     [Dasbor Tab: Belum Terverifikasi / Pending]
                  │
                  ├─► Badge Visual: [🚨 ISU BANTUAN] jika ada keluhan logistik
                  ├─► Opsi Gabung Berita Susulan [🔗 Merge]
                  └─► Buka Modal: Koreksi Metadata & Input Real Data Lapangan
                  │
                  ▼ (4. Transisi Status Verifikasi)
          ┌───────┴───────┐
          ▼               ▼
      [ HOAKS ]    [ TERVERIFIKASI ]
    (Wajib Catat          │
    Alasan Bantahan)      ▼ (5. Pilihan Dual Output Satu-Klik)
                  ┌───────┴────────────────────────┐
                  ▼                                ▼
          [ 📋 Salin Ringkasan WA ]       [ 📄 Unduh Word (.docx) Bagian A ]
          (Format Klaster Pimpinan)       (Kop Pusdalops Resmi, Frasa Baku Dinas)
```

---

## 4. Struktur Antarmuka & Menu Sistem (*Web UI Structure*)

Sistem memiliki **4 Menu Utama**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ PUSDALOPS BNPB  [Dasbor Pemantauan] [Riwayat Bencana] [Pusat Ekspor] [Master Data]│
└────────────────────────────────────────────────────────────────────────┘
```

### 4.1. Menu 1: Dasbor Pemantauan (Halaman Kerja Utama)
* **Header & Quick Trigger**:
  * Tombol **`[🔄 Tarik Data Sekarang / Sync Now]`**: Eksekusi penarikan data langsung *on-demand* dengan spinner loading.
  * Status Shift & Identitas Operator yang sedang bertugas.
* **Pengendali Siklus**:
  * Dropdown/Selector Tanggal Siklus Operasional (07.00 – 07.00 WIB).
  * Tombol navigasi cepat: `[◀ Siklus Sebelumnya]` | `[Siklus Berikutnya ▶]` | `[Siklus Berjalan]`.
  * Indikator Hitung Mundur Menuju Cut-Off 07.00 WIB.
* **Tab Status Dinamis**:
  1. `🔴 Belum Terverifikasi (Pending)`: Antrean aktif berita yang wajib dicek ke daerah.
  2. `🟢 Terverifikasi`: Daftar kejadian valid yang sudah dikonfirmasi satgas dan siap diekspor.
  3. `⚫ Hoaks`: Arsip berita fiktif/daur ulang yang ditolak (menampilkan alasan bantahan resmi).
  4. `⚪ Semua Data`: Agregasi lengkap seluruh temuan pada siklus tersebut.
* **Tombol Aksi Cepat**:
  * `[+ Tambah Kejadian Manual]`: Membuka modal input ad-hoc dari telepon/radio BPBD.
  * `[📋 Salin Format WA]`: Satu-klik salin ringkasan teks untuk grup WhatsApp pimpinan.
  * `[📄 Unduh Word Bagian A]`: Satu-klik unduh dokumen dinas Microsoft Word `.docx`.
* **Baris Tabel Temuan (Data Grid)**:
  * Waktu Tayang Media, Wilayah Kemendagri, Judul & Ringkasan, Badge `[🚨 ISU BANTUAN]`, Tautan Media Asli (Lead & Rujukan), Catatan Konfirmasi, Tombol Gabung Berita Susulan `[🔗 Merge]`, dan Tombol Utama `[✏️ Edit Metadata & Verifikasi]`.

### 4.2. Menu 2: Riwayat Bencana (Arsip Digital / Logbook)
* Kumpulan seluruh kejadian berstatus `TERVERIFIKASI` dari siklus-siklus lampau.
* Pencarian multi-parameter: rentang tanggal kalender, jenis bencana, dan wilayah (Provinsi/Kabupaten).

### 4.3. Menu 3: Pusat Ekspor Laporan (*Report Generator & Lock Snapshot*)
* **Pratinjau Naskah Resmi**: Preview struktur dokumen Bagian A BNPB sebelum diunduh.
* **Penguncian Status (*Lock Snapshot*)**: Supervisor mengunci siklus setelah laporan diserahkan ke Kepala BNPB. Pada siklus terkunci, tombol edit beralih ke mode `[👁️ Lihat Data]` (*read-only*).
* **Fitur Darurat (*Emergency Unlock*)**: Tombol buka kunci khusus akun bertingkat Supervisor jika terjadi ralat darurat dari daerah, dengan kewajiban mengisi alasan pembukaan kunci ke dalam log audit.

### 4.4. Menu 4: Pengaturan & Master Data (Hak Akses Supervisor)
* **Manajemen Petugas (RBAC)**: Pengelolaan akun operator piket dan pembagian shift kerja (Shift 1, 2, 3).
* **Pemutakhiran Master Kemendagri**: Sinkronisasi basis data kode dan nama wilayah Kepmendagri 100.1.1-6117/2022.

---

## 5. Anatomi Formulir & Interaksi Modal

### 5.1. Modal Pop-up: "Edit Metadata & Input Real Data" (5 Blok Ringkas)
1. **Blok 1 (Wilayah Kemendagri)**: Dropdown hierarkis (Provinsi $\rightarrow$ Kab/Kota $\rightarrow$ Kecamatan). Kolom Kecamatan opsional jika gempa bumi terjadi di perairan lepas pantai.
2. **Blok 2 (Waktu Nyata Bencana)**: Input tanggal dan jam riil kejadian di lapangan.
3. **Blok 3 (Fakta Dampak Lapangan)**: 
   * Korban Jiwa: Meninggal, Luka-Luka, Hilang, Mengungsi.
   * Kerusakan Fisik: Rumah Rusak Berat, Sedang, Ringan, Terendam, Fasilitas Umum, Luas Area Terbakar/Terdampak (Ha).
4. **Blok 4 (Tindakan TRC & Kondisi Terkini)**: Upaya penanganan yang dilakukan tim di lapangan dan kondisi mutakhir.
5. **Blok 5 (Keputusan Status & Jejak Audit)**: Radio button status (`Pending`, `Terverifikasi`, `Hoaks`), nama personel BPBD yang dikonfirmasi, catatan konfirmasi (*wajib diisi jika status HOAKS sebagai bahan klarifikasi pers*), dan akun operator editor.

### 5.2. Modal Pop-up: "Tambah Kejadian Manual" (`[+ Tambah Manual]`)
Digunakan jika laporan bencana diterima langsung melalui saluran telepon darurat atau radio HF Pusdalops tanpa ada artikel berita di media daring:
* **Kolom Input**:
  1. Jenis Bencana (Dropdown: Banjir, Gempa Bumi, Longsor, Karhutla, dll.).
  2. Wilayah Kemendagri (Provinsi $\rightarrow$ Kab/Kota $\rightarrow$ Kecamatan).
  3. Waktu Kejadian Riil (Tanggal & Jam).
  4. Judul Ringkas Laporan & Narasi Kronologi.
  5. Rincian Dampak Lapangan (Korban & Kerusakan).
  6. Sumber Informasi Awal (contoh: *"Laporan Telepon Pusdalops BPBD Kab. Agam"*).
  7. Status Awal: Langsung dapat disetel `TERVERIFIKASI` atau `PENDING`.
* **Penyimpanan**: Disimpan dengan flag `is_manual_entry = TRUE`.

### 5.3. Modal Pop-up: "Gabung Berita Susulan" (`[🔗 Merge]`)
Digunakan ketika dua temuan di dasbor ternyata merupakan peristiwa yang sama:
* Operator menekan `[🔗 Gabung]` pada Kejadian B.
* Modal memunculkan daftar kejadian aktif dalam siklus tersebut.
* Operator memilih Kejadian A sebagai kejadian induk.
* **Aksi Sistem**:
  1. Seluruh artikel berita (`berita_bencana`) yang melekat pada Kejadian B dipindahkan ke Kejadian A.
  2. Kejadian B dihapus dari antrean aktif dan dicatat ke log audit.
  3. Kejadian A diperbarui jumlah rujukan medianya.

---

## 6. Spesifikasi Skema Basis Data (*Database Architecture*)

Sistem dibangun menggunakan Django ORM dengan tipe universal **`models.JSONField`** yang secara otomatis kompatibel dengan **SQLite (lingkungan pengujian lokal)** dan memetakan secara native ke **PostgreSQL `JSONB` (lingkungan server produksi)** tanpa perubahan kode.

| Nama Tabel | Fungsi Utama | Kolom Kunci & Tipe Data |
|---|---|---|
| `master_wilayah` | Hierarki kode dan nama wilayah Kemendagri | `id_wilayah` (VARCHAR PK), `nama_wilayah` (VARCHAR), `level` (ENUM: PROVINSI, KAB_KOTA, KECAMATAN), `parent_id` (FK) |
| `siklus_laporan` | Penguncian rentang 24 jam operasional | `kode_siklus` (VARCHAR PK: `SIKLUS-YYYYMMDD`), `waktu_buka` (TIMESTAMPTZ), `waktu_tutup` (TIMESTAMPTZ), `is_locked` (BOOLEAN), `locked_by` (VARCHAR), `locked_at` (TIMESTAMPTZ) |
| `kejadian_bencana` | Data faktual lapangan kejadian bencana | `id_kejadian` (SERIAL PK), `kode_kejadian` (VARCHAR UNIQUE), `kode_siklus` (FK), `jenis_bencana` (VARCHAR), `id_wilayah` (FK NULLABLE), `waktu_kejadian_riil` (TIMESTAMPTZ), `waktu_kejadian_text` (VARCHAR), `dampak_korban` (JSONField), `dampak_kerusakan` (JSONField), `upaya` (TEXT), `kondisi_mutakhir` (TEXT), `status_verifikasi` (ENUM: PENDING, TERVERIFIKASI, HOAKS), `is_manual_entry` (BOOLEAN), `is_isu_bantuan` (BOOLEAN) |
| `berita_bencana` | Tautan media hasil tarikan scraper/RSS | `id_berita` (SERIAL PK), `id_kejadian` (FK), `judul` (VARCHAR), `url_artikel` (TEXT), `nama_portal` (VARCHAR), `isi_ringkas` (TEXT), `waktu_terbit` (TIMESTAMPTZ), `similarity_score` (FLOAT), `is_master_source` (BOOLEAN) |
| `log_audit_verifikasi` | Rekaman jejak forensik verifikasi | `id_log` (SERIAL PK), `id_kejadian` (FK), `id_user` (VARCHAR), `shift` (VARCHAR), `status_sebelum` (VARCHAR), `status_sesudah` (VARCHAR), `kontak_bpbd_dihubungi` (VARCHAR), `catatan` (TEXT), `waktu_aksi` (TIMESTAMPTZ) |

---

## 7. Spesifikasi Dual Output (*Export Specifications*)

### 7.1. Luaran 1: Teks Ringkasan WhatsApp (Pimpinan)
Teks tersusun otomatis per alfabet klaster bencana, menggunakan frasa baku dinas, dan siap disalin ke WhatsApp:

```text
*LAPORAN HARIAN SITUASI BENCANA PUSDALOPS BNPB*
*PERIODE SIKLUS: 09 OKTOBER 2026 (07.00 WIB) - 10 OKTOBER 2026 (07.00 WIB)*
Status Data: TERVERIFIKASI

*A. BANJIR & CUACA EKSTREM*
1. KAB. BANDUNG, JAWA BARAT (Kec. Dayeuhkolot)
   - Waktu: 09/10/2026, 13:45 WIB
   - Dampak: Nihil korban jiwa; 2 Luka Ringan; 450 Jiwa Mengungsi; 127 Rumah Terendam.
   - Upaya: TRC BPBD Kab. Bandung mengerahkan 3 perahu karet & mendirikan tenda darurat.
   - Kondisi Terkini: TMA genangan air 40-70 cm, cuaca gerimis, situasi aman terkendali.
   - Konfirmasi: Satgas BPBD Kab. Bandung (Budi Santoso)
   - Referensi: Detikcom (Lead) & 3 Portal Berita

*B. GEMPA BUMI*
1. KOTA BITUNG, SULAWESI UTARA
   - Waktu: 09/10/2026, 18:22 WIB
   - Parameter: M 5.2, Kedalaman 8 km, Tidak berpotensi tsunami.
   - Dampak: Nihil korban jiwa & nihil kerusakan sarana prasarana.
   - Konfirmasi: Pusdalops BPBD Kota Bitung & BMKG Wilayah IV

_Pusdalops Penanggulangan Bencana BNPB RI - Hotline 117_
```

### 7.2. Luaran 2: Berkas Microsoft Word (`.docx`) Bagian A Resmi BNPB
Dokumen dinas resmi yang dibuat menggunakan pustaka `python-docx` dengan durasi komputasi $\le 5$ detik:
* **Kop Resmi**: Lambang Pusdalops BNPB, Arial Bold 13 pt, warna *Deep Navy* (`#002060`).
* **Format Penomoran**: Judul huruf kapital tebal.
* **Format Atribut Peluru (*Bullet Identation*)**:
  * ➢ **Waktu Kejadian**
  * ➢ **Lokasi Kejadian** (*Desa/Kecamatan, Kabupaten/Kota, Provinsi*)
  * ➢ **Kronologi**
  * ➢ **Korban Jiwa & Terdampak** *(Null-safety: "Nihil korban jiwa" jika 0)*
  * ➢ **Kerusakan Materil & Sarana Prasarana** *(Null-safety: "Nihil kerusakan" jika 0)*
  * ➢ **Upaya Penanganan TRC**
  * ➢ **Kondisi Mutakhir Lapangan**
  * ➢ **Kontak Konfirmasi & Portal Rujukan Media**

---

## 8. Spesifikasi Kebutuhan Non-Fungsional & Kinerja (*Performance & SLA*)

1. **Durasi Komputasi Ekspor Word**: $\le 5$ detik untuk 50 kejadian terverifikasi.
2. **Akurasi Deduplikasi**: Lapis 1 ($\ge 0.80$) dan Lapis 2 ($\ge 0.60$ dengan kesamaan wilayah & waktu).
3. **Ketersediaan Layanan**: Arsitektur *fault-tolerant*; bila salah satu RSS media atau API BMKG down/timeout, antrean berita lainnya tetap berjalan normal.
4. **Keamanan & Integritas**: Siklus yang telah dikunci (*Locked*) memiliki proteksi *write-block*, dapat dibuka hanya oleh otorisasi supervisor via tombol *Emergency Unlock*.

---

## 9. Rencana Kerja & Tahapan Pengembangan (*Implementation Roadmap*)

* **Tahap 1: Backend Database & Model ORM** (Model `siklus_laporan`, `master_wilayah`, `kejadian_bencana`, `berita_bencana`, `log_audit_verifikasi` + Seeding wilayah Kemendagri).
* **Tahap 2: Windowing Engine & Ingestion Filtering** (Helper pemotong siklus 07.00–07.00 WIB, filter gempa adaptif, dan endpoint trigger sync manual).
* **Tahap 3: Antarmuka Web (UI 4 Menu) & 3 Modal Interaktif** (Dasbor pemantauan aktif, Modal Verifikasi 5 Blok, Modal Tambah Manual, dan Modal Merge).
* **Tahap 4: Dual Output Generator** (Generator Teks WhatsApp & Word Bagian A resmi $\le 5\text{ detik}$).
* **Tahap 5: Pengujian Bersama & UAT**.

---
*Dokumen ini merupakan acuan tunggal (*Single Source of Truth*) yang 100% final dan siap dieksekusi ke kode program.*
