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
    url = 'http://www.dvdspring.com/b/46834/'
    response = requests.get(url=url, headers=headers)

    selector = parsel.Selector(response.text)

    dd_list = selector.xpath('//*[@id="list"]/dl/dd')
    global mulus
    mulus = []
    for dd_item in dd_list:
        # 通过xpath获取链接
        href_item = dd_item.xpath('.//a/@href').get()
        # pprint.pprint(href_item)
        # 通过css
        # href_item1 = dd_item.css('a::attr(href)').get()
        # pprint.pprint(href_item1)

        mulus.append(href_item)

        pass
    # 通过set进行去重并排序
    list(set(mulus)).sort()
    pprint.pprint(mulus)
    pass


def xiaoshuo_neirong(page):
    url = r'http://www.dvdspring.com{}'.format(mulus[page])
    pprint.pprint(str(page)+" "+url)
    response = requests.get(url=url, headers=headers)

    selector = parsel.Selector(response.text)

    content = selector.css('#content::text') .getall()
    pprint.pprint(content)
    pass


if __name__ == '__main__':
    xiaoshuo_mulu()
    xiaoshuo_neirong(0)
    # for page in range(0, 10):
    #     main_thread = threading.Thread(target=main, args=(page,))
    #     main_thread.start()
