import os
import re
import time
from selenium import webdriver
import pdfkit


chrome = webdriver.Chrome()
# chrome.add_experimental_option('excludeSwitches', ['enable-automation'])
url = 'https://www.cnvd.org.cn/flaw/show/CNVD-2020-30413'
chrome.get(url)
chrome.get(url)
info_content = chrome.find_element_by_class_name('blkContainerSblk')
html_content = info_content.text
print(info_content)
# print(chrome.page_source)

file_path = '/home/shijiuyi/桌面/other_crawl/crawl_cnvd_list/first.txt'
if not os.path.exists(file_path):
    os.mkdir(file_path)

with open(file_path, 'wb') as f:
    f.write(html_content.encode())
    f.close()

time.sleep(3)
chrome.close()
