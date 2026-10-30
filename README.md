# Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

> **Capstone Design Project** — S1 Sistem Informasi Telkom University Jakarta  
> **Unit Operasional:** Pusat Pengendalian Operasi Penanggulangan Bencana (Pusdalops-PB) BNPB

Platform intelijen kebencanaan terintegrasi yang mengotomasi pemantauan 24 jam (siklus operasional 07:00 – 07:00 WIB), integrasi multi-sumber (BMKG & media), deduplikasi laporan berita multi-lapis, dan penyusunan otomatis **Laporan Harian Situasi Bencana (Lapsit Bagian A)**.

---

## 🌟 Fitur Utama

1. **Windowing Siklus Operasional 24 Jam**:
   - Siklus cut-off resmi 07:00 – 07:00 WIB dengan countdown timer menuju cut-off.
   - Fitur kunci (*lock*) dan buka kunci (*unlock*) siklus dengan audit trail.
2. **Dual-Trigger Data Ingestion**:
   - Background ingestion otomatis dan sinkronisasi manual instan (*On-Demand Sync*).
   - Integrasi API Gempa Real-time BMKG dan agregator berita kebencanaan.
3. **Penyaring & Deduplikasi Cerdas**:
   - Filter adaptif gempa bumi signifikan ($M \ge 5.0$, kedalaman $\le 20\text{ km}$, atau gempa darat merusak).
   - Deduplikasi 2 lapis (kemiripan teks $\ge 80\%$ dan kemiripan entitas wilayah $\ge 60\%$).
   - Fitur penggabungan berita susulan (*Merge Follow-up Reports*).
4. **Antrean Meja Piket & Verifikasi**:
   - Status tab: `Belum Terverifikasi`, `Terverifikasi`, `Hoaks`, dan `Semua Data`.
   - Klasifikasi otomatis tag darurat (misal: `ISU BANTUAN`).
5. **Ekspor & Pelaporan Otomatis**:
   - Generator dokumen resmi format Word/DOCX (*Laporan Harian Situasi Bencana*).
   - Formatter ringkasan pesan cepat untuk WhatsApp grup komando pimpinan.

---

## 🏗️ Struktur Direktori

```text
├── apps/
│   ├── analytics/        # Logika deduplikasi, tagger isu darurat, pencocokan wilayah
│   ├── dashboard/        # Antarmuka Command Center & Generator DOCX/WA
│   ├── disasters/        # Model database kejadian bencana & audit trail verifikasi
│   └── ingestion/        # Adapter sumber data (BMKG, Google News, media sosial)
├── config/               # Konfigurasi Django & ASGI/WSGI
├── data/                 # Master data wilayah (Kemendagri)
├── docs/capstone/        # Dokumen laporan lengkap Capstone, bab 1-7 & diagram arsitektur
├── stitch_pusdalops_.../ # Prototipe desain antarmuka dashboard Pusdalops
├── manage.py             # Script utilitas manajemen Django
├── requirements.txt      # Dependensi project Python
└── README.md
```

---

## 🚀 Panduan Menjalankan Sistem

### 1. Prasyarat
- Python 3.10 atau lebih baru
- Virtual environment (direkomendasikan)

### 2. Instalasi Dependensi
```bash
python -m venv env
# Windows:
.\env\Scripts\activate
# Linux/macOS:
source env/bin/activate

pip install -r requirements.txt
```

### 3. Migrasi Database & Seeding Data
```bash
python manage.py makemigrations
python manage.py migrate
python seed_and_ingest.py
```

### 4. Menjalankan Server Pengembangan
```bash
python manage.py runserver
```
Akses dashboard pada peramban melalui: `http://127.0.0.1:8000/`

---

## 📄 Lisensi & Hak Cipta
Capstone Design Project — Dikembangkan untuk pemenuhan kelulusan S1 Sistem Informasi Telkom University Jakarta berkolaborasi dengan Pusdalops-PB BNPB.