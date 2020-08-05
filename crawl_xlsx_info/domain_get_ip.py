import requests
import socket
from socket import gethostbyname


# # 单个域名获取ip
# def getIp(domain):
#     # 通过域名获取ip
#     myaddr = socket.getaddrinfo(domain, None)
#     return myaddr[0][4][0]
#
# domain = 'dancheng.gov.cn'
# print(getIp(domain))


def get_all_ip(domain):
    try:
        host = gethostbyname(domain)  # 域名反解析的ip
        # print(host)
    except Exception as e:
        with open('result.csv', 'a+') as err:
            err.write('null' + '\n')
    else:
        with open('result.csv', 'a+') as r:
            # r.write(line.strip('\n') + ':')  # 显示有ip绑定的域名，用空格隔开
            if host == '0.0.0.0':
                r.write('null' + '\n')
            else:
                r.write(host + '\n')


# 批量域名获取ip
domain_data = []
with open('text.txt', 'r') as f:
    line_domain = f.readlines()
    # print(line_domain)
    for line in range(0, len(line_domain)):
        domain_data.append(line_domain[line].strip())
        # print(domain_data[line])  # 循环打印
# print(domain_data[0])
# print(domain_data)
if __name__ == '__main__':
    count = 0
    for num in domain_data:
        # print(num)
        domain = num
        count += 1
        print('count{}:  '.format(count)+domain)
        get_all_ip(domain)
    print('总共 {} 条数据'.format(count))
