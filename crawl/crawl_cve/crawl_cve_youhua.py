import requests
from bs4 import BeautifulSoup
import re, time, os, random
import dload

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
proxies = {
    "http": "http://193.111.30.83:58891"
}
name_list = []


def get_cve_name(url):
    """
    get cve name info
    :return:
    """
    res = requests.get(url=url, headers=headers, proxies=proxies, timeout=60)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.content.decode('utf-8')

    date = re.findall('date: (.*?)<BR>', html)[0]
    print("date: "+date)

    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find_all('a')
    # print(info)
    print(len(info))
    for i in info:
        name = i.text
        name_list.append(name)
    return date


def download_cve_json(date):
    """
    download cve json file
    :return:
    """
    count = 0
    for name in name_list:
        file = 'file_use/{}.txt'.format(date)
        if not os.path.exists(file):
            os.mknod(file)
        with open(file, 'a') as fa:
            fa.write(name+'\n')
        # 重组url
        s_name = name.split('-')
        year = s_name[0]
        number = s_name[1]
        s_number = number[:-3]
        # 分割数字，重组所需的数据
        t_number = s_number + 'xxx'
        # print(t_number)
        url1 = 'https://raw.githubusercontent.com/CVEProject/cvelist/master/'
        t_url = url1 + year + '/' + t_number + '/CVE-' + name + '.json'
        # print(t_url)
        # list_href.append(t_url)
        # 创建文件夹并下载到文件夹
        file1 = '/home/shijiuyi/Desktop/other_crawl/crawl_cve/cve-json/{}'.format(date)
        # print(file)
        if not os.path.exists(file1):
            os.mkdir(file1)
        j_file = file1 + '/{}.json'.format(name)
        try:
            dload.save(t_url, j_file)
        except:
            try:
                dload.save(t_url, j_file)
            except:
                with open('file_use/{}-name.txt', 'a') as f:
                    f.write(name+'\n')
        count += 1
        print('download json success: {} {}'.format(name, count))
        time.sleep(1)


if __name__ == '__main__':
    url = 'https://cassandra.cerias.purdue.edu/CVE_changes/today.html'
    date = get_cve_name(url)
    download_cve_json(date)
