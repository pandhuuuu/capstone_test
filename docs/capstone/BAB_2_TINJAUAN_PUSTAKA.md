# BAB II: TINJAUAN PUSTAKA

## 2.1 Body of Knowledge (BoK) Sistem Informasi

Pelaksanaan Capstone Design Project pada Program Studi S1 Sistem Informasi berpedoman pada kerangka kompetensi internasional **IS2020: A Competency Model for Undergraduate Programs in Information Systems** yang disusun bersama oleh *Association for Computing Machinery (ACM)* dan *Association for Information Systems (AIS)*. Kurikulum ini mensyaratkan integrasi minimal dua domain Body of Knowledge. Dalam perancangan Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB, diintegrasikan empat domain BoK utama:

### 2.1.1 Domain Data / Information Management
Domain ini berfokus pada kemampuan merancang, menyimpan, mengelola, serta memproses data organisasi hingga menghasilkan informasi yang bernilai strategis. Pada proyek ini, domain data diimplementasikan pada:
1. **Pengelolaan Basis Data Relasional & Semi-Terstruktur**: Perancangan skema database terintegrasi menggunakan Django ORM dengan pemanfaatan tipe `JSONField` (kompatibel secara native dengan SQLite dan PostgreSQL `JSONB`). Hal ini memungkinkan penyimpanan data faktual lapangan yang dinamis (seperti rincian korban terdampak dan kerusakan fisik fasilitas).
2. **Text Processing & Intelijen Teks**: Penerapan ekstraksi informasi tekstual dari artikel berita daring (*unstructured text*) melalui proses *tokenization*, pembersihan karakter khusus, penghapusan kata umum (*stopword removal*), serta pembobotan kata menggunakan algoritma *Term Frequency-Inverse Document Frequency* (TF-IDF).
3. **Normalisasi Data Wilayah Administratif**: Penyelarasan toponimi dan ejaan nama wilayah administratif Indonesia berdasarkan basis data master wilayah nasional untuk menjamin konsistensi data lintas instansi.

### 2.1.2 Domain Development (Pengembangan Aplikasi & Perancangan Sistem)
Domain *Development* mencakup seluruh siklus hidup pengembangan perangkat lunak (*Software Development Life Cycle* / SDLC), pemodelan kebutuhan sistem, arsitektur perangkat lunak, serta perancangan antarmuka pengguna:
1. **Systems Analysis & Design (SAD)**: Pemodelan kebutuhan sistem menggunakan diagram alir data (*data pipeline workflow*), *Entity Relationship Diagram* (ERD), dan perancangan kamus data.
2. **Web Programming & Application Architecture**: Pembangunan aplikasi web hulu-ke-hilir menggunakan arsitektur Model-View-Template (MVT) pada framework Django 5 (Python).
3. **User Interface (UI) & User Experience (UX) Design**: Perancangan antarmuka dasbor pemantauan meja piket Pusdalops yang mengadopsi prinsip efisiensi kognitif operator, dilengkapi sistem tab dinamis 4 status (`Pending`, `Terverifikasi`, `Hoaks`, `Semua Data`), badge alarm visual kontras `[🚨 ISU BANTUAN]`, serta modal interaktif 5 blok untuk mempercepat input data lapangan.

### 2.1.3 Domain Technology (Infrastruktur Teknologi & Komputasi Aman)
Domain ini mencakup penyediaan infrastruktur komputasi, komunikasi data antar-sistem, dan pemrosesan asinkron:
1. **Asynchronous Task Queue & Scheduling**: Pemanfaatan *Celery* dan penjadwal berkala (*Celery Beat*) untuk mengeksekusi penarikan data berkala (*feed ingestion*) dari API BMKG dan RSS portal media berita daring di latar belakang tanpa menghambat performa antarmuka pengguna (*non-blocking I/O*).
2. **Secure Computing & Role-Based Access Control (RBAC)**: Penerapan kontrol akses berbasis peran antara akun Operator Piket dan akun Supervisor. Khusus akun Supervisor, disediakan wewenang penguncian siklus (*Lock Snapshot*) dan pembukaan darurat (*Emergency Unlock*) yang mencatat setiap aksi ke dalam rekaman audit forensik (*log audit*).

### 2.1.4 Domain Integration (IS Project Management)
Domain integrasi berfokus pada pengelolaan proyek perangkat lunak dari inisiasi hingga serah terima solusi:
1. **Manajemen Batasan Waktu & SLA**: Penerapan metodologi *Agile Iterative* untuk memastikan modul sistem diselesaikan sesuai jadwal 16 minggu Capstone Design Project, dengan pemenuhan *Service Level Agreement* (SLA) ekspor naskah resmi $\le 5$ detik.
2. **Pengujian Verifikasi & Validasi Sistem**: Pelaksanaan pengujian fungsional berbasis *Blackbox Testing* serta pengujian penerimaan pengguna (*User Acceptance Testing* / UAT) bersama pemangku kepentingan Pusdalops BNPB.

---

## 2.2 Teori, Konsep, dan Kerangka Standar Terkait Perancangan

### 2.2.1 Penyelenggaraan Penanggulangan Bencana & Pusdalops-PB
Berdasarkan Undang-Undang Republik Indonesia Nomor 24 Tahun 2007 tentang Penanggulangan Bencana, penanggulangan bencana adalah serangkaian upaya yang meliputi penetapan kebijakan pembangunan yang berisiko timbulnya bencana, kegiatan pencegahan bencana, tanggap darurat, dan rehabilitasi. 

Pusat Pengendalian Operasi Penanggulangan Bencana (Pusdalops-PB) berfungsi sebagai unsur pelaksana operasional yang menyelenggarakan kegiatan pemantauan, penerimaan laporan, pengolahan data, dan diseminasi informasi situasi darurat bencana kepada pimpinan dan masyarakat secara *real-time*. Dalam pelaksanaannya, Pusdalops memerlukan data yang terverifikasi dan akurat agar penetapan status keadaan darurat oleh pemerintah tidak didasarkan pada laporan yang keliru atau kabar bohong (*hoaks*).

### 2.2.2 Konsep Siklus Operasional 24 Jam (*Windowing Engine*)
Dalam sistem pelaporan situasi bencana nasional, pencatatan kejadian harian tidak dihitung per hari kalender sipil biasa (pukul 00.00 hingga 23.59 WIB). Secara konvensi operasional kedaruratan, 1 siklus operasional 24 jam didefinisikan sejak pukul **07.00:00 WIB hari berjalan hingga pukul 06.59:59 WIB hari berikutnya**.

Sistem windowing dirancang dengan formula kode siklus:
$$\text{Kode Siklus} = \text{SIKLUS-YYYYMMDD}$$
di mana $YYYYMMDD$ merujuk pada tanggal saat siklus tersebut dibuka pukul 07.00 WIB. Mekanisme ini memecahkan anomali pergantian tanggal kalender di tengah pergantian shift malam (*Shift 3*) sehingga laporan pagi yang diserahkan ke Kepala BNPB merangkum tepat 24 jam kondisi riil lapangan.

### 2.2.3 Natural Language Processing (NLP) & Deduplikasi Cosine Similarity
Deduplikasi berita bencana bertujuan mengelompokkan berbagai artikel berita dari portal yang berbeda yang memberitakan peristiwa bencana yang sama menjadi satu entri kejadian induk (*lead incident*).

1. **TF-IDF (*Term Frequency - Inverse Document Frequency*)**:
   TF-IDF digunakan untuk merepresentasikan dokumen teks berita ke dalam bentuk vektor bobot numerik:
   $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{|D|}{1 + |\{d \in D : t \in d\}|}\right)$$
   di mana $t$ adalah term/kata, $d$ adalah dokumen berita, dan $D$ adalah korpus dokumen.

2. **Cosine Similarity**:
   Tingkat kesamaan semantik antara dua vektor dokumen berita $\vec{A}$ dan $\vec{B}$ dihitung menggunakan formula sudut cosinus:
   $$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

3. **Mekanisme Deduplikasi 2 Lapis (*Two-Tier Deduplication*)**:
   * **Lapis 1 (Kesamaan Leksikal Utuh)**: Dua berita langsung digabungkan jika $\text{Similarity} \ge 0.80$ tanpa memandang wilayah.
   * **Lapis 2 (Kesamaan Kontekstual Wilayah & Waktu)**: Jika $\text{Similarity} \ge 0.60$, sistem memeriksa apakah kedua berita merujuk pada Kabupaten/Kota yang sama dan selisih waktu terbit $< 24$ jam. Jika terpenuhi, berita kedua ditautkan sebagai berita susulan (*child reference*).

### 2.2.4 Standar Wilayah Administrasi Pemerintahan (Kepmendagri)
Toponimi penamaan wilayah mengacu pada Keputusan Menteri Dalam Negeri (Kepmendagri) Nomor 100.1.1-6117 Tahun 2022 tentang Pemberian dan Pemutakhiran Kode, Data Wilayah Administrasi Pemerintahan, dan Pulau. Standar ini membagi hierarki wilayah Indonesia ke dalam format relasional:
$$\text{Provinsi} \rightarrow \text{Kabupaten/Kota} \rightarrow \text{Kecamatan} \rightarrow \text{Desa/Kelurahan}$$
Penerapan standar ini mencegah terjadinya salah tafsir penamaan lokasi bencana di media sosial (misal: singkatan "Kab. Bdg" diselaraskan menjadi "KABUPATEN BANDUNG").

### 2.2.5 Standar Kualitas Perangkat Lunak ISO/IEC 25010
Perancangan dan pengujian sistem mengacu pada standar kualitas sistem dan perangkat lunak **ISO/IEC 25010 System and Software Quality Models**, dengan fokus pengujian pada karakteristik:
1. **Functional Suitability**: Kelengkapan fitur penarikan data, deduplikasi, verifikasi, dan ekspor.
2. **Performance Efficiency**: Durasi waktu pembuatan laporan dokumen Word Bagian A ($\le 5$ detik) dan waktu komputasi deduplikasi teks.
3. **Usability**: Kemudahan penggunaan antarmuka dasbor meja piket bagi operator lintas shift.
4. **Reliability & Fault Tolerance**: Sistem tetap beroperasi normal meskipun salah satu sumber feed berita mengalami *timeout* atau tidak merespons.
5. **Security**: Pengendalian akses otorisasi supervisor untuk pembukaan kunci darurat (*emergency unlock*) dan integritas jejak audit.

### 2.2.6 Standar Tata Naskah Dinas Pusdalops BNPB
Format naskah dinas resmi Laporan Harian Situasi Bencana (Lapsit Bagian A) mengacu pada Peraturan Kepala BNPB tentang Tata Naskah Dinas. Naskah wajib memiliki struktur baku:
* Kop resmi lambang Pusdalops BNPB dengan tipografi Arial tebal warna *Deep Navy* (`#002060`).
* Huruf kapital tebal untuk judul bencana dan wilayah.
* Indentasi atribut peluru (*bullet points*) berurutan: Waktu Kejadian, Lokasi, Kronologi, Korban Jiwa & Terdampak, Kerusakan Sarana Prasarana, Upaya TRC, Kondisi Mutakhir, dan Kontak Konfirmasi.
* Aturan *Null-Safety*: Jika tidak ada korban jiwa atau kerusakan, sistem tidak boleh mencetak angka `0`, melainkan frasa resmi dinas *"Nihil korban jiwa"* dan *"Nihil kerusakan sarana prasarana"*.
