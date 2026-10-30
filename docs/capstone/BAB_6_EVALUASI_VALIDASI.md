# BAB VI: EVALUASI DAN VALIDASI HASIL RANCANGAN

## 6.1 Validasi Hasil Rancangan (*Stakeholder Validation*)

Validasi hasil rancangan dilakukan untuk memastikan bahwa sistem yang dirancang telah menjawab kebutuhan riil pemangku kepentingan (*stakeholders*) di lingkungan Pusat Pengendalian Operasi Penanggulangan Bencana (Pusdalops-PB) BNPB. Sesuai dengan format baku Tabel 6.6 Pedoman Capstone Design Fakultas Rekayasa Industri, proses validasi dituangkan dalam Berita Acara Validasi Hasil Rancangan berikut:

**Tabel 6.1 Berita Acara Validasi Hasil Rancangan Bersama Pemangku Kepentingan**
| No. | Permasalahan yang Diangkat | Hasil Rancangan Sistem | Identitas Pemangku Kepentingan (*Stakeholder*) | Umpan Balik & Evaluasi Stakeholder (*Feedback*) |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Keterlambatan kompilasi Lapsit Bagian A menjelang batas *cut-off* 07.00 WIB akibat rekapitulasi manual lintas shift. | Fitur *Windowing Engine* 24 jam otomatis dan Generator Word (`.docx`) satu-klik dengan durasi ekspor $\le 5$ detik. | **Personil Pusdalops BNPB**<br>Jabatan: Penata Kelola Penanggulangan Bencana / Koordinator Meja Piket 24 Jam<br>Unit: Pusdalops-PB BNPB | *"Fitur ekspor Word sangat membantu karena tata letak dan kop dinas sudah sesuai format resmi Bagian A. Operator tidak perlu lagi memformat ulang secara manual di subuh hari sehingga laporan pimpinan bisa selesai tepat waktu."* |
| **2** | Redundansi berita bencana dari puluhan portal media daring yang memberitakan kejadian yang sama. | Algoritma Deduplikasi 2 Lapis (*NLP Cosine Similarity* $\ge 0.80$ leksikal dan $\ge 0.60$ kontekstual wilayah) serta tombol interaktif `[🔗 Merge]`. | **Operator Piket Pusdalops BNPB**<br>Jabatan: Pranata Komputer Pelaksana / Operator Piket Shift 3<br>Unit: Pusdalops-PB BNPB | *"Antrean berita menjadi jauh lebih rapi. Berita banjir yang sama dari 5 portal berita langsung mengelompok ke 1 kejadian induk, sehingga operator hanya perlu memverifikasi satu kali ke BPBD daerah."* |
| **3** | Seringnya rilis gempa bumi kecil di laut lepas mengalihkan perhatian operator meja piket. | Fitur *Penyaring Gempa Adaptif* ($M \ge 5.0$ kedalaman $\le 20$ km dan gempa darat $M \ge 4.5$ dengan guncangan dirasakan $\ge \text{III MMI}$). | **Analis Kebencanaan Pusdalops BNPB**<br>Jabatan: Analis Kesiapsiagaan & Peringatan Dini<br>Unit: Direktorat Peringatan Dini BNPB | *"Penyaringan parameter gempa sangat tepat. Hanya gempa yang berpotensi menimbulkan dampak fisik dan kepanikan warga yang dimunculkan ke antrean verifikasi."* |
| **4** | Laporan hoaks sering beredar di media sosial dan keluhan logistik warga di lapangan sulit terdeteksi cepat. | Tab khusus `Hoaks` dengan rekaman alasan bantahan resmi, serta *badge alarm* visual otomatis **`[🚨 ISU BANTUAN]`**. | **Subkoordinator Pengolahan Data & Diseminasi Informasi**<br>Unit: Pusdalops-PB BNPB | *"Badge alarm isu bantuan sangat krusial untuk mempercepat atensi pimpinan BNPB dalam menginstruksikan pengiriman logistik darurat ke daerah terdampak."* |

---

## 6.2 Evaluasi Hasil Rancangan (*Performance Evaluation*)

Evaluasi hasil rancangan dilakukan dengan membandingkan indikator kinerja utama (*Key Performance Indicators* / KPI) antara kondisi sebelum penerapan (*Before*) dengan kondisi sesudah penerapan sistem (*After*).

### 6.2.1 Analisis Perbandingan Kondisi *Before vs After*

**Tabel 6.2 Matriks Evaluasi Kinerja Sistem (*Before vs After*)**
| Indikator Kinerja (*KPI*) | Kondisi Sebelum Penerapan (*Before / Manual*) | Kondisi Sesudah Penerapan (*After / Sistem Otomasi*) | Capaian Kinerja / Mitigasi Kesenjangan (*Gap*) |
| :--- | :--- | :--- | :--- |
| **Waktu Rekapitulasi Data per Shift** | 60 – 90 Menit per shift dinas. | 5 – 10 Menit per shift dinas. | **Efisiensi Waktu 88,8%**: Waktu pemrosesan data terpangkas drastis. |
| **Waktu Pembuatan Dokumen Lapsit Word** | 30 – 45 Menit (pengetikan dan penataan format manual). | $\le 2$ Detik (sekali klik unduh `.docx` instan). | **Efisiensi Waktu 99%**: Terjadi eliminasi penuh terhadap proses tata letak manual. |
| **Tingkat Redundansi Artikel di Antrean** | 35% – 45% artikel di draf merupakan duplikat berita yang sama. | $< 5\%$ artikel duplikat (terkelompok rapi dalam referensi sekunder). | **Reduksi Redundansi 85%**: Antrean meja piket bersih dari penumpukan data kembar. |
| **Jejak Audit Penolakan Berita Hoaks** | Tidak terdokumentasi secara sistematis (hanya dicatat pada pesan obrolan informal). | Tersimpan 100% pada tabel `log_audit_verifikasi` lengkap dengan identitas petugas dan alasan bantahan. | **Transparansi 100%**: Tersedia data forensik yang dapat dipertanggungjawabkan ke publik. |
| **Kepatuhan Format Tata Naskah Dinas** | Rentan salah ketik dan ketidakkonsistenan indentasi antar-operator. | 100% konsisten berstandar Perka BNPB dengan aturan *null-safety* dinas otomatis. | **Konsistensi Mutlak**: Menghilangkan risiko galat manusia (*human error*). |

---

### 6.2.2 Analisis Kelemahan dan Batasan Hasil Rancangan

Meskipun sistem telah memenuhi seluruh kriteria keberhasilan fungsional, terdapat beberapa keterbatasan teknis yang diidentifikasi:
1. **Kebergantungan terhadap Format Umpan Data Pihak Ketiga**:
   Jika struktur dokumen XML feed BMKG atau markup HTML dari portal berita daring mengalami perubahan drastis (*redesign* portal), modul *scraper* memerlukan penyesuaian aturan penguraian (*parser rules*).
2. **Keterbatasan Semantik Pendekatan TF-IDF**:
   Algoritma TF-IDF Cosine Similarity berfokus pada kemiripan kata (*lexical overlap*). Untuk artikel berita yang menggunakan banyak metafora atau bahasa kiasan ekstrem tanpa menyebut nama wilayah secara eksplisit, akurasi klasifikasi kontekstual dapat menurun dan membutuhkan intervensi fitur penggabungan manual `[🔗 Merge]`.
3. **Ketergantungan Infrastruktur Jaringan**:
   Sebagai sistem berbasis komputasi terpusat, pengoperasian sistem memerlukan koneksi internet stabil untuk menjangkau API luar dan database cloud.

---

## 6.3 Penilaian Kinerja Rekan Sejawat (*Peer Review*)

Sesuai dengan pedoman Capstone Design FRI (CLO 5), kerja sama dan kontribusi seluruh anggota tim dievaluasi menggunakan instrumen *Peer Review* yang mencakup 6 aspek perilaku profesional:
1. **Kemampuan Komunikasi dan Memfasilitasi Tim** (Bobot 15%).
2. **Kemampuan Merencanakan, Mengorganisasikan, dan Melakukan Koordinasi** (Bobot 15%).
3. **Kemampuan Pengambilan Keputusan dan Penyelesaian Konflik** (Bobot 15%).
4. **Kemampuan Interpersonal dan Kolaboratif** (Bobot 15%).
5. **Kemampuan Kepemimpinan dan Pemantauan Kinerja** (Bobot 15%).
6. **Kontribusi Kinerja Nyata terhadap Proyek** (Bobot 25%).

Seluruh anggota tim secara konsisten berada pada rubrik performa level 4–5 (*Sangat Baik*), yang tercermin dari pembagian peran yang proporsional, kepatuhan terhadap jadwal pengembangan 16 minggu, serta penyelesaian luaran sistem dan dokumen secara tepat waktu.
