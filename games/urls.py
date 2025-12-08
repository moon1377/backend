from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.games_list, name="games_list"),
    path("<int:game_id>/", views.play_game, name="play_game"),
    path("<int:game_id>/close/", views.close_game, name="close_game"),
]