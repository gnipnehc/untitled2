import time, json, datetime, os
import psycopg2


def tabletojson():
    try:
        conn = psycopg2.connect(database='vulnerability', user='postgres', password='123456',
                                host='localhost', port='5432')
        print('connect success')

        cur = conn.cursor()
        sql = "select * from all_cnvd_info where id < 30"
        cur.execute(sql)
        data = cur.fetchall()
        # print(rows)  # 列表数据
        cur.close()
        jsonData = []
        for row in data:
            result = {}
            result['id'] = row[0]
            result['title'] = row[1]
            result['cnvd_id'] = row[2]
            result['cve_id'] = row[3]
            result['cve_url'] = row[4]
            result['level'] = row[5]
            result['affect_product'] = row[6]
            result['vul_type'] = row[7]
            result['posted_time'] = row[8]
            result['update_time'] = row[9]
            result['company_name'] = row[10]
            result['refer_link'] = row[11]
            result['solve_way'] = row[12]
            result['describe'] = row[13]
            result['patch'] = row[14]
            result['patch_describe'] = row[15]
            jsonData.append(result)
    except:
        print('connect failed')
    else:
        # 使用json.dumps将数据转换为json格式，json.dumps方法默认会输出成这种格式"\u5377\u76ae\u6298\u6263"，加ensure_ascii=False，则能够防止中文乱码。
        # JSON采用完全独立于语言的文本格式，事实上大部分现代计算机语言都以某种形式支持它们。这使得一种数据格式在同样基于这些结构的编程语言之间交换成为可能。
        # json.dumps()是将原始数据转为json（其中单引号会变为双引号），而json.loads()是将json转为原始数据。
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
        # 去除首尾的中括号
        return jsondatar[1: len(jsondatar)-1]


if __name__ == '__main__':
    jsonData = tabletojson()
    with open('test_cnvd.txt', 'w+') as f:
        f.write(jsonData+'\n')
    f.close()
