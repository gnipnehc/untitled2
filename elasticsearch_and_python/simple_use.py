# -*-coding:utf-8-*-
from elasticsearch import Elasticsearch


es_service = [{'host': '127.0.0.1', 'port': '9200'}]
es_auth = ('stone', 'Sovereign')
es = Elasticsearch(es_service, http_auth=es_auth)

# 创建es索引
# es.indices.create(index='p2', ignore=400)
# es.indices.create(index='p5', ignore=400)

# 删除es索引
# es.indices.delete(index='p2', ignore=[400, 404])

# data = {
#     'title': '莱纳德单节16分打爆詹皇 受球迷刺激他轰30+6+5',
#     'url': 'https://sports.163.com/19/1023/13/ES65333E0005877U.html',
#     'date': '2020-06-05'
# }
# res = es.create(index='p1', id=1, body=data, doc_type='politics')
# print(res)

# 获取es数据
# res = es.get(index='p1', id=1)
# print(res)

# 更新es数据
# data = {
#     'title': '莱纳德单节16分打爆詹皇 受球迷刺激他轰30+6+5',
#     'url': 'https://sports.163.com/19/1023/13/ES65333E0005877U.html',
#     'date': '2020-06-05',
#     'address': '郑州',
#     'tianqi': 'qing',
#     'wendu': 'cold very'
# }
# es.index(index='p1', id=1, body=data)

mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}
es.indices.create(index='p1', ignore=400)
res = es.indices.put_mapping(index='p1', body=mapping)

# 预备数据
datas = [
 {
   'title': '莱纳德单节16分打爆詹皇 受球迷刺激他轰30+6+5',
   'url': 'https://sports.163.com/19/1023/13/ES65333E0005877U.html',
   'date': '2019-10-23'
 },
 {
   'title': '詹姆斯:最伟大湖人记忆是00西决 科比一直激励着我',
   'url': 'https://sports.163.com/19/1023/08/ES5LOKPC0005877U.html',
   'date': '2019-10-23'
 },
 {
   'title': '詹皇18+9+8末节哑火4中1 单节3失误遭小卡碾压',
   'url': 'https://sports.163.com/19/1023/13/ES64TISL0005877U.html',
   'date': '2019-10-23'
 },
 {
   'title': '60比19!轻轻松松碾压 快船的这一特性湖人真比不了',
   'url': 'https://sports.163.com/19/1023/13/ES65RM0J0005877U.html',
   'date': '2019-10-23'
 }
]
# 批量插入数据
for data in datas:
    es.index(index='p1', body=data)

# # 搜索数据
# dsl = {'query': {'match': {'title': '詹姆斯'}}}
# res = es.search(index='p1', body=dsl)
# print(res)
