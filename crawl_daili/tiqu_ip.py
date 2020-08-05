import re

file = 'ip_pool.txt'
content = open(file, 'r').read()
content = str(content)
# print(content)
content1 = content.split('\n')
print(content1)

for i in content1:
    info = i.split('@'[0])
    # print(info)
    # print(info[0])
    with open('ip_pools.txt', 'a') as f:
        f.write(info[0]+'\n')
print('ok')
