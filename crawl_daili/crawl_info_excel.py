import os
import re
import time
import xlwt
from selenium import webdriver
import pdfkit


chrome = webdriver.Chrome()
# chrome.add_experimental_option('excludeSwitches', ['enable-automation'])
url = 'https://www.cnvd.org.cn/flaw/show/CNVD-2020-30413'
chrome.get(url)
chrome.get(url)

info_title = chrome.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div[1]/h1')
title = info_title.text
print(title)

info_content = chrome.find_elements_by_xpath('/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody/tr')
# print(info_content)

book = xlwt.Workbook()
sheet = book.add_sheet('123')

row = 0
for job in info_content:
    fields = job.find_elements_by_tag_name('td')
    col = 0
    for field in fields:
        stringFields = field.text
        # print(stringFields, end=' ')
        sheet.write(row, col, stringFields)
        col += 1
    print('')
    row += 1

# 保存到文件
book.save('/home/shijiuyi/桌面/other_crawl/crawl_cnvd_list/first_info.xls')

time.sleep(3)
chrome.close()
