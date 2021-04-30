import pprint

import parsel
import requests

url = 'https://unsplash.com/napi/search/photos'
kw = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36 '
    , 'referer': 'https://unsplash.com/s/photos/dog'
}
params = {
    'query': 'dog',
    'per_page': '20',
    'page': '2'
}

try:
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, headers=kw, params=params)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    selector = parsel.Selector(r.text)
    pprint.pprint(r.text)

    pprint.pprint(list)
except Exception as err:
    print(err)
    print("========")
