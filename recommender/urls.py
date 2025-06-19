from django.urls import path
from . import views

urlpatterns = [
    path('songs/', views.all_songs),
    path('songs/<int:id>/', views.single_song),
    path('recommend/', views.recommend_songs_by_name),  # ✅ Must be present
]
