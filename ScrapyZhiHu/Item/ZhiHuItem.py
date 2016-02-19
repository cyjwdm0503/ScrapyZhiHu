# -*- coding: utf-8 -*-
import scrapy


class ScrapyzhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Question_Topic = scrapy.Field()
    Question_Content= scrapy.Field()
    Question_Href = scrapy.Field()
