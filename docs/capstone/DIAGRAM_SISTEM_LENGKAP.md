# DOKUMENTASI LENGKAP 7 DIAGRAM PERANCANGAN SISTEM
## Sistem Otomasi Pemantauan Kebencanaan Pusdalops BNPB
**Pembagian Tugas Tim Capstone:**
1. **BPMN AS-IS & TO-BE** — *Abid*
2. **User Interface (UI / Mockup)** — *Seto & Pandhu*
3. **Use Case Diagram & Spesifikasi** — *Adel*
4. **Activity Diagram** — *Abid*
5. **Class Diagram** — *Adel*
6. **Entity Relationship Diagram (ERD)** — *Seto*
7. **Sequence Diagram** — *Pandhu*

---

## 1. BPMN (BUSINESS PROCESS MODEL AND NOTATION) — Penanggung Jawab: Abid

### 1.1 BPMN AS-IS (Proses Bisnis Eksisting / Konvensional)
Proses bisnis yang saat ini berjalan secara manual di meja piket Pusdalops BNPB:

```mermaid
sequenceDiagram
    autonumber
    actor Media as Portal Media & BMKG
    actor Operator as Operator Meja Piket (3 Shift)
    actor BPBD as Satgas BPBD Daerah
    actor Pimpinan as Kepala BNPB / Pimpinan

    Media->>Operator: Terbit berita bencana & rilis gempa (tersebar)
    Note over Operator: Buka puluhan tab browser manual
    Note over Operator: Membaca & menyalin teks satu per satu
    Note over Operator: Memilah manual berita duplikat (mata telanjang)
    Operator->>BPBD: Hubungi via telepon / grup WhatsApp manual
    BPBD-->>Operator: Konfirmasi data korban & kerusakan
    Note over Operator: Rekapitulasi di lembar kerja & spreadsheet
    Note over Operator: Pergantian shift (serah terima catatan manual)
    Note over Operator: Menjelang cut-off 07.00 WIB: Ketik ulang ke Microsoft Word
    Note over Operator: Format indentasi & kop dinas diatur manual (60-90 menit)
    Operator->>Pimpinan: Serahkan naskah fisik / kirim file Word (Sering terlambat)
```

**Karakteristik & Kelemahan Proses AS-IS:**
* **Beban Kognitif Tinggi**: Operator harus memantau banyak portal secara manual 24 jam.
* **Redundansi Berulang**: 30%–40% artikel yang disalin merupakan pengulangan dari kejadian yang sama.
* **Risiko *Human Error***: Pengetikan ulang rentan salah toponimi wilayah dan salah hitung korban.
* **Keterlambatan Ekspor**: Penyusunan laporan Lapsit memakan waktu 60–90 menit menjelang pukul 07.00 WIB.

---

### 1.2 BPMN TO-BE (Proses Bisnis Usulan dengan Sistem Otomasi)
Proses bisnis baru setelah sistem otomasi diterapkan di Pusdalops BNPB:

```mermaid
flowchart TD
    Start([Mulai: Siklus 24 Jam 07.00 WIB]) --> Feeds[1. Ingestion Otomatis Celery / Tombol Sync Now]
    Feeds --> FilterGempa{2. Filter Gempa Adaptif?}
    FilterGempa -- "Tidak (M < 5.0 / Non-Signifikan)" --> DropGempa[Abaikan / Log Buffer]
    FilterGempa -- "Ya (M >= 5.0 / Dangkal Merusak)" --> Dedup
    
    Feeds --> Dedup{3. Deduplikasi 2 Lapis NLP?}
    Dedup -- "Similarity >= 0.80 Leksikal" --> MergeAuto[Gabung Otomatis ke Kejadian Induk]
    Dedup -- "Similarity >= 0.60 & Kab/Waktu Sama" --> MergeAuto
    Dedup -- "Berita Unik Baru" --> AntreanPending[4. Masuk Antrean Dasbor: Tab PENDING]
    MergeAuto --> AntreanPending

    AntreanPending --> CekBantuan{Terdeteksi Kata Kunci Keluhan Warga?}
    CekBantuan -- Ya --> SetBadge[Sematkan Badge: 🚨 ISU BANTUAN]
    CekBantuan -- Tidak --> MejaPiket
    SetBadge --> MejaPiket[5. Operator Membuka Modal Verifikasi 5 Blok]

    MejaPiket --> KontakDaerah[Hubungi Satgas BPBD Daerah via Kontak Tertera]
    KontakDaerah --> KeputusanStatus{Hasil Verifikasi Lapangan?}
    
    KeputusanStatus -- "Berita Palsu / Hoaks" --> SetHoaks[Ubah Status: HOAKS + Catat Alasan Bantahan]
    KeputusanStatus -- "Valid & Faktual" --> SetValid[Ubah Status: TERVERIFIKASI + Input Dampak Riil]
    
    SetHoaks --> AuditLog[Catat ke log_audit_verifikasi]
    SetValid --> AuditLog

    AuditLog --> Supervisor{Supervisor: Kunci Siklus?}
    Supervisor -- "Lock Snapshot" --> Lock[Kunci Status Siklus: Read-Only]
    
    Lock --> DualExport[6. Dual Output Satu-Klik]
    DualExport --> ExportWA[📋 Salin Format WhatsApp Pimpinan]
    DualExport --> ExportWord[📄 Unduh Berkas Word .docx Bagian A Resmi <= 5s]
    ExportWA --> Selesai([Laporan Terkirim Tepat Waktu])
    ExportWord --> Selesai
```

---

## 2. USER INTERFACE (UI / WIREFRAME & MOCKUP) — Penanggung Jawab: Seto & Pandhu

Sistem antarmuka dirancang dengan empat halaman/modal utama:

### 2.1 UI 1: Dasbor Pemantauan Meja Piket (Halaman Utama)
* **Header Bar**:
  * Logo Pusdalops BNPB + Teks *"Sistem Otomasi Pemantauan Kebencanaan Pusdalops-PB"*.
  * Tombol Quick Trigger: `[🔄 Tarik Data Sekarang / Sync Now]`.
  * Status Operator: *"Petugas: [Nama Operator] | Shift 3 (Malam) | Siklus: SIKLUS-20261012"*.
  * Widget *Countdown Timer Cut-Off*: *"⏳ 06j 14m 20s menuju Cut-Off 07.00 WIB"*.
* **Selector Siklus**:
  * Tombol navigasi: `[◀ Siklus Kemarin]` | `[Pilih Tanggal: YYYY-MM-DD]` | `[Siklus Besok ▶]`.
* **Tab Navigasi Status (4 Tab Dinamis)**:
  1. `🔴 Belum Terverifikasi (Pending)` *(dengan badge jumlah artikel antrean aktif)*.
  2. `🟢 Terverifikasi` *(daftar kejadian valid siap ekspor)*.
  3. `⚫ Hoaks` *(daftar berita ditolak beserta alasan bantahan)*.
  4. `⚪ Semua Data` *(seluruh data siklus)*.
* **Tabel Antrean Data Grid**:
  * Kolom: Waktu Tayang | Jenis Bencana | Wilayah (Provinsi/Kabupaten Kemendagri) | Judul Berita & Ringkasan | Rujukan Media (*Lead + N Sumber*) | Status Badge (`[🚨 ISU BANTUAN]`) | Tombol Aksi: `[🔗 Gabung / Merge]` & `[✏️ Edit Metadata & Verifikasi]`.

---

### 2.2 UI 2: Modal Pop-up "Edit Metadata & Verifikasi" (5 Blok Ringkas)
Modal yang muncul ketika tombol `[✏️ Edit Metadata]` ditekan:
* **Blok 1: Wilayah Kemendagri**:
  * Dropdown bertingkat: *Pilih Provinsi* → *Pilih Kabupaten/Kota* → *Pilih Kecamatan*.
* **Blok 2: Waktu Kejadian Faktual Lapangan**:
  * Input *Tanggal Kejadian* (Date Picker) & *Waktu Kejadian* (Time Picker WIB).
  * Dropdown *Pindahkan ke Siklus* (untuk kejadian batas waktu *edge case*).
* **Blok 3: Fakta Dampak Lapangan**:
  * Korban Jiwa: Meninggal, Luka-Luka, Hilang, Mengungsi (Input numerik dengan default 0).
  * Kerusakan Fisik: Rumah Rusak Berat, Sedang, Ringan, Terendam, Sarana Fasum.
* **Blok 4: Upaya TRC & Situasi Mutakhir**:
  * Textarea: *Upaya Penanganan BPBD di Lokasi*.
  * Textarea: *Kondisi Mutakhir Lapangan (Tinggi Genangan, Cuaca, Situasi)*.
* **Blok 5: Keputusan Status & Jejak Audit**:
  * Radio Button: `( ) PENDING` | `(*) TERVERIFIKASI` | `( ) HOAKS`.
  * Input: *Nama Personil BPBD yang Dikonfirmasi* & *No. Kontak*.
  * Textarea: *Catatan Forensik / Alasan Bantahan (Wajib jika status HOAKS)*.
  * Tombol: `[Batal]` | `[💾 Simpan & Perbarui Status]`.

---

### 2.3 UI 3: Modal "Gabung Berita Susulan (Merge)" & "Tambah Manual"
* **Modal Gabung Berita (`[🔗 Merge]`)**:
  * Menampilkan informasi Berita B yang akan digabung.
  * Dropdown: *Pilih Kejadian Induk A dalam Siklus Berjalan*.
  * Tombol `[Konfirmasi Gabung Berita]` → Memindahkan seluruh rujukan artikel Berita B ke Kejadian Induk A.
* **Modal Tambah Manual (`[+ Tambah Kejadian Manual]`)**:
  * Formulir ad-hoc untuk input bencana dari sambungan telepon darurat / radio HF Pusdalops.

---

### 2.4 UI 4: Pusat Ekspor Laporan (*Export Center & Lock Snapshot*)
* **Pratinjau Format Dokumen Resmi**: Menampilkan preview layout naskah Lapsit Bagian A.
* **Tombol Penguncian (*Lock Snapshot*)**:
  * Tombol `[🔒 Kunci Siklus Laporan]` *(khusus akun Supervisor)* → Mengubah antrean menjadi *read-only*.
  * Tombol `[🔓 Buka Kunci Darurat / Emergency Unlock]` dengan modal alasan pembukaan.
* **Tombol Aksi Ekspor**:
  * `[📄 Unduh Berkas Word (.docx) Bagian A Resmi]` (komputasi $\le 5$ detik).
  * `[📋 Salin Format Ringkasan WhatsApp]` (format klaster dinas).

---

## 3. USE CASE DIAGRAM & SPESIFIKASI — Penanggung Jawab: Adel

### 3.1 Use Case Diagram (UML)

```mermaid
flowchart LR
    subgraph AKTOR
        OP[Operator Meja Piket]
        SP[Supervisor Pusdalops]
        EXT[Sistem Eksternal: BMKG / RSS]
        BPBD[Satgas BPBD Daerah]
    end

    subgraph SISTEM_PUSDALOPS [Sistem Otomasi Pemantauan Pusdalops BNPB]
        UC1([UC-01: Tarik Feed Otomatis & On-Demand])
        UC2([UC-02: Memantau Antrean Berdasarkan Siklus 24 Jam])
        UC3([UC-03: Filter Status Data Pending / Terverifikasi / Hoaks])
        UC4([UC-04: Menggabungkan Berita Susulan - Merge])
        UC5([UC-05: Tambah Kejadian Manual Radio/Telepon])
        UC6([UC-06: Verifikasi & Koreksi Metadata Lapangan 5 Blok])
        UC7([UC-07: Catat Bantahan Berita Hoaks & Log Audit])
        UC8([UC-08: Kunci Siklus - Lock Snapshot])
        UC9([UC-09: Buka Kunci Darurat - Emergency Unlock])
        UC10([UC-10: Ekspor Berkas Word .docx Bagian A Resmi])
        UC11([UC-11: Salin Ringkasan Pesan WhatsApp Pimpinan])
        UC12([UC-12: Kelola Master Wilayah Kemendagri & Akun])
    end

    EXT --> UC1
    OP --> UC1
    OP --> UC2
    OP --> UC3
    OP --> UC4
    OP --> UC5
    OP --> UC6
    OP --> UC7
    OP --> UC10
    OP --> UC11

    BPBD -.->|Dikonfirmasi via Telepon| UC6
    BPBD -.->|Klarifikasi Kebenaran| UC7

    SP --> UC2
    SP --> UC8
    SP --> UC9
    SP --> UC10
    SP --> UC11
    SP --> UC12

    UC8 -.->|Includes| UC2
    UC6 -.->|Updates| UC3
```

---

## 4. ACTIVITY DIAGRAM — Penanggung Jawab: Abid

### 4.1 Activity Diagram: Verifikasi, Deduplikasi & Ekspor Laporan
Menjelaskan aliran kontrol operasional sistem dari data mentah masuk hingga terbitnya laporan dinas:

```mermaid
stateDiagram-v2
    [*] --> IngestionData: Celery Beat / Tombol Sync Now
    
    state IngestionData {
        [*] --> FetchFeeds: Ambil XML RSS & API BMKG
        FetchFeeds --> ParsingText: Ekstraksi Judul & Toponimi
    }

    IngestionData --> CekGempa: Evaluasi Parameter
    state CekGempa <<choice>>
    CekGempa --> DiscardGempa: M < 5.0 & Tidak Merusak
    DiscardGempa --> [*]
    CekGempa --> HitungDeduplikasi: Gempa M >= 5.0 / Bencana Umum

    HitungDeduplikasi --> EvaluasiSimilarity: Hitung TF-IDF & Cosine Similarity
    state EvaluasiSimilarity <<choice>>
    EvaluasiSimilarity --> LinkToMaster: Similarity >= 0.80 (Lapis 1)
    EvaluasiSimilarity --> CekWilayah: Similarity 0.60 - 0.79
    EvaluasiSimilarity --> CreateNewIncident: Similarity < 0.60

    state CekWilayah <<choice>>
    CekWilayah --> LinkToMaster: Wilayah & Waktu Sama (<24 jam) (Lapis 2)
    CekWilayah --> CreateNewIncident: Wilayah / Waktu Berbeda

    LinkToMaster --> AntreanPiket: Tambah Referensi Sekunder
    CreateNewIncident --> AntreanPiket: Masuk Tab PENDING

    AntreanPiket --> PeriksaIsu: Evaluasi Kata Kunci Keluhan
    state PeriksaIsu <<choice>>
    PeriksaIsu --> BeriBadgeAlarm: Ada Kata 'Bantuan/Tenda/Kelaparan'
    PeriksaIsu --> TampilkanNormal: Teks Normal
    BeriBadgeAlarm --> TampilkanNormal

    TampilkanNormal --> OperatorReview: Operator Buka Modal 5 Blok
    OperatorReview --> HubungiBPBD: Kroscek Telepon/WA ke Satgas Daerah

    HubungiBPBD --> KeputusanVerifikasi: Tentukan Status Kejadian
    state KeputusanVerifikasi <<choice>>
    KeputusanVerifikasi --> StatusHoaks: Informasi Fiktif / Kedaluwarsa
    KeputusanVerifikasi --> StatusTerverifikasi: Informasi Valid Faktual

    StatusHoaks --> SimpanAudit: Catat Alasan Bantahan Resmi
    StatusTerverifikasi --> SimpanAudit: Input Dampak Korban & Fasilitas

    SimpanAudit --> CekKesiapanEkspor: Tab PENDING Bersih?
    state CekKesiapanEkspor <<choice>>
    CekKesiapanEkspor --> AntreanPiket: Masih Ada Data Pending
    CekKesiapanEkspor --> KunciSiklus: Supervisor Eksekusi Lock Snapshot

    KunciSiklus --> EksporOutput: Pilihan Format Luaran
    state EksporOutput {
        [*] --> GenWord: python-docx Generator (<=5s)
        [*] --> GenWA: WhatsApp Text Cluster Formatter
    }

    EksporOutput --> [*]: Distribusi Lapsit ke Pimpinan
```

---

## 5. CLASS DIAGRAM — Penanggung Jawab: Adel

### 5.1 Class Diagram (Struktur Kelas & Service Architecture)

```mermaid
classDiagram
    class MasterWilayah {
        +String id_wilayah
        +String nama_wilayah
        +String level
        +String parent_id
        +get_full_hierarchy() String
        +match_toponym(text: String) MasterWilayah
    }

    class SiklusLaporan {
        +String kode_siklus
        +DateTime waktu_buka
        +DateTime waktu_tutup
        +Boolean is_locked
        +String locked_by
        +DateTime locked_at
        +lock_cycle(user: String) void
        +emergency_unlock(user: String, reason: String) void
        +is_cut_off_passed() Boolean
    }

    class KejadianBencana {
        +Integer id_kejadian
        +String kode_kejadian
        +String jenis_bencana
        +DateTime waktu_kejadian_riil
        +String waktu_kejadian_text
        +JSON dampak_korban
        +JSON dampak_kerusakan
        +Text upaya
        +Text kondisi_mutakhir
        +String status_verifikasi
        +Boolean is_manual_entry
        +Boolean is_isu_bantuan
        +verify(status: String, user: String) void
        +merge_with(secondary_id: Integer) void
        +get_formatted_korban() String
        +get_formatted_kerusakan() String
    }

    class BeritaBencana {
        +Integer id_berita
        +String judul
        +Text url_artikel
        +String nama_portal
        +Text isi_ringkas
        +DateTime waktu_terbit
        +Float similarity_score
        +Boolean is_master_source
        +extract_clean_text() String
    }

    class LogAuditVerifikasi {
        +Integer id_log
        +String id_user
        +String shift
        +String status_sebelum
        +String status_sesudah
        +String kontak_bpbd_dihubungi
        +Text catatan
        +DateTime waktu_aksi
    }

    class DeduplicationEngine {
        -Float threshold_tier1 = 0.80
        -Float threshold_tier2 = 0.60
        +compute_similarity(text1: String, text2: String) Float
        +evaluate_duplicate(new_news: BeritaBencana, existing_list: List) KejadianBencana
    }

    class WindowingEngine {
        +get_current_cycle(target_time: DateTime) Tuple
        +assign_incident_to_cycle(incident: KejadianBencana) SiklusLaporan
        +get_countdown_to_cutoff() String
    }

    class DocxReportGenerator {
        -String template_path
        +generate_bagian_a(kejadian_list: List, siklus: SiklusLaporan) Document
        +apply_null_safety(val: Object, default_phrase: String) String
        +save_to_stream() BytesIO
    }

    class WhatsAppFormatter {
        +format_by_clusters(kejadian_list: List, siklus: SiklusLaporan) String
    }

    MasterWilayah "1" <-- "0..*" MasterWilayah : parent-child
    MasterWilayah "1" <-- "0..*" KejadianBencana : located_at
    SiklusLaporan "1" <-- "0..*" KejadianBencana : belongs_to
    KejadianBencana "1" <-- "1..*" BeritaBencana : references
    KejadianBencana "1" <-- "0..*" LogAuditVerifikasi : logs

    KejadianBencana ..> DeduplicationEngine : uses
    SiklusLaporan ..> WindowingEngine : manages
    DocxReportGenerator ..> KejadianBencana : transforms
    WhatsAppFormatter ..> KejadianBencana : transforms
```

---

## 6. ENTITY RELATIONSHIP DIAGRAM (ERD) — Penanggung Jawab: Seto

### 6.1 ERD Relasional Basis Data (Crow's Foot Notation)

```mermaid
erDiagram
    MASTER_WILAYAH ||--o{ MASTER_WILAYAH : "parent_of"
    MASTER_WILAYAH ||--o{ KEJADIAN_BENCANA : "lokasi_kejadian"
    SIKLUS_LAPORAN ||--o{ KEJADIAN_BENCANA : "periode_siklus"
    KEJADIAN_BENCANA ||--|{ BERITA_BENCANA : "merujuk_artikel"
    KEJADIAN_BENCANA ||--o{ LOG_AUDIT_VERIFIKASI : "merekam_jejak"

    MASTER_WILAYAH {
        VARCHAR(20) id_wilayah PK "Kode Kemendagri"
        VARCHAR(100) nama_wilayah "Nama Provinsi/Kab/Kec"
        VARCHAR(20) level "PROVINSI/KAB_KOTA/KECAMATAN"
        VARCHAR(20) parent_id FK "Relasi ke induk"
    }

    SIKLUS_LAPORAN {
        VARCHAR(30) kode_siklus PK "SIKLUS-YYYYMMDD"
        TIMESTAMPTZ waktu_buka "Pukul 07.00 WIB H"
        TIMESTAMPTZ waktu_tutup "Pukul 07.00 WIB H+1"
        BOOLEAN is_locked "Status kunci laporan"
        VARCHAR(100) locked_by "Akun supervisor"
        TIMESTAMPTZ locked_at "Waktu penguncian"
    }

    KEJADIAN_BENCANA {
        SERIAL id_kejadian PK "ID Kejadian"
        VARCHAR(50) kode_kejadian UK "DIS-YYYYMMDD-XXX"
        VARCHAR(30) kode_siklus FK "Relasi siklus"
        VARCHAR(50) jenis_bencana "Banjir/Gempa/Longsor"
        VARCHAR(20) id_wilayah FK "Relasi wilayah"
        TIMESTAMPTZ waktu_kejadian_riil "Waktu riil kejadian"
        VARCHAR(100) waktu_kejadian_text "Label waktu dinas"
        JSONField dampak_korban "Meninggal/Luka/Hilang/Mengungsi"
        JSONField dampak_kerusakan "Rumah/Fasum/Lahan"
        TEXT upaya "Tindakan TRC BPBD"
        TEXT kondisi_mutakhir "Situasi terkini di lokasi"
        VARCHAR(20) status_verifikasi "PENDING/TERVERIFIKASI/HOAKS"
        BOOLEAN is_manual_entry "True jika input radio/telepon"
        BOOLEAN is_isu_bantuan "True jika keluhan logistik"
    }

    BERITA_BENCANA {
        SERIAL id_berita PK "ID Berita"
        INTEGER id_kejadian FK "Relasi kejadian induk"
        VARCHAR(255) judul "Judul artikel media"
        TEXT url_artikel "Tautan asli media"
        VARCHAR(100) nama_portal "Detik/Kompas/Antara/BMKG"
        TEXT isi_ringkas "Ringkasan narasi"
        TIMESTAMPTZ waktu_terbit "Timestamp rilis media"
        FLOAT similarity_score "Skor kemiripan NLP"
        BOOLEAN is_master_source "True jika rujukan utama"
    }

    LOG_AUDIT_VERIFIKASI {
        SERIAL id_log PK "ID Log Forensik"
        INTEGER id_kejadian FK "Relasi kejadian"
        VARCHAR(100) id_user "Akun operator piket"
        VARCHAR(20) shift "Shift 1 / 2 / 3"
        VARCHAR(20) status_sebelum "Status lama"
        VARCHAR(20) status_sesudah "Status baru"
        VARCHAR(100) kontak_bpbd_dihubungi "Nama & nomor petugas daerah"
        TEXT catatan "Alasan bantahan jika hoaks"
        TIMESTAMPTZ waktu_aksi "Timestamp pencatatan"
    }
```

---

## 7. SEQUENCE DIAGRAM — Penanggung Jawab: Pandhu

### 7.1 Sequence Diagram: Skenario Ingestion, Verifikasi Lapangan, dan Ekspor Laporan Resmi

```mermaid
sequenceDiagram
    autonumber
    actor Operator as Operator Meja Piket
    actor Supervisor as Supervisor Pusdalops
    participant UI as Dasbor Web Pusdalops
    participant Controller as Pusdalops View/Controller
    participant Dedup as Deduplication NLP Engine
    participant DB as Basis Data (Django ORM)
    participant DocxGen as Docx Report Generator

    %% Skenario 1: On-Demand Ingestion
    Operator->>UI: Klik tombol [🔄 Sync Now]
    UI->>Controller: POST /api/ingest/sync/
    activate Controller
    Controller->>Controller: Tarik API BMKG & RSS Berita
    Controller->>Dedup: Evaluasi Teks & Parameter Gempa
    activate Dedup
    Dedup-->>Controller: Hasil Deduplikasi (Induk & Referensi)
    deactivate Dedup
    Controller->>DB: Simpan ke kejadian_bencana & berita_bencana
    Controller-->>UI: 200 OK (Data Teragregasi & Terpotong Siklus)
    deactivate Controller
    UI-->>Operator: Tampilkan antrean di Tab PENDING (Alarm Bantuan aktif)

    %% Skenario 2: Verifikasi Data 5 Blok
    Operator->>UI: Klik [✏️ Edit Metadata & Verifikasi]
    UI-->>Operator: Buka Modal 5 Blok (Toponimi, Dampak, Upaya, Kontak)
    Operator->>UI: Isi data dampak riil & pilih status [TERVERIFIKASI]
    Operator->>UI: Klik [💾 Simpan & Perbarui Status]
    UI->>Controller: POST /api/kejadian/{id}/verify/
    activate Controller
    Controller->>DB: Update kejadian_bencana (status='TERVERIFIKASI')
    Controller->>DB: INSERT log_audit_verifikasi (user, shift, kontak, waktu)
    Controller-->>UI: 200 OK (Status Berpindah ke Tab TERVERIFIKASI)
    deactivate Controller

    %% Skenario 3: Penguncian Siklus oleh Supervisor
    Supervisor->>UI: Buka Pusat Ekspor & Klik [🔒 Lock Snapshot]
    UI->>Controller: POST /api/siklus/{kode}/lock/
    activate Controller
    Controller->>DB: UPDATE siklus_laporan SET is_locked=TRUE
    Controller-->>UI: 200 OK (Siklus Terkunci - Read Only)
    deactivate Controller

    %% Skenario 4: Ekspor Dokumen Resmi
    Operator->>UI: Klik [📄 Unduh Word (.docx) Bagian A]
    UI->>Controller: GET /export/docx/?siklus=SIKLUS-20261012
    activate Controller
    Controller->>DB: SELECT * WHERE status='TERVERIFIKASI' & siklus=SIKLUS-20261012
    DB-->>Controller: Daftar kejadian terverifikasi
    Controller->>DocxGen: build_lapsit_bagian_a_docx(kejadian_list)
    activate DocxGen
    DocxGen->>DocxGen: Terapkan Kop Navy, Tabel, & Null-Safety Dinas
    DocxGen-->>Controller: File Stream .docx (Durasi <= 1.42s)
    deactivate DocxGen
    Controller-->>UI: File Download (Lapsit_Bagian_A_Pusdalops_BNPB.docx)
    deactivate Controller
    UI-->>Operator: Unduh Berkas Word Resmi Siap Kirim ke Pimpinan
```
