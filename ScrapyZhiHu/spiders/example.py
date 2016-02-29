# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.http import FormRequest
import  json
from ..items import *


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

    offset=0
    start=0

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
        return self.FormRequestNextPage(response,"https://www.zhihu.com/node/TopStory2FeedList",self.offset,self.start)


    def OutPutFile(self,filename,strlist):
        f = open(filename,'a+')
        for k in strlist:
            k = k.encode("gbk")+"\n"
          #  print k
            f.write(k)
        return


    #post 方式下一页
    def FormRequestNextPage(self,response,url,offset,start):
        print url
        self.postheader['Cookie']=response.request.headers['Cookie']
        return scrapy.FormRequest(url,formdata={'params':'{"offset":'+str(offset)+',"start":"'+str(start)+'"}',
                                         'method':'next',
                                         '_xsrf':self.xsrf},
                                  method="POST",
                                  headers=response.request.headers,
                                  callback=self.ScrapyNextIndexJson)

    def ScrapyNextIndexJson(self,s):
        res = json.loads(s.body)
        for response in res['msg']:
            #获取对应的topic_question
            topic_question = Selector(text= response).xpath('//div[@class="feed-main"]')
            topic = topic_question.xpath('//div[@class="source"]/a/text()').extract()
            question = topic_question.xpath('//div[@class="content"]/h2/a/text()').extract()
            #首页问题主题
            #topic = (Selector(text = response).xpath('//div[@class="feed-main"]/div[@class="source"]/a/text()').extract())
            sigletopic = set(topic)

            ##首页问题内容
            #question = (Selector(text=response).xpath('//div[@class="feed-main"]/div[@class="content"]/h2/a/text()').extract())
            singlequestion = set(question)
            self.OutPutFile("question.txt",sigletopic)
            self.OutPutFile("question.txt",singlequestion)


        self.start=self.start+20
        self.offset=self.start+40
        return self.FormRequestNextPage(s,"https://www.zhihu.com/node/TopStory2FeedList",self.offset,self.start)



class ZhiHuCollect(scrapy.Spider):
    name="ZhiHuCollect"
    start_urls=("https://www.zhihu.com/#signin",)
    allowed_domains=["zhihu.com"]
    xsrf=""

    reqmorefollowerparam = None
    flowerscount = 0
    maxflowerscount = 0
    def parse(self, response):
        self.xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print self.xsrf
        return  self.reqlogin()


    #请求登陆
    def reqlogin(self):
        return [scrapy.FormRequest("https://www.zhihu.com/login/email",
                                   formdata={'_xsrf':self.xsrf,
                                             'email': 'cyjwdm0503@foxmail.com',
                                             'password': '4523608',
                                             'remember_me':'true'},
                                   callback=self.rsplogin)]

    #登陆回调
    def rsplogin(self,response):
        #先获取自己的收藏在查询关注着
        #return self.reqCollections("https://www.zhihu.com/people/cyjwdm0503")
        return  self.reqfollowers("https://www.zhihu.com/people/cyjwdm0503")

    #查询第一次关注者
    def reqfollowers(self,peopleurl):
        self.initgetMoreFolloweer()
        return Request(peopleurl+"/followees",callback=self.rspflowers)


    #第一次查询关注者回调
    def rspflowers(self,response):
        #返回初始长度的关注人列表
        href_name_list = Selector(response).xpath('//a[@class="zg-link"]')
        self.flowerscount =  len(href_name_list)+self.flowerscount
        self.maxflowerscount  = Selector(response).xpath('//div[@class="zm-profile-side-following zg-clear"]/a/strong/text()').extract()[0]
        print "maxfollowers"+str(self.maxflowerscount)

        for href_name in href_name_list:
            users = ScrapyUsers()
            users['href'] =  href_name.xpath('@href').extract()
            users['name'] =  href_name.xpath('text()').extract()[0].encode('gbk')
            print users['href']
            print users['name']
            #yield  self.reqCollections(href_name.xpath('@href').extract()[0].encode('gbk'))
            #users.Save()
            #href = Selector(text=href_name).xpath('//@href').extract()
            #print href
        yield self.reqmorefollowers(response)


    #第一次调用时候的初始化更多关注者是的信息
    def initgetMoreFolloweer(self):
        self.flowerscount = 0
        self.maxflowerscount  = 0
        self.reqmorefollowerparam =  None

    #获取更多关注者
    def reqmorefollowers(self,response):
        if self.flowerscount >= self.maxflowerscount:
            return  None

        more_buf = self.getMoreFolloweer(response,self.flowerscount)
        return scrapy.FormRequest("https://www.zhihu.com/node/ProfileFolloweesListV2",
                                      formdata={'params':more_buf,
                                         'method':'next',
                                         '_xsrf':self.xsrf},
                                  method="POST",
                                  headers=response.request.headers,
                                  callback=self.rspmorefollows)

    #获取更多的关注人取到offset .hash_id
    def getMoreFolloweer(self,response,nextoffset):
        if self.reqmorefollowerparam == None:
            data_init = Selector(response).xpath('//div[@class="zh-general-list clearfix"]/@data-init').extract()[0]
            print data_init
            dc = json.loads(data_init)
            dc['params']['offset'] = nextoffset
            self.reqmorefollowerparam =  json.dumps(dc['params'])
            return self.reqmorefollowerparam
        else:
            self.reqmorefollowerparam = json.loads(self.reqmorefollowerparam)
            self.reqmorefollowerparam['offset']=nextoffset
            self.reqmorefollowerparam = json.dumps(self.reqmorefollowerparam)
            return  self.reqmorefollowerparam


    #更多关注者回调
    def rspmorefollows(self,js):
        res = json.loads(js.body)
        peopleurl = None
        for response in res['msg']:
            href_name_list = Selector(text=response).xpath('//a[@class="zg-link"]')
            self.flowerscount =  len(href_name_list)+self.flowerscount
            for href_name in href_name_list:
                users = ScrapyUsers()
                users['href'] =  href_name.xpath('@href').extract()
                users['name'] =  href_name.xpath('text()').extract()[0].encode('gbk')
                print users['href']
                print users['name']
                #查询对应people的收藏
                peopleurl = href_name.xpath('@href').extract()[0].encode('gbk')
                #yield self.reqCollections(href_name.xpath('@href').extract()[0].encode('gbk'))
                yield self.reqfollowers(peopleurl)

        if self.flowerscount < self.maxflowerscount:
            yield self.reqmorefollowers(js)

        #else:
            #申请下一次关注者回调
        #    yield self.reqmorefollowers(js)


    def reqCollections(self,peopleurl):
        collections_url = peopleurl
        return  Request(collections_url+"/collections",callback=self.rspCollections)


    def rspCollections(self,response):
        collections_list = Selector(response).xpath('//a[@class="zm-profile-fav-item-title"]')
        for collection_name in collections_list:
            collection_url =  "https://www.zhihu.com"+collection_name.xpath('@href').extract()[0]
            collection_name = collection_name.xpath('text()').extract()[0].encode('gbk')
            collections = ScrapyCollections()
            collections['user_href'] = self.getLChildUrl(  str(response.url),1)
            collections['collection_name'] = collection_name
            collections['collection_url'] = collection_url
            print collection_url, collection_name,collections['user_href']
            yield self.reqColletion(collection_url)


    #获取子字符串 endPoint 为去掉多少位"/"
    def getLChildUrl(self,url,endPoint=None):
        buffer = str(url)
        point  = len(buffer)
        currentpos = 0
        lastpos = 0
        for point in buffer:
            if point == '/' or point =='\'':
                lastpos = currentpos
            currentpos = currentpos+1

        print lastpos
        return buffer[0:lastpos]

    #查询一个收藏下面的所有问题与答案
    def reqColletion(self,collect_url):
        return Request(collect_url,callback=self.rspCollection)

    def rspCollection(self,response):
        collection_name = Selector(response).xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()[0]

        question_answers = Selector(response).xpath('//div[@class="zm-item"]').extract()
        question_href= None
        question_name = None
        for question in question_answers:
            question_answer =  Selector(text=question)
            if len(question_answer.xpath('//h2[@class="zm-item-title"]').extract()) != 0:
                question_href  = question_answer.xpath('//h2[@class="zm-item-title"]/a/@href').extract()[0]
                question_name = question_answer.xpath('//h2[@class="zm-item-title"]/a/text()').extract()[0]

            answer_user_href = None
            answer_user_name = None
            answer_user_href = question_answer.xpath('//div[@class="zm-item-answer-author-info"]/a/@href').extract()
            if len(answer_user_href) != 0:
                answer_user_href = question_answer.xpath('//div[@class="zm-item-answer-author-info"]/a/@href').extract()[0]
                answer_user_name = question_answer.xpath('//div[@class="zm-item-answer-author-info"]/a/text()').extract()[0]
            answer_href = question_answer.xpath('//div[@class="zm-item-rich-text js-collapse-body"]/@data-entry-url').extract()[0]
            answer_head = question_answer.xpath('//div[@class="zh-summary summary clearfix"]/text()').extract()
            print collection_name,answer_user_name,question_href,question_name,answer_user_href,answer_href
