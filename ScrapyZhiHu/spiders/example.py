# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request



class Zhihu(scrapy.Spider):
    name = "ZhiHu"
    allowed_domains=["zhihu.com"]
    start_urls=("https://www.zhihu.com/#signin",)
    xsrf=""

    #获取对应信息，进行登录
    def parse(self, response):
        self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print self.xsrf
        return  self.login()

    #请求登录
    def login(self):
        return [scrapy.FormRequest("https://www.zhihu.com/login/email",
                                   formdata={'_xsrf':self.xsrf,'email': 'cyjwdm0503@foxmail.com', 'password': '4523608','remember_me':'true'},callback=self.logged_in)]

    #登陆后操作
    def logged_in(self,response):
            return Request("http://www.zhihu.com/",callback=self.ScrapyIndex)

    #首页内容
    def ScrapyIndex(self,response):
        f = open("source.txt",'w')
        topic = (Selector(response).xpath('//div[@class="feed-main"]/div[@class="source"]/a/text()').extract())
        sigletopic = set(topic)
        for k in sigletopic:
            print k
        self.OutPutFile("topic.txt",sigletopic)


    def OutPutFile(self,filename,strlist):
        f = open(filename,'w')
        for k in strlist:
            buf = k.encode("gb2312")+"\n"
            f.write(buf)
        return