import pandas as pd

file = '/home/shijiuyi/桌面/三门峡（单位）v1.xlsx'


def get_cols():
    # 提取xlsx表格中的某一列数据,names=None，不要列名
    domain = pd.read_excel(file, usecols=[1], names=None)
    # print(domain)
    df = pd.read_excel(file, usecols=[0, 1, 2])  # 提取xlsx表格中某几列的数据
    # print(df)

    list_domain = domain.values.tolist()  # 转换为列表
    result = []
    for items in list_domain:
        result.append(items[0])
    # print(result)
    for i in range(len(result)):
        domain_info = result[i]
        # print(domain_info)
        with open('domain_pandas.txt', 'a+') as f:
            f.write(domain_info+'\n')

# # 提取xlsx表格中的行数据，以列表形式输出
# # df = pd.read_excel(file, usecols=[1])  # 只提取主域名列的行数据
# df = pd.read_excel(file)  # 提取所有列的行数据
# df_li = df.values.tolist()
# print(df_li)
# print(df_li[0:4])  # 提取指定行的数据


if __name__ == '__main__':
    get_cols()
