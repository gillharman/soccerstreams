from django.urls import path, re_path
from .views import home, ajax_league_matches, watch_game, get_match_info

urlpatterns = [
    path('', home, name="home"),
    path('ajax/league_matches', ajax_league_matches, name="league_matches"),
    # path('new_all_games', new_get_games, name="new_all_games"),
    path('watch_game/<int:match_id>', watch_game, name="watch_game"),
    # re_path(r'^watch_game/(?:match_id=(?P<match_id>\w+)/)?$', watch_game, name="watch_game"),
    re_path('ajax/match_info', get_match_info, name="get_match_info"),
]