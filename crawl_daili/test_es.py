from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch()  # 本地连接
doc = {
    'author': 'sovereign',
    'text': 'Elasticsearch;cool.bonsai cool.',
    'timestamp': datetime.now()
}
res = es.index(index="test-index", id=1, body=doc)
print(res['result'])

res = es.get(index="test-index", id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s%(author)s:%(text)s" % hit["_source"])
