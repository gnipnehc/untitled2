import requests

data = {
    'domain': 'hdu.gov.cn',
    'name': '杭州电子科技大学',
    'subject': '事业单位',
    'type': '非交互式',
    'owner': '杭州电子科技大学',
    'agency': '浙江省杭州市下沙开发区网安大队',
    'time': '2016-05-19',
    'num': '',
    'is_filing': False
}


res = requests.post('http://10.125.0.10:5005/push', json=data)

print(res.json())
