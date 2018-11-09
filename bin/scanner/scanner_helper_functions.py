import requests
from games.models import Logs


def make_request(url):
    r = requests.get(url, headers={"user_agent": "laptop:soccerStreams:v 0.1 (by/u/gillhimmy)"})
    #print('Connecting...')
    while r.status_code != 200:
        # sleep(1)  # Wait a second to make another request
        r = requests.get(url, headers={"user_agent": "laptop:soccerStreams:v 0.1 (by/u/gillhimmy)"})

    data = r.json()

    #Log the request call
    log = Logs()
    log.endPoint = url
    log.httpStatusCode = r.status_code
    log.exception = str(r.raise_for_status())
    log.requestContent = r.url
    log.responseContent = data
    log.save()

    return data