from datetime import date

from bin.helper_scripts.makeRequest import make_request, request_headers

def get_matches(date=date.today()):
    url = "http://api.football-data.org/v2/matches?dateFrom=" + str(date) + "&dateTo=" + str(date)
    request = make_request(url, request_headers["football-api"])
    try:
        data = request['data']
    except KeyError:
        print(request['message'])
        raise
    return data