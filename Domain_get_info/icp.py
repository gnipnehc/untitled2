import requests
from tld import get_fld


with open('domain.txt') as f:
    for line in f.readlines():
        try:
            # domain = get_fld(line.strip().strip())
            url = 'http://10.125.0.26:10000/dispatch'
            data = {
                'domain': line,
                'refresh': True,
                'source': "人为收录"
            }

            resp = requests.post(url, json=data)
            print(resp.json())
        except Exception as e:
            print(e)
