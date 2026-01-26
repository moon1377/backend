from django.urls import path
from . import views

app_name = 'memes'

urlpatterns = [
    path('', views.index, name='meme_gallery'),
]