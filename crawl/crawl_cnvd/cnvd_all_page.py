import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import os
import shutil
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


def get_all_page():
    for number in range(0, 6):
        # num=0为首页，num=20为第二页, num=40为第三页，以此类推
        num = 20*number
        page_url = 'https://www.cnvd.org.cn/flaw/list.htm?flag=true&number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&field=&order=&max=20&offset={}'.format(num)
        req = requests.post(url=page_url, headers=headers).content
        soup = BeautifulSoup(req, 'html.parser')
        tbody = soup.find('tbody')
        cnvd_links = re.findall('<a href="(.*?)" .*?>', str(tbody))
        for link in cnvd_links:
            cnvd_url = 'https://www.cnvd.org.cn'+link
            url_list.append(cnvd_url)
        time.sleep(1)


def get_one_info(url):
    req = requests.get(url=url, headers=headers).content

    soup = BeautifulSoup(req, 'html.parser')
    title_name = soup.find('h1').text
    # print(title_name)
    item['title'] = title_name

    body = soup.find('tbody')
    tr = body.find_all('tr')
    # print(tr)
    cnvd_id = tr[0].text.replace('CNVD-ID', '').strip()
    item['cnvd_id'] = cnvd_id
    public_date = tr[1].text.replace('公开日期', '').strip()
    item['public_date'] = public_date

    d_con = re.findall('>(.*?)</a>', str(tr[2]))
    level = ''.join(tr[2].text.replace('危害级别', '').replace(d_con[0], '').replace('(', '').replace(')', '').split())
    item['danger_level'] = level

    level_content = soup.find('div', id="showDiv")
    level_tbody = level_content.find('tbody')
    td = level_tbody.find_all('td')
    item['attack_method'] = ''.join(td[0].text.replace('攻击途径：', '').split())
    item['attack_level'] = ''.join(td[1].text.replace('攻击复杂度：', '').split())
    item['certification'] = ''.join(td[2].text.replace('认证：', '').split())
    item['confidentiality'] = ''.join(td[3].text.replace('机密性：', '').split())
    item['completeness'] = ''.join(td[4].text.replace('完整性：', '').split())
    item['availability'] = ''.join(td[5].text.replace('可用性：', '').split())
    vul_score = re.findall('<div style="text-align: center;font-size: 19px;">(.*?)</div>', str(level_content))
    item['vul_score'] = vul_score[0].replace('漏洞评分 ：', '').strip()

    affect_all = re.findall('(.*?)<br/>', str(tr[3]))
    affect_list = []
    for a_info in affect_all:
        affect = ''.join(a_info.replace('\t', ''))
        affect_list.append(affect)
    item['affect'] = affect_list

    for content in tr:
        cve_id = re.findall('>CVE ID<', str(content))
        if len(cve_id) > 0:
            cve_id = re.findall('>(.*?)</a>', str(content))
            item['cve_id'] = cve_id[0].strip()
            cve_url = re.findall('<a href="(.*?)" .*?>', str(content))
            item['cve_url'] = cve_url[0].strip()
            break
        else:
            item['cve_id'] = 'null'
            item['cve_url'] = 'null'

    descrip = ''.join(tr[len(tr)-11].text.replace('漏洞描述', '').split())
    item['description'] = descrip
    vul_type = ''.join(tr[len(tr)-10].text.replace('漏洞类型', '').split())
    item['vul_type'] = vul_type

    refer_list = []
    referlink = re.findall('<a href="(.*?)">', str(tr[len(tr)-9]))
    for i in range(len(referlink)):
        refer_list.append(referlink[i].replace('\r', '').strip())
    item['referlinks'] = refer_list

    solveway = ' '.join(tr[len(tr)-8].text.replace('漏洞解决方案', '').split())
    item['solve_way'] = solveway
    patch_title = ''.join(tr[len(tr)-7].text.replace('厂商补丁', '').replace('(', '').replace(')', '').split())
    item['patch_title'] = patch_title
    patch_url_list = re.findall('<a href="(.*?)">', str(tr[len(tr)-7]))
    if len(patch_url_list) > 0:
        patch_url = 'https://www.cnvd.org.cn'+patch_url_list[0]
        item['patch_url'] = patch_url
    if len(patch_url_list) == 0:
        item['patch_url'] = 'null'
    # res = requests.get(url=patch_url, headers=headers).content
    # soup2 = BeautifulSoup(res, 'html.parser')
    # patch_tbody = soup2.find('tbody')
    # patch_tr = patch_tbody.find_all('tr')
    # if len(patch_tr) == 8:
    #     patch_link = re.findall('<a href="(.*?)">', str(patch_tr[1]))
    #     item['patch_link'] = patch_link[0]
    #     patch_description = ''.join(patch_tr[3].text.replace('补丁描述', '').split())
    #     item['patch_description'] = patch_description
    #     patch_attach = ''.join(patch_tr[4].text.replace('补丁附件', '').replace('(', '').replace(')', '').split())
    #     item['patch_attach'] = patch_attach
    #     patch_status = ''.join(patch_tr[5].text.replace('补丁状态', '').replace('(', '').replace(')', '').split())
    #     item['patch_status'] = patch_status

    is_verify = ''.join(tr[len(tr)-6].text.replace('验证信息', '').replace('(', '').replace(')', '').split())
    item['is_verify'] = is_verify
    report_time = ''.join(tr[len(tr)-5].text.replace('报送时间', '').split())
    item['report_time'] = report_time
    collect_time = ''.join(tr[len(tr)-4].text.replace('收录时间', '').split())
    item['collect_time'] = collect_time
    update_time = ''.join(tr[len(tr)-3].text.replace('更新时间', '').split())
    item['update_time'] = update_time
    vul_attach = ''.join(tr[len(tr)-2].text.replace('漏洞附件', '').replace('(', '').replace(')', '').split())
    item['vul_attach'] = vul_attach
    # print(item)


def write_file():
    if not os.path.exists(file):
        os.mkdir(file)
    json_name = file+item['cnvd_id']+'.json'
    if not os.path.exists(json_name):
        os.mknod(json_name)
    with open(json_name, 'w') as fw:
        json_content = json.dumps(item, indent=4, ensure_ascii=False)
        fw.write(json_content)


if __name__ == '__main__':
    get_all_page()
    count = 1
    file = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd/all_page_info/'
    shutil.rmtree(file)
    time.sleep(2)
    for url in url_list:
        before_file = 'before_cnvd_url.txt'
        if not os.path.exists(before_file):
            os.mknod(before_file)
        fr = open('before_cnvd_url.txt', 'r').readline()
        if url != fr:
            get_one_info(url)
            write_file()
            print('success {}: {}'.format(count, item['cnvd_id']))
            count += 1
            time.sleep(1)
        else:
            print('today cnvd update had get')
            break
    with open('before_cnvd_url.txt', 'w') as f:
        f.write(url_list[0])
        f.close()
