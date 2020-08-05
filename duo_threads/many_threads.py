import threading
import time
from queue import Queue
from urllib.parse import urlencode

import pymysql
import requests


headers = {
    'Accept': '*/*',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/explore',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 中间者，存放爬取返回结果队列
result_queue = Queue()


class Threading_product(threading.Thread):
	# 初始化
    def __init__(self ,name, url_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.name = name
    # 重写threading中的run()执行方法
    def run(self):
        print('生产者{0}正在爬取...'.format(self.name))
        self.spider()
        print('生产者{0}爬取完成...'.format(self.name))
    # 简单的对信息进行爬取
    def spider(self):
        while True:
            if self.url_queue.empty():
                break
            else:
                url = self.url_queue.get()
                response = requests.get(url, headers=headers)
                json_text = response.json()
                # 将返回结果存入中间者，返回结果队列当中
                result_queue.put(json_text.get('subjects'))


class Threading_constumer(threading.Thread):
    # 初始化
    def __init__(self,name,result_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.result_queue = result_queue
    # 重写run()方法
    def run(self):
        print('消费者{0}正在解析页面并进行电影信息输出：'.format(self.name))
        self.spider()

	# 简单的进行输出
    def spider(self):
        while True:
            if self.result_queue.empty():
                break
            else:
                response = self.result_queue.get()
                for item in response:
                    print('电影评分：{0}，电影名称：{1}，电影链接：{2}'.format(item.get('rate'), item.get('title'), item.get('url')))


def main():
	# 产生程序开始时间
    time3 = time.time()
    # 每20个为一页的信息，创建10页
    page = [i * 20 for i in range(10)]
    # 存放页面的url队列
    url_queue = Queue()
    # 构造url链接
    for i in page:
        params = {
            'type': 'movie',
            'tag': '热门',
            'sort': 'recommend',
            'page_limit': '20',
            'page_start': i
        }
        url = 'https://movie.douban.com/j/search_subjects?' + urlencode(params)
        # 放入url队列当中
        url_queue.put(url)
    # 生产者队列
    threading_product_list = []
    # 创建5个生产者
    for i in range(5):
    	# 产生生产者
        threading_product = Threading_product(i, url_queue)
        # 执行
        threading_product.start()
        # 将生产者放入生产者队列当中
        threading_product_list.append(threading_product)
    # 遍历生产者，阻塞主线程，也就是说让每一个生成者都执行完自己的线程内容
    for i in threading_product_list:
        i.join()
    # 消费者队列
    threading_constumer_list = []
    # 创建3个消费者
    for i in range(5):
        # 产生消费者
        threading_constumer = Threading_constumer(i, result_queue)
        # 执行
        threading_constumer.start()
        # 将消费者放入队列当中
        threading_constumer_list.append(threading_constumer)
    # 遍历消费者，阻塞主线程，也就是说让每一个消费者都执行完自己的线程内容
    for i in threading_constumer_list:
        i.join()
    # 获取代码执行完的最后时间
    time4 = time.time()
    print('共用时：{}'.format(time4 - time3))


if __name__ == '__main__':
    main()
