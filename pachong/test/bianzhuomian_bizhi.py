import pprint

import parsel
import requests

url = 'http://www.netbian.com/weimei/index.htm'
kw = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    , 'referer': 'https://link.csdn.net/?target=http%3A%2F%2Fwww.netbian.com%2Fweimei%2Findex.htm'

}

try:
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, headers=kw )
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    selector = parsel.Selector(r.text)

    list=selector.css("#main > div.list").xpath("//ul/li").xpath(".//a/img/@src").getall()

    pprint.pprint(list)
except Exception as err:
    print(err)
    print("========")