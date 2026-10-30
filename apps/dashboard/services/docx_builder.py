# apps/dashboard/services/docx_builder.py
import io
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def build_sitrep_docx(verified_events, current_cycle) -> io.BytesIO:
    """
    Menghasilkan dokumen resmi Microsoft Word (.docx) format SITREP Bagian A Pusdalops BNPB.
    Mengembalikan: io.BytesIO buffer siap unduh atau disimpan.
    """
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Kop Pusdalops BNPB
    p_kop = doc.add_paragraph()
    r_kop = p_kop.add_run("BADAN NASIONAL PENANGGULANGAN BENCANA\nPUSAT PENGENDALIAN OPERASI (PUSDALOPS PB)")
    r_kop.font.name = "Arial"
    r_kop.font.size = Pt(13)
    r_kop.font.bold = True
    r_kop.font.color.rgb = RGBColor(0, 32, 96)
    p_kop.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run(f"LAPORAN HARIAN SITUASI BENCANA\nPERIODE: {current_cycle.range_display.upper()}")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sec = doc.add_paragraph()
    r_sec = p_sec.add_run("BAGIAN A. RINCIAN KEJADIAN BENCANA")
    r_sec.font.name = "Arial"
    r_sec.font.size = Pt(11)
    r_sec.font.bold = True

    if not verified_events.exists():
        p_empty = doc.add_paragraph()
        r_empty = p_empty.add_run("(Tidak ada kejadian bencana berstatus TERVERIFIKASI RESMI untuk periode siklus ini)")
        r_empty.font.name = "Arial"
        r_empty.font.italic = True
    else:
        for idx, ev in enumerate(verified_events, 1):
            lead = ev.lead_article
            title = lead.judul if lead else f"Kejadian {ev.jenis_bencana}"
            p_ev_t = doc.add_paragraph()
            r_ev_t = p_ev_t.add_run(f"{idx}. {title.upper()}")
            r_ev_t.font.name = "Arial"
            r_ev_t.font.size = Pt(10)
            r_ev_t.font.bold = True

            sources = [b.nama_portal for b in ev.berita_list.all()]
            sources_str = ", ".join(set(sources)) if sources else "BNPB / Media Siber"

            # Format Null-Safety untuk dampak
            korban_parts = []
            if ev.korban_meninggal > 0:
                korban_parts.append(f"{ev.korban_meninggal} Meninggal Dunia")
            if ev.korban_luka > 0:
                korban_parts.append(f"{ev.korban_luka} Luka-Luka")
            if ev.korban_hilang > 0:
                korban_parts.append(f"{ev.korban_hilang} Hilang")
            if ev.korban_mengungsi > 0:
                korban_parts.append(f"{ev.korban_mengungsi} Mengungsi")
            korban_text = " • ".join(korban_parts) if korban_parts else "Nihil korban jiwa"

            kerusakan_parts = []
            if ev.rumah_terendam > 0:
                kerusakan_parts.append(f"{ev.rumah_terendam} unit rumah terendam")
            if ev.luas_ha > 0:
                kerusakan_parts.append(f"{ev.luas_ha} Ha lahan terdampak")
            kerusakan_text = " • ".join(kerusakan_parts) if kerusakan_parts else "Nihil kerusakan berat"

            attrs = [
                ("Waktu Kejadian", ev.waktu_kejadian_text or "Dalam konfirmasi"),
                ("Lokasi Kejadian", ev.wilayah.hierarchy_display if ev.wilayah else "Wilayah Nasional"),
                ("Kronologi", lead.isi_ringkas if lead else "-"),
                ("Korban Jiwa & Terdampak", korban_text),
                ("Kerusakan Materil & Sarana Prasarana", kerusakan_text),
                ("Upaya Penanganan TRC", ev.upaya),
                ("Kondisi Mutakhir Lapangan", ev.kondisi_mutakhir),
                ("Status Kejadian", f"Terverifikasi Resmi (Kode: {ev.kode_kejadian})"),
                ("Sumber Rujukan Media", f"{sources_str} ({ev.berita_list.count()} rujukan portal)"),
            ]

            for label, val in attrs:
                p_line = doc.add_paragraph()
                p_line.paragraph_format.left_indent = Inches(0.25)
                p_line.paragraph_format.space_after = Pt(2)

                r_label = p_line.add_run(f"➢ {label}: ")
                r_label.font.name = "Arial"
                r_label.font.size = Pt(9.5)
                r_label.font.bold = True

                r_val = p_line.add_run(str(val))
                r_val.font.name = "Arial"
                r_val.font.size = Pt(9.5)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
