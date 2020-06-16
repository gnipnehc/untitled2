from datetime import datetime
from elasticsearch_dsl import Date, Document, Text, Integer, Keyword
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class ActicleType(Document):
    # 伯乐在线文章类型
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    front_image_url = Keyword()
    front_image_path = Keyword()
    praise_nums = Integer()
    comment_nums = Integer()
    fav_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "jobbile"
        doc_type = "article"


if __name__ == "__main__":
    ActicleType.init()