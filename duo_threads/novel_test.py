import requests
import re
import os, random
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
proxies_list = [
    {'http': '163.204.240.171:9999'},
    {'http': '171.35.223.236:9999'},
    {'http': '113.124.94.51:9999'},
    {'http': '218.76.35.18:10006'},
    {'http': '113.194.48.61:9999'},
    {'http': '182.34.37.61:9999'},
    {'http': '171.11.29.134:9999'},
    {'http': '1.197.204.65:9999'}
]
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#                   '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# }
# headers = {'User-Agent': random.choice(User_Agent)}
chapter_content = []
chapter_data = {}
lock = Lock()


def create_file():
    file = '/home/shijiuyi/Desktop/other_crawl/crawl_noval/{}'.format("斗罗大陆IV终极斗罗")
    if not os.path.exists(file):
        os.mkdir(file)


def get_info():
    for number in range(14, 41):
        url = 'https://m.52bqg.net/chapters_121650/{}'.format(number)
        # print(url)
        headers = {'User-Agent': random.choice(User_Agent),
                   'Cookies': 'Hm_lvt_cec763d47d2d30d431932e526b7f1218=1594362719; __gads=ID=4df6536937052c1c-22ab82b07cc200e2:T=1594781896:RT=1594781896:S=ALNI_MYJk79YmPaOVzs4GRjEjBoEW1E-eg; Hm_lpvt_cec763d47d2d30d431932e526b7f1218=1595314430'}
        proxies = random.choice(proxies_list)
        res = requests.get(url, headers=headers, proxies=proxies)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        res = res.text
        # print(res)

        soup = BeautifulSoup(res, 'html.parser')
        # print(soup)
        url_content = soup.find('div', id="alllist")
        # print(url_content)
        # print(type(url_content))
        url_content = str(url_content)  # soup获得的数据类型不是re解析的类型，需要先转换
        href_link = re.findall('<a href="(.*?)">(.*?)</a>', url_content)
        # print(href_link)
        for i in href_link[1:31]:
            url_link = i[0]
            # print(url_link)
            # 拼接完整url地址
            url_link = 'https://m.52bqg.net' + url_link
            # print(url_link)
            # with open('chapter_url.txt', 'a') as f:
            #     f.write(url_link+'\n')
            chapter_name = i[1]
            # chapter_data[chapter_name] = [url_link]
            headers = {'User-Agent': random.choice(User_Agent),
                       'Cookie': 'Hm_lvt_cec763d47d2d30d431932e526b7f1218=1594362719; '
                                 '__gads=ID=4df6536937052c1c-22ab82b07cc200e2:T=1594781896:'
                                 'RT=1594781896:S=ALNI_MYJk79YmPaOVzs4GRjEjBoEW1E-eg; '
                                 'Hm_lpvt_cec763d47d2d30d431932e526b7f1218=1595301559'}
            proxies = random.choice(proxies_list)
            res = requests.get(url_link, headers=headers, proxies=proxies)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            res = res.text

            soup = BeautifulSoup(res, 'html.parser')
            content = soup.find('div', id="nr1").get_text()
            # print(content)
            # chapter_content.append(content)
            # print(chapter_content)
            file = '/home/shijiuyi/Desktop/other_crawl/crawl_noval/斗罗大陆IV终极斗罗/{}'.format(chapter_name) + '.txt'
            if not os.path.exists(file):
                os.mknod(file)
                print('success create file')
            with open(file, 'w') as f:
                f.write(content)
                print('success write file: {}'.format(chapter_name))
            time.sleep(random.randrange(2, 5))
        time.sleep(random.randint(1, 5))

    # for title, url1 in chapter_data.items():
    #     print(title)
    #     # print(url1)
    #     url = url1[0]
    #     # print(url)
    #     headers = {'User-Agent': random.choice(User_Agent)}
    #     proxies = random.choice(proxies_list)
    #     res = requests.get(url, headers=headers, proxies=proxies, stream=True)
    #     res.raise_for_status()
    #     res.encoding = res.apparent_encoding
    #     res = res.text
    #
    #     soup = BeautifulSoup(res, 'html.parser')
    #     content = soup.find('div', id="nr1").get_text()
    #     # print(content)
    #     chapter_content.append(content)
    #     # print(chapter_content)
    #     file = '/home/shijiuyi/Desktop/other_crawl/crawl_noval/斗罗大陆IV终极斗罗/{}'.format(title) + '.txt'
    #     if not os.path.exists(file):
    #         os.mknod(file)
    #         print('success create file')
    #     with open(file, 'w') as f:
    #         f.write(content)
    #         print('success write file')
    #     time.sleep(random.randrange(2, 5))

#
# def main():
#     p = Pool(4)
#     p.apply(func=get_info)
#     p.close()
#     p.join()


if __name__ == '__main__':
    p = Pool(4)
    p.apply_async(get_info)
    p.close()
    p.join()
    print('success')
