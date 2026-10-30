# BAB VII: KESIMPULAN DAN SARAN

## 7.1 Kesimpulan

Berdasarkan hasil perancangan, implementasi, pengujian fungsional, dan validasi bersama pemangku kepentingan di Pusdalops BNPB, dapat diambil kesimpulan yang menjawab seluruh tujuan perancangan yang telah ditetapkan pada Bab I:

1. **Arsitektur Sistem 4-Tier Terpadu**: Berhasil dirancang dan dibangun sistem otomasi pemantauan kebencanaan berbasis framework Django 5 dengan arsitektur 4-tier (*External Sources, Intelligence Ingestion, Storage ORM, Presentation & Export*) yang tangguh, terukur, dan mampu menangani proses agregasi data heterogen secara asinkron (*non-blocking*).
2. **Implementasi Windowing Engine 24 Jam**: Berhasil dikembangkan mekanisme pemotongan siklus operasional kedaruratan (pukul 07.00 WIB hari berjalan hingga pukul 07.00 WIB hari berikutnya) dengan formula kode siklus `SIKLUS-YYYYMMDD`, dilengkapi fitur fleksibilitas pemindahan siklus kejadian batas waktu (*edge cases*) dan widget hitung mundur (*countdown timer*) menuju batas *cut-off*.
3. **Intelijen Teks & Penyaring Adaptif**: Berhasil diimplementasikan algoritma *Penyaring Gempa Adaptif* ($M \ge 5.0$ kedalaman $\le 20$ km dan $M \ge 4.5$ dengan intensitas $\ge \text{III MMI}$) serta algoritma *Deduplikasi 2 Lapis* berbasis NLP Cosine Similarity ($\ge 0.80$ leksikal dan $\ge 0.60$ kontekstual wilayah) yang terbukti memangkas redundansi artikel berita hingga **85%** dan mendeteksi keluhan logistik darurat melalui badge alarm **`[🚨 ISU BANTUAN]`**.
4. **Antarmuka Meja Piket yang Efisien**: Berhasil dibangun antarmuka dasbor web meja piket dengan 4 tab status dinamis (`Pending`, `Terverifikasi`, `Hoaks`, `Semua Data`), formulir koreksi metadata 5 blok yang mempercepat input lapangan, formulir tambah kejadian manual ad-hoc, serta fitur penggabungan berita susulan (*merge*).
5. **Dual Output Generator Berstandar Tata Naskah Dinas**: Berhasil diwujudkan modul ekspor otomatis satu-klik yang mampu menghasilkan berkas Microsoft Word (`.docx`) Bagian A resmi berstandar Tata Naskah Dinas Pusdalops BNPB dalam durasi komputasi rata-rata **1,42 detik** ($\le 5$ detik target SLA) dengan jaminan kepatuhan frasa baku *null-safety*, serta generator ringkasan pesan instan WhatsApp terklaster untuk pimpinan.
6. **Kelayakan Investasi yang Sangat Tinggi**: Analisis kelayakan finansial membuktikan bahwa perancangan sistem ini sangat menguntungkan instansi dengan nilai *Net Present Value* (**NPV = +Rp 129.401.129**), *Benefit-Cost Ratio* (**BCR = 3,14**), dan titik impas tercapai dalam waktu singkat (**Payback Period = 9,85 bulan**).

---

## 7.2 Saran dan Rekomendasi

Untuk meningkatkan efektivitas pemanfaatan sistem serta kesinambungan pengembangannya di masa mendatang, disarankan beberapa hal sebagai berikut:

### 7.2.1 Rekomendasi bagi Instansi (Pusdalops BNPB)
1. **Adopsi ke Lingkungan Server Produksi Nasional**: Disarankan agar Pusdalops BNPB segera menempatkan aplikasi pada pusat data *cloud* instansi dengan konfigurasi *high-availability* dan basis data PostgreSQL PostGIS agar dapat diakses secara terdesentralisasi oleh seluruh BPBD provinsi/kabupaten/kota.
2. **Pembaruan Standar Operasional Prosedur (SOP) Meja Piket**: Perlu diterbitkan revisi SOP meja piket resmi yang menetapkan dasbor sistem sebagai sarana verifikasi tunggal dan mewajibkan penggunaan fitur penguncian siklus (*Lock Snapshot*) oleh supervisor sebelum laporan resmi dipublikasikan.
3. **Penguatan Kerja Sama API Antar-Lembaga**: Memperluas jalur komunikasi data langsung berbasis API tertutup dengan BMKG, PVMBG (Badan Geologi), dan Kementerian PUPR untuk memperkaya variasi indikator bencana geologi dan hidrometeorologi.

### 7.2.2 Rekomendasi untuk Pengembangan Sistem Lanjutan
1. **Integrasi Model Bahasa Alami Tingkat Lanjut (*Transformer/BERT*)**: Pada penelitian dan pengembangan lanjutan, model pembobotan TF-IDF dapat ditingkatkan menggunakan model bahasa terlatih berbahasa Indonesia (seperti *IndoBERT*) untuk meningkatkan akurasi ekstraksi entitas bernama (*Named Entity Recognition* / NER) terhadap nama desa dan dusun terpencil.
2. **Aplikasi Mobile untuk Satgas Lapangan (TRC BPBD)**: Mengembangkan aplikasi mobile terintegrasi bagi personil Tim Reaksi Cepat (TRC) di lapangan agar konfirmasi dampak korban dan foto kerusakan fisik dapat diunggah secara *real-time* langsung dari titik nol kejadian bencana.
3. **Modul Analisis Prediktif Spasial**: Mengintegrasikan sistem informasi geografis (GIS) dengan model pembelajaran mesin untuk memprediksi potensi jalur luapan banjir susulan berdasarkan data curah hujan dan elevasi topografi.
