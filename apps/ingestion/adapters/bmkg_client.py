# apps/ingestion/adapters/bmkg_client.py
import requests
from .base import BaseScraperAdapter

class BMKGAdapter(BaseScraperAdapter):
    def __init__(self):
        self.endpoint_autogempa = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
        self.endpoint_terkini = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"

    def fetch_latest(self) -> list:
        results = []
        try:
            # 1. Fetch autogempa (Gempa M >= 5.0 atau terupdate)
            resp = requests.get(self.endpoint_autogempa, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get("Infogempa", {}).get("gempa", {})
                if data:
                    title = f"GEMPA BUMI M {data.get('Magnitude')} - {data.get('Wilayah')}"
                    summary = (
                        f"Pusat gempa berada di kedalaman {data.get('Kedalaman')}. "
                        f"Waktu: {data.get('Tanggal')} {data.get('Jam')}. "
                        f"Koordinat: {data.get('Coordinates')}. Potensi: {data.get('Potensi')}."
                    )
                    results.append({
                        "title": title,
                        "summary": summary,
                        "url": "https://www.bmkg.go.id",
                        "source_name": "BMKG Open Data",
                        "source_type": "API_GOV",
                        "published_at": f"{data.get('Tanggal')} {data.get('Jam')}"
                    })
        except Exception as e:
            print(f"[BMKGAdapter] Gagal mengambil autogempa: {e}")

        try:
            # 2. Fetch 5 gempa terkini
            resp_terkini = requests.get(self.endpoint_terkini, timeout=10)
            if resp_terkini.status_code == 200:
                gempa_list = resp_terkini.json().get("Infogempa", {}).get("gempa", [])
                for g in gempa_list[:5]:
                    title = f"GEMPA BUMI M {g.get('Magnitude')} - {g.get('Wilayah')}"
                    summary = (
                        f"Kedalaman {g.get('Kedalaman')}, Waktu: {g.get('Tanggal')} {g.get('Jam')}, "
                        f"Potensi: {g.get('Potensi')}."
                    )
                    results.append({
                        "title": title,
                        "summary": summary,
                        "url": "https://www.bmkg.go.id",
                        "source_name": "BMKG Open Data",
                        "source_type": "API_GOV",
                        "published_at": f"{g.get('Tanggal')} {g.get('Jam')}"
                    })
        except Exception as e:
            print(f"[BMKGAdapter] Gagal mengambil gempa terkini: {e}")

        return results
