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
df = pd.read_sql_query("""select main_domain from test_info;""",
                       con=engine)

df1 = np.array(df)  # 先使用array()将DataFrame转换一下
df2 = df1.tolist()  # 再将转换后的数据用tolist()转成列表
print(len(df2))
pg_data = []
for i in df2:
    domain_list = i[0]
    domain_list = domain_list.strip('\n')
    # print(domain_list)
    pg_data.append(domain_list)
# print(pg_data)

fr = open('domain1.txt', 'r')

file_data = []
for i in fr:
    file_list = i.strip('\n')
    file_data.append(file_list)
print(file_data)


for data in file_data:
    if data in pg_data:
        pass
    else:
        with open('domain_test.txt', 'a') as f:
            no_data = str(data)
            f.write(no_data+'\n')

# print(df2[0])  # 打印某一行数据是
#
# dic = set()
# for i in range(0, len(df2)):
#     domain = df2[i][1].strip()
#     dic.add(domain)
#
# print(len(dic))
