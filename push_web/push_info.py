import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import requests


# 连接pgdb
connect = psycopg2.connect(database='test_beian', user='postgres', password='123456',
                        host='localhost', port='5432')
connect.cursor()

engine = create_engine('postgresql://postgres:123456@localhost:5432/test_beian')

# df = pd.read_sql_query("""select * from gonganbeian_info where id >2500 and id < 2600;""",
#                        con=engine)
df = pd.read_sql_query("""select * from "Heibei_info";""",
                       con=engine)

df1 = np.array(df)  # 先使用array()将DataFrame转换一下
df2 = df1.tolist()  # 再将转换后的数据用tolist()转成列表

print(df2[0])  # 打印某一行数据是

# dic = set()
# for i in range(0, len(df2)):
#     domain = df2[i][1].strip()
#     dic.add(domain)
#
# print(len(dic))

# 循环打印所有的数据
for i in range(0, len(df2)):
    # df.to_csv(r'test.txt')  # 导出pg数据库数据为csv文件
    # beian_info = df2[i][2]  # 打印制定的那一列数据
    beian_info = df2[i]  # 打印每一行所有数据
    # print(beian_info)
    domain = df2[i][1].strip()
    name = df2[i][2].strip()
    subjecet = df2[i][3].strip()
    i_type = df2[i][4].strip()
    owner = df2[i][5].strip()
    num = df2[i][6].strip()
    agency = df2[i][7].strip()
    time = df2[i][8].strip()
    is_filling = df2[i][9]
    # print('domain: ', domain)
    # print('name: ', name)
    # print('subject: ', subjecet)
    # print('i_type: ', i_type)
    # print('owner: ', owner)
    # print('num: ', num)
    # print('agency: ', agency)
    # print('time: ', time)
    # print('is_filling: ', is_filling)
    # print('\n')

    data = {
        'domain': domain,
        'name': name,
        'subject': subjecet,
        'type': i_type,
        'owner': owner,
        'agency': agency,
        'time': time,
        'num': num,
        'is_filing': is_filling
    }

    res = requests.post('http://10.125.0.10:5005/push', json=data)
    print(res.json())


print(len(df2))
