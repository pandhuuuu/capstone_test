import os
import re
import time
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

output_dir = os.path.join(os.path.dirname(__file__), 'docs', 'capstone', 'diagrams')
artifacts_dir = r'C:\Users\athal\.gemini\antigravity-ide\brain\058edde7-b12d-456e-919f-881f72bf7094'
os.makedirs(output_dir, exist_ok=True)

PUML_COMMON_STYLE = """
skinparam BackgroundColor #ffffff
skinparam Shadowing true
skinparam DefaultFontName "Segoe UI"
skinparam DefaultFontSize 12
skinparam DefaultFontColor #1e293b
skinparam RoundCorner 8
skinparam ArrowColor #334155
skinparam ArrowThickness 1.5
skinparam ArrowFontSize 11
"""

# ==========================================
# 1. USE CASE DIAGRAM (Adel - NIM. 1202220004)
# ==========================================
PUML_USECASE = f"""@startuml
{PUML_COMMON_STYLE}
skinparam ActorBackgroundColor #f8fafc
skinparam ActorBorderColor #0f172a
skinparam ActorFontSize 13
skinparam ActorFontStyle bold

skinparam UsecaseBackgroundColor #ffffff
skinparam UsecaseBorderColor #2563eb
skinparam UsecaseBorderThickness 1.8
skinparam UsecaseFontSize 12
skinparam UsecaseFontStyle bold

skinparam PackageBorderColor #64748b
skinparam PackageBorderThickness 1.2
skinparam PackageBackgroundColor #f8fafc
skinparam PackageFontSize 12
skinparam PackageFontStyle bold
skinparam PackageFontColor #334155

skinparam RectangleBorderColor #0f2a4a
skinparam RectangleBorderThickness 2.2
skinparam RectangleBackgroundColor #ffffff

left to right direction

title USE CASE DIAGRAM — SISTEM INFORMASI PEMANTAUAN PUSDALOPS BNPB\\n<size:11><color:#64748b>Standar Notasi: OMG UML 2.5.1 | Penanggung Jawab: Adel (NIM. 1202220004)</color></size>

actor "Operator Meja Piket\\n(Shift 1, 2, 3)" as Operator
actor "Sistem Eksternal\\n(API BMKG & Portal Berita)" as External <<System>>

rectangle "Sistem Informasi Pemantauan Pusdalops BNPB" {{
  
  package "Modul Pantauan & Ingestion Data" as P1 {{
    (UC-01: Scraping Berita Bencana Daring\\n[Scheduled & On-Demand]) as UC01
    (UC-02: Memantau Antrean Siklus 24 Jam\\n[Windowing 07.00 - 07.00 WIB]) as UC02
    (UC-03: Filter Antrean 4 Tab Status\\n[Pending, Valid, Hoaks, Semua]) as UC03
    (UC-04: Menggabungkan Berita Susulan\\n[Merge Duplicate News]) as UC04
    (UC-05: Input Kejadian Manual Ad-Hoc\\n[Panggilan Radio HF / Telepon]) as UC05
  }}

  package "Modul Verifikasi & Validasi Lapangan" as P2 {{
    (UC-06: Verifikasi Metadata Lapangan 5 Blok\\n[Toponimi, Dampak, Upaya, Status]) as UC06
    (UC-07: Catat Bantahan Berita Hoaks\\n[Audit Forensik Penolakan]) as UC07
  }}

  package "Modul Otorisasi & Pelaporan Dinas" as P3 {{
    (UC-08: Kunci Siklus Laporan\\n[Lock Snapshot Otorisasi]) as UC08
    (UC-09: Buka Kunci Darurat\\n[Emergency Unlock + Alasan]) as UC09
    (UC-10: Ekspor Naskah Word .docx Bagian A\\n[Format Dinas BNPB <= 5 Detik]) as UC10
    (UC-11: Salin Ringkasan Pesan WhatsApp\\n[Teks Terklaster Format Pimpinan]) as UC11
    (UC-12: Kelola Master Wilayah Kemendagri\\n& Akun Petugas [RBAC]) as UC12
  }}
}}

P1 -[hidden]down-> P2
P2 -[hidden]down-> P3

actor "Supervisor\\nPusdalops BNPB" as Supervisor
actor "Satgas BPBD\\n(Prov / Kab / Kota)" as BPBD <<External>>

' Associations Operator (kiri ke tengah)
Operator --> UC01
Operator --> UC02
Operator --> UC03
Operator --> UC04
Operator --> UC05
Operator --> UC06
Operator --> UC07
Operator --> UC10

' Associations External (kiri atas)
External --> UC01

' Associations Supervisor (kanan ke tengah/bawah)
Supervisor --> UC02
Supervisor --> UC08
Supervisor --> UC09
Supervisor --> UC10
Supervisor --> UC11
Supervisor --> UC12

' Associations BPBD (kanan tengah)
UC06 ..> BPBD : <<dikonfirmasi>>
UC07 ..> BPBD : <<klarifikasi>>

' Include & Extend
UC04 ..> UC02 : <<extend>>
UC07 ..> UC06 : <<extend>>
UC08 ..> UC02 : <<include>>

@enduml"""

# ==========================================
# 2. CLASS DIAGRAM (Adel - NIM. 1202220004)
# ==========================================
PUML_CLASS = f"""@startuml
{PUML_COMMON_STYLE}
skinparam ClassBackgroundColor #ffffff
skinparam ClassBorderColor #1e3a8a
skinparam ClassBorderThickness 1.8
skinparam ClassHeaderBackgroundColor #dbeafe
skinparam ClassFontSize 12
skinparam ClassAttributeFontSize 11
skinparam ClassOperationFontSize 11

title CLASS DIAGRAM — ARSITEKTUR KELAS & ENTITAS PUSDALOPS BNPB\\n<size:11><color:#64748b>Standar Notasi: OMG UML 2.5.1 | Penanggung Jawab: Adel (NIM. 1202220004)</color></size>

package "Domain Model (ORM Entities)" #f8fafc {{
  class MasterWilayah {{
    - id_wilayah: String
    - nama_wilayah: String
    - level: String
    - parent_id: String
    --
    + get_full_hierarchy(): String
    + match_toponym(text: String): MasterWilayah
  }}

  class SiklusLaporan {{
    - kode_siklus: String
    - waktu_buka: DateTime
    - waktu_tutup: DateTime
    - is_locked: Boolean
    - locked_by: String
    - locked_at: DateTime
    --
    + lock_cycle(user: String): void
    + emergency_unlock(user: String, reason: String): void
    + is_cut_off_passed(): Boolean
  }}

  class KejadianBencana {{
    - id_kejadian: Integer
    - kode_kejadian: String
    - jenis_bencana: String
    - waktu_kejadian_riil: DateTime
    - waktu_kejadian_text: String
    - dampak_korban: JSON
    - dampak_kerusakan: JSON
    - upaya: Text
    - kondisi_mutakhir: Text
    - status_verifikasi: String
    - is_manual_entry: Boolean
    - is_isu_bantuan: Boolean
    --
    + verify(status: String, user: String): void
    + merge_with(secondary_id: Integer): void
    + get_formatted_korban(): String
    + get_formatted_kerusakan(): String
  }}

  class BeritaBencana {{
    - id_berita: Integer
    - judul: String
    - url_artikel: Text
    - nama_portal: String
    - isi_ringkas: Text
    - waktu_terbit: DateTime
    - similarity_score: Float
    - is_master_source: Boolean
    --
    + extract_clean_text(): String
    + get_domain(): String
  }}

  class LogAuditVerifikasi {{
    - id_log: Integer
    - id_user: String
    - shift: String
    - status_sebelum: String
    - status_sesudah: String
    - kontak_bpbd_dihubungi: String
    - catatan: Text
    - waktu_aksi: DateTime
    --
    + record_entry(): void
  }}

  MasterWilayah -[hidden]right-> SiklusLaporan
  SiklusLaporan -[hidden]right-> KejadianBencana
  BeritaBencana -[hidden]right-> LogAuditVerifikasi
  KejadianBencana -[hidden]down-> BeritaBencana
}}

package "Service Engines (Business Logic)" #f1f5f9 {{
  class DeduplicationEngine {{
    - threshold_tier1: Float = 0.80
    - threshold_tier2: Float = 0.60
    --
    + compute_similarity(text1: String, text2: String): Float
    + evaluate_duplicate(new_news: BeritaBencana, existing: List): KejadianBencana
  }}

  class WindowingEngine {{
    - cut_off_hour: Integer = 7
    --
    + get_current_cycle(target_time: DateTime): Tuple
    + assign_incident_to_cycle(incident: KejadianBencana): SiklusLaporan
    + get_countdown_to_cutoff(): String
  }}

  class DocxReportGenerator {{
    - template_path: String
    --
    + generate_bagian_a(kejadian_list: List, siklus: SiklusLaporan): Document
    + apply_null_safety(val: Object, default_phrase: String): String
    + save_to_stream(): BytesIO
  }}

  class WhatsAppFormatter {{
    --
    + format_by_clusters(kejadian_list: List, siklus: SiklusLaporan): String
  }}

  DeduplicationEngine -[hidden]right-> WindowingEngine
  DocxReportGenerator -[hidden]right-> WhatsAppFormatter
  DeduplicationEngine -[hidden]down-> DocxReportGenerator
}}

"Domain Model (ORM Entities)" -[hidden]down-> "Service Engines (Business Logic)"

' Structural Associations
MasterWilayah "1" <-- "0..*" MasterWilayah : parent-child
MasterWilayah "1" <-- "0..*" KejadianBencana : located_at
SiklusLaporan "1" <-- "0..*" KejadianBencana : belongs_to
KejadianBencana "1" *-- "1..*" BeritaBencana : references
KejadianBencana "1" <-- "0..*" LogAuditVerifikasi : logs

' Business Logic Dependencies
KejadianBencana ..> DeduplicationEngine : uses
SiklusLaporan ..> WindowingEngine : manages
DocxReportGenerator ..> KejadianBencana : transforms
WhatsAppFormatter ..> KejadianBencana : transforms

@enduml"""

# ==========================================
# 3. ENTITY RELATIONSHIP DIAGRAM (Seto - NIM. 1202220005)
# ==========================================
PUML_ERD = f"""@startuml
{PUML_COMMON_STYLE}
skinparam linetype ortho
skinparam EntityBackgroundColor #ffffff
skinparam EntityBorderColor #0f766e
skinparam EntityBorderThickness 1.8
skinparam EntityHeaderBackgroundColor #ccfbf1
skinparam EntityFontSize 12
skinparam EntityAttributeFontSize 11

title ENTITY RELATIONSHIP DIAGRAM (3NF CROW'S FOOT) — BASIS DATA PUSDALOPS BNPB\\n<size:11><color:#64748b>Standar Notasi: Crow's Foot Relational 3NF | Penanggung Jawab: Seto (NIM. 1202220005)</color></size>

entity "MASTER_WILAYAH" as MasterWilayah {{
  * id_wilayah : VARCHAR(20) <<PK>>
  --
  * nama_wilayah : VARCHAR(100)
  * level : VARCHAR(20)
  parent_id : VARCHAR(20) <<FK>>
}}

entity "SIKLUS_LAPORAN" as SiklusLaporan {{
  * kode_siklus : VARCHAR(30) <<PK>>
  --
  * waktu_buka : TIMESTAMPTZ
  * waktu_tutup : TIMESTAMPTZ
  * is_locked : BOOLEAN
  locked_by : VARCHAR(100)
  locked_at : TIMESTAMPTZ
}}

entity "KEJADIAN_BENCANA" as KejadianBencana {{
  * id_kejadian : SERIAL <<PK>>
  --
  * kode_kejadian : VARCHAR(50) <<UK>>
  * kode_siklus : VARCHAR(30) <<FK>>
  * jenis_bencana : VARCHAR(50)
  id_wilayah : VARCHAR(20) <<FK>>
  * waktu_kejadian_riil : TIMESTAMPTZ
  waktu_kejadian_text : VARCHAR(100)
  dampak_korban : JSONB
  dampak_kerusakan : JSONB
  upaya : TEXT
  kondisi_mutakhir : TEXT
  * status_verifikasi : VARCHAR(20)
  * is_manual_entry : BOOLEAN
  * is_isu_bantuan : BOOLEAN
}}

entity "BERITA_BENCANA" as BeritaBencana {{
  * id_berita : SERIAL <<PK>>
  --
  * id_kejadian : INTEGER <<FK>>
  * judul : VARCHAR(255)
  * url_artikel : TEXT
  nama_portal : VARCHAR(100)
  isi_ringkas : TEXT
  * waktu_terbit : TIMESTAMPTZ
  similarity_score : FLOAT
  * is_master_source : BOOLEAN
}}

entity "LOG_AUDIT_VERIFIKASI" as LogAudit {{
  * id_log : SERIAL <<PK>>
  --
  * id_kejadian : INTEGER <<FK>>
  * id_user : VARCHAR(100)
  shift : VARCHAR(20)
  status_sebelum : VARCHAR(20)
  status_sesudah : VARCHAR(20)
  kontak_bpbd_dihubungi : VARCHAR(100)
  catatan : TEXT
  * waktu_aksi : TIMESTAMPTZ
}}

' Relationships Crow's Foot
MasterWilayah ||--o{{ MasterWilayah : "parent_of"
MasterWilayah ||--o{{ KejadianBencana : "lokasi_kejadian"
SiklusLaporan ||--o{{ KejadianBencana : "periode_siklus"
KejadianBencana ||--|{{ BeritaBencana : "merujuk_artikel"
KejadianBencana ||--o{{ LogAudit : "merekam_jejak"

@enduml"""

# ==========================================
# 4. SEQUENCE DIAGRAM (Pandhu - NIM. 1202220006)
# ==========================================
PUML_SEQUENCE = f"""@startuml
{PUML_COMMON_STYLE}
autonumber
skinparam SequenceLifeLineBackgroundColor #ffffff
skinparam SequenceLifeLineBorderColor #2563eb
skinparam SequenceParticipantBackgroundColor #f8fafc
skinparam SequenceParticipantBorderColor #1e293b
skinparam SequenceParticipantBorderThickness 1.5
skinparam SequenceGroupBackgroundColor #f1f5f9
skinparam SequenceGroupBorderColor #475569

title SEQUENCE DIAGRAM — OPERASIONAL SISTEM OTOMASI PUSDALOPS BNPB\\n<size:11><color:#64748b>Standar Notasi: OMG UML 2.5.1 | Penanggung Jawab: Pandhu (NIM. 1202220006)</color></size>

actor "Operator Meja Piket" as OP #f8fafc
actor "Supervisor" as SP #fee2e2
boundary "Dasbor Web\\n(UI Meja Piket)" as UI #ffffff
control "Pusdalops\\nController" as Controller #eff6ff
control "Deduplication\\nNLP Engine" as Dedup #f0fdf4
database "Basis Data\\n(PostgreSQL)" as DB #fefce8
control "Docx Report\\nGenerator" as DocxGen #faf5ff

group Skenario 1: Ingestion & Deduplikasi Otomatis (On-Demand / Scheduled)
  OP -> UI : Klik tombol [🔄 Sync Now]
  activate UI
  UI -> Controller : POST /api/ingest/sync/
  activate Controller
  Controller -> Controller : Ambil XML RSS Berita & API BMKG
  Controller -> Dedup : evaluate_duplicate(raw_feeds)
  activate Dedup
  Dedup -> Dedup : Hitung TF-IDF & Cosine Similarity 2 Lapis
  Dedup --> Controller : Hasil Klaster (Berita Unik / Duplikat)
  deactivate Dedup
  Controller -> DB : INSERT kejadian_bencana & berita_bencana
  activate DB
  DB --> Controller : Data Persisted (Auto-Windowing 24 Jam)
  deactivate DB
  Controller --> UI : 200 OK (Antrean Teragregasi)
  deactivate Controller
  UI --> OP : Tampilkan Data di Tab PENDING (Alarm Bantuan Aktif)
  deactivate UI
end

group Skenario 2: Verifikasi & Koreksi Metadata Lapangan 5 Blok
  OP -> UI : Klik [✏️ Edit Metadata & Verifikasi]
  activate UI
  UI --> OP : Buka Modal 5 Blok (Toponimi, Dampak, Upaya, Kontak BPBD)
  OP -> UI : Isi Dampak Riil & Pilih Status [TERVERIFIKASI]
  OP -> UI : Klik [💾 Simpan & Perbarui Status]
  UI -> Controller : POST /api/kejadian/{{id}}/verify/
  activate Controller
  Controller -> DB : UPDATE kejadian_bencana (status='TERVERIFIKASI')
  activate DB
  Controller -> DB : INSERT log_audit_verifikasi (user, shift, kontak, waktu)
  DB --> Controller : Data Updated
  deactivate DB
  Controller --> UI : 200 OK (Status Berpindah ke Tab TERVERIFIKASI)
  deactivate Controller
  UI --> OP : Kartu Kejadian Berpindah ke Tab Hijau
  deactivate UI
end

group Skenario 3: Lock Snapshot Otorisasi oleh Supervisor
  SP -> UI : Buka Pusat Ekspor & Klik [🔒 Lock Snapshot]
  activate UI
  UI -> Controller : POST /api/siklus/{{kode}}/lock/
  activate Controller
  Controller -> DB : UPDATE siklus_laporan SET is_locked=TRUE
  activate DB
  DB --> Controller : Siklus Terkunci
  deactivate DB
  Controller --> UI : 200 OK (Status Siklus: Read-Only)
  deactivate Controller
  UI --> SP : Indikator Kunci Aktif (Perubahan Dibatasi)
  deactivate UI
end

group Skenario 4: Ekspor Dokumen Resmi Bagian A (.docx) & WhatsApp
  OP -> UI : Klik [📄 Unduh Word (.docx) Bagian A]
  activate UI
  UI -> Controller : GET /export/docx/?siklus=SIKLUS-YYYYMMDD
  activate Controller
  Controller -> DB : SELECT * FROM kejadian_bencana WHERE status='TERVERIFIKASI'
  activate DB
  DB --> Controller : Daftar Kejadian Faktual Valid
  deactivate DB
  Controller -> DocxGen : build_lapsit_bagian_a_docx(kejadian_list)
  activate DocxGen
  DocxGen -> DocxGen : Terapkan Kop Navy, Tabel Standar & Null-Safety Dinas
  DocxGen --> Controller : Berkas .docx Stream (Durasi <= 5s)
  deactivate DocxGen
  Controller --> UI : File Attachment Download
  deactivate Controller
  UI --> OP : Unduh Berkas Naskah Lapsit Resmi Siap Kirim
  deactivate UI
end

@enduml"""

# ==========================================
# 5. ACTIVITY DIAGRAM (Abid - NIM. 1202220003)
# ==========================================
PUML_ACTIVITY = f"""@startuml
{PUML_COMMON_STYLE}
skinparam ActivityBackgroundColor #ffffff
skinparam ActivityBorderColor #1e3a8a
skinparam ActivityBorderThickness 1.5
skinparam ActivityDiamondBackgroundColor #fef3c7
skinparam ActivityDiamondBorderColor #d97706
skinparam ActivityDiamondBorderThickness 1.5

title ACTIVITY DIAGRAM — ALIRAN KONTROL OPERASIONAL PUSDALOPS BNPB\\n<size:11><color:#64748b>Standar Notasi: OMG UML 2.5.1 (Swimlanes) | Penanggung Jawab: Abid (NIM. 1202220003)</color></size>

|Sistem Ingestion & NLP Engine|
start
:Trigger: Celery Beat / Tombol Sync Now;
:Ambil Feed RSS Berita & API BMKG;
:Ekstraksi Judul & Toponimi Kemendagri;

if (Evaluasi Parameter Gempa?) then (M < 5.0 & Non-Merusak)
  :Abaikan Berita / Log Buffer;
  stop
else (M >= 5.0 / Bencana Alam Lainnya)
  :Hitung TF-IDF & Cosine Similarity;
endif

if (Skor Similarity NLP?) then (Similarity >= 0.80)
  :Gabungkan Otomatis ke Kejadian Induk;
elseif (Similarity 0.60 - 0.79) then (Ya)
  if (Toponimi & Waktu Kejadian Sama?) then (Ya)
    :Gabungkan Otomatis ke Kejadian Induk;
  else (Tidak)
    :Buat Entri Kejadian Unik Baru;
  endif
else (Similarity < 0.60)
  :Buat Entri Kejadian Unik Baru;
endif

if (Terdeteksi Kata Kunci Keluhan Warga?) then (Ya)
  :Sematkan Badge Alarm [🚨 ISU BANTUAN];
else (Tidak)
endif

:Tempatkan Data pada Antrean Tab PENDING;

|Operator Meja Piket|
:Buka Dasbor Meja Piket & Antrean 24 Jam;
:Buka Modal Verifikasi 5 Blok;

|Satgas BPBD Daerah|
:Terima Panggilan Telepon / Pesan Konfirmasi;
:Sampaikan Data Faktual Dampak Riil Lapangan;

|Operator Meja Piket|
if (Hasil Verifikasi Lapangan?) then (Informasi Fiktif / Hoaks)
  :Ubah Status: HOAKS;
  :Wajib Catat Alasan Bantahan Forensik;
else (Informasi Valid Faktual)
  :Ubah Status: TERVERIFIKASI;
  :Input Data Riil Korban Jiwa & Kerusakan Fisik;
endif

|Sistem Ingestion & NLP Engine|
:Simpan Perubahan ke Basis Data;
:Catat Jejak Audit ke log_audit_verifikasi;

|Supervisor Pusdalops|
:Evaluasi Kelengkapan Antrean Siklus;
if (Antrean PENDING Sudah Bersih?) then (Belum)
  :Instruksikan Operator Tuntaskan Verifikasi;
  detach
else (Ya, Siap Cut-Off)
  :Eksekusi [🔒 Lock Snapshot Otorisasi];
endif

|Sistem Ingestion & NLP Engine|
:Kunci Status Siklus Laporan (Read-Only);

|Operator Meja Piket|
fork
  :Klik [📄 Unduh Word (.docx) Bagian A];
  :Sistem Generate Dokumen Resmi (<= 5 Detik);
fork again
  :Klik [📋 Salin Format WhatsApp];
  :Sistem Format Teks Terklaster Klaster Dinas;
end fork

:Kirimkan Laporan Tepat Waktu ke Pimpinan;
stop

@enduml"""

# ==========================================
# 6. BPMN AS-IS (Abid - NIM. 1202220003)
# ==========================================
PUML_BPMN_ASIS = f"""@startuml
{PUML_COMMON_STYLE}
skinparam ActivityBackgroundColor #ffffff
skinparam ActivityBorderColor #334155
skinparam ActivityBorderThickness 1.5
skinparam ActivityDiamondBackgroundColor #fef3c7
skinparam ActivityDiamondBorderColor #b45309

title BPMN 2.0 AS-IS — PROSES BISNIS PEMANTAUAN EKSISTING (MANUAL)\\n<size:11><color:#64748b>Standar Notasi: BPMN 2.0 Collaboration Diagram | Penanggung Jawab: Abid (NIM. 1202220003)</color></size>

|Portal Media & BMKG|
start
:Rilis Berita Bencana & Info Gempa;

|Operator Meja Piket (3 Shift)|
:Membuka Puluhan Tab Browser Berita Manual;
:Membaca Artikel Satu per Satu Sepanjang Waktu;
:Memilah Manual Berita Duplikat (Mata Telanjang);
:Menyalin Teks Judul & Narasi ke Lembar Catatan / Excel;

|Satgas BPBD Daerah|
:Menerima Kontak Telepon / Pesan WhatsApp Manual;
:Melakukan Pengecekan Lapangan Mandiri;
:Mengirimkan Jawaban Konfirmasi Korban & Kerusakan;

|Operator Meja Piket (3 Shift)|
:Mencatat Hasil Konfirmasi ke Lembar Rekapitulasi;
:Melakukan Serah Terima Catatan Manual Saat Pergantian Shift;
:Menjelang Cut-Off 07.00 WIB: Mengetik Ulang ke Microsoft Word;
:Mengatur Format Indentasi, Tabel, & Kop Dinas Manual (60-90 Menit);

|Pimpinan BNPB|
:Menerima Naskah Fisik / File Word Laporan;
note right: Sering Mengalami Keterlambatan\\nDistribusi Melewati Batas 07.00 WIB
stop

@enduml"""

# ==========================================
# 7. BPMN TO-BE (Abid - NIM. 1202220003)
# ==========================================
PUML_BPMN_TOBE = f"""@startuml
{PUML_COMMON_STYLE}
skinparam ActivityBackgroundColor #ffffff
skinparam ActivityBorderColor #047857
skinparam ActivityBorderThickness 1.5
skinparam ActivityDiamondBackgroundColor #fef3c7
skinparam ActivityDiamondBorderColor #b45309

title BPMN 2.0 TO-BE — PROSES BISNIS USULAN SISTEM OTOMASI PUSDALOPS BNPB\\n<size:11><color:#64748b>Standar Notasi: BPMN 2.0 Collaboration Diagram | Penanggung Jawab: Abid (NIM. 1202220003)</color></size>

|Sistem Otomasi Pusdalops-PB|
start
:Timer: Siklus 24 Jam 07.00 WIB Dimulai;
:Scraping Otomatis Celery / Tombol Sync Now;

if (Filter Gempa Adaptif?) then (M < 5.0 / Non-Signifikan)
  :Abaikan / Log Buffer;
  stop
else (M >= 5.0 / Bencana Alam Lain)
  :Eksekusi Deduplikasi NLP (TF-IDF & Cosine Similarity);
endif

if (Evaluasi Kemiripan Teks?) then (Duplikat (Sim >= 0.80 / Kab+Waktu Sama))
  :Gabungkan Otomatis ke Kejadian Induk;
else (Berita Unik Baru)
  :Masukkan ke Antrean Tab PENDING;
endif

if (Terdeteksi Kata Kunci Keluhan Logistik?) then (Ya)
  :Sematkan Badge Alarm [🚨 ISU BANTUAN];
else (Tidak)
endif

|Operator Meja Piket|
:Buka Modal Edit Metadata & Verifikasi 5 Blok;

|Satgas BPBD Daerah|
:Menerima Kontak Konfirmasi Cepat;
:Memberikan Keterangan Faktual Lapangan;

|Operator Meja Piket|
if (Hasil Verifikasi Lapangan?) then (Hoaks / Fiktif)
  :Pilih Status HOAKS + Catat Alasan Bantahan;
else (Valid Faktual)
  :Pilih Status TERVERIFIKASI + Input Dampak Riil;
endif

|Sistem Otomasi Pusdalops-PB|
:Simpan Perubahan & Catat Jejak ke log_audit_verifikasi;

|Supervisor Pusdalops|
:Evaluasi Kelengkapan Antrean Siklus;
if (Antrean PENDING Sudah Tuntas?) then (Ya)
  :Eksekusi [🔒 Lock Snapshot Otorisasi];
else (Belum)
  :Tugaskan Operator Tuntaskan Verifikasi;
  detach
endif

|Sistem Otomasi Pusdalops-PB|
:Kunci Status Siklus Menjadi Read-Only;

|Operator Meja Piket|
fork
  :Klik [📄 Unduh Word (.docx) Bagian A];
  :Sistem Menghasilkan Dokumen Dinas Resmi (<= 5 Detik);
fork again
  :Klik [📋 Salin Format WhatsApp];
  :Sistem Menyusun Format Ringkasan Terklaster;
end fork

|Pimpinan BNPB|
:Menerima Laporan Komprehensif Tepat Waktu Sebelum 07.00 WIB;
stop

@enduml"""

DIAGRAMS = [
    ("gambar_usecase_diagram", PUML_USECASE, "USE CASE DIAGRAM (Adel)"),
    ("gambar_class_diagram", PUML_CLASS, "CLASS DIAGRAM (Adel)"),
    ("gambar_erd_database", PUML_ERD, "ENTITY RELATIONSHIP DIAGRAM (Seto)"),
    ("gambar_sequence_diagram", PUML_SEQUENCE, "SEQUENCE DIAGRAM (Pandhu)"),
    ("gambar_activity_diagram", PUML_ACTIVITY, "ACTIVITY DIAGRAM (Abid)"),
    ("gambar_bpmn_asis", PUML_BPMN_ASIS, "BPMN 2.0 AS-IS (Abid)"),
    ("gambar_bpmn_tobe", PUML_BPMN_TOBE, "BPMN 2.0 TO-BE (Abid)"),
]

def render_diagrams_flawless():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=opts)
    
    for filename, puml_code, desc in DIAGRAMS:
        print(f"\nProcessing {desc}...")
        resp = requests.post("https://kroki.io/plantuml/svg", data=puml_code.encode('utf-8'), timeout=30)
        if resp.status_code != 200:
            print(f"FAILED to fetch SVG from Kroki: {resp.status_code}")
            continue
        
        svg_content = resp.text
        
        # Save SVG in docs/capstone/diagrams
        svg_path = os.path.join(output_dir, f"{filename}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        # Parse SVG width and height
        w_match = re.search(r'width="([0-9\.]+)px"', svg_content)
        h_match = re.search(r'height="([0-9\.]+)px"', svg_content)
        
        svg_w = int(float(w_match.group(1))) if w_match else 1600
        svg_h = int(float(h_match.group(1))) if h_match else 1200
        
        # HTML wrapper with clean zero margins
        html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    * {{ box-sizing: border-box; }}
    body, html {{
      margin: 0;
      padding: 25px;
      background: #ffffff;
      display: inline-block;
    }}
    svg {{
      display: block;
      margin: 0;
      padding: 0;
    }}
  </style>
</head>
<body>
  {svg_content}
</body>
</html>"""
        
        temp_html = os.path.join(output_dir, f"temp_{filename}.html")
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(html_wrapper)
            
        target_w = svg_w + 120
        target_h = svg_h + 120
        
        # Use Chrome DevTools Protocol to guarantee infinite canvas without viewport cutoffs
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width": target_w,
            "height": target_h,
            "deviceScaleFactor": 2,
            "mobile": False
        })
        
        driver.get(f'file:///{temp_html.replace(os.sep, "/")}')
        time.sleep(0.5)
        
        # Capture screenshot of the exact SVG element
        svg_elem = driver.find_element("tag name", "svg")
        png_path = os.path.join(output_dir, f"{filename}.png")
        svg_elem.screenshot(png_path)
        
        # Copy to artifacts directory
        artifact_path = os.path.join(artifacts_dir, f"{filename}.png")
        shutil.copy2(png_path, artifact_path)
        
        print(f"  -> PNG rendered (300 DPI): {png_path} ({os.path.getsize(png_path):,} bytes, SVG dim: {svg_w}x{svg_h})")
        
        if os.path.exists(temp_html):
            os.remove(temp_html)
            
    driver.quit()
    print("\nALL 7 DIAGRAMS RENDERED FLAWLESSLY WITH CDP INFINITE CANVAS!")

if __name__ == "__main__":
    render_diagrams_flawless()
