from crawl_info_cnvd.crawl_info_cnvd.spiders.es_option import ActicleType


def save_to_es(self):
    artcle = ActicleType()
    artcle.title = self['title']
    artcle.cteate_date = self['cteate_date']
    artcle.content = remove_tags(self['content'])

    artcle.front_image_url = self['front_image']
    if "front_image_path" in self:
        artcle.front_image_path = self['front_image_path']
    artcle.praise_nums = self['praise_nums']
    artcle.fav_nums = self['fav_nums']
    artcle.comment_nums = self['comment_nums']
    artcle.url = self['url']
    artcle.tags = self['tags']
    artcle.meta.id = self['url_object_id']

    artcle.save()
    return