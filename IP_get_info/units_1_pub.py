import pandas as pd

from celery import Celery
from kombu.common import Broadcast
from config import file, es

# pip install celery==4.3.0
# pip install elasticsearch==7.8.0

app = Celery(__name__, broker='amqp://admin:ODWB6IaRqI@192.168.199.142:5672/units')
app.conf.task_queues = (
    Broadcast('units_collector', ),
)
app.conf.task_routes = {
    'units_collector': {
        'queue': 'units_collector',
        'exchange_type': 'fanout',
        'exchange': 'units_collector',
    },
}


def query(unit_name):
    response = es.search(index='units', body={
        "query": {
            "term": {
                "unit_name.keyword": unit_name
            }
        }
    })
    return response['hits']['total']['value'] > 0


def unit_collector(keyword):
    if not query(keyword):
        print("发布异步任务: ", keyword)
        return app.send_task('collector', queue='units_collector', kwargs={'keyword': keyword})


if __name__ == '__main__':
    df = pd.read_excel(file)
    list(map(unit_collector, set(df['责任单位'])))
    # df['单位名称'].map(unit_collector)
