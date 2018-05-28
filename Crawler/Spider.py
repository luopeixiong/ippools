 #coding:utf-8

import sys
import json


from jsonpath import jsonpath
from Crawler.HTML_DOWNLOAD import download_many
from Dbs import redis_client
from scrapy import Selector
from .HTML_PARSE import HtmlParse
from configs import TIMEOUT
from .error import ParseError

class CrawlerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['CrawlerFunList'] = []
        count = 0
        for name, function in attrs.items():
            if name.startswith('crawler_'):
                attrs['CrawlerFunList'].append(function)
                count + 1
        attrs['CrawlerFunCount'] = count
        return type.__new__(cls, name, bases, attrs)

class Spider(HtmlParse, metaclass=CrawlerMetaclass):
    def __init__(self):
        self.redis = redis_client.OrderSetClient()

    def html_parse(self, _configs, name, timeout=TIMEOUT):
        '''
        解析配置 html页面
        '''
        for html in download_many(_configs['urls'], timeout=timeout):
            self.redis.logger.debug(html)
            for sel in Selector(text=html).xpath(_configs['pattern']):
                ip = sel.xpath(_configs['position']['ip']).extract_first()
                port = sel.xpath(_configs['position']['port']).extract_first()
                if not (ip or port):
                    raise ParseError(name)
                proxy = '%s:%s' % (ip.strip(), port.strip())
                if not self.redis.exits(proxy):
                    self.redis.add(proxy)

    def json_parse(self, _configs, name, timeout=TIMEOUT):
        '''
        解析配置 json字符串
        '''
        for html in download_many(_configs['urls'], timeout=timeout):
            self.redis.logger.debug(html)
            for sel in jsonpath(json.loads(html), _configs['pattern']):
                ip = jsonpath(sel, _configs['position']['ip'])
                port = jsonpath(sel, _configs['position']['port'])
                if not (ip or port):
                    raise ParseError(name)
                proxy = '%s:%s' % (ip[0].strip(), port[0].strip())
                if not self.redis.exits(proxy):
                    self.redis.add(proxy)

    def crawler_kuaidaili(self, page=10):
        '''
        快代理 抓取
        @return: None 
        '''
        _configs = {'urls': ['https://www.kuaidaili.com/free/inha/%(page)s/' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//div[@id="list"]//tr[td]',
                    'position': {'ip': './td[@data-title="IP"]/text()','port': './td[@data-title="PORT"]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_xici(self, page=10):
        '''
        西刺代理 抓取
        @return: None 
        '''
        _configs = {'urls': ['http://www.xicidaili.com/nn/%(page)s' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//*[@id="ip_list"]//tr[td]',
                    'position': {'ip': './td[2]/text()','port': './td[3]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_66ip(self, page=32):
        '''
        66ip 抓取
        @return: None 
        '''
        _configs = {'urls': ['http://www.66ip.cn/areaindex_%(page)s/1.html' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//tr[td[text()="ip"]]/following-sibling::tr',
                    'position': {'ip': './td[1]/text()','port': './td[2]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_data5u(self, page=1):
        '''
        无忧代理 抓取
        @return: None 
        '''
        _configs = {'urls': ['http://www.data5u.com/free/gngn/index.shtml' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//*[@class="wlist"]//ul[@class="l2"]',
                    'position': {'ip': './span[1]/li[1]/text()','port': './span[2]/li[1]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_swei360(self, page=7, timeout=15): # 此网站延迟较高
        '''
        360代理 抓取
        @return: None 
        '''
        _configs = {'urls': ['http://www.swei360.com/free/?stype=1&page=%(page)s' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//tr[td[7]]',
                    'position': {'ip': './td[1]/text()','port': './td[2]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)(), timeout)

    def crawler_ip3366(self, page=1):
        '''
        云代理 抓取
        @return: None 
        '''
        _configs = {'urls': ['http://www.ip3366.net/free/?page=1' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//*[@id="list"]//tr[td]',
                    'position': {'ip': './td[1]/text()','port': './td[2]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_cz88(self, page=1):
        '''
        纯真代理 抓取
        @return: None 
        '''
        _configs = {'urls': ['http://www.cz88.net/proxy/' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//ul/li[div[@class="ip"]][position()>1]',
                    'position': {'ip': './div[1]/text()','port': './div[2]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_mogumiao(self, page=1):
        '''
        蘑菇代理 抓取
        @return: None 
        '''
        _configs = {'urls': ['http://www.mogumiao.com/proxy/api/freeIp?count=15', 'http://www.mogumiao.com/proxy/free/listFreeIp'],
                    'pattern': '$.msg[:]',
                    'position': {'ip': '$.ip','port': '$.port'}}
        self.json_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_yqie(self, page=1):
        _configs = {'urls': ['http://ip.yqie.com/ipproxy.htm' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//div[h1[text()="国内高匿代理IP"]]//tr[td]',
                    'position': {'ip': './td[1]/text()','port': './td[2]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())

    def crawler_ihuan(self, page=10, timeout=15):
        '''
        小幻HTTP代理 抓取
        @return: None
        '''
        _configs = {'urls': ['https://ip.ihuan.me/address/5Lit5Zu9.html?page=%(page)s' % {'page':page} for page in range(1,page+1)],
                    'pattern': '//tr[td[1 and a]]',
                    'position': {'ip': './td[1]/a/text()','port': './td[2]/text()'}}
        self.html_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)(), timeout)

    def crawler_89ip(self, page=1):
        '''
        流年代理 抓取
        @return: None
        '''
        _configs = {'urls': ['http://www.89ip.cn/tiqv.php?sxb=&tqsl=30&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1'],
                    'pattern': '(\d+\.\d+\.\d+\.\d+):(\d+)',
                    'position': {'ip': 0,'port':1}}
        self.regex_parse(_configs, (lambda:sys._getframe(1).f_code.co_name)())



if __name__ == '__main__':
    Spider().crawler_kuaidaili()


    
