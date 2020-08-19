# cnnvd大概每天下午5点左右更新
import requests
from bs4 import BeautifulSoup
import re
import time, datetime
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
links = []


def get_info(url):
    res = requests.get(url=url, headers=headers).content.decode('utf-8')

    selector = html.fromstring(res)
    for i in range(0, 10):
        url_list = selector.xpath(f'//*[@id="vulner_{i}"]/p/a/@href')
        t_url = 'http://www.cnnvd.org.cn' + url_list[0]
        # print(t_url)
        links.append(t_url)
    return links


def download_json(number, count):
    file_dir = '/home/shijiuyi/Desktop/other_crawl/crawl_cnnvd/json_cnnvd_oneday'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    file = file_dir+'/'+number+'.json'
    # print(file)
    with open(file, 'w') as fw:
        json_data = json.dumps(item, indent=4, ensure_ascii=False)
        fw.write(json_data)
        print('success {}: {}'.format(count, number))


def get_one_info(one_url):
    res = requests.get(url=one_url, headers=headers)
    xml = res.text

    soup = BeautifulSoup(xml, 'html.parser')
    content = soup.find('div', class_="detail_xq w770")
    title = content.find('h2')
    title = ''.join(title.text.strip())
    item['title'] = title
    info = content.find_all('li')
    # print(len(info))
    cnnvd_id = info[0].text.replace('CNNVD编号：', '').strip()
    item['cnnvd_id'] = cnnvd_id
    # print(cnnvd_id)
    level = info[1].text.replace('危害等级： ', '').strip()
    if len(level) > 0:
        item['level'] = level
    if len(level) == 0:
        item['level'] = 'null'
    cve_id = ''.join(info[2].text.replace('CVE编号：', '').split())
    item['cve_id'] = cve_id
    vul_type = ''.join(info[3].text.replace('漏洞类型：', '').split())
    item['vul_type'] = vul_type
    push_time = ''.join(info[4].text.replace('发布时间：', '').split())
    item['push_time'] = push_time
    update_time = ''.join(info[6].text.replace('更新时间：', '').split())
    item['update_time'] = update_time
    threate = ''.join(info[5].text.replace('威胁类型：', '').split())
    if len(threate) == 0:
        item['threat_type'] = 'null'
    if len(threate) > 0:
        item['threat_type'] = threate
    company = ''.join(info[7].text.replace('厂        商：', '').split())
    if len(company) > 0:
        item['company'] = company
    if len(company) == 0:
        item['company'] = 'null'
    vul_come = ' '.join(info[8].text.replace('漏洞来源：', '').split())
    if len(vul_come) > 0:
        item['vul_come'] = vul_come
    if len(vul_come) == 0:
        item['vul_come'] = 'null'

    desciption = soup.find('div', class_="d_ldjj")
    descrip = ''.join(desciption.text.replace('漏洞简介', '').split())
    item['description'] = descrip

    vul_content = soup.find_all('div', class_="d_ldjj m_t_20")
    gonggao = ' '.join(vul_content[0].text.replace('漏洞公告', '').split())
    item['vul_notice'] = gonggao

    # cankao = ';'.join(vul_content[1].text.replace('参考网址', '').split())
    # item['refer_link'] = cankao
    # # print(item['refer_link'])
    refer_content = vul_content[1]
    referlinks = re.findall('链接:(.*?)<', str(refer_content))
    referlink = refer_content.find_all('p')
    # print(referlink)
    one_refer = referlink[len(referlink)-1].text.replace('链接:', '').strip()
    referlinks.append(one_refer)
    # print(referlinks)
    item['referlinks'] = referlinks

    affect = ''.join(vul_content[2].text.replace('受影响实体', '').replace("更多>>", '').split())
    item['affect'] = affect
    patch_title = ''.join(vul_content[3].text.replace('补丁', '').replace("更多>>", '').split())
    item['patch_title'] = patch_title

    patch_info = vul_content[3]
    patch_href = re.findall('a class="a_title2" href="(.*?)"', str(patch_info))
    time.sleep(1)
    if len(patch_href) > 0:
        patch_link = 'http://www.cnnvd.org.cn' + patch_href[0]
        req = requests.get(url=patch_link, headers=headers).text
        soup = BeautifulSoup(req, 'html.parser')
        patch_content = soup.find('div', class_="detail_xq w770")
        li = patch_content.find_all('li')
        for k in range(0, len(li)):
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

        # patch_refer = re.findall('href="(.*?)"', str(refer))
        # if len(patch_refer[0]) > 0:
        #     item['patch_refer'] = '来源：'+patch_refer[0]
        # if len(patch_refer[0]) == 0:
        #     item['patch_refer'] = 'null'
    if len(patch_href) == 0:
        item['patch_id'] = 'null'
        item['patch_size'] = 'null'
        item['patch_level'] = 'null'
        item['patch_time'] = 'null'
        item['patch_company'] = 'null'
        item['patch_page'] = 'null'
        item['patch_MD5code'] = 'null'
        item['patch_refer'] = 'null'
    # print(item)
    return cnnvd_id


if __name__ == '__main__':
    # # 爬取单页的cnnvd信息，并保存为json格式
    # url = 'http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?pageno=1&repairLd='
    # get_info(url)
    # count = 1
    # for link in links:
    #     number = get_one_info(link)
    #     download_json(number, count)
    #     count += 1

    count = 1
    for j in range(1, 9):
        url = f'http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?pageno={j}&repairLd='
        get_info(url)
        time.sleep(1)
    # print(len(links))
    for link in links:
        fr = open('before_cnnvd_url.txt', 'r').readline()
        if link != fr:
            number = get_one_info(link)
            download_json(number, count)
            count += 1
        else:
            print('today update had get')
            break
    with open('before_cnnvd_url.txt', 'w') as f:
        f.write(links[0])
        f.close()
