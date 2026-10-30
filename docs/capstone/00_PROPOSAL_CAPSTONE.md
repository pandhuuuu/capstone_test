# PROPOSAL CAPSTONE DESIGN & PROJECT
## PERANCANGAN SISTEM OTOMASI PEMANTAUAN KEBENCANAAN PUSDALOPS BNPB BERBASIS INTELIJEN TEKS DAN DUAL OUTPUT GENERATOR

---

### ABSTRAK

Pusat Pengendalian Operasi Penanggulangan Bencana (Pusdalops-PB) Badan Nasional Penanggulangan Bencana (BNPB) bertugas memantau situasi kebencanaan di seluruh wilayah Indonesia selama 24 jam non-stop melalui tiga giliran kerja (*shift*). Salah satu luaran utama yang wajib diterbitkan setiap pagi adalah Laporan Harian Situasi Bencana (Lapsit Bagian A) untuk Kepala BNPB dan Presiden RI. Namun, proses agregasi data saat ini masih dilakukan secara manual dan terfragmentasi dengan membuka puluhan portal berita daring, pesan grup relawan, serta feed BMKG. Hal ini menyebabkan beban kognitif tinggi bagi operator piket, penumpukan 30%–40% artikel berita duplikat, kesulitan penyaringan anomali gempa kecil, risiko disinformasi berita hoaks, serta potensi keterlambatan kompilasi laporan melewati batas *cut-off* pukul 07.00 WIB.

Untuk menyelesaikan permasalahan tersebut, proyek Capstone Design ini mengusulkan perancangan sistem informasi pemantauan kebencanaan berbasis web terintegrasi menggunakan framework Django 5 dan arsitektur pemrosesan asinkron Celery. Sistem mengimplementasikan *Windowing Engine* 24 jam (pukul 07.00–07.00 WIB) sesuai konvensi dinas kedaruratan, *Penyaring Gempa Adaptif* ($M \ge 5.0$ kedalaman $\le 20$ km dan gempa darat $M \ge 4.5$ dengan intensitas $\ge \text{III MMI}$), serta *Deduplikasi 2 Lapis* berbasis NLP *Cosine Similarity* ($\ge 0.80$ leksikal dan $\ge 0.60$ kontekstual wilayah) untuk mereduksi berita ganda hingga $\ge 80\%$. Sistem dilengkapi dasbor meja piket 4 tab status (`Pending`, `Terverifikasi`, `Hoaks`, `Semua Data`), badge alarm `[🚨 ISU BANTUAN]`, formulir verifikasi 5 blok, dan modul *Dual Output Generator* yang mampu mengekspor berkas Microsoft Word (`.docx`) berstandar resmi Tata Naskah Dinas BNPB dalam waktu $\le 5$ detik serta ringkasan pesan WhatsApp pimpinan.

**Kata Kunci:** *Pusdalops BNPB, Otomasi Pemantauan Bencana, Windowing 24 Jam, Deduplikasi NLP, Dual Output Generator.*

---

## 1. Rencana Waktu Pelaksanaan Perancangan (Timeline Proposal)

Sesuai ketentuan Pedoman Capstone Design FRI Telkom University (Tabel 6.4), jadwal pelaksanaan perancangan dijabarkan mulai dari Minggu ke-5 hingga Minggu ke-15:

**Tabel Timeline Pelaksanaan Perancangan Capstone Design (Minggu 5 – 15)**
| No | Aktivitas Perancangan | Mg 5 | Mg 6 | Mg 7 | Mg 8 | Mg 9 | Mg 10 | Mg 11 | Mg 12 | Mg 13 | Mg 14 | Mg 15 | Penanggung Jawab |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :--- |
| 1 | Pengumpulan Data Lapangan & Analisis SOP Pusdalops | [X] | [X] | | | | | | | | | | Tim Mahasiswa |
| 2 | Pemodelan Arsitektur 4-Tier & Skema Basis Data ORM | | [X] | [X] | | | | | | | | | Tim Mahasiswa |
| 3 | Pengembangan Ingestion Engine & Windowing 24 Jam | | | [X] | [X] | | | | | | | | Tim Mahasiswa |
| 4 | Implementasi Algoritma Deduplikasi NLP 2 Lapis | | | | [X] | [X] | | | | | | | Tim Mahasiswa |
| 5 | Evaluasi Tengah Semester (Laporan Progress) | | | | [X] | | | | | | | | Pembimbing / Tim |
| 6 | Pembuatan Antarmuka Dasbor Web 4 Tab & Modal 5 Blok | | | | | [X] | [X] | [X] | | | | | Tim Mahasiswa |
| 7 | Pengembangan Modul Dual Output Word (.docx) & WA | | | | | | | [X] | [X] | | | | Tim Mahasiswa |
| 8 | Verifikasi Fungsional Sistem (Blackbox Testing) | | | | | | | | [X] | [X] | | | Tim Mahasiswa |
| 9 | Validasi Pengguna & UAT Meja Piket Pusdalops | | | | | | | | | [X] | [X] | | Stakeholder / Tim |
| 10 | Analisis Biaya, Kelayakan Finansial (CBA), & Laporan Akhir | | | | | | | | | | [X] | [X] | Tim Mahasiswa |
| 11 | Presentasi Laporan Akhir & Pameran Prototipe Produk | | | | | | | | | | | [X] | Seluruh Tim & Penguji |

---

## 2. Pemetaan Komponen Sistem Terintegrasi (5M)

Sesuai ketentuan Panduan Capstone (Tabel 6.5), analisis sistem dipetakan ke dalam 5 pilar sistem terintegrasi:

**Tabel Pemetaan Objek dan Solusi ke dalam Komponen Sistem Terintegrasi (5M)**
| Pilar Komponen | Objek Riil Eksisting (Sistem Konvensional) | Usulan Solusi Sistem Otomasi Pusdalops BNPB |
| :--- | :--- | :--- |
| **Manusia (*Man*)** | Tiga giliran (*shift*) operator meja piket yang menyalin data secara manual; Operator berisiko mengalami kelelahan kognitif pada shift subuh. | Peran terstruktur (*RBAC*): Operator Piket bertugas memvalidasi data dan Supervisor berwenang mengunci laporan (*Lock Snapshot*) dengan audit log forensik. |
| **Material / Aset Data (*Material*)** | Ratusan teks berita daring acak, pesan obrolan WhatsApp grup, dan rilis kegempaan yang belum terstruktur. | Entri kejadian bencana terstruktur (`kejadian_bencana`), entri rujukan media (`berita_bencana`), dan master wilayah resmi Kemendagri. |
| **Mesin / Alat Fasilitas (*Machine / Facility*)** | Peramban web dengan puluhan tab terbuka, dokumen pengolah kata lokal, dan spreadsheet manual yang rentan konflik versi. | Server web Django 5, *Task Scheduler* Celery Beat, basis data PostgreSQL/SQLite, pustaka *scikit-learn* (NLP) dan *python-docx*. |
| **Informasi (*Information*)** | Tumpukan berita duplikat, tidak adanya penanda isu bantuan darurat, dan format laporan yang diketik ulang manual. | Antrean dasbor 4 tab dinamis, penanda alarm otomatis `[🚨 ISU BANTUAN]`, rekomendasi penggabungan berita susulan (*merge*), serta Lapsit Bagian A Word & WA. |
| **Energi / Jam Kerja (*Energy*)** | Pemborosan 60–90 menit per shift untuk aktivitas klerikal salin-tempel teks manual. | Efisiensi kerja $> 80\%$, mengalihkan jam kerja operator ke konfirmasi faktual prioritas tinggi ke BPBD daerah. |

---

*(Naskah Bab I, Bab II, dan Bab III proposal mengacu lengkap pada file [BAB_1_PENDAHULUAN.md](file:///c:/Users/athal/Documents/bnpb_disaster_system/docs/capstone/BAB_1_PENDAHULUAN.md), [BAB_2_TINJAUAN_PUSTAKA.md](file:///c:/Users/athal/Documents/bnpb_disaster_system/docs/capstone/BAB_2_TINJAUAN_PUSTAKA.md), dan [BAB_3_SPESIFIKASI_PERANCANGAN.md](file:///c:/Users/athal/Documents/bnpb_disaster_system/docs/capstone/BAB_3_SPESIFIKASI_PERANCANGAN.md))*.
