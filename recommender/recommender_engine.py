from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender.models import Song

# Global cache variables
_engine_cache = {
    "song_ids": [],
    "tfidf_matrix": None,
    "vectorizer": None
}

def build_engine():
    songs = list(Song.objects.values('id', 'text'))
    if not songs:
        raise ValueError("No songs found in database.")

    song_ids = [s['id'] for s in songs]
    lyrics = [s['text'] for s in songs]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(lyrics)

    # Cache the engine components
    _engine_cache["song_ids"] = song_ids
    _engine_cache["tfidf_matrix"] = tfidf_matrix
    _engine_cache["vectorizer"] = vectorizer

    return song_ids, tfidf_matrix, vectorizer

def get_recommender_engine():
    if _engine_cache["tfidf_matrix"] is None:
        return build_engine()
    return (_engine_cache["song_ids"], _engine_cache["tfidf_matrix"], _engine_cache["vectorizer"])

def recommend(query, top_n=5):
    if not query.strip():
        return []

    try:
        song_ids, tfidf_matrix, vectorizer = get_recommender_engine()

        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        if similarities.size == 0:
            return []

        top_indices = similarities.argsort()[-top_n:][::-1]
        top_song_ids = [song_ids[i] for i in top_indices]

        return Song.objects.filter(id__in=top_song_ids)

    except Exception as e:
        print(f"⚠️ Error in recommend(): {e}")
        return []
