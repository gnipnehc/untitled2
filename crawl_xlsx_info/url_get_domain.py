import tldextract
import csv
import os


data = []
with open('url.txt', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)
    # print(data)

list = []
for i in data:
    url = i[0]
    tld = tldextract.extract(url)
    # print(tld)

    # 万维网+主机名
    # sub_hos = '.'.join(tld[:2])
    # print(sub_hos)

    # 主机名+顶级域名
    host = tld.registered_domain
    list.append(host)
    # print(host)
# print(list)

with open('domain.txt', 'a') as f:
    for h in list:
        f.write(h+'\n')
    print('success')

# tld = tldextract.extract('http://jyj.jiyuan.gov.cn')
# print(tld)
# st = '.'.join(tld[:2])
# print(st)
# inf = tld.registered_domain
# print(inf)
"""
'w'表示写入模式，若要写入的文件不存在，则会自动创建，若要写入的文件已经存在，Python在返回文件对象之前会清空该文件。

'r'表示只读模式，若不传递mode参数，默认会以只读'r'打开文件

'a'表示附加模式，若要操作的文件不存在，则会自动创建，若文件已经存在，则会在末尾追加要写入的内容。
"""
