import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = os.path.join(os.path.dirname(__file__), 'docs', 'capstone', 'diagrams')
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'

# ==========================================
# 1. GAP ANALYSIS CHART
# ==========================================
def generate_gap_analysis_chart():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    categories = ['Waktu Rekap\nManual (Menit)', 'Waktu Ekspor\nLapsit (Menit)', 'Toleransi Berita\nDuplikat (%)', 'Waktu Verifikasi\nHoaks (Menit)']
    existing = [75, 45, 35, 30]
    target = [10, 0.1, 5, 5]
    x = range(len(categories))
    width = 0.35
    
    rects1 = ax.bar([i - width/2 for i in x], existing, width, label='Kondisi Manual Eksisting', color='#c0392b', alpha=0.85)
    rects2 = ax.bar([i + width/2 for i in x], target, width, label='Target Sistem Otomasi (Capstone)', color='#27ae60', alpha=0.85)
    
    ax.set_ylabel('Nilai Metrik', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.set_title('Perbandingan Kesenjangan Kinerja Operasional (Eksisting vs Target)', fontsize=13, fontweight='bold', pad=15, color='#2c3e50')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(frameon=True, facecolor='#f8f9fa')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h}', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#962d22')
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h}', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1e8449')
                    
    plt.tight_layout()
    chart_path = os.path.join(output_dir, 'gambar_1_1_gap_analisis.png')
    plt.savefig(chart_path)
    plt.close()
    print(f"Generated: {chart_path}")

# ==========================================
# 2. FISHBONE DIAGRAM
# ==========================================
def generate_fishbone_diagram():
    fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.annotate('', xy=(10.5, 4), xytext=(1.5, 4),
                arrowprops=dict(arrowstyle="->", lw=3.5, color="#1a252f"))

    box_problem = patches.FancyBboxPatch((10.5, 3.1), 2.2, 1.8, boxstyle="round,pad=0.2",
                                         facecolor='#c0392b', edgecolor='#962d22', lw=2)
    ax.add_patch(box_problem)
    ax.text(11.6, 4.0, "KETERLAMBATAN\n& RISIKO GALAT\nLAPSIT BENCANA\nPUSDALOPS",
            ha='center', va='center', color='white', fontsize=9.5, fontweight='bold')

    categories = [
        {"name": "MANUSIA (OPERATOR)", "x_top": 3.8, "y_top": 6.8, "x_bot": 3.0, "y_bot": 1.2,
         "causes_top": ["Kelelahan operator Shift 3 (Subuh)", "Beda gaya penulisan antar-piket"],
         "causes_bot": ["Beban konfirmasi telepon tinggi", "Keterbatasan personil meja piket"]},
        {"name": "METODE & PROSES", "x_top": 6.3, "y_top": 6.8, "x_bot": 5.5, "y_bot": 1.2,
         "causes_top": ["Rekapitulasi manual spreadsheet", "Cut-off 07.00 WIB tanpa reminder"],
         "causes_bot": ["Ketiadaan log audit bantahan hoaks", "Format tata naskah dinas rumit"]},
        {"name": "TEKNOLOGI (SISTEM)", "x_top": 8.8, "y_top": 6.8, "x_bot": 8.0, "y_bot": 1.2,
         "causes_top": ["Belum ada agregator multi-feed", "Ketiadaan deduplikasi NLP otomatis"],
         "causes_bot": ["Filter gempa BMKG belum adaptif", "Generator Word .docx belum ada"]}
    ]

    for cat in categories:
        x_top_base = cat["x_top"] - 0.8
        ax.plot([cat["x_top"], x_top_base], [cat["y_top"] - 0.5, 4], color='#2980b9', lw=2.5)
        box_top = patches.FancyBboxPatch((cat["x_top"] - 1.1, cat["y_top"] - 0.4), 2.2, 0.6,
                                         boxstyle="round,pad=0.1", facecolor='#2980b9', edgecolor='#1a5276', lw=1.5)
        ax.add_patch(box_top)
        ax.text(cat["x_top"], cat["y_top"] - 0.1, cat["name"], ha='center', va='center', color='white', fontsize=9, fontweight='bold')

        for i, cause in enumerate(cat["causes_top"]):
            y_sub = 5.8 - i * 0.9
            x_sub_start = x_top_base + (y_sub - 4) * (cat["x_top"] - x_top_base) / (cat["y_top"] - 0.5 - 4)
            ax.plot([x_sub_start - 1.3, x_sub_start], [y_sub, y_sub], color='#7f8c8d', lw=1.2, linestyle='--')
            ax.text(x_sub_start - 1.4, y_sub + 0.1, cause, ha='right', va='bottom', fontsize=8, color='#2c3e50')

        x_bot_base = cat["x_bot"] + 0.8
        ax.plot([cat["x_bot"], x_bot_base], [cat["y_bot"] + 0.5, 4], color='#d35400', lw=2.5)
        box_bot = patches.FancyBboxPatch((cat["x_bot"] - 1.1, cat["y_bot"] - 0.2), 2.2, 0.6,
                                         boxstyle="round,pad=0.1", facecolor='#d35400', edgecolor='#a04000', lw=1.5)
        ax.add_patch(box_bot)
        ax.text(cat["x_bot"], cat["y_bot"] + 0.1, cat["name"], ha='center', va='center', color='white', fontsize=9, fontweight='bold')

        for i, cause in enumerate(cat["causes_bot"]):
            y_sub = 2.2 + i * 0.9
            x_sub_start = x_bot_base + (y_sub - 4) * (cat["x_bot"] - x_bot_base) / (cat["y_bot"] + 0.5 - 4)
            ax.plot([x_sub_start - 1.3, x_sub_start], [y_sub, y_sub], color='#7f8c8d', lw=1.2, linestyle='--')
            ax.text(x_sub_start - 1.4, y_sub - 0.1, cause, ha='right', va='top', fontsize=8, color='#2c3e50')

    plt.tight_layout()
    fishbone_path = os.path.join(output_dir, 'gambar_1_2_fishbone_diagram.png')
    plt.savefig(fishbone_path)
    plt.close()
    print(f"Generated: {fishbone_path}")

# ==========================================
# 3. SISTEMATIKA PERANCANGAN (BAB 3)
# ==========================================
def generate_flowchart_perancangan():
    fig, ax = plt.subplots(figsize=(8, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    steps = [
        ("Mulai: Observasi Lapangan & Identifikasi Masalah Meja Piket Pusdalops", "#2c3e50"),
        ("Kajian Literatur & Body of Knowledge IS2020", "#34495e"),
        ("Perumusan Spesifikasi Kebutuhan & Batasan Realistis", "#2980b9"),
        ("Perancangan Arsitektur Sistem 4-Tier & Skema Basis Data ORM", "#16a085"),
        ("Pengembangan Windowing Engine 24 Jam & Pipeline Deduplikasi NLP", "#27ae60"),
        ("Implementasi Antarmuka Web Dasbor & Dual Output Generator", "#f39c12"),
        ("Verifikasi Fungsional (Blackbox) & Validasi Stakeholder BNPB", "#d35400"),
        ("Analisis Kelayakan Finansial (CBA, NPV, BEP) & Evaluasi", "#8e44ad"),
        ("Selesai: Penyusunan Laporan Akhir & Dokumentasi", "#2c3e50")
    ]

    y_start = 11.2
    box_w = 7.4
    box_h = 0.75
    gap = 0.5

    for i, (text, color) in enumerate(steps):
        y = y_start - i * (box_h + gap)
        box = patches.FancyBboxPatch((5 - box_w/2, y - box_h/2), box_w, box_h,
                                     boxstyle="round,pad=0.15", facecolor=color, edgecolor='#1a252f', lw=1.2)
        ax.add_patch(box)
        ax.text(5, y, f"Tahap {i+1}: {text}" if i not in [0, 8] else text,
                ha='center', va='center', color='white', fontsize=8.5, fontweight='bold')
        
        if i < len(steps) - 1:
            y_arrow_top = y - box_h/2
            y_arrow_bot = y - box_h/2 - gap
            ax.annotate('', xy=(5, y_arrow_bot), xytext=(5, y_arrow_top),
                        arrowprops=dict(arrowstyle="->", lw=2, color="#2c3e50"))

    plt.tight_layout()
    flowchart_path = os.path.join(output_dir, 'gambar_3_1_sistematika_perancangan.png')
    plt.savefig(flowchart_path)
    plt.close()
    print(f"Generated: {flowchart_path}")

# ==========================================
# 4. ARSITEKTUR SISTEM (BAB 4)
# ==========================================
def generate_arsitektur_sistem():
    fig, ax = plt.subplots(figsize=(11, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    tiers = [
        {"title": "TIER 1: EXTERNAL DATA SOURCES & FEEDS", "y": 8.5, "color": "#ebf5fb", "border": "#2980b9",
         "items": ["BMKG API (Autogempa & Real-time M>=5.0)", "RSS Media Daring (Detikcom, Kompas, Antara News)", "Portal Bencana Internasional (GDACS)"]},
        {"title": "TIER 2: INGESTION, WINDOWING & INTELLIGENCE LAYER", "y": 6.0, "color": "#e8f8f5", "border": "#16a085",
         "items": ["Celery Beat / On-Demand Sync", "Windowing 24 Jam (07.00 - 07.00 WIB)", "Penyaring Gempa Adaptif", "Deduplikasi 2 Lapis (NLP Cosine Similarity)"]},
        {"title": "TIER 3: STORAGE & AUDIT ORM LAYER", "y": 3.5, "color": "#fef9e7", "border": "#f39c12",
         "items": ["master_wilayah (Kemendagri)", "siklus_laporan (Lock/Unlock)", "kejadian_bencana (JSONField)", "berita_bencana (Multi-reference)", "log_audit_verifikasi"]},
        {"title": "TIER 4: PRESENTATION & DUAL OUTPUT LAYER", "y": 1.0, "color": "#f4ecf7", "border": "#8e44ad",
         "items": ["Dasbor Meja Piket 4 Tab", "Modal Verifikasi 5 Blok", "Modal Gabung (Merge)", "Generator Word (.docx) Bagian A", "Formatter Ringkasan WhatsApp"]}
    ]

    for t in tiers:
        box_tier = patches.FancyBboxPatch((0.8, t["y"] - 0.9), 10.4, 1.8, boxstyle="round,pad=0.2",
                                          facecolor=t["color"], edgecolor=t["border"], lw=2)
        ax.add_patch(box_tier)
        ax.text(1.2, t["y"] + 0.6, t["title"], ha='left', va='center', fontsize=10, fontweight='bold', color=t["border"])
        
        n_items = len(t["items"])
        w_item = 9.8 / n_items
        for idx, item in enumerate(t["items"]):
            x_pos = 1.1 + idx * w_item
            box_sub = patches.FancyBboxPatch((x_pos, t["y"] - 0.7), w_item - 0.2, 1.1,
                                             boxstyle="round,pad=0.1", facecolor='white', edgecolor=t["border"], lw=1)
            ax.add_patch(box_sub)
            ax.text(x_pos + (w_item - 0.2)/2, t["y"] - 0.15, item, ha='center', va='center',
                    fontsize=8, fontweight='bold', color='#2c3e50', wrap=True)

    for y_mid in [7.4, 4.9, 2.4]:
        ax.annotate('', xy=(6.0, y_mid - 0.4), xytext=(6.0, y_mid + 0.1),
                    arrowprops=dict(arrowstyle="<->", lw=2.5, color="#2c3e50"))

    plt.tight_layout()
    arch_path = os.path.join(output_dir, 'gambar_4_1_arsitektur_sistem.png')
    plt.savefig(arch_path)
    plt.close()
    print(f"Generated: {arch_path}")

# ==========================================
# 5. USE CASE DIAGRAM (ADEL)
# ==========================================
def generate_usecase_diagram():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Kotak Sistem Boundary
    rect_sys = patches.FancyBboxPatch((3.2, 0.4), 6.4, 9.2, boxstyle="round,pad=0.2",
                                      facecolor='#f8f9fa', edgecolor='#2c3e50', lw=2)
    ax.add_patch(rect_sys)
    ax.text(6.4, 9.3, "Sistem Otomasi Pemantauan Pusdalops BNPB", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#2c3e50')

    # Aktor Kiri: Operator Piket
    ax.text(1.5, 6.0, "👤\nOPERATOR MEJA PIKET", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#2980b9')
    # Aktor Kiri Bawah: Sistem Eksternal
    ax.text(1.5, 2.5, "🌐\nSISTEM EKSTERNAL\n(BMKG / RSS)", ha='center', va='center', fontsize=9, fontweight='bold', color='#7f8c8d')
    # Aktor Kanan: Supervisor Pusdalops
    ax.text(10.8, 6.0, "👤\nSUPERVISOR\nPUSDALOPS", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#c0392b')

    usecases = [
        ("UC-01: Tarik Feed Otomatis & On-Demand", 8.4, True, True, False),
        ("UC-02: Pantau Antrean Siklus 24 Jam", 7.5, True, False, True),
        ("UC-03: Filter 4 Tab Status Kejadian", 6.6, True, False, True),
        ("UC-04: Gabung Berita Susulan (Merge)", 5.7, True, False, False),
        ("UC-05: Tambah Kejadian Manual Ad-Hoc", 4.8, True, False, False),
        ("UC-06: Verifikasi Metadata 5 Blok", 3.9, True, False, False),
        ("UC-07: Catat Bantahan Hoaks & Audit Log", 3.0, True, False, False),
        ("UC-08: Kunci Siklus (Lock Snapshot)", 2.1, False, False, True),
        ("UC-09: Ekspor Word .docx & Format WA", 1.2, True, False, True),
    ]

    for uc_text, y, by_op, by_ext, by_sp in usecases:
        ellipse = patches.FancyBboxPatch((3.6, y - 0.32), 5.6, 0.64, boxstyle="round,pad=0.2",
                                         facecolor='#e8f8f5', edgecolor='#16a085', lw=1.2)
        ax.add_patch(ellipse)
        ax.text(6.4, y, uc_text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#16a085')

        if by_op:
            ax.plot([2.2, 3.6], [6.0, y], color='#2980b9', lw=1.2, linestyle='-')
        if by_ext:
            ax.plot([2.2, 3.6], [2.5, y], color='#7f8c8d', lw=1.2, linestyle='--')
        if by_sp:
            ax.plot([10.0, 9.2], [6.0, y], color='#c0392b', lw=1.2, linestyle='-')

    plt.tight_layout()
    uc_path = os.path.join(output_dir, 'gambar_usecase_diagram.png')
    plt.savefig(uc_path)
    plt.close()
    print(f"Generated: {uc_path}")

# ==========================================
# 6. ERD (SETO)
# ==========================================
def generate_erd_diagram():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    entities = [
        {"name": "SIKLUS_LAPORAN", "x": 1.0, "y": 7.0, "w": 3.0, "h": 2.2,
         "attrs": ["PK: kode_siklus (VARCHAR)", "waktu_buka (TIMESTAMPTZ)", "waktu_tutup (TIMESTAMPTZ)", "is_locked (BOOLEAN)", "locked_by (VARCHAR)"], "color": "#fef9e7", "border": "#f39c12"},
        {"name": "MASTER_WILAYAH", "x": 8.0, "y": 7.0, "w": 3.0, "h": 2.2,
         "attrs": ["PK: id_wilayah (VARCHAR)", "nama_wilayah (VARCHAR)", "level (ENUM)", "FK: parent_id (VARCHAR)"], "color": "#ebf5fb", "border": "#2980b9"},
        {"name": "KEJADIAN_BENCANA", "x": 4.5, "y": 3.5, "w": 3.5, "h": 3.2,
         "attrs": ["PK: id_kejadian (SERIAL)", "FK: kode_siklus", "FK: id_wilayah", "jenis_bencana (VARCHAR)", "dampak_korban (JSONField)", "dampak_kerusakan (JSONField)", "status_verifikasi (ENUM)", "is_isu_bantuan (BOOLEAN)"], "color": "#e8f8f5", "border": "#16a085"},
        {"name": "BERITA_BENCANA", "x": 1.0, "y": 0.5, "w": 3.0, "h": 2.4,
         "attrs": ["PK: id_berita (SERIAL)", "FK: id_kejadian", "judul (VARCHAR)", "url_artikel (TEXT)", "nama_portal (VARCHAR)", "similarity_score (FLOAT)"], "color": "#f4ecf7", "border": "#8e44ad"},
        {"name": "LOG_AUDIT_VERIFIKASI", "x": 8.0, "y": 0.5, "w": 3.0, "h": 2.4,
         "attrs": ["PK: id_log (SERIAL)", "FK: id_kejadian", "id_user (VARCHAR)", "shift (VARCHAR)", "status_sebelum/sesudah", "catatan (TEXT)", "waktu_aksi (TIMESTAMP)"], "color": "#fbeee6", "border": "#d35400"}
    ]

    for ent in entities:
        box = patches.FancyBboxPatch((ent["x"], ent["y"]), ent["w"], ent["h"], boxstyle="round,pad=0.1",
                                     facecolor=ent["color"], edgecolor=ent["border"], lw=2)
        ax.add_patch(box)
        header_h = 0.5
        box_hdr = patches.FancyBboxPatch((ent["x"], ent["y"] + ent["h"] - header_h), ent["w"], header_h,
                                         boxstyle="round,pad=0.05", facecolor=ent["border"], edgecolor=ent["border"], lw=1)
        ax.add_patch(box_hdr)
        ax.text(ent["x"] + ent["w"]/2, ent["y"] + ent["h"] - header_h/2, ent["name"],
                ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        
        y_text = ent["y"] + ent["h"] - header_h - 0.25
        for attr in ent["attrs"]:
            ax.text(ent["x"] + 0.15, y_text, attr, ha='left', va='center', fontsize=7.5, color='#2c3e50')
            y_text -= 0.28

    # Relasi Crow's foot connectors
    # Siklus -> Kejadian
    ax.annotate('1:N', xy=(4.5, 5.5), xytext=(4.0, 7.5),
                arrowprops=dict(arrowstyle="->", lw=2, color="#f39c12"))
    # Wilayah -> Kejadian
    ax.annotate('1:N', xy=(8.0, 5.5), xytext=(8.0, 7.5),
                arrowprops=dict(arrowstyle="->", lw=2, color="#2980b9"))
    # Kejadian -> Berita
    ax.annotate('1:N', xy=(2.5, 2.9), xytext=(4.5, 4.0),
                arrowprops=dict(arrowstyle="->", lw=2, color="#8e44ad"))
    # Kejadian -> Log Audit
    ax.annotate('1:N', xy=(9.5, 2.9), xytext=(8.0, 4.0),
                arrowprops=dict(arrowstyle="->", lw=2, color="#d35400"))

    plt.tight_layout()
    erd_path = os.path.join(output_dir, 'gambar_erd_database.png')
    plt.savefig(erd_path)
    plt.close()
    print(f"Generated: {erd_path}")

# ==========================================
# 7. BREAK EVEN POINT CHART (BAB 5)
# ==========================================
def generate_bep_chart():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    months = range(0, 13)
    cost_kumulatif = [45 + 2.5 * m for m in months]
    benefit_kumulatif = [0 + 8.5 * m for m in months]
    
    ax.plot(months, cost_kumulatif, label='Total Biaya Kumulatif (Investasi + OPEX)', color='#c0392b', lw=2.5, marker='o')
    ax.plot(months, benefit_kumulatif, label='Total Manfaat Kumulatif (Penghematan Man-Hour)', color='#27ae60', lw=2.5, marker='s')
    
    ax.scatter([7.5], [45 + 2.5 * 7.5], color='#f39c12', s=120, zorder=5, label='Titik Impas (BEP): Bulan ke-7.5')
    ax.axvline(x=7.5, color='#7f8c8d', linestyle='--', alpha=0.7)
    
    ax.set_xlabel('Bulan Operasional', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.set_ylabel('Nilai Kumulatif (Juta Rupiah)', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.set_title('Analisis Titik Impas (Break-Even Point) Sistem Otomasi BNPB', fontsize=13, fontweight='bold', pad=15, color='#2c3e50')
    ax.set_xticks(months)
    ax.legend(frameon=True, facecolor='#f8f9fa')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    bep_path = os.path.join(output_dir, 'gambar_5_1_analisis_kelayakan_bep.png')
    plt.savefig(bep_path)
    plt.close()
    print(f"Generated: {bep_path}")

if __name__ == '__main__':
    generate_gap_analysis_chart()
    generate_fishbone_diagram()
    generate_flowchart_perancangan()
    generate_arsitektur_sistem()
    generate_usecase_diagram()
    generate_erd_diagram()
    generate_bep_chart()
    print("All diagrams (including Use Case & ERD) generated successfully!")
