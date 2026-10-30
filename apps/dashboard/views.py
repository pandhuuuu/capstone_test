# apps/dashboard/views.py
import datetime
import zoneinfo
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
from django.db import models
from apps.disasters.models import (
    MasterWilayah,
    SiklusLaporan,
    KejadianBencana,
    BeritaBencana,
    LogAuditVerifikasi,
)
from .services import build_sitrep_docx, format_wa_sitrep

WIB = zoneinfo.ZoneInfo("Asia/Jakarta")


def index(request):
    """
    Dasbor Pemantauan Kebencanaan 24 Jam (Meja Piket Pusdalops BNPB).
    Mendukung tab status dinamis (PENDING, TERVERIFIKASI, HOAKS, SEMUA) & filter multi-dimensi.
    """
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    status_tab = request.GET.get('tab', 'PENDING').upper()
    search_query = request.GET.get('q', '').strip()
    provinsi_filter = request.GET.get('provinsi', '').strip()
    bencana_filter = request.GET.get('bencana', '').strip()

    events_qs = KejadianBencana.objects.filter(siklus=current_cycle).select_related('wilayah', 'siklus').prefetch_related('berita_list')

    # Status Tab Filter
    if status_tab in ['PENDING', 'TERVERIFIKASI', 'HOAKS']:
        events = events_qs.filter(status_verifikasi=status_tab)
    else:
        events = events_qs

    # Search & Dropdown Filters
    if search_query:
        events = events.filter(
            models.Q(jenis_bencana__icontains=search_query) |
            models.Q(berita_list__judul__icontains=search_query) |
            models.Q(wilayah__nama_wilayah__icontains=search_query)
        ).distinct()
    if provinsi_filter and provinsi_filter != 'Semua Provinsi (38)':
        events = events.filter(wilayah__nama_wilayah__icontains=provinsi_filter)
    if bencana_filter and bencana_filter != 'Semua Jenis Bencana':
        events = events.filter(jenis_bencana__iexact=bencana_filter)

    events = events.order_by('-created_at')

    # Pill Counter Stats
    counts = {
        'pending': events_qs.filter(status_verifikasi='PENDING').count(),
        'terverifikasi': events_qs.filter(status_verifikasi='TERVERIFIKASI').count(),
        'hoaks': events_qs.filter(status_verifikasi='HOAKS').count(),
        'semua': events_qs.count(),
    }

    # Data for Modals & Dropdowns
    provinces = MasterWilayah.objects.filter(level='PROVINSI').order_by('nama_wilayah')
    kab_kotas = MasterWilayah.objects.filter(level='KAB_KOTA').order_by('nama_wilayah')
    kecamatans = MasterWilayah.objects.filter(level='KECAMATAN').order_by('nama_wilayah')

    context = {
        'current_cycle': current_cycle,
        'status_tab': status_tab,
        'events': events,
        'counts': counts,
        'provinces': provinces,
        'kab_kotas': kab_kotas,
        'kecamatans': kecamatans,
        'search_query': search_query,
        'provinsi_filter': provinsi_filter,
        'bencana_filter': bencana_filter,
        'now_wib': timezone.now().astimezone(WIB),
        'active_menu': 'dashboard',
    }
    return render(request, 'dashboard/index.html', context)


def event_detail(request, pk):
    """
    Halaman detail terdedikasi untuk suatu kejadian bencana.
    """
    event = get_object_or_404(
        KejadianBencana.objects.select_related('wilayah', 'siklus').prefetch_related('berita_list', 'audit_logs'),
        pk=pk
    )
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    context = {
        'event': event,
        'current_cycle': current_cycle,
        'now_wib': timezone.now().astimezone(WIB),
    }
    return render(request, 'dashboard/detail.html', context)


@require_GET
def get_event_json(request, pk):
    """
    Mengembalikan data kejadian dalam format JSON untuk kebutuhan pemuatan modal verifikasi via AJAX.
    """
    event = get_object_or_404(KejadianBencana.objects.select_related('wilayah', 'siklus'), pk=pk)
    lead = event.lead_article

    wilayah_data = {
        "id_wilayah": event.wilayah.id_wilayah if event.wilayah else "",
        "nama_wilayah": event.wilayah.nama_wilayah if event.wilayah else "",
        "hierarchy": event.wilayah.hierarchy_display if event.wilayah else "Wilayah Nasional",
        "provinsi_id": "",
        "kab_kota_id": "",
        "kecamatan_id": ""
    }

    if event.wilayah:
        if event.wilayah.level == 'KECAMATAN':
            wilayah_data['kecamatan_id'] = event.wilayah.id_wilayah
            if event.wilayah.parent:
                wilayah_data['kab_kota_id'] = event.wilayah.parent.id_wilayah
                if event.wilayah.parent.parent:
                    wilayah_data['provinsi_id'] = event.wilayah.parent.parent.id_wilayah
        elif event.wilayah.level == 'KAB_KOTA':
            wilayah_data['kab_kota_id'] = event.wilayah.id_wilayah
            if event.wilayah.parent:
                wilayah_data['provinsi_id'] = event.wilayah.parent.id_wilayah
        elif event.wilayah.level == 'PROVINSI':
            wilayah_data['provinsi_id'] = event.wilayah.id_wilayah

    data = {
        "id": event.id_kejadian,
        "id_kejadian": event.id_kejadian,
        "kode_kejadian": event.kode_kejadian,
        "jenis_bencana": event.jenis_bencana,
        "status_verifikasi": event.status_verifikasi,
        "waktu_kejadian_text": event.waktu_kejadian_text or "",
        "waktu_kejadian_riil": event.waktu_kejadian_riil.strftime('%Y-%m-%d') if event.waktu_kejadian_riil else "",
        "waktu_kejadian_jam": event.waktu_kejadian_riil.strftime('%H:%M') if event.waktu_kejadian_riil else "",
        "upaya": event.upaya,
        "kondisi_mutakhir": event.kondisi_mutakhir,
        "wilayah": wilayah_data,
        "dampak_korban": event.dampak_korban or {},
        "dampak_kerusakan": event.dampak_kerusakan or {},
        "lead_judul": lead.judul if lead else f"Kejadian {event.jenis_bencana}",
        "lead_portal": lead.nama_portal if lead else "Pusdalops BNPB",
        "lead_url": lead.url_artikel if lead else "#",
        "lead_ringkas": lead.isi_ringkas if lead else "",
        "lead_waktu": lead.waktu_terbit.strftime('%d/%m/%Y %H:%M WIB') if (lead and lead.waktu_terbit) else ""
    }
    return JsonResponse({"status": "success", "event": data})


@require_POST
def update_verification(request, pk):
    """
    Menyimpan pembaruan hasil verifikasi lapangan 5 blok dari modal verifikasi.
    """
    event = get_object_or_404(KejadianBencana, pk=pk)
    old_status = event.status_verifikasi

    # 1. Wilayah Administratif
    id_wilayah = request.POST.get('id_wilayah')
    if id_wilayah:
        wilayah_obj = MasterWilayah.objects.filter(id_wilayah=id_wilayah).first()
        if wilayah_obj:
            event.wilayah = wilayah_obj

    # 2. Waktu Kejadian Riil
    tanggal_str = request.POST.get('incident_date')
    waktu_str = request.POST.get('incident_time')
    if tanggal_str and waktu_str:
        try:
            time_part = waktu_str.replace(" WIB", "").strip()
            dt_raw = datetime.datetime.strptime(f"{tanggal_str} {time_part}", "%Y-%m-%d %H:%M")
            event.waktu_kejadian_riil = dt_raw.replace(tzinfo=WIB)
            event.waktu_kejadian_text = f"{dt_raw.strftime('%d/%m/%Y')} {time_part} WIB"
        except Exception:
            event.waktu_kejadian_text = f"{tanggal_str} {waktu_str}"

    # 3. Fakta Dampak Lapangan
    korban = dict(event.dampak_korban or {})
    korban['meninggal'] = int(request.POST.get('korban_meninggal', 0) or 0)
    korban['luka_ringan'] = int(request.POST.get('korban_luka', 0) or 0)
    korban['hilang'] = int(request.POST.get('korban_hilang', 0) or 0)
    korban['mengungsi'] = int(request.POST.get('korban_mengungsi', 0) or 0)
    korban['lokasi_pengungsi'] = request.POST.get('lokasi_pengungsi', korban.get('lokasi_pengungsi', ''))
    event.dampak_korban = korban

    kerusakan = dict(event.dampak_kerusakan or {})
    kerusakan['rumah_terendam'] = int(request.POST.get('rumah_terendam', 0) or 0)
    kerusakan['luas_ha'] = int(request.POST.get('luas_terdampak', 0) or 0)
    event.dampak_kerusakan = kerusakan

    # 4. Upaya TRC & Kondisi
    if request.POST.get('upaya_trc'):
        event.upaya = request.POST.get('upaya_trc').strip()
    if request.POST.get('kondisi_lapangan'):
        event.kondisi_mutakhir = request.POST.get('kondisi_lapangan').strip()

    # 5. Keputusan Status & Jejak Audit
    new_status = request.POST.get('verification_status', old_status).upper()
    if new_status in ['PENDING', 'TERVERIFIKASI', 'HOAKS']:
        event.status_verifikasi = new_status

    event.save()

    # Catat Log Audit Forensik
    petugas = request.POST.get('petugas_validasi', 'Personel TRC Lapangan')
    catatan = request.POST.get('catatan_verifikasi', 'Pembaruan verifikasi via modal lapangan')
    LogAuditVerifikasi.objects.create(
        kejadian=event,
        id_user="Operator Shift 1 (Budi)",
        shift="Shift 1 (07.00 - 15.00 WIB)",
        status_sebelum=old_status,
        status_sesudah=event.status_verifikasi,
        kontak_bpbd_dihubungi=petugas,
        catatan=catatan
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
        return JsonResponse({"status": "success", "message": f"Kejadian {event.kode_kejadian} berhasil diperbarui!"})

    return redirect('index')


@require_POST
def create_manual_event(request):
    """
    Menyimpan laporan kejadian manual ad-hoc (FORM: DI-01/BNPB).
    """
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    now = timezone.now().astimezone(WIB)

    # Generate sequential incident code
    cycle_date_str = current_cycle.kode_siklus.replace('SIKLUS-', '')
    existing_count = KejadianBencana.objects.filter(siklus=current_cycle).count()
    new_code = f"BNPB-{cycle_date_str}-{(existing_count + 1):03d}"

    jenis_bencana = request.POST.get('jenis_bencana', 'Banjir').strip()
    saluran_masuk = request.POST.get('saluran_masuk', 'Telepon/Radio Satgas BPBD').strip()

    # Wilayah Kemendagri
    id_wilayah = request.POST.get('id_wilayah')
    wilayah_obj = MasterWilayah.objects.filter(id_wilayah=id_wilayah).first() if id_wilayah else None

    # Waktu
    tanggal_str = request.POST.get('tanggal_kejadian', now.strftime('%Y-%m-%d'))
    waktu_str = request.POST.get('waktu_kejadian', now.strftime('%H:%M'))
    try:
        dt_raw = datetime.datetime.strptime(f"{tanggal_str} {waktu_str}", "%Y-%m-%d %H:%M")
        waktu_riil = dt_raw.replace(tzinfo=WIB)
        waktu_text = f"{dt_raw.strftime('%d/%m/%Y')} {waktu_str} WIB"
    except Exception:
        waktu_riil = now
        waktu_text = f"{now.strftime('%d/%m/%Y')} {now.strftime('%H:%M')} WIB"

    # Kronologi & Dampak
    kronologi = request.POST.get('kronologi', 'Laporan ad-hoc via satgas daerah').strip()
    sarpras = request.POST.get('sarpras', '').strip()
    upaya = request.POST.get('upaya', 'BPBD setempat menuju lokasi asesmen').strip()

    dampak_korban = {
        "meninggal": int(request.POST.get('meninggal', 0) or 0),
        "luka_berat": 0,
        "luka_ringan": int(request.POST.get('luka', 0) or 0),
        "hilang": int(request.POST.get('hilang', 0) or 0),
        "mengungsi": int(request.POST.get('mengungsi', 0) or 0),
        "lokasi_pengungsi": "Posko Darurat Lapangan"
    }

    dampak_kerusakan = {
        "rumah_rb": 0, "rumah_rs": 0, "rumah_rr": 0,
        "rumah_terendam": 0, "fasum": 0, "luas_ha": 0,
        "sarpras_keterangan": sarpras
    }

    initial_status = request.POST.get('initial_status', 'PENDING').upper()
    if initial_status not in ['PENDING', 'TERVERIFIKASI']:
        initial_status = 'PENDING'

    kejadian = KejadianBencana.objects.create(
        kode_kejadian=new_code,
        siklus=current_cycle,
        jenis_bencana=jenis_bencana,
        wilayah=wilayah_obj,
        waktu_kejadian_riil=waktu_riil,
        waktu_kejadian_text=waktu_text,
        dampak_korban=dampak_korban,
        dampak_kerusakan=dampak_kerusakan,
        upaya=upaya,
        kondisi_mutakhir="Dalam penanganan awal tim gabungan satgas.",
        status_verifikasi=initial_status,
        is_manual_entry=True
    )

    # Buat berita lead internal
    judul_lead = f"Laporan {jenis_bencana} di {wilayah_obj.hierarchy_display if wilayah_obj else 'Wilayah Nasional'}"
    BeritaBencana.objects.create(
        kejadian=kejadian,
        judul=judul_lead,
        url_artikel="#",
        nama_portal=saluran_masuk,
        isi_ringkas=kronologi,
        waktu_terbit=waktu_riil,
        similarity_score=1.0,
        is_master_source=True
    )

    # Audit log
    LogAuditVerifikasi.objects.create(
        kejadian=kejadian,
        id_user="Operator Shift 1 (Budi)",
        shift="Shift 1 (07.00 - 15.00 WIB)",
        status_sebelum="INPUT_BARU",
        status_sesudah=initial_status,
        kontak_bpbd_dihubungi=saluran_masuk,
        catatan="Input manual formulir DI-01/BNPB ke dalam siklus aktif."
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
        return JsonResponse({"status": "success", "message": f"Kejadian manual {new_code} berhasil diterbitkan!", "kode": new_code})

    return redirect('index')


@require_POST
def merge_events(request):
    """
    Menggabungkan artikel berita dari kejadian duplikat/susulan ke kejadian target induk.
    """
    source_id = request.POST.get('source_id')
    target_id = request.POST.get('target_id')

    source_event = get_object_or_404(KejadianBencana, pk=source_id)
    target_event = get_object_or_404(KejadianBencana, pk=target_id)

    # Pindahkan seluruh berita dari source ke target
    for b in source_event.berita_list.all():
        b.kejadian = target_event
        b.is_master_source = False
        b.similarity_score = 0.85
        b.save()

    # Catat audit log pada target event
    LogAuditVerifikasi.objects.create(
        kejadian=target_event,
        id_user="Operator Shift 1 (Budi)",
        shift="Shift 1 (07.00 - 15.00 WIB)",
        status_sebelum=target_event.status_verifikasi,
        status_sesudah=target_event.status_verifikasi,
        kontak_bpbd_dihubungi="Sistem Deduplikasi",
        catatan=f"Penggabungan berita susulan dari #{source_event.kode_kejadian}."
    )

    # Hapus source event yang telah dimerge
    source_event.delete()

    return JsonResponse({
        "status": "success",
        "message": f"Berita berhasil digabungkan ke kejadian induk #{target_event.kode_kejadian}."
    })


@require_POST
def quick_status_change(request, pk):
    """
    Mengubah status verifikasi secara langsung dari dropdown baris tabel (Pending / Terverifikasi / Hoaks).
    """
    event = get_object_or_404(KejadianBencana, pk=pk)
    old_status = event.status_verifikasi
    new_status = request.POST.get('status', '').upper()

    if new_status in ['PENDING', 'TERVERIFIKASI', 'HOAKS'] and new_status != old_status:
        event.status_verifikasi = new_status
        event.save()

        LogAuditVerifikasi.objects.create(
            kejadian=event,
            id_user="Operator Shift 1 (Budi)",
            shift="Shift 1 (07.00 - 15.00 WIB)",
            status_sebelum=old_status,
            status_sesudah=new_status,
            kontak_bpbd_dihubungi="Dropdown Meja Kerja",
            catatan=f"Pembaruan status kilat via dropdown tabel dari {old_status} menjadi {new_status}."
        )

    return JsonResponse({"status": "success", "new_status": event.status_verifikasi})


def export_word_report(request):
    """
    Ekspor Dokumen Microsoft Word (.docx) Bagian A BNPB.
    Hanya menyertakan kejadian berstatus 'TERVERIFIKASI'.
    """
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    verified_events = KejadianBencana.objects.filter(
        siklus=current_cycle,
        status_verifikasi='TERVERIFIKASI'
    ).order_by('created_at')

    buffer = build_sitrep_docx(verified_events, current_cycle)
    filename = f"Laporan_Harian_BNPB_Bagian_A_{current_cycle.kode_siklus}.docx"
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def export_wa_summary(request):
    """
    Menghasilkan ringkasan teks siaran WhatsApp Pimpinan Pusdalops BNPB.
    """
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    verified_events = KejadianBencana.objects.filter(
        siklus=current_cycle,
        status_verifikasi='TERVERIFIKASI'
    ).order_by('jenis_bencana', 'created_at')

    text_output = format_wa_sitrep(verified_events, current_cycle)
    return JsonResponse({"status": "success", "text": text_output})


@require_POST
def sync_now(request):
    """Trigger manual sinkronisasi data."""
    try:
        from seed_and_ingest import run_seed_and_ingest
        run_seed_and_ingest()
        return JsonResponse({"status": "success", "message": "Sinkronisasi data berhasil dijalankan!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def export_center(request):
    """
    Menu 3: Pusat Ekspor Laporan & Pengesahan Sitrep Bagian A (PRD Section 4.3 & DESIGN Section 3.5).
    Menyediakan:
    - Pratinjau Naskah Dinas Resmi Pusdalops BNPB format cetak A4.
    - Kontrol status siklus: Draf Terbuka vs Terkunci Resmi.
    - Tombol Lock Snapshot & Emergency Unlock (Supervisor).
    - Ekspor berkas Word (.docx) & format siaran WhatsApp.
    """
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    verified_events = KejadianBencana.objects.filter(
        siklus=current_cycle,
        status_verifikasi='TERVERIFIKASI'
    ).select_related('wilayah').prefetch_related('berita_list').order_by('jenis_bencana', 'created_at')

    # Ringkasan Eksekutif Dampak Bencana
    stats = {
        'total_kejadian': verified_events.count(),
        'total_meninggal': sum(ev.korban_meninggal for ev in verified_events),
        'total_luka': sum(ev.korban_luka for ev in verified_events),
        'total_hilang': sum(ev.korban_hilang for ev in verified_events),
        'total_mengungsi': sum(ev.korban_mengungsi for ev in verified_events),
        'total_rusak_berat': sum(ev.rumah_rusak_berat for ev in verified_events),
        'total_rusak_sedang': sum(ev.rumah_rusak_sedang for ev in verified_events),
        'total_rusak_ringan': sum(ev.rumah_rusak_ringan for ev in verified_events),
        'total_terendam': sum(ev.rumah_terendam for ev in verified_events),
    }

    # Pengelompokan kejadian berdasarkan Jenis Bencana (A. BANJIR, B. GEMPA BUMI, ...)
    clusters = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    grouped = {}
    for ev in verified_events:
        grouped.setdefault(ev.jenis_bencana, []).append(ev)

    for i, (jenis, items) in enumerate(grouped.items()):
        clusters.append({
            'label': letters[i % len(letters)],
            'jenis': jenis,
            'items': items,
        })

    # Jejak Audit Siklus
    cycle_logs = LogAuditVerifikasi.objects.filter(siklus=current_cycle).order_by('-waktu_aksi')[:10]

    context = {
        'current_cycle': current_cycle,
        'verified_events': verified_events,
        'clusters': clusters,
        'stats': stats,
        'cycle_logs': cycle_logs,
        'now_wib': timezone.now().astimezone(WIB),
        'active_menu': 'export_center',
    }
    return render(request, 'dashboard/export_center.html', context)


@require_POST
def lock_cycle(request):
    """
    Mengunci siklus pemantauan 24 jam (Lock Snapshot) oleh Supervisor.
    Setelah dikunci, data berstatus Read-Only untuk mencegah perubahan tanpa izin.
    """
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    supervisor_name = request.POST.get('supervisor_name', 'Kasubdit Pengendalian Operasi').strip() or 'Kasubdit Pengendalian Operasi'
    catatan = request.POST.get('catatan', 'Pengesahan dan penguncian resmi laporan siklus 24 jam untuk penyerahan ke Kepala BNPB.').strip()

    if current_cycle.is_locked:
        return JsonResponse({"status": "error", "message": "Siklus ini sudah terkunci sebelumnya."}, status=400)

    current_cycle.is_locked = True
    current_cycle.locked_by = supervisor_name
    current_cycle.locked_at = timezone.now()
    current_cycle.save()

    # Catat audit log
    LogAuditVerifikasi.objects.create(
        siklus=current_cycle,
        id_user=supervisor_name,
        shift='Supervisor Pusdalops',
        status_sebelum='DRAF_TERBUKA',
        status_sesudah='TERKUNCI_RESMI',
        catatan=catatan
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            "status": "success",
            "message": f"Siklus {current_cycle.kode_siklus} berhasil dikunci secara resmi oleh {supervisor_name}."
        })
    return redirect('export_center')


@require_POST
def unlock_cycle(request):
    """
    Buka Kunci Darurat (Emergency Unlock) oleh Supervisor.
    Wajib menyertakan alasan pembukaan kunci untuk akuntabilitas dinas Pusdalops.
    """
    current_cycle = SiklusLaporan.get_or_create_current_cycle()
    supervisor_name = request.POST.get('supervisor_name', 'Supervisor Pusdalops').strip() or 'Supervisor Pusdalops'
    alasan_unlock = request.POST.get('alasan_unlock', '').strip()

    if not current_cycle.is_locked:
        return JsonResponse({"status": "error", "message": "Siklus ini saat ini tidak terkunci."}, status=400)

    if not alasan_unlock:
        return JsonResponse({"status": "error", "message": "Alasan pembukaan kunci darurat wajib diisi demi kepatuhan audit!"}, status=400)

    current_cycle.is_locked = False
    current_cycle.locked_by = None
    current_cycle.locked_at = None
    current_cycle.save()

    # Catat audit log
    LogAuditVerifikasi.objects.create(
        siklus=current_cycle,
        id_user=supervisor_name,
        shift='Supervisor Pusdalops',
        status_sebelum='TERKUNCI_RESMI',
        status_sesudah='DRAF_TERBUKA',
        catatan=f"EMERGENCY UNLOCK: {alasan_unlock}"
    )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            "status": "success",
            "message": f"Siklus {current_cycle.kode_siklus} berhasil dibuka kuncinya. Data kembali dapat dimutakhirkan."
        })
    return redirect('export_center')

