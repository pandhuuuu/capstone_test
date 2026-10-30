# seed_and_ingest.py
import os
import json
import datetime
import zoneinfo
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from apps.disasters.models import (
    MasterWilayah,
    SiklusLaporan,
    KejadianBencana,
    BeritaBencana,
    LogAuditVerifikasi,
    default_dampak_korban,
    default_dampak_kerusakan,
)

WIB = zoneinfo.ZoneInfo("Asia/Jakarta")


def seed_master_wilayah():
    print("=== 1. SEEDING MASTER DATA WILAYAH KEMENDAGRI ===")
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'kemendagri_sample.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        wilayah_list = json.load(f)

    for item in wilayah_list:
        # Provinsi
        prov, _ = MasterWilayah.objects.get_or_create(
            id_wilayah=item['provinsi_kode'],
            defaults={
                'nama_wilayah': item['provinsi_nama'],
                'level': 'PROVINSI'
            }
        )
        # Kab/Kota
        kab, _ = MasterWilayah.objects.get_or_create(
            id_wilayah=item['kab_kota_kode'],
            defaults={
                'nama_wilayah': item['kab_kota_nama'],
                'level': 'KAB_KOTA',
                'parent': prov
            }
        )
        # Kecamatan
        MasterWilayah.objects.get_or_create(
            id_wilayah=item['kecamatan_kode'],
            defaults={
                'nama_wilayah': item['kecamatan_nama'],
                'level': 'KECAMATAN',
                'parent': kab
            }
        )
    print(f"Total Master Wilayah di database: {MasterWilayah.objects.count()} entri.")


def run_seed_and_ingest():
    seed_master_wilayah()

    print("\n=== 2. MENYIAPKAN SIKLUS OPERASIONAL 24 JAM (07.00 - 07.00 WIB) ===")
    cycle = SiklusLaporan.get_or_create_current_cycle()
    print(f"Siklus Aktif: {cycle.kode_siklus} [{cycle.range_display}]")

    print("\n=== 3. SEEDING KEJADIAN BENCANA & BERITA RUJUKAN ===")

    # Master Wilayah Helpers
    wilayah_dayeuhkolot = MasterWilayah.objects.filter(id_wilayah='32.04.11').first()
    wilayah_nabire = MasterWilayah.objects.filter(id_wilayah='94.01.01').first()
    wilayah_agam = MasterWilayah.objects.filter(id_wilayah='13.06.01').first()
    wilayah_penjaringan = MasterWilayah.objects.filter(id_wilayah='31.72.01').first()
    wilayah_kebayoran = MasterWilayah.objects.filter(id_wilayah='31.74.05').first()

    now = timezone.now().astimezone(WIB)

    sample_incidents = [
        {
            "kode": f"BNPB-{cycle.kode_siklus.replace('SIKLUS-', '')}-001",
            "jenis": "Banjir",
            "wilayah": wilayah_dayeuhkolot,
            "waktu_text": f"{now.strftime('%d/%m/%Y')} 13:45 WIB",
            "waktu_riil": now - datetime.timedelta(minutes=15),
            "status": "PENDING",
            "is_isu_bantuan": False,
            "is_manual": False,
            "dampak_korban": {
                "meninggal": 0, "luka_berat": 0, "luka_ringan": 2, "hilang": 0, "mengungsi": 450,
                "lokasi_pengungsi": "Posko Kantor Desa Dayeuhkolot & Masjid As-Shofia"
            },
            "dampak_kerusakan": {
                "rumah_rb": 0, "rumah_rs": 0, "rumah_rr": 0, "rumah_terendam": 127, "fasum": 1, "luas_ha": 15,
                "sarpras_keterangan": "Akses jalan penghubung Dayeuhkolot - Baleendah terputus"
            },
            "upaya": "TRC BPBD Kab. Bandung mendirikan 2 tenda darurat dan menerjunkan 3 unit perahu karet evakuasi warga kelompok rentan.",
            "kondisi_mutakhir": "Tinggi muka air genangan 40-70 cm, cuaca gerimis, situasi evakuasi terkendali.",
            "lead_judul": "Banjir Luapan Citarum Rendam Ratusan Rumah di Dayeuhkolot",
            "lead_portal": "Detikcom",
            "lead_url": "https://news.detik.com/berita/banjir-citarum-dayeuhkolot",
            "lead_ringkas": "Tinggi muka air mencapai 80-150 cm akibat hujan deras berdurasi 4 jam di hulu sungai. Akses jalan terputus, 450 jiwa mengungsi di kantor desa.",
            "extra_sources": [
                ("Kompas.com", "https://kompas.com/regional/banjir-bandung", "Ketinggian air banjir Dayeuhkolot belum surut petang ini."),
                ("Antara News", "https://antaranews.com/berita/banjir-jabar", "BPBD Jabar salurkan bantuan selimut dan perahu ke Dayeuhkolot.")
            ]
        },
        {
            "kode": f"BNPB-{cycle.kode_siklus.replace('SIKLUS-', '')}-002",
            "jenis": "Karhutla",
            "wilayah": wilayah_nabire,
            "waktu_text": f"{now.strftime('%d/%m/%Y')} 11:20 WIB",
            "waktu_riil": now - datetime.timedelta(hours=2, minutes=40),
            "status": "PENDING",
            "is_isu_bantuan": True,
            "is_manual": False,
            "dampak_korban": {
                "meninggal": 0, "luka_berat": 0, "luka_ringan": 0, "hilang": 0, "mengungsi": 35,
                "lokasi_pengungsi": "Puskesmas Nabire Kota"
            },
            "dampak_kerusakan": {
                "rumah_rb": 0, "rumah_rs": 0, "rumah_rr": 0, "rumah_terendam": 0, "fasum": 0, "luas_ha": 172,
                "sarpras_keterangan": "Lahan gambut pesisir terbakar, jarak pandang < 400 meter"
            },
            "upaya": "Manggala Agni bersama BPBD memblokade rembetan titik api menuju perkampungan padat.",
            "kondisi_mutakhir": "Asap pekat masih mengepul, kebutuhan mendesak: 5.000 masker N95 & tangki air portabel.",
            "lead_judul": "Karhutla 172 Ha Lahan Gambut, Warga Keluhkan Bantuan Masker Terlambat",
            "lead_portal": "Antara News",
            "lead_url": "https://antaranews.com/karhutla-nabire-papua",
            "lead_ringkas": "Kabut asap mulai mengganggu jarak pandang di pesisir Nabire hingga di bawah 400 meter. Kebutuhan mendesak: 5.000 masker N95 & tangki air portable.",
            "extra_sources": []
        },
        {
            "kode": f"BNPB-{cycle.kode_siklus.replace('SIKLUS-', '')}-003",
            "jenis": "Tanah Longsor",
            "wilayah": wilayah_agam,
            "waktu_text": f"{now.strftime('%d/%m/%Y')} 09:15 WIB",
            "waktu_riil": now - datetime.timedelta(hours=4, minutes=30),
            "status": "PENDING",
            "is_isu_bantuan": False,
            "is_manual": False,
            "dampak_korban": {
                "meninggal": 0, "luka_berat": 1, "luka_ringan": 0, "hilang": 0, "mengungsi": 80,
                "lokasi_pengungsi": "Balai Pertemuan Nagari Tanjung Sani"
            },
            "dampak_kerusakan": {
                "rumah_rb": 2, "rumah_rs": 3, "rumah_rr": 5, "rumah_terendam": 0, "fasum": 1, "luas_ha": 3,
                "sarpras_keterangan": "Akses jalan lingkar danau tertutup material longsor sepanjang 35 meter"
            },
            "upaya": "Dua alat berat loader dikerahkan dari posko Maninjau untuk pembersihan badan jalan.",
            "kondisi_mutakhir": "Jalan dibuka darurat satu jalur, pembersihan material terus berlangsung.",
            "lead_judul": "Material Longsor Tutup Badan Jalan Kelok 44, Tim TRC Bersihkan Jalur",
            "lead_portal": "Padang Ekspres",
            "lead_url": "https://padek.jawapos.com/longsor-kelok-44",
            "lead_ringkas": "Tebing setinggi 12 meter runtuh menutupi tikungan ke-17. Dua alat berat loader dikerahkan dari posko Maninjau. Arus dialihkan via Pariaman.",
            "extra_sources": []
        },
        {
            "kode": f"BNPB-{cycle.kode_siklus.replace('SIKLUS-', '')}-004",
            "jenis": "Gempa Bumi / Tsunami",
            "wilayah": wilayah_penjaringan,
            "waktu_text": f"{now.strftime('%d/%m/%Y')} 08:30 WIB",
            "waktu_riil": now - datetime.timedelta(hours=5, minutes=15),
            "status": "HOAKS",
            "is_isu_bantuan": False,
            "is_manual": False,
            "dampak_korban": default_dampak_korban(),
            "dampak_kerusakan": default_dampak_kerusakan(),
            "upaya": "Tim Siber Pusdalops BNPB mengklarifikasi video arsip tahun 2021 yang disebarkan ulang tanpa konteks.",
            "kondisi_mutakhir": "Situasi perairan Teluk Jakarta normal, pasang surut sensor BMKG nihil anomali seismik.",
            "lead_judul": "Beredar Video Bernarasi Tsunami Teluk Jakarta - Hasil Cek Fakta BMKG Nihil Aktivitas Seismik",
            "lead_portal": "TikTok Viral & WAG",
            "lead_url": "https://cekfakta.bnpb.go.id/hoaks-tsunami-jakarta",
            "lead_ringkas": "Potongan video gelombang tinggi di pelabuhan adalah arsip tahun 2021. BMKG & InaRISK konfirmasi nihil anomali sensor pasut.",
            "extra_sources": []
        },
        {
            "kode": f"BNPB-{cycle.kode_siklus.replace('SIKLUS-', '')}-005",
            "jenis": "Banjir",
            "wilayah": wilayah_kebayoran,
            "waktu_text": f"{now.strftime('%d/%m/%Y')} 06:45 WIB",
            "waktu_riil": now - datetime.timedelta(hours=7),
            "status": "TERVERIFIKASI",
            "is_isu_bantuan": False,
            "is_manual": True,
            "dampak_korban": {
                "meninggal": 0, "luka_berat": 0, "luka_ringan": 0, "hilang": 0, "mengungsi": 25,
                "lokasi_pengungsi": "Masjid Al-Ihsan Kebayoran Lama"
            },
            "dampak_kerusakan": {
                "rumah_rb": 0, "rumah_rs": 0, "rumah_rr": 0, "rumah_terendam": 40, "fasum": 0, "luas_ha": 2,
                "sarpras_keterangan": "Genangan jalan Ciputat Raya 30-50 cm, surut dalam 2 jam"
            },
            "upaya": "Pompa mobil Dinas SDA DKI dan Damkar dikerahkan menyedot genangan ke kali Pesanggrahan.",
            "kondisi_mutakhir": "Air telah surut total, warga membersihkan sisa lumpur, lalu lintas lancar.",
            "lead_judul": "Genangan Air Luapan Kali Pesanggrahan di Kebayoran Lama Surut Total",
            "lead_portal": "Panggilan Radio Satgas BPBD DKI",
            "lead_url": "https://bpbd.jakarta.go.id/pantauan-kali-pesanggrahan",
            "lead_ringkas": "Laporan manual ad-hoc DI-01 via radio satgas. Pompa mobil bergerak cepat mengatasi genangan.",
            "extra_sources": []
        }
    ]

    for item in sample_incidents:
        kejadian, created = KejadianBencana.objects.get_or_create(
            kode_kejadian=item['kode'],
            defaults={
                'siklus': cycle,
                'jenis_bencana': item['jenis'],
                'wilayah': item['wilayah'],
                'waktu_kejadian_text': item['waktu_text'],
                'waktu_kejadian_riil': item['waktu_riil'],
                'status_verifikasi': item['status'],
                'is_isu_bantuan': item['is_isu_bantuan'],
                'is_manual_entry': item['is_manual'],
                'dampak_korban': item['dampak_korban'],
                'dampak_kerusakan': item['dampak_kerusakan'],
                'upaya': item['upaya'],
                'kondisi_mutakhir': item['kondisi_mutakhir']
            }
        )

        if created:
            # Lead Article
            BeritaBencana.objects.create(
                kejadian=kejadian,
                judul=item['lead_judul'],
                url_artikel=item['lead_url'],
                nama_portal=item['lead_portal'],
                isi_ringkas=item['lead_ringkas'],
                waktu_terbit=item['waktu_riil'],
                similarity_score=1.0,
                is_master_source=True
            )

            # Additional sources
            for portal_name, url_extra, ringkas_extra in item.get('extra_sources', []):
                BeritaBencana.objects.create(
                    kejadian=kejadian,
                    judul=f"{item['lead_judul']} ({portal_name})",
                    url_artikel=url_extra,
                    nama_portal=portal_name,
                    isi_ringkas=ringkas_extra,
                    waktu_terbit=item['waktu_riil'] + datetime.timedelta(minutes=10),
                    similarity_score=0.88,
                    is_master_source=False
                )

            # Audit Log
            LogAuditVerifikasi.objects.create(
                kejadian=kejadian,
                id_user="Operator Shift 1 (Budi)",
                shift="Shift 1 (07.00 - 15.00 WIB)",
                status_sebelum="DRAFT_INGESTION",
                status_sesudah=item['status'],
                kontak_bpbd_dihubungi="TRC BPBD Setempat",
                catatan="Penetapan data awal pada dasbor pemantauan siklus 24 jam."
            )

    print(f"\n[SUKSES] Data Kejadian Berhasil Disiapkan:")
    print(f"  • Belum Terverifikasi (Pending) : {KejadianBencana.objects.filter(siklus=cycle, status_verifikasi='PENDING').count()}")
    print(f"  • Terverifikasi Resmi           : {KejadianBencana.objects.filter(siklus=cycle, status_verifikasi='TERVERIFIKASI').count()}")
    print(f"  • Hoaks / Ditolak               : {KejadianBencana.objects.filter(siklus=cycle, status_verifikasi='HOAKS').count()}")
    print(f"  • Total Kejadian Siklus Ini     : {KejadianBencana.objects.filter(siklus=cycle).count()}")


if __name__ == '__main__':
    run_seed_and_ingest()
