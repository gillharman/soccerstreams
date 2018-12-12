from django.urls import path, re_path
from .views import matches, watch_game, get_match_info, new_get_games

urlpatterns = [
    path('all_games', matches, name="all_games"),
    path('new_all_games', new_get_games, name="new_all_games"),
    re_path(r'^watch_game/(?:match_id=(?P<match_id>\w+)/)?$', watch_game, name="watch_game"),
    re_path('ajax/match_info', get_match_info, name="get_match_info"),
]