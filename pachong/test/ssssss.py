import re

import requests
from lxml.html import etree

url_xpath = '//dd/p[1]/a[1]/@href'
title_xpath = '//dd/p[1]/a[1]/@title'
data_xpaht = '//dd/p[2]/text()'
headers = {
    'rpferpr': 'https://sh.zu.fang.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}
rp = requests.get('https://sh.zu.fang.com/', headers=headers)
rp.encoding = rp.apparent_encoding
html = etree.HTML(rp.text)
url = html.xpath(url_xpath)
title = html.xpath(title_xpath)
data = re.findall('<p class="font15 mt12 bold">(.*?)</p>', rp.text, re.S)
mold_lis = []
house_type_lis = []
area_lis = []
for a in data:
    a = re.sub('�O', '平方米', a)
    mold = re.findall('\r\n\s.*?(\S.*?)<span class="splitline">', a)
    house_type_area = re.findall('</span>(.*?)<span class="splitline">', a)
    try:
        mold_lis.append(mold[0])
        house_type_lis.append(house_type_area[0])
        area_lis.append(house_type_area[1])
    except:
        pass

data_zip = zip(title, url, mold_lis, house_type_lis, area_lis)

with open('info.txt', 'a', encoding='utf8') as fa:
    for a in data_zip:
        fa.write(str(a))
        fa.write('\n')
