import pandas as pd


file = '/home/shijiuyi/Desktop/work/公安备案/陕西主域名.csv'


def get_data():
    domain = pd.read_csv(file)
    # print(domain)

    list_domain = domain.values.tolist()
    result = []
    for items in list_domain:
        result.append(items[0])
    # print(result)
    for i in range(len(result)):
        domain_info = result[i]
        # print(domain_info)
        with open('domain_csv.txt', 'a+') as f:
            f.write(domain_info+'\n')


get_data()
