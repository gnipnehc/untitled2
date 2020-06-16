from .spiders.es_option import ActicleType
from w3lib.html import remove_tags

class ElasticsearchPipeline(object):
    # 将数据写入到es中
    def process_item(self,item,spider):
        # 将item转换为es数据
        item.save_to_es()
        return item