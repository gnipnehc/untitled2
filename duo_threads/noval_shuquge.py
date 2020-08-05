import requests, parsel
import re
import os, random, json
import time
import threading  # 多线程的前提
from multiprocessing import Process, Pool, Lock, Queue  # 多进程
from bs4 import BeautifulSoup


User_Agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
pxies_list = [
    {'http': '163.204.240.171:9999'},
    {'http': '171.35.223.236:9999'},
    {'http': '113.124.94.51:9999'},
    {'http': '218.76.35.18:10006'},
    {'http': '113.194.48.61:9999'},
    {'http': '182.34.37.61:9999'},
    {'http': '171.11.29.134:9999'},
    {'http': '1.197.204.65:9999'}
]
url_list = []


def get_data():
    url = 'http://www.shuquge.com/txt/8400/index.html'
    # url = 'http://www.baidu.com'
    headers = {'User-Agent': random.choice(User_Agent),
               'Cookie': 'Hm_lvt_3806e321b1f2fd3d61de33e5c1302fa5=1595294839; '
                         'Hm_lpvt_3806e321b1f2fd3d61de33e5c1302fa5=1595296040'}
    # pxies = random.choice(pxies_list)
    req = requests.get(url=url, headers=headers)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    all_data = soup.find('div', class_="listmain")
    all_data = str(all_data)
    chapter = re.findall('<dd><a href="(.*?)">(.*?)</a></dd>', all_data)
    # print(chapter[0])
    # print(len(chapter))

    for url1, title in chapter[14:]:
        # print(url1)
        # print(title)
        chapter_url = 'http://www.shuquge.com/txt/8400/'+url1
        # print(chapter_url)
        res = requests.get(url=chapter_url, headers=headers)
        res.encoding = res.apparent_encoding
        html = res.text
        # print(html)
        sel = parsel.Selector(html)
        content = sel.css('#content::text').getall()
        # print(content)

        time.sleep(random.randrange(1, 2))
        file = '/home/shijiuyi/Desktop/other_crawl/crawl_noval/fanre/'
        if not os.path.exists(file):
            os.mkdir(file)
        u_file = file + '{}'.format(title) + '.txt'
        if not os.path.exists(u_file):
            os.mknod(u_file)
        with open(u_file, 'w') as f:
            for con in content:
                contents = con.strip()+'\n'
                f.write(contents)
            print('success write file: {}'.format(title))


if __name__ == '__main__':
    get_data()
