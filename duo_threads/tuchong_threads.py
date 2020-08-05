import threading
from queue import Queue
import requests
import os
import time

CRAWL_EXIT = False


class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue):
        # threading.Thread.__init__()
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = thread_name
        self.page_queue = page_queue

    def run(self):
        print(self.threadName + '启动********')
        while not CRAWL_EXIT:
            try:
                # global tag, url, img_format  # 把全局的拿过来
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
                                  "(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE"
                }

                # 队列为空，产生异常
                page = self.page_queue.get(block=False)  # 从里面获取值
                spider_url = 'https://tuchong.com/rest/tags/%E9%A3%8E%E5%85%89/posts?page={}&count=20&order=weekly'.format(page)
                print(spider_url)
            except:
                break

            timeout = 4  # 合格的地方是尝试获取三次，三次都失败，就跳出
            while timeout > 0:
                timeout -= 1
                try:
                    with requests.Session() as s:
                        response = s.get(spider_url, headers=headers, timeout=3)
                        json_data = response.json()
                        if json_data is not None:
                            imgs = json_data["postList"]
                            for i in imgs:
                                imgs = i["images"]
                                for img in imgs:
                                    user_id = img["user_id"]
                                    img_id = img["img_id"]
                                    img_url = 'https://photo.tuchong.com/{}/f/{}.jpg'.format(user_id, img_id)
                                    # self.data_queue.put(img_url)  # 捕获到图片链接，之后，存入一个新的队列里面，等待下一步的操作
                                    title = 'download/'+str(img_id)
                                    response = requests.get(img_url)

                                    # 保存图片名字有问题，可能重复
                                    with open(title+'.jpg', 'wb') as f:
                                        f.write(response.content)
                                        time.sleep(3)
                    break
                except Exception as e:
                    print(e)
            if timeout <= 0:
                print('time out')


def main():
    # 声明一个队列，使用循环在里面存入100个页码
    page_queue = Queue(10)
    for i in range(1, 11):
        page_queue.put(i)

    # 采集结果（等待下载的图片地址）
    # data_queue = Queue()

    # 记录线程的列表
    thread_crawl = []
    # 每次开启4个线程
    crawl_list = ['采集线程1号', '采集线程2号', '采集线程3号', '采集线程4号']
    if not os.path.exists('/home/shijiuyi/桌面/crawl_changyong/crawl_picture/download'):
        os.mkdir('/home/shijiuyi/桌面/crawl_changyong/crawl_picture/download')
    for thread_name in crawl_list:
        c_thread = ThreadCrawl(thread_name, page_queue)
        c_thread.start()
        thread_crawl.append(c_thread)

    # 等待page_queue队列为空，也就是等待之前的操作执行完毕
    while not page_queue.empty():
        pass
    # 如果page_queue为空，采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True


if __name__ == '__main__':
    main()
