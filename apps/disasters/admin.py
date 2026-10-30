# apps/disasters/admin.py
from django.contrib import admin
from .models import (
    MasterWilayah,
    SiklusLaporan,
    KejadianBencana,
    BeritaBencana,
    LogAuditVerifikasi,
)


@admin.register(MasterWilayah)
class MasterWilayahAdmin(admin.ModelAdmin):
    list_display = ('id_wilayah', 'nama_wilayah', 'level', 'parent')
    search_fields = ('id_wilayah', 'nama_wilayah')
    list_filter = ('level',)


@admin.register(SiklusLaporan)
class SiklusLaporanAdmin(admin.ModelAdmin):
    list_display = ('kode_siklus', 'waktu_buka', 'waktu_tutup', 'is_locked', 'locked_by')
    list_filter = ('is_locked',)
    search_fields = ('kode_siklus', 'locked_by')


class BeritaBencanaInline(admin.TabularInline):
    model = BeritaBencana
    extra = 0


class LogAuditVerifikasiInline(admin.TabularInline):
    model = LogAuditVerifikasi
    extra = 0
    readonly_fields = ('id_user', 'shift', 'status_sebelum', 'status_sesudah', 'kontak_bpbd_dihubungi', 'catatan', 'waktu_aksi')


@admin.register(KejadianBencana)
class KejadianBencanaAdmin(admin.ModelAdmin):
    list_display = (
        'kode_kejadian',
        'jenis_bencana',
        'wilayah',
        'status_verifikasi',
        'siklus',
        'is_isu_bantuan',
        'is_manual_entry',
        'updated_at'
    )
    list_filter = ('status_verifikasi', 'is_isu_bantuan', 'is_manual_entry', 'siklus')
    search_fields = ('kode_kejadian', 'jenis_bencana', 'upaya', 'kondisi_mutakhir')
    inlines = [BeritaBencanaInline, LogAuditVerifikasiInline]


@admin.register(BeritaBencana)
class BeritaBencanaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'nama_portal', 'kejadian', 'similarity_score', 'is_master_source', 'waktu_terbit')
    list_filter = ('nama_portal', 'is_master_source')
    search_fields = ('judul', 'isi_ringkas')


@admin.register(LogAuditVerifikasi)
class LogAuditVerifikasiAdmin(admin.ModelAdmin):
    list_display = ('kejadian', 'id_user', 'shift', 'status_sebelum', 'status_sesudah', 'waktu_aksi')
    list_filter = ('shift', 'status_sesudah', 'waktu_aksi')
