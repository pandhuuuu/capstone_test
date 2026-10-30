# apps/disasters/models.py
import datetime
import zoneinfo
from django.db import models
from django.utils import timezone

WIB = zoneinfo.ZoneInfo("Asia/Jakarta")


class MasterWilayah(models.Model):
    """
    Tabel Master Wilayah Administratif Kemendagri.
    Mendukung relasi bertingkat: PROVINSI -> KAB_KOTA -> KECAMATAN.
    """
    TINGKAT_CHOICES = [
        ('PROVINSI', 'Provinsi'),
        ('KAB_KOTA', 'Kabupaten/Kota'),
        ('KECAMATAN', 'Kecamatan'),
    ]

    id_wilayah = models.CharField(max_length=30, primary_key=True, help_text="Contoh: '32.04.11'")
    nama_wilayah = models.CharField(max_length=150, help_text="Contoh: 'Dayeuhkolot'")
    level = models.CharField(max_length=20, choices=TINGKAT_CHOICES)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        db_table = 'master_wilayah'
        verbose_name = 'Master Wilayah Kemendagri'
        verbose_name_plural = 'Master Wilayah Kemendagri'
        indexes = [
            models.Index(fields=['level'], name='idx_wilayah_level'),
            models.Index(fields=['parent'], name='idx_wilayah_parent'),
        ]

    def __str__(self):
        return f"{self.nama_wilayah} [{self.id_wilayah}] ({self.level})"

    @property
    def hierarchy_display(self):
        """Menghasilkan representasi breadcrumb hierarkis Kemendagri."""
        if self.level == 'PROVINSI':
            return self.nama_wilayah
        elif self.level == 'KAB_KOTA':
            prov = self.parent.nama_wilayah if self.parent else ''
            return f"{prov} > {self.nama_wilayah}" if prov else self.nama_wilayah
        elif self.level == 'KECAMATAN':
            kab = self.parent.nama_wilayah if self.parent else ''
            prov = self.parent.parent.nama_wilayah if (self.parent and self.parent.parent) else ''
            parts = [p for p in [prov, kab, self.nama_wilayah] if p]
            return " > ".join(parts)
        return self.nama_wilayah


class SiklusLaporan(models.Model):
    """
    Tabel Siklus Operasional 24 Jam Pusdalops BNPB (Windowing 07.00 - 07.00 WIB).
    Mencegah tumpang tindih data antarshift kerja (pagi, sore, dan malam).
    """
    kode_siklus = models.CharField(max_length=30, primary_key=True, help_text="Contoh: 'SIKLUS-20261009'")
    waktu_buka = models.DateTimeField(help_text="07.00.00 WIB hari pertama")
    waktu_tutup = models.DateTimeField(help_text="07.00.00 WIB hari berikutnya")
    is_locked = models.BooleanField(default=False, help_text="Status kunci resmi supervisor")
    locked_by = models.CharField(max_length=100, null=True, blank=True)
    locked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'siklus_laporan'
        verbose_name = 'Siklus Laporan 24 Jam'
        verbose_name_plural = 'Siklus Laporan 24 Jam'
        indexes = [
            models.Index(fields=['is_locked'], name='idx_siklus_locked'),
        ]

    def __str__(self):
        buka_str = self.waktu_buka.astimezone(WIB).strftime('%d/%m/%Y %H:%M')
        tutup_str = self.waktu_tutup.astimezone(WIB).strftime('%d/%m/%Y %H:%M')
        return f"{self.kode_siklus} ({buka_str} - {tutup_str} WIB)"

    @classmethod
    def get_or_create_current_cycle(cls, dt=None):
        """
        Menentukan dan mengembalikan objek SiklusLaporan berjalan sesuai cut-off 07.00 WIB.
        Jika waktu sekarang 14.00 WIB tanggal 9 Okt -> SIKLUS-20261009 (09/10 07.00 s/d 10/10 07.00 WIB).
        Jika waktu sekarang 02.00 WIB tanggal 10 Okt -> SIKLUS-20261009 (karena belum pukul 07.00 WIB).
        """
        if dt is None:
            now_wib = timezone.now().astimezone(WIB)
        elif timezone.is_naive(dt):
            now_wib = dt.replace(tzinfo=WIB)
        else:
            now_wib = dt.astimezone(WIB)

        if now_wib.hour < 7:
            cycle_date = now_wib.date() - datetime.timedelta(days=1)
        else:
            cycle_date = now_wib.date()

        kode_siklus = f"SIKLUS-{cycle_date.strftime('%Y%m%d')}"
        waktu_buka = datetime.datetime.combine(cycle_date, datetime.time(7, 0, 0), tzinfo=WIB)
        waktu_tutup = waktu_buka + datetime.timedelta(days=1)

        siklus, _ = cls.objects.get_or_create(
            kode_siklus=kode_siklus,
            defaults={
                'waktu_buka': waktu_buka,
                'waktu_tutup': waktu_tutup,
                'is_locked': False
            }
        )
        return siklus

    @property
    def range_display(self):
        """Menghasilkan format teks rentang siklus dinas BNPB."""
        buka_wib = self.waktu_buka.astimezone(WIB)
        tutup_wib = self.waktu_tutup.astimezone(WIB)
        bulan_id = [
            '', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
            'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
        ]
        return (
            f"{buka_wib.day:02d} {bulan_id[buka_wib.month].upper()} {buka_wib.year} (07.00 WIB) - "
            f"{tutup_wib.day:02d} {bulan_id[tutup_wib.month].upper()} {tutup_wib.year} (07.00 WIB)"
        )

    @property
    def countdown_text(self):
        """Menghitung waktu mundur sisa jam/menit menuju cut-off 07.00 WIB."""
        now_wib = timezone.now().astimezone(WIB)
        tutup_wib = self.waktu_tutup.astimezone(WIB)
        diff = tutup_wib - now_wib
        if diff.total_seconds() <= 0:
            return "Siklus telah ditutup (07.00 WIB)"
        jam = int(diff.total_seconds() // 3600)
        menit = int((diff.total_seconds() % 3600) // 60)
        return f"{jam:02d}j {menit:02d}m menuju cut-off 07.00 WIB"


def default_dampak_korban():
    return {
        "meninggal": 0,
        "luka_berat": 0,
        "luka_ringan": 0,
        "hilang": 0,
        "mengungsi": 0,
        "lokasi_pengungsi": ""
    }


def default_dampak_kerusakan():
    return {
        "rumah_rb": 0,
        "rumah_rs": 0,
        "rumah_rr": 0,
        "rumah_terendam": 0,
        "fasum": 0,
        "luas_ha": 0,
        "sarpras_keterangan": ""
    }


class KejadianBencana(models.Model):
    """
    Tabel Entitas Kejadian Bencana Faktual (Hasil Klastering & Triage).
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending / Belum Terverifikasi'),
        ('TERVERIFIKASI', 'Terverifikasi Resmi'),
        ('HOAKS', 'Hoaks / Ditolak'),
    ]

    id_kejadian = models.BigAutoField(primary_key=True)
    kode_kejadian = models.CharField(max_length=50, unique=True, help_text="Contoh: 'BNPB-20261009-001'")
    siklus = models.ForeignKey(
        SiklusLaporan,
        on_delete=models.RESTRICT,
        related_name='kejadian_list'
    )
    jenis_bencana = models.CharField(max_length=100, default='Banjir')
    wilayah = models.ForeignKey(
        MasterWilayah,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='kejadian_list'
    )

    # Metadata Waktu Riil Hasil Konfirmasi
    waktu_kejadian_riil = models.DateTimeField(null=True, blank=True)
    waktu_kejadian_text = models.CharField(max_length=150, null=True, blank=True, default='Dalam konfirmasi')

    # Fakta Dampak Lapangan (Universal JSONField)
    dampak_korban = models.JSONField(default=default_dampak_korban)
    dampak_kerusakan = models.JSONField(default=default_dampak_kerusakan)

    upaya = models.TextField(default="• Dalam koordinasi dengan BPBD setempat")
    kondisi_mutakhir = models.TextField(default="• Situasi terpantau aman terkendali")

    status_verifikasi = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_manual_entry = models.BooleanField(default=False)
    is_isu_bantuan = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kejadian_bencana'
        verbose_name = 'Kejadian Bencana'
        verbose_name_plural = 'Daftar Kejadian Bencana'
        indexes = [
            models.Index(fields=['siklus'], name='idx_kejadian_siklus'),
            models.Index(fields=['status_verifikasi'], name='idx_kejadian_status'),
        ]

    @property
    def id(self):
        return self.id_kejadian

    def __str__(self):
        return f"[{self.status_verifikasi}] {self.kode_kejadian} - {self.jenis_bencana}"

    @property
    def lead_article(self):
        """Mengambil artikel berita utama (Lead Media) dari kejadian ini."""
        return self.berita_list.filter(is_master_source=True).first() or self.berita_list.first()

    @property
    def additional_sources_count(self):
        """Menghitung jumlah portal berita sekunder selain lead."""
        total = self.berita_list.count()
        return max(0, total - 1)

    @property
    def relative_time(self):
        """Menampilkan jarak waktu relatif dari publikasi/pencatatan data."""
        now = timezone.now()
        ref_time = self.waktu_kejadian_riil or self.created_at
        diff = now - ref_time
        seconds = diff.total_seconds()
        if seconds < 60:
            return "Baru saja"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m lalu"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}j lalu"
        else:
            return f"{int(seconds // 86400)}h lalu"

    # Quick Accessors untuk Dampak Lapangan
    @property
    def korban_meninggal(self):
        return (self.dampak_korban or {}).get('meninggal', 0)

    @property
    def korban_luka(self):
        data = self.dampak_korban or {}
        return data.get('luka_ringan', 0) + data.get('luka_berat', 0) if ('luka_berat' in data) else data.get('luka', 0)

    @property
    def korban_hilang(self):
        return (self.dampak_korban or {}).get('hilang', 0)

    @property
    def korban_mengungsi(self):
        return (self.dampak_korban or {}).get('mengungsi', 0)

    @property
    def rumah_terendam(self):
        return (self.dampak_kerusakan or {}).get('rumah_terendam', 0)

    @property
    def rumah_rusak_berat(self):
        return (self.dampak_kerusakan or {}).get('rumah_rusak_berat', 0)

    @property
    def rumah_rusak_sedang(self):
        return (self.dampak_kerusakan or {}).get('rumah_rusak_sedang', 0)

    @property
    def rumah_rusak_ringan(self):
        return (self.dampak_kerusakan or {}).get('rumah_rusak_ringan', 0)

    @property
    def fasum_rusak(self):
        return (self.dampak_kerusakan or {}).get('fasum_rusak', 0)

    @property
    def luas_ha(self):
        return (self.dampak_kerusakan or {}).get('luas_ha', 0)


class BeritaBencana(models.Model):
    """
    Tabel Berita Media Siber yang Terikat pada Suatu Kejadian Bencana.
    """
    id_berita = models.BigAutoField(primary_key=True)
    kejadian = models.ForeignKey(
        KejadianBencana,
        on_delete=models.CASCADE,
        related_name='berita_list'
    )
    judul = models.CharField(max_length=500)
    url_artikel = models.URLField(max_length=1000)
    nama_portal = models.CharField(max_length=100, help_text="Contoh: 'Detikcom', 'Kompas.com', 'BMKG'")
    isi_ringkas = models.TextField(null=True, blank=True)
    waktu_terbit = models.DateTimeField(null=True, blank=True)
    similarity_score = models.FloatField(default=1.0)
    is_master_source = models.BooleanField(default=False)

    class Meta:
        db_table = 'berita_bencana'
        verbose_name = 'Berita Bencana'
        verbose_name_plural = 'Daftar Berita Bencana'
        indexes = [
            models.Index(fields=['kejadian'], name='idx_berita_kejadian'),
        ]

    def __str__(self):
        return f"{self.nama_portal}: {self.judul[:60]}"


class LogAuditVerifikasi(models.Model):
    """
    Tabel Log Audit Forensik Verifikasi Petugas Piket PUSDALOPS.
    Merekam setiap perubahan status kejadian, identitas operator, dan penguncian siklus.
    """
    id_log = models.BigAutoField(primary_key=True)
    siklus = models.ForeignKey(
        SiklusLaporan,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    kejadian = models.ForeignKey(
        KejadianBencana,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    id_user = models.CharField(max_length=100, default='Operator Shift 1 (Budi)')
    shift = models.CharField(max_length=50, default='Shift 1 (07.00 - 15.00 WIB)')
    status_sebelum = models.CharField(max_length=30)
    status_sesudah = models.CharField(max_length=30)
    kontak_bpbd_dihubungi = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Nama personel BPBD/satgas yang dikonfirmasi"
    )
    catatan = models.TextField(null=True, blank=True)
    waktu_aksi = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log_audit_verifikasi'
        verbose_name = 'Log Audit Verifikasi'
        verbose_name_plural = 'Log Audit Verifikasi'
        indexes = [
            models.Index(fields=['kejadian'], name='idx_audit_kejadian'),
        ]

    def __str__(self):
        waktu_str = self.waktu_aksi.astimezone(WIB).strftime('%H:%M:%S')
        return f"[{waktu_str}] {self.id_user}: {self.status_sebelum} -> {self.status_sesudah}"
