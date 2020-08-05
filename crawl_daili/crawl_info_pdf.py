import os
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pdfkit
import PyPDF2


chrome = webdriver.Chrome()
# chrome.add_experimental_option('excludeSwitches', ['enable-automation'])
url = 'https://www.cnvd.org.cn/flaw/show/CNVD-2020-26428'
chrome.get(url)
chrome.get(url)
# print(chrome.page_source)

info_title = chrome.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[1]/h1')
title = info_title.text
newtitle = re.split(r'-', title)
print(newtitle)

html_content = chrome.find_element_by_class_name('gg_detail')
info_content = html_content.text
# print(info_content)

# 保存为html文件
file_path = '/home/shijiuyi/桌面/other_crawl/crawl_cnvd_list/'
filename = title+".html"
path = file_path+filename
# if not os.path.exists(path):
#     os.mkdir(path)
# with open(path, 'wb') as f:
#     f.write(info_content.encode())
#     f.close()

# 将html文件转为pdf
# pdfname = title+".pdf"
# htmlfile = open(path, 'r')
# confg = pdfkit.configuration(
#     wkhtmltopdf=""
# )
# if not os.path.exists(file_path):
#     os.mkdir(file_path)
#
# file_name = title
# path = file_path+file_name+'.pdf'
# with open(path, 'wb') as f:
#     f.write(info_content.encode())
#     f.close()
#
# path_wk = r'/home/shijiuyi/untitled3/venv/lib/python3.8/site-packages/wkhtmltopdf'
# confg = pdfkit.configuration(wkhtmltopdf=path_wk)
# pdfkit.from_url(url, path, configuration=confg)

time.sleep(3)
chrome.close()
