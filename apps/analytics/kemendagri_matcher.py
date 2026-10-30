# apps/analytics/kemendagri_matcher.py
import json
import os

class KemendagriMatcher:
    def __init__(self, master_data_path=None):
        if master_data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            master_data_path = os.path.join(base_dir, 'data', 'kemendagri_sample.json')
        
        with open(master_data_path, 'r', encoding='utf-8') as f:
            self.master_data = json.load(f)
            
        # Index nama kecamatan, kabupaten, provinsi
        self.kecamatans = {row['kecamatan_nama'].lower(): row for row in self.master_data}
        self.kab_kotas = {row['kab_kota_nama'].lower(): row for row in self.master_data}
        self.provinsis = {row['provinsi_nama'].lower(): row for row in self.master_data}

    def match_hierarchy_from_text(self, text):
        """
        Menganalisis teks berita untuk menemukan hierarki wilayah:
        Kecamatan -> Kabupaten/Kota -> Provinsi
        """
        text_lower = text.lower()
        
        # 1. Prioritas cari Kecamatan (tingkat paling spesifik)
        for kec_name, data in self.kecamatans.items():
            if kec_name in text_lower:
                return {
                    "matched_level": "KECAMATAN",
                    "id_wilayah": data["kecamatan_kode"],
                    "kecamatan": data["kecamatan_nama"],
                    "kab_kota": data["kab_kota_nama"],
                    "provinsi": data["provinsi_nama"],
                    "confidence": 1.0,
                    "keterangan": f"Ditemukan pencocokan presisi pada Kecamatan {data['kecamatan_nama']}"
                }
                
        # 2. Cari Kabupaten / Kota
        for kab_name, data in self.kab_kotas.items():
            # hapus awalan 'kabupaten' atau 'kota' untuk pencarian fleksibel
            clean_kab = kab_name.replace("kabupaten ", "").replace("kota ", "")
            if clean_kab in text_lower or kab_name in text_lower:
                return {
                    "matched_level": "KAB_KOTA",
                    "id_wilayah": data["kab_kota_kode"],
                    "kecamatan": None,
                    "kab_kota": data["kab_kota_nama"],
                    "provinsi": data["provinsi_nama"],
                    "confidence": 0.85,
                    "keterangan": f"Ditemukan pencocokan pada {data['kab_kota_nama']}"
                }
                
        # 3. Cari Provinsi
        for prov_name, data in self.provinsis.items():
            if prov_name in text_lower:
                return {
                    "matched_level": "PROVINSI",
                    "id_wilayah": data["provinsi_kode"],
                    "kecamatan": None,
                    "kab_kota": None,
                    "provinsi": data["provinsi_nama"],
                    "confidence": 0.70,
                    "keterangan": f"Hanya teridentifikasi tingkat Provinsi {data['provinsi_nama']}"
                }
                
        return None
