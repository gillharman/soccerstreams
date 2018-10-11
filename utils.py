import requests

def count_words_at_url(url):
    r = requests.get(url)
    return(len(r.text.split()))