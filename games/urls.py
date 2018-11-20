from django.urls import path, re_path
from .views import matches, watch_game

urlpatterns = [
    path('all_games', matches, name="all_games"),
    re_path(r'^watch_game/(?:match_id=(?P<match_id>\w+)/)?$', watch_game, name="watch_game")
]