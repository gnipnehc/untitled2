import requests
import re, os
import requests_html
import execjs, random
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
# 爬取时跟新一下cookies
headers = {'User-Agent': random.choice(User_Agent),
           'Cookie': "__jsluid_s=91ac7f92dfcab0d2a80589a9c16fa2fc; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1596167163; Hm_lpvt_d7682ab43891c68a00de46e9ce5b76aa=1596167212; JSESSIONID=1CDC72AA9B0078D384D3CFA442DD85D4; puk=1e5b39c5fb66ce5eb7f47e7ce06568230f5058b89e5fa8c10f145d012b2816154deb10d7948be8489c8b3020cf6493bbb036aecc1c02db86149bce082d312577dec22c1e8cd65948e441396fe6bf728b78e8dcab9fa310e95764654fa3ac3d62b708ca14068838ba68051290e6b6c7c3842ee2f2d2a573f6e6d2513f530eaffa"}
url = 'https://www.cnvd.org.cn/shareData/list'
list_href = []
list_title = []


def get_data():
    res = requests.get(url=url, headers=headers)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.text
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody')
    a_td = tbody.find_all('a')
    # print(a_td)
    for items in a_td:
        href = items['href']
        title = items.text
        list_title.append(title)
        # print(title)
        # print(href)
        t_url = 'https://www.cnvd.org.cn'+href
        list_href.append(t_url)

        file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/xml_test/{}'.format(title)
        if not os.path.exists(file):
            os.mknod(file)
        req = requests.get(url=t_url, headers=headers)
        req.raise_for_status()
        html = req.content

        with open(file, 'wb') as f:
            f.write(html)
            print('success: '+title)


if __name__ == '__main__':
    get_data()

