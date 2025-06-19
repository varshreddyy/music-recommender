from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender.models import Song

def build_engine():
    songs = list(Song.objects.values('id', 'text'))
    texts = [s['text'] for s in songs]
    ids = [s['id'] for s in songs]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    return ids, tfidf_matrix, vectorizer

# Build engine on module load
song_ids, tfidf_matrix, vectorizer = build_engine()

def recommend(query, top_n=5):
    if not query.strip():
        return []

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    if similarities.size == 0:
        return []

    top_indices = similarities.argsort()[-top_n:][::-1]
    top_song_ids = [song_ids[i] for i in top_indices]

    return Song.objects.filter(id__in=top_song_ids)
