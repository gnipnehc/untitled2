import time
from selenium import webdriver
import pdfkit
from selenium.webdriver.support.ui import WebDriverWait
import os

# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# self.browser = webdriver.Chrome(options=options)
# self.wait = WebDriverWait(self.browser, 30)

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
#                   "(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE"
# }

browsers = webdriver.ChromeOptions()
# 使用无头模式
browsers.add_argument('--headless')

url = 'https://www.cnvd.org.cn/flaw/list.html'
browsers = webdriver.Chrome(chrome_options=browsers)
browsers.get(url)
browsers.get(url)
time.sleep(2)

browsers.implicitly_wait(5)
links = browsers.find_elements_by_xpath(
    '/html/body/div[4]/div[1]/div/div[1]/table/tbody/tr/td[1]/a')
length = len(links)

info_list = []
for i in range(0, 6):
    links = browsers.find_elements_by_xpath(
        '/html/body/div[4]/div[1]/div/div[1]/table/tbody/tr/td[1]/a')
    link = links[i]
    url = link.get_attribute('href')
    browsers.get(url)
    time.sleep(3)

    title = browsers.find_element_by_xpath(
        '/html/body/div[4]/div[1]/div[1]/div[1]/h1').text
    print(title)
    content = browsers.find_element_by_xpath(
        '/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table').text
    # print(content)
    con_list = []
    con_list.append(content)
    print(con_list)
    info_list.append(con_list)
    print('\n')

    browsers.back()
    time.sleep(5)
print(length)

# info_content = browsers.find_element_by_class_name('tlist')
# html_content = info_content.text
# print(html_content)

# 保存到文件
for i in info_list:
    file_path = '/home/shijiuyi/桌面/other_crawl/crawl_cnvd_list/one.docx'
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    info_content = i[0]
    with open(file_path, 'wb') as f:
        f.write(info_content.encode())
        f.close()

# file_path = '/home/shijiuyi/桌面/other_crawl/crawl_cnvd_list/one.docx'
# if not os.path.exists(file_path):
#     os.mkdir(file_path)
#
# with open(file_path, 'wb') as f:
#     f.write(info_list)
#     f.close()

time.sleep(3)
browsers.close()
