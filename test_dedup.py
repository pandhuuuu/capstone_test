from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from apps.analytics.deduplication import clean_text, ID_STOPWORDS

articles = [
    {
        "id": 1,
        "source": "Detikcom",
        "title": "Banjir Rendam Puluhan Rumah di Dayeuhkolot Kabupaten Bandung Akibat Luapan Citarum",
        "summary": "Banjir setinggi 50 hingga 100 cm merendam pemukiman warga di Dayeuhkolot Bandung setelah Sungai Citarum meluap."
    },
    {
        "id": 2,
        "source": "Kompas.com",
        "title": "Sungai Citarum Meluap, Ratusan Rumah di Dayeuhkolot Bandung Terendam Banjir",
        "summary": "Hujan deras menyebabkan Sungai Citarum meluap dan membanjiri kawasan Dayeuhkolot Kabupaten Bandung setinggi 1 meter."
    },
    {
        "id": 3,
        "source": "Tribunnews",
        "title": "Tanah Longsor Terjang Jalur Utama di Tarutung Tapanuli Utara",
        "summary": "Material longsor menutupi badan jalan lintas Sumatera di Tarutung Tapanuli Utara sehingga arus lalu lintas lumpuh."
    }
]

corpus = [clean_text(f"{a['title']} {a['summary']}") for a in articles]
for i, c in enumerate(corpus):
    print(f"Token Bersih Berita {i+1}: {c}")

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)
sim_matrix = cosine_similarity(tfidf_matrix)

print("\n=== HASIL KEMIRIPAN SETELAH STOPWORDS REMOVAL ===")
print(f"Berita 1 (Detik) vs Berita 2 (Kompas): {sim_matrix[0][1]:.4f} (KEMBAR/IDENTIK)")
print(f"Berita 1 (Detik) vs Berita 3 (Tribun): {sim_matrix[0][2]:.4f} (BERBEDA)")
