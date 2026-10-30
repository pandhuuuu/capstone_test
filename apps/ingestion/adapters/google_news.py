# apps/ingestion/adapters/google_news.py
import urllib.parse
import feedparser
from .base import BaseScraperAdapter

class GoogleNewsAdapter(BaseScraperAdapter):
    def __init__(self, query="bencana alam OR banjir OR longsor OR gempa when:1d"):
        encoded_query = urllib.parse.quote_plus(query)
        self.feed_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=id&gl=ID&ceid=ID:id"

    def fetch_latest(self) -> list:
        feed = feedparser.parse(self.feed_url)
        results = []
        for entry in feed.entries[:25]:
            title_parts = entry.title.rsplit(" - ", 1)
            clean_title = title_parts[0]
            source_name = title_parts[1] if len(title_parts) > 1 else "Google News"
            
            results.append({
                "title": clean_title,
                "summary": getattr(entry, "summary", clean_title),
                "url": entry.link,
                "source_name": source_name,
                "source_type": "RSS_PORTAL",
                "published_at": getattr(entry, "published", "")
            })
        return results
