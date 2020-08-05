import requests
import os
import time
import threading
import urllib.parse as parse

from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from queue import Queue
from bs4 import BeautifulSoup

# 多线程爬取
bookname_list = ['大道争锋']
save_path = '/home/shijiuyi/Desktop/other_crawl/crawl_noval/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
target_url = 'https://m.52bqg.net/'
try:
    os.mkdir(save_path)
except:
    pass


# 定义两个函数获取书的url和章节的url
def get_chapter_content(i):  # 根据章节url返回章节内容
    chapter_now = requests.get(target_url+i, headers)
    chapter_now.encoding = 'gbk'
    chapter_now = chapter_now.text  # 源码
    chapter_now = etree.HTML(chapter_now)
    chapter_content = '\n'.join(chapter_now.xpath('//div[@id="nr1"]/descendant::text()'))
    next_page_num = 1
    while '下一页' in chapter_now.xpath('//div[@class="nr_page"]//td[@class="next"]/descendant::text()'):
        chapter_content = chapter_content.replace('本章未完，点击下一页继续阅读', '')\
            .replace('-->>', '').replace('&n', '')
        next_page_num += 1
        chapter_now = requests.get(target_url+i.replace('.html', '_'+str(next_page_num)+'.html'), headers)
        chapter_now.encoding = 'gbk'
        chapter_now = chapter_now.text

        chapter_now = etree.HTML(chapter_now)
        chapter_content_next = '\n'.join(chapter_now.xpath('//div[@id="nr1"]/descendant::text()'))
        chapter_content_next = chapter_content_next.replace('本章未完，点击下一页继续阅读', '')\
            .replace('-->>', '').replace('&n', '')
        chapter_content = chapter_content + chapter_content_next
    return chapter_content


def get_chapter_link(i):  # 确定章节的数目,爬取所有章节link
    global url_all, headers
    if i == 0:
        req_next = requests.get(url_all, headers)
    else:
        req_next = requests.get(url_all+'/'+str(i+1), headers)
    req_next.encoding = 'gbk'
    html_next = etree.HTML(req_next.text)
    chapter_name_next = html_next.xpath('//ul[@class="last9"]//li[@class="even"]//a/descendant::text()|//ul[@class="last9"]//li//a/descendant::text()')
    chapter_url_next = html_next.xpath('//ul[@class="last9"]//li[@class="even"]/a/@href|//ul[@class="last9"]//li/a/@href')
    chapter_name = chapter_name_next[1:]
    chapter_url = chapter_url_next[1:]
    return chapter_name, chapter_url


"""------# 对于所有章节的url内容爬取------"""
noval = []

for k in bookname_list:
    start = time.time()
    url = 'https://m.52bqg.com/modules/article/waps.php?searchtype=articlename&searchkey='+parse.quote(k, encoding='gbk')+'&t_btnsearch='
    req = requests.get(url, headers)
    req.encoding = 'gbk'
    if 'book_' in req.url and 'search' not in req.url:  # 搜索结果不是清单则直接开始爬
        url_all = req.url
        url_all = url_all.replace('book', 'chapters')
    else:  # 是清单则判断是否有完全匹配项，若无则只爬榜1
        search_result = req.text
        html_search = etree.HTML(search_result)
        search_book = html_search.xpath('//div[@class="article"]/a/text()')
        search_book_url = html_search.xpath('//div[@class="article"]/a[1]/@href')
        if k in search_book:
            url_all = target_url + search_book_url[search_book.index(k)]
            url_all = url_all.replace('book', 'chapters')
        else:
            url_all = target_url+search_book_url[0]
            url_all = url_all.replace('book', 'chapters')

    # 根据书名判断章节页数
    req_all = requests.get(url_all, headers)
    req_all.encoding = 'gbk'
    html_all = etree.HTML(req_all.text)
    chapter_page_all = html_all.xpath('//table[@class="page-book"]//td/a/@href')
    chapter_page_all = chapter_page_all[1].split('/')
    chapter_page_all = int(chapter_page_all[-1])

    # 开始多线程抓取
    with ThreadPoolExecutor(250) as executor:
        # 根据章节页数,得到章节url
        chapter = list(executor.map(get_chapter_link, range(chapter_page_all)))
        chapter = list(zip(*chapter))
        chapter_url = list(chapter[1])
        chapter_name = list(chapter[0])
        chapter_url = sum(chapter_url, [])
        chapter_name = sum(chapter_name, [])
        chapter_all = list(executor.map(get_chapter_content, chapter_url))
    end = time.time()
    print('total time: '+str(int(end-start))+'秒')
    for i in range(len(chapter_all)):
        chapter_all[i] = chapter_name[i]+'\n'+chapter_all[i]
    target = '\n'.join(chapter_all)
    f = open(save_path+'\\'+k+'.txt', 'a+', encoding='utf-8')
    f.read()
    f.write(target)
    f.close()
    print(k+'完成')
