# apps/analytics/issue_tagger.py
AID_COMPLAINT_KEYWORDS = [
    "keluhan bantuan", "belum menerima bantuan", "bantuan belum tiba",
    "kekurangan logistik", "terisolir", "sulit dijangkau", "bantuan terhambat",
    "kelaparan", "butuh tenda", "butuh makanan", "bantuan lambat",
    "protes warga", "tersendat", "minim bantuan", "kekurangan obat"
]

def detect_aid_issue(text):
    """
    Mendeteksi apakah artikel berita memuat isu keluhan logistik atau hambatan bantuan.
    Mengembalikan: (is_issue: bool, detected_keywords: list)
    """
    text_lower = text.lower()
    matched = []
    for kw in AID_COMPLAINT_KEYWORDS:
        if kw in text_lower:
            matched.append(kw)
            
    is_issue = len(matched) > 0
    return {
        "is_issue": is_issue,
        "keywords": matched,
        "label": "PERINGATAN ISU LOGISTIK/BANTUAN" if is_issue else "INFORMASI KEJADIAN REGULER"
    }
