import urllib.request
import urllib.parse
import re

# 代理服务器地址：http://31f.cn/
url = 'http://31f.cn/'
head = {}
head['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
                     '(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

reponse = urllib.request.urlopen(url)
html_document = reponse.read().decode('utf-8')
pattern_ip = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>[\s\S]*?'
                        r'<td>(\d{2,4})</td>')

ip_list = pattern_ip.findall(html_document)
print(len(ip_list))
for i in ip_list:
    print("ip地址是：%s 端口号是：%s" % (i[0], i[1]))