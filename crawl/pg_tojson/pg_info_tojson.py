import time, json, datetime, os
import psycopg2


def tabletojson():
    try:
        conn = psycopg2.connect(database='vulnerability', user='postgres', password='123456',
                                host='localhost', port='5432')
        print('connect success')

        cur = conn.cursor()
        sql = "select * from all_cnvd_info where id < 601"
        cur.execute(sql)
        data = cur.fetchall()
        # print(rows)  # 列表数据
        cur.close()
        jsonData = []
        with open('pg_json.txt', 'w+') as f:
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
                jsondata = json.dumps(result, ensure_ascii=False)
                f.write(jsondata+'\n')
    except:
        print('connect failed')


tabletojson()
