# SYSTEM ARCHITECTURE & UI/UX DESIGN SPECIFICATION
## Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB
**Berkas:** `DESIGN.md`  
**Versi:** 2.2.0-FINAL  
**Tanggal:** 10 Oktober 2026  
**Status:** Disetujui 100% & Terkunci untuk Implementasi (*Final Approved Blueprint*)  
**Dokumen Induk:** [`PRD.md`](file:///c:/Users/athal/Documents/bnpb_disaster_system/PRD.md)  

---

## 1. Design System & Pedoman Visual (*Design Tokens*)

Antarmuka dirancang secara khusus untuk lingkungan **Ruang Kendali Operasi (Pusdalops Situation Room 24/7)** mengusung gaya **Tactical Modernism** dan **High-Density Utilitarianism**. Seluruh tata letak dioptimalkan untuk monitor command center ($1920 \times 1080$ piksel) dengan nol ornamen berlebih, menjaga ketajaman visual operator selama rotasi kerja shift 24 jam penuh.

### 1.1. Tipografi & Skala Huruf (*Typography System*)
Sistem menggunakan font utama **Plus Jakarta Sans** (alternatif fallback: **Inter**, serta **JetBrains Mono** untuk angka tabular/waktu/kode) guna menjamin keterbacaan data numerik dan teks laporan bencana:

| Tingkat (*Hierarchy*) | Ukuran (*Size*) | Ketebalan (*Weight*) | Jarak Baris (*Line Height*) | Penggunaan Komponen |
|---|---|---|---|---|
| **Display / Header 1** | 20px (`text-xl`) | SemiBold (600) | 28px | Judul header navigasi (*"PUSDALOPS BNPB"*). |
| **Header 2** | 16px (`text-base`) | Bold (700) | 24px | Judul modal & rentang teks Siklus 24 Jam. |
| **Section Title** | 14px (`text-sm`) | SemiBold (600) | 20px | Header tab status & judul blok modal (Blok 1–5). |
| **Table Header** | 11px (`text-xs`) | Bold (700) - Uppercase | 16px | Kolom tabel (`WAKTU`, `WILAYAH`, `JENIS`, `STATUS`, `AKSI`). |
| **Body / Headline** | 13px (`text-sm`) | Medium (500) | 18px | Judul tautan berita & nama wilayah administratif. |
| **Body Text / Snippet** | 12px (`text-xs`) | Regular (400) | 16px | Ringkasan narasi artikel 2 baris & catatan konfirmasi. |
| **Badge / Caption** | 11px (`text-[11px]`) | SemiBold (600) | 14px | Counter tab, timer cut-off, chip jenis bencana. |

---

### 1.2. Token Warna & Palet Visual Resmi BNPB (*Tactical Palette*)

#### A. Identitas Utama (*Brand Colors*)
* **BNPB Emergency Orange**: `#EA580C` (Primary CTA, tombol Unduh Word, aksen tab aktif).
* **Orange Hover**: `#C2410C` (Status tombol saat kursor melayang).
* **Deep Navy Slate**: `#0B192C` (Background Top Navigation Bar).
* **Dark Slate Sub-Nav**: `#1E293B` (Garis pemisah dan aksen sidebar/footer).

#### B. Permukaan & Latar Belakang (*Surfaces*)
* **Canvas Base**: `#F8FAFC` (Latar belakang utama kanvas aplikasi - minim ketegangan mata).
* **Surface White**: `#FFFFFF` (Latar kontainer kartu tabel dan formulir modal).
* **Border Neutral**: `#E2E8F0` (Garis tepi tipis 1px pemisah baris tabel dan kartu).
* **Table Header Fill**: `#F1F5F9` (Latar abu-abu terang kepala tabel).

#### C. Warna Status Kedaruratan (*Semantic Indicators*)
* **Pending / Belum Terverifikasi**: Teks `#B45309`, Latar `#FEF3C7`, Border `#FDE68A` (Amber).
* **Terverifikasi / Sah**: Teks `#047857`, Latar `#D1FAE5`, Border `#A7F3D0` (Emerald Green).
* **Hoaks / Ditolak**: Teks `#B91C1C`, Latar `#FEE2E2`, Border `#FECACA` (Crimson Red).
* **Isu Bantuan / Keluhan Logistik**: Teks `#FFFFFF`, Latar `#DC2626` (Red Alert Chip `[🚨 ISU BANTUAN]`).
* **Aksi WhatsApp**: Teks `#FFFFFF`, Latar `#16A34A` (Tombol Salin Format WA).

```css
:root {
    /* Brand Tokens */
    --bnpb-orange: #EA580C;
    --bnpb-orange-hover: #C2410C;
    --bnpb-navy-slate: #0B192C;
    --bnpb-slate-subnav: #1E293B;

    /* Surface Tokens */
    --bnpb-canvas: #F8FAFC;
    --bnpb-surface-white: #FFFFFF;
    --bnpb-border-neutral: #E2E8F0;
    --bnpb-th-fill: #F1F5F9;

    /* Semantic Status Tokens */
    --status-pending-text: #B45309;
    --status-pending-bg: #FEF3C7;
    --status-pending-border: #FDE68A;

    --status-verified-text: #047857;
    --status-verified-bg: #D1FAE5;
    --status-verified-border: #A7F3D0;

    --status-hoax-text: #B91C1C;
    --status-hoax-bg: #FEE2E2;
    --status-hoax-border: #FECACA;

    --status-isu-bantuan: #DC2626;
    --action-wa: #16A34A;
}
```

---

### 1.3. Dimensi Komponen & Spasi (*Sizing & Spacing*)

* **Top Navigation Bar**: Tinggi tetap `64px`, padding horizontal `24px` (`px-6`), latar `#0B192C`.
* **Banner Siklus 24 Jam**: Tinggi `48px`, padding horizontal `20px` (`px-5`), latar `#FFFFFF`, border bawah 1px solid `#E2E8F0`.
* **Baris Kontrol Tab & Aksi**: Jarak antar-tombol `12px` (`gap-3`), margin bawah `16px` (`mb-4`).
* **Tabel Pemantauan (High-Density Grid)**:
  * Tinggi baris kepala tabel (*Header Row*): `36px`.
  * Tinggi baris data (*Data Row*): `56px` s.d. `64px` (padat informasi tanpa whitespace berlebih).
  * Padding sel tabel: `py-3 px-4`.
* **Formulir Modal (5 Blok)**:
  * Lebar maksimal (*Max Width*): `768px` s.d. `800px` (terpusat horizontal).
  * Sudut membulat (*Border Radius*): `rounded-lg` (8px) atau `rounded-xl` (12px).
  * Bayangan (*Drop Shadow*): `shadow-2xl` dengan latar belakang semi-transparan `rgba(15, 23, 42, 0.6)` (*backdrop-blur*).

---

### 1.4. Bentuk Komponen Interaktif (*UI Components Spec*)

* **Chip Hierarki Wilayah Kemendagri**:
  * Format visual: Badge abu-abu netral dengan border halus (`bg-slate-100 text-slate-700 text-xs px-2 py-0.5 rounded`).
  * Teks berformat penanda: `Jawa Barat > Kab. Bandung > Kec. Dayeuhkolot`.
* **Dropdown Status Baris Tabel**:
  * Tinggi: `32px` (`h-8`), teks 12px, padding horizontal 8px.
  * Warna latar dropdown otomatis berubah mengikuti status yang dipilih:
    * 🟡 Kuning saat **Pending** (`bg-[#FEF3C7] text-[#B45309] border-[#FDE68A]`).
    * 🟢 Hijau saat **Terverifikasi** (`bg-[#D1FAE5] text-[#047857] border-[#A7F3D0]`).
    * 🔴 Merah saat **Hoaks** (`bg-[#FEE2E2] text-[#B91C1C] border-[#FECACA]`).
* **Tombol Ekspor (Dual Output)**:
  * **Tombol WA**: Tinggi `36px`, font 12px SemiBold, ikon salin + teks, warna latar `#16A34A` (`hover:bg-green-700 text-white`).
  * **Tombol Word**: Tinggi `36px`, font 12px SemiBold, ikon dokumen + teks, warna latar `#EA580C` (`hover:bg-[#C2410C] text-white`).

---

## 2. Arsitektur Informasi & Peta Situs (*Sitemap*)

Sistem memiliki navigasi terpusat dengan **4 Menu Utama** pada Header Komando:

```
[ HEADER UTAMA: Identitas BNPB + 4 Menu + Badge Operator + Jam WIB Live + Tombol [🔄 Sync Now] ]
  ├── 1. [Dasbor Pemantauan]   (/)           ── Meja kerja aktif verifikasi harian & tabel grid kejadian
  ├── 2. [Riwayat Bencana]     (/history/)   ── Arsip logbook kejadian lampau per siklus harian
  ├── 3. [Pusat Ekspor]        (/reports/)   ── Preview Bagian A, Lock & Emergency Unlock Supervisor
  └── 4. [Pengaturan & Master] (/settings/)  ── Manajemen Petugas RBAC, Master Wilayah Kemendagri
```

---

## 3. Spesifikasi Wireframe & Tata Letak Antarmuka (*UI Wireframes*)

### 3.1. Menu 1: Dasbor Pemantauan (Halaman Kerja Meja Piket 24 Jam)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [▲] PUSDALOPS BNPB               Dasbor Pemantauan  Riwayat Bencana  Pusat Ekspor  Pengaturan & Master │
│     Sistem Pemantauan 24 Jam       (Border Oranye)                                                     │
│                                           [👤 Operator: Budi (Shift 1)]  [🕒 13:45 WIB]  [🔄 Sync Now]  │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SIKLUS OPERASIONAL: 09 OKTOBER 2026 (07.00 WIB) - 10 OKTOBER 2026 (07.00 WIB)                         │
│ [◀ Sebelumnya] [Berikutnya ▶]                              [⏳ 06j 18m menuju cut-off 07.00 WIB]       │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [TAB STATUS DINAMIS DENGAN PILL COUNTERS]                [BARIS AKSI CEPAT / ACTION BUTTONS]           │
│ [ Belum Terverifikasi (14) ] [ Terverifikasi (6) ]        [+ Tambah Kejadian Manual]                    │
│ [ Hoaks (2) ]               [ Semua Data (22) ]          [📋 Salin Format WA]                         │
│                                                          [📄 Unduh Word (.docx) Bagian A]              │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [BAR PENCARIAN & FILTER MULTI-DIMENSI]                                                                 │
│ 🔍 [ Cari kata kunci, wilayah, nama bencana...        ]                                                │
│ [ Semua Provinsi (38) ▼ ]  [ Semua Jenis Bencana ▼ ]  [ Tingkat Urgensi ▼ ]  [🟢 Auto-refresh: 30s]    │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [HIGH-DENSITY DATA GRID / TABEL MONITORING RESMI]                                                      │
│ ┌──────────────┬──────────────────┬──────────────┬──────────────────────────────┬──────────┬─────────┐ │
│ │ WAKTU (WIB)  │ WIL. KEMENDAGRI  │ JENIS BENCAN │ RINGKASAN & RUJUKAN MEDIA    │ STATUS   │ AKSI    │ │
│ ├──────────────┼──────────────────┼──────────────┼──────────────────────────────┼──────────┼─────────┤ │
│ │ 09/10/2026   │ 32.04.11         │ 💧 BANJIR    │ Banjir Luapan Citarum Rendam │ [Pending │ [🔗 Mrg]│ │
│ │ 13:45 WIB    │ Jabar > Bandung  │              │ Ratusan Rumah di Dayeuhkolot │   ▼    ] │ [✏️ Edit│ │
│ │ (15m lalu)   │ Kec. Dayeuhkolot │              │ [Detikcom (Lead)] +2 Portal  │          │  & Ver] │ │
│ ├──────────────┼──────────────────┼──────────────┼──────────────────────────────┼──────────┼─────────┤ │
│ │ 09/10/2026   │ 94.01.01         │ 🔥 KARHUTLA  │ [🚨 ISU BANTUAN] Karhutla 172│ [Pending │ [🔗 Mrg]│ │
│ │ 11:20 WIB    │ Papua Tengah >   │              │ Ha Lahan Gambut Nabire...    │   ▼    ] │ [✏️ Edit│ │
│ │ (2j 40m lalu)│ Distrik Nabire   │              │ [Antara News (Lead)]         │          │  & Ver] │ │
│ ├──────────────┼──────────────────┼──────────────┼──────────────────────────────┼──────────┼─────────┤ │
│ │ 09/10/2026   │ 31.72.01         │ 🌊 GEMPA /   │ [🚨 DISINFORMASI] Video Hoaks│ [Hoaks   │ [🔗 Mrg]│ │
│ │ 08:30 WIB    │ DKI > Jakut >    │    TSUNAMI   │ Tsunami Teluk Jakarta...     │   ▼    ] │ [✏️ Edit│ │
│ │ (6j 15m lalu)│ Kec. Penjaringan │              │ [TikTok Viral & WAG]         │          │  & Ver] │ │
│ └──────────────┴──────────────────┴──────────────┴──────────────────────────────┴──────────┴─────────┘ │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Menampilkan 1 - 4 dari 14 data pending • Total: 22   [◀ Prev] [1] [2] [3] [Next ▶]  InaRISK: TERHUBUNG │
│                                                                                     BMKG: SINKRON      │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.2. Modal Pop-up: Formulir "Verifikasi Lapangan & Koreksi Metadata" (5 Blok Ringkas)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ [FORM VERIFIKASI #DAY-202610-001] [PRIORITAS TINGGI]                           [ESC / ✕]│
│ Verifikasi Lapangan & Koreksi Metadata Kejadian                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ 📰 RUJUKAN BERITA SIBER AWAL:                                                           │
│ Detikcom (Lead) • Diterbitkan 09/10/2026 13:45 WIB                                      │
│ "Banjir Luapan Citarum Rendam Ratusan Rumah di Dayeuhkolot"  [↗ Buka Berita Asli]       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [1] WILAYAH ADMINISTRATIF KEMENDAGRI (Kode: 32.04.11)                                   │
│ Provinsi: [ 32 - Jawa Barat        ▼ ]  Kab/Kota: [ 32.04 - Kab. Bandung            ▼ ] │
│ Kecamatan: [ 32.04.11 - Dayeuhkolot  ▼ ]                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [2] WAKTU KEJADIAN RIIL (TERVALIDASI)                                                   │
│ Tanggal Kejadian: [ 2026-10-09 📅 ]      Waktu Kejadian Riil: [ 13:45 WIB 🕒 ]          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [3] FAKTA DAMPAK LAPANGAN FAKTUAL                                                       │
│ Korban Jiwa:                                                                            │
│   Meninggal: [ 0 ] Jiwa   Luka: [ 2 ] Jiwa   Hilang: [ 0 ] Jiwa   Mengungsi: [ 450 ] Jiwa│
│   Lokasi Pengungsi Utama: [ Posko Kantor Desa Dayeuhkolot & Masjid As-Shofia          ] │
│ Kerusakan Aset:                                                                         │
│   Rumah Terendam: [ 127 ] Unit               Luas Terdampak: [ 15 ] Ha                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [4] UPAYA TRC & KONDISI MUTAKHIR                                                        │
│ Upaya Penanganan TRC:                                                                   │
│ [ TRC BPBD Kab. Bandung mendirikan 2 tenda darurat dan menerjunkan 3 perahu karet.    ] │
│ Kondisi Terkini di Lapangan:                                                            │
│ [ Tinggi muka air genangan 40-70 cm, cuaca gerimis, evakuasi warga terkendali.        ] │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [5] STATUS VERIFIKASI & AUDIT PETUGAS                                                   │
│ Keputusan Verifikasi:                                                                   │
│ ( ) ⏳ Pending / Antrean    (•) 🟢 Terverifikasi Resmi    ( ) 🔴 Hoaks / Ditolak        │
│                                                                                         │
│ Personel Satgas yang Dikonfirmasi: [ Budi Santoso (TRC BPBD Kab. Bandung)           ✓ ] │
│ Catatan Verifikasi               : [ Divalidasi via telepon, data konsisten           ] │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Operator: Shift 1 (Budi) • Sesi: JKT-PST-01 • Siklus 09 Okt 2026                        │
│                                            [ Batal ]   [ 💾 Simpan & Perbarui Data ]    │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.3. Modal Pop-up: Formulir "Tambah Laporan Kejadian Manual" (`FORM: DI-01/BNPB`)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ [AD-HOC INCIDENT ENTRY] [FORM: DI-01/BNPB]                                     [ESC / ✕]│
│ Tambah Laporan Kejadian Manual (Ad-Hoc Entry)                                           │
│ Input cepat laporan mendesak via telepon satgas darurat atau radio HF daerah.           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [1] INFORMASI AWAL & KLASIFIKASI                                                        │
│ Jenis Bencana: [ Tanah Longsor (Geologi)   ▼ ]  Siklus: [ SIKLUS-20261009 (Berjalan) ▼]│
│ Saluran Masuk: [ Panggilan Telepon Pusdalops BPBD Kab. Agam (Radio HF Kanal 2)       ] │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [2] WILAYAH ADMINISTRATIF KEMENDAGRI (Kode: 13.06.12)                                   │
│ Provinsi: [ 13 - Sumbar ▼ ]  Kab/Kota: [ 13.06 - Kab. Agam ▼ ]  Kecamatan: [ Malalak ▼ ]│
│ Lokasi Spesifik: [ Jorong Campago, Nagari Malalak Selatan (Jalur Alternatif Km 42)    ] │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [3] WAKTU & KRONOLOGI KEJADIAN                                                          │
│ Tanggal Terjadi: [ 2026-10-10 📅 ]       Waktu Terjadi: [ 08:30 WIB 🕒 ]                 │
│ Kronologi Ringkas:                                                                      │
│ [ Hujan deras berintensitas tinggi memicu tebing setinggi 20m longsor menutup jalan.  ] │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [4] DAMPAK FAKTUAL LAPANGAN                                                             │
│ Meninggal: [ 0 ] Jiwa   Luka: [ 0 ] Jiwa   Hilang: [ 0 ] Jiwa   Mengungsi: [ 12 ] Jiwa   │
│ Kerusakan Fisik & Sarpras:                                                              │
│ [ 2 unit rumah warga tertimbun material lumpur, tiang listrik roboh, akses jalan putus] │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [5] PENANGANAN TRC & STATUS AWAL                                                        │
│ Upaya TRC: [ BPBD Kab. Agam bersama TNI/Polri di lokasi, koordinasi alat berat loader ] │
│ Klasifikasi Validasi Awal:                                                              │
│ (•) 🟢 Langsung Terverifikasi (Data bersumber dari otoritas BPBD resmi & radio satgas)  │
│ ( ) ⏳ Simpan sebagai Pending  (Memerlukan cross-check lapangan lanjutan oleh analis)    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Operator Pencatat: Shift 1 (Budi) • CLUSTER: JKT-PST-01                                 │
│                                            [ Batal ]   [ 💾 Simpan Kejadian Baru ]      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.4. Modal Pop-up: "Gabung Berita Susulan" (`[🔗 Merge]`)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ GABUNGKAN BERITA SUSULAN KE KEJADIAN INDUK                     [X Tutup]                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ Berita yang Digabungkan:                                                                │
│ "Banjir Dayeuhkolot Meluas, 500 Rumah Terendam" (Kompas.com - 14:20 WIB)                │
│                                                                                         │
│ Pilih Kejadian Induk Target dalam Siklus Ini:                                           │
│ (•) [BNPB-20261009-001] Banjir Dayeuhkolot Kab. Bandung (Detik.com - 13:45 WIB)         │
│ ( ) [BNPB-20261009-003] Genangan Air Cicaheum Kota Bandung (Antara - 12:10 WIB)         │
│                                                                                         │
│ ℹ️ Catatan Sistem: Seluruh artikel berita akan dipindahkan ke kejadian induk, dan       │
│    kejadian duplikat ini akan diarsipkan secara otomatis.                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                [ Batal ]   [ 🔗 Konfirmasi Gabung ]     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.5. Menu 3: Pusat Ekspor Laporan (*Lock & Emergency Unlock*)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PUSDALOPS PB  •  PUSAT EKSPOR LAPORAN SITUASI (SITREP BAGIAN A)                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Periode Siklus: SIKLUS-20261009 (09/10/2026 07.00 - 10/10/2026 07.00 WIB)               │
│ Status Dokumen: 🟢 DRAF TERBUKA  (Bisa diedit)                                         │
│                                                                                        │
│ [ 📄 Unduh Berkas Word (.docx) Resmi Bagian A ]   [ 🔒 Kunci Siklus (Lock Snapshot) ]  │
│                                                                                        │
│ *(Jika Siklus Terkunci oleh Supervisor)*:                                               │
│ 🔒 STATUS SIKLUS: TERKUNCI OLEH KASUBDIT PADA 10/10/2026 07:15 WIB                     │
│ [ 📄 Unduh Dokumen Word ]   [ 🔓 Buka Kunci Darurat (Emergency Unlock - Supervisor) ]  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [PRATINJAU NASKAH RESMI DINAS PUSDALOPS BNPB]                                          │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │                     BADAN NASIONAL PENANGGULANGAN BENCANA                          │ │
│ │                  PUSAT PENGENDALIAN OPERASI (PUSDALOPS PB)                         │ │
│ │                       LAPORAN HARIAN SITUASI BENCANA                               │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Spesifikasi Skema Database Fisik (*Universal ORM Architecture*)

Basis data relasional dengan 5 tabel inti berintegritas referensial dan dukungan universal `models.JSONField`:

```sql
-- 1. TABEL MASTER WILAYAH KEMENDAGRI
CREATE TABLE master_wilayah (
    id_wilayah VARCHAR(30) PRIMARY KEY,      -- Contoh: '32.04.11'
    nama_wilayah VARCHAR(150) NOT NULL,      -- Contoh: 'DAYEUHKOLOT'
    level VARCHAR(20) NOT NULL,              -- 'PROVINSI', 'KAB_KOTA', 'KECAMATAN'
    parent_id VARCHAR(30) REFERENCES master_wilayah(id_wilayah) ON DELETE CASCADE
);
CREATE INDEX idx_wilayah_level ON master_wilayah(level);
CREATE INDEX idx_wilayah_parent ON master_wilayah(parent_id);

-- 2. TABEL SIKLUS LAPORAN 24 JAM
CREATE TABLE siklus_laporan (
    kode_siklus VARCHAR(30) PRIMARY KEY,     -- Contoh: 'SIKLUS-20261009'
    waktu_buka TIMESTAMPTZ NOT NULL,         -- 2026-10-09 07:00:00+07
    waktu_tutup TIMESTAMPTZ NOT NULL,        -- 2026-10-10 07:00:00+07
    is_locked BOOLEAN DEFAULT FALSE,
    locked_by VARCHAR(100),
    locked_at TIMESTAMPTZ
);
CREATE INDEX idx_siklus_locked ON siklus_laporan(is_locked);

-- 3. TABEL KEJADIAN BENCANA FAKTUAL
CREATE TYPE status_verif_enum AS ENUM ('PENDING', 'TERVERIFIKASI', 'HOAKS');

CREATE TABLE kejadian_bencana (
    id_kejadian SERIAL PRIMARY KEY,
    kode_kejadian VARCHAR(50) UNIQUE NOT NULL, -- Contoh: 'BNPB-20261009-001'
    kode_siklus VARCHAR(30) REFERENCES siklus_laporan(kode_siklus) ON DELETE RESTRICT,
    jenis_bencana VARCHAR(100) NOT NULL,       -- 'Banjir', 'Gempa Bumi', 'Karhutla', dll.
    id_wilayah VARCHAR(30) REFERENCES master_wilayah(id_wilayah),
    
    -- Metadata Riil Hasil Konfirmasi
    waktu_kejadian_riil TIMESTAMPTZ,
    waktu_kejadian_text VARCHAR(150),
    
    -- Dampak Lapangan (JSONField Universal)
    dampak_korban JSONB DEFAULT '{"meninggal": 0, "luka_berat": 0, "luka_ringan": 0, "hilang": 0, "mengungsi": 0}',
    dampak_kerusakan JSONB DEFAULT '{"rumah_rb": 0, "rumah_rs": 0, "rumah_rr": 0, "rumah_terendam": 0, "fasum": 0, "luas_ha": 0}',
    
    upaya TEXT DEFAULT '• Dalam koordinasi dengan BPBD setempat',
    kondisi_mutakhir TEXT DEFAULT '• Situasi terpantau aman terkendali',
    
    status_verifikasi status_verif_enum DEFAULT 'PENDING',
    is_manual_entry BOOLEAN DEFAULT FALSE,
    is_isu_bantuan BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_kejadian_siklus ON kejadian_bencana(kode_siklus);
CREATE INDEX idx_kejadian_status ON kejadian_bencana(status_verifikasi);

-- 4. TABEL BERITA BENCANA (ARTIKEL TERIKAT HASIL CLUSTERING)
CREATE TABLE berita_bencana (
    id_berita SERIAL PRIMARY KEY,
    id_kejadian INT REFERENCES kejadian_bencana(id_kejadian) ON DELETE CASCADE,
    judul VARCHAR(500) NOT NULL,
    url_artikel VARCHAR(1000) NOT NULL,
    nama_portal VARCHAR(100) NOT NULL,        -- 'Detik.com', 'Kompas.com', 'BMKG'
    isi_ringkas TEXT,
    waktu_terbit TIMESTAMPTZ,
    similarity_score FLOAT DEFAULT 1.0,
    is_master_source BOOLEAN DEFAULT FALSE
);
CREATE INDEX idx_berita_kejadian ON berita_bencana(id_kejadian);

-- 5. TABEL LOG AUDIT VERIFIKASI FORENSIK
CREATE TABLE log_audit_verifikasi (
    id_log SERIAL PRIMARY KEY,
    id_kejadian INT REFERENCES kejadian_bencana(id_kejadian) ON DELETE CASCADE,
    id_user VARCHAR(100) NOT NULL,           -- Akun operator piket
    shift VARCHAR(50) NOT NULL,              -- 'Shift 1 (07.00 - 15.00 WIB)'
    status_sebelum VARCHAR(30) NOT NULL,
    status_sesudah VARCHAR(30) NOT NULL,
    kontak_bpbd_dihubungi VARCHAR(200),      -- Nama personel BPBD yang dikonfirmasi
    catatan TEXT,
    waktu_aksi TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_audit_kejadian ON log_audit_verifikasi(id_kejadian);
```

---

## 5. Alur Interaksi Pengguna & Logika Bisnis (*Business Logic*)

### 5.1. Logika Penentuan Siklus Otomatis (Helper Function)
```python
import datetime
import zoneinfo

WIB = zoneinfo.ZoneInfo("Asia/Jakarta")

def get_current_operational_cycle(dt: datetime.datetime = None) -> str:
    """
    Menghasilkan kode siklus 24 jam dengan cut-off pukul 07.00 WIB.
    Contoh:
    - 2026-10-09 14:00 WIB -> SIKLUS-20261009
    - 2026-10-10 02:00 WIB -> SIKLUS-20261009 (karena belum jam 07.00 WIB)
    - 2026-10-10 07:00:01 WIB -> SIKLUS-20261010
    """
    if dt is None:
        dt = datetime.datetime.now(WIB)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=WIB)

    if dt.hour < 7:
        cycle_date = dt.date() - datetime.timedelta(days=1)
    else:
        cycle_date = dt.date()

    return f"SIKLUS-{cycle_date.strftime('%Y%m%d')}"
```

### 5.2. Logika Deduplikasi 2 Lapis (*Two-Tier Deduplication*)
```python
def check_is_duplicate(new_article, existing_event) -> bool:
    """
    Lapis 1: Cosine similarity teks >= 0.80 -> Otomatis duplikat.
    Lapis 2: Jika Kab/Kota sama & Bencana sama & Waktu < 24 jam -> Threshold 0.60.
    """
    score = calculate_cosine_similarity(new_article.text, existing_event.lead_text)
    if score >= 0.80:
        return True
    
    if (new_article.kab_kota == existing_event.kab_kota and 
        new_article.jenis_bencana == existing_event.jenis_bencana and
        time_difference_hours(new_article.published_at, existing_event.created_at) < 24):
        if score >= 0.60:
            return True
            
    return False
```

---

## 6. Spesifikasi Dual Output Generator

### 6.1. Mesin Ekspor Teks WhatsApp (Pimpinan)
* Mengelompokkan kejadian `TERVERIFIKASI` berdasarkan alfabet klaster bencana (**A. BANJIR & CUACA EKSTREM**, **B. GEMPA BUMI**, dll.).
* Menggunakan frasa baku dinas: *"Nihil korban jiwa"*, *"Situasi aman terkendali"*.
* Dilengkapi tombol satu-klik `navigator.clipboard.writeText()` dengan toast notifikasi.

### 6.2. Mesin Dokumen Word (`python-docx`) Bagian A
* **Latensi Komputasi**: $\le 5$ detik streaming langsung via HTTP response Django.
* **Layout Sesuai Tata Naskah Dinas BNPB**:
  * Margin 1 inci di keempat sisi.
  * Kop surat: Arial Bold 13 pt, warna Biru Pusdalops `#002060`.
  * Format peluru hierarkis:
    * ➢ **Waktu Kejadian**
    * ➢ **Lokasi Kejadian**
    * ➢ **Kronologi**
    * ➢ **Korban Jiwa & Terdampak** *(Null-safety: "Nihil korban jiwa" jika 0)*
    * ➢ **Kerusakan Materil & Sarana Prasarana** *(Null-safety: "Nihil kerusakan" jika 0)*
    * ➢ **Upaya Penanganan TRC**
    * ➢ **Kondisi Mutakhir Lapangan**
    * ➢ **Kontak Konfirmasi & Portal Rujukan Media**

---

## 7. Rencana Kerja Implementasi Bertahap (*Next Action Plan*)

| Tahap | Modul yang Dikerjakan | Target Hasil |
|---|---|---|
| **Tahap 1** | **Backend Database & Model ORM** | Membuat 5 model (`master_wilayah`, `siklus_laporan`, `kejadian_bencana`, `berita_bencana`, `log_audit_verifikasi`) + Seeding wilayah Kemendagri. |
| **Tahap 2** | **Windowing Engine & Ingestion Filtering** | Implementasi fungsi pemotong siklus 07.00–07.00 WIB, filter gempa adaptif, dan endpoint trigger sync manual. |
| **Tahap 3** | **Web UI (4 Menu) & 3 Modal Interaktif** | Dasbor pemantauan aktif, Modal Verifikasi 5 Blok, Modal Tambah Manual, dan Modal Merge. |
| **Tahap 4** | **Dual Output Generator** | Pembuat Teks Ringkasan WhatsApp & generator dokumen Word Bagian A resmi $\le 5\text{ detik}$. |
| **Tahap 5** | **UAT & Pengujian Komprehensif** | Verifikasi end-to-end dari penarikan data hingga unduh laporan dinas. |

---
*Dokumen ini merupakan cetak biru resmi desain teknis antarmuka dan basis data sistem pemantauan kebencanaan BNPB.*
