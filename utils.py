# External libraries
import ast
import requests

# Models
from lineups.models import Lineup
from logs.models import RequestLogs
from teams.models import Team


##########################
# View Helper Functions #
##########################

# Returns team information with their logos
def team_info(team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return {}
    else:
        return {
            "name": team.short_name,
            "logo_96x96": str(team.get_logo_url(96)),
            "logo_48x48": str(team.get_logo_url(48))
        }


# Returns lineup information for a match
def lineup_info(match_id, home):
    lineup_available = False
    goalkeeper = []
    defense = []
    midfield = []
    attack = []
    if home:
        lineup = Lineup.objects.get_home_lineup(match_id=match_id)
    else:
        lineup = Lineup.objects.get_away_lineup(match_id=match_id)

    if lineup:
        lineup_available = True
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
        "lineupAvailable": lineup_available,
        "players": {
            "goalkeeper": goalkeeper,
            "defense": defense,
            "midfield": midfield,
            "attack": attack
        }
    }


# Group AceStreams by streamers
# Parameter: QuerySet of links
# Returns: Object
# {
#   "streamerName": "streamerName",
#   "links": ["link1", "link2"]
# }
def group_by_streamer(arr):
    streamers = {}
    for i in arr:
        current_streamer = i['streamer']
        if current_streamer not in streamers:
            links = [i['link']]
            streamers[current_streamer] = links
        else:
            streamers[current_streamer].append(i['link'])
    return streamers


#####################################
#  Template Tag Helper functions  #
#####################################

# Returns class name from an array based on a value
def link_class_classifier(value, classes):
    if value > 0:
        ret_val = classes[0]
    elif value < 0:
        ret_val = classes[1]
    else:
        ret_val = classes[2]

    return ret_val


##################################
# API - Request Helper functions #
##################################

def make_request(url, header, _type="json"):
    count = 0
    ret_val = {}

    r = requests.get(url, headers=ast.literal_eval(header))

    while r.status_code != 200:
        r = requests.get(url, headers=ast.literal_eval(header))
        if count >= 10:
            ret_val['status'] = 'FAILED'
            ret_val['message'] = 'Exceeded the max number of tries.'
            return ret_val
        count += 1

    ret_val['status'] = 'SUCCESS'
    ret_val['message'] = 'Connection Successful.'
    if _type == 'json':
        ret_val['data'] = r.json()
    else:
        ret_val['data'] = r.text

    # Log the request call
    log = RequestLogs()
    log.endPoint = url
    log.httpStatusCode = r.status_code
    log.exception = str(r.raise_for_status())
    log.requestContent = r.url
    log.responseContent = ret_val['data']
    log.save()

    return ret_val


###########################
# Miscellaneous functions #
###########################

# Function to retrieve "html" word count from a url
def count_words_at_url(url):
    r = requests.get(url)
    return (
        len(r.text.split())
    )


# Check if the Incoming request is from a mobile device
def is_mobile(request):
    return (
            request.user_agent.is_mobile or request.user_agent.is_tablet
    )


# Returns a formatted capitalized string. Example: IN_PLAY -> In Play
def sanitize_string(string, delimiter=None):
    sanitized_string = ""
    if string is not None:
        if delimiter is None:
            sanitized_string = string.capitalize()
        else:
            words = string.split(delimiter)
            capitalized_words = []
            for word in words:
                capitalized_words.append(word.capitalize())
            sanitized_string = " ".join(capitalized_words)

    return sanitized_string
