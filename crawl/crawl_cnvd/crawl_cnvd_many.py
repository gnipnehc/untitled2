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
url1 = 'https://www.cnvd.org.cn/flaw/list.htm?flag=%5BLjava.lang.String%3B%402ce70e91&number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&field=&order=&max=20&offset=20'
num = 0
number = 0
list_title = []
list_href = []


def get_data(num):
    url = 'https://www.cnvd.org.cn/flaw/list.htm?' \
          'flag=%5BLjava.lang.String%3B%402ce70e91&' \
          'number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&' \
          'startDate=&endDate=&field=&order=&max=20&offset={}'.format(num)
    res = requests.post(url=url, headers=headers)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.text
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('tbody')
    info = data.find_all('a')
    # print(info)
    for items in range(len(info)):
        content = str(info[items])
        tit_href = re.findall('<a href="(.*?)" title="(.*?)">', content)
        # print(tit_href)
        title = tit_href[0][1]
        list_title.append(title)
        # print(title)
        href = tit_href[0][0]
        list_href.append(href)
        # print(info[items])


def get_content():
    # print(list_href)
    global number
    for items in range(len(list_href)):
        url = 'https://www.cnvd.org.cn'+list_href[items]
        # print(url)
        req = requests.get(url=url, headers=headers)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')
        title_name = soup.find('h1').text
        # print(title_name)
        file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/cnvd_2020-07/{}'.format(title_name) + '.txt'
        if not os.path.exists(file):
            os.mknod(file)
        else:
            break
        tbody = soup.find('tbody')
        all_tr = tbody.find_all('tr')
        # print(len(all_tr))
        # print(all_tr[0])

        for i in range(len(all_tr) - 1):
            info = all_tr[i]
            info1 = list(info)
            # print(info1)
            title = info1[1].text
            # print(title)
            content = info1[3].text.strip()
            # print(content)
            # print(title + ': ' + content + '\n')

            with open(file, 'a+') as f:
                f.write(title + ': ' + content + '\n')
        with open(file, 'a+') as f:
            parser = all_tr[len(all_tr) - 1].text.strip()
            # print(parser)
            f.write(str(parser) + '\n')
            number += 1
            print('success: '+title_name.split(')')[0])
        time.sleep(2)


if __name__ == '__main__':
    for i in range(14, 83):
        num += 20
        get_data(num)
        time.sleep(1)
    get_content()
    print(number)
