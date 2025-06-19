from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recommender.urls')),  # ✅ Must include the recommender app
    path('', lambda request: HttpResponse("Welcome to the Music Recommender API!")),
]