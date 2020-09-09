import requests
from bs4 import BeautifulSoup
import re
import time, datetime
import os
import random
import dload
import json
import scrapy
from lxml import html
from multiprocessing import Pool, Queue, Process
from pool_daili.ua_pool import ua

# headers = {'User-Agent': random.choice(ua)}
fr = open('/home/shijiuyi/untitled2/pool_daili/ip.txt', 'r').readlines()
list_ip = []
for i in range(len(fr)):
    ip_addr = fr[i].strip()
    list_ip.append(ip_addr)
patch_url = []
item = {}
patch = {}


def get_patch_all(url):
    proxy = {'http': random.choice(list_ip)}
    headers = {'User-Agent': random.choice(ua)}
    res = requests.get(url=url, headers=headers, proxies=proxy)
    if res.status_code == 200:
        selector = html.fromstring(res.content)
        content = selector.xpath('//*[@class="list_list"]/ul/li/div/a/@href')
        up_time = selector.xpath('//*[@class="list_list"]/ul/li/div[2]/text()')
        patch_id = selector.xpath('//*[@class="list_list"]/ul/li/div[1]/p/a/text()')
        # print(content)
        if patch_id:
            for j in range(0, len(content)):
                p_url = 'http://www.cnnvd.org.cn'+content[j]
                patch['patch_url'] = p_url
                patch['patch_id'] = patch_id[j]
                patch['push_time'] = up_time[j]
                print(f'success get {patch_id[j]} and {up_time[j]}')
                # patch_url.append(p_url)
                with open('patch_cnnvd_url.txt', 'a') as fa:
                    fa.write(p_url+'\n')
                time.sleep(0.5)
                with open('patch_info.json', 'a') as fa:
                    data = json.dumps(patch, indent=4, ensure_ascii=False)
                    fa.write(data + ',' + '\n')
        else:
            with open('patch_queshi.txt', 'a') as f:
                f.write(url+'\n')
    else:
        proxy = {'http': random.choice(list_ip)}
        headers = {'User-Agent': random.choice(ua)}
        res = requests.get(url=url, headers=headers, proxies=proxy)
        if res.status_code == 200:
            selector = html.fromstring(res.content)
            content = selector.xpath('//*[@class="list_list"]/ul/li/div/a/@href')
            up_time = selector.xpath('//*[@class="list_list"]/ul/li/div[2]/text()')
            patch_id = selector.xpath('//*[@class="list_list"]/ul/li/div[1]/p/a/text()')
            # print(content)
            if patch_id:
                for j in range(0, len(content)):
                    p_url = 'http://www.cnnvd.org.cn' + content[j]
                    patch['patch_url'] = p_url
                    patch['patch_id'] = patch_id[j]
                    patch['push_time'] = up_time[j]
                    print(f'success get {patch_id[j]} and {up_time[j]}')
                    # patch_url.append(p_url)
                    with open('patch_cnnvd_url.txt', 'a') as fa:
                        fa.write(p_url + '\n')
                    time.sleep(0.5)
                    with open('patch_info.json', 'a') as fa:
                        data = json.dumps(patch, indent=4, ensure_ascii=False)
                        fa.write(data + ',' + '\n')
            else:
                with open('patch_queshi.txt', 'a') as f:
                    f.write(url+'\n')
        else:
            proxy = {'http': '101.4.136.34:81'}
            headers = {'User-Agent': random.choice(ua)}
            res = requests.get(url=url, headers=headers, proxies=proxy)
            selector = html.fromstring(res.content)
            content = selector.xpath('//*[@class="list_list"]/ul/li/div/a/@href')
            up_time = selector.xpath('//*[@class="list_list"]/ul/li/div[2]/text()')
            patch_id = selector.xpath('//*[@class="list_list"]/ul/li/div[1]/p/a/text()')
            # print(content)
            if patch_id:
                for j in range(0, len(content)):
                    p_url = 'http://www.cnnvd.org.cn' + content[j]
                    patch['patch_url'] = p_url
                    patch['patch_id'] = patch_id[j]
                    patch['push_time'] = up_time[j]
                    print(f'success get {patch_id[j]} and {up_time[j]}')
                    # patch_url.append(p_url)
                    with open('patch_cnnvd_url.txt', 'a') as fa:
                        fa.write(p_url + '\n')
                    time.sleep(0.5)
                    with open('patch_info.json', 'a') as fa:
                        data = json.dumps(patch, indent=4, ensure_ascii=False)
                        fa.write(data + ',' + '\n')
            else:
                with open('patch_queshi.txt', 'a') as f:
                    f.write(url + '\n')
    time.sleep(random.randint(4, 9))


def get_patch_info(url):
    proxy = {'http': random.choice(list_ip)}
    headers = {'User-Agent': random.choice(ua)}
    res = requests.get(url=url, headers=headers, proxies=proxy, timeout=30).content
    soup = BeautifulSoup(res, 'html.parser')
    patch_content = soup.find('div', class_="detail_xq w770")
    li = patch_content.find_all('li')
    # print(len(li))
    for k in range(0, len(li)):
        # print(li[i].text)
        item['patch_id'] = ''.join(li[0].text.replace('补丁编号：', '').split())
        item['patch_size'] = ''.join(li[1].text.replace('补丁大小：', '').split())
        patch_level = ''.join(li[2].text.replace('重要级别：', '').split())
        if len(patch_level) > 0:
            item['patch_level'] = patch_level
        if len(patch_level) == 0:
            item['patch_level'] = 'null'
        item['patch_time'] = ''.join(li[3].text.replace('发布时间：', '').split())
        patch_company = ''.join(li[4].text.replace('厂      商：', '').split())
        if len(patch_company) > 0:
            item['patch_company'] = patch_company
        if len(patch_company) == 0:
            item['patch_company'] = 'null'
        patch_page = ''.join(li[5].text.replace('厂商主页：', '').split())
        if len(patch_page) > 0:
            item['patch_page'] = patch_page
        if len(patch_page) == 0:
            item['patch_page'] = 'null'
        item['patch_MD5code'] = ''.join(li[6].text.replace('MD5验证码：', '').split())
    refer = soup.find('div', class_="d_ldjj")
    refer_content = refer.text
    if len(refer_content) > 0:
        item['patch_refer'] = '; '.join(refer_content.replace('来源：', '').replace('参考网址', '').split())
    if len(refer_content) == 0:
        item['patch_refer'] = 'null'
    time.sleep(random.randint(3, 5))


def main():
    print('start to get patch url')
    with open('patch_info.json', 'a') as f:
        f.write('[')
        f.close()
    pool = Pool(processes=12)
    for j in range(1, 8272):
        url = f'http://www.cnnvd.org.cn/web/cnnvdpatch/querylist.tag?pageno={j}'
        # get_patch_all(url)
        pool.apply_async(get_patch_all, args=(url, ))
    pool.close()
    pool.join()
    with open('patch_info.json', 'a') as f:
        f.write(']')
        f.close()
    print('patch url have get')


if __name__ == '__main__':
    count = 1
    main()
