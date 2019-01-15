import requests
from logs.models import RequestLogs

import ast

request_headers = {
    "reddit": "{'user_agent': 'laptop:soccerStreams:v 0.1 (by/u/gillhimmy)'}",
    "football-api": "{'x-auth-token': '335ffd5c439f4d3ea4f5ade02de7b207'}",
    "rotowire": "{'user_agent': 'pc'}"
}

def make_request(url, header, type="json"):
    count = 0
    retVal = {}

    r = requests.get(url, headers=ast.literal_eval(header))
    while r.status_code != 200:
        # print(r.status_code)
        r = requests.get(url)
        if count >= 10:
            retVal['status'] = 'FAILED'
            retVal['message'] = 'Exceeded the max number of tries.'
            return retVal
        count =+ 1

    retVal['status'] = 'SUCCESS'
    retVal['message'] = 'Connection Successful.'
    if type == 'json':
        retVal['data'] = r.json()
    else:
        retVal['data'] = r.text

    #Log the request call
    log = RequestLogs()
    log.endPoint = url
    log.httpStatusCode = r.status_code
    log.exception = str(r.raise_for_status())
    log.requestContent = r.url
    log.responseContent = retVal['data']
    log.save()

    return retVal