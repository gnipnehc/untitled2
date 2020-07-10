import re

import numpy as np
import pandas as pd
import requests

"""
pip install requests
pip install openpyxl
pip install pandas
pip install numpy
pip install xlrd
"""
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
        location = data['province'] + data['city']
        ip_type = data['scene']
        # 键值对保存数据
        result[ip] = [location, ip_type]


def main(filename):
    # 打开表格
    df = pd.read_excel(filename)
    # 将NaN替换为空
    df = df.replace(np.NaN, '')
    df['IP节点'].map(get_ipinfo)
    for ip, values in result.items():
        df.loc[df['IP节点'] == ip, 'IP类型'] = values[1]
        df.loc[df['IP节点'] == ip, 'IP归属地'] = values[0]
    new_filename = '.'.join(filename.split('.')[:-1]) + '-new.xlsx'
    df.to_excel(new_filename)


if __name__ == '__main__':
    file = '/home/shijiuyi/桌面/郑州网信办（IP）.xlsx'
    main(file)

"""
1）行（列）选取（单维度选取）：df[]。这种情况一次只能选取行或者列，即一次选取中，只能为行或者列设置筛选条件（只能为一个维度设置筛选条件）。

2）区域选取（多维选取）：df.loc[]，df.iloc[]，df.ix[]。这种方式可以同时为多个维度设置筛选条件。

3）单元格选取（点选取）：df.at[]，df.iat[]。准确定位一个单元格。
"""

"""
u: 后面字符串以 Unicode 格式 进行编码，一般用在中文字符串前面，防止因为源码储存格式问题，导致再次使用时出现乱码
r: 去掉反斜杠的转移机制,防止发生转义，常用于正则表达式，对应着re模块
f: 以 f开头表示在字符串内支持大括号{}内的python 表达式
b: 表示后面跟的字符串以bytes类型，bytes与str在Python3中的转换：str.encode('utf-8');bytes.decode('utf-8')
"""
