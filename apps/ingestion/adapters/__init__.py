from .base import BaseScraperAdapter
from .google_news import GoogleNewsAdapter
from .bmkg_client import BMKGAdapter
from .social_adapter import SocialMediaExtensibleAdapter

__all__ = [
    "BaseScraperAdapter",
    "GoogleNewsAdapter",
    "BMKGAdapter",
    "SocialMediaExtensibleAdapter"
]
