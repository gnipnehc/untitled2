from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch('localhost:9200')
mappings = {
    "mappings": {
        "type_doc_test": {              # type_doc_test为doc_type
          "properties": {
            "id": {
              "type": "long",
              "index": "false"
            },
            "serial": {
              "type": "keyword",  # keyword不会进行分词,text会分词
              "index": "false"  # 不建索引
            },
            # tags可以存json格式，访问tags.content
            "tags": {
              "type": "object",
              "properties": {
                "content": {"type": "keyword", "index": True},
                "dominant_color_name": {"type": "keyword", "index": True},
                "skill": {"type": "keyword", "index": True},
              }
            },
            "hasTag": {
              "type": "long",
              "index": True
            },
            "status": {
              "type": "long",
              "index": True
            },
            "createTime": {
              "type": "date",
              "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            },
            "updateTime": {
              "type": "date",
              "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            }
          }
        }
      }
}
res = es.index(index='index_test', id=2, body=mappings)
print(res['result'])

res = es.get(index='index_test', id=2)
print(res['_source'])