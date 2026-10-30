import feedparser
import requests

print("=== 1. TESTING GOOGLE NEWS RSS (Bencana Alam Indonesia) ===")
url = "https://news.google.com/rss/search?q=bencana+alam+OR+banjir+OR+longsor+when:2d&hl=id&gl=ID&ceid=ID:id"
feed = feedparser.parse(url)
print(f"Total berita ditemukan: {len(feed.entries)}")
for i, item in enumerate(feed.entries[:3], 1):
    print(f"[{i}] {item.title}")
    print(f"    Link: {item.link}")
    print(f"    Tanggal: {item.published}")

print("\n=== 2. TESTING OPEN DATA RESMI BMKG ===")
try:
    resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", timeout=10)
    if resp.status_code == 200:
        data = resp.json()["Infogempa"]["gempa"]
        print(f"Gempa Terkini: M {data.get('Magnitude')} | Kedalaman: {data.get('Kedalaman')}")
        print(f"Wilayah: {data.get('Wilayah')}")
        print(f"Waktu: {data.get('Tanggal')} {data.get('Jam')}")
        print(f"Potensi: {data.get('Potensi')}")
except Exception as e:
    print(f"BMKG Error: {e}")
