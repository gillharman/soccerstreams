import difflib

from matches.models import Match
from streamablematches.models import ScannedMatch, StreamableMatch

def match_streamable_games():
    # d = '2018-12-22'
    ignore = 0
    insert = 0
    update = 0
    todays_matches = Match.objects.get_games()
    streamable_matches = ScannedMatch.objects.get_games().values('id','match')
    match_name = streamable_matches.values_list('match', flat=True)

    for match in todays_matches:
        ### CREATE MATCH NAME ###
        full_match_name = ' vs '.join([match.home_team.name, match.away_team.name])

        ### RUN CLOSE MATCH ###
        close_match_full_name = difflib.get_close_matches(full_match_name, match_name, n=1)

        ### SAVE IF MATCH FOUND ###
        if close_match_full_name:
                if StreamableMatch.objects.filter(match=match):
                    ignore += 1
                else:
                    streamable_game = StreamableMatch()
                    streamable_game.match = match
                    stream = ScannedMatch.objects.get(id=streamable_matches.get(match=close_match_full_name[0])['id'])
                    streamable_game.streamable_games = stream
                    streamable_game.save()
                    insert += 1
    return {
        'insert': str(insert),
        'update': str(update),
        'ignore': str(ignore)
    }