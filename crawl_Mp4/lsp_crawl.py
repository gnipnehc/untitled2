import requests
import os, time, random
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
url = 'https://www.pearvideo.com/category_59'
headers = {'User-Agent': random.choice(User_Agent)}


def get_data():
    res = requests.get(url=url, headers=headers)
    res.encoding = res.apparent_encoding
    html = res.text

    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find('ul', id="listvideoListUl")
    info = str(info)
    m_url = re.findall(r'<a [^>]+href="vi(.*?)">', info)
    # m_url = info.find_all('a', attrs={'class': "vervideo-lilink actplay"}, href=True)
    # print(m_url)

    for j_url in m_url:
        req = requests.get(url='https://www.pearvideo.com/vi'+j_url, headers=headers)
        req.encoding = req.apparent_encoding
        t_html = req.content

        soup = BeautifulSoup(t_html, 'html.parser')
        title = soup.find('h1').text
        # print(title)
        data = str(soup)
        srcurl = re.findall('ldUrl="",srcUrl="(.*?)"', data)
        # print(srcurl)

        file = '/home/shijiuyi/Desktop/other_crawl/crawl_mp4/梨视频/'
        if not os.path.exists(file):
            os.mkdir(file)
        m_file = file+title+'.mp4'
        if not os.path.exists(m_file):
            os.mknod(m_file)
        for t_url in srcurl:
            t_res = requests.get(t_url, headers=headers)
            t_res.encoding = t_res.apparent_encoding
            t_data = t_res.content

            with open(m_file, 'wb') as f:
                f.write(t_data)
                print('success write file')


if __name__ == '__main__':
    get_data()
