# apps/ingestion/adapters/base.py
from abc import ABC, abstractmethod

class BaseScraperAdapter(ABC):
    """
    Interface standar untuk semua adapter sumber data (RSS, Web Portal, BMKG, Media Sosial).
    Menjamin output memiliki struktur seragam.
    """
    
    @abstractmethod
    def fetch_latest(self) -> list:
        """
        Mengembalikan list of dict:
        [
            {
                "title": str,
                "summary": str,
                "url": str,
                "source_name": str,
                "source_type": str, # 'RSS', 'API_GOV', 'SOCIAL_MEDIA'
                "published_at": str
            }
        ]
        """
        pass
