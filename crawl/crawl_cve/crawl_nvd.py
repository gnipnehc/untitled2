import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random
import dload
import json
from googletrans import Translator
import datetime


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
today = datetime.date.today()
oneday = datetime.timedelta(days=1)
yesterday = today - oneday
date = yesterday


def get_all_info():
    fd = open('file_use/{}.txt'.format(date), 'r').readlines()
    for i in range(len(fd)):
        name = fd[i].strip('\n')
        # print(name)
        url = 'https://nvd.nist.gov/vuln/detail/CVE-{}'.format(name)
        # print(url)
        # with open('file_use/2020-08-10-url.txt', 'a') as file:
            # file.write(url+'\n')
        # print('success')
        try:
            item = get_info(url)
            file_dir = '/home/shijiuyi/Desktop/other_crawl/crawl_cve/cve-json/{}'.format(date)
            file = file_dir+'/{}'.format(name)+'.json'
            if os.path.exists(file):
                f = open(file, 'r')
                f_dict = json.load(f)
                f_dict.update(item)
                file_new = file_dir+'-new'
                if not os.path.exists(file_new):
                    os.mkdir(file_new)
                json_file = file_new+'/{}'.format(name)+'.json'
                with open(json_file, 'w') as fr:
                    new_josn = json.dumps(f_dict, indent=4, ensure_ascii=False)
                    fr.write(new_josn)
                    print('success writer {}'.format(name))
            time.sleep(1)
        except:
            print(url)
            try:
                item = get_info(url)
                file_dir = '/home/shijiuyi/Desktop/other_crawl/crawl_cve/cve-json/{}'.format(date)
                file = file_dir + '/{}'.format(name) + '.json'
                if os.path.exists(file):
                    f = open(file, 'r')
                    f_dict = json.load(f)
                    f_dict.update(item)
                    file_new = file_dir + '-new'
                    if not os.path.exists(file_new):
                        os.mkdir(file_new)
                    json_file = file_new + '/{}'.format(name) + '.json'
                    with open(json_file, 'w') as fr:
                        new_josn = json.dumps(f_dict, indent=4, ensure_ascii=False)
                        fr.write(new_josn)
                        print('success writer {}'.format(name))
                time.sleep(1)
            except:
                print(url)
                try:
                    item = get_info(url)
                    file_dir = '/home/shijiuyi/Desktop/other_crawl/crawl_cve/cve-json/{}'.format(date)
                    file = file_dir + '/{}'.format(name) + '.json'
                    if os.path.exists(file):
                        f = open(file, 'r')
                        f_dict = json.load(f)
                        f_dict.update(item)
                        file_new = file_dir + '-new'
                        if not os.path.exists(file_new):
                            os.mkdir(file_new)
                        json_file = file_new + '/{}'.format(name) + '.json'
                        with open(json_file, 'w') as fr:
                            new_josn = json.dumps(f_dict, indent=4, ensure_ascii=False)
                            fr.write(new_josn)
                            print('success writer {}'.format(name))
                    time.sleep(1)
                except:
                    print(url)
                    info = url.split('/')
                    number = info[-1][4:]
                    with open('file_use/{}-error.txt'.format(date), 'a') as file:
                        file.write(number+'\n')


def get_info(url):
    res = requests.get(url=url, headers=headers, proxies=proxies, timeout=50)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.content.decode('utf-8')
    # print(type(html))

    item = {}
    soup = BeautifulSoup(html, 'html.parser')
    translator = Translator(service_urls=['translate.google.cn'])

    modified = re.findall('<p data-testid="vuln-warning-banner-content">(.*?)</p>', html)
    if len(modified) > 0:
        modify = translator.translate(modified[0], dest='zh-CN').text
        item['modified'] = modify
    if len(modified) == 0:
        item['modified'] = 'null'

    description = re.findall('<p data-testid="vuln-description">(.*?)</p>', html)
    descript = translator.translate(description[0], dest='zh-CN').text
    item['descrip'] = descript

    nist = re.findall('panel-source">(.*?)<', html)
    k = len(nist)
    try:
        code = re.findall('class="label label.*?>(.*?)<', html)
        for i in range(0, len(nist)):
            item[nist[k - i - 1]] = code[k - i - 1]
    except:
        code = re.findall('>(.*?)</a></span></span>', html)
        for i in range(0, len(nist)):
            item[nist[k-i-1]] = code[k-i-1]

    hyperlinks = soup.find('div', id="vulnHyperlinksPanel")
    tbody = hyperlinks.find('tbody')
    a_href = tbody.find_all('a')
    href_list = []
    links = {}
    link = re.findall('<a href="(.*?)" .*?>', str(a_href))
    for li in link:
        links['link'] = li
        href_list.append(links)
    # print(href_list)
    item['links'] = str(href_list).replace('[', '').replace(']', '')

    hyperlinks = soup.find('div', id="vulnHyperlinksPanel")
    tbody = hyperlinks.find('tbody')
    td = tbody.find_all('td')
    info_list = []
    for p in range(len(td)):
        resource = {}
        if p % 2 != 0:
            patch = td[p].text.replace('\t', '').replace('\xa0\r', '')
            # print(patch)
            resource['patch'] = patch
            info_list.append(resource)
    item['resource'] = str(info_list).replace('[', '').replace(']', '')

    weakness = soup.find('div', id="vulnTechnicalDetailsDiv")
    table = weakness.find('tbody')
    td = table.find_all('td')
    info_list = []
    for j in td:
        info = j.text.replace('&nbsp;', '').replace('\n', '').replace('\t', '')
        # print(info)
        info_list.append(info.strip())
    for i in range(len(info_list)):
        item['cwe_id'] = info_list[0]
        item['cwe_name'] = info_list[1]
        item['source'] = info_list[2]
    # print(item)
    return item


if __name__ == '__main__':
    get_all_info()
