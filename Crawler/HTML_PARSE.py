# coding:utf-8


import re


from configs import TIMEOUT
from scrapy import Selector
from Dbs import redis_client
from .HTML_DOWNLOAD import download_many
from .error import ParseError


class HtmlParse(object):
    redis = redis_client.OrderSetClient()

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

    def regex_parse(self, _configs, name, timeout=TIMEOUT):
        '''
        解析配置 html页面
        '''
        for html in download_many(_configs['urls'], timeout=timeout):
            self.redis.logger.debug(html)
            for sel in re.compile(_configs['pattern']).findall(html):
                ip = sel[_configs['position']['ip']]
                port = sel[_configs['position']['port']]
                if not (ip or port):
                    raise ParseError(name)
                proxy = '%s:%s' % (ip.strip(), port.strip())
                if not self.redis.exits(proxy):
                    self.redis.add(proxy)

