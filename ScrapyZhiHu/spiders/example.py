# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
class ExampleSpider(scrapy.Spider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]
    start_urls = (
        'http://xueqiu.com/stock/f10/compinfo.json?symbol=SZ000001&page=1&size=4&_=14557248756',
    )

    def parse(self, response):
        pass

class Zhihu(scrapy.Spider):
    name = "ZhiHu"
    allowed_domains=["zhihu.com"]
    start_urls=("https://www.zhihu.com/#signin",)
    xsrf=""

    def parse(self, response):
        self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print self.xsrf
        return  self.login()

    def login(self):
        return [scrapy.FormRequest("https://www.zhihu.com/login/email",
                                   formdata={'_xsrf':self.xsrf,'email': 'cyjwdm0503@foxmail.com', 'password': '4523608','remember_me':'true'},callback=self.logged_in)]

    def logged_in(self,response):
            return Request("http://www.zhihu.com/",callback=self.zhihu)

    def zhihu(self,response):
        f = open('zhihu.html','w')
        f.write(response.body)

