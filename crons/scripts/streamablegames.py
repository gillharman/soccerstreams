import difflib

from streamablematches.models.competitions import Match
from streamablematches.models.streamablematches import ScannedMatch, StreamableMatch


def match_streamable_games():
    ignore = 0
    insert = 0
    update = 0
    todays_matches = Match.objects.get_games()
    streamable_matches = ScannedMatch.objects.get_games().values('id','match')
    match_name = streamable_matches.values_list('match', flat=True)

    for match in todays_matches:
        # CREATE MATCH NAME
        full_match_name = ' vs '.join([match.home_team.name, match.away_team.name])

        # RUN CLOSE MATCH
        close_match_full_name = difflib.get_close_matches(full_match_name, match_name, n=1)

        # SAVE IF MATCH FOUND
        if close_match_full_name:
                if StreamableMatch.objects.filter(match=match):
                    if not match.ace_link:
                        match.ace_link = True
                        match.save()
                        update += 1
                    ignore += 1
                else:
                    streamable_game = StreamableMatch()
                    streamable_game.match = match
                    scanned_match = ScannedMatch.objects.get(id=streamable_matches.get(match=close_match_full_name[0])['id'])
                    streamable_game.scanned_match = scanned_match
                    streamable_game.save()
                    match.ace_link = True
                    match.save()
                    insert += 1
    return {
        'insert': str(insert),
        'update': str(update),
        'ignore': str(ignore)
    }