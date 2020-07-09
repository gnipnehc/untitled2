import re


f = open('domain1.txt', 'r')
print(len(f.read().split('\n')))  # 打印文件的长度

# count = 0
# # 循环打印每一行
# for i in f:
#     count += 1
#     print(count, i)

u_list = []
with open('domain1.txt', 'r') as f:
    for line in f.readlines()[2214:]:
        curline = line.strip()
        u_list.append(curline)
# print(u_list)
print(len(u_list))
with open('tiqu_bugen.txt', 'w') as f:
    for info in u_list:
        data = info
        # print(data)
        f.write(data+'\n')

# data = open('tiqu_bugen.txt', 'r')
# data = data.read().strip('\n')
# # print(data)
# print(len(data))
