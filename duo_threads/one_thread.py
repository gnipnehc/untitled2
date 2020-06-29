import threading
import time
from queue import Queue
from urllib.parse import urlencode

import pymysql
import requests

# '''单线程爬取 200个电影信息 用时3.1670422554016113秒'''
headers = {
    'Accept': '*/*',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/explore',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# def save(information):
#        #把数据存入数据库
#        #建立数据库连接
#        connection = pymysql.connect(host = 'localhost',
#                                     user = 'root',
#                                     password = '123456',
#                                     database = '豆瓣电影信息',
#                                     charset = 'utf8'
#        )
#        #增加数据
#        for item in information:
#            try:
#                with connection.cursor() as cursor:
#                    sql = 'insert into 电影信息 (电影名字,电影评分,电影链接) values (%s,%s,%s)'
#                    cursor.execute(sql,(item.get('title'),item.get('rate'),item.get('url')))
#                    #提交数据库事务
#                    connection.commit()
#            except pymysql.DatabaseError:
#                #数据库事务回滚
#                connection.rollback()
#
#        connection.close()

sum = 0
def output(json_text):
    global sum
    for item in json_text:
        sum+=1
        print('电影评分：{0}，电影名称：{1}，电影链接：{2}'.format(item.get('rate'),item.get('title'),item.get('url')))
def get_json_text(url_list):
    for url in url_list:
        response = requests.get(url, headers=headers)
        json_text = response.json()
        output(json_text.get('subjects'))

def main():
    time1 = time.time()
    page = [i * 20 for i in range(10)]
    url_list = []
    for i in page:
        params = {
            'type': 'movie',
            'tag': '热门',
            'sort': 'recommend',
            'page_limit': '20',
            'page_start': i
        }
        url = 'https://movie.douban.com/j/search_subjects?' + urlencode(params)
        url_list.append(url)
    get_json_text(url_list)
    time2 = time.time()
    print('共爬取电影信息：{0}个，共用时：{1}'.format(sum, (time2 - time1)))


if __name__ == '__main__':
    main()
