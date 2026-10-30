# apps/dashboard/services/wa_formatter.py

def format_wa_sitrep(verified_events, current_cycle) -> str:
    """
    Menghasilkan ringkasan teks laporan situasi terkluster (A, B, C...)
    yang siap disiarkan (broadcast) ke WhatsApp Pimpinan dan Posko Pusdalops BNPB.
    """
    lines = [
        "🔴 *LAPORAN SITUASI BENCANA PUSDALOPS BNPB*",
        f"📅 Periode Siklus: *{current_cycle.range_display}*",
        "----------------------------------------",
        ""
    ]

    if not verified_events.exists():
        lines.append("Nihil kejadian bencana terverifikasi resmi pada siklus pemantauan ini.")
    else:
        current_cluster = None
        cluster_counter = 0
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for ev in verified_events:
            if ev.jenis_bencana != current_cluster:
                current_cluster = ev.jenis_bencana
                cluster_label = letters[cluster_counter % len(letters)]
                cluster_counter += 1
                lines.append(f"*{cluster_label}. {current_cluster.upper()}*")

            lead = ev.lead_article
            title = lead.judul if lead else ev.jenis_bencana
            loc = ev.wilayah.hierarchy_display if ev.wilayah else "Wilayah Terdampak"
            lines.append(f"• *{title}*")
            lines.append(f"  Lokasi: {loc}")
            lines.append(f"  Waktu: {ev.waktu_kejadian_text or '-'}")
            
            # Dampak ringkas
            korban = []
            if ev.korban_meninggal > 0:
                korban.append(f"{ev.korban_meninggal} MD")
            if ev.korban_mengungsi > 0:
                korban.append(f"{ev.korban_mengungsi} Mengungsi")
            dampak_str = ", ".join(korban) if korban else "Nihil korban jiwa"
            lines.append(f"  Dampak: {dampak_str}")
            lines.append(f"  Kondisi: {ev.kondisi_mutakhir}")
            lines.append("")

    lines.append("----------------------------------------")
    lines.append("Demikian dilaporkan. Pusdalops BNPB Siaga 24 Jam.")

    return "\n".join(lines)
