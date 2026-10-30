# apps/ingestion/adapters/social_adapter.py
from .base import BaseScraperAdapter

class SocialMediaExtensibleAdapter(BaseScraperAdapter):
    """
    Adapter modular untuk mengintegrasikan Media Sosial di masa depan
    (misal: Telegram Channel BPBD, Twitter Disaster API, atau Facebook Public Post).
    
    Dirancang menggunakan prinsip Open-Closed (SOLID) sehingga BNPB dapat
    mengaktifkan kanal medsos baru cukup dengan mengisi token/kredensial API di sini.
    """
    def __init__(self, platform_name="Telegram BPBD Channel", api_token=None):
        self.platform_name = platform_name
        self.api_token = api_token

    def fetch_latest(self) -> list:
        # Simulasi / Plug-in point jika kredensial belum dikonfigurasi
        if not self.api_token:
            return []
            
        # Logika penarikan API Medsos (Telegram Bot API / Twitter API v2)
        return []
