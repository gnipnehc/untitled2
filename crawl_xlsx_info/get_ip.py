from socket import gethostbyname


# 通过域名反解析ip
domain = 'domain1.txt'
count = 0
with open(domain, 'r') as f:
    for line in f.readlines():
        try:
            host = gethostbyname(line.strip('\n'))  # 域名反解析的ip
            count += 1
            print(count)
        except Exception as e:
            with open('error.txt', 'a+') as err:  # err.txt里面存的是没有ip绑定的域名
                err.write(line.strip() + '\n')
        else:
            with open('result.csv', 'a+') as r:  # result.txt里面存的是批量解析后的结果
                # r.write(line.strip('\n') + ':')  # 显示有ip绑定的域名，用空格隔开
                r.write(host + '\n')
