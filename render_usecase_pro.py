import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

output_dir = os.path.join(os.path.dirname(__file__), 'docs', 'capstone', 'diagrams')
os.makedirs(output_dir, exist_ok=True)

# 1. GENERATE PROFESSIONAL SVG USE CASE DIAGRAM (OMG UML 2.5.1 COMPLIANT)
svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 960" width="1400" height="960" style="background-color: #ffffff; font-family: 'Segoe UI', Arial, sans-serif;">
  <defs>
    <!-- Shadow Filter for Clean Modern Look -->
    <filter id="drop-shadow" x="-5%" y="-5%" width="115%" height="115%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <filter id="glow-badge" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#0284c7" flood-opacity="0.15"/>
    </filter>
    <!-- Arrow Markers -->
    <marker id="arrow-include" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7"/>
    </marker>
    <marker id="arrow-extend" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706"/>
    </marker>
  </defs>

  <!-- ================= HEADER BANNER ================= -->
  <text x="700" y="45" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f2a4a" letter-spacing="0.5">USE CASE DIAGRAM — SISTEM OTOMASI PEMANTAUAN KEBENCANAAN PUSDALOPS BNPB</text>
  <text x="700" y="70" text-anchor="middle" font-size="13" fill="#64748b">Standar Notasi: OMG UML 2.5.1 | Penanggung Jawab: Adel (S1 Sistem Informasi Telkom University)</text>

  <!-- ================= SYSTEM BOUNDARY ================= -->
  <!-- Outer Box -->
  <rect x="260" y="100" width="880" height="820" rx="14" ry="14" fill="#f8fafc" stroke="#334155" stroke-width="2.5" filter="url(#drop-shadow)"/>
  
  <!-- Boundary Header Tab -->
  <path d="M 260 114 Q 260 100 274 100 L 640 100 L 655 136 L 260 136 Z" fill="#1e293b"/>
  <text x="280" y="125" font-size="14" font-weight="bold" fill="#ffffff">Batas Sistem: Pusdalops-PB BNPB Web System</text>

  <!-- ================= USE CASES (ELLIPSES) ================= -->
  <!-- Column 1 (Left Column Inside Boundary, x=460) -->
  <!-- UC-01 -->
  <g id="uc-01">
    <ellipse cx="460" cy="180" rx="160" ry="32" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="460" y="176" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-01: Scraping Berita Daring</text>
    <text x="460" y="193" text-anchor="middle" font-size="11" fill="#64748b">(Scheduled &amp; On-Demand)</text>
  </g>

  <!-- UC-02 -->
  <g id="uc-02">
    <ellipse cx="460" cy="275" rx="165" ry="32" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="460" y="271" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-02: Memantau Antrean Siklus</text>
    <text x="460" y="288" text-anchor="middle" font-size="11" fill="#64748b">(Windowing 24 Jam 07.00 WIB)</text>
  </g>

  <!-- UC-03 -->
  <g id="uc-03">
    <ellipse cx="460" cy="370" rx="160" ry="32" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="460" y="366" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-03: Filter 4 Tab Status</text>
    <text x="460" y="383" text-anchor="middle" font-size="11" fill="#64748b">(Pending, Valid, Hoaks, Semua)</text>
  </g>

  <!-- UC-04 -->
  <g id="uc-04">
    <ellipse cx="460" cy="465" rx="160" ry="32" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="460" y="461" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-04: Gabung Berita Susulan</text>
    <text x="460" y="478" text-anchor="middle" font-size="11" fill="#64748b">(Merge Duplicates)</text>
  </g>

  <!-- UC-05 -->
  <g id="uc-05">
    <ellipse cx="460" cy="560" rx="160" ry="32" fill="#ffffff" stroke="#2563eb" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="460" y="556" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-05: Input Kejadian Manual</text>
    <text x="460" y="573" text-anchor="middle" font-size="11" fill="#64748b">(Panggilan Telepon / Radio HF)</text>
  </g>

  <!-- Column 2 (Right Column Inside Boundary, x=940) -->
  <!-- UC-06 -->
  <g id="uc-06">
    <ellipse cx="940" cy="180" rx="160" ry="32" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="940" y="176" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-06: Verifikasi Metadata 5 Blok</text>
    <text x="940" y="193" text-anchor="middle" font-size="11" fill="#64748b">(Toponimi, Dampak, Upaya, Status)</text>
  </g>

  <!-- UC-07 -->
  <g id="uc-07">
    <ellipse cx="940" cy="275" rx="160" ry="32" fill="#ffffff" stroke="#059669" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="940" y="271" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-07: Catat Bantahan Berita Hoaks</text>
    <text x="940" y="288" text-anchor="middle" font-size="11" fill="#64748b">(Audit Forensik Penolakan)</text>
  </g>

  <!-- UC-08 -->
  <g id="uc-08">
    <ellipse cx="940" cy="370" rx="160" ry="32" fill="#ffffff" stroke="#dc2626" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="940" y="366" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-08: Kunci Siklus Laporan</text>
    <text x="940" y="383" text-anchor="middle" font-size="11" fill="#64748b">(Lock Snapshot Otorisasi)</text>
  </g>

  <!-- UC-09 -->
  <g id="uc-09">
    <ellipse cx="940" cy="465" rx="160" ry="32" fill="#ffffff" stroke="#dc2626" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="940" y="461" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-09: Buka Kunci Darurat</text>
    <text x="940" y="478" text-anchor="middle" font-size="11" fill="#64748b">(Emergency Unlock + Log Alasan)</text>
  </g>

  <!-- UC-10 -->
  <g id="uc-10">
    <ellipse cx="940" cy="560" rx="160" ry="32" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="940" y="556" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-10: Ekspor Word (.docx) Bagian A</text>
    <text x="940" y="573" text-anchor="middle" font-size="11" fill="#64748b">(Format Dinas BNPB &lt;= 5 Detik)</text>
  </g>

  <!-- UC-11 (Center-Right x=850, y=665) -->
  <g id="uc-11">
    <ellipse cx="850" cy="665" rx="160" ry="32" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="850" y="661" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-11: Salin Ringkasan WhatsApp</text>
    <text x="850" y="678" text-anchor="middle" font-size="11" fill="#64748b">(Teks Terklaster Format Pimpinan)</text>
  </g>

  <!-- UC-12 (Center-Left x=550, y=780) -->
  <g id="uc-12">
    <ellipse cx="550" cy="780" rx="165" ry="32" fill="#ffffff" stroke="#475569" stroke-width="2" filter="url(#drop-shadow)"/>
    <text x="550" y="776" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#1e293b">UC-12: Kelola Master Wilayah</text>
    <text x="550" y="793" text-anchor="middle" font-size="11" fill="#64748b">(Sinkronisasi Kepmendagri &amp; Akun)</text>
  </g>

  <!-- ================= RELATIONSHIPS (INCLUDE & EXTEND) ================= -->
  <!-- UC-04 extend UC-02 -->
  <path d="M 460 433 L 460 307" stroke="#d97706" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#arrow-extend)"/>
  <rect x="420" y="358" width="80" height="20" rx="4" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
  <text x="460" y="372" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#b45309">&lt;&lt;extend&gt;&gt;</text>

  <!-- UC-07 extend UC-06 -->
  <path d="M 940 243 L 940 212" stroke="#d97706" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#arrow-extend)"/>
  <rect x="900" y="217" width="80" height="18" rx="4" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
  <text x="940" y="230" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#b45309">&lt;&lt;extend&gt;&gt;</text>

  <!-- UC-08 include UC-02 -->
  <path d="M 800 355 L 610 295" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#arrow-include)"/>
  <rect x="670" y="315" width="84" height="20" rx="4" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1"/>
  <text x="712" y="329" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0369a1">&lt;&lt;include&gt;&gt;</text>

  <!-- ================= ACTOR 1: OPERATOR MEJA PIKET (LEFT) ================= -->
  <g id="actor-operator" transform="translate(110, 320)">
    <!-- Stickman Vector -->
    <circle cx="25" cy="20" r="14" fill="#ffffff" stroke="#1e293b" stroke-width="3"/>
    <line x1="25" y1="34" x2="25" y2="75" stroke="#1e293b" stroke-width="3"/>
    <line x1="0" y1="50" x2="50" y2="50" stroke="#1e293b" stroke-width="3"/>
    <line x1="25" y1="75" x2="8" y2="115" stroke="#1e293b" stroke-width="3"/>
    <line x1="25" y1="75" x2="42" y2="115" stroke="#1e293b" stroke-width="3"/>
    <!-- Label -->
    <text x="25" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">Operator Meja Piket</text>
    <text x="25" y="156" text-anchor="middle" font-size="11" fill="#64748b">(Shift 1, 2, 3)</text>
  </g>

  <!-- Lines from Operator to Use Cases -->
  <line x1="160" y1="350" x2="310" y2="185" stroke="#475569" stroke-width="1.8"/>
  <line x1="160" y1="365" x2="295" y2="275" stroke="#475569" stroke-width="1.8"/>
  <line x1="160" y1="375" x2="300" y2="370" stroke="#475569" stroke-width="1.8"/>
  <line x1="160" y1="385" x2="300" y2="465" stroke="#475569" stroke-width="1.8"/>
  <line x1="160" y1="395" x2="305" y2="555" stroke="#475569" stroke-width="1.8"/>
  <line x1="160" y1="360" x2="780" y2="185" stroke="#475569" stroke-width="1.5" stroke-dasharray="2,2"/>
  <line x1="160" y1="410" x2="780" y2="560" stroke="#475569" stroke-width="1.5" stroke-dasharray="2,2"/>
  <line x1="160" y1="420" x2="695" y2="660" stroke="#475569" stroke-width="1.5" stroke-dasharray="2,2"/>

  <!-- ================= ACTOR 2: SISTEM EKSTERNAL (LEFT BOTTOM) ================= -->
  <g id="actor-external" transform="translate(70, 710)">
    <!-- System Component Box -->
    <rect x="0" y="0" width="120" height="65" rx="6" fill="#ffffff" stroke="#0369a1" stroke-width="2.5"/>
    <text x="60" y="24" text-anchor="middle" font-size="11" font-weight="bold" fill="#0284c7">&lt;&lt;system&gt;&gt;</text>
    <text x="60" y="42" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">API BMKG &amp;</text>
    <text x="60" y="56" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0f172a">Portal Berita</text>
  </g>
  <line x1="190" y1="740" x2="330" y2="200" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="4,3"/>

  <!-- ================= ACTOR 3: SUPERVISOR PUSDALOPS (RIGHT) ================= -->
  <g id="actor-supervisor" transform="translate(1220, 320)">
    <!-- Stickman Vector -->
    <circle cx="25" cy="20" r="14" fill="#ffffff" stroke="#b91c1c" stroke-width="3"/>
    <line x1="25" y1="34" x2="25" y2="75" stroke="#b91c1c" stroke-width="3"/>
    <line x1="0" y1="50" x2="50" y2="50" stroke="#b91c1c" stroke-width="3"/>
    <line x1="25" y1="75" x2="8" y2="115" stroke="#b91c1c" stroke-width="3"/>
    <line x1="25" y1="75" x2="42" y2="115" stroke="#b91c1c" stroke-width="3"/>
    <!-- Label -->
    <text x="25" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#7f1d1d">Supervisor</text>
    <text x="25" y="156" text-anchor="middle" font-size="11" fill="#64748b">Pusdalops BNPB</text>
  </g>

  <!-- Lines from Supervisor to Use Cases -->
  <line x1="1220" y1="355" x2="1100" y2="370" stroke="#b91c1c" stroke-width="2"/>
  <line x1="1220" y1="375" x2="1100" y2="465" stroke="#b91c1c" stroke-width="2"/>
  <line x1="1220" y1="390" x2="1100" y2="560" stroke="#b91c1c" stroke-width="2"/>
  <line x1="1220" y1="410" x2="1010" y2="660" stroke="#b91c1c" stroke-width="2"/>
  <line x1="1220" y1="430" x2="715" y2="775" stroke="#b91c1c" stroke-width="2"/>

  <!-- ================= ACTOR 4: SATGAS BPBD DAERAH (RIGHT BOTTOM) ================= -->
  <g id="actor-bpbd" transform="translate(1220, 680)">
    <!-- Stickman Vector -->
    <circle cx="25" cy="20" r="14" fill="#ffffff" stroke="#047857" stroke-width="2.5"/>
    <line x1="25" y1="34" x2="25" y2="75" stroke="#047857" stroke-width="2.5"/>
    <line x1="0" y1="50" x2="50" y2="50" stroke="#047857" stroke-width="2.5"/>
    <line x1="25" y1="75" x2="8" y2="115" stroke="#047857" stroke-width="2.5"/>
    <line x1="25" y1="75" x2="42" y2="115" stroke="#047857" stroke-width="2.5"/>
    <!-- Label -->
    <text x="25" y="140" text-anchor="middle" font-size="12" font-weight="bold" fill="#065f46">Satgas BPBD</text>
    <text x="25" y="156" text-anchor="middle" font-size="10.5" fill="#64748b">(Provinsi / Kab / Kota)</text>
  </g>
  <!-- Interaction to UC-06 and UC-07 via Telephone Confirmation -->
  <line x1="1220" y1="710" x2="1080" y2="200" stroke="#059669" stroke-width="1.5" stroke-dasharray="3,3"/>
  <line x1="1220" y1="730" x2="1085" y2="285" stroke="#059669" stroke-width="1.5" stroke-dasharray="3,3"/>

</svg>
"""

svg_file = os.path.join(output_dir, 'usecase_diagram_pro.svg')
with open(svg_file, 'w', encoding='utf-8') as f:
    f.write(svg_content)
print(f"SVG saved: {svg_file}")

# 2. RENDER SVG TO HIGH RESOLUTION PNG VIA HEADLESS CHROME (SELENIUM)
html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body, html {{ margin: 0; padding: 0; background: #ffffff; display: flex; justify-content: center; align-items: center; }}
    svg {{ display: block; }}
  </style>
</head>
<body>
  {svg_content}
</body>
</html>
"""

html_file = os.path.join(output_dir, 'temp_usecase.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_wrapper)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=2800,1920')
options.add_argument('--force-device-scale-factor=2') # 2x DPI Rendering

driver = webdriver.Chrome(options=options)
driver.get(f'file:///{html_file.replace(os.sep, "/")}')
time.sleep(1) # Allow SVG DOM to render

png_file = os.path.join(output_dir, 'gambar_usecase_diagram.png')
driver.save_screenshot(png_file)
driver.quit()

if os.path.exists(html_file):
    os.remove(html_file)

print(f"High-Res PNG saved: {png_file} (Size: {os.path.getsize(png_file)} bytes)")
