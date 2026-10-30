# apps/analytics/deduplication.py
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ID_STOPWORDS = {
    "yang", "di", "dan", "ke", "dari", "ini", "itu", "untuk", "pada", "adalah", "dengan",
    "oleh", "dalam", "setelah", "mulai", "hingga", "sehingga", "akibat", "merendam",
    "warga", "puluhan", "ratusan", "setinggi", "kawasan", "pemukiman", "jalur", "badan",
    "mengatakan", "terjadi", "saat", "juga", "tersebut", "ada", "bisa", "lebih"
}

def clean_text(text):
    text = (text or "").lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = [w for w in text.split() if w not in ID_STOPWORDS and len(w) > 2]
    return " ".join(tokens)

class DeduplicationEngine:
    def __init__(self, threshold=0.60):
        self.threshold = threshold

    def cluster_articles(self, articles):
        """
        articles: list of dicts with 'id', 'title', 'summary', 'source'
        Mengembalikan kelompok klaster kejadian.
        """
        if not articles:
            return []
            
        cleaned_texts = [clean_text(f"{a.get('title', '')} {a.get('summary', '')}") for a in articles]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
        sim_matrix = cosine_similarity(tfidf_matrix)

        visited = set()
        clusters = []

        for i in range(len(articles)):
            if i in visited:
                continue
                
            current_cluster = [articles[i]]
            visited.add(i)

            for j in range(i + 1, len(articles)):
                if j not in visited and sim_matrix[i][j] >= self.threshold:
                    current_cluster.append(articles[j])
                    visited.add(j)

            clusters.append({
                "lead_article": current_cluster[0],
                "all_articles": current_cluster,
                "total_sources": len(current_cluster),
                "is_duplicated": len(current_cluster) > 1
            })

        return clusters
