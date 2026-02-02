from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(user_skills, job_text):
    """
    Calculates match score (%) between user skills/resume text
    and job description using TF-IDF + cosine similarity
    """

    if not user_skills or not job_text:
        return 0

    documents = [
        user_skills.lower(),
        job_text.lower()
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)
