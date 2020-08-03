import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import requests


# 连接pgdb
connect = psycopg2.connect(database='vulnerability', user='postgres', password='123456',
                        host='localhost', port='5432')
connect.cursor()

engine = create_engine('postgresql://postgres:123456@localhost:5432/vulnerability')

list = []

df = pd.read_sql_query("""select * from all_cnvd_info where id < 30;""",
                       con=engine)
list.append(df)

for i in list:
    df.to_csv(r'test.csv')
