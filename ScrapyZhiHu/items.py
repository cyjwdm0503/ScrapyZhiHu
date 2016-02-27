# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyzhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ScrapyUsers(scrapy.Item):
    href = scrapy.Field()
    name = scrapy.Field()


    def Save(self):
        pass


class ScrapyCollections(scrapy.Item):
    user_href = scrapy.Field()
    collection_name = scrapy.Field()
    collection_url = scrapy.Field()


