def isMobile(request):
    return request.user_agent.is_mobile or request.user_agent.is_tablet

def groupByStreamer(arr):
    streamers = {}
    for i in arr:
        currentStreamer = i['streamer']
        if currentStreamer not in streamers:
            links = []
            links.append(i['link'])
            streamers[currentStreamer] = links
        else:
            streamers[currentStreamer].append(i['link'])
    return streamers

def link_class_classifier(value, classes):
    if value > 0:
        retVal = classes[0]
    elif value < 0:
        retVal = classes[1]
    else:
        retVal = classes[2]

    return retVal