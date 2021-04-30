from pathlib import Path

import requests
import parsel
import csv
import threading
import pprint

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

mulus = []


def xiaoshuo_mulu():
    url = 'http://jandan.net/ooxx/'
    response = requests.get(url=url, headers=headers)

    selector = parsel.Selector(response.text)

    dd_list = selector.xpath('//*[@id="comments"]/ol/li')

    global mulus
    mulus = []
    for dd_item in dd_list:
        # 通过xpath获取链接
        href_item = dd_item.xpath('./div/div/div[2]/p/img/@src').get()
        pprint.pprint(href_item)
        if href_item is None:
            continue

        # 通过css
        # href_item1 = dd_item.css('a::attr(href)').get()
        # pprint.pprint(href_item1)

        mulus.append(href_item)

        pass
    # 通过set进行去重并排序
    list(set(mulus)).sort()
    pprint.pprint(mulus)
    pass


def download(url):
    '''下载'''

    # 创建目录
    img_path = Path("D:\\python\\demo\\电脑壁纸\\img")
    img_path.mkdir(parents=True, exist_ok=True)
    # 拼接
    path = img_path / '{}.jpg'.format("test_name111")

    by_data = requests.get(url='http:' + url, headers=headers).content
    with open(path, 'wb') as f1:
        f1.write(by_data)
    print('%s 成功' % path)


if __name__ == '__main__':
    xiaoshuo_mulu()
    # xiaoshuo_neirong(0)
    download(mulus[0], )
    # for page in range(0, 10):
    #     main_thread = threading.Thread(target=main, args=(page,))
    #     main_thread.start()
