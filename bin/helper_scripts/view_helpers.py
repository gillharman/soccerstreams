from teams.models import Team
from lineups.models import Lineup

def team_info(team_id):
    team = Team.objects.filter(id=team_id).first()
    if team:
        return {
            "name": team.short_name,
            "logo_96x96": str(team.get_logo_url(96)),
            "logo_48x48": str(team.get_logo_url(48))
        }
    else:
        return {}

def lineup_info(match_id, home):
    lineupAvailable = False
    goalkeeper = []
    defense = []
    midfield = []
    attack = []
    if home:
        lineup = Lineup.objects.get_home_lineup(match_id=match_id)
    else:
        lineup = Lineup.objects.get_away_lineup(match_id=match_id)

    if lineup:
        lineupAvailable = True
        for player in lineup:
            if player.position.startswith('G'):
                goalkeeper.append(player)
            elif player.position.startswith('D'):
                defense.append(player)
            elif player.position.startswith('M'):
                midfield.append(player)
            elif player.position.startswith('F'):
                attack.append(player)

    return {
        "lineupAvailable": lineupAvailable,
        "players": {
            "goalkeeper": goalkeeper,
            "defense": defense,
            "midfield": midfield,
            "attack": attack
        }
    }