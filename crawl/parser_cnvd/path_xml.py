import os
path = '/home/shijiuyi/Desktop/other_crawl/crawl_cnvd_list/xml_test'
list_name = []
count = 0

for file in os.listdir(path):
    file_path = os.path.join(path, file)
    if os.path.isdir(file_path):
        os.listdir(file_path, list_name)
    else:
        list_name.append(file_path)

# print(list_name)
    with open('xml_test.txt', 'w') as f:
        count += 1
        for i in list_name:
            f.write(i+'\n')
        print('success: {}'.format(count))
