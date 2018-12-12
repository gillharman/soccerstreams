import requests
from games.models import Logs

import ast

request_headers = {
    "reddit": "{'user_agent': 'laptop:soccerStreams:v 0.1 (by/u/gillhimmy)'}",
    "football-api": "{'x-auth-token': '335ffd5c439f4d3ea4f5ade02de7b207'}"
}

def make_request(url, header):
    r = requests.get(url, headers=ast.literal_eval(header))

    while r.status_code != 200:
        r = requests.get(url)

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