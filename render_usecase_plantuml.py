import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

output_dir = os.path.join(os.path.dirname(__file__), 'docs', 'capstone', 'diagrams')
os.makedirs(output_dir, exist_ok=True)

# PlantUML 2-Package Clean Architecture Layout
puml_code = """@startuml
skinparam BackgroundColor #ffffff
skinparam Shadowing true
skinparam DefaultFontName "Segoe UI"
skinparam DefaultFontSize 12
skinparam DefaultFontColor #1e293b

skinparam ActorBackgroundColor #f8fafc
skinparam ActorBorderColor #0f172a
skinparam ActorFontColor #0f172a
skinparam ActorFontSize 13
skinparam ActorFontStyle bold

skinparam UsecaseBackgroundColor #ffffff
skinparam UsecaseBorderColor #2563eb
skinparam UsecaseBorderThickness 1.5
skinparam UsecaseFontColor #0f172a
skinparam UsecaseFontSize 12
skinparam UsecaseFontStyle bold

skinparam PackageBorderColor #64748b
skinparam PackageBorderThickness 1
skinparam PackageBackgroundColor #f1f5f9
skinparam PackageFontSize 11
skinparam PackageFontStyle italic
skinparam PackageFontColor #475569

skinparam RectangleBorderColor #1e293b
skinparam RectangleBorderThickness 2
skinparam RectangleBackgroundColor #ffffff

skinparam ArrowColor #334155
skinparam ArrowThickness 1.5

left to right direction

actor "Operator Meja Piket\\n(Shift 1, 2, 3)" as Operator
actor "Sistem Eksternal\\n(API BMKG & Portal Berita)" as External <<System>>

rectangle "Sistem Informasi Pemantauan Pusdalops BNPB" {
  
  package "Modul Pantauan & Ingestion Data" {
    usecase "UC-01: Scraping Berita Daring\\n(Scheduled & On-Demand)" as UC01
    usecase "UC-02: Memantau Antrean Siklus 24 Jam\\n(Windowing 07.00 - 07.00 WIB)" as UC02
    usecase "UC-03: Filter Antrean 4 Tab Status\\n(Pending, Valid, Hoaks, Semua)" as UC03
    usecase "UC-04: Menggabungkan Berita Susulan\\n(Merge Duplicate News)" as UC04
    usecase "UC-05: Input Kejadian Manual Ad-Hoc\\n(Panggilan Radio HF / Telepon)" as UC05
  }

  package "Modul Verifikasi & Validasi Lapangan" {
    usecase "UC-06: Verifikasi Metadata Lapangan 5 Blok\\n(Toponimi, Dampak, Upaya, Status)" as UC06
    usecase "UC-07: Catat Bantahan Berita Hoaks\\n(Audit Forensik Penolakan)" as UC07
  }

  package "Modul Otorisasi & Pelaporan Dinas" {
    usecase "UC-08: Kunci Siklus Laporan\\n(Lock Snapshot Otorisasi)" as UC08
    usecase "UC-09: Buka Kunci Darurat\\n(Emergency Unlock + Alasan)" as UC09
    usecase "UC-10: Ekspor Naskah Word (.docx) Bagian A\\n(Format Dinas BNPB <= 5 Detik)" as UC10
    usecase "UC-11: Salin Ringkasan WhatsApp\\n(Teks Terklaster Format Pimpinan)" as UC11
    usecase "UC-12: Kelola Master Wilayah Kemendagri\\n& Akun Petugas (RBAC)" as UC12
  }
}

actor "Supervisor\\nPusdalops BNPB" as Supervisor
actor "Satgas BPBD\\n(Prov / Kab / Kota)" as BPBD <<External>>

' Hubungan Operator
External --> UC01
Operator --> UC01
Operator --> UC02
Operator --> UC03
Operator --> UC04
Operator --> UC05
Operator --> UC06

' Hubungan Konfirmasi Daerah
UC06 ..> BPBD : <<dikonfirmasi>>
UC07 ..> BPBD : <<klarifikasi>>

' Hubungan Supervisor
Supervisor --> UC08
Supervisor --> UC09
Supervisor --> UC10
Supervisor --> UC11
Supervisor --> UC12

' Hubungan Bersama Ekspor
Operator --> UC10
Operator --> UC11

' Hubungan Include & Extend
UC04 .> UC02 : <<extend>>
UC07 .> UC06 : <<extend>>
UC08 .> UC02 : <<include>>

@enduml"""

resp = requests.post("https://kroki.io/plantuml/svg", data=puml_code.encode('utf-8'))
if resp.status_code != 200:
    raise Exception(f"Gagal generate SVG: {resp.status_code}")

svg_content = resp.text

html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body, html {{ margin: 0; padding: 25px; background: #ffffff; display: inline-block; }}
    svg {{ display: block; }}
  </style>
</head>
<body>
  {svg_content}
</body>
</html>
"""

html_file = os.path.join(output_dir, 'temp_puml2.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_wrapper)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--force-device-scale-factor=2')

driver = webdriver.Chrome(options=options)
driver.get(f'file:///{html_file.replace(os.sep, "/")}')

body = driver.find_element("tag name", "body")
w = body.size['width'] + 60
h = body.size['height'] + 60
driver.set_window_size(w, h)

png_file = os.path.join(output_dir, 'gambar_usecase_diagram.png')
body.screenshot(png_file)
driver.quit()

if os.path.exists(html_file):
    os.remove(html_file)

print(f"Updated Use Case Diagram saved to: {png_file}")
