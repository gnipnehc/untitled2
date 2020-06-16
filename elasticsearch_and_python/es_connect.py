# -*-coding:utf-8-*-
from elasticsearch import Elasticsearch

from datetime import datetime


es_service = [{
    "host": "127.0.0.1",
    "port": "9200"
}]

es = Elasticsearch(es_service)

date = {
    'author': 'stone',
    'text': "今天的天气不太热",
    'timestamp': datetime.now(),
}

res = es.index(index='test-index', doc_type='tweet', id=1, body=date)
print(res)  # 打印索引信息

res = es.get(index='test-index', doc_type='tweet', id=1)
print(res['_source'])  # 打印内容

es.indices.refresh(index="test-index")

# 自定义查找顺序
res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    # print(hit["_source"])
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
