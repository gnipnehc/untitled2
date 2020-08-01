import requests
import re, time
import requests_html
import execjs, random, os
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
headers = {'User-Agent': random.choice(User_Agent)}
url = 'https://www.cnvd.org.cn/flaw/list.htm'


def get_data():
    res = requests.get(url=url, headers=headers)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.text
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('tbody')
    info = data.find_all('a')
    # print(info)
    for items in info:
        t_url = items['href']
        # print(t_url)
        u_url = 'https://www.cnvd.org.cn'+t_url
        req = requests.get(url=u_url, headers=headers)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        html1 = req.text

        soup = BeautifulSoup(html1, 'html.parser')
        title_name = soup.find('h1').text
        # print(title_name)
        file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/{}'.format(title_name) + '.txt'
        if not os.path.exists(file):
            os.mknod(file)
        data1 = soup.find('tbody')
        tr = data1.find_all('tr')

        # print(tr[1])
        for i in range(0, 14):
            info = tr[i]
            info1 = list(info)
            # print(info1)
            title = info1[1].text
            # print(title)
            content = info1[3].text.strip()
            # print(content)

            with open(file, 'a+') as f:
                f.write(title + ': ' + content + '\n')
        with open(file, 'a+') as f:
            parser = tr[14].text.strip()
            # print(parser)
            f.write(str(parser) + '\n')
            print('success')


if __name__ == '__main__':
    get_data()
