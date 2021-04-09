import requests
import parsel
import csv
import threading

f = open('data_1.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=['标题', '薪资', '城市',
                                           '学历', '工作经验', '公司名字',
                                           '融资情况', '公司福利', '招聘时间',
                                           '简历反馈时间'
                                           ])
csv_writer.writeheader()





def main(page):
    url = 'https://www.liepin.com/zhaopin/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

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
        csv_writer.writerow(dit)

if __name__ == '__main__':
    for page in range(0, 10):
        main_thread = threading.Thread(target=main, args=(page,))
        main_thread.start()
