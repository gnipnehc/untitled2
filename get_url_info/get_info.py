
import requests
import xlwt
from tld import get_fld
import re
from urllib import parse
import socket
a = 0
results = []
with open('domain.txt') as f:
    for line in f.readlines():
        url = line.strip()
        try:
            res1 = requests.post("http://10.125.0.10:5012/website/archived/list/inter", json={"filter": {"url": url}}, timeout=60)
        except Exception as e:
            try:
                domain = get_fld(url.strip())
                res5 = requests.post("http://10.125.0.26:10000/query", json={"domain": domain})
                if res5.json()['code'] == 200:
                    sponsor = res5.json()['data']['sponsor']
                    sponsor_type = res5.json()['data']['sponsor_type']
                    if sponsor != '未备案':
                        try:
                            res0 = requests.get(url, timeout=10)
                            if res0.encoding == 'ISO-8859-1':
                                encodings = requests.utils.get_encodings_from_content(res0.text)
                                res0.encoding = requests.utils.get_encodings_from_content(res0.text)
                                if encodings:
                                    encoding = encodings[0]
                                    res0.encoding = encodings[0]
                                else:
                                    encoding = res0.apparent_encoding
                                    res0.encoding = res0.apparent_encoding
                            else:
                                encoding = res0.encoding
                            # encode_content = res0.content.decode(encoding, 'ignore').encode('utf-8', 'ignore')
                            # print(encode_content)
                            if res0.status_code == 200:
                                pat = r'<title>(.*)</title>'
                                title = re.findall(pat, res0.text)
                                print(title[0])
                                try:
                                    subdomin = parse.urlparse(url).netloc
                                    ip = socket.gethostbyname(subdomin)
                                except Exception as e:
                                    ip = ''
                                print([url, title[0], domain, sponsor, ip, sponsor_type])
                                results.append([url, title[0], domain, sponsor, ip, sponsor_type])
                            else:
                                results.append([url, '', domain, sponsor, '', sponsor_type])
                        except Exception as e:
                            print(e)
                            results.append([url, '', domain, sponsor, '', sponsor_type])
                    else:
                        results.append([url, '', domain, sponsor, '', sponsor_type])
                else:
                    sponsor = '错误'
                    sponsor_type = '错误'
                    print("error", domain)
                    results.append([url, '', '', sponsor, '', sponsor_type])
            except Exception as e:
                results.append([url, '', '', '', '', ''])
            continue
        if res1.json()['status'] and len(res1.json()['data']['records']) != 0:
            a += 1
            data = res1.json()['data']['records'][0]
            results.append([url, data['title'], data['domain'], data['host_dept'], data['ip'], data['host_type']])
        else:
            headers = {
                'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTIyOTUxNDQsIm5iZiI6MTU5MjI5NT'
                                 'E0NCwianRpIjoiYWQ2ZTM1NTktYTliZS00NmMyLTkxNGQtODY5Y2MzMmM4MjliIiwiZXhwIjoxNTkyMzE2NzQ0'
                                 'LCJpZGVudGl0eSI6IkhVQU5HWlAiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcy'
                                 'I6eyJ1c2VyX2lkIjoiYmRiZjAwM2YtYmU0MS00MGJkLWEyMzUtNzllYWMzNGI5OWI3IiwidXNlcm5hbWUiOiJI'
                                 'VUFOR1pQIiwiZW1haWwiOiJodWFuZ3poYW5ncGVuZ0Bzb2NtYXAubmV0IiwicGhvbmUiOiIxNTUxODk5NzY4My'
                                 'IsInJvbGUiOjAsIm5hbWUiOiJIVUFOR1pQIiwiYXZhdGFyIjoiaHR0cHM6Ly9naXQuc29jbWFwLm9yZy91cGxv'
                                 'YWRzLy0vc3lzdGVtL3VzZXIvYXZhdGFyLzMxL2F2YXRhci5wbmciLCJ0ZWxlcGhvbmUiOiIiLCJnaXRsYWJfb2'
                                 'F1dGgiOnRydWV9LCJjc3JmIjoiMjY2NWQ3NjktNGI1Yy00YzEyLWExOWQtZWNlYzU0YmEwNTQxIn0.lFZ7NoNF'
                                 'mLcQPJJA87AQyx_OWURkNCZwwy2DUqn4Bco'
           }
            data = {
                'filter': {
                    'url': url
                }
            }

            try:
                res2 = requests.post('http://10.125.0.10:5068/website/news/list', headers=headers, json=data, timeout=60)
            except Exception as e:
                try:
                    domain = get_fld(url.strip())
                    res5 = requests.post("http://10.125.0.26:10000/query", json={"domain": domain})
                    if res5.json()['code'] == 200:
                        sponsor = res5.json()['data']['sponsor']
                        sponsor_type = res5.json()['data']['sponsor_type']
                        if sponsor != '未备案':
                            try:
                                res0 = requests.get(url, timeout=10)
                                if res0.encoding == 'ISO-8859-1':
                                    encodings = requests.utils.get_encodings_from_content(res0.text)
                                    res0.encoding = requests.utils.get_encodings_from_content(res0.text)
                                    if encodings:
                                        encoding = encodings[0]
                                        res0.encoding = encodings[0]
                                    else:
                                        encoding = res0.apparent_encoding
                                        res0.encoding = res0.apparent_encoding
                                else:
                                    encoding = res0.encoding
                                # encode_content = res0.content.decode(encoding, 'ignore').encode('utf-8', 'ignore')
                                # print(encode_content)
                                if res0.status_code == 200:
                                    pat = r'<title>(.*)</title>'
                                    title = re.findall(pat, res0.text)
                                    print(title[0])
                                    try:
                                        subdomin = parse.urlparse(url).netloc
                                        ip = socket.gethostbyname(subdomin)
                                    except Exception as e:
                                        ip = ''
                                    print([url, title[0], domain, sponsor, ip, sponsor_type])
                                    results.append([url, title[0], domain, sponsor, ip, sponsor_type])
                                else:
                                    results.append([url, '', domain, sponsor, '', sponsor_type])
                            except Exception as e:
                                print(e)
                                results.append([url, '', domain, sponsor, '', sponsor_type])
                        else:
                            results.append([url, '', domain, sponsor, '', sponsor_type])
                    else:
                        sponsor = '错误'
                        sponsor_type = '错误'
                        print("error", domain)
                        results.append([url, '', '', sponsor, '', sponsor_type])
                except Exception as e:
                    results.append([url, '', '', '', '', ''])
                continue

            if res2.json()['status'] and len(res2.json()['data']['records']) != 0:
                a += 1
                data1 = res2.json()['data']['records'][0]
                # print(data1)
                results.append([url, data1['title'], data1['domain'], data1['host_dept'], data1['ip'], data1['host_type']])
            else:
                try:
                    res3 = requests.post("http://10.125.0.10:5012/website/invalid/list/inter",
                                        json={"filter": {"url": url}}, timeout=60)
                except Exception as e:

                    try:
                        domain = get_fld(url.strip())
                        res5 = requests.post("http://10.125.0.26:10000/query", json={"domain": domain})
                        if res5.json()['code'] == 200:
                            sponsor = res5.json()['data']['sponsor']
                            sponsor_type = res5.json()['data']['sponsor_type']
                            if sponsor != '未备案':
                                try:
                                    res0 = requests.get(url, timeout=10)
                                    if res0.encoding == 'ISO-8859-1':
                                        encodings = requests.utils.get_encodings_from_content(res0.text)
                                        res0.encoding = requests.utils.get_encodings_from_content(res0.text)
                                        if encodings:
                                            encoding = encodings[0]
                                            res0.encoding = encodings[0]
                                        else:
                                            encoding = res0.apparent_encoding
                                            res0.encoding = res0.apparent_encoding
                                    else:
                                        encoding = res0.encoding
                                    # encode_content = res0.content.decode(encoding, 'ignore').encode('utf-8', 'ignore')
                                    # print(encode_content)
                                    if res0.status_code == 200:
                                        pat = r'<title>(.*)</title>'
                                        title = re.findall(pat, res0.text)
                                        print(title[0])
                                        try:
                                            subdomin = parse.urlparse(url).netloc
                                            ip = socket.gethostbyname(subdomin)
                                        except Exception as e:
                                            ip = ''
                                        print([url, title[0], domain, sponsor, ip, sponsor_type])
                                        results.append([url, title[0], domain, sponsor, ip, sponsor_type])
                                    else:
                                        results.append([url, '', domain, sponsor, '', sponsor_type])
                                except Exception as e:
                                    print(e)
                                    results.append([url, '', domain, sponsor, '', sponsor_type])
                            else:
                                results.append([url, '', domain, sponsor, '', sponsor_type])
                        else:
                            sponsor = '错误'
                            sponsor_type = '错误'
                            print("error", domain)
                            results.append([url, '', '', sponsor, '', sponsor_type])
                    except Exception as e:
                        results.append([url, '', '', '', '', ''])
                    continue

                if res3.json()['status'] and len(res3.json()['data']['records']) != 0:
                    a += 1
                    data2 = res3.json()['data']['records'][0]
                    results.append([url, data2['title'], data2['domain'], data2['host_dept'], data2['ip'], data2['host_type']])
                else:
                    try:
                        domain = get_fld(url.strip())
                        res5 = requests.post("http://10.125.0.26:10000/query", json={"domain": domain})
                        if res5.json()['code'] == 200:
                            sponsor = res5.json()['data']['sponsor']
                            sponsor_type = res5.json()['data']['sponsor_type']
                            if sponsor != '未备案':
                                try:
                                    res0 = requests.get(url, timeout=10)
                                    if res0.encoding == 'ISO-8859-1':
                                        encodings = requests.utils.get_encodings_from_content(res0.text)
                                        res0.encoding = requests.utils.get_encodings_from_content(res0.text)
                                        if encodings:
                                            encoding = encodings[0]
                                            res0.encoding = encodings[0]
                                        else:
                                            encoding = res0.apparent_encoding
                                            res0.encoding = res0.apparent_encoding
                                    else:
                                        encoding = res0.encoding
                                    # encode_content = res0.content.decode(encoding, 'ignore').encode('utf-8', 'ignore')
                                    # print(encode_content)
                                    if res0.status_code == 200:
                                        pat = r'<title>(.*)</title>'
                                        title = re.findall(pat, res0.text)
                                        print(title[0])
                                        try:
                                            subdomin = parse.urlparse(url).netloc
                                            ip = socket.gethostbyname(subdomin)
                                        except Exception as e:
                                            ip = ''
                                        print([url, title[0], domain, sponsor, ip, sponsor_type])
                                        results.append([url, title[0], domain, sponsor, ip, sponsor_type])
                                    else:
                                        results.append([url, '', domain, sponsor, '', sponsor_type])
                                except Exception as e:
                                    print(e)
                                    results.append([url, '', domain, sponsor, '', sponsor_type])
                            else:
                                results.append([url, '', domain, sponsor, '', sponsor_type])
                        else:
                            sponsor = '错误'
                            sponsor_type = '错误'
                            print("error", domain)
                            results.append([url, '', '', sponsor, '', sponsor_type])
                    except Exception as e:
                        results.append([url, '', '', '', '', ''])


def write_excel():
    mm = 1
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('数据', cell_overwrite_ok=True)
    row0 = ["网址", "网站名称", "主域名", "备案单位", "IP", "单位性质"]
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])
    for i in range(len(results)):
        k=0
        for j in results[i]:

            sheet1.write(mm, k, j)
            k += 1
        mm += 1
    f.save('周口资产梳理.xls')

print(a)
print(len(results))
write_excel()
