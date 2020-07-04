import re

import numpy as np
import pandas as pd
import requests


result = {}
# 正则验证ip是否符合
ipv4 = re.compile(r'^\d+\.\d+\.\d+\.\d+$')


def get_ipinfo(ip):
    if not ipv4.match(ip):
        return
    url = f'http://192.168.199.156:5027/service/offline?ip={ip}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        # print(data)
        location = data['province'] + data['city']
        ip_type = data['scene']
        address = data['continent'] + data['country'] + data['province'] + data['city']
        print(location)
        print(address)
        print(ip_type)
        user = data['owner']
        # print(data['accuracy'])
        # print(data['district'])
        # print(data['lat'])
        # print(data['lng'])
        # print(data['owner'])
        # print(data['radius'])
        # print(data['source'])
        # print(data['zipcode'])
        # 键值对保存数据
        result[ip] = [location, ip_type, user]


def main(filename):
    df = pd.read_excel(filename)
    df = df.replace(np.NaN, '')
    df['ip节点'].map(get_ipinfo)
    for ip, values in result.items():
        df.loc[df['ip节点'] == ip, 'ip类型'] = values[1]
        df.loc[df['ip节点'] == ip, 'ip地址'] = values[0]
        df.loc[df['ip节点'] == ip, '拥有者'] = values[2]

    new_filename = '.'.join(filename.split('.')[:-1]) + '-new.xlsx'
    df.to_excel(new_filename)


if __name__ == '__main__':
    file = '/home/shijiuyi/桌面/result_ip.xlsx'
    main(file)

# # 单个ip获取信息
# ip = '122.114.5.100'
# get_ipinfo(ip)
# print(result)
