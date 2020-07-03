import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


df = pd.read_csv('/home/shijiuyi/桌面/河北.csv')
# print(df)
df1 = np.array(df)  # 先使用array()将DataFrame转换一下
df2 = df1.tolist()  # 再将转换后的数据用tolist()转成列表
dic = set()
for i in range(0, len(df2)):
    domain = df2[i][0].strip()
    dic.add(domain)

print(len(dic))
