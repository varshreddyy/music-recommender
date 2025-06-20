from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import TemplateView
from recommender.views_frontend import index
urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('recommender.urls')), 
    path('', lambda request: HttpResponse("Welcome to the Music Recommender API!")),
    path('', TemplateView.as_view(template_name='index.html')),
]