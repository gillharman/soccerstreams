from django.urls import path
from .views import matches, watch_game

urlpatterns = [
    path('all_games', matches, name="all_games"),
    path('watch_game', watch_game, name="watch_game")
]