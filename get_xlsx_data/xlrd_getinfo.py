import xlrd


file = '/home/shijiuyi/桌面/郑州网信办.xlsx'


# xlrd包提取表格某列信息
def get_info():
    data = xlrd.open_workbook(file)
    sheet = data.sheets()[0]
    info = sheet.col_values(1)  # 列表形式
    name = sheet.col_values(0)  # 列表形式
    # print(info)
    # print(name)
    for items in range(len(info)):
        domain = info[items]
        with open('domain_xlrd.txt', 'a+') as f:
            f.write(domain+'\n')


if __name__ == '__main__':
    get_info()
