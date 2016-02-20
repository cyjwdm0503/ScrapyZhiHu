# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.http import FormRequest
import  json


class Zhihu(scrapy.Spider):
    name = "ZhiHu"
    allowed_domains=["zhihu.com"]
    start_urls=("https://www.zhihu.com/#signin",)
    xsrf=""
    postheader={
        'Accept': '*/*',
        'Origin': 'https://www.zhihu.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.zhihu.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
       #$a 'Cookie':'_ga=GA1.2.1555722577.1432823794;q_c1=29afeb27dbc34d9e90e5c5c3f5d09aad|1455936022000|1455936022000; cap_id="NTk0YjU2OWQ1OWY3NGJiZTg5ZmEzZjA2YjQ4NTFkY2Q=|1455936022|337db9eac58eb8818504d9147922bdea477f2b75"; _za=8793075f-c2fc-41c0-bf94-b713f2f42180; z_c0="QUFCQUNIZ2hBQUFYQUFBQVlRSlZUUnRmNzFZWWZiWEFlVGVJbmJUaGI0NmRKMVN2cG1FLW1RPT0=|1455936027|23e4203cbd991f8e1ec756769ee4d67abf740e8f"; aliyungf_tc=AQAAAIri6mt+UQYAXRLAtzsjD2l2jYS/; __utmt=1; __utma=51854390.1555722577.1432823794.1455942772.1455943503.2; __utmb=51854390.3.9.1455952556043; __utmc=51854390; __utmz=51854390.1455942772.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20131128=1^3=entry_date=20131128=1'
    }
    #获取对应信息，进行登录
    def parse(self, response):
        self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print self.xsrf
        return  self.login()

    #请求登录
    def login(self):
        return [scrapy.FormRequest("https://www.zhihu.com/login/email",
                                   formdata={'_xsrf':self.xsrf,'email': 'cyjwdm0503@foxmail.com', 'password': '4523608','remember_me':'true'},
                                   callback=self.logged_in)]

    #登陆后操作
    def logged_in(self,response):
            return Request("http://www.zhihu.com/",callback=self.ScrapyIndex)

    #首页内容
    def ScrapyIndex(self,response):
        print response.request.headers
        f = open("source.txt",'w')
        #首页问题主题
        topic = (Selector(response).xpath('//div[@class="feed-main"]/div[@class="source"]/a/text()').extract())
        sigletopic = set(topic)


        ##首页问题内容
        question = (Selector(response).xpath('//div[@class="feed-main"]/div[@class="content"]/h2/a/text()').extract())
        singlequestion = set(question)

        self.OutPutFile("topic.txt",sigletopic)
        self.OutPutFile("question.txt",singlequestion)
        return self.FormRequestNextPage(response,"https://www.zhihu.com/node/TopStory2FeedList")


    def OutPutFile(self,filename,strlist):
        f = open(filename,'a+')
        for k in strlist:
            print k
            k = k.encode("utf8")+"\n"
            f.write(k)
        return


    #post 方式下一页
    def FormRequestNextPage(self,response,url):
        print url
        self.postheader['Cookie']=response.request.headers['Cookie']
        return scrapy.FormRequest(url,formdata={'params':'{"offset":20,"start":"20"}',
                                         'method':'next',
                                         '_xsrf':self.xsrf},
                                  method="POST",
                                  headers=response.request.headers,
                                  callback=self.ScrapyNextIndex)

    def ScrapyNextIndex(self,s):
        res = json.loads(s.body)
        for response in res['msg']:
            #获取对应的topic_question
            topic_question = Selector(text= response).xpath('//div[@class="feed-main"]')
            #首页问题主题
            topic = (Selector(text = response).xpath('//div[@class="feed-main"]/div[@class="source"]/a/text()').extract())
            sigletopic = set(topic)

            ##首页问题内容
            question = (Selector(text=response).xpath('//div[@class="feed-main"]/div[@class="content"]/h2/a/text()').extract())
            singlequestion = set(question)
            self.OutPutFile("topic.txt",sigletopic)
            self.OutPutFile("question.txt",singlequestion)