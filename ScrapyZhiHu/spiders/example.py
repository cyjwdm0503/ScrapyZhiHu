# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]
    start_urls = (
        'http://xueqiu.com/stock/f10/compinfo.json?symbol=SZ000001&page=1&size=4&_=14557248756',
    )

    def parse(self, response):
        pass
