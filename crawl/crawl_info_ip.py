from selenium import webdriver
import time
import os


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server=http://125.123.152.103:3000")
browsers = webdriver.Chrome(chrome_options=chrome_options)

url = "https://www.cnvd.org.cn/flaw/list.html"
browsers.get(url)
browsers.get(url)
time.sleep(2)

browsers.implicitly_wait(5)
links = browsers.find_elements_by_xpath(
    '/html/body/div[4]/div[1]/div/div[1]/table/tbody/tr/td[1]/a')
length = len(links)

m_list = []
for i in range(0, length):
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
    print(content)
    u_list = []
    u_list.append(content)

    m_list.append(u_list)
    print('\n')

    browsers.back()
    time.sleep(5)
print(length)
# print(m_list)

# for i in m_list:
#     file_path = '/home/shijiuyi/桌面/other_crawl/crawl_cnvd_list/one.docx'
#     if not os.path.exists(file_path):
#         os.mkdir(file_path)
#     info_content = m_list[length]
#     with open(file_path, 'wb') as f:
#         f.write(info_content.encode())
#         f.close()

file_path = '/home/shijiuyi/桌面/other_crawl/crawl_cnvd_list/one.docx'
if not os.path.exists(file_path):
    os.mkdir(file_path)
with open(file_path, 'wb') as f:
    f.write(content.encode())
    f.close()

time.sleep(3)
browsers.close()
