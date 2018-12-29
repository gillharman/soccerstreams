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