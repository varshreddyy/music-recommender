from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from .recommender_engine import recommend
from django.http import JsonResponse
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

    # Try to match user query with an existing song's name
    matched_song = Song.objects.filter(Q(song__icontains=song_name)).first()

    if not matched_song:
        return Response({'error': 'No matching song found in database'}, status=404)

    try:
        # Pass the full "text" field for better recommendation
        recommended = recommend(matched_song.text)
        serializer = SongSerializer(recommended, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"⚠️ Error in recommend_songs_by_name: {e}")
        return Response({'error': str(e)}, status=500)



