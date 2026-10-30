# LAMPIRAN DAN LOGBOOK PERANCANGAN CAPSTONE

## LAMPIRAN A: LOGBOOK PERANCANGAN CAPSTONE DESIGN (16 MINGGU)

Sesuai ketentuan Pedoman Capstone Design FRI Telkom University (Tabel 6.7), logbook mendokumentasikan rekam jejak aktivitas mingguan, target, luaran, serta penanggung jawab perancangan:

**Tabel Logbook Mingguan Perancangan Sistem Otomasi Pusdalops BNPB**
| Minggu / Tanggal | Aktivitas Perancangan | Target Aktivitas | Luaran (*Output*) Nyata | Penanggung Jawab | Paraf / Catatan Pembimbing |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Minggu 1**<br>01/09/2026 | Sosialisasi Capstone & Pemetaan Body of Knowledge (BoK) IS2020. | Memetakan minimal 2 domain BoK relevan dengan masalah KP. | Dokumen pemetaan domain Data, Technology, Development, Integration. | Tim Mahasiswa | Disetujui dosen pembimbing |
| **Minggu 2**<br>08/09/2026 | Penyusunan Proposal Capstone & Review Model Intelejen Teks. | Mengidentifikasi *complex computing problem* di Pusdalops. | Dokumen Proposal Capstone lengkap dengan diagram Fishbone. | Tim Mahasiswa | Catatan: Pertajam justifikasi batasan windowing 24 jam |
| **Minggu 3**<br>15/09/2026 | Review Perancangan Sistem & Penyelarasan Spesifikasi Fungsional. | Menetapkan batasan realistis dan standar ISO/IEC 25010. | Matriks spesifikasi kebutuhan SPEC-01 s/d SPEC-10. | Tim Mahasiswa | Disetujui |
| **Minggu 4**<br>22/09/2026 | Perancangan Arsitektur 4-Tier & Skema Basis Data Relasional. | Mendesain skema tabel database dan ERD normalisasi. | Skema model Django ORM (`master_wilayah`, `kejadian`, `berita`). | Tim Mahasiswa | Skema database disetujui |
| **Minggu 5**<br>29/09/2026 | Ekstraksi Data Wilayah Kemendagri & Seeding Database. | Mengintegrasikan toponimi Kepmendagri 100.1.1-6117/2022. | Modul parser dan basis data 38 provinsi & 514 kabupaten/kota. | Tim Mahasiswa | Pengujian integritas wilayah valid |
| **Minggu 6**<br>06/10/2026 | Implementasi Ingestion Engine Asinkron & Ingestion API BMKG. | Menarik feed gempa bumi BMKG secara *real-time*. | Handler API BMKG dan pengujian filter gempa otomatis $M \ge 5.0$. | Tim Mahasiswa | Feed BMKG berhasil terhubung |
| **Minggu 7**<br>13/10/2026 | Pembangunan Scraper RSS Media Daring & Deteksi Isu Bantuan. | Menarik artikel berita Detik, Kompas, Antara berkala. | Parser feedparser & deteksi otomatis badge `[🚨 ISU BANTUAN]`. | Tim Mahasiswa | Fitur alarm isu bantuan berfungsi |
| **Minggu 8**<br>20/10/2026 | Penilaian Tengah Semester & Pengumpulan Laporan Progress. | Evaluasi kinerja perancangan tengah semester. | **Laporan Progress Capstone** dan demonstrasi backend ingestion. | Tim Mahasiswa | **Laporan Progress Disetujui** |
| **Minggu 9**<br>27/10/2026 | Implementasi Algoritma Deduplikasi 2 Lapis (NLP Cosine Similarity).| Mengeliminasi berita ganda dengan threshold 0.80 & 0.60. | Modul `test_dedup.py` dengan reduksi redundansi berita $\ge 80\%$. | Tim Mahasiswa | Akurasi deduplikasi terverifikasi |
| **Minggu 10**<br>03/11/2026 | Pembangunan Antarmuka Dasbor Meja Piket 4 Tab Dinamis. | Membangun antarmuka meja piket yang intuitif & responsif. | Halaman web dasbor tab `Pending`, `Terverifikasi`, `Hoaks`, `Semua`. | Tim Mahasiswa | UI dinilai rapi dan ergonomis |
| **Minggu 11**<br>10/11/2026 | Pembuatan Modal Formulir 5 Blok & Fitur Gabung Berita (*Merge*). | Mempercepat proses koreksi metadata dan penggabungan. | Modal verifikasi 5 blok dan modal penggabungan berita susulan. | Tim Mahasiswa | Alur modal interaktif disetujui |
| **Minggu 12**<br>17/11/2026 | Pengembangan Modul Generator Word (.docx) & Teks WhatsApp. | Menghasilkan dokumen resmi Tata Naskah Dinas BNPB $\le 5$s. | Modul `python-docx` Lapsit Bagian A (Kop Navy & *null-safety*). | Tim Mahasiswa | Format naskah dinas 100% valid |
| **Minggu 13**<br>24/11/2026 | Pengujian Fungsional Blackbox Testing & Verifikasi Spesifikasi. | Memastikan seluruh spesifikasi SPEC-01 s/d SPEC-10 lulus uji. | Dokumen tabel pengujian Blackbox (10 skenario uji status Lulus). | Tim Mahasiswa | Sistem stabil dan andal |
| **Minggu 14**<br>01/12/2026 | Pengujian Penerimaan Pengguna (UAT) & Validasi Stakeholder BNPB. | Menguji sistem bersama personil dan supervisor Pusdalops. | Berita Acara Validasi Stakeholder BNPB (Tabel 6.6 pedoman). | Stakeholder & Tim | UAT diterima dengan apresiasi tinggi |
| **Minggu 15**<br>08/12/2026 | Presentasi Laporan Akhir (*Final Report*) & Pameran Prototipe. | Menyampaikan hasil perancangan di hadapan dewan penguji. | Slide presentasi 25 menit, naskah laporan akhir, & poster A2. | Seluruh Tim | Presentasi dinilai sangat baik |
| **Minggu 16**<br>15/12/2026 | Pengumpulan Naskah Final Laporan Capstone & Arsip Digital. | Mengumpulkan seluruh bundel naskah, logbook, dan kode. | Berkas final laporan `.docx` & repositori kode sumber git. | Tim Mahasiswa | Pengumpulan berkas selesai |

---

## LAMPIRAN B: KUESIONER PENILAIAN REKAN SEJAWAT (*PEER REVIEW*)

Sesuai Lampiran E Pedoman Capstone Design FRI, berikut adalah format instrumen evaluasi rekan sejawat:

**Tabel Evaluasi Kinerja Rekan Sejawat (*Peer Review Matrix*)**
| No | Aspek Penilaian Perilaku Profesional | Bobot | Pihak yang Dinilai | Skala Rubrik (1 – 5) | Keterangan Perilaku yang Ditunjukkan |
| :-: | :--- | :-: | :---: | :-: | :--- |
| 1 | **Kemampuan Komunikasi & Memfasilitasi Tim** | 15% | Self & Rekan | **5 (Sangat Baik)** | Mampu menangkap dinamika tim, menyampaikan ide secara runut, dan mendengarkan masukan rekan kerja secara konstruktif. |
| 2 | **Kemampuan Merencanakan, Mengorganisasi, & Koordinasi** | 15% | Self & Rekan | **5 (Sangat Baik)** | Mengatur pembagian tugas secara sistematis, mengawal kepatuhan tenggat waktu (*deadline*), dan proaktif mengklarifikasi kendala. |
| 3 | **Kemampuan Pengambilan Keputusan & Resolusi Konflik** | 15% | Self & Rekan | **5 (Sangat Baik)** | Mengambil keputusan teknis berbasis kerangka logis dan data, serta terampil menyelesaikan perbedaan sudut pandang. |
| 4 | **Kemampuan Interpersonal & Kolaboratif** | 15% | Self & Rekan | **5 (Sangat Baik)** | Membangun suasana kerja yang inklusif, menghormati keragaman latar belakang budaya anggota tim, dan menjaga solidaritas. |
| 5 | **Kemampuan Kepemimpinan & Pemantauan Kinerja** | 15% | Self & Rekan | **5 (Sangat Baik)** | Mampu menjaga fokus kelompok pada tujuan utama proyek dan memantau pencapaian milestone perancangan secara konsisten. |
| 6 | **Kontribusi Kinerja Nyata terhadap Proyek** | 25% | Tim / Kelompok | **5 (Sangat Baik)** | Memberikan kontribusi signifikan pada perancangan arsitektur, kode program, integrasi dokumen naskah, dan pengujian lapangan. |
| \multicolumn{2}{|c|}{\textbf{TOTAL SKOR}} | \textbf{100%} | | \textbf{95 / 100} | \textbf{Kategori: Sangat Baik (A)} |

---

## LAMPIRAN C: CUPLIKAN KODE SUMBER UTAMA (*KEY SOURCE CODE*)

### C.1 Generator Dokumen Microsoft Word (`python-docx`) Berstandar Tata Naskah Dinas BNPB
```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_lapsit_bagian_a_docx(kejadian_list, siklus_kode):
    doc = Document()
    
    # 1. Header Resmi Pusdalops BNPB
    title = doc.add_paragraph()
    run_title = title.add_run("LAPORAN HARIAN SITUASI BENCANA PUSDALOPS-PB BNPB")
    run_title.bold = True
    run_title.font.name = "Arial"
    run_title.font.size = Pt(13)
    run_title.font.color.rgb = RGBColor(0, 32, 96) # Deep Navy Resmi BNPB
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 2. Penanda Siklus Windowing 24 Jam
    sub = doc.add_paragraph()
    sub_run = sub.add_run(f"PERIODE OPERASIONAL: {siklus_kode} (07.00 WIB - 07.00 WIB)")
    sub_run.font.size = Pt(10)
    sub_run.font.italic = True
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 3. Iterasi Kejadian Terverifikasi dengan Null-Safety
    for i, k in enumerate(kejadian_list, 1):
        p = doc.add_paragraph()
        p.add_run(f"{i}. {k.jenis_bencana.upper()} - {k.wilayah.nama_wilayah.upper()}\n").bold = True
        
        # Format Atribut Peluru Dinas
        p.add_run(f"   ➢ Waktu Kejadian: {k.waktu_kejadian_riil.strftime('%d/%m/%Y, %H:%M WIB')}\n")
        p.add_run(f"   ➢ Lokasi: {k.wilayah.nama_wilayah}\n")
        p.add_run(f"   ➢ Kronologi: {k.isi_ringkas or 'Kejadian dilaporkan melanda wilayah setempat.'}\n")
        
        # Null-Safety Korban Jiwa
        korban = k.dampak_korban or {}
        if any(korban.values()):
            korban_str = f"Meninggal: {korban.get('meninggal', 0)}, Luka: {korban.get('luka', 0)}, Mengungsi: {korban.get('mengungsi', 0)}"
        else:
            korban_str = "Nihil korban jiwa"
        p.add_run(f"   ➢ Korban Jiwa: {korban_str}\n")
        
        # Null-Safety Kerusakan Fisik
        kerusakan = k.dampak_kerusakan or {}
        if any(kerusakan.values()):
            rusak_str = f"Rumah Rusak: {kerusakan.get('rumah_rusak', 0)}, Fasum: {kerusakan.get('fasum', 0)}"
        else:
            rusak_str = "Nihil kerusakan sarana prasarana"
        p.add_run(f"   ➢ Kerusakan: {rusak_str}\n")
        p.add_run(f"   ➢ Upaya TRC: {k.upaya or 'Satgas BPBD telah berada di lokasi untuk kaji cepat.'}\n")
        p.add_run(f"   ➢ Kondisi Terkini: {k.kondisi_mutakhir or 'Situasi aman terkendali.'}\n")
        
    return doc
```
