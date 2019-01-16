from datetime import datetime, date

from bin.helper_scripts.makeRequest import make_request, request_headers

def get_matches(date=date.today()):
    data = {}
    try:
        d = datetime.strftime(date, '%Y-%m-%d')
        url = "http://api.football-data.org/v2/matches?dateFrom=" + d + "&dateTo=" + d
        request = make_request(url, request_headers["football-api"])
        try:
            data = request['data']
        except KeyError:
            print(request['message'])
            raise
    except ValueError:
        raise ValueError('Invalid Date Format')

    return data