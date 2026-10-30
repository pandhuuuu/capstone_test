# BAB V: ANALISIS BIAYA DAN KELAYAKAN PERANCANGAN

## 5.1 Identifikasi Biaya Perancangan dan Implementasi (*Cost Identification*)

Perhitungan biaya pengembangan dan implementasi Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB disusun menggunakan pendekatan *Total Cost of Ownership* (TCO) yang mencakup biaya investasi awal (*Capital Expenditure* / CAPEX) dan biaya operasional tahunan (*Operational Expenditure* / OPEX). 

Standar biaya tenaga kerja pengembangan mengacu pada Pedoman Standar Remunerasi Minimal Tenaga Ahli Ikatan Nasional Konsultan Indonesia (INKINDO) 2026 dan Upah Minimum Provinsi (UMP) DKI Jakarta (lokasi kantor pusat BNPB, Jakarta Timur).

### 5.1.1 Biaya Investasi Awal (*Capital Expenditure* / CAPEX)

Biaya investasi awal mencakup seluruh aktivitas rekayasa perangkat lunak selama periode perancangan sistem:

**Tabel 5.1 Rincian Biaya Investasi Awal (*CAPEX*) Pengembangan Sistem**
| No. | Komponen Investasi | Volume / Durasi | Satuan Biaya (Rp) | Total Biaya (Rp) | Dasar Acuan / Keterangan |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | **Tenaga Kerja Pengembang (*Software Team*)** | | | | |
| a | *Systems Analyst & Lead Designer* | 2 Orang-Bulan | 12.000.000 | 24.000.000 | Analisis proses bisnis & arsitektur |
| b | *Fullstack Software Engineer* (Django/Python) | 2 Orang-Bulan | 10.000.000 | 20.000.000 | Implementasi backend, NLP, & frontend |
| c | *QA & Testing Engineer* | 1 Orang-Bulan | 7.000.000 | 7.000.000 | Pengujian fungsional & verifikasi V&V |
| **2** | **Infrastruktur & Lingkungan Uji Coba** | | | | |
| a | Setup Server & CI/CD Pipeline | 1 Paket | 3.500.000 | 3.500.000 | Konfigurasi Linux, PostgreSQL, & Celery |
| b | Lisensi & Domain Kedinasan Terproteksi SSL | 1 Tahun | 1.500.000 | 1.500.000 | Domain instansi & sertifikat SSL EV |
| **3** | **Pelatihan & *Change Management*** | | | | |
| a | Pelatihan Operator Piket (3 Shift) & Supervisor | 3 Sesi | 1.500.000 | 4.500.000 | Modul panduan & simulasi meja piket |
| \multicolumn{4}{|c|}{\textbf{TOTAL BIAYA INVESTASI AWAL (CAPEX)}} | \textbf{60.500.000} | |

### 5.1.2 Biaya Operasional dan Pemeliharaan Tahunan (*OPEX*)

Biaya operasional tahunan diperlukan untuk menjaga kelangsungan operasional sistem 24 jam non-stop:

**Tabel 5.2 Rincian Biaya Operasional Tahunan (*OPEX*)**
| No. | Komponen Operasional | Volume | Satuan Biaya / Bulan (Rp) | Total per Tahun (Rp) | Keterangan |
| :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | *Cloud VPS Hosting* (4 vCPU, 8 GB RAM, NVMe) | 12 Bulan | 1.200.000 | 14.400.000 | Hosting aplikasi web & Celery worker |
| 2 | Pemeliharaan Teknis & *Bug Fixing* (SLA) | 12 Bulan | 1.000.000 | 12.000.000 | Dukungan teknis berkala |
| 3 | Cadangan Bandwidth & Pembaruan Sertifikat SSL | 1 Tahun | - | 2.000.000 | Pembaruan sertifikat & cadangan koneksi |
| \multicolumn{4}{|c|}{\textbf{TOTAL BIAYA OPERASIONAL TAHUNAN (OPEX)}} | \textbf{28.400.000} | *(Rp 2.366.667 / Bulan)* |

---

## 5.2 Analisis Kelayakan Hasil Rancangan (*Financial Feasibility Analysis*)

Kelayakan hasil rancangan dinilai dengan membandingkan biaya yang dikeluarkan dengan nilai penghematan riil (*tangible benefit*) yang diperoleh instansi.

### 5.2.1 Kuantifikasi Manfaat Penghematan Jam Kerja (*Man-Hour Savings*)
Manfaat ekonomi utama yang dihasilkan adalah efisiensi waktu kerja operator meja piket Pusdalops BNPB yang bertugas dalam 3 shift per hari (365 hari per tahun = 1.095 sesi piket per tahun).

1. **Perhitungan Waktu yang Dihemat**:
   * Kondisi manual eksisting: Rata-rata waktu rekapitulasi dan pengetikan laporan per shift = **75 menit (1,25 jam)**.
   * Kondisi dengan sistem otomasi: Waktu verifikasi dan ekspor berkurang menjadi **10 menit (0,167 jam)**.
   * Penghematan waktu per shift = **1,083 jam**.
   * Total jam kerja yang dihemat per tahun = $1.095 \text{ shift} \times 1,083 \text{ jam} = \mathbf{1.186\text{ jam/tahun}}$.

2. **Valuasi Finansial Penghematan Jam Kerja**:
   * Standar biaya kerja personil piket (berdasarkan standar biaya masukan pemerintah / UMP DKI): Rp 65.000 per jam.
   * Nilai efisiensi jam kerja langsung = $1.186 \text{ jam} \times \text{Rp } 65.000 = \mathbf{\text{Rp } 77.090.000\text{ / tahun}}$.
   * Nilai mitigasi risiko keterlambatan pengiriman Lapsit ke pimpinan dan pencegahan disinformasi/hoaks (diestimasi secara konservatif): $\mathbf{\text{Rp } 25.000.000\text{ / tahun}}$.
   * **Total Manfaat Finansial Tahunan ($B_t$)** = $\text{Rp } 77.090.000 + \text{Rp } 25.000.000 = \mathbf{\text{Rp } 102.090.000\text{ / tahun}}$.

---

### 5.2.2 Analisis Arus Kas (*Cost-Benefit Analysis* / CBA)

Evaluasi kelayakan investasi dihitung untuk horizon perencanaan 3 tahun dengan tingkat suku bunga diskonto (*discount rate*) sosial pemerintah sebesar $r = 8\%$ per tahun:

**Tabel 5.3 Analisis Arus Kas Bersih dan Nilai Sekarang (*Discounted Cash Flow*)**
| Tahun ($t$) | Biaya / CAPEX + OPEX (Rp) | Manfaat Finansial (Rp) | Arus Kas Bersih / $CF_t$ (Rp) | Faktor Diskonto ($DF_{8\%}$) | *Present Value* / $PV$ (Rp) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | 60.500.000 | 0 | -60.500.000 | 1,0000 | -60.500.000 |
| **1** | 28.400.000 | 102.090.000 | +73.690.000 | 0,9259 | +68.231.571 |
| **2** | 28.400.000 | 102.090.000 | +73.690.000 | 0,8573 | +63.174.437 |
| **3** | 28.400.000 | 102.090.000 | +73.690.000 | 0,7938 | +58.495.121 |
| \multicolumn{4}{|c|}{\textbf{NET PRESENT VALUE (NPV)}} | | \textbf{+129.401.129} |

1. **Net Present Value (NPV)**:
   $$\text{NPV} = \sum_{t=0}^{3} \frac{CF_t}{(1 + r)^t} = \mathbf{\text{Rp } 129.401.129} > 0 \quad (\textbf{SANGAT LAYAK})$$
2. **Benefit-Cost Ratio (BCR)**:
   $$\text{Present Value of Benefits} = 68.231.571 + 63.174.437 + 58.495.121 = \text{Rp } 189.901.129$$
   $$\text{Present Value of Costs} = 60.500.000$$
   $$\text{BCR} = \frac{189.901.129}{60.500.000} = \mathbf{3,14} > 1 \quad (\textbf{SANGAT LAYAK})$$
3. **Payback Period / Titik Impas (BEP)**:
   $$\text{Penghematan Bersih per Bulan} = \frac{\text{Rp } 73.690.000}{12} = \text{Rp } 6.140.833\text{ / bulan}$$
   $$\text{Payback Period} = \frac{\text{Rp } 60.500.000}{\text{Rp } 6.140.833} = \mathbf{9,85\text{ Bulan}} \quad (< 1\text{ Tahun})$$

Grafik kurva titik impas (*Break-Even Point*) disajikan pada Gambar 5.1.

![Grafik Analisis Kelayakan BEP](/docs/capstone/diagrams/gambar_5_1_analisis_kelayakan_bep.png)
*Gambar 5.1 Grafik Titik Impas (Break-Even Point) Sistem Otomasi Pemantauan Pusdalops BNPB*

---

### 5.2.3 Analisis Sensitivitas Biaya (*Sensitivity Analysis*)

Analisis sensitivitas dilakukan untuk menguji ketahanan kelayakan investasi terhadap dua skenario risiko:
* **Skenario 1 (Kenaikan Biaya OPEX +20%)**: Biaya sewa server dan pemeliharaan naik menjadi Rp 34.080.000/tahun.
  * Hasil: NPV turun menjadi **Rp 114.770.852** (tetap bernilai positif tinggi $>0$), BCR = **2,90**.
* **Skenario 2 (Penurunan Efisiensi Manfaat -15%)**: Manfaat penghematan jam kerja berkurang 15% menjadi Rp 86.776.500/tahun.
  * Hasil: NPV turun menjadi **Rp 89.288.631** (tetap bernilai positif $>0$), BCR = **2,47**.

Kedua skenario membuktikan bahwa investasi perancangan sistem ini memiliki ketahanan finansial yang kokoh (*robust*) dan memberikan nilai tambah ekonomis yang tinggi bagi instansi pemerintah.

---

## 5.3 Rencana Implementasi Hasil Rancangan (*Implementation & Change Management*)

Agar sistem dapat diadopsi dengan sukses di meja piket Pusdalops BNPB, disusun rencana penerapan bertahap yang mencakup manajemen perubahan:

**Tabel 5.4 Rencana Jadwal Penerapan Sistem (*Rollout Roadmap*)**
| Pekan / Tahap | Aktivitas Utama | Pihak yang Terlibat | Luaran / *Deliverables* |
| :---: | :--- | :--- | :--- |
| **Pekan 1** | *Staging & Environment Provisioning* | Tim IT BNPB & Pengembang | Server produksi Linux & PostgreSQL aktif |
| **Pekan 2** | Migrasi Master Data Wilayah & Pengujian Beban | Pengembang & Tim Data | Master Kemendagri 100% tersinkronisasi |
| **Pekan 3** | Sosialisasi & Pelatihan Meja Piket (Shift 1, 2, 3) | Seluruh Operator Piket | Operator mampu menggunakan antarmuka 5 blok |
| **Pekan 4 – 5** | *Parallel Run* (Sistem Berjalan Berdampingan) | Operator Piket & Supervisor | Verifikasi ganda hasil Lapsit Word vs manual |
| **Pekan 6 dst.** | *Full Cutover* & Operasional Mandiri | Pusdalops BNPB | Sistem resmi menjadi alat kerja utama dinas |

### Manajemen Perubahan (*Change Management*):
1. **Pembaruan Standard Operating Procedure (SOP)**: Menerbitkan revisi SOP meja piket yang mewajibkan konfirmasi data dilakukan melalui dasbor sistem dan mewajibkan penguncian status (*Lock Snapshot*) oleh supervisor sebelum laporan dikirim ke pimpinan.
2. **Buku Panduan Pengoperasian (*User Manual*)**: Menyediakan buku manual ringkas berukuran saku di setiap meja piket yang menjelaskan langkah-langkah verifikasi dan prosedur darurat pembukaan kunci (*Emergency Unlock*).
