from django.urls import path, re_path
from .views import league_matches, watch_game, add_ace_stream

urlpatterns = [
    re_path(r'^$', league_matches, name="league_matches"),  # USES A DEFAULT PARAMETER
    re_path(r'^(?P<league>\w+)/$', league_matches, name="league_matches"),
    re_path(r'watch_game/(?P<match_id>\d+)/$', watch_game, name="watch_game"),
    re_path(r'\w+/watch_game/(?P<match_id>\d+)/$', watch_game, name="watch_game"),
    path('add-ace-stream', add_ace_stream, name="add_ace_stream")
]