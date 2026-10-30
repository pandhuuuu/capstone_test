# pipeline_demo.py
"""
Demonstrasi Alur Lengkap Sistem Informasi Pusdalops BNPB (Hulu ke Hilir):
1. Ingestion (RSS Google News + BMKG API)
2. Analytics (TF-IDF Deduplikasi, Validasi Kemendagri, Deteksi Isu Bantuan)
3. Hilir (Generator Dokumen Resmi BNPB Bagian A .docx)
"""
import os
import sys
import datetime

# Pastikan UTF-8 support di Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Pastikan path modul terdeteksi
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from apps.ingestion.adapters import GoogleNewsAdapter, BMKGAdapter
from apps.analytics.deduplication import DeduplicationEngine
from apps.analytics.kemendagri_matcher import KemendagriMatcher
from apps.analytics.issue_tagger import detect_aid_issue

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def run_pipeline():
    print("=" * 65)
    print(">> MENJALANKAN PIPELINE LENGKAP SISTEM INFORMASI PUSDALOPS BNPB")
    print("=" * 65)

    # 1. INGESTION
    print("\n[LANGKAH 1] MENARIK DATA SUMBER TERBUKA (INGESTION)...")
    gn_adapter = GoogleNewsAdapter()
    bmkg_adapter = BMKGAdapter()

    raw_articles = []
    
    # Ambil data BMKG
    bmkg_data = bmkg_adapter.fetch_latest()
    print(f"  [OK] Data BMKG diperoleh: {len(bmkg_data)} entri")
    raw_articles.extend(bmkg_data)

    # Ambil data Google News
    news_data = gn_adapter.fetch_latest()
    print(f"  [OK] Berita Media Daring diperoleh: {len(news_data)} entri")
    raw_articles.extend(news_data)

    print(f"  Total Data Mentah Terkumpul: {len(raw_articles)} artikel/peringatan.")

    # 2. DEDUPLIKASI (ANALYTICS)
    print("\n[LANGKAH 2] DEDUPLIKASI & CLUSTERING BERITA KEMBAR...")
    dedup = DeduplicationEngine(threshold=0.45) # Ambang klastering
    clusters = dedup.cluster_articles(raw_articles)
    print(f"  [OK] Dari {len(raw_articles)} artikel mentah, berhasil dikelompokkan menjadi:")
    print(f"       -> {len(clusters)} Kejadian Unik!")

    # 3. KEMENDAGRI GEOTAGGING & ISSUE CLASSIFICATION
    print("\n[LANGKAH 3] VALIDASI WILAYAH KEMENDAGRI & PENANDAAN ISU BANTUAN...")
    matcher = KemendagriMatcher()

    verified_events = []
    for idx, c in enumerate(clusters, 1):
        lead = c["lead_article"]
        text_corpus = f"{lead['title']} {lead['summary']}"

        # Pencocokan hierarki wilayah
        geo = matcher.match_hierarchy_from_text(text_corpus)
        if geo:
            lokasi_str = f"{geo.get('kecamatan') or '-'}, {geo.get('kab_kota') or '-'}, Prov. {geo.get('provinsi') or '-'}"
        else:
            lokasi_str = "Lokasi dalam verifikasi petugas"

        # Deteksi isu keluhan bantuan
        issue = detect_aid_issue(text_corpus)

        # Sumber-sumber yang meliput
        all_sources = list(set([a["source_name"] for a in c["all_articles"]]))
        sumber_str = ", ".join(all_sources)

        event_entry = {
            "no": str(idx),
            "title": lead["title"],
            "waktu": lead.get("published_at", "Dalam konfirmasi"),
            "lokasi": lokasi_str,
            "kronologi": lead["summary"][:250] + ("..." if len(lead["summary"]) > 250 else ""),
            "korban": "• Dalam proses pendataan oleh BPBD setempat.",
            "kerusakan": "• Belum ada laporan kerusakan signifikan / Masih asesmen.",
            "upaya": "• TRC BPBD menuju lokasi kejadian untuk kaji cepat dan evakuasi.",
            "kondisi": "• Petugas piket Pusdalops memantau perkembangan situasi.",
            "sumber": sumber_str,
            "total_berita": len(c["all_articles"]),
            "flag_isu": issue["label"]
        }
        verified_events.append(event_entry)

    # 4. HILIR - GENERATOR LAPORAN WORD .DOCX (BAGIAN A)
    print("\n[LANGKAH 4] PEMBENTUKAN DOKUMEN RESMI BAGIAN A (.DOCX)...")
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Kop Surat Resmi
    p_kop = doc.add_paragraph()
    r_kop = p_kop.add_run("BADAN NASIONAL PENANGGULANGAN BENCANA\nPUSAT PENGENDALIAN OPERASI (PUSDALOPS PB)")
    r_kop.font.name = "Arial"
    r_kop.font.size = Pt(13)
    r_kop.font.bold = True
    r_kop.font.color.rgb = RGBColor(0, 32, 96)
    p_kop.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc.add_paragraph()
    today_str = datetime.datetime.now().strftime("%d %B %Y").upper()
    r_sub = p_sub.add_run(f"LAPORAN HARIAN SITUASI BENCANA\nPERIODE: {today_str}")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sec = doc.add_paragraph()
    r_sec = p_sec.add_run("BAGIAN A. RINCIAN KEJADIAN BENCANA")
    r_sec.font.name = "Arial"
    r_sec.font.size = Pt(11)
    r_sec.font.bold = True

    # Batasi cetak 10 kejadian teratas untuk demo
    for ev in verified_events[:10]:
        p_ev_t = doc.add_paragraph()
        r_ev_t = p_ev_t.add_run(f"{ev['no']}. {ev['title'].upper()}")
        r_ev_t.font.name = "Arial"
        r_ev_t.font.size = Pt(10)
        r_ev_t.font.bold = True

        attrs = [
            ("Waktu Kejadian", ev["waktu"]),
            ("Lokasi", ev["lokasi"]),
            ("Kronologi", ev["kronologi"]),
            ("Korban Jiwa & Terdampak", ev["korban"]),
            ("Kerusakan Materil", ev["kerusakan"]),
            ("Upaya Penanganan", ev["upaya"]),
            ("Kondisi Mutakhir", ev["kondisi"]),
            ("Status / Isu", ev["flag_isu"]),
            ("Sumber Rujukan Terintegrasi", f"{ev['sumber']} (Diliput {ev['total_berita']} sumber)"),
        ]

        for label, val in attrs:
            p_line = doc.add_paragraph()
            p_line.paragraph_format.left_indent = Inches(0.25)
            p_line.paragraph_format.space_after = Pt(2)
            
            r_label = p_line.add_run(f"➢ {label}: ")
            r_label.font.name = "Arial"
            r_label.font.size = Pt(9.5)
            r_label.font.bold = True

            r_val = p_line.add_run(val)
            r_val.font.name = "Arial"
            r_val.font.size = Pt(9.5)

    output_file = "Laporan_Harian_Pusdalops_BNPB_Bagian_A.docx"
    doc.save(output_file)
    
    print(f"\n[SUKSES] Dokumen Laporan Harian BNPB berhasil dibuat:")
    print(f"   -> File: {os.path.abspath(output_file)}")
    print(f"   -> Selesai dalam hitungan detik!")
    print("=" * 65)

if __name__ == "__main__":
    run_pipeline()
