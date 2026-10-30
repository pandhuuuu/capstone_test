# BAB IV: HASIL PERANCANGAN

## 4.1 Proses Perancangan

Proses perancangan Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB dilaksanakan berdasarkan sistematika dan spesifikasi kebutuhan yang telah dirumuskan pada Bab III. Proses ini mencakup perancangan arsitektur sistem, skema basis data, dan algoritma inti.

### 4.1.1 Arsitektur Sistem 4-Tier (*High-Level Architecture*)

Arsitektur sistem dirancang menggunakan pendekatan modular 4-tier berlapis untuk menjamin skalabilitas, ketahanan terhadap kegagalan (*fault-tolerance*), serta kemudahan pemeliharaan (*maintainability*). Arsitektur sistem disajikan pada Gambar 4.1.

![Arsitektur Sistem 4-Tier](/docs/capstone/diagrams/gambar_4_1_arsitektur_sistem.png)
*Gambar 4.1 Arsitektur Sistem 4-Tier Pemantauan Kebencanaan Pusdalops BNPB*

Deskripsi per lapis (*layer*):
1. **Tier 1: External Data Sources & Feeds**:
   Lapisan sumber data eksternal yang mencakup:
   * **API BMKG**: Menarik data guncangan gempa bumi terkini (*real-time auto-earthquake feed*).
   * **RSS Media Daring Nasional**: Menarik artikel bencana terverifikasi (*Detikcom, Kompas.com, Antara News*).
   * **Portal Bencana Global (GDACS)**: Memantau potensi bencana berskala regional.
2. **Tier 2: Ingestion, Windowing & Intelligence Layer**:
   Lapisan pemrosesan latar belakang dan intelejen teks:
   * **Dual Trigger Ingestion**: Penjadwalan otomatis berkala via *Celery Beat* dan tombol instan *on-demand* `[🔄 Tarik Data Sekarang / Sync Now]`.
   * **Windowing Engine 24 Jam**: Memotong dan menetapkan artikel ke siklus dinas (07.00 – 07.00 WIB).
   * **Penyaring Gempa Adaptif**: Menyaring gempa $M \ge 5.0$ kedalaman $\le 20$ km atau $M \ge 4.5$ dengan guncangan dirasakan $\ge \text{III MMI}$.
   * **Deduplikasi 2 Lapis (NLP Cosine Similarity)**: Menghitung skor kemiripan teks menggunakan pembobotan TF-IDF untuk mencegah penumpukan berita ganda.
3. **Tier 3: Storage & Audit ORM Layer**:
   Lapisan penyimpanan data relasional terstruktur yang diakses melalui Django ORM:
   * Mengelola tabel `master_wilayah`, `siklus_laporan`, `kejadian_bencana`, `berita_bencana`, dan `log_audit_verifikasi`.
   * Memanfaatkan `JSONField` untuk fleksibilitas penyimpanan struktur dampak korban dan kerusakan.
4. **Tier 4: Presentation & Dual Output Layer**:
   Lapisan antarmuka pengguna berbasis web dan generator luaran resmi:
   * Antarmuka dasbor meja piket 4 tab status (`Pending`, `Terverifikasi`, `Hoaks`, `Semua Data`).
   * Formulir koreksi metadata 5 blok, formulir tambah kejadian manual, dan modal penggabungan berita (*merge*).
   * Generator dokumen Word (`.docx`) Bagian A resmi berstandar Tata Naskah Dinas BNPB ($\le 5$ detik) dan formatter pesan WhatsApp pimpinan.

---

### 4.1.2 Skema Relasi Basis Data (*Entity Relationship Diagram*)

Struktur basis data dirancang dengan derajat normalisasi tinggi untuk memastikan integritas data dan jejak audit forensik:

**Tabel 4.1 Kamus Data Skema Basis Data Pusdalops BNPB**
| Nama Tabel | Tipe Kunci | Kolom Utama | Tipe Data | Deskripsi Fungsi |
| :--- | :--- | :--- | :--- | :--- |
| `master_wilayah` | PK: `id_wilayah`<br>FK: `parent_id` | `nama_wilayah`<br>`level`<br>`parent_id` | VARCHAR(20)<br>ENUM<br>VARCHAR(20) | Menyimpan hierarki kode & nama wilayah Kemendagri (Provinsi, Kab/Kota, Kecamatan). |
| `siklus_laporan` | PK: `kode_siklus` | `waktu_buka`<br>`waktu_tutup`<br>`is_locked`<br>`locked_by`<br>`locked_at` | TIMESTAMPTZ<br>TIMESTAMPTZ<br>BOOLEAN<br>VARCHAR(100)<br>TIMESTAMPTZ | Mengatur rentang windowing 24 jam (`SIKLUS-YYYYMMDD`) dan status penguncian supervisor. |
| `kejadian_bencana` | PK: `id_kejadian`<br>FK: `kode_siklus`<br>FK: `id_wilayah` | `kode_kejadian`<br>`jenis_bencana`<br>`dampak_korban`<br>`dampak_kerusakan`<br>`status_verifikasi`<br>`is_isu_bantuan` | VARCHAR(50)<br>VARCHAR(50)<br>JSONField<br>JSONField<br>ENUM<br>BOOLEAN | Menyimpan entri fakta lapangan terverifikasi, status (`Pending`, `Terverifikasi`, `Hoaks`), dan badge bantuan. |
| `berita_bencana` | PK: `id_berita`<br>FK: `id_kejadian` | `judul`<br>`url_artikel`<br>`nama_portal`<br>`similarity_score`<br>`is_master_source` | VARCHAR(255)<br>TEXT<br>VARCHAR(100)<br>FLOAT<br>BOOLEAN | Menyimpan seluruh artikel berita media daring yang ditautkan ke kejadian induk (*multi-reference*). |
| `log_audit_verifikasi`| PK: `id_log`<br>FK: `id_kejadian` | `id_user`<br>`shift`<br>`status_sebelum`<br>`status_sesudah`<br>`catatan`<br>`waktu_aksi` | VARCHAR(100)<br>VARCHAR(20)<br>VARCHAR(20)<br>VARCHAR(20)<br>TEXT<br>TIMESTAMPTZ | Merekam setiap perubahan status, nama petugas daerah yang dikonfirmasi, dan alasan bantahan berita hoaks. |

---

### 4.1.3 Logika Algoritma Windowing dan Deduplikasi 2 Lapis

1. **Algoritma Pemotongan Siklus (*Windowing Engine*)**:
   ```python
   def get_siklus_operasional(target_dt=None):
       # Jika jam saat ini < 07.00 WIB, maka siklus dimulai dari kemarin pukul 07.00 WIB
       # Jika jam saat ini >= 07.00 WIB, maka siklus dimulai dari hari ini pukul 07.00 WIB
       now = target_dt or timezone.now()
       if now.hour < 7:
           start_date = now.date() - timedelta(days=1)
       else:
           start_date = now.date()
       kode_siklus = f"SIKLUS-{start_date.strftime('%Y%m%d')}"
       return kode_siklus, start_date
   ```

2. **Algoritma Deduplikasi 2 Lapis (*Two-Tier Deduplication*)**:
   ```python
   # Ekstraksi representasi vektor teks berita menggunakan TF-IDF
   tfidf_matrix = vectorizer.fit_transform(corpus_berita)
   sim_score = cosine_similarity(new_vec, existing_vec)[0][0]

   if sim_score >= 0.80:
       # Lapis 1: Kesamaan leksikal tinggi -> Otomatis gabung ke kejadian induk
       tautkan_ke_kejadian_induk(berita_baru, kejadian_induk, sim_score)
   elif sim_score >= 0.60:
       # Lapis 2: Kesamaan moderat -> Periksa kesesuaian wilayah Kemendagri & jendela waktu
       if berita_baru.kabupaten == kejadian_induk.kabupaten and selisih_waktu_jam < 24:
           tautkan_ke_kejadian_induk(berita_baru, kejadian_induk, sim_score)
       else:
           buat_entri_kejadian_baru(berita_baru)
   else:
       buat_entri_kejadian_baru(berita_baru)
   ```

---

## 4.2 Hasil Rancangan Sistem

Hasil implementasi Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB menghasilkan empat modul fungsional utama:

### 4.2.1 Dasbor Pemantauan Meja Piket (Halaman Utama)
Dasbor pemantauan menampilkan informasi waktu riil yang disesuaikan dengan pola kerja meja piket:
* **Header & Quick Trigger**: Menampilkan tombol `[🔄 Tarik Data Sekarang / Sync Now]`, identitas operator piket yang sedang bertugas, indikator shift, serta widget *countdown timer* menuju batas *cut-off* pukul 07.00 WIB.
* **Pengendali Siklus**: Memungkinkan pemilihan siklus operasional yang sedang aktif maupun melihat arsip siklus lampau.
* **4 Tab Status Dinamis**:
  1. `🔴 Belum Terverifikasi (Pending)`: Antrean artikel berita yang baru masuk dan wajib dikonfirmasi ke satgas daerah. Dilengkapi badge visual kontras **`[🚨 ISU BANTUAN]`** jika narasi memuat keluhan warga terkait keterlambatan bantuan logistik.
  2. `🟢 Terverifikasi`: Daftar kejadian bencana yang sudah valid, memiliki data korban dan kerusakan terverifikasi, serta siap diekspor ke laporan resmi.
  3. `⚫ Hoaks`: Arsip kejadian palsu/daur ulang yang dibantah oleh satgas daerah, lengkap dengan catatan alasan bantahan resmi.
  4. `⚪ Semua Data`: Rekapitulasi komprehensif seluruh temuan pada siklus tersebut.

### 4.2.2 Modal Formulir Koreksi Metadata 5 Blok
Ketika operator menekan tombol `[✏️ Edit Metadata & Verifikasi]`, sistem memunculkan formulir modal yang terstruktur rapi ke dalam 5 blok kerja:
* **Blok 1 (Wilayah Kemendagri)**: Dropdown hierarkis bertingkat (Provinsi $\rightarrow$ Kabupaten/Kota $\rightarrow$ Kecamatan).
* **Blok 2 (Waktu Kejadian Riil)**: Input tanggal dan jam faktual bencana di lokasi.
* **Blok 3 (Fakta Dampak Lapangan)**: Pengisian jumlah korban (meninggal, luka, hilang, mengungsi) dan kerusakan fisik (rumah rusak berat/sedang/ringan/terendam, sarana umum).
* **Blok 4 (Upaya TRC & Kondisi Terkini)**: Catatan penanganan darurat BPBD dan perkembangan situasi mutakhir.
* **Blok 5 (Keputusan Status & Jejak Audit)**: Pemilihan status akhir (`Pending`, `Terverifikasi`, `Hoaks`), nama petugas BPBD yang dihubungi, dan nomor kontak.

### 4.2.3 Modal Tambah Kejadian Manual dan Gabung Berita Susulan (*Merge*)
* **Tambah Manual (`[+ Tambah Kejadian Manual]`)**: Memfasilitasi pencatatan laporan bencana mendesak yang diterima melalui radio komunikasi HF atau sambungan telepon darurat sebelum tersiar di media daring.
* **Gabung Berita Susulan (`[🔗 Gabung / Merge]`)**: Fitur interaktif bagi operator untuk menggabungkan dua entri kejadian di antrean yang secara faktual merupakan peristiwa yang sama. Sistem secara otomatis memindahkan seluruh rujukan artikel ke entri kejadian induk.

### 4.2.4 Pusat Ekspor & Penguncian Status (*Dual Output Generator*)
Modul ekspor menyediakan dua jenis keluaran satu-klik:
1. **Format Pesan Singkat WhatsApp Pimpinan**: Teks terstruktur siap salin yang dikelompokkan berdasarkan klaster bencana (Banjir & Cuaca Ekstrem, Gempa Bumi, Tanah Longsor, Karhutla), lengkap dengan kontak satgas konfirmasi dan rujukan media.
2. **Dokumen Microsoft Word (`.docx`) Bagian A Resmi BNPB**: Naskah dinas resmi lengkap dengan Kop Lambang Pusdalops BNPB (*Deep Navy*), tabel rekapitulasi, dan indentasi peluru sesuai Perka BNPB tentang Tata Naskah Dinas dengan mekanisme *null-safety* otomatis (*"Nihil korban jiwa"*, *"Nihil kerusakan"*).
3. **Penguncian Siklus (*Lock Snapshot*) & *Emergency Unlock***: Supervisor dapat mengunci siklus setelah laporan dikirimkan. Jika terdapat ralat data mendadak dari daerah, supervisor dapat menggunakan fitur pembukaan kunci darurat dengan kewajiban mencatat alasan ke log audit.

---

## 4.3 Verifikasi Hasil Rancangan (*Functional Verification*)

Verifikasi hasil rancangan dilakukan dengan membandingkan fungsionalitas sistem aktual terhadap seluruh butir spesifikasi kebutuhan (*SPEC-01* s/d *SPEC-10*) yang ditetapkan pada Bab III melalui metode *Blackbox Testing*.

**Tabel 4.2 Hasil Verifikasi Fungsionalitas Sistem (*Blackbox Testing*)**
| Kode Spesifikasi | Skenario Pengujian | Hasil yang Diharapkan | Hasil Pengujian Aktual | Status |
| :--- | :--- | :--- | :--- | :---: |
| **SPEC-01** | Input data pada pukul 02.30 WIB tanggal H+1. | Data otomatis terikat ke `SIKLUS-YYYYMMDD` tanggal H (07.00–07.00 WIB). | Data terikat ke `SIKLUS-YYYYMMDD` tanggal H dengan benar. | **LULUS** |
| **SPEC-02** | Ekspor berkas Word `.docx` untuk 25 kejadian terverifikasi. | Waktu komputasi pembuatan dokumen selesai dalam $\le 5$ detik. | Dokumen berhasil terunduh dalam durasi **1.42 detik**. | **LULUS** |
| **SPEC-03** | Ingestion dua artikel berita dengan kalimat identik $\ge 80\%$. | Berita kedua otomatis menjadi referensi sekunder pada kejadian pertama. | Terdeteksi similarity 0.88, artikel digabung otomatis. | **LULUS** |
| **SPEC-04** | Dua artikel memberitakan banjir di Kab. Bandung pada hari yang sama (similarity 0.65). | Berita kedua digabung ke kejadian induk karena wilayah sama dalam 24 jam. | Terdeteksi kesamaan wilayah dan waktu, berhasil digabung. | **LULUS** |
| **SPEC-05** | Penarikan feed gempa BMKG dengan parameter $M=5.2$, kedalaman 10 km. | Gempa otomatis masuk ke antrean dasbor pemantauan. | Gempa lolos filter dan muncul di dasbor. | **LULUS** |
| **SPEC-06** | Penarikan feed gempa BMKG dengan parameter $M=3.1$, kedalaman 120 km di laut. | Gempa diabaikan dan tidak membanjiri antrean dasbor. | Gempa disaring keluar dari sistem secara otomatis. | **LULUS** |
| **SPEC-07** | Pengujian volume 50 artikel berita yang memuat 10 kejadian riil. | Reduksi artikel ganda minimal 80%. | Dihasilkan 10 kejadian induk dari 50 artikel (reduksi **80%**). | **LULUS** |
| **SPEC-08** | Input toponimi wilayah "Kab. Bandung Barat". | Otomatis terpetakan ke kode wilayah Kemendagri `32.17`. | Terpetakan sempurna sesuai hierarki master Kemendagri. | **LULUS** |
| **SPEC-09** | Penekanan tombol `[🔄 Tarik Data Sekarang / Sync Now]`. | Respon visual spinner aktif dalam waktu $\le 3$ detik. | Spinner aktif seketika ($< 0.5$ detik), data tersinkronisasi. | **LULUS** |
| **SPEC-10** | Pengubahan status kejadian dari `Pending` menjadi `Hoaks`. | Perubahan status dan catatan alasan bantahan tersimpan di `log_audit_verifikasi`. | Seluruh data audit tersimpan lengkap dengan identitas petugas. | **LULUS** |

Berdasarkan hasil pengujian pada Tabel 4.2, seluruh spesifikasi rancangan (**100%**) dinyatakan **LULUS** verifikasi teknis dan siap dioperasikan dalam lingkungan uji coba.
