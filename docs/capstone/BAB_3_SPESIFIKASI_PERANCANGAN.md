# BAB III: SPESIFIKASI DAN MEKANISME PERANCANGAN

## 3.1 Batasan Realistis (*Realistic Constraints*)

Dalam merancang Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB, diidentifikasi beberapa batasan realistis yang ada pada lingkungan operasional instansi dan infrastruktur teknologi:
1. **Batasan Sumber Daya Manusia & Pola Kerja Shift**:
   Sistem harus dapat dioperasikan secara bergantian oleh operator meja piket pada tiga giliran kerja (*Shift 1: 07.00–15.00 WIB, Shift 2: 15.00–23.00 WIB, Shift 3: 23.00–07.00 WIB*) tanpa menimbulkan disrupsi data antar-shift. Antarmuka harus dirancang intuitif (*zero-learning-curve*) agar operator baru dapat langsung bertugas tanpa memerlukan pelatihan teknis pemrograman yang rumit.
2. **Batasan Akses API & Kebergantungan Pihak Ketiga**:
   Penarikan data eksternal bergantung pada ketersediaan layanan publik (API BMKG, RSS portal berita, dan portal GDACS). Sistem harus memiliki mekanisme penanganan kegagalan (*fault tolerance* / *graceful degradation*); jika salah satu feed mengalami *timeout* atau *downtime*, sistem tidak boleh macet (*crash*) dan harus tetap memproses feed lain yang tersedia.
3. **Batasan Format Baku Tata Naskah Dinas**:
   Struktur luaran dokumen laporan harian (Lapsit Bagian A) tidak boleh dimodifikasi sembarangan karena merupakan dokumen legal resmi negara yang diserahkan ke Kepala BNPB dan Presiden RI. Gaya tipografi, warna kop (*Deep Navy #002060*), penomoran, urutan atribut peluru, dan frasa baku dinas harus 100% patuh pada aturan naskah dinas BNPB.
4. **Batasan Infrastruktur Server & Basis Data**:
   Sistem harus dirancang fleksibel untuk berjalan pada lingkungan pengujian lokal (berbasis SQLite) dan siap dipindahkan tanpa perubahan arsitektur ke peladen produksi instansi (berbasis Linux, PostgreSQL dengan ekstensi PostGIS, serta Nginx/Gunicorn).

---

## 3.2 Standar Keteknikan dan Regulasi (*Engineering Standards*)

Perancangan sistem mengadopsi standar keteknikan perangkat lunak dan regulasi kedinasan resmi:

1. **Standar Rekayasa Perangkat Lunak ISO/IEC 25010**:
   Menjadi acuan evaluasi kualitas sistem, berfokus pada:
   * *Functional Suitability*: Seluruh fungsionalitas (penarikan data, deduplikasi, verifikasi, ekspor Word/WA) beroperasi sesuai spesifikasi.
   * *Performance Efficiency*: Waktu pemrosesan ekspor dokumen Word $\le 5$ detik untuk 50 kejadian terverifikasi.
   * *Reliability*: Ketersediaan layanan (*uptime*) dengan penanganan galat asinkron.
   * *Usability*: Antarmuka dasbor responsif dengan pembedaan warna status yang jelas.
2. **Standar Keamanan Web OWASP Top 10**:
   Pencegahan kerentanan keamanan web, meliputi perlindungan *Cross-Site Request Forgery (CSRF)* pada setiap formulir POST, mitigasi *SQL Injection* melalui Django ORM *parameterized queries*, serta pembatasan hak akses berbasis peran (*Role-Based Access Control* / RBAC).
3. **Regulasi Kode Wilayah Nasional (Kepmendagri No. 100.1.1-6117 Tahun 2022)**:
   Digunakan sebagai standar rujukan tunggal toponimi wilayah hierarkis (Provinsi $\rightarrow$ Kabupaten/Kota $\rightarrow$ Kecamatan).
4. **Regulasi Penanggulangan Bencana (UU No. 24 Tahun 2007 & Perka BNPB)**:
   Menjadi landasan penentuan atribut dampak bencana (korban jiwa: meninggal, luka, hilang, mengungsi; kerusakan sarana: rumah rusak berat/sedang/ringan, fasilitas umum, lahan terdampak).

---

## 3.3 Spesifikasi Rancangan (*Design Specifications*)

Spesifikasi rancangan dirumuskan secara terukur dengan indikator kuantitatif yang jelas:

**Tabel 3.1 Spesifikasi Kebutuhan Fungsional dan Kinerja Sistem**
| Kode | Parameter Spesifikasi | Nilai Metrik Target | Satuan / Tolok Ukur |
| :--- | :--- | :--- | :--- |
| **SPEC-01** | *Windowing Operasional* | Tepat pukul 07.00:00 WIB s/d 06.59:59 WIB | 24 Jam (Hari H s/d H+1) |
| **SPEC-02** | Waktu Ekspor Dokumen Word (.docx) | $\le 5.0$ | Detik (untuk $\le 50$ kejadian) |
| **SPEC-03** | Ambang Batas Deduplikasi Lapis 1 | Cosine Similarity $\ge 0.80$ | Skor kemiripan teks utuh |
| **SPEC-04** | Ambang Batas Deduplikasi Lapis 2 | Cosine Similarity $\ge 0.60$ | Jika Kab/Kota sama & selisih waktu $< 24$ jam |
| **SPEC-05** | Penyaring Gempa Bumi Otomatis | $M \ge 5.0$ & Kedalaman $\le 20$ km | Parameter BMKG lolos otomatis |
| **SPEC-06** | Penyaring Gempa Darat Merusak | $M \ge 4.5$ & Intensitas $\ge \text{III MMI}$ | Parameter guncangan dirasakan |
| **SPEC-07** | Reduksi Redundansi Berita Bencana | $\ge 80.0$ | Persentase eliminasi artikel duplikat |
| **SPEC-08** | Akurasi Normalisasi Wilayah | $100.0$ | Kepatuhan master wilayah Kemendagri |
| **SPEC-09** | Waktu Tanggap Tombol *Sync Now* | $\le 3.0$ | Detik respon visual (spinner aktif) |
| **SPEC-10** | *Audit Trail Logging* | $100.0$ | Seluruh perubahan status & bantahan hoaks tercatat |

---

## 3.4 Batasan dan Asumsi Perancangan

### 3.4.1 Batasan Perancangan
1. Sumber data artikel berita daring dibatasi pada media nasional terakreditasi Dewan Pers yang memiliki feed RSS atau struktur berita publik yang stabil (*Detikcom, Kompas.com, Antara News, CNN Indonesia*).
2. Data parameter kegempaan mengandalkan feed resmi BMKG (Badan Meteorologi, Klimatologi, dan Geofisika).
3. Penguncian siklus (*Lock Snapshot*) hanya dapat dieksekusi setelah seluruh kejadian pada tab `Pending` telah dikonfirmasi menjadi `Terverifikasi` atau `Hoaks`.

### 3.4.2 Asumsi Perancangan
1. Jaringan internet di lingkungan meja piket Pusdalops BNPB tersedia secara kontinu 24 jam dengan latensi stabil.
2. Operator piket memiliki pemahaman dasar terkait terminologi kebencanaan dan prosedur koordinasi dengan BPBD daerah.
3. Seluruh kejadian yang berstatus `Terverifikasi` telah melalui konfirmasi silang (*cross-check*) via telepon/WhatsApp kepada satgas BPBD daerah terkait.

---

## 3.5 Mekanisme Perancangan

### 3.5.1 Sistematika Perancangan (*Engineering Design Flowchart*)

Sistematika pelaksanaan perancangan proyek Capstone disusun secara terstruktur dalam 9 tahapan berurutan sebagaimana disajikan pada Gambar 3.1.

![Sistematika Perancangan](/docs/capstone/diagrams/gambar_3_1_sistematika_perancangan.png)
*Gambar 3.1 Diagram Alir Sistematika Perancangan Sistem Otomasi BNPB*

Penjelasan tahapan perancangan:
1. **Tahap 1: Observasi Lapangan & Identifikasi Masalah**: Mengkaji operasional meja piket Pusdalops BNPB selama periode Kerja Praktek, mengidentifikasi *pain points* rekapitulasi manual lintas shift.
2. **Tahap 2: Kajian Literatur & Body of Knowledge IS2020**: Memetakan landasan teori pengolahan teks NLP, arsitektur sistem informasi web, serta standar ISO/IEC 25010.
3. **Tahap 3: Perumusan Spesifikasi Kebutuhan**: Menetapkan batasan realistis, kriteria keberhasilan fungsional, dan SLA ekspor dokumen.
4. **Tahap 4: Perancangan Arsitektur & Basis Data**: Merancang arsitektur sistem 4-tier dan skema tabel Django ORM (`master_wilayah`, `siklus_laporan`, `kejadian_bencana`, `berita_bencana`, `log_audit_verifikasi`).
5. **Tahap 5: Pengembangan Engine Inti**: Membangun algoritma windowing 24 jam, penyaring gempa adaptif, dan algoritma deduplikasi 2 lapis.
6. **Tahap 6: Implementasi Antarmuka & Modul Ekspor**: Membangun dasbor 4 tab status, modal verifikasi 5 blok, dan generator dokumen Word/WA.
7. **Tahap 7: Verifikasi & Validasi Sistem**: Menjalankan *Blackbox Testing* fungsional serta validasi UAT bersama personil Pusdalops BNPB.
8. **Tahap 8: Analisis Kelayakan & Evaluasi**: Melakukan *Cost-Benefit Analysis* (CBA), perhitungan BEP/NPV, dan evaluasi kesenjangan performa.
9. **Tahap 9: Dokumentasi & Laporan Akhir**: Menyusun laporan akhir lengkap, poster pameran A2, dan logbook.

### 3.5.2 Mekanisme Pengumpulan Data

Data yang digunakan dalam perancangan dikumpulkan melalui tiga metode utama:

**Tabel 3.2 Matriks Sumber Data dan Teknik Pengumpulan**
| Jenis Data | Sumber Data | Teknik Pengumpulan | Instrumen yang Digunakan | Tujuan Penggunaan |
| :--- | :--- | :--- | :--- | :--- |
| **Data Alur Kerja Meja Piket** | Personil Operator Piket & Supervisor Pusdalops BNPB | Observasi langsung & Wawancara semi-terstruktur | Panduan wawancara & lembar observasi shift | Pemodelan proses bisnis dan perancangan antarmuka dasbor |
| **Data Master Wilayah Administrasi** | Kementerian Dalam Negeri RI | Ekstraksi data tabular resmi Kepmendagri 100.1.1-6117/2022 | Skrip parser CSV/JSON Kemendagri | Seeding basis data hierarki wilayah Indonesia |
| **Data Feed Kegempaan** | BMKG (Badan Meteorologi, Klimatologi, dan Geofisika) | Pengambilan data API REST/XML publik | Endpoint HTTP client `requests` | Pengujian algoritma penyaring gempa adaptif |
| **Data Artikel Berita Bencana** | Portal media daring nasional (*Detik, Kompas, Antara*) | Pengambilan feed RSS & scraping berkala | Feedparser & modul ekstraksi teks | Pengujian akurasi deduplikasi NLP Cosine Similarity |
| **Format Tata Naskah Dinas** | Bagian Humas & Tata Usaha Pusdalops BNPB | Dokumentasi arsip laporan Lapsit Bagian A | Sampel dokumen resmi Word (.docx) BNPB | Template acuan generator dokumen otomatis |

### 3.5.3 Mekanisme Verifikasi dan Validasi (V&V)

1. **Mekanisme Verifikasi (*Verification*)**:
   * Memastikan sistem dibangun sesuai dengan spesifikasi teknis (*building the system right*).
   * Dilakukan melalui pengujian fungsional *Blackbox Testing* untuk setiap fitur: keakuratan windowing siklus 07.00 WIB, presisi deduplikasi teks $\ge 0.80$ dan $\ge 0.60$, durasi komputasi ekspor $\le 5$ detik, serta keberhasilan penanganan *null-safety* pada dokumen Word.
2. **Mekanisme Validasi (*Validation*)**:
   * Memastikan sistem menyelesaikan permasalahan riil pemangku kepentingan (*building the right system*).
   * Dilakukan melalui *User Acceptance Testing* (UAT) dan demonstrasi langsung di hadapan personil/supervisor Pusdalops BNPB.
   * Umpan balik dicatat ke dalam **Berita Acara Validasi Hasil Rancangan** (sesuai format Tabel 6.6 pedoman) yang memuat nama, jabatan, serta evaluasi kemanfaatan solusi.
