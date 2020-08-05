import requests
import os, time, random
from bs4 import BeautifulSoup
import re
from selenium import webdriver


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
url = 'https://so.tv.sohu.com/list_p11001_p2323_p3323302_p4_p5_p6_p7_p8_p9_p10_p11_p12_p13.html'
headers = {'User-Agent': random.choice(User_Agent)}


def get_data():
    req = requests.get(url=url, headers=headers)
    req.encoding = req.apparent_encoding
    html = req.text
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find('ul', class_="st-list short cfix")
    print(type(info))
    a = info.find_all('a')
    # print(a)
    for i in a:
        href = i['href']
        print(href)
    # for i in info:
    #     href = i['a']
    #     print(href)

    # info = soup.find('div', class_="column-bd wemd cfix")
    # # print(info)
    # data = info.find_all('div', class_="st-pic")
    # # print(data)
    # data = str(data)
    # mp_url = re.findall('<a[^>]+href="(.*?)"+[^>]>', data)  # url通用匹配
    # print(mp_url)


if __name__ == '__main__':
    get_data()
