from datetime import datetime
from elasticsearch_dsl import connections, Document, Keyword, Text, Integer, Date

connections.create_connection(hosts=['localhost'])


class Article(Document):
    title = Text(analyzer='snowball')
    body = Text(analyzer='snowball')
    tags = Keyword()
    published_from = Date()
    lines = Integer

    class Index:
        name = "blog"
        settings = {
            "number_of_shards": 3
        }

    def save(self, **kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(**kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from


Article.init()

article = Article(meta={'id': 42}, title='Hello elasticsearch!', tags=['text'])
article.body = '"looong text"'
article.published_from = datetime.now()
article.save()

article = Article.get(id=42)
print(article.is_published())

print(connections.get_connection().cluster.health)
