from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from .recommender_engine import get_recommender_engine
from django.db.models import Q

@api_view(['GET'])
def all_songs(request):
    songs = Song.objects.all()[:100]  # limit for performance
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def single_song(request, id):
    try:
        song = Song.objects.get(id=id)
        serializer = SongSerializer(song)
        return Response(serializer.data)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=404)


@api_view(['GET'])
def recommend_songs_by_name(request):
    song_name = request.GET.get('song_name', '').strip()

    if not song_name:
        return Response({'error': 'Song name required'}, status=400)

    # Find matching song
    matched_song = Song.objects.filter(Q(song__icontains=song_name)).first()

    if not matched_song:
        return Response({'error': 'No matching song found in database'}, status=404)

    try:
        # Dynamically load the recommender engine
        song_ids, tfidf_matrix, vectorizer = get_recommender_engine()

        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np

        # Find the index of the matched song
        index = song_ids.index(matched_song.id)
        song_vector = tfidf_matrix[index]
        similarities = cosine_similarity(song_vector, tfidf_matrix).flatten()

        # Get top 5 most similar songs (excluding itself)
        similar_indices = similarities.argsort()[::-1][1:6]
        similar_ids = [song_ids[i] for i in similar_indices]

        recommended_songs = Song.objects.filter(id__in=similar_ids)
        serializer = SongSerializer(recommended_songs, many=True)
        return Response(serializer.data)

    except Exception as e:
        print(f"⚠️ Error in recommend_songs_by_name: {e}")
        return Response({'error': str(e)}, status=500)



