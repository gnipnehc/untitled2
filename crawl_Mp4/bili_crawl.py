import requests, parsel
import os, time, random, json
from bs4 import BeautifulSoup
import re


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
headers = {'User-Agent': random.choice(User_Agent)}
url = 'https://www.bilibili.com/v/music/mv/?spm_id_from=333.5.b_7375626e6176.7#/614097'
'https://www.bilibili.com/v/music/?spm_id_from=333.6.b_7375626e6176.1'
'https://www.bilibili.com/v/music/mv/?spm_id_from=333.5.b_7375626e6176.7#/'
'https://www.bilibili.com/v/music/mv/?spm_id_from=333.5.b_7375626e6176.7#/614097'
'https://www.bilibili.com/video/BV1NT4y1E7cC'
params = {
    'page_size': 10,
    'next_offset': str('num'),
    'tag': '今日热门',
    'platform': 'pc'
}


def get_data():
    res = requests.get(url=url, headers=headers, params=params)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.text
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find('div', class_="video-floor-m")
    title = info.find('span', class_="name").text
    print(title)
    data = info.find_all('div', class_="v-list")
    print(data)

    # sel = parsel.Selector(html)
    # data_css = sel.css('#app > div > div.sub-channel-m > div:nth-child(2) > div.l-con > div.video-floor-m > div.storey-box.clearfix > div > div:nth-child(1)')
    # print(data_css)


if __name__ == '__main__':
    get_data()
