import requests
import parsel
import csv
import threading

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}


def xiaoshuo_list():
    url = 'http://www.dvdspring.com/b/46834/'
    response = requests.get(url=url, headers=headers)

    selector = parsel.Selector(response.text)

    dd_list = selector.xpath('//*[@id="list"]/dl/dd')
    print(dd_list)
    results = []
    for dd_item in dd_list:

        href_item = dd_item.css('a@href')
        results.append(href_item)
        print(href_item)
        pass
    list(set(results)).sort()
    print(results)
    pass


def main(page):
    url = 'http://www.dvdspring.com/b/46834/'

    params = {
        'compkind': '',
        'dqs': '',
        'pubTime': '',
        'pageSize': '40',
        'salary': '',
        'compTag': '',
        'sortFlag': '',
        'degradeFlag': '0',
        'compIds': '',
        'subIndustry': '',
        'jobKind': '',
        'industries': '',
        'compscale': '',
        'key': 'python',
        'siTag': 'I-7rQ0e90mv8a37po7dV3Q~fA9rXquZc5IkJpXC-Ycixw',
        'd_sfrom': 'search_fp',
        'd_ckId': 'cd74f9fdbdb63c6d462bad39feddc7f1',
        'd_curPage': '2',
        'd_pageSize': '40',
        'd_headId': 'cd74f9fdbdb63c6d462bad39feddc7f1',
        'curPage': page,
    }

    response = requests.get(url=url, params=params, headers=headers)

    selector = parsel.Selector(response.text)

    lis = selector.css('div.job-content div:nth-child(1) ul li')
    for li in lis:
        title = li.css('.job-info h3 a::text').get().strip()
        money = li.css('.condition span.text-warning::text').get()
        city = li.css('.condition .area::text').get()
        edu = li.css('.condition .edu::text').get()
        experience = li.css('.condition span:nth-child(4)::text').get()
        company = li.css('.company-name a::text').get()
        financing = li.css('.field-financing span::text').get()
        temptation_list = li.css('p.temptation.clearfix span::text').getall()
        temptation_str = '|'.join(temptation_list)
        release_time = li.css('p.time-info.clearfix time::text').get()
        feedback_time = li.css('p.time-info.clearfix span::text').get()
        dit = {
            '标题': title,
            '薪资': money,
            '城市': city,
            '学历': edu,
            '工作经验': experience,
            '公司名字': company,
            '融资情况': financing,
            '公司福利': temptation_str,
            '招聘时间': release_time,
            '简历反馈时间': feedback_time,
        }
        print(dit)


if __name__ == '__main__':
    xiaoshuo_list()
    # for page in range(0, 10):
    #     main_thread = threading.Thread(target=main, args=(page,))
    #     main_thread.start()
