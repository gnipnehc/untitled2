import time


file = open('/home/shijiuyi/untitled2/crawl/parser_cnvd/xml_test.txt', 'r')
number = 0
for i in file:
    path = i.strip()
    number += 1
    print("解析第{}个xml文件".format(number))
    time.sleep(0.5)
