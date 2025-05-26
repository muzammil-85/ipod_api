from django.urls import path
from .views import create_podcast

urlpatterns = [
    path('create-podcast/', create_podcast),
]
