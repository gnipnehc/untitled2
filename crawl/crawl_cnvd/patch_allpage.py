import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import os
import random
import dload
import json
from googletrans import Translator
from lxml import html

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
item = {}
url_list = []


def get_patch_page():
    print('start to get patch url '+'-'*20)
    for number in range(0, 7):
        num = number * 20
        page_url = 'https://www.cnvd.org.cn/patchInfo/list?max=20&offset={}'.format(num)
        res = requests.get(url=page_url, headers=headers).content
        soup = BeautifulSoup(res, 'html.parser')
        patch_content = soup.find('div', id="patchList")
        patch_tbody = patch_content.find('tbody')
        patch_tr = patch_tbody.find_all('tr')
        patch_links = re.findall('<a href="(.*?)">', str(patch_tr))
        for link in patch_links:
            patch_url = 'https://www.cnvd.org.cn'+link
            url_list.append(patch_url)
        time.sleep(1)
    print('get patch url length {}'.format(len(url_list)))


def get_patch_one(url):
    res = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(res, 'html.parser')
    patch_title = soup.find('h1')
    item['patch_title'] = patch_title.text
    patch_tbody = soup.find('tbody')
    patch_tr = patch_tbody.find_all('tr')
    # print(len(patch_tr))
    if len(patch_tr) == 8:
        cnvd_id = ''.join(patch_tr[0].text.replace('所属漏洞编号', '').split())
        item['cnvd_id'] = cnvd_id
        cnvd_url = re.findall('<a href="(.*?)">', str(patch_tr[0]))
        item['cnvd_url'] = 'https://www.cnvd.org.cn'+cnvd_url[0]
        patch_link = re.findall('<a href="(.*?)">', str(patch_tr[1]))
        item['patch_link'] = patch_link[0]
        patch_description = ''.join(patch_tr[3].text.replace('补丁描述', '').split())
        item['patch_description'] = patch_description
        patch_attach = ''.join(patch_tr[4].text.replace('补丁附件', '').replace('(', '').replace(')', '').split())
        item['patch_attach'] = patch_attach
        patch_status = ''.join(patch_tr[5].text.replace('补丁状态', '').replace('(', '').replace(')', '').split())
        item['patch_status'] = patch_status
    # print(item)
    return item


def write_file():
    file_dir = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd/patch_info/'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    file = file_dir+item['cnvd_id']+'.json'
    with open(file, 'w') as fw:
        json_info = json.dumps(item, indent=4, ensure_ascii=False)
        fw.write(json_info)
        print('success {}: {}'.format(count, item['cnvd_id']))


if __name__ == '__main__':
    get_patch_page()
    count = 1
    for url in url_list:
        file = 'before_file/before_cnvd_url.txt'
        if not os.path.exists(file):
            os.mknod(file)
        fr = open(file, 'r').readline()
        if url != fr:
            get_patch_one(url)
            write_file()
            count += 1
            time.sleep(1)
        else:
            break
    with open('before_file/before_cnvd_url.txt', 'w') as f:
        f.write(url_list[0])
    # print(len(url_list))
